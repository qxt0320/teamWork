# app.py
from flask import Flask, request, jsonify
import jwt
import datetime
from database.db import init_db, get_user, add_user, create_room, join_room, generate_token

app = Flask(__name__)

SECRET_KEY = "0f574d86d10ae8778feffc0dc47810907e436a8fc14c2971"


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

    token = generate_token(user['id'])

    # 显示用户登录成功
    print(user['real_name']+" logged in successfully")

    return jsonify({"token": token, "userId": user['id'], "username": user['username']}), 200


@app.route('/api/createroom', methods=['POST'])
def api_create_room():
    room_id = request.json.get('RoomID')
    if not room_id:
        return jsonify({"error": "RoomID是必须的"}), 400

    create_room(room_id)
    token = generate_token("room_creator")  # 你可能需要一个实际的用户ID来生成令牌
    return jsonify({"token": token, "RoomID": room_id}), 200


@app.route('/api/joinroom', methods=['POST'])
def api_join_room():
    room_id = request.json.get('RoomID')
    user_id = request.json.get('UserID')
    if not room_id or not user_id:
        return jsonify({"error": "RoomID和UserID都是必须的"}), 400

    join_room(room_id, user_id)
    token = generate_token(user_id)
    return jsonify({"token": token, "RoomID": room_id}), 200


@app.route('/auth/register', methods=['POST'])
def register():
    # print(request.headers)
    # print(request.data)  # 打印原始请求数据
    # print(request.get_json(silent=True))  # 使用 silent=True 防止解析错误

    username = request.json.get('phonenumber')
    password = request.json.get('password')
    yourname = request.json.get('yourname')  # 获取 yourname 字段

    #print(username, password, yourname)

    if not username or not password or not yourname:
        return jsonify({"error": "缺少必要的参数"}), 400

    if get_user(username):
        return jsonify({"error": "InvalidUserID", "message": "The provided UserID exists."}), 400

    add_user(username, password, yourname)  # 添加 yourname 参数

    # 用户注册成功后，生成令牌
    token = generate_token(username)

    # 显示用户注册成功
    print(yourname+" registered successfully")

    return jsonify({"token": token, "message": "User registered successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
