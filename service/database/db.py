# database/db.py
import sqlite3
import jwt
import datetime

# 数据库文件的路径
DATABASE_PATH = 'game_data.db'
# 你的 SECRET_KEY 应该放在配置文件或环境变量中
SECRET_KEY = "0f574d86d10ae8778feffc0dc47810907e436a8fc14c2971"


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
        participants TEXT DEFAULT ''
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


def create_room(room_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO rooms (id, participants) VALUES (?, ?)', (room_id, ''))
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
    return token.decode('utf-8') if isinstance(token, bytes) else token


# 调用 init_db 函数以初始化数据库
init_db()
