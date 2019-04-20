# -*- coding: utf-8 -*-
"""
@author: 杨涛
"""

import pymysql
import os
import math
import requests
import pandas as pd
import jieba
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



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


f = open('C:/Users/win8/Desktop/1111stop.txt','r', encoding='utf-8')
stopword=f.read()


db = pymysql.connect(host="127.0.0.1",database="weixin",user="root",password="yt6655050",port=3306,charset='utf8mb4')   #链接数据库
with db:
    #对整体语料库的统计
    cur = db.cursor()
    # cur.execute("SELECT * FROM weixin1 WHERE 公众号名称 LIKE '电子商务头条'")
    #cur.execute("truncate table weixin.after_cut")
    cur.execute("SELECT * FROM weixin1")
    numrows = int(cur.rowcount)
    print(numrows)
    rows = cur.fetchall()
    r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>"关闭""微信""赞赏""二维码""公众""号""苹果公司""转账""赞赏""别忘了""支持""猜""喜欢""评论""留言""影响""版""功能"?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'#用户也可以在此进行自定义过滤字符
    r2 = u'\s+;'
    total_read=0
    total_like=0
    for i in range(numrows):
        total_read += rows[i][4]
        total_like += rows[i][5]
    average_read = total_read/numrows #计算平均阅读
    average_like = total_like/numrows #计算平均喜欢
    print(total_read)
    print(total_like)
    print(average_read)
    print(average_like)
    print(average_read/average_like)

    excel_url = 'C:/Users/win8/Desktop/已爬取公众号汇总 - 副本.xlsx'
    df=pd.read_excel(excel_url)

    # 分别对每个公众号进行统计
    for g in range(0,140):   #在这里输入需要处理的公众号数量
        gzh=df.iloc[[g], [0]]
        gzh = re.split(r'\s+', str(gzh))
        gzh=str(gzh).split(", '")[3].split("']")[0]
        print(gzh)
        cur = db.cursor()
        sqlword="SELECT * FROM weixin1 WHERE 公众号名称 LIKE "+"'"+gzh+"'"
        print(sqlword)
        cur.execute(sqlword)
        numrows = int(cur.rowcount)
        print(numrows)
        rows = cur.fetchall()

        min_read=rows[0][4]
        max_read=0
        min_like=rows[0][5]
        max_like=0
        for i in range(numrows):
            if min_read >= rows[i][4]:
                min_read = rows[i][4]
            if max_read <= rows[i][4]:
                max_read = rows[i][4]
            if min_like >= rows[i][5]:
                min_like = rows[i][5]
            if max_like <= rows[i][5]:
                max_like = rows[i][5]
        print(min_read, max_read, min_like, max_like)
        for i in range(numrows):
            if rows[i][4]*rows[i][5]!=0:     #判断二者非零
                #分词，去停用词，去噪声词
                tem=re.sub(r1, '', rows[i][1])#过滤标题中的所有英文数字和符号
                tem = cut_word(tem)
                tem = del_stop_words(tem, stopword)
                tem1=re.sub(r1, '', rows[i][3]) #过滤文本中的所有英文数字和符号
                tem1 = cut_word(tem1)
                tem1 = del_stop_words(tem1, stopword)

                # 计算评分
                if (max_like - min_like)==0 or (max_read - min_read)==0:
                    inner_like_point=2
                    inner_read_point=2
                else:
                    inner_like_point = (rows[i][5] - min_like) / (max_like - min_like) + 1  # 在公众号内部进行标准化
                    inner_read_point = (rows[i][4] - min_read) / (max_read - min_read) + 1
                ratio_like_read = 30.209  #通过计算语料库获得的一般喜欢数与阅读数的比值
                ratio_like_point = (rows[i][5]/rows[i][4])+1 # 对喜欢数与阅读数的比值加一后取平方
                ratio_like_point = ratio_like_point*ratio_like_point #取平方
                read_point= rows[i][4]**0.5
                like_point = (rows[i][5] * ratio_like_read)**0.5
                final_point = ratio_like_point*((inner_like_point*like_point)+(inner_read_point*read_point))

                #cur.execute("INSERT INTO after_cut(Id,文章名称,公众号名称,文章内容,阅读数,点赞数,发文日期,发文时间,图片数,公众号类型,公众号排名,预估粉丝数,周发文数,西瓜指数,公众号备注) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (rows[i][0],tem, rows[i][2], tem1, rows[i][4], rows[i][5], rows[i][6], rows[i][7], rows[i][8], rows[i][9], rows[i][10], rows[i][11], rows[i][12], rows[i][13], rows[i][14]))
                insert_data = ("INSERT INTO after_cut value('" + rows[i][0] + "','" + rows[i][1] + "', '" + rows[i][2] + "', '" + rows[i][3] + "', " + str(rows[i][4]) + "," + str(rows[i][5]) + ", '" + rows[i][6] + "','" + rows[i][7] + "', " + str(rows[i][8]) + ", '" + rows[i][9] + "', '" + rows[i][10] + "', " + str(rows[i][11]) + ", " + str(rows[i][12]) + ", " + str(rows[i][13]) + ", '" + rows[i][14] + "'," + str(final_point) + ",'" + ','.join(tem) + "', '" + ','.join(tem1) + "')")
                try:
                    cur.execute(insert_data)
                except:
                    db = pymysql.connect(host="127.0.0.1", database="weixin", user="root", password="yt6655050", port=3306,
                                         charset='utf8mb4')  # 链接数据库
                    cur = db.cursor()
                    cur.execute(insert_data)
                db.commit()

