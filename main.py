from openai import OpenAI
import os
import time
import yaml
import threading
import random
from concurrent.futures import ThreadPoolExecutor
import requests
import json
from zhipuai import ZhipuAI
from openai import AzureOpenAI
import re
class chat_agent:
    def __init__(self,config):
        self.model = config["model"]
        self.api_key = config["api_key"]
        self.provider = config["provider"]
        match(self.provider):
            case "baidu":
                self.serect_key = config["secret_key"]
                self.token_url = config["token_url"]
            case "azure" | "Azure":
                self.api_version = config["api_version"]
        self.split_word = config["split_word"]
        self.base_url = config["base_url"]
        self.temperature = config["temperature"]
        self.thread_num = config["thread_num"]
        self.shuffle = config["shuffle"]
        self.top_p = config["top_p"]
        self.prompt = config["prompt"]
        self.max_repeat_times = config["max_repeat_times"]
        self.path = config["path"]
        self.text = config["text"]
        self.combination_num = config["combination_num"]
        self.filter = config["filter"]
        self.filter_wav = []
        if self.filter["filterscp"] != None:
            with open(self.filter["filterscp"],"r") as f:
                for line in f:
                    self.filter_wav.append(line.split()[0])
        self.substitue = config["substitue"]
        self.format = config["format"]

    def get_access_token(self):
        url = self.token_url
        params = {"grant_type": "client_credentials", "client_id": self.api_key, "client_secret": self.serect_key}
        return str(requests.post(url, params=params).json().get("access_token"))


    def response(self,prompt,task)  :
        match(self.provider):
            case "baidu":
                url = self.base_url + self.get_access_token()
                payload = json.dumps({
                "messages":[
                    # {"role": "system", "content": prompt},
                    {"role": "user", "content": prompt+'\n'+task}
                ],
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "penalty_score": 1,
                    "disable_search": False,
                    "enable_citation": False,
                    "response_format": "text"
                })
                headers = {
                    'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                data = response.json()
                result = data.get("result", "No text found in response.")
                return result
        # openai,deepseek,dashscope,
            case "zhipuai":
                client = ZhipuAI(api_key=self.api_key)
                answer = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": task}
                ],
                temperature=self.temperature,
                top_p=self.top_p,
                )
                return answer.choices[0].message.content
            case "azure":
                client = AzureOpenAI(
                    api_key=self.api_key,
                    api_version=self.api_version,
                    azure_endpoint = self.base_url
                    )
                response = client.chat.completions.create(
                        model=self.model, 
                        messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": task}
                ],
                temperature=self.temperature,
                top_p=self.top_p,)
                return response.choices[0].message.content
            case _:
                client = OpenAI(api_key=self.api_key, base_url=self.base_url)
                answer = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": task}
                ],
                temperature=self.temperature,
                top_p=self.top_p,
                )
                return answer.choices[0].message.content
    def extract_model_task(self,path):
        lines = []
        with open(path,"r") as f:
            for line in f:
                lines.append(line)
        if  self.shuffle == True:
            random.shuffle(lines)
        for line in lines:
            wav = line.split(" ")[0]
            self.wavs.append(wav)
            self.sentences.append(line[len(wav):-1])
    def extrac_response_anwser(self,num,response):
        answers = []
        diff_tags = []
        strs = f"(\{self.format['flag_symbol'][0]}.*?\{self.format['flag_symbol'][1]}\{self.format['output_symbol'][0]}.*?\{self.format['output_symbol'][1]})"
        extract_response  = re.findall(strs,response)
        for item in extract_response:
            strs = f"\{self.format['flag_symbol'][0]}(.*?)\{self.format['flag_symbol'][1]}\{self.format['output_symbol'][0]}(.*?)\{self.format['output_symbol'][1]}"
            m = re.search(strs,item)
            diff_tag,answer = m.groups()
            print(diff_tag,answer)
            # answer = re.sub(r'[，。、；：？！“”‘’『』【】《》（）\[\]{}<>,·.!?"\'-*]+',"",answer)
            answers.append(answer)
            diff_tags.append(diff_tag)
        if len(answers) != num:
            print(diff_tags,answers)
            assert(0)
        return answers,diff_tags


    def thread_response_function(self,tasks):
        diffs = []
        task = ""
        for wav,sentence in tasks:
            task +=self.split_word+sentence.strip()+"\n"
        response = ""
        answers = []
        try:
            response = self.response(self.prompt,task)
            answers,diff_tags = self.extrac_response_anwser(len(tasks),response)
        except:
            print(response)
            self.repeat_task.append(tasks)
            self.errs.append([tasks,response])
            print("error",len(tasks),len(answers),len(diffs))
            return False
        assert(len(tasks) == len(answers))
        for (wav,sentence),answer,tag in zip(tasks,answers,diff_tags):
            if tag == self.format["changed_flag"]:
                diffs.append(f"{sentence.strip()}->{answer}")
            else:
                diffs.append(None)
        # save info
        self.responses.append(task+response)
        for (wav,sentence),answer,diff,tag in zip(tasks,answers,diffs,diff_tags):
            if tag == self.format["changed_flag"]:
                self.infos.append({"wav":wav,"sentence":sentence,"answer":self.substitue_func(answer),"diff":diff})
            elif tag == self.format["keep_flag"]:
                self.infos.append({"wav":wav,"sentence":sentence,"answer":sentence,"diff":diff})
            else:
                print(tag)
                print("Tag wrong")
        print("success",len(self.infos))
        return True
    def filter_func(self,wav,sentence):
        if self.filter["flag"] == False:
            return True
        for item in self.filter["keyword"]:
            if item in sentence:
                return False
        if wav in self.filter_wav:
            return False
        return True
    def substitue_func(self,sentence:str):
        if self.substitue["flag"] == False:
            return sentence
        for item in self.substitue["keyword"]:
            sentence = sentence.replace(item,self.substitue["keyword"][item])
        return sentence
    def run(self,config):
        result_path = str(time.asctime())
        for task_name in self.path:
            self.start_time = time.time()
            self.infos = []
            self.wavs = []
            self.sentences = []
            self.responses = []
            self.errs = []
            self.extract_model_task(self.path[task_name])
            self.repeat_task = []
            tasks = []
            self.skips = []
            filter_num = 0
            with ThreadPoolExecutor(max_workers=self.thread_num) as executor:
                for wav,sentence in zip(self.wavs,self.sentences):
                    if self.filter_func(wav,sentence):
                        print("True",sentence)
                        tasks.append([wav,sentence])
                        if len(tasks) % self.combination_num == 0:
                            # self.thread_response_function(tasks)
                            executor.submit(self.thread_response_function,tasks)
                            tasks = []
                    else:
                        self.skips.append([wav,sentence])
                        filter_num += 1
                        self.infos.append({"wav":wav,"sentence":sentence,"answer":sentence,"diff":None})
                        print(f"False:",sentence)
                    
                executor.submit(self.thread_response_function,tasks)
            repeat_times = 0
            while( (len(self.repeat_task) != 0) and (repeat_times < self.max_repeat_times )):
                repeat_times += 1
                with ThreadPoolExecutor(max_workers=self.thread_num) as executor:
                    print("repeat_task",len(self.repeat_task),"success sentence",len(self.infos))
                    while(len(self.repeat_task) != 0 ):
                        tasks = self.repeat_task.pop(0)
                        executor.submit(self.thread_response_function,tasks)
            print(f"time comsume:{time.time() - self.start_time:.2f} s")
            print(f"sentence num:{len(self.infos)}")
            os.makedirs(f"result/{result_path}/{task_name}",exist_ok=True)
            with open(f"result/{result_path}/{task_name}/text","w") as f:
                for info in self.infos:
                    f.write(info["wav"]+" "+info["answer"]+"\n")
                for tasks in self.repeat_task:
                    for wav,sentence in tasks:
                        f.write(wav+" "+sentence.strip()+"\n")
            with open(f"result/{result_path}/{task_name}/diff","w") as f:
                for info in self.infos:
                    if info["diff"]!= None:
                        f.write(info["diff"]+"\n")
            with open(f"result/{result_path}/{task_name}/response","w") as f:
                for response in self.responses:
                    f.write(response+"\n*************************\n")
            with open(f"result/{result_path}/{task_name}/err","w") as f:
                for err in self.errs:
                    f.write(str(err)+"\n")
            with open(f"result/{result_path}/{task_name}/skips","w") as f:
                for skip in self.skips:
                    f.write(skip[0]+" "+skip[1]+"\n")
            with open(f"result/{result_path}/{task_name}/config","w") as f:
                yaml.safe_dump(config,f,encoding="utf-8",allow_unicode=True)
            with open(f"result/{result_path}/{task_name}/total","w") as f:
                f.write(f"time comsume:{time.time() - self.start_time:.2f} s\n")
                f.write(f"sentence num:{len(self.infos)}\n")
                f.write(f"sentence num:{filter_num}\n")
                f.write(f"success sentecne: {len(self.infos)-filter_num}\n")
                f.write(f"error tasks {len(self.repeat_task)}\n")
                for tasks in self.repeat_task:
                    for wav,sentence in tasks:
                        f.write(wav+" "+sentence.strip()+"\n")
            os.system(f"python ./tools/compute-wer.py --char=1 --v=1 '{self.text}' 'result/{result_path}/{task_name}/text' > 'result/{result_path}/{task_name}/wer' ")
            os.system(f"python ./tools/extrac_err_from_wer.py  'result/{result_path}/{task_name}/' ")
        
def main():
    with open("/home/fyg/Integrate-LLM-into-ASR/config/aishell1/gpt_u2_conformer.yaml",'r') as f:
        config = yaml.safe_load(f)
    agent = chat_agent(config)
    agent.run(config)
if __name__ == "__main__":
    main()