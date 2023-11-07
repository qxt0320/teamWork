import sqlite3

# 连接到数据库（如果不存在则会创建）
conn = sqlite3.connect('game_data.db')
cursor = conn.cursor()

# 创建用户表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT,
        score INTEGER,
        rank INTEGER
    )
''')
conn.commit()

# 添加用户
def add_user(username, password):
    cursor.execute('''
        INSERT INTO users (username, password, score, rank) VALUES (?, ?, 0, 0)
    ''', (username, password))
    conn.commit()

# 根据用户名获取用户信息
def get_user(username):
    cursor.execute('''
        SELECT * FROM users WHERE username = ?
    ''', (username,))
    return cursor.fetchone()

# 更新用户积分
def update_score(username, new_score):
    cursor.execute('''
        UPDATE users SET score = ? WHERE username = ?
    ''', (new_score, username))
    conn.commit()

# 更新用户排名
def update_rank(username, new_rank):
    cursor.execute('''
        UPDATE users SET rank = ? WHERE username = ?
    ''', (new_rank, username))
    conn.commit()

# 获取排名前N的用户
def get_top_users(limit):
    cursor.execute('''
        SELECT username, score, rank FROM users ORDER BY score DESC LIMIT ?
    ''', (limit,))
    return cursor.fetchall()

# 示例操作：
add_user('player1', 'password1')
add_user('player2', 'password2')

update_score('player1', 100)
update_score('player2', 150)

update_rank('player1', 2)
update_rank('player2', 1)

top_users = get_top_users(5)
print("排名前5的用户：", top_users)

conn.close()
