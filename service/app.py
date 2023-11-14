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
        print(username, password)
        return jsonify({"error": "用户名和密码都是必须的"}), 400
    print(username, password)
    user = get_user(username)
    if not user:
        return jsonify({"error": "用户名不存在"}), 401
    if user['password'] != password:
        return jsonify({"error": "密码错误"}), 401

    token = generate_token(user['id'])
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


# 其他API端点...

if __name__ == '__main__':
    app.run(debug=True)
