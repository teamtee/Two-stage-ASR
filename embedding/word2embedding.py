from num2words import num2words
import os
import time
import pandas as pd
import numpy as np
import tiktoken
from openai import AzureOpenAI
from concurrent.futures import ThreadPoolExecutor
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
import argparse

parse = argparse.ArgumentParser()
parse.add_argument("diff_path")
parse.add_argument("two_stage_path")
parse.add_argument("label_path")
args = parse.parse_args()

client = AzureOpenAI(
  api_key = "",  
  api_version = "",
  azure_endpoint = ""
)

def generate_embeddings(text, model="text"): # model = "deployment_name"
    print(text)
    return client.embeddings.create(input = [text], model=model).data[0].embedding
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
original_sentence,changed_sentence = [],[]
with open(args.diff_path,"r") as f:
    for line in f:
        original,changed = line.split("->")
        changed = changed.strip()
        if original != changed:
            original_sentence.append(original)
            changed_sentence.append(changed)
changed_wav = []
for changed in changed_sentence:
    with open(args.two_stage_path,"r") as f:
        for line in f:
            wav= line.split()[0]
            sentence = line[len(wav):-1].strip()
            if sentence == changed:
                changed_wav.append(wav)
                break
label_sentence = []
for changedwav in changed_wav:
    with open(args.label_path,"r") as f:
        for line in f:
            wav= line.split()[0]
            sentence = line[len(wav):-1].strip()
            if wav == changedwav:
                label_sentence.append(sentence)
                break

with ThreadPoolExecutor(max_workers=10) as executor:
  future = [ executor.submit(generate_embeddings,i) for i in original_sentence]  
original_embedding = [ i.result() for i in future]
with ThreadPoolExecutor(max_workers=10) as executor:
  future = [ executor.submit(generate_embeddings,i) for i in changed_sentence]  
changed_embedding = [ i.result() for i in future]
with ThreadPoolExecutor(max_workers=10) as executor:
  future = [ executor.submit(generate_embeddings,i) for i in label_sentence]  
label_embedding = [ i.result() for i in future]

original_embedding = np.array(original_embedding)
changed_embedding = np.array(changed_embedding)
label_embedding = np.array(label_embedding)
time_name = time.asctime()
os.mkdir(f"./embedding/{time_name}")
np.savetxt(f"./embedding/{time_name}/orginal_embedding",original_embedding)
np.savetxt(f"./embedding/{time_name}/changed_embedding",changed_embedding)
np.savetxt(f"./embedding/{time_name}/label_embedding",label_embedding)
embedding = np.concatenate([original_embedding ,changed_embedding,label_embedding])
pca = PCA(n_components=2)
X_pca = pca.fit_transform(embedding)

fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(x=X_pca[:len(original_embedding)-1, 0], y=X_pca[:len(original_embedding)-1, 1])
ax.scatter(x=X_pca[len(original_embedding):len(original_embedding)+len(changed_embedding)-1, 0], y=X_pca[len(original_embedding):len(original_embedding)+len(changed_embedding)-1, 1])
ax.scatter(x=X_pca[len(original_embedding)+len(changed_embedding):, 0], y=X_pca[len(original_embedding)+len(changed_embedding):, 1])
ax.set_title("PCA visualization of sentence embedding")
ax.legend(["ASR","Two-stage","Label"])
# ax.legend(["Two-stage","label"])
# ax.title("t-SNE visualization of Custom Classification dataset")
# ax.set_xlabel("First t-SNE")
# ax.xaxis_title("First t-SNE")
# ax.yaxis_title("Second t-SNE")
plt.savefig(f"./embedding/{time_name}/example.png")

original_sum = np.sum(original_embedding,axis=0)
changed_sum = np.sum(changed_embedding,axis=0)
label_sum = np.sum(label_embedding,axis=0)
with open(f"./embedding/{time_name}/total.txt",'w') as f:
    f.write(args.diff_path+"\n")
    f.write(args.two_stage_path+"\n")
    f.write(args.label_path+"\n")
    f.write("orginal cosine:"+str(cosine_similarity(original_sum , label_sum))+"\n")
    f.write("changed cosine:"+str(cosine_similarity(changed_sum , label_sum))+"\n")