# -*- coding:utf-8 -*-
# project:
# user:徐嘉艺
# Author: Jiayi Xu
# createtime: 2022/3/7 17:36
import csv

import pandas as pd
import difflib
mulu= ''

#打开需要进行实体对齐的总文件
f = open(r"Data_preprocess.csv",encoding='UTF8')
df = pd.read_csv(f)
f1 = open(r"replace_Attraction.csv",encoding='UTF8')
df1 = pd.read_csv(f1)

def replace_function(entity_type,entity1,entity2):
    data = df[entity_type]
    for t in data:
        a = pd.isnull(t)
        if a == False:  # 判断空值(等于False则不是空值）
            t = t.replace(entity2,entity1) #把entity2 替换为 entity1
            return t
        else:
            return ''
data = df['Attraction']
with open(mulu_count + "Attraction_replace.csv", 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow('entity')
    for t in data:
        a = pd.isnull(t)
        if a == False:  # 判断空值(等于False则不是空值）
            for i in range(0, len(df1)):  # 遍历每一行
                pre_list = [df1.iloc[i][0],df1.iloc[i][1]]
                t = t.replace(entity2,entity1) #把entity2 替换为 entity1
# #计算相似度
# def string_similar(s1, s2):
#     return difflib.SequenceMatcher(None, s1, s2).quick_ratio()
#
#打开实体计数文件
def open_file(file):
    f = open(mulu_count+"Count"+file+".csv",encoding='UTF8')
    df = pd.read_csv(f)
    return df.iloc[:,0] #返回第一列的实体（列表）
#
#计算出目前相似性最大的实体
def max_entity(entity_list,entity,similar):
    max_similar = 0
    max_entity = '000'
    for i in range(0,len(entity_list)):
        #取出一个实体
        similar_value = string_similar(entity,entity_list[i])
        if similar_value > similar and similar_value >= max_similar and entity != entity_list[i]:
            max_entity = entity_list[i]
            max_similar = similar_value
    if max_entity == '000':
        return False
    else:
        return max_entity

# 遍历替换函数

def entity_repace(entity_type,similar):
    #取出需要进行实体对其的列
    data = df[entity_type]

    #取出名为entity_name的实体的列表
    entity_list = open_file(entity_type)
    for t in entity_list:
        judge = max_entity(entity_list,t,similar)
        if judge != False:
            if len(t) > judge:
                quit = judge
                replace_function(entity_type,t,judge)
            if len(t) <= judge:
                quit = t
                replace_function(entity_type,judge,t)   #完成了一次替换
        entity_list.remove(quit)





