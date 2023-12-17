import jwt
from flask import Flask, request, jsonify, render_template
from functools import wraps
import datetime
from db import *
from game_manager import *
from flask_cors import CORS
import random
from flask_socketio import SocketIO, join_room
from threading import Timer
from flask_socketio import emit

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)
socketio = SocketIO(app,cors_allowed_origins="http://api2.andylive.cn") # 创建 Flask-SocketIO 实例
game_manager = GameManager(socketio)  # 创建 GameManager 实例

SECRET_KEY = "0f574d86d10ae8778feffc0dc47810907e436a8fc14c2971"

def generate_token(username):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({'username': username, 'exp': expiration_time}, SECRET_KEY, algorithm='HS256')
    print("使用以下串生成令牌：" + username)
    return token.decode('utf-8') if isinstance(token, bytes) else token


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
    room_type = request.json.get('RoomType')  # 3 or 4
    if not room_id:
        return jsonify({"error": "RoomID是必须的"}), 400

    if room_exists(room_id):
        return jsonify({"error": "RoomID已存在"}), 409  # 409 Conflict

    if room_type not in [3, 4]:
        return jsonify({"error": "房间类型有误"}), 405

    create_room(room_id, username, room_type)  # 将 'user_id' 更改为 'username'
    return jsonify({"RoomID": room_id}), 200


@app.route('/api/joinroom', methods=['POST'])
@token_required
def api_join_room(username):  # 通过装饰器传递的参数
    room_id = request.json.get('RoomID')
    if not room_id:
        return jsonify({"error": "RoomID是必须的"}), 400

    result, status_code = join_room1(room_id, username)
    return jsonify({"message": result}), status_code


@app.route('/api/outroom', methods=['POST'])
@token_required
def api_out_room(username):
    room_id = request.json.get('RoomID')
    if not room_id:
        return jsonify({"error": "RoomID是必须的"}), 400

    result, status_code = out_room(room_id, username)
    if status_code != 200:
        return jsonify({"error": result}), status_code
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


@app.route('/api/readygame', methods=['POST'])
@token_required
def api_ready_game(username):
    room_id = request.json.get('RoomID')
    player_ready = request.json.get('ReadyStatus')  # 准备状态，True 或 False

    if not room_id or player_ready is None:
        return jsonify({"error": "RoomID 和 ReadyStatus 是必需的"}), 400

    # 检查房间是否存在
    if not room_exists(room_id):
        return jsonify({"error": "Room not found"}), 404

    # 获取房间信息
    room_data = get_room_data(room_id)

    # 识别并更新玩家的准备状态
    if 'player1_username' in room_data and username == room_data['player1_username']:
        update_ready_status(room_id, 'player1_ready', player_ready)
    elif 'player2_username' in room_data and username == room_data['player2_username']:
        update_ready_status(room_id, 'player2_ready', player_ready)
    elif 'player3_username' in room_data and username == room_data['player3_username']:
        update_ready_status(room_id, 'player3_ready', player_ready)
    else:
        return jsonify({"error": "You are not a participant in this room"}), 403

    # 重新获取房间信息以检查所有玩家是否已准备
    updated_room_data = get_room_data(room_id)

    # 检查是否三名玩家都已准备
    if all([updated_room_data.get(f'player{i}_ready') for i in range(1, 4)]):
        start_game(room_id)

    return jsonify({"message": "Ready status updated successfully"}), 200


@app.route('/api/adminregister', methods=['POST'])
def admin_register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': '用户名和密码都是必须的'}), 400

    if admin_user_exists(username):
        return jsonify({'error': '用户名已存在'}), 409

    # 这里应该添加密码散列步骤
    hashed_password = password  # 示例中未散列密码，但在生产中应该这么做

    add_admin_user(username, hashed_password)
    return jsonify({'message': '管理员用户注册成功'}), 201


@app.route('/api/adminlogin', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': '用户名和密码都是必须的'}), 400

    if validate_admin_login(username, password):
        # 登录成功，生成 token 或其他认证机制
        token = generate_token(username)  # 假设您有一个生成 token 的函数
        return jsonify({'message': '登录成功', 'token': token}), 200
    else:
        return jsonify({'error': '用户名不存在或密码错误'}), 401


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token_parts = auth_header.split()
            if token_parts[0].lower() == "bearer" and len(token_parts) == 2:
                token = token_parts[1]
            else:
                return jsonify({"error": "Authorization header must start with 'Bearer'."}), 401

        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get('username')
            # Check if the user is an admin
            if not admin_user_exists(username):
                return jsonify({"error": "Invalid token or user is not an admin."}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        kwargs['username'] = username
        return f(*args, **kwargs)

    return decorated


@app.route('/api/userlist', methods=['GET'])
@admin_token_required
def get_user_list(username):
    users = get_all_users()
    user_list = []

    for user in users:
        user_data = {
            'id': user['id'],
            'username': user['username'],
            'real_name': user['real_name'],
            'score': user['score'],
            'rank': user['rank']
        }
        user_list.append(user_data)

    return jsonify(user_list)


@app.route('/api/delplayer', methods=['POST'])
@admin_token_required
def delete_player(username):
    data = request.get_json()
    username = data.get('username')  # 使用正确的键名

    if not username:
        return jsonify({'error': '用户名是必须的'}), 400

    if not user_exists(username):  # 确保 user_exists 函数也使用 username 参数
        return jsonify({'error': '用户不存在'}), 404

    if delete_user(username):
        return jsonify({'message': '用户删除成功'}), 200
    else:
        return jsonify({'error': '删除用户失败'}), 500


@app.route('/api/gamelist', methods=['GET'])
@admin_token_required
def get_game_list(username):
    game_records = get_all_game_records()
    game_list = []

    for record in game_records:
        game_data = {
            'id': record['id'],
            'player1_username': record['player1_username'],
            'player2_username': record['player2_username'],
            'player3_username': record['player3_username'],
            'player4_username': record['player4_username'],
            'winner_username': record['winner_username'],
            'game_type': record['game_type'],
            'game_date': record['game_date']
        }
        game_list.append(game_data)

    return jsonify(game_list)


@app.route('/api/addgame', methods=['POST'])
@admin_token_required
def add_game(username):
    data = request.get_json()
    player1 = data.get('player1')
    player2 = data.get('player2')
    player3 = data.get('player3')
    player4 = data.get('player4')
    winner = data.get('winner')
    game_type = data.get('game_type')

    add_game_record(player1, player2, player3, player4, winner, game_type)
    return jsonify({'message': '对战记录添加成功'}), 201


@app.route('/api/roomlist', methods=['GET'])
@admin_token_required
def get_room_list(username):
    rooms = get_all_rooms()
    room_list = []

    for room in rooms:
        room_data = {
            'id': room['id'],
            'creator_username': room['creator_username'],
            'participants': room['participants'].split(',')  # 假设参与者是以逗号分隔的字符串
        }
        room_list.append(room_data)

    return jsonify(room_list)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
