import sys
import time
import os
import sqlite3
import json

sys.path.append('libs')
import L
import T
import X
import ServerUtils
from datetime import datetime  




def swap(obj1,obj2):
    return obj2, obj1







def inserthots():
    global allsize
    score=[];likesize=[];commentsize=[]
    videosize =0
    newssize = 0

    sql = sqlite3.connect(db_path) 
    cursor = sql.cursor()
    data=cursor.execute("SELECT * FROM news WHERE readnum!='0'").fetchall()
    for i in  range(0,len(data)):
        id=data[i][0]
        X.sethots(id,False)
        
        comment = cursor.execute("SELECT * FROM comment WHERE videoid==" +str(id)).fetchall()
        readnum = int(data[i][8])

        likesize.append(len(data[i][6].split(",")))
        commentsize.append(len(comment))
        
        score.append(readnum + commentsize[i] * 5 +likesize[i] * 5)
        if i ==0: continue
        if score[i] < score[i-1]:
            data[i],data[i-1] = swap(data[i],data[i-1])
            likesize[i],likesize[i-1] = swap(likesize[i],likesize[i-1])
            commentsize[i],commentsize[i-1] = swap(commentsize[i],commentsize[i-1])

    jsonArray = []
    size=[]
    
    for j in range(0,30):  
        jsonObject = {};
        row = data[j]
        
        X.sethots(row[0],True)
        jsonObject["id"] = row[0]
        jsonObject["title"] = row[1]
        jsonObject["commentsize"] = commentsize[i]
        jsonObject["readnum"] = int(row[8])
        jsonObject["likesize"] = likesize[i]
        jsonObject["score"] = score[i]
        jsonArray.append(jsonObject)

    with open('profile/top', 'w',encoding="utf-8") as f:  
        f.write(json.dumps(jsonArray,ensure_ascii=False))
        
    
    video = cursor.execute("SELECT * FROM news WHERE type=='视频'").fetchall()
    alldata = cursor.execute("SELECT * FROM news").fetchall()
    newsize = len(alldata) - len(video)
    size.append(newsize)
    size.append(len(video))
    with open('profile/percent', 'w',encoding="utf-8") as f:  
        f.write(json.dumps(size,ensure_ascii=False))


    now = datetime.now()
    weekday = now.weekday()
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']

    alljson = {};
    alljson["value"]=len(alldata)
    alljson["name"]= weekdays[weekday]

    allsize.append(alljson)

    if len(allsize) > 7:
        allsize = [x for x in allsize if x != 1]  
        
    with open('profile/trend', 'w',encoding="utf-8") as f:  
        f.write(json.dumps(allsize,ensure_ascii=False))

    
        
db_path="db/news.db"
allsize=[]
inserthots()



while True:  
    inserthots()
    time.sleep(24 * 60 * 60)



