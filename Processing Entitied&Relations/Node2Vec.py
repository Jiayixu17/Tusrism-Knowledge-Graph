# -*- coding:utf-8 -*-
# project: 节点嵌入，随机游走
# user:徐嘉艺
# Author: Jiayi Xu
# createtime: 2022/8/25 23:05
import networkx as nx
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import axes3d
df = pd.read_csv(r"EntityExtracted\Relation_ALL.tsv",sep = "\\t")
G = nx.from_pandas_edgelist(df,"product","service",create_using=nx.Graph())

def get_randomwalk(node,path_length):
    random_walk = [node]
    for i in range(path_length-1):
        temp = list(G.neighbors(node))
        temp = list(set(temp) - set(random_walk))
        if len(temp) == 0:
            break
        random_node = random.choice(temp)
        random_walk.append(random_node)
        node = random_node
    return random_walk

all_nodes = list(G.nodes())
gamma = 10 #每个节点作为起始点生成随机游走序列个数
walk_length = 2 #随机游走序列最大长度
from tqdm import tqdm
random_walks = []
for n in tqdm(all_nodes):
    for i in range(gamma):
        random_walks.append(get_randomwalk(n,walk_length))

model = Word2Vec(vector_size=128,
                 window=2,
                 sg=1,
                 hs=0,
                 negative=10,
                 alpha=0.003,
                 min_alpha=0.0007,
                 seed=14)

model.build_vocab(random_walks,progress_per=2)
model.train(random_walks,total_examples=model.corpus_count,epochs=50,report_delay=1)
f1 = open(r"Provider_FromCtrip.csv", encoding='utf-8')
id_from_Ctrip = pd.read_csv(f1)

f2 = open(r"Provider_NotFromCtrip.csv",encoding='utf-8')
id_NotFrom_Ctrip = pd.read_csv(f2)

Ctrip_List = id_from_Ctrip['code']
NotCtrip_List = id_NotFrom_Ctrip['code']
X_Ctrip = []
X_NotCtrip = []
for i in Ctrip_List:
    try:
        X_Ctrip.append(model.wv.get_vector(i))
    except Exception as e:
        continue
len(X_Ctrip)

for j in NotCtrip_List:
    try:
        X_NotCtrip.append(model.wv.get_vector(j))
    except Exception as e:
        continue

X = model.wv.vectors
pca = PCA(n_components=3)
embed_2d = pca.fit_transform(X)

embed_2d_Ctrip = pca.fit_transform(X_Ctrip)
embed_2d_NotCtrip = pca.fit_transform(X_NotCtrip)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')  # 可进行多图绘制
# plt.scatter(embed_2d_Ctrip[:,0],embed_2d_Ctrip[:,1],c = 'r')
# plt.scatter(embed_2d_NotCtrip[:,0],embed_2d_NotCtrip[:,1],c='g')
x1 = embed_2d_Ctrip[:,0]
y1 = embed_2d_Ctrip[:,1]
z1 = embed_2d_Ctrip[:,2]
ax.scatter(x1,y1,z1,c='r')
x2 = embed_2d_NotCtrip[:,0]
y2 = embed_2d_NotCtrip[:,1]
z2 = embed_2d_NotCtrip[:,2]
ax.scatter(x2,y2,z2,c='g')
plt.show()