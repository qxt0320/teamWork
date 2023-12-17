# database/db.py
import os
import sqlite3

# 数据库文件的路径
DATABASE_PATH = 'game_data.db'
# 你的 SECRET_KEY 应该放在配置文件或环境变量中
SECRET_KEY = "0f574d86d10ae8778feffc0dc47810907e436a8fc14c2971"


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def database_exists():
    return os.path.isfile(DATABASE_PATH)


def init_db():
    # 检查数据库是否存在
    if not database_exists():
        conn = get_db_connection()
        try:
            # 使用 cursor 对象执行 SQL 命令
            cursor = conn.cursor()

            # 删除现有的 users 表，如果它已经存在
            cursor.execute('DROP TABLE IF EXISTS users')

            # 重新创建 users 表
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
                    room_type INT,
                    participants TEXT DEFAULT '',
                    player1_ready BOOLEAN DEFAULT FALSE,
                    player2_ready BOOLEAN DEFAULT FALSE,
                    player3_ready BOOLEAN DEFAULT FALSE,
                    player4_ready BOOLEAN DEFAULT FALSE     
                )
            ''')


            # 创建 adminuser 表
            cursor.execute('''
                        CREATE TABLE adminuser (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL
                        )
                        ''')

            # 创建 game_records 表 # '3-player' 或 '4-player'
            cursor.execute('''
                            CREATE TABLE game_records (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                player1_username TEXT,
                                player2_username TEXT,
                                player3_username TEXT,
                                player4_username TEXT,
                                winner_username TEXT,
                                game_type TEXT,  
                                game_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (player1_username) REFERENCES users (username),
                                FOREIGN KEY (player2_username) REFERENCES users (username),
                                FOREIGN KEY (player3_username) REFERENCES users (username),
                                FOREIGN KEY (player4_username) REFERENCES users (username),
                                FOREIGN KEY (winner_username) REFERENCES users (username)
                            )
                        ''')

            # 提交事务
            conn.commit()
        except sqlite3.Error as e:
            # 打印数据库相关错误
            print(f"Database error: {e}")
        finally:
            # 关闭数据库连接
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


def create_room(room_id, username, room_type):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 确保 SQL 语句包括 creator_id 列
    cursor.execute('INSERT INTO rooms (id, creator_username, room_type, participants) VALUES (?, ?, ?, ?)',
                   (room_id, username, room_type, username))

    conn.commit()
    conn.close()


def join_room1(room_id, username):
    conn = get_db_connection()
    cursor = conn.cursor()
    # 验证房间是否存在
    if not room_exists(room_id):
        conn.close()
        return "Room not found", 404
    # 获取房间的参与者列表
    cursor.execute('SELECT participants FROM rooms WHERE id = ?', (room_id,))
    room_data = cursor.fetchone()
    cursor.execute('SELECT room_type FROM rooms WHERE id = ?', (room_id,))
    max_participants = cursor.fetchone()
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

    # 检查用户是否在房间中
    if username not in participants:
        conn.close()
        return "User not in room", 403  # 或者其他适当的HTTP状态码

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


def start_game(room_id):
    # 在这里添加游戏开始的逻辑
    pass


def get_room_data(room_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rooms WHERE id = ?', (room_id,))
    room_data = cursor.fetchone()
    conn.close()

    if room_data:
        participants = room_data['participants'].split(',')
        return {
            'id': room_data['id'],
            'creator_username': room_data['creator_username'],
            'participants': room_data['participants'],
            'player1_username': participants[0] if len(participants) > 0 else None,
            'player2_username': participants[1] if len(participants) > 1 else None,
            'player3_username': participants[2] if len(participants) > 2 else None,
            'player4_username': participants[3] if len(participants) > 3 else None,
            'player1_ready': room_data['player1_ready'],
            'player2_ready': room_data['player2_ready'],
            'player3_ready': room_data['player3_ready'],
            'player4_ready': room_data['player4_ready'],
        }
    else:
        return None


def update_ready_status(room_id, player_field, ready_status):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 确保字段名有效
    if player_field not in ['player1_ready', 'player2_ready']:
        conn.close()
        return "Invalid player field", 400

    # 更新准备状态字段
    cursor.execute(f'UPDATE rooms SET {player_field} = ? WHERE id = ?', (ready_status, room_id))
    conn.commit()
    conn.close()


def add_admin_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO adminuser (username, password)
        VALUES (?, ?)
    ''', (username, password))
    conn.commit()
    conn.close()


def validate_admin_login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM adminuser WHERE username = ?', (username,))
    admin = cursor.fetchone()
    conn.close()

    if admin and admin['password'] == password:
        return True  # 用户名和密码匹配
    else:
        return False  # 用户名不存在或密码不匹配


def admin_user_exists(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM adminuser WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None


def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, real_name, score, rank FROM users')
    users = cursor.fetchall()
    conn.close()
    return users


def delete_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 检查用户是否存在
    user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if not user:
        conn.close()
        return False  # 用户不存在

    cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    conn.close()
    return True  # 用户删除成功


def get_all_game_records():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, player1_username, player2_username, player3_username, player4_username, 
               winner_username, game_type, game_date 
        FROM game_records
    ''')
    game_records = cursor.fetchall()
    conn.close()
    return game_records


def add_game_record(player1, player2, player3, player4, winner, game_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO game_records (player1_username, player2_username, player3_username, player4_username, winner_username, game_type)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (player1, player2, player3, player4, winner, game_type))
    conn.commit()
    conn.close()


def get_all_rooms():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, creator_username, participants 
        FROM rooms
    ''')
    rooms = cursor.fetchall()
    conn.close()
    return rooms


# 调用 init_db 函数以初始化数据库
init_db()
