import sqlite3

# 数据库连接
conn = sqlite3.connect('game_data.db')  # 替换为您的数据库文件名
cursor = conn.cursor()



cursor.execute('''
        INSERT INTO rooms (id, creator_username, room_type,participants, player1_ready, player2_ready, player3_ready, player4_ready)
        VALUES ('1223', '1',4,'qxt,yyq,yyc,clh', FALSE, FALSE, FALSE, FALSE)
    ''',)


# 提交并保存更改
conn.commit()

# 关闭数据库连接
conn.close()
