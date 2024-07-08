import argparse

data = []
with open("/home/fyg/Integrate-LLM-into-ASR/data/aishell2/aishell2.scp") as f:
    for line in f:
        wav,path = line.split()
        path = path.strip()
        data.append({"key":wav,"wav":path})
with open("/home/fyg/Integrate-LLM-into-ASR/data/aishell2/text") as f:
    for line in f:
        wav = line.split()[0]
        lable = line[len(wav):].strip()
        print(lable)
        for item in data:
            if item["wav"] == wav:
                print(wav)
