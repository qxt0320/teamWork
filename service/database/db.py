# database/db.py
import sqlite3
import jwt
import datetime
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

# 数据库文件的路径
DATABASE_PATH = 'game_data.db'
# 你的 SECRET_KEY 应该放在配置文件或环境变量中
SECRET_KEY = "0f574d86d10ae8778feffc0dc47810907e436a8fc14c2971"


def verify_token(token):
    try:
        # Decode the token
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return data  # Return the token data (e.g., user ID)
    except ExpiredSignatureError:
        # Token has expired
        return 'Token has expired', 401
    except InvalidTokenError:
        # Token is invalid
        return 'Token is invalid', 401


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 删除现有的 users 表，如果它已经存在
    cursor.execute('DROP TABLE IF EXISTS users')

    # 重新创建 users 表，这次包括 real_name 列
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        real_name TEXT,
        score INTEGER DEFAULT 0,
        rank INTEGER DEFAULT 0
    )
    ''')

    # 创建房间表
    cursor.execute('''
        CREATE TABLE rooms (
            id TEXT PRIMARY KEY,
            creator_username TEXT,
            participants TEXT DEFAULT '',  -- 添加 participants 列
            FOREIGN KEY (creator_username) REFERENCES users (username)
        )
        ''')

    # 创建房间参与者表
    cursor.execute('''
        CREATE TABLE room_participants (
            room_id TEXT,
            user_username TEXT,
            FOREIGN KEY (room_id) REFERENCES rooms (id),
            FOREIGN KEY (user_username) REFERENCES users (username)
        )
        ''')

    conn.commit()
    conn.close()


def add_user(username, password, real_name):
    # 更新函数以接受 real_name 参数
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, password, real_name, score, rank)
        VALUES (?, ?, ?, 0, 0)
    ''', (username, password, real_name))
    conn.commit()
    conn.close()


def get_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user


def create_room(room_id, username):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 确保 SQL 语句包括 creator_id 列
    cursor.execute('INSERT INTO rooms (id, creator_username, participants) VALUES (?, ?, ?)',
                   (room_id, username, username))

    conn.commit()
    conn.close()


def join_room(room_id, username, max_participants=2):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 验证房间是否存在
    if not room_exists(room_id):
        conn.close()
        return "Room not found", 404

    # 获取房间的参与者列表
    cursor.execute('SELECT participants FROM rooms WHERE id = ?', (room_id,))
    room_data = cursor.fetchone()
    if room_data is None:
        conn.close()
        return "Room data not found", 404

    participants_str = room_data[0]
    participants = participants_str.split(',')

    # 验证用户是否已经在房间中
    if username in participants:
        conn.close()
        return "User already in the room", 400

    # 验证房间人数是否已满
    if len(participants) >= max_participants:
        conn.close()
        return "Room is full", 400

    # 更新参与者列表
    participants.append(username)
    new_participants_str = ','.join(participants)

    cursor.execute('UPDATE rooms SET participants = ? WHERE id = ?', (new_participants_str, room_id))
    conn.commit()
    conn.close()
    return "User joined the room successfully", 200


# 修改 generate_token 函数，接受 username 作为参数
def generate_token(username):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({'username': username, 'exp': expiration_time}, SECRET_KEY, algorithm='HS256')
    print("使用以下串生成令牌：" + username)
    return token.decode('utf-8') if isinstance(token, bytes) else token


def room_exists(room_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM rooms WHERE id = ?', (room_id,))
    room = cursor.fetchone()
    conn.close()
    return room is not None


def user_exists(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    print("检查用户是否存在：" + username)
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return bool(user)


def out_room(room_id, username):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 验证房间是否存在
    if not room_exists(room_id):
        conn.close()
        return "Room not found", 404

    # 获取房间的参与者列表
    cursor.execute('SELECT participants, creator_username FROM rooms WHERE id = ?', (room_id,))
    room_data = cursor.fetchone()
    if room_data is None:
        conn.close()
        return "Room data not found", 404

    participants_str = room_data[0]
    participants = participants_str.split(',')
    creator_username = room_data[1]

    # 如果退出房间的是创建者，需要转交房主给其他用户（如果有其他用户的话）
    if username == creator_username:
        if len(participants) > 1:
            new_creator = [user for user in participants if user != username][0]
            cursor.execute('UPDATE rooms SET creator_username = ? WHERE id = ?', (new_creator, room_id))
        else:
            # 如果没有其他用户，删除房间
            cursor.execute('DELETE FROM rooms WHERE id = ?', (room_id,))
    else:
        # 如果退出房间的不是创建者，只需从参与者列表中移除用户
        participants.remove(username)
        new_participants_str = ','.join(participants)
        cursor.execute('UPDATE rooms SET participants = ? WHERE id = ?', (new_participants_str, room_id))

    conn.commit()
    conn.close()

    return "User left the room", 200


# 调用 init_db 函数以初始化数据库
init_db()
