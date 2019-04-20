# coding=utf-8

import pymysql
import os
import math
import requests
import pandas as pd
import jieba
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import silhouette_score, calinski_harabaz_score
from sqlalchemy import create_engine
from sklearn.cluster import KMeans

def cut_word(words):   #分词
    result = jieba.cut(words,cut_all=False)  #使用精确模式
    new_words = []
    for r in result:
        new_words.append(r)
    return new_words

def del_stop_words(words,stop_words_set):
#   words是已经切词但是没有去除停用词的文档。
#   返回的会是去除停用词后的文档
    new_words = []
    for r in words:
        if r not in stop_words_set:
            new_words.append(r)
    return new_words

f1 = open('C:/Users/win8/Desktop/1111stop.txt','r', encoding='utf-8')
stopword=f1.read()

str1 = input("请输入文章内容：")
print("你输入的内容是: ", str1)

db = pymysql.connect(host="127.0.0.1",database="weixin",user="root",password="yt6655050",port=3306,charset='utf8mb4')   #链接数据库
with db:
    cur = db.cursor()
    # cur.execute("truncate table weixin.train")
    # cur.execute("SELECT * FROM after_cut WHERE 公众号名称 LIKE '牛气电商'")
    # cur.execute("SELECT * FROM after_cut  WHERE 公众号类型 LIKE '零售'")
    cur.execute("SELECT * FROM train")
    numrows = int(cur.rowcount)
    print(numrows)
    rows = cur.fetchall()
    #写入训练集数据
    f = open('C:/Users/win8/PycharmProjects/textmining/test.txt', 'w',encoding='utf-8')
    for i in range(numrows):
        r=''.join(rows[i][17].split('\r\n'))
        f.write(rows[i][9]+'\t'+r)
        f.write("\n")#换行
    r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>"关闭""微信""赞赏""二维码""公众""号""苹果公司""转账""赞赏""别忘了""支持""猜""喜欢""评论""留言""影响""版""功能"?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'#用户也可以在此进行自定义过滤字符
    r2 = u'\s+;'
    tem1 = re.sub(r1, '', str1)  # 过滤文本中的所有英文数字和符号
    tem1 = cut_word(tem1)
    tem1 = del_stop_words(tem1, stopword)
    tem2 = ','.join(tem1)
    text_content=str(tem2)
    fans_num = 547468  # 输入公众号粉丝数
    ddd = ''.join(text_content.split('\r\n'))
    f.write("未分类" + '\t' + ddd)
    f.write("\n")

train_df = pd.read_csv('C:/Users/win8/PycharmProjects/textmining/test.txt', sep='\t', header=None, )
print(train_df.shape)
train_df = train_df.astype(str)
print(train_df.shape)

train_df.columns = ['分类', '文章']
stopword_list = [k.strip() for k in open('C:/Users/win8/PycharmProjects/textmining/venv/1111stop.txt', encoding='utf8').readlines() if k.strip() != '']
cutWords_list = []
i = 0
startTime = time.time()
for article in train_df['文章']:
    cutWords = [k for k in jieba.cut(article) if k not in stopword_list]
    i += 1
    if i % 1000 == 0:
        print('前%d篇文章分词共花费%.2f秒' %(i, time.time()-startTime))
    cutWords_list.append(cutWords)
print(i)
with open('C:/Users/win8/PycharmProjects/textmining/venv/cutWords_list.txt', 'w',encoding='utf-8') as file:
    for cutWords in cutWords_list:
        file.write(' '.join(cutWords) + '\n')
with open('C:/Users/win8/PycharmProjects/textmining/venv/cutWords_list.txt',encoding='utf-8') as file:
    cutWords_list = [k.split() for k in file.readlines()]


tfidf = TfidfVectorizer(cutWords_list, min_df=10, max_df=0.6)
X = tfidf.fit_transform(train_df['文章'])
print(X.shape)

train_df = pd.read_csv('C:/Users/win8/PycharmProjects/textmining/test.txt', sep='\t', header=None)
train_df = train_df.astype(str)
labelEncoder = LabelEncoder()
y = labelEncoder.fit_transform(train_df[0].values)

#降维
from sklearn.feature_selection import SelectKBest,chi2
X=SelectKBest(chi2,k=500).fit_transform(X,y)

X1=X[2006]

#划分训练测试集
from sklearn.model_selection import train_test_split
train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.2)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=9,min_samples_split=3)
model.fit(train_x, train_y)

predict = model.predict(X1)

for i in range(len(y)):
    if predict == y[i]:
        print(train_df[0].values[i])
        corpus = []
        db = pymysql.connect(host="127.0.0.1", database="weixin", user="root", password="yt6655050", port=3306,
                             charset='utf8mb4')  # 链接数据库
        with db:
            cur = db.cursor()
            leixing = str(train_df[0].values[i])
            sqlword = "SELECT * FROM train WHERE 公众号类型 LIKE " + "'" + leixing + "'"
            cur.execute("truncate table weixin.after_vector")
            cur.execute(sqlword)
            numrows = int(cur.rowcount)
            print(numrows)
            rows = cur.fetchall()
            for i in range(numrows):
                corpus.append(rows[i][17])  # 存放所有文档分词结果
                insert_data = ("INSERT INTO after_vector value(" + str(i) + ",'" + str(rows[i][0]) + "')")  # 存放索引
                try:
                    cur.execute(insert_data)
                except:
                    db = pymysql.connect(host="127.0.0.1", database="weixin", user="root", password="yt6655050",
                                         port=3306,
                                         charset='utf8mb4')  # 链接数据库
                    cur = db.cursor()
                    cur.execute(insert_data)
                db.commit()
            #插入预测目标
            corpus.append(text_content)
            i=250
            id=1234567
            insert_data = ("INSERT INTO after_vector value(" + str(i) + ",'" + str(id) + "')")  # 存放索引
            try:
                cur.execute(insert_data)
            except:
                db = pymysql.connect(host="127.0.0.1", database="weixin", user="root", password="yt6655050",
                                     port=3306,
                                     charset='utf8mb4')  # 链接数据库
                cur = db.cursor()
                cur.execute(insert_data)
            db.commit()

        vectorizer = CountVectorizer(max_df=0.6, min_df=5)  # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
        X = vectorizer.fit_transform(corpus)
        word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
        # print(word)
        print(word.__len__())  # 词典的长度
        # print(word.__getitem__(1))#获得词典中特定位置的词
        pd.DataFrame(X.toarray(), columns=word)
        # print(pd.DataFrame(X.toarray(), columns=word)) #输出词频矩阵
        transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值,设置当设置为浮点数时，过滤出现在超过max_df/低于min_df比例的句子中的词语；正整数时,则是超过max_df句句子。这样就可以帮助我们过滤掉出现太多的无意义词语。
        tfidf = transformer.fit_transform(
            vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
        weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
        # print(weight.__len__())
        weight_data = pd.DataFrame(weight, columns=word)

        print('Start Kmeans:')

        clf = KMeans(n_clusters=33, random_state=1, algorithm='auto', n_init=10, init='k-means++')
        s1 = clf.fit(weight)
        s = clf.fit_predict(weight)

        j = 1  # 选取需要输出的簇
        print(clf.labels_[j])
        # 将簇内的文章输出
        for i in range(len(clf.labels_)):
            if clf.labels_[i] == clf.labels_[j]:
                print(i)
                sqlword = "SELECT * FROM after_vector WHERE 列数 LIKE " + "'" + str(i) + "'"
                cur.execute(sqlword)
                rows = cur.fetchall()
                k = rows[0][1]
                sqlword = "SELECT * FROM train WHERE id LIKE " + "'" + str(k) + "'"
                cur.execute(sqlword)
                rows = cur.fetchall()
                print(rows[0][2])
                print(rows[0][1])
        break