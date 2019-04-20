import os
import math
import pymysql
import requests
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import heapq

#这段程序用于统计语料库中各种数值

db = pymysql.connect(host="127.0.0.1",database="weixin",user="root",password="yt6655050",port=3306,charset='utf8mb4')   #链接数据库
with db:
    cur = db.cursor()
    # cur.execute("truncate table weixin.train")
    # cur.execute("SELECT * FROM after_cut WHERE 公众号名称 LIKE '牛气电商'")
    cur.execute("SELECT * FROM after_cut  WHERE 公众号类型 LIKE '零售'")
    #cur.execute("SELECT * FROM after_cut")
    numrows = int(cur.rowcount)
    print(numrows)
    rows = cur.fetchall()
    total1=0
    for i in range(numrows):
        total1+=rows[i][4]
    b = total1 / numrows
    print(b)
    total=0
    for i in range(numrows):
        total+=rows[i][11]
    a=total/numrows
    print(a)


#这段代码用于挑选最终测试系统的文章

# db = pymysql.connect(host="127.0.0.1",database="weixin",user="root",password="yt6655050",port=3306,charset='utf8mb4')   #链接数据库
# with db:
#     #导入语料库
#     cur = db.cursor()
#     #cur.execute("truncate table weixin.train")
#     # cur.execute("SELECT * FROM after_cut WHERE 公众号名称 LIKE '牛气电商'")
#     cur.execute("SELECT * FROM after_cut  WHERE 公众号类型 LIKE '互联网'")
#     numrows = int(cur.rowcount)
#     print(numrows)
#     rows = cur.fetchall()
#     k = 251  #250篇评分最高的
#     output = []
#     for i in range(numrows):
#         if len(output) < k:
#             output.append(rows[i][15])
#         else:
#             output = heapq.nlargest(k, output)
#             if rows[i][15] <= output[0]:
#                 continue
#             else:
#                 output[0] = rows[i][15]
#
#     print(output.__len__())
#     output=set(output)
#     print(output.__len__())
#     output = heapq.nlargest(k, output)
#     print(output[250])
#     for i in range(numrows):
#         if rows[i][15]==output[250]:
#             for j in range(18):
#                print(rows[i][j])