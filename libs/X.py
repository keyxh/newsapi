import sqlite3
import json
from datetime import datetime
from urllib.parse import unquote
import T 
import L
import urllib


#插入
#时间 标题 正文 时间 用户id号 用户头像 类型,封面图片
def insert(title,content,userid,avater,tp,cover):
    now = datetime.now()  
    nowstr = now.strftime("%Y-%m-%d %H:%M:%S")
    data = (title,content,nowstr,userid,avater,"",cover,"0",tp,"0")
    sql = sqlite3.connect(db_path)
    cursor = sql.cursor()
    sql.execute('INSERT INTO news (title,content,createTime,userid,avater,likearray,cover,hot,type,readnum) VALUES (?,?,?,?,?,?,?,?,?,?)', data)
    sql.commit()

    cursor.execute('SELECT last_insert_rowid()')
    lastId = cursor.fetchone()[0] 
    sql.close()
    return lastId




#随机从数据库获取视频
def getvideo():
    sql = sqlite3.connect(db_path) 
    cursor = sql.cursor()
    cursor.execute("SELECT * FROM news WHERE type='视频' ORDER BY RANDOM() LIMIT 1;")  
    data = cursor.fetchone()
    if not data:
        data = {"msg": "暂无数据","code": 500} 
        return json.dumps(data,ensure_ascii=False)

    readnum = int(data[8]) +1
    cursor.execute("UPDATE news SET readnum = ? WHERE id = ?", (str(readnum),data[0]))
    sql.commit()
    sql.close()

    jsonObject = {};jsontext={}
    jsonObject["id"] = data[0]
    jsonObject["title"] = data[1]
    jsonObject["content"] = data[2]
    jsonObject["createTime"] = data[3]
    jsonObject["userid"] = data[4]
    jsonObject["avater"] = data[5]
    jsonObject["likearray"] = data[6]
    jsonObject["cover"] = data[7]
    jsonObject["readnum"] = readnum
    jsonObject["hot"] = data[9]
    jsonObject["type"] = data[10]
    jsontext["code"]=200;jsontext["msg"]="操作成功";jsontext["row"]=jsonObject
    return json.dumps(jsontext,ensure_ascii=False)




    


    
#前期刚学写的查询...，本来想的给后面调用
def query(pagenum,pagesize):
    mincount = int(pagenum) * 20
    maxcount = mincount  + int(pagesize)
    sql = sqlite3.connect(db_path)
    data = sql.execute("SELECT * FROM news where type != '视频' And id >"+
                       str(mincount)+" And id <="+str(maxcount)  ).fetchall()            
    sql.close()
    return data



def searchtitle(title):
    sqline = "title LIKE '" + title + "%' or content LIKE '" + title + "%' or userid Like  '" + title + "%'"
    return search(sqline)
    


#获取热门新闻
def gethots():
    jsontext={}
    sql = sqlite3.connect(db_path)
    cursor = sql.cursor()  
    data = sql.execute("select * from news where hot='%s'" % "1").fetchall()
    if not data:
        jsontext["code"]=500;jsontext["msg"]="查询失败"
        return json.dumps(jsontext,ensure_ascii=False)


def getlikelists(token): #sql创建的有问题，正常点赞和评论都要要存成一个表。。。。如果用户量大尽量别用这个口吧
    jsonArray = [];jsontext={}
    sql = sqlite3.connect(db_path)
    user=""
    userid=""
    querydata = L.getuser(token)
    if not querydata:
        data = {"msg": "权限不足","code": 401} 
        return json.dumps(data, ensure_ascii=False)
    if T.vertoken(user,token) !=3: #判断token是否过期
        data = {"msg": "token已过期","code": 401} 
        return json.dumps(data,ensure_ascii=False)
    
    user=querydata[1]
    userid=querydata[0]
    data = sql.execute("SELECT * FROM news where likearray LIKE '" + str(userid) + ",%'" ).fetchall()
    
    
    for row in data:
        likearray = row[6].split(",")
        
        for i in range(0,len(likearray) -1):
            if likearray[i]==str(userid):   
                jsonObject = {};
                jsonObject["id"] = row[0]
                jsonObject["title"] = row[1]
                jsonObject["createTime"] = row[3]
                jsonObject["userid"] = row[4]
                jsonObject["avater"] = row[5]
                jsonObject["cover"] = row[7]
                jsonObject["hot"] = row[9]
                jsonArray.append(jsonObject)
                continue
        
            
    jsontext["code"]=200;jsontext["msg"]="操作成功";jsontext["row"]=jsonArray
    return json.dumps(jsontext,ensure_ascii=False)


        
def getpush(token):
    user=""
    querydata = L.getuser(token)
    if not querydata:
        data = {"msg": "权限不足","code": 401} 
        return json.dumps(data, ensure_ascii=False)
    if T.vertoken(user,token) !=3: #判断token是否过期
        data = {"msg": "token已过期","code": 401} 
        return json.dumps(data,ensure_ascii=False)
    
    user=querydata[1]
    return search("userid = " + "'" + user +"'")


def sethots(id,ishot):
    sql = sqlite3.connect(db_path)  
    cursor = sql.cursor()  
    if(ishot):
        cursor.execute("UPDATE news SET hot = ? WHERE id = ?", ("1",str(id)))  
    else:
        cursor.execute("UPDATE news SET hot = ? WHERE id = ?", ("0",str(id)))
        
    sql.commit()  
    sql.close()
    


#搜索
def search(condition):
    jsonArray = [];jsontext={}
    sql = sqlite3.connect(db_path)
    data = sql.execute("SELECT * FROM news where " + condition).fetchall()
    sql.close()

    if not data:
        data = {"msg": "无结果","code": 500} 
        return json.dumps(data, ensure_ascii=False)

    for row in data:
        jsonObject = {};
        jsonObject["id"] = row[0]
        jsonObject["title"] = row[1]
        jsonObject["createTime"] = row[3]
        jsonObject["userid"] = row[4]
        jsonObject["avater"] = row[5]
        jsonObject["cover"] = row[7]
        jsonObject["hot"] = row[9]
        jsonArray.append(jsonObject)
        
    jsontext["code"]=200;jsontext["msg"]="操作成功";jsontext["row"]=jsonArray
    return json.dumps(jsontext,ensure_ascii=False)









def create_sql():
    sql = sqlite3.connect(db_path)
    sql.execute("""create table if not exists
        %s(
        %s integer primary key autoincrement,
        %s varchar(128),
        %s varchar(128),
        %s varchar(128),
        %s varchar(128),
        %s varchar(128),
        %s varchar(128),
        %s varchar(128),
        %s varchar(128),
        %s varchar(128),
        %s varchar(128))"""
        % ('news',
            'id',
            'title',
            'content',
            'createTime',
            'userid',
            'avater',
            'likearray',
            'cover',
            'readnum',
            'hot',
            'type'
           ))


    #  id 用户id 头像  视频评论 视频id  子id    时间   点赞数
    # id userid avater comment videoid subid createTime likesize
    sql.execute("""create table if not exists
        %s(
        %s integer primary key autoincrement,
        %s varchar(128),
        %s varchar(128),
        %s varchar(128),
        %s varchar(128),
        %s varchar(128),
        %s varchar(128))"""
        % ('comment',
            'id',
            'userid',
            'avater',
            'comment',
            'videoid',
            'subid',
            'createTime'
           ))

    

    sql.close()




def querysubid(subid):
    jsonArray = [];jsontext={}
    sql = sqlite3.connect(db_path)
    cursor = sql.cursor()   
    data = sql.execute("SELECT * FROM comment where subid == '"+ subid +"'" ).fetchall()

    for row in data:
        jsonObject = {};
        jsonObject["id"] = row[0]
        jsonObject["userid"] = row[1]
        jsonObject["avater"] = row[2]
        jsonObject["comment"] = row[3]
        jsonObject["videoid"] = row[4]
        jsonObject["subid"] = row[5]
        jsonObject["createTime"] = row[6]
        jsonArray.append(jsonObject)
        
    jsontext["code"]=200;jsontext["msg"]="操作成功";jsontext["row"]=jsonArray
    return json.dumps(jsontext,ensure_ascii=False)




#查询评论
def querycomment(videoid):
    jsonArray = [];jsontext={}
    sql = sqlite3.connect(db_path)
    cursor = sql.cursor()   
    data = sql.execute("SELECT * FROM comment where subid == '-1' And videoid=='" + videoid + "'").fetchall() 
    for row in data:
        jsonObject = {};
        jsonObject["id"] = row[0]
        jsonObject["userid"] = row[1]
        jsonObject["avater"] = row[2]
        jsonObject["comment"] = row[3]
        jsonObject["videoid"] = row[4]
        jsonObject["subid"] = row[5]
        jsonObject["createTime"] = row[6]
        jsonArray.append(jsonObject)
        

    jsontext["code"]=200;jsontext["msg"]="操作成功";jsontext["row"]=jsonArray
    



    return json.dumps(jsontext,ensure_ascii=False)




#新建回复
def createcomment(token,comment,videoid,subid = "-1"):
    querydata = L.getuser(token) #通过数据库去查token对应的用户
    user = L.getuser(token)
    if not querydata:
        data = {"msg": "权限不足","code": 401} 
        return json.dumps(data, ensure_ascii=False)
    if T.vertoken(user,token) !=3: #判断token是否过期
        data = {"msg": "token已过期","code": 401} 
        return json.dumps(data,ensure_ascii=False)
    user=unquote(querydata[1])
    img=unquote(querydata[3])

    now = datetime.now()  
    nowstr = now.strftime("%Y-%m-%d %H:%M:%S")
    sql = sqlite3.connect(db_path)
    cursor = sql.cursor()

    if not comment or not videoid:
        data = {"msg": "存在空数据，可能是没填","code": 500} 
        return json.dumps(data, ensure_ascii=False)
    

    data = (user,img,comment,videoid,subid,nowstr)
    sql.execute('INSERT INTO comment (userid,avater,comment,videoid,subid,createTime) VALUES (?,?,?,?,?,?)', data)
    sql.commit()

    cursor.execute('SELECT last_insert_rowid()')
    lastId = cursor.fetchone()[0] 


    if subid == "-1":
        data = sql.execute("select * from comment where id='%s'" % videoid).fetchone()
        if data:
            writenotification(data[4],user + "评论了你" ,videoid)
    else:
        data = sql.execute("select * from comment where subid='%s'" % subid).fetchone()
        if data:
            writenotification(user,data[1] + "评论了你" ,videoid)

    
    sql.close()
    data = {"msg": "发布成功","id":lastId ,"code": 200}
    return json.dumps(data,ensure_ascii=False)





    




    
#获取文章详情
def newscontent(id):
    jsontext={}
    sql = sqlite3.connect(db_path)
    cursor = sql.cursor()  
    data = sql.execute("select * from news where id='%s'" % id).fetchone()
    if not data:
        jsontext["code"]=500;jsontext["msg"]="ID不存在"
        return json.dumps(jsontext,ensure_ascii=False)

    readnum = int(data[8]) +1
    cursor.execute("UPDATE news SET readnum = ? WHERE id = ?", (str(readnum),id))
    sql.commit()  
    sql.close()
    
    
    #加入数据
    jsonObject = {};jsontext={}
    jsonObject["id"] = data[0]
    jsonObject["title"] = data[1]
    jsonObject["content"] = data[2]
    jsonObject["createTime"] = data[3]
    jsonObject["userid"] = data[4]
    jsonObject["avater"] = data[5]
    jsonObject["likearray"] = data[6]
    jsonObject["readnum"] = data[8]
    jsonObject["cover"] = data[7]
    jsonObject["hot"] = data[9]
    jsonObject["type"] = data[10]
    jsontext["code"]=200;jsontext["msg"]="操作成功";jsontext["row"]=jsonObject
    return json.dumps(jsontext,ensure_ascii=False)


    

    

#根据pagenum和pagesize生成json
def newsList(pagenum,pagesize):
    jsonArray = [];jsontext={}
    data= query(pagenum,pagesize)
    for row in data:
        jsonObject = {};
        jsonObject["id"] = row[0]
        jsonObject["title"] = row[1]
        jsonObject["createTime"] = row[3]
        jsonObject["userid"] = row[4]
        jsonObject["avater"] = row[5]
        jsonObject["cover"] = row[7]
        jsonObject["hot"] = row[9]
        jsonArray.append(jsonObject)

    jsontext["code"]=200;jsontext["msg"]="操作成功";jsontext["row"]=jsonArray
    return json.dumps(jsontext,ensure_ascii=False)
    


        
#给文章视频点赞,这个位置和取消点赞调用有误，能正常用，但是输出的是id
def like(id,token):
    sql = sqlite3.connect(db_path)  
    cursor = sql.cursor()
    user = L.getuser(token)
    jsontext={}
    if not user:
        jsontext["code"]=401;jsontext["msg"]="权限不足"
        return json.dumps(jsontext,ensure_ascii=False)

    if T.vertoken(user,token) !=3: #判断token是否过期
        data = {"msg": "token已过期","code": 401} 
        return json.dumps(data,ensure_ascii=False)
    
    data = sql.execute("select * from news where id='%s'" % id).fetchone()

    likearr=data[6]
    if str(user[0]) in likearr:
        data = {"msg": "用户已点赞","code": 500} 
        return json.dumps(data,ensure_ascii=False)
    
    likearr=likearr+str(user[0]) +","  #sqlite里没有数组...，要么用新表, 仅限用户量<10w
    cursor.execute("UPDATE news SET likearray = ? WHERE id = ?", (likearr,id))  
    sql.commit()  
    sql.close()
    data = {"msg": "点赞成功","code": 200} 
    return json.dumps(data,ensure_ascii=False)


#给文章/视频取消点赞
def unlike(id,token):
    jsontext={}
    sql = sqlite3.connect(db_path)  
    cursor = sql.cursor()
    user = L.getuser(token)

    if not user:
        jsontext["code"]=401;jsontext["msg"]="权限不足"
        return json.dumps(jsontext,ensure_ascii=False)

    if T.vertoken(user,token) !=3: #判断token是否过期
        data = {"msg": "token已过期","code": 401} 
        return json.dumps(data,ensure_ascii=False)

    data = sql.execute("select * from news where id='%s'" % id).fetchone()
    likearr=data[6]
    
    if str(user[0]) in likearr:
        likearr = likearr.replace(str(user[0])+",","")
        cursor.execute("UPDATE news SET likearray = ? WHERE id = ?", (likearr,id))  
        sql.commit()  
        data = {"msg": "取消点赞成功","code": 200} 
        return json.dumps(data,ensure_ascii=False)
    else:
        data = {"msg": "取消点赞失败","code": 500} 
        return json.dumps(data,ensure_ascii=False)


    sql.close()
    


#创建新视频
def new_news(title,content,token,tp,cover):
    user="";img=""
    if not title or not content:
        data = {"msg": "标题和正文均不能为空","code": 500} 
        return json.dumps(data, ensure_ascii=False)
        
    querydata = L.getuser(token) #通过数据库去查token对应的用户
    if not querydata:
        data = {"msg": "权限不足","code": 401} 
        return json.dumps(data, ensure_ascii=False)
    if T.vertoken(user,token) !=3: #判断token是否过期
        data = {"msg": "token已过期","code": 401} 
        return json.dumps(data,ensure_ascii=False)

    #查询用户所有信息,获取头像
    user=querydata[1]
    img=querydata[3]
    news_id = insert(title,content,user,img,tp,cover)
    data = {"msg": "发布成功","id":news_id ,"code": 200} 
    return json.dumps(data,ensure_ascii=False)

    
    #评论记录模块最好再多个表，这里为了快速写，选择文件的方式
def writenotification(user,comment,id):
    pass #函数有问题，暂时不使用
    #with open(unquote("notification/" + id),"a+",encoding="utf-8") as file:
     #   file.write(unquote(comment + ";;;"  +user +"\n"))
        



db_path="db/news.db"
create_sql()
#print(createcomment("Wh294594","你好1","1"))
#print(createcomment("Wh294594","你是谁1","1","1"))
#print(querysubid("1"))
#print(querycomment("1"))

#get_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjY2IiwiZXhwIjoxNjkyMTA5MjUxfQ.RJpxWW7yNFxg_WE0daHV2uUx0DUgMVsc7Sp7K8Gl3UI"
#print(new_news("今天是什么情况","今天",get_token,"知乎",""))
#print(like(2,"wh294594"))
#print(like("2","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzIiwiZXhwIjoxNjkyMTA1NzcxfQ.gvZcZvt-pee_htfPtShcrfnn065K1ulDzHSdT6ni0Tk"))
#print(newscontent("11"))
