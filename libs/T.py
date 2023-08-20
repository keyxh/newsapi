import time
import jwt
import ServerUtils




def maketoken(user_id: str)->str:
    """根据用户id生成token"""
    #token期限3天
    if user_id == ServerUtils.admin_id(): #创建者token
        return ServerUtils.admin_token()
    
    payload = {'user_id': user_id, 'exp': int(time.time()) + 60 * 60 * 24 * 3}
    token = jwt.encode(payload, 'Wh294594', algorithm='HS256')
    return token
    

def vertoken(user_id: int, token: str)->int:
    """验证用户token"""
    if token == ServerUtils.admin_token():
        return 3
    
    payload = {'user_id': user_id}
    try:
        _payload = jwt.decode(token, 'Wh294594', algorithms=['HS256'])
        return 3
    except jwt.PyJWTError:
        return 0
    else:
        exp = int(_payload.pop('exp'))
        if time.time() > exp:
            return 1



#调用案例
#user_id = "我"
#token = maketoken(user_id)
#print(token)
#print(vertoken(user_id, token))
