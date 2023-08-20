import requests
import json
from urllib.parse import urlsplit
from bs4 import BeautifulSoup  

import sys
sys.path.append('libs')
import L
import T
import X
import ServerUtils
import time
import random


#https://v.api.aa1.cn/api/zhihu-news/index.php?aa1=xiarou


def getvideojson1():
    url = "http://c.m.163.com/recommend/getChanListNews?channel=T1457068979049&size=5"
    response = requests.get(url)
    jsontx = response.text
    data = json.loads(jsontx)
    title,image,content = "", "", ""
        
    for news_item in data["视频"]:  
        image = news_item["cover"]  
        title = news_item["title"]
        content = getcontent(news_item["mp4_url"])

        print(content)
        
        #print( X.new_news(title,content,"Wh294594","视频",image) + "\n")
        #time.sleep(random.randint(0, 5))

    time.sleep(random.randint(10, 60))












    


def getvideojson():
    #url = 'https://v.api.aa1.cn/api/api-vs/index.php'
    #url ="https://v.api.aa1.cn/api/api-tplist/go.php/api/News/local_news?name=" + city +"&page="+str(random.randint(0, 300))
    #response = requests.get(url)
    #jsontx = response.text
    #print(jsontx)

    title = input("输入标题:")
    vdourl = input("输入视频url:")
    tu = input("输入图片:")

    print( X.new_news(title,vdourl,"Wh294594","视频",tu) + "\n")

    #https://zj.v.api.aa1.cn/api/ksjx/
    #url ="https://zj.v.api.aa1.cn/api/ksjx/"
    #rese = requests.get(url)
    #jsontext = rese.text
    #videodata = json.loads(jsontext)
    #videourl = videodata['Video_Url']
    #print( X.new_news('这是一个视频',videourl,"Wh294594","视频",tu) + "\n")



def getcontent(url):
    response = requests.get(url)  
    html_content = response.text    
    soup = BeautifulSoup(html_content, 'html.parser')   
    text = soup.get_text()  
    text = text.split('\n')[14:-5]  
    text = ''.join(text)  
    text = text.replace('\n', '<br/>')  
    return text

def getjson3(city):
    #https://v.api.aa1.cn/api/api-tplist/go.php/api/News/local_news?name=
    url ="https://v.api.aa1.cn/api/api-tplist/go.php/api/News/local_news?name=" + city +"&page="+str(random.randint(0, 300))
    response = requests.get(url)
    jsontx = response.text
    data = json.loads(jsontx)
    title,image,content = "", "", ""
        
    for news_item in data["data"]:  
        image = news_item["imgsrc"]  
        title = news_item["digest"]
        print(news_item["url"])
        content = getcontent(news_item["url"])  
        print( X.new_news(title,content,"Wh294594",city,image) + "\n")
        time.sleep(random.randint(0, 5))

    time.sleep(random.randint(10, 60))




def getjson1():
    url = "https://v.api.aa1.cn/api/zhihu-news/index.php?aa1=xiarou"  
    response = requests.get(url)  
    jsontx = response.text[:-4]
    data = json.loads(jsontx)

    title,image,content = "", "", ""  
    for news_item in data["news"]:  
        print(news_item)
        image = news_item["image"]  
        title = news_item["title"]  
        content = getcontent(news_item["url"])  
  
        print( X.new_news(title,content,"Wh294594","知乎",image) + "\n")
        


rand = ['福建省_福州市','福建省_莆田市',
        '福建省_泉州市',"福建省_宁德市" ,
        '北京市','江苏省','浙江省',"云南省",
        "黑龙江省","青海省"]
#getvideojson1()



while True:
    getvideojson()

     
#getjson3(random.choice(rand))
    
#getjson1()
#print(getcontent("https://3g.163.com/news/article/IBP4A5DV0546D0ZP.html"))
    

