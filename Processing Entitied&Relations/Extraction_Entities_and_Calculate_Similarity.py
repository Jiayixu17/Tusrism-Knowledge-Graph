# -*- coding:utf-8 -*-
# project: 基于供应商维度的每月产品相似度计算（把抽取过程和计算放在一起）
# user:徐嘉艺
# Author: Jiayi Xu
# createtime: 2022/5/7 15:28
import csv
import pandas as pd
import numpy as np
import time
#文本原文件
r = '波士顿文本数据-跟团游.csv' #NER之后的文本数据
provider_road = '塞班岛供应商.txt' #所有供应商的名称文件

#保存路径
save_road = '' #保存目录
name = '纽约_跟团游' #城市名（也可以不定义）

#读取文本文件
f = open(r,encoding='ANSI')
df = pd.read_csv(f)

def read_txt(r):
    # 读取所有的行数，并按列输出
    SaveList = []  # 存档列表
    # 读取文本内容到列表
    with open(r, "r", encoding='utf-8') as file:
        for line in file:
            line = line.strip('\n')  # 删除换行符
            SaveList.append(line)
        file.close()
    return SaveList

mulu = "" #保存提取之后的实体与关系
accom = read_txt(mulu+'Accom.txt')
accom_dz = read_txt(mulu+'Accom_对照.txt')
attraction = read_txt(mulu+'attraction.txt')
food = read_txt(mulu+'food.txt')
shopping = read_txt(mulu+'shopping.txt')
service = read_txt(mulu+'service.txt')
entertainment = read_txt(mulu+'entertainment.txt')
attraction_dz = read_txt(mulu+'attraction_对照.txt')
food_dz = read_txt(mulu+'food_对照.txt')
shopping_dz = read_txt(mulu+'shopping_对照.txt')
service_dz = read_txt(mulu+'service_对照.txt')
entertainment_dz = read_txt(mulu+'entertainment_对照.txt')
city = read_txt(mulu+'city.txt')
city_dz = read_txt(mulu+'city_对照.txt')


with open(save_road+name+'实体抽取'+'.csv','w',newline='',encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['date','ProviderFullName','Text','City','Accommodation','food','attraction','shopping','service','entertainment'])
    provider_list = []
    dt_list=[]
    n = 0
    for providername in df['ProviderFullName']:
        provider_list.append(providername)
    for dt in df['date']:
        dt_list.append(dt)
    for text in df['Text']:
        accom_list = []
        food_list = []
        attraction_list = []
        shopping_list = []
        service_list = []
        entertainment_list = []
        city_list =[]

        for a in range(0,len(accom)):
            if accom[a] in text:
                accom_list.append(accom_dz[a])
        for a in range(0,len(food)):
            if food[a] in text:
                food_list.append(food_dz[a])
        for a in range(0,len(attraction)):
            if attraction[a] in text:
                attraction_list.append(attraction_dz[a])
        for a in range(0,len(shopping)):
            if shopping[a] in text:
                shopping_list.append(shopping_dz[a])

        for a in range(0,len(service)):
            if service[a] in text:
                service_list.append(service_dz[a])

        for a in range(0,len(entertainment)):
            if entertainment[a] in text:
                entertainment_list.append(entertainment_dz[a])

        for a in range(0,len(city)):
            if city[a] in text:
                city_list.append(city_dz[a])

        accom_list = list(set(accom_list))
        food_list = list(set(food_list))
        attraction_list = list(set(attraction_list))
        shopping_list = list(set(shopping_list))
        service_list = list(set(service_list))
        entertainment_list = list(set(entertainment_list))
        city_list = list(set(city_list))

        writer.writerow([dt_list[n],provider_list[n],text,";".join(city_list),";".join(accom_list),";".join(food_list),";".join(attraction_list),";".join(shopping_list),";".join(service_list),";".join(entertainment_list)])
        n += 1


#提取供应商
file = open(provider_road, encoding='UTF-8')
file_data = file.readlines() #读取所有行
company_list=[]
for row in file_data:
    company_list.append(row[:-1])
print("公司列表:",company_list)

time.sleep(2)


#读取抽取出来的文件
f1 = open(save_road+name+'实体抽取'+'.csv',encoding='utf-8')
df1 = pd.read_csv(f1)
xiecheng = '上海携程国际旅行社有限公司'

#提出总实体
def extraction_entity(d):
    dict_entity = []
    for i in df1[d]:
        i = str(i)
        if ';' in i:
            a = i.split(";")
            for j in a:
                if j in dict_entity:
                    continue
                else:
                    dict_entity.append(j)
        else:
            if i != 0:
                if i in dict_entity:
                    continue
                else:
                    dict_entity.append(i)
            else:
                continue
    print(dict_entity)
    return dict_entity

#每个公司、每个维度、每个时间下 [向量]
def xjy(c,d,t):
    all_entity = extraction_entity(d)
    c_dict = {}
    for k in all_entity:
        c_dict[k] = 0
    df_c = df1[(df1['ProviderFullName']==c)&(df1['date']==t)] #选出来c公司在t时间内所有行
    df_c_d = df_c[d] #选出来d维度的列
    for entity in all_entity:
        n = 0
        for p in df_c_d:
            p = str(p)
            if entity in p:
                n += 1
            else:
                continue
        c_dict[entity] = n

    a2 = [v for k, v in c_dict.items()]
    return a2

#c公司在t时间下，d维度与携程的相似度
def similarity(c,d,t):
    xc = xjy(xiecheng,d,t)
    c_ = xjy(c,d,t)
    vec1 = np.array(xc)
    vec2 = np.array(c_)
    cos_sim = vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return cos_sim

with open(save_road+name+'_供应商每月相似度2ddd.csv','w',newline='',encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    year = ['2017','2018']
    writer.writerow(['时间','公司','City','Accommodation','food','attraction','shopping','service','entertainment'])
    for y in year:
        for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
            time = str(y) + '年' + month +'月'+'01'+"日"
            for com in company_list:
                l = []
                for d in ['City','Accommodation','food','attraction','shopping','service','entertainment']:
                    l.append(similarity(com,d,time))
                #writer.writerow([time]+[com]+l)
                print([time]+[com]+l)