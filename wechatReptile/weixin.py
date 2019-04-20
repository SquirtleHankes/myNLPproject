# -*- coding: utf-8 -*-
"""
@author: 杨涛
"""
import pymysql
import os
import random
import threading
import time
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import Series, DataFrame
import re
import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning 
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
global db
db = pymysql.connect(host="127.0.0.1",database="weixin",user="root",password="yt6655050",port=3306,charset='utf8mb4')   #链接数据库


gzh_name="退役军人事务部"      #公众号名称，每次爬取需要手动输入
gzh_intro="发布权威信息，解读退役军人相关政策。"      #公众号介绍，手动录入

excel_url='C:/Users/win8/Desktop/公众号汇总.xlsx'
df=pd.read_excel(excel_url)

df['公众号'].astype('str')
df['类型'].astype('str')
df['排名信息'].astype('str')
#通过对收集的excel表对公众号名称和他的信息进行匹配
df1=df.loc[df['公众号'].isin([gzh_name])]
df2=df1.iloc[[0], [1]]
df3=df1.iloc[[0], [2]]
df4=df1.iloc[[0], [3]]
df5=df1.iloc[[0], [4]]
df6=df1.iloc[[0], [5]]
df2=re.split(r'\s+',str(df2))
df3=re.split(r'\s+',str(df3))
df4=re.split(r'\s+',str(df4))
df5=re.split(r'\s+',str(df5))
df6=re.split(r'\s+',str(df6))
gzh_type=str(df2).split(", '")[3].split("']")[0] #类型
gzh_rank=str(df3).split(", '")[3].split("']")[0] #排名
gzh_fans=str(df4).split(", '")[3].split("']")[0] #预估粉丝数
gzh_week=str(df5).split(", '")[3].split("']")[0] #周发文数
gzh_point=str(df6).split(", '")[3].split("']")[0] #西瓜指数


filepath='wxgzh/'+gzh_name+"/"
if not os.path.exists(filepath):
    os.mkdir(filepath)

def see():#关闭程序
    global sees
    while sees:
        try:
            db.ping()
        except:
            db = pymysql.connect(host="127.0.0.1", database="weixin", user="root", password="yt6655050", port=3306,
                                 charset='utf8mb4')  # 链接数据库
        pass
    print('cookie已失效 请重新抓包')
    db.close()
    time.sleep(2)
    os._exit(0)

def get(urls):#获取文章列表
    time.sleep(random.randint(1,3))
    r=requests.get(urls,headers=headers)
    rj=r.json()
    if rj['errmsg']=='ok':
        rjs.append(rj)#存入存放列表的list
        print('存入URL list')
    else:
        global sees  # 当被ban时关闭程序
        sees=False
      
def dojs():#解析文章列表中各个文章的url
    global j
    while True:
        try:
            rj=rjs[0]
            lis=json.loads(rj['general_msg_list'])['list']
            lils=[]
            for li in lis:
                try:
                    dt=li['comm_msg_info']['datetime']
                    lil=li['app_msg_ext_info']
                    
                    k=[lil['title'],lil['content_url'],dt]
                    lils.append(k)
                except:
                    pass
            j.extend(lils)#存入存放文章url的list
        except:
            pass
        try:
            rjs.pop(0)
        except:
            pass

def downloadimg(i,iu,typ,nam):#下载文章中的图片
    fla=True
    while fla:
        try:
                h2={
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection":"keep-alive",
    "Host":"mmbiz.qpic.cn",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
                }
                r=requests.get(iu,headers=h2,verify=False)
                with open(filepath+nam+'/'+str(i)+'.'+typ,'ab') as f:
                    f.write(r.content)
                fla=False
        except:
                pass

def getall(uu):#处理文章页面
        global numT,paras,db
        texttime=datetime.datetime.fromtimestamp(int(uu[2]))
        textday=datetime.datetime.strftime(texttime,'%Y-%m-%d')#获取文章发布时间
        texthour=datetime.datetime.strftime(texttime,'%H')
        try:
            ui = uu[1].split('mid=')[1].split('&amp')[0] #获取每篇文章的特有ID
        except:
            print(uu[1],'aha')

        cursor = db.cursor()
        try:
            cursor.execute('select count(*) from weixin1 where id='+ui)
        except:
            db = pymysql.connect(host="127.0.0.1", database="weixin", user="root", password="yt6655050", port=3306,
                                 charset='utf8')  # 链接数据库
            cursor = db.cursor()
            cursor.execute('select count(*) from weixin1 where id=' + ui)
        cursor.close()
        num=int(cursor.fetchall()[0][0])
        if num>0:
            return 0


        r=requests.get(uu[1],headers=headers,verify=False)
        #print(uu[1])
        if random.randint(0, 50) < 40:
            time.sleep(random.randint(4, 8))
        while '操作频繁，请稍后再试' in r.text:
            r=requests.get(uu[1],headers=headers,verify=False)
            time.sleep(random.randint(5,6))
        Soup=BeautifulSoup(r.text,'lxml')
        imgs=Soup.find_all('img',attrs={"data-src": True})
        i=0
        uu[0]=','.join(re.findall('\w+',uu[0]))
        tq=uu[0]
        kq=1
        while os.path.exists(filepath+uu[0]):
            uu[0]=tq+str(kq)
            kq+=1
        try:
            os.mkdir(filepath+uu[0])
        except:
            pass
        
        #获取点赞数和阅读数的url
        jsurl='https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&'+paras+'&'+'&'.join(uu[1].split('?')[1].split('&amp;')).split('#')[0]+'&abtest_cookie=&devicetype=Windows%208&version=62060028&is_need_ticket=0&is_need_ad=0&is_need_reward=0&both_ad=0&reward_uin_count=0&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&is_temp_url=0&item_show_type=0&tmp_version=1&more_read_type=0&appmsg_like_type=1'+'&appmsg_type=9'
        #print(jsurl)
        dzurl=requests.post(jsurl,headers=headers,verify=False)
        if random.randint(0, 50) < 40:
            time.sleep(random.randint(4, 8))
        rj=dzurl.json()
        print(rj['appmsgstat']['like_num'])#喜欢数
        print(rj['appmsgstat']['read_num'])#阅读数
        
        for im in imgs:
            iu=im['data-src']
            if iu!='':
                typ=iu.split('=')[-1]
                #yu=threading.Thread(target=downloadimg,args=(i,iu,typ,uu[0],))#下载图片
                #yu.start()
                im['data-src']=str(i)+'.'+typ
                im['src']=str(i)+'.'+typ
            i+=1
        img_num = i;
        html = str(Soup)
        with open(filepath+uu[0]+"/index.html", 'wb') as f:
            f.write(html.encode('utf8'))#这里只是把整个网站存下来，如果想要什么文字信息的话可以修改
        text=Soup.find(id='img-content').get_text().replace(" ","").replace("\t","")
        str_read = str(rj['appmsgstat']['read_num'])
        str_like = str(rj['appmsgstat']['like_num'])
        str_img = str(img_num)
        str_texttime = str(texttime)
        #with open(filepath+uu[0]+"/"+str_read+" "+str_like+" "+str_img+" "+str_texttime+".txt", 'w',encoding='utf8') as f:
        #    f.write(text)
        #print(uu[1])
        cursor = db.cursor()
        insert_data = ("INSERT INTO weixin1 value('" + ui + "','" + uu[0] + "','" + gzh_name + "','" + text.replace("'","").replace("\\", "").replace('"',"") + "'," + str_read + "," + str_like + ",'" + textday + "','" + texthour + "'," + str_img + ",'" + gzh_type + "','" + gzh_rank + "'," + gzh_fans + "," + gzh_week + "," + gzh_point + ",'" + gzh_intro + "')")
        try:
            cursor.execute(insert_data)
        except:
            db = pymysql.connect(host="127.0.0.1", database="weixin", user="root", password="yt6655050", port=3306,
                                 charset='utf8mb4')  # 链接数据库
            cursor = db.cursor()
            cursor.execute(insert_data)
        db.commit()
        if numT>100:
            global sees  # 当爬到100时关闭程序
            sees = False
        numT+=1
        print(numT)
        print(uu[0])
        if  numT%5==0:
            print('开始休息')
            time.sleep(10)

def gettext():#从文章url的list中取出元素进行处理
    global j
    ps=[]
    while True:
        try:
            time.sleep(5)
            p=threading.Thread(target=getall,args=(j[0],))
            p.start()
            ps.append(p)
            if len(ps)%20==0:
                for p in ps:
                    p.join()
                ps=[]
            j.pop(0)
        except:
            pass
if __name__ == '__main__':
    global j,rjs
    j=[]
    headers={
"Host":"mp.weixin.qq.com",
"Connection":"keep-alive",
"Accept":"*/*",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400",
"X-Requested-With":"XMLHttpRequest",
#"Referer":" https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI0Mjc2NDc2OQ==&scene=124&uin=OTQwNjU3NTQx&key=df104bdfc549579e440a81f0d0289354a5c6988fbe4c10251f779f662e40b099f3614085e6a3ee882d705f64779199adf1299d05c0da5a0470db93fdf35c7eb213857cd6514fbbe8cdbd1b653e5a111f&devicetype=Windows+8&version=62060028&lang=zh_CN&a8scene=7&pass_ticket=p1BdK%2BLTIgRwhjAuarMA%2FHWP4R18E0A6aIupK78KlVXmKpisCOWUD5d2aPoF1lku&winzoom=1",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4",

#用fiddler中的cookie替换下条
"Cookie":"rewardsn=; wxtokenkey=777; wxuin=542829443; devicetype=Windows8; version=62060739; lang=zh_CN; pass_ticket=vGl95Gqpwyu8mSMtpgkWd3KlFCgum1uz38gZU1RNd0kfXf8wTXLg8P8T6dY3JKyW; wap_sid2=CIPX64ICEogBRWJnTF9mdVR6YnlvUU1KOWxuLVNud3p3VVlzaWhrMmJDTzRCYS1RT0ZRenZSdXFwNkVJNEYtQloyM0JZUkNxamFMMkMzUTNWT0VPS3JjdElGWVpJdzgyYk1KVE56cHpXaTgwTXk2aWlDa1ZkejVSNVBtSUstWllKUnpwOVR5ei03QU1BQUF+fjCAisLlBTgNQJVO"
}
    url='http://mp.weixin.qq.com'

    #fiddler中的第一行替换下条
    hist="/mp/profile_ext?action=getmsg&__biz=MzU0NDkyMzYwNw==&f=json&offset=20&count=10&is_ok=1&scene=124&uin=NTQyODI5NDQz&key=f6869c76f8fd06b86e127fe65bee3d785073ca6354c97e8e2b799ca892c99f3240e47470ad114b587e87a055d280176dc9ee41e59d920a6ff4352addb94ee39dd636992ce8a3cbf988add79d05ee217d&pass_ticket=vGl95Gqpwyu8mSMtpgkWd3KlFCgum1uz38gZU1RNd0kfXf8wTXLg8P8T6dY3JKyW&wxtoken=&appmsg_token=1004_VocIirQ6Nc2OeL%252FiJsFsWwGbUepRD1be28APBA~~&x5=0&f=json HTTP/1.1"
    hist=re.sub('(?<=offset=)\d+','{start}',hist)
    global paras
    paras='&'.join(hist.split('&')[7:]).replace(' HTTP/1.1','')
    kkk=threading.Thread(target=dojs)#开启解析列表的进程
    qqq=threading.Thread(target=gettext)#开启解析文章的进程
    eee=threading.Thread(target=see)#开启当cookie失效时的进程
    kkk.start()
    qqq.start()
    global sees
    sees=True
    eee.start()
    rjs=[]
    print('开始爬取')
    global numT
    numT = 0
    for i in range(50):
        urls=url+hist.format(start=str(i*10))
        get(urls)#获取文章列表
        if random.randint(0,50)<40:
            time.sleep(random.randint(3,5))
    while len(j)>0:
        pass
    