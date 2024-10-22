"""Extract text
Exract wav-sentence text file fom the wer file generated by wenet's tools
"""
import argparse
import os
import re
def extract_text(wer_path,output_path):
    output = []
    print(output_path)
    with open(wer_path) as f:
        count = 0
        err = False
        for line in f:
            count+=1
            if count % 6 == 2 and line[0:3] == "utt":
                wav = line
            if count % 6 == 3 and line[0:3] == "WER" and line[0:9] != "WER: 0.00":
                output.append(re.sub(" ","",wav))
                err = True
            if count % 6 == 0:
                if err == True:
                    output.append("\n")
                err = False
            if err ==  True:
                output.append(re.sub(" ","",line))
    with open(output_path,"w") as f:
        for line in output:
            f.write(line)

# def main():
#     parse = argparse.ArgumentParser()
#     parse.add_argument("--wer_path")
#     parse.add_argument("--outpub_path")
#     pass

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("path")
    args = parse.parse_args()
    print(args)
    for path,dirs,files in os.walk(args.path):
        if "wer" in files:
            print(os.path.join(path,"wer"))
            extract_text(os.path.join(path,"wer"),os.path.join(path,"wrong_sentence"))
