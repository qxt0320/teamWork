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
       CREATE TABLE IF NOT EXISTS rooms (
           id TEXT PRIMARY KEY,
           creator_id INTEGER,  -- 新增的列，用于存储创建房间的用户的ID
           participants TEXT DEFAULT '',
           FOREIGN KEY (creator_id) REFERENCES users (id)  -- 外键关联到 users 表的 id
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


def create_room(room_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # 确保 SQL 语句包括 creator_id 列
    cursor.execute('INSERT INTO rooms (id, creator_id, participants) VALUES (?, ?, ?)', (room_id, user_id, ''))
    conn.commit()
    conn.close()


def join_room(room_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE rooms SET participants = participants || ? || ', ' WHERE id = ?', (user_id, room_id))
    conn.commit()
    conn.close()


def generate_token(username):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({'username': username, 'exp': expiration_time}, SECRET_KEY, algorithm='HS256')
    print("使用以下串生成令牌："+username)
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
    print("检查用户是否存在："+username)
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return bool(user)


# 调用 init_db 函数以初始化数据库
init_db()
