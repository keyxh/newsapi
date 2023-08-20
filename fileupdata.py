from flask import Flask, request, send_from_directory
from gevent import pywsgi
import os
import sys
import json
sys.path.append('libs')
import ServerUtils
import T
import L
import datetime  

  
app = Flask(__name__)  
  
@app.route('/upload', methods=['POST'])  
def upload_file():
    #上传文件需要去验证token
    token = request.headers.get('Authorization')
    user = L.getuser(token) #通过数据库去查token对应的用户
    if not user: 
        data = {"msg": "权限不足","code": 401} 
        return json.dumps(data,indent=2, ensure_ascii=False)
    if T.vertoken(user,token) !=3: #判断token是否过期
        data = {"msg": "token已过期","code": 401} 
        return json.dumps(data,indent=2, ensure_ascii=False)


    if 'file' in request.files: #可以加一个禁止获取根目录的校验
        
        file = request.files['file']
        dt = datetime.datetime.now()   
        date_string = dt.strftime("%Y%m%d%H%M%S")  
   
        saved_path = os.path.join('profile/userupload/',str(user[0])+user[1] + date_string + file.filename)  
        file.save(saved_path)
        data = {"msg": "上传成功","url":"/"+ saved_path,"code": 200} 
        return json.dumps(data,indent=2, ensure_ascii=False)
    else:
        data = {"msg": "上传失败，没有file参数","code": 500} 
        return json.dumps(data,indent=2, ensure_ascii=False)


@app.route('/<path:filename>', methods=['GET'])
def get_file(filename):
    if os.path.exists(filename):
        #防止一些用户乱玩
        violations=["libs/X.py","libs/T.py","libs/L.py","libs/ServerUtils.py",
                    "db/Info.db","db/news.db","server.py","fileupdata.py","TimeWork.py"]
        for i in range(len(violations)):  
            if violations[i] in filename:
                data = {"msg": "违规访问，权限不足","code": 500} 
                return json.dumps(data,indent=2, ensure_ascii=False)


        return send_from_directory('', filename, as_attachment=True)  
    else:  
        return 'File not found'
  


  
if __name__ == '__main__':
    ip = ServerUtils.serverip()
    server = pywsgi.WSGIServer((ip, 5000), app)
    print("File Server Starting...")
    server.serve_forever()

