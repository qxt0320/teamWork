from flask import Flask, render_template, request, jsonify , redirect, url_for
import mysql.connector

app = Flask(__name__)

#链接数据库
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="yyq20030103",
    database="turtle"
)
cursor = conn.cursor()
# 建表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        phone VARCHAR(15) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
''')
conn.commit()

# Route - Display registration page
@app.route('/')
def register_page():
    return render_template('register.html')

# 在注册用户之前检查手机号是否已存在
def is_phone_unique(phone):
    cursor.execute('SELECT COUNT(*) FROM users WHERE phone = %s', (phone,))
    count = cursor.fetchone()[0]
    return count == 0

# 路由请求连接
@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        username = data['username']
        phone = data['phone']
        password = data['password']

         # 检查手机号是否唯一
        if not is_phone_unique(phone):
            response = {'message': '注册失败，该电话号码已被注册过.'}
            return jsonify(response)

        # 插入信息至数据库
        cursor.execute('INSERT INTO users (username, phone, password) VALUES (%s, %s, %s)', (username, phone, password))
        conn.commit()

        # 注册成功后重定向到 user_list 页面
        return redirect(url_for('user_list'))
    except Exception as e:
        response = {'message': 'Registration failed. Error: ' + str(e)}
        return jsonify(response)

# 显示用户列表（排行榜）
@app.route('/user_list')
def user_list():
    # 从数据库中获取用户信息
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    return render_template('user_list.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)

