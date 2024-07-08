from openai import OpenAI
import yaml
import requests
import json
from zhipuai import ZhipuAI

class chat_agent:
    def __init__(self,config):
        self.model = config["model"]
        self.api_key = config["api_key"]
        if self.model in ["ERNIE-3.5"]:
            self.serect_key = config["secret_key"]
            self.token_url = config["token_url"]
        self.base_url = config["base_url"]
        self.temperature = config["temperature"]
        self.top_p = config["top_p"]
        self.tests = config["tests"]

    def get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = self.token_url
        params = {"grant_type": "client_credentials", "client_id": self.api_key, "client_secret": self.serect_key}
        return str(requests.post(url, params=params).json().get("access_token"))


    def response(self,prompt,task)  :
        # try:
            if self.model in ["ERNIE-3.5","ERNIE 4.0"]:
                url = self.base_url + self.get_access_token()
                payload = json.dumps({
                "messages":[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": task}
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
            # elif self.model in ["glm-4","glm-3-turbo"]:
            #     client = ZhipuAI(api_key=self.api_key)
            #     answer = client.chat.completions.create(
            #     model=self.model,
            #     messages=[
            #         {"role": "system", "content": prompt},
            #         {"role": "user", "content": task}
            #     ],
            #     temperature=self.temperature,
            #     top_p=self.top_p,
            #     )
            #     return answer.choices[0].message.content
            else:
                client = OpenAI(api_key=self.api_key, base_url=self.base_url)
                answer = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": task}
                ],
                temperature=self.temperature,
                top_p=self.top_p
                )
                return answer.choices[0].message.content
        # except:
        #     print(f"[Response Error]sentence:{task}")
        #     return ""
    @staticmethod
    def extrac_response_anwser(response):
        try:
                begin_index = response.index("[",)
                end_index = response.index("]")
                return response[begin_index+1:end_index]
        except:
            # print(f"[Extrac Error]response:{response}")
            return ""
    def run(self):

        data = {}
        for test in self.tests:
            faild = 0
            success = 0
            prompt = self.tests[test]["prompt"]
            tasks = self.tests[test]["tasks"]
            results = self.tests[test]["results"]
            describe = self.tests[test]["describe"]
            print("*****"*20)
            print(test)
            print("describe:",describe)
            print("*****"*20)
            print("-----"*20)
            print(prompt)
            print("-----"*20)
            for task,result in zip(tasks,results):
                response = self.response(prompt,task)
                print(f"task:{task}")
                print(f"Response:{response}")
                print(f"Result:{result}")
                try:
                    if self.extrac_response_anwser(response) == result.strip():
                        print("Pass😊")
                        success += 1
                    else:
                        print(self.extrac_response_anwser(response))
                        print("Faild😥")
                        faild += 1
                except:
                    print("Faild😥")
                    faild += 1
                print(f"-----"*20)
            print("*****"*20)
            print(test,f"success😊:{success}",f"faild😥:{faild}")
            data[test] = { "success😊":success,"faild😥":faild}
            print("*****"*20)
        print(file)
        for item in data:
            print(item,data[item])

            

def main():

    with open(file,'r') as f:
        config = yaml.safe_load(f)
    agent = chat_agent(config)
    agent.run()
if __name__ == "__main__":
    file = "./config/test/English/gpt.yaml"
    main()