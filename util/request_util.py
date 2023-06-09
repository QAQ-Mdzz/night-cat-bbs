from flask import jsonify
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def check_args(data : dict, *args) -> bool:
    is_full = True
    for i in args:
        if not i:
            is_full = False
            data['status'] = 'no'
            if not data.get('data'):
                data['data'] = dict()
            data['data']['msg'] = '参数错误'
    return is_full

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    data = {
        "data": {
            "msg": "登录过期"
        },
        "status": "no"
    }
    return jsonify(data)

@jwt.unauthorized_loader
def my_invalid_token(callback):
    data = {
        "data": {
            "msg": "缺少 token"
        },
        "status": "no"
    }
    return jsonify(data)