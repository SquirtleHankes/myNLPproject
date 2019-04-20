import pymysql
import os
import math
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import heapq

#在这里划分测试集和训练集

db = pymysql.connect(host="127.0.0.1",database="weixin",user="root",password="yt6655050",port=3306,charset='utf8mb4')   #链接数据库
with db:
    #导入语料库
    cur = db.cursor()
    #cur.execute("truncate table weixin.train")
    # cur.execute("SELECT * FROM after_cut WHERE 公众号名称 LIKE '牛气电商'")
    cur.execute("SELECT * FROM after_cut  WHERE 公众号类型 LIKE '军事'")
    numrows = int(cur.rowcount)
    print(numrows)
    rows = cur.fetchall()
    k = 250  #250篇评分最高的
    output = []
    for i in range(numrows):
        if len(output) < k:
            output.append(rows[i][15])
        else:
            output = heapq.nlargest(k, output)
            if rows[i][15] <= output[0]:
                continue
            else:
                output[0] = rows[i][15]

    print(output.__len__())
    output=set(output)
    print(output.__len__())
    for i in range(numrows):
        if rows[i][15] in output:
            r = ''.join(rows[i][17].split('\r\n'))
            insert_data = ("INSERT INTO train value('" + rows[i][0] + "','" + rows[i][1] + "', '" + rows[i][
                        2] + "', '" + rows[i][3] + "', " + str(rows[i][4]) + "," + str(rows[i][5]) + ", '" + rows[i][
                                       6] + "','" + rows[i][7] + "', " + str(rows[i][8]) + ", '" + rows[i][9] + "', '" +
                                   rows[i][10] + "', " + str(rows[i][11]) + ", " + str(rows[i][12]) + ", " + str(
                                rows[i][13]) + ", '" + rows[i][14] + "'," + str(rows[i][15]) + ",'" + rows[i][16] + "', '" + r + "')")
            try:
                cur.execute(insert_data)
            except:
                db = pymysql.connect(host="127.0.0.1", database="weixin", user="root", password="yt6655050",port=3306,charset='utf8mb4')  # 链接数据库
                cur = db.cursor()
                cur.execute(insert_data)
            db.commit()

# f = open("data/train.txt", 'a')
    # excel_url = 'C:/Users/win8/Desktop/已爬取公众号汇总 - 副本.xlsx'
    # df = pd.read_excel(excel_url)
    #
    # # 分别对每个公众号进行统计
    # for g in range(0, 101):  # 在这里输入需要处理的公众号数量
    #     gzh = df.iloc[[g], [0]]
    #     gzh = re.split(r'\s+', str(gzh))
    #     gzh = str(gzh).split(", '")[3].split("']")[0]
    #     print(gzh)
    #     cur = db.cursor()
    #     sqlword = "SELECT * FROM weixin1 WHERE 公众号名称 LIKE " + "'" + gzh + "'"
    #     print(sqlword)
    #     cur.execute(sqlword)
    #     numrows = int(cur.rowcount) #公众号内的文章数
    #     print(numrows)
    #     rows = cur.fetchall()


        # for i in range(numrows):
        #         insert_data = ("INSERT INTO temp value('" + rows[i][0] + "','" + rows[i][1] + "', '" + rows[i][
        #             2] + "', '" + rows[i][3] + "', " + str(rows[i][4]) + "," + str(rows[i][5]) + ", '" + rows[i][
        #                            6] + "','" + rows[i][7] + "', " + str(rows[i][8]) + ", '" + rows[i][9] + "', '" +
        #                        rows[i][10] + "', " + str(rows[i][11]) + ", " + str(rows[i][12]) + ", " + str(
        #                     rows[i][13]) + ", '" + rows[i][14] + "'," + str(rows[i][15]) + ",'" + rows[i][16] + "', '" + rows[i][17] + "')")
        #         try:
        #             cur.execute(insert_data)
        #         except:
        #             db = pymysql.connect(host="127.0.0.1", database="weixin", user="root", password="yt6655050",
        #                                  port=3306,
        #                                  charset='utf8mb4')  # 链接数据库
        #             cur = db.cursor()
        #             cur.execute(insert_data)
        #         db.commit()
