import pymysql
import os
import math
import requests
import pandas as pd
import jieba
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
        f.write("\n")                 #换行