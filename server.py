
import json
import http.server
import urllib
import os
from urllib import parse
from datetime import datetime
from http import HTTPStatus
from socketserver import ThreadingTCPServer  
from http.server import BaseHTTPRequestHandler, HTTPServer  
from urllib.parse import parse_qs
from urllib.parse import unquote

import sys
sys.path.append('libs')
import L
import T
import X
import ServerUtils








class RequestHandlerImpl(http.server.BaseHTTPRequestHandler):
    import random
    import os
    import datetime

    

    def do_GET(self):
        get_str=""
        get_cmd=self.requestline[5:self.requestline.find("HTTP/1.1")]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        get_str=checkget(unquote(get_cmd),self.headers)
        if not get_str:
            with open('download.html', 'r',encoding='utf-8') as f:
                get_str=f.read()

        self.wfile.write(get_str.encode("utf-8"))
        
                         
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()  
        if  "upload" in self.path:
            self.wfile.write("上传文件在5000端口".encode("utf-8")) 
        else:
            req_body = self.rfile.read(int(self.headers["Content-Length"])).decode()
            get_str=checkpost(unquote(self.path),unquote(req_body),self.headers)
            self.wfile.write(get_str.encode("utf-8"))
            self.end_headers()









def checkget(get_cmd="",head=""):
    #不再客户端执行sqlie语句
    token =  head.get("Authorization") #获取头里的token
    get_cmd = unquote(get_cmd)
    if get_cmd[0:len("gettime")]=="gettime":
        now = datetime.now()  
        nowstr = now.strftime("%Y-%m-%d %H:%M:%S")
        return nowstr
    
    elif get_cmd[0:len("randomvideo")]=="randomvideo":
        return X.getvideo()

    elif get_cmd[0:len("news/pushlist")]=="news/pushlist":
        return unquote(X.getpush(token))



    elif get_cmd[0:len("personlist")]=="personlist":
        return unquote(L.getpersonjson(token))

    elif get_cmd[0:len("news/search?text=")]=="news/search?text=":
        return unquote(X.searchtitle(get_cmd[len("news/search?text="):].replace(" ","")))
    

    

    elif get_cmd[0:len("news/list?")]=="news/list?":
        
        text = get_cmd[len("news/list?"):].split("&")
        pagenum, pagesize = "0", "20"  
        for i in text:
            if "pagenum=" in i: pagenum = i[len("pagenum="):]  
            elif "pagesize=" in i: pagesize = i[len("pagesize="):].replace(' ', '')

        return X.newsList(pagenum,pagesize)

    elif get_cmd[0:len("news/likelist")]=="news/likelist":
        return X.getlikelists(token) 


        
    
    elif get_cmd[0:len("news/content?id=")]=="news/content?id=":
        return X.newscontent(get_cmd[len("news/content?id="):])
    
    elif get_cmd[0:len("news/like?id=")]=="news/like?id=":
        response=json.loads(X.like(get_cmd[len("news/like?id="):],token), strict=False)
        return json.dumps(response, indent=2, ensure_ascii=False)

    elif get_cmd[0:len("news/comment/get?id=")]=="news/comment/get?id=":
        return unquote(X.querycomment(get_cmd[len("news/comment/get?id="):].replace(" ","")))
    

    elif get_cmd[0:len("news/comment/getsub?id=")]=="news/comment/getsub?id=":
        return unquote(X.querysubid(get_cmd[len("news/comment/getsub?id="):].replace(" ","")))

    

    elif get_cmd[0:len("news/unlike?id=")]=="news/unlike?id=":
        return X.unlike(get_cmd[len("news/unlike?id="):].replace(" ",""),token)

    elif get_cmd[0:len("news/banner")]=="news/banner":
        return X.search("type=='知乎'")
    
    elif get_cmd[0:len("news/hot")]=="news/hot":
        return X.search("hot=='1'")

    elif get_cmd[0:len("vertoken")]=="vertoken":
        return L.vertoken(token)

    elif get_cmd[0:len("news/type=")]=="news/type=":
        parts = get_cmd.split('=')
        return X.search("type='" + parts[1].replace(" ","") +"' ORDER BY RANDOM() LIMIT 10;")
    
    
    elif get_cmd[0:len("news/search=")]=="news/search=":
        parts = get_cmd.split('=')
        return X.searchtitle(parts[1].replace(" ",""))
   

    else:
        pass



        
        

def checkpost(path,post_str,head=""):
    token =  head.get("Authorization") #获取头里的token
    if path=="/login":
        text = post_str.split("&")
        username, password, avater = "", "", ""  
        for i in text:  
            if "username=" in i: username = i[len("username="):].replace(' ', '')   
            elif "password=" in i: password = i[len("password="):].replace(' ', '')
       
        response=json.loads(L.Login(username,password), strict=False)
        return json.dumps(response, indent=2, ensure_ascii=False)
    
    elif path == "/update_avatar":
        avater=""
        if "avater=" in post_str: avater = post_str[len("avater="):].replace(' ', '')
        return L.update_avater(token,avater)


    elif path == "/update_password":
        password=""
        if "password=" in post_str: password = post_str[len("password="):].replace(' ', '')
        return L.update_pw(token,password)
    
    elif path == "/logout":
        return L.Logout(token)

    elif path=="/register":
        text = post_str.split("&")  
        username, password, avater = "", "", ""  
        for i in text:  
            if "username=" in i: username = i[len("username="):].replace(' ', '') 
            elif "password=" in i: password = i[len("password="):].replace(' ', '')  
            elif "avater=" in i: avater = i[len("avater="):].replace(' ', '')
            

        response=json.loads(L.Reg(username,password,avater), strict=False)
        return json.dumps(response, indent=2, ensure_ascii=False)


    elif path == "/news/comment/create":
        text = post_str.split("&")  
        comment, videoid, sub= "", "", ""
    
        for i in text:

            if "comment=" in i: comment = i[len("comment="):].replace(' ', '')   
            elif "id=" in i: videoid = i[len("id="):].replace(' ', '')  
            elif "sub=" in i: sub = i[len("sub="):].replace(' ', '')

        if not sub:
            return X.createcomment(token,comment,videoid)
        else:
            return X.createcomment(token,comment,videoid,sub)


    elif path == "/news/create":
        text = post_str.split("&")  
        title, content, tp, cover= "", "", "",""
        for i in text:  
            if "title=" in i: title = i[len("title="):]
            elif "content=" in i: content = i[len("content="):]
            elif "type=" in i: tp = i[len("type="):]
            elif "cover=" in i: cover = i[len("cover="):]
        return X.new_news(title,content,token,tp,cover)

    else:
        return "post错误"    


        

ip = ServerUtils.serverip();port =ServerUtils.serverport()
server_address = (ip, port)
print("app starting ip= " + str(server_address[0]) +"port="+ str(server_address[1]))
httpd = ThreadingTCPServer(server_address, RequestHandlerImpl)
httpd.serve_forever()

        
