import sqlite3
import json
import T
import ServerUtils


def vertoken(token):
    querydata = getuser(token) #通过数据库去查token对应的用户
    if not querydata:
        msg="无效oken";code=401
    elif T.vertoken(user,token) !=3: #判断token是否过期
        msg="token已过期";code=401
    else:
        msg="token有效";code=200

    data = {"msg": msg,"code": 200} 
    return json.dumps(data,ensure_ascii=False)
        

def insert(user,pw,avater):
    data = (user,pw,avater,"")
    sql = sqlite3.connect(db_path)
    cur = sql.cursor()
    sql.execute('INSERT INTO userinfo (user, pass,avater,token) VALUES (?, ?,?,?)', data)
    sql.commit()
    sql.close()

def getuser(token):
    sql = sqlite3.connect(db_path)
    data = sql.execute("select * from userinfo where token='%s'" % token).fetchone()
    sql.close()
    return data

def getpersonjson(token):
    data=getuser(token)
    jsontext={}
    if not data:
        jsontext["code"] = 500
        jsontext["name"] = "没有对象"
    elif T.vertoken(data[1],token) !=3:
        jsontext["code"] = 401
        jsontext["name"] = "权限不足"
    else:
        jsontext["code"] = 200
        jsontext["msg"]="查询成功"
        jsontext["id"] = data[0]
        jsontext["name"] = data[1]
        jsontext["img"] = data[3]
    return json.dumps(jsontext,ensure_ascii=False)
    
    


def update_avater(token,avater):
    querydata =getuser(token) #通过数据库去查token对应的用户
    if not querydata:
        msg="权限不足";code=401
    elif T.vertoken(querydata[1],token) !=3: #判断token是否过期
        msg="token已过期";code=401
    else:
        msg="修改成功";code=200
        sql = sqlite3.connect(db_path)  
        cursor = sql.cursor()  
        cursor.execute("UPDATE userinfo SET avater = ? WHERE token = ?", (avater, token))  
        sql.commit()  
        sql.close()

    data = {"msg": "修改成功","code": 200} 
    return json.dumps(data,ensure_ascii=False)
    


def update_pw(token,password):
    querydata = getuser(token) #通过数据库去查token对应的用户
    if not querydata:
        msg="权限不足";code=401
    elif T.vertoken(querydata[1],token) !=3: #判断token是否过期
        msg="token已过期";code=401
    elif len(password) < 8:
        msg="密码小于8位";code=401
    else:
        sql = sqlite3.connect(db_path)  
        cursor = sql.cursor()  
        cursor.execute("UPDATE userinfo SET pass = ? WHERE token = ?", (password, token))  
        sql.commit()  
        sql.close()

    data = {"msg": "修改成功","code": 200} 
    return json.dumps(data,ensure_ascii=False)


def update_token(user, new_token):

    sql = sqlite3.connect(db_path)  
    cursor = sql.cursor()  
    cursor.execute("UPDATE userinfo SET token = ? WHERE user = ?", (new_token, user))  
    sql.commit()  
    sql.close()
    


def query(user):
    sql = sqlite3.connect(db_path)
    data = sql.execute("select * from userinfo where user='%s'" % user).fetchone()
    sql.close()
    return data

def queryall():
    sql = sqlite3.connect(db_path)
    cursor = sql.execute('SELECT * FROM userinfo')
    data = cursor.fetchall()
    sql.close()
    return data

	



def create_sql():
    sql = sqlite3.connect(db_path)
    sql.execute("""create table if not exists
        %s(
        %s integer primary key autoincrement,
        %s varchar(128),
        %s varchar(128),
        %s varchar(128),
        %s varchar(128))"""
        % ('userinfo',
            'id',
            'user',
            'pass',
            'avater',
            'token'
           ))
    
     
    sql.close()




#前期构建的时候有点问题，导致部分口不是通过id识别用户，而是user，所以不能重名

def Login(u,p):
    userdata=query(u)
    if not userdata:
        msg="登录失败;用户不存在";code=500
    elif userdata[2]==p:
        msg="登录成功";code=200;token=T.maketoken(u)
        update_token(u,token)
    else:
        msg="登录失败，密码不正确";code=300

    if code==200:
        data = {"msg": msg,"code": code,"token":token} #死python原生库就一个json库可以处理json还这么难用 
    else:
        data = {"msg": msg,"code": code} 

    
    return  json.dumps(data)


def Logout(token):
    user = getuser(token) #通过数据库去查token对应的用户
    if not user:
        data = {"msg": "退出失败用户不存在","code": 500}
        return json.dumps(data,indent=2, ensure_ascii=False)
    else:
        update_token(user[1],"")
        data = {"msg": "退出登录成功","code": 200}
        return json.dumps(data,indent=2, ensure_ascii=False)
        



def Reg(user,pw,avater):
    msg="";code=""
    
    violations=[",",";","_","'",":",">","<"]
    for i in range(len(violations)):  
        if violations[i] in user:
             msg="违规字符";code=500
             break

    if not user or not pw:
        msg="账号或密码为空，注册失败";code=500
    elif  len(pw) < 8:
        msg="密码小于8位，注册失败";code=500
    elif not query(user):
        insert(user,pw,avater)
        msg="注册成功";code=200
    else:
        msg="用户已存在注册失败";code=500

    
        
    data = {"msg": msg,"code": code} 
    return  json.dumps(data)


db_path="db/Info.db"
create_sql()
#查询默认创建者用户是否存在
creator=query(ServerUtils.admin_id())
if not creator:
    insert(ServerUtils.admin_id(),ServerUtils.admin_token(),"/profile/admin.jpg")
    update_token(ServerUtils.admin_id(),ServerUtils.admin_token())
    
#print(getpersonjson("wh294594"))

