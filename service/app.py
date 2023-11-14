# app.py
import jwt
from flask import Flask, request, jsonify, abort
from database.db import get_user, add_user, create_room, join_room, generate_token, verify_token, room_exists, \
    user_exists
from functools import wraps
from jwt import ExpiredSignatureError, InvalidTokenError, decode

app = Flask(__name__)

SECRET_KEY = "0f574d86d10ae8778feffc0dc47810907e436a8fc14c2971"


# 装饰器，用于验证令牌
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token_parts = auth_header.split()  # Split by space
            if token_parts[0].lower() == "bearer" and len(token_parts) == 2:
                token = token_parts[1]
            else:
                return jsonify({"error": "Authorization header must start with 'Bearer'."}), 401

        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            # Decode the token
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get('username')
            # Now, check if the user exists in the database
            if not user_exists(username):
                print("使用以下串检查令牌:", username)
                return jsonify({"error": "Invalid token: user does not exist."}), 401
        except Exception as e:
            # Handle other exceptions
            return jsonify({"error": str(e)}), 401

        # Attach username to kwargs
        kwargs['username'] = username
        return f(*args, **kwargs)

    return decorated


@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('phonenumber')
    password = request.json.get('password')

    if not username or not password:
        # print(username, password)
        return jsonify({"error": "用户名和密码都是必须的"}), 400
    # print(username, password)
    user = get_user(username)
    if not user:
        return jsonify({"error": "用户名不存在"}), 401
    if user['password'] != password:
        return jsonify({"error": "密码错误"}), 401

    token = generate_token(username)  # 使用 username 作为参数

    # 显示用户登录成功
    print(user['real_name'] + " logged in successfully")

    return jsonify({"token": token, "userId": user['id'], "username": user['username']}), 200


@app.route('/api/createroom', methods=['POST'])
@token_required
def api_create_room(username):  # 将参数名称更改为 'username'
    room_id = request.json.get('RoomID')
    if not room_id:
        return jsonify({"error": "RoomID是必须的"}), 400

    if room_exists(room_id):
        return jsonify({"error": "RoomID已存在"}), 409  # 409 Conflict

    create_room(room_id, username)  # 将 'user_id' 更改为 'username'
    return jsonify({"RoomID": room_id}), 200


@app.route('/api/joinroom', methods=['POST'])
@token_required
def api_join_room(username):  # 通过装饰器传递的参数
    room_id = request.json.get('RoomID')
    if not room_id:
        return jsonify({"error": "RoomID和UserID都是必须的"}), 400

    result, status_code = join_room(room_id, username)
    return jsonify({"message": result}), status_code


@app.route('/api/register', methods=['POST'])
def register():
    # print(request.headers)
    # print(request.data)  # 打印原始请求数据
    # print(request.get_json(silent=True))  # 使用 silent=True 防止解析错误

    username = request.json.get('phonenumber')
    password = request.json.get('password')
    yourname = request.json.get('yourname')  # 获取 yourname 字段

    # print(username, password, yourname)

    if not username or not password or not yourname:
        return jsonify({"error": "缺少必要的参数"}), 400

    if get_user(username):
        return jsonify({"error": "InvalidUserID", "message": "The provided UserID exists."}), 400

    add_user(username, password, yourname)  # 添加 yourname 参数

    print("Username:", username)
    print("Password:", password)
    print("Yourname:", yourname)

    # 用户注册成功后，生成令牌
    token = generate_token(username)

    # 显示用户注册成功
    print(yourname + " registered successfully")

    return jsonify({"token": token, "message": "User registered successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
