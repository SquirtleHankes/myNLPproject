# -*- coding: utf-8 -*-
"""
@author: 杨涛
"""

import pymysql
import os
import math
import requests
import pandas as pd
import numpy as np
import re
import jieba
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import silhouette_score, calinski_harabaz_score
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#构建词袋空间VSM(vector space model)
import matplotlib.pyplot as plt
corpus = []
db = pymysql.connect(host="127.0.0.1",database="weixin",user="root",password="yt6655050",port=3306,charset='utf8mb4')   #链接数据库
with db:
    cur = db.cursor()
    cur.execute("truncate table weixin.after_vector")
    cur.execute("SELECT * FROM train WHERE 公众号类型 LIKE '电商'")
    #cur.execute("SELECT * FROM train")
    numrows = int(cur.rowcount)
    print(numrows)
    rows = cur.fetchall()
    for i in range(numrows):
        corpus.append(rows[i][17])#存放所有文档分词结果
        insert_data = ("INSERT INTO after_vector value(" + str(i) + ",'" + str(rows[i][0]) + "')") #存放索引
        try:
            cur.execute(insert_data)
        except:
            db = pymysql.connect(host="127.0.0.1", database="weixin", user="root", password="yt6655050", port=3306,
                                 charset='utf8mb4')  # 链接数据库
            cur = db.cursor()
            cur.execute(insert_data)
        db.commit()

vectorizer = CountVectorizer(max_df=0.6, min_df=5)  # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
X = vectorizer.fit_transform(corpus)
word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
#print(word)
print(word.__len__()) #词典的长度
#print(word.__getitem__(1))#获得词典中特定位置的词
pd.DataFrame(X.toarray(), columns=word)
#print(pd.DataFrame(X.toarray(), columns=word)) #输出词频矩阵
transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值,设置当设置为浮点数时，过滤出现在超过max_df/低于min_df比例的句子中的词语；正整数时,则是超过max_df句句子。这样就可以帮助我们过滤掉出现太多的无意义词语。
tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
#print(weight.__len__())
weight_data=pd.DataFrame(weight, columns=word)


print('Start Kmeans:')
# i = []
# y_silhouette_score = []
# inertia_score = []
# calinskiharabaz_score = []
# for k in range(10,51):
#     clf = KMeans(n_clusters=k, random_state = 1,algorithm='auto', n_init=10,init='k-means++')
#     s1 = clf.fit(weight)
#     s = clf.fit_predict(weight)
#     #print(s)
#     # 中心点
#     #print(clf.cluster_centers_)
#     # 每个样本所属的簇
#     # print(clf.labels_)
#     # i = 0
#     # while i < len(clf.labels_):
#     #     print(i, clf.labels_[i])
#     #     i = i + 1
#     print(clf.inertia_)
#     silhouettescore = silhouette_score(weight, s)
#     print("silhouette_score for cluster '{}'".format(k))
#     print(silhouettescore)
#     calinskiharabazscore = calinski_harabaz_score(weight, s)
#     print("calinski_harabaz_score '{}'".format(k))
#     print(calinskiharabazscore)
#     i.append(k)
#     y_silhouette_score.append(silhouettescore)
#     inertia_score.append(clf.inertia_)
#     calinskiharabaz_score.append(calinskiharabazscore)
#     print("kmeans_model.inertia_score for cluster '{}'".format(k))

clf = KMeans(n_clusters=33, random_state = 1,algorithm='auto', n_init=10,init='k-means++')
s1 = clf.fit(weight)
s = clf.fit_predict(weight)

j=1 #选取需要输出的簇

fans=[]
wordsss=[]
print(clf.labels_[j])
#将簇内的文章输出
for i in range(len(clf.labels_)):
    if clf.labels_[i]==clf.labels_[j]:
        print(i)
        sqlword = "SELECT * FROM after_vector WHERE 列数 LIKE " + "'" + str(i) + "'"
        cur.execute(sqlword)
        rows = cur.fetchall()
        k=rows[0][1]
        sqlword = "SELECT * FROM train WHERE id LIKE " + "'" + str(k) + "'"
        cur.execute(sqlword)
        rows = cur.fetchall()

        fans_num


        print(rows[0][2])
        print(rows[0][1])
#绘制效果图，选取最合适的k值

# plt.style.use('ggplot')
#
# plt.figure(num=None, figsize=None, dpi=None, facecolor=None, edgecolor=None, frameon=False)
# plt.plot(i,y_silhouette_score)
# plt.xlabel("k")
# plt.ylabel("Silhouette Coefficient")
# plt.show()
#
# plt.figure(num=None, figsize=None, dpi=None, facecolor=None, edgecolor=None, frameon=False)
# plt.plot(i,inertia_score)
# plt.xlabel("k")
# plt.ylabel("inertia score")
# plt.show()
#
# plt.figure(num=None, figsize=None, dpi=None, facecolor=None, edgecolor=None, frameon=False)
# plt.plot(i,calinskiharabaz_score)
# plt.xlabel("k")
# plt.ylabel("Calinski-Harabaz Index")
# plt.show()
#
#
# max_indx=np.argmax(y_silhouette_score)#max value index
# min_indx=np.argmin(y_silhouette_score)#min value index
# max_indx_x=i[max_indx]
# min_indx_x=i[min_indx]
# plt.plot(i,y_silhouette_score, 'c.')
# plt.plot(max_indx_x,y_silhouette_score[max_indx],'m.')
# show_max='['+str(max_indx_x)+','+str(round(y_silhouette_score[max_indx],3))+']'
# plt.annotate(show_max,xytext=(max_indx_x,y_silhouette_score[max_indx]),xy=(max_indx_x,y_silhouette_score[max_indx]))
# plt.plot(min_indx_x,y_silhouette_score[min_indx],'g.')
# show_min='['+str(min_indx_x)+','+str(round(y_silhouette_score[min_indx],3))+']'
# plt.annotate(show_min,xytext=(min_indx_x,y_silhouette_score[min_indx]),xy=(min_indx_x,y_silhouette_score[min_indx]))
# plt.xlabel("k")
# plt.ylabel("Silhouette Coefficient")
# plt.xticks(np.arange(10,50,5))
# plt.show()
#
# max_indx=np.argmax(calinskiharabaz_score)#max value index
# min_indx=np.argmin(calinskiharabaz_score)#min value index
# max_indx_x=i[max_indx]
# min_indx_x=i[min_indx]
# plt.plot(i,calinskiharabaz_score, 'c.')
# plt.plot(max_indx_x,calinskiharabaz_score[max_indx],'m.')
# show_max='['+str(max_indx_x)+','+str(round(calinskiharabaz_score[max_indx],3))+']'
# plt.annotate(show_max,xytext=(max_indx_x,calinskiharabaz_score[max_indx]),xy=(max_indx_x,calinskiharabaz_score[max_indx]))
# plt.plot(min_indx_x,calinskiharabaz_score[min_indx],'g.')
# show_min='['+str(min_indx_x)+','+str(round(calinskiharabaz_score[min_indx],3))+']'
# plt.annotate(show_min,xytext=(min_indx_x,calinskiharabaz_score[min_indx]),xy=(min_indx_x,calinskiharabaz_score[min_indx]))
# plt.xlabel("k")
# plt.ylabel("Calinski-Harabaz Index")
# plt.xticks(np.arange(10,50,5))
# plt.show()
#
# max_indx=np.argmax(inertia_score)#max value index
# min_indx=np.argmin(inertia_score)#min value index
# max_indx_x=i[max_indx]
# min_indx_x=i[min_indx]
# plt.plot(i,inertia_score, 'c.')
# plt.plot(max_indx_x,inertia_score[max_indx],'m.')
# show_max='['+str(max_indx_x)+','+str(round(inertia_score[max_indx],3))+']'
# plt.annotate(show_max,xytext=(max_indx_x,inertia_score[max_indx]),xy=(max_indx_x,inertia_score[max_indx]))
# plt.plot(min_indx_x,inertia_score[min_indx],'g.')
# show_min='['+str(min_indx_x)+','+str(round(inertia_score[min_indx],3))+']'
# plt.annotate(show_min,xytext=(min_indx_x,inertia_score[min_indx]),xy=(min_indx_x,inertia_score[min_indx]))
# plt.xlabel("k")
# plt.ylabel("inertia score")
# plt.xticks(np.arange(10,50,5))
# plt.show()



