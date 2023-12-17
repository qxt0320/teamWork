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
#CORS(app, resources={r"/socket.io/*": {"origins": "http://socket.andylive.cn"}})
#socketio = SocketIO(app,cors_allowed_origins="http://api2.andylive.cn") # 创建 Flask-SocketIO 实例
CORS(app)
socketio=SocketIO(app)
game_manager = GameManager(socketio)  # 创建 GameManager 实例
player_scores = {1: 0, 2: 0, 3: 0, 4: 0}
player_scores3 = {1: 0, 2: 0, 3: 0}

SECRET_KEY = "0f574d86d10ae8778feffc0dc47810907e436a8fc14c2971"

hands = ['']
special_cards = ["turtle", "swap", "switch"]
player_to_hand_index = {}
out_cards = []
players = {}
is_switch_active = False
current_player_turn = 1  # 添加一个全局变量来跟踪当前回合的玩家
player_names = {}
player_has_cards = {1: True, 2: True, 3: True, 4: True}
player_has_cards3 = {1: True, 2: True, 3: True}
finish_order4 = []  # 记录玩家完成游戏的顺序
finish_order = []  # 记录玩家完成游戏的顺序


def get_room_participants():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, room_type,participants FROM rooms')
    rooms_data = cursor.fetchall()
    print(rooms_data)
    conn.close()
    room_participants = []
    for room in rooms_data:
        room_id = room['id']
        room_type = room['room_type']
        participants = room['participants'].split(',')
        room_participants.append({'room_id': room_id, 'room_type':room_type,'participants': participants})
    return room_participants


def deal_cards():
    global hands
    hands = [[] for _ in range(3)]
    suits = ['红桃', '方块', '黑桃', '梅花']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [f"{suit}{rank}" for rank in ranks for suit in suits]
    pairs = []
    while len(pairs) < 18:
        selected_pair = random.sample(deck, k=2)
        if selected_pair[0][2] == selected_pair[1][2]:
            pairs.extend(selected_pair)
            for card in selected_pair:
                deck.remove(card)
    random.shuffle(pairs)
    all_cards = pairs + special_cards
    random.shuffle(all_cards)
    # 分配牌给每个玩家
    for i in range(len(all_cards)):
        hands[i % 3].append(all_cards[i])
    print("Hands:", hands)
    return {
        'player1Cards': hands[0],
        'player2Cards': hands[1],
        'player3Cards': hands[2],
    }


def shuffle_hand(player_index):
    global hands
    if 0 <= player_index < len(hands):
        random.shuffle(hands[player_index])
    else:
        print(f"Invalid player index: {player_index}")


def check_players_and_deal_cards():
    if len(players) == 3:
        # 等待3秒
        Timer(3.0, auto_deal_cards).start()


# 自动发牌的函数
def auto_deal_cards():
    global current_player_turn
    current_player_turn = 1  # 设置初始玩家为1
    dealt_cards = deal_cards()  # 发牌逻辑
    for session_id, player_id in players.items():
        if player_id == 1:
            player_cards = dealt_cards[f'player1Cards']
            opponent1_cards = dealt_cards[f'player2Cards']
            opponent2_cards = dealt_cards[f'player3Cards']
        elif player_id == 2:
            player_cards = dealt_cards[f'player2Cards']
            opponent1_cards = dealt_cards[f'player3Cards']
            opponent2_cards = dealt_cards[f'player1Cards']
        else:
            player_cards = dealt_cards[f'player3Cards']
            opponent1_cards = dealt_cards[f'player1Cards']
            opponent2_cards = dealt_cards[f'player2Cards']
        socketio.emit('cards_dealt',
                      {'player_id': player_id, 'playerCards': player_cards, 'opponent1Cards': opponent1_cards,
                       'opponent2Cards': opponent2_cards}, room=session_id)


@app.route('/game3player')
def index3():
    return render_template('game3player.html')


@app.route('/result3')
def result3():
    return render_template('result3.html')


@app.route('/api/get_cards', methods=['GET'])
def get_cards():
    cards_data = deal_cards()
    return jsonify(cards_data)


@app.route('/api/draw_card', methods=['POST'])
def draw_card():
    data = request.json
    player_index = data['playerIndex']
    opponent_index = data['opponentIndex']
    card_index = data['cardIndex']
    # 从对手手中移除并添加到玩家手中
    card = hands[opponent_index].pop(card_index)
    hands[player_index].append(card)
    return jsonify({
        'playerCards': hands[player_index],
        'opponent1Cards': hands[1],
        'opponent2Cards': hands[2]
    })


@socketio.on('draw_card')
def handle_draw_card(data):
    global current_player_turn, player_scores3
    player_id = data['player_id']
    if player_id != current_player_turn:
        emit('not_your_turn', {'message': '当前不是您的回合'}, room=request.sid)
        return
    opponent_id = data['opponent_id']
    card_index = data['card_index']
    player_index = player_to_hand_index[player_id]
    opponent_index = player_to_hand_index[opponent_id]
    # 检查目标玩家是否有牌
    if not hands[opponent_index]:
        # 如果目标玩家没有牌，则跳过当前玩家的回合
        current_player_turn = update_next_turn(current_player_turn)
        print(current_player_turn)
        emit('update_turn', {'currentPlayerTurn': current_player_turn}, broadcast=True)
        return
    card = hands[opponent_index].pop(card_index)
    if not hands[player_index]:
        update_finish_order(player_index)
    if card not in out_cards:  # 只有未打出的牌才能被添加
        hands[player_index].append(card)
    if not hands[opponent_index]:
        update_finish_order(opponent_index)
    # 广播更新到所有客户端
    for session_id, p_id in players.items():
        player_cards = hands[player_to_hand_index[p_id]]
        # 确保对手牌组被正确分配
        if p_id == 1:
            opponent1_cards = hands[player_to_hand_index[2]]
            opponent2_cards = hands[player_to_hand_index[3]]
        elif p_id == 2:
            opponent1_cards = hands[player_to_hand_index[3]]
            opponent2_cards = hands[player_to_hand_index[1]]
        else:
            opponent1_cards = hands[player_to_hand_index[1]]
            opponent2_cards = hands[player_to_hand_index[2]]
        socketio.emit('cards_updated',
                      {'player_id': p_id, 'playerCards': player_cards, 'opponent1Cards': opponent1_cards,
                       'opponent2Cards': opponent2_cards, 'outCards': out_cards}, room=session_id)
    if is_switch_active == False:
        if current_player_turn == 1:
            current_player_turn = 3
            if not hands[2]:
                current_player_turn = 2
            if not hands[1]:
                print("over")
        elif current_player_turn == 3:
            current_player_turn = 2
            if not hands[1]:
                current_player_turn = 1
            if not hands[0]:
                print("over")
        else:
            current_player_turn = 1
            if not hands[0]:
                current_player_turn = 3
            if not hands[2]:
                print("over")
    else:
        if current_player_turn == 1:
            current_player_turn = 2
            if not hands[1]:
                current_player_turn = 3
            if not hands[2]:
                print("over")
        elif current_player_turn == 3:
            current_player_turn = 1
            if not hands[0]:
                current_player_turn = 2
            if not hands[1]:
                print("over")
        else:
            current_player_turn = 3
            if not hands[2]:
                current_player_turn = 1
            if not hands[0]:
                print("over")
    emit('update_turn', {'currentPlayerTurn': current_player_turn}, broadcast=True)
    over()


def update_next_turn(current_player_turn):
    # 根据当前玩家回合更新下一个玩家回合
    if current_player_turn == 1:
        next_player_turn = 3
    elif current_player_turn == 3:
        next_player_turn = 2
    elif current_player_turn == 2:
        next_player_turn = 1
    # 检查并跳过无牌玩家
    while not player_has_cards3[next_player_turn]:
        if next_player_turn == 1:
            next_player_turn = 3
        elif next_player_turn == 3:
            next_player_turn = 2
        elif next_player_turn == 2:
            next_player_turn = 1
    return next_player_turn


@app.route('/api/pairs', methods=['POST'])
def pairs():
    data = request.json
    player_id = data['player_id']  # 从请求中获取 player_id
    new_player_cards = data.get('newPlayerCards')
    # 从 player_id 获取手牌索引
    player_index = player_to_hand_index.get(player_id)
    # 更新玩家的手牌
    global hands
    if new_player_cards is not None:
        hands[player_index] = new_player_cards
    print("Updated hands:", hands[player_index])
    return jsonify({
        'playerCards': hands[player_index],
        # 返回其他需要的信息
    })


@socketio.on('play_pairs')
def handle_play_pairs(data):
    global current_player_turn, player_scores3
    player_id = data['player_id']
    pairs = data['pairs']
    new_player_cards = data['newPlayerCards']
    # 从 player_id 获取手牌索引
    global hands
    player_index = player_to_hand_index[player_id]
    hands[player_index] = new_player_cards
    if not hands[player_index]:
        update_finish_order(player_index)
    # 将打出的对子牌添加到 out_cards
    for pair in pairs:
        out_cards.extend(pair)
    # 更新所有客户端
    for session_id, p_id in players.items():
        player_cards = hands[player_to_hand_index[p_id]]
        # 确保对手牌组被正确分配
        if p_id == 1:
            opponent1_cards = hands[player_to_hand_index[2]]
            opponent2_cards = hands[player_to_hand_index[3]]
        elif p_id == 2:
            opponent1_cards = hands[player_to_hand_index[3]]
            opponent2_cards = hands[player_to_hand_index[1]]
        else:
            opponent1_cards = hands[player_to_hand_index[1]]
            opponent2_cards = hands[player_to_hand_index[2]]
        socketio.emit('cards_updated',
                      {'player_id': p_id, 'playerCards': player_cards, 'opponent1Cards': opponent1_cards,
                       'opponent2Cards': opponent2_cards, 'outCards': out_cards}, room=session_id)
    over()


@app.route('/api/swap_cards', methods=['POST'])
def swap_cards():
    global hands
    data = request.json
    hands[0] = data['playerCards']
    hands[1] = data['opponent1Cards']
    hands[2] = data['opponent2Cards']
    # 检查是否有 swapOpponentIndex 参数，并且它不是 None
    swap_opponent_index = data.get('swapOpponentIndex')
    if swap_opponent_index is not None:
        print(f"Shuffling opponent {swap_opponent_index} hand")
        shuffle_hand(swap_opponent_index)

    return jsonify({'message': 'Cards updated successfully'})


@socketio.on('swap_cards')
def handle_swap_cards(data):
    player_id = data['player_id']
    target_player_id = data['target_player_id']
    playerCards = data['playerCard']
    opponentCards = data['opponentCard']
    outcards = data['outCards']  # 接收更新后的废牌堆
    print(outcards)
    last_element = outcards[-1]  # 获取最后一个元素，即 "swap"
    out_cards.append(last_element)  # 更新废牌堆
    print(out_cards)
    if player_id == 1:
        if target_player_id == 1:
            target_player_id = 2
        elif target_player_id == 2:
            target_player_id = 3
    elif player_id == 2:
        if target_player_id == 1:
            target_player_id = 3
        elif target_player_id == 2:
            target_player_id = 1
    elif player_id == 3:
        if target_player_id == 1:
            target_player_id = 1
        elif target_player_id == 2:
            target_player_id = 2
    print(playerCards)
    # 更新玩家的手牌
    hands[player_id - 1] = playerCards
    hands[target_player_id - 1] = opponentCards
    for session_id, p_id in players.items():
        player_cards = hands[player_to_hand_index[p_id]]
        # 确保对手牌组被正确分配
        if p_id == 1:
            opponent1_cards = hands[player_to_hand_index[2]]
            opponent2_cards = hands[player_to_hand_index[3]]
        elif p_id == 2:
            opponent1_cards = hands[player_to_hand_index[3]]
            opponent2_cards = hands[player_to_hand_index[1]]
        else:
            opponent1_cards = hands[player_to_hand_index[1]]
            opponent2_cards = hands[player_to_hand_index[2]]
        socketio.emit('cards_updated',
                      {'player_id': p_id, 'playerCards': player_cards, 'opponent1Cards': opponent1_cards,
                       'opponent2Cards': opponent2_cards, 'outCards': out_cards}, room=session_id)

print(1)
@socketio.on('connect')
def on_connect():
    print("on_connect")
    global players, player_to_hand_index
    room_participants = get_room_participants()
    room_participants=room_participants[-1]
    print(room_participants)
    room_player_names = {}
    room_id = room_participants['room_id']
    num=room_participants['room_type']
    participants = room_participants['participants']
    for i, username in enumerate(participants, start=1):
        room_player_names[i] = username
    join_room(room_id)
    if(num==3):
        emit('room_participant_info', {'room_id': room_id, 'playerNames': room_player_names})
        print(room_player_names)
        session_id = request.sid
        player_id = len(players) + 1
        players[session_id] = player_id
        player_to_hand_index[player_id] = player_id - 1
        player_name = room_player_names.get(player_id, "Unknown Player")
        print(player_name)
        socketio.emit('player_id_assigned', {'player_id': player_id}, room=session_id)
        emit('set_player_name', {'playerId': player_id, 'playerName': player_name}, room=session_id)
        check_players_and_deal_cards()  # 检查玩家人数并在满足条件时自动发牌
        emit('update_turn', {'currentPlayerTurn': current_player_turn})
    else:
        emit('room_participant_info4', {'room_id': room_id, 'playerNames': room_player_names})
        print(room_player_names)
        session_id = request.sid
        player_id = len(players) + 1
        players[session_id] = player_id
        player_to_hand_index[player_id] = player_id - 1
        player_name = room_player_names.get(player_id, "Unknown Player")
        print(player_name)
        socketio.emit('player_id_assigned4', {'player_id': player_id}, room=session_id)
        emit('set_player_name4', {'playerId': player_id, 'playerName': player_name}, room=session_id)
        check_players_and_deal_cards4()  # 检查玩家人数并在满足条件时自动发牌
        emit('update_turn4', {'currentPlayerTurn': current_player_turn})


@socketio.on('deal_cards')
def handle_deal_cards(data):
    dealt_cards = deal_cards()  # 发牌逻辑
    for session_id, player_id in players.items():
        player_cards = dealt_cards[f'player{player_id}Cards']
        opponent1_cards = dealt_cards[f'player{(player_id % 3) + 1}Cards']
        opponent2_cards = dealt_cards[f'player{((player_id + 1) % 3) + 1}Cards']
        socketio.emit('cards_dealt',
                      {'player_id': player_id, 'playerCards': player_cards, 'opponent1Cards': opponent1_cards,
                       'opponent2Cards': opponent2_cards}, room=session_id)


@socketio.on('play_switch_card')
def handle_play_switch_card(data):
    global is_switch_active, currentPlayerTurnId
    player_id = data['player_id']
    switch_card_index = data['card_index']  # 获取 switch 牌的索引
    # 将 switch 牌从玩家手牌移除并加入废牌堆
    switch_card = hands[player_to_hand_index[player_id]].pop(switch_card_index)
    out_cards.append(switch_card)
    # 更新 switch 状态
    is_switch_active = not is_switch_active
    # 广播更新到所有客户端
    for session_id, p_id in players.items():
        player_cards = hands[player_to_hand_index[p_id]]
        # 确保对手牌组被正确分配
        if p_id == 1:
            opponent1_cards = hands[player_to_hand_index[2]]
            opponent2_cards = hands[player_to_hand_index[3]]
        elif p_id == 2:
            opponent1_cards = hands[player_to_hand_index[3]]
            opponent2_cards = hands[player_to_hand_index[1]]
        else:
            opponent1_cards = hands[player_to_hand_index[1]]
            opponent2_cards = hands[player_to_hand_index[2]]
        socketio.emit('cards_updated',
                      {'player_id': p_id, 'playerCards': player_cards, 'opponent1Cards': opponent1_cards,
                       'opponent2Cards': opponent2_cards, 'outCards': out_cards}, room=session_id)
    emit('switch_status_changed', {'isSwitchActive': is_switch_active}, broadcast=True)


@socketio.on('end_turn')
def handle_end_turn(data):
    global current_player_turn
    player_id = data['player_id']
    if player_id == current_player_turn:
        if is_switch_active == False:
            if current_player_turn == 1:
                current_player_turn = 3
                if not hands[2]:
                    current_player_turn = 2
                if not hands[1]:
                    print("over")
            elif current_player_turn == 3:
                current_player_turn = 2
                if not hands[1]:
                    current_player_turn = 1
                if not hands[0]:
                    print("over")
            else:
                current_player_turn = 1
                if not hands[0]:
                    current_player_turn = 3
                if not hands[2]:
                    print("over")
        else:
            if current_player_turn == 1:
                current_player_turn = 2
                if not hands[1]:
                    current_player_turn = 3
                if not hands[2]:
                    print("over")
            elif current_player_turn == 3:
                current_player_turn = 1
                if not hands[0]:
                    current_player_turn = 2
                if not hands[1]:
                    print("over")
            else:
                current_player_turn = 3
                if not hands[2]:
                    current_player_turn = 1
                if not hands[0]:
                    print("over")
        emit('update_turn', {'currentPlayerTurn': current_player_turn}, broadcast=True)
    else:
        emit('error', {'message': '不是您的回合'}, room=request.sid)


def over():
    global current_player_turn, player_scores3
    update_player_cards_status()  # 更新玩家手中牌的状态
    players_with_cards_count = sum(1 for cards in hands if cards)
    if players_with_cards_count <= 1:
        formatted_scores = calculate_scores()
        emit('game_over', {'playerScores': formatted_scores}, broadcast=True)


def update_player_cards_status():
    global player_has_cards3, hands
    for player_id, cards in enumerate(hands, start=1):
        player_has_cards3[player_id] = bool(cards)  # 如果玩家手中还有牌，则为 True

def update_finish_order(player_id):
    global finish_order
    if player_id+1 not in finish_order:
        player_id=player_id+1
        print(f"Player {player_id} finished")
        finish_order.append(player_id)

def calculate_scores():
    global player_scores3, finish_order4
    score_values = [ 30, 15, 0]  # 根据完成顺序的积分
    max_scores_idx = len(score_values) - 1  # 最大索引
    for idx, player_id in enumerate(finish_order):
        score_idx = min(idx, max_scores_idx)  # 确保索引不会超出范围
        player_scores3[player_id] = score_values[score_idx]
    # 如果有玩家没有在 finish_order 中，给他们最低分
    for player_id in range(1, 4):
        if player_id not in finish_order:
            player_scores3[player_id] = score_values[-1]

    print("游戏结束！玩家积分如下：")
    for player_id, score in player_scores3.items():
        print(f"玩家 {player_id}: {score} 分")

    return player_scores3


# 随机发牌4
def deal_cards4():
    global hands
    hands = [[] for _ in range(4)]
    suits = ['红桃', '方块', '黑桃', '梅花']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [f"{suit}{rank}" for rank in ranks for suit in suits]
    pairs = []
    while len(pairs) < 24:
        selected_pair = random.sample(deck, k=2)
        if selected_pair[0][2] == selected_pair[1][2]:
            pairs.extend(selected_pair)
            for card in selected_pair:
                deck.remove(card)
    random.shuffle(pairs)
    all_cards = pairs + special_cards
    random.shuffle(all_cards)
    # 分配牌给每个玩家
    for i in range(len(all_cards)):
        hands[i % 4].append(all_cards[i])
    print("Hands:", hands)
    return {
        'player1Cards': hands[0],
        'player2Cards': hands[1],
        'player3Cards': hands[2],
        'player4Cards': hands[3],
    }


def shuffle_hand4(player_index):
    global hands
    if 0 <= player_index < len(hands):
        random.shuffle(hands[player_index])
    else:
        print(f"Invalid player index: {player_index}")


def check_players_and_deal_cards4():
    if len(players) == 4:
        # 等待3秒
        Timer(3.0, auto_deal_cards4).start()


# 自动发牌的函数
def auto_deal_cards4():
    global current_player_turn
    current_player_turn = 1  # 设置初始玩家为1
    dealt_cards = deal_cards4()  # 发牌逻辑
    for session_id, player_id in players.items():
        if player_id == 1:
            player_cards = dealt_cards[f'player1Cards']
            opponent1_cards = dealt_cards[f'player2Cards']
            opponent2_cards = dealt_cards[f'player3Cards']
            opponent3_cards = dealt_cards[f'player4Cards']
        elif player_id == 2:
            player_cards = dealt_cards[f'player2Cards']
            opponent1_cards = dealt_cards[f'player3Cards']
            opponent2_cards = dealt_cards[f'player4Cards']
            opponent3_cards = dealt_cards[f'player1Cards']
        elif player_id == 3:
            player_cards = dealt_cards[f'player3Cards']
            opponent1_cards = dealt_cards[f'player4Cards']
            opponent2_cards = dealt_cards[f'player1Cards']
            opponent3_cards = dealt_cards[f'player2Cards']
        else:
            player_cards = dealt_cards[f'player4Cards']
            opponent1_cards = dealt_cards[f'player1Cards']
            opponent2_cards = dealt_cards[f'player2Cards']
            opponent3_cards = dealt_cards[f'player3Cards']
        socketio.emit('cards_dealt4',
                      {'player_id': player_id, 'playerCards': player_cards, 'opponent1Cards': opponent1_cards,
                       'opponent2Cards': opponent2_cards, 'opponent3Cards': opponent3_cards, }, room=session_id)


@app.route('/game4player')
def index4():
    return render_template('game4player.html')


@app.route('/result4')
def result4():
    return render_template('result4.html')


@app.route('/api/get_cards4', methods=['GET'])
def get_cards4():
    cards_data = deal_cards4()
    return jsonify(cards_data)


@app.route('/api/draw_card4', methods=['POST'])
def draw_card4():
    data = request.json
    player_index = data['playerIndex']
    opponent_index = data['opponentIndex']
    card_index = data['cardIndex']

    # 从对手手中移除并添加到玩家手中
    card = hands[opponent_index].pop(card_index)
    hands[player_index].append(card)
    return jsonify({
        'playerCards': hands[player_index],
        'opponent1Cards': hands[1],
        'opponent2Cards': hands[2],
        'opponent3Cards': hands[3],
    })


@socketio.on('draw_card4')
def handle_draw_card4(data):
    global current_player_turn, player_scores
    player_id = data['player_id']
    if player_id != current_player_turn:
        emit('not_your_turn4', {'message': '当前不是您的回合'}, room=request.sid)
        return
    opponent_id = data['opponent_id']
    card_index = data['card_index']
    player_index = player_to_hand_index[player_id]
    opponent_index = player_to_hand_index[opponent_id]
    # 检查目标玩家是否有牌
    if not hands[player_index]:
        # 如果目标玩家没有牌，则跳过当前玩家的回合
        current_player_turn = update_next_turn4(current_player_turn)
        print(current_player_turn)
        emit('update_turn4', {'currentPlayerTurn': current_player_turn}, broadcast=True)
        return
    card = hands[opponent_index].pop(card_index)
    if not hands[player_index]:
        update_finish_order4(player_index)
    if card not in out_cards:  # 只有未打出的牌才能被添加
        hands[player_index].append(card)
    if not hands[opponent_index]:
        update_finish_order4(opponent_index)
    # 广播更新到所有客户端
    for session_id, p_id in players.items():
        player_cards = hands[player_to_hand_index[p_id]]
        # 确保对手牌组被正确分配
        if p_id == 1:
            opponent1_cards = hands[player_to_hand_index[2]]
            opponent2_cards = hands[player_to_hand_index[3]]
            opponent3_cards = hands[player_to_hand_index[4]]
        elif p_id == 2:
            opponent1_cards = hands[player_to_hand_index[3]]
            opponent2_cards = hands[player_to_hand_index[4]]
            opponent3_cards = hands[player_to_hand_index[1]]
        elif p_id == 3:
            opponent1_cards = hands[player_to_hand_index[4]]
            opponent2_cards = hands[player_to_hand_index[1]]
            opponent3_cards = hands[player_to_hand_index[2]]
        else:
            opponent1_cards = hands[player_to_hand_index[1]]
            opponent2_cards = hands[player_to_hand_index[2]]
            opponent3_cards = hands[player_to_hand_index[3]]
        socketio.emit('cards_updated4',
                      {'player_id': p_id, 'playerCards': player_cards, 'opponent1Cards': opponent1_cards,
                       'opponent2Cards': opponent2_cards, 'opponent3Cards': opponent3_cards, 'outCards': out_cards},
                      room=session_id)
    if is_switch_active == False:
        if current_player_turn == 1:
            current_player_turn = 4
            if not hands[3]:
                current_player_turn = 3
                if not hands[2]:
                    current_player_turn = 2
                    if not hands[1]:
                        print("over")
        elif current_player_turn == 4:
            current_player_turn = 3
            if not hands[2]:
                current_player_turn = 2
                if not hands[1]:
                    current_player_turn = 1
                    if not hands[0]:
                        print("over")
        elif current_player_turn == 2:
            current_player_turn = 1
            if not hands[0]:
                current_player_turn = 4
                if not hands[3]:
                    current_player_turn = 3
                    if not hands[2]:
                        print("over")
        else:
            current_player_turn = 2
            if not hands[1]:
                current_player_turn = 1
                if not hands[0]:
                    current_player_turn = 4
                    if not hands[3]:
                        print("over")
    else:
        if current_player_turn == 1:
            current_player_turn = 2
            if not hands[1]:
                current_player_turn = 3
                if not hands[2]:
                    current_player_turn = 4
                    if not hands[3]:
                        print("over")
        elif current_player_turn == 4:
            current_player_turn = 1
            if not hands[0]:
                current_player_turn = 2
                if not hands[1]:
                    current_player_turn = 3
                    if not hands[2]:
                        print("over")
        elif current_player_turn == 2:
            current_player_turn = 3
            if not hands[2]:
                current_player_turn = 4
                if not hands[3]:
                    current_player_turn = 1
                    if not hands[0]:
                        print("over")
        else:
            current_player_turn = 4
            if not hands[3]:
                current_player_turn = 1
                if not hands[0]:
                    current_player_turn = 2
                    if not hands[1]:
                        print("over")
    emit('update_turn4', {'currentPlayerTurn': current_player_turn}, broadcast=True)
    over4()


def update_next_turn4(current_player_turn):
    # 根据当前玩家回合更新下一个玩家回合
    if is_switch_active == False:
        if current_player_turn == 1:
            next_player_turn = 4
        elif current_player_turn == 4:
            next_player_turn = 3
        elif current_player_turn == 3:
            next_player_turn = 2
        elif current_player_turn == 2:
            next_player_turn = 1
        # 检查并跳过无牌玩家
        while not player_has_cards[next_player_turn]:
            if next_player_turn == 1:
                next_player_turn = 4
            elif next_player_turn == 4:
                next_player_turn = 3
            elif next_player_turn == 3:
                next_player_turn = 2
            elif next_player_turn == 2:
                next_player_turn = 1
    else:
        if current_player_turn == 1:
            next_player_turn = 2
        elif current_player_turn == 2:
            next_player_turn = 3
        elif current_player_turn == 3:
            next_player_turn = 4
        elif current_player_turn == 4:
            next_player_turn = 1
        # 检查并跳过无牌玩家
        while not player_has_cards[next_player_turn]:
            if next_player_turn == 1:
                next_player_turn = 2
            elif next_player_turn == 2:
                next_player_turn = 3
            elif next_player_turn == 3:
                next_player_turn = 4
            elif next_player_turn == 4:
                next_player_turn = 1

    return next_player_turn


@app.route('/api/pairs4', methods=['POST'])
def pairs4():
    data = request.json
    player_id = data['player_id']  # 从请求中获取 player_id
    new_player_cards = data.get('newPlayerCards')
    # 从 player_id 获取手牌索引
    player_index = player_to_hand_index.get(player_id)
    # 更新玩家的手牌
    global hands
    if new_player_cards is not None:
        hands[player_index] = new_player_cards
    print("Updated hands:", hands[player_index])
    return jsonify({
        'playerCards': hands[player_index],
        # 返回其他需要的信息
    })


@socketio.on('play_pairs4')
def handle_play_pairs4(data):
    global current_player_turn, player_scores
    player_id = data['player_id']
    pairs = data['pairs']
    new_player_cards = data['newPlayerCards']
    # 从 player_id 获取手牌索引
    global hands
    player_index = player_to_hand_index[player_id]
    hands[player_index] = new_player_cards
    if not hands[player_index]:
        update_finish_order4(player_index)
    # 将打出的对子牌添加到 out_cards
    for pair in pairs:
        out_cards.extend(pair)
    # 更新所有客户端
    for session_id, p_id in players.items():
        player_cards = hands[player_to_hand_index[p_id]]
        # 确保对手牌组被正确分配
        if p_id == 1:
            opponent1_cards = hands[player_to_hand_index[2]]
            opponent2_cards = hands[player_to_hand_index[3]]
            opponent3_cards = hands[player_to_hand_index[4]]
        elif p_id == 2:
            opponent1_cards = hands[player_to_hand_index[3]]
            opponent2_cards = hands[player_to_hand_index[4]]
            opponent3_cards = hands[player_to_hand_index[1]]
        elif p_id == 3:
            opponent1_cards = hands[player_to_hand_index[4]]
            opponent2_cards = hands[player_to_hand_index[1]]
            opponent3_cards = hands[player_to_hand_index[2]]
        else:
            opponent1_cards = hands[player_to_hand_index[1]]
            opponent2_cards = hands[player_to_hand_index[2]]
            opponent3_cards = hands[player_to_hand_index[3]]
        socketio.emit('cards_updated4',
                      {'player_id': p_id, 'playerCards': player_cards, 'opponent1Cards': opponent1_cards,
                       'opponent2Cards': opponent2_cards, 'opponent3Cards': opponent3_cards, 'outCards': out_cards},
                      room=session_id)
    over4()
    


@app.route('/api/swap_cards4', methods=['POST'])
def swap_cards4():
    global hands
    data = request.json
    hands[0] = data['playerCards']
    hands[1] = data['opponent1Cards']
    hands[2] = data['opponent2Cards']
    hands[3] = data['opponent3Cards']
    # 检查是否有 swapOpponentIndex 参数，并且它不是 None
    swap_opponent_index = data.get('swapOpponentIndex')
    if swap_opponent_index is not None:
        print(f"Shuffling opponent {swap_opponent_index} hand")
        shuffle_hand4(swap_opponent_index)

    return jsonify({'message': 'Cards updated successfully'})


@socketio.on('swap_cards4')
def handle_swap_cards4(data):
    player_id = data['player_id']
    target_player_id = data['target_player_id']
    playerCards = data['playerCard']
    opponentCards = data['opponentCard']
    outcards = data['outCards']  # 接收更新后的废牌堆
    print(outcards)
    last_element = outcards[-1]  # 获取最后一个元素，即 "swap"
    out_cards.append(last_element)  # 更新废牌堆
    print(out_cards)
    if player_id == 1:
        if target_player_id == 1:
            target_player_id = 2
        elif target_player_id == 2:
            target_player_id = 3
        elif target_player_id == 3:
            target_player_id = 4
    elif player_id == 2:
        if target_player_id == 1:
            target_player_id = 3
        elif target_player_id == 2:
            target_player_id = 4
        elif target_player_id == 3:
            target_player_id = 1
    elif player_id == 3:
        if target_player_id == 1:
            target_player_id = 4
        elif target_player_id == 2:
            target_player_id = 1
        elif target_player_id == 3:
            target_player_id = 2
    elif player_id == 4:
        if target_player_id == 1:
            target_player_id = 1
        elif target_player_id == 2:
            target_player_id = 2
        elif target_player_id == 3:
            target_player_id = 3
    print(playerCards)
    # 更新玩家的手牌
    hands[player_id - 1] = playerCards
    hands[target_player_id - 1] = opponentCards
    for session_id, p_id in players.items():
        player_cards = hands[player_to_hand_index[p_id]]
        if p_id == 1:
            opponent1_cards = hands[player_to_hand_index[2]]
            opponent2_cards = hands[player_to_hand_index[3]]
            opponent3_cards = hands[player_to_hand_index[4]]
        elif p_id == 2:
            opponent1_cards = hands[player_to_hand_index[3]]
            opponent2_cards = hands[player_to_hand_index[4]]
            opponent3_cards = hands[player_to_hand_index[1]]
        elif p_id == 3:
            opponent1_cards = hands[player_to_hand_index[4]]
            opponent2_cards = hands[player_to_hand_index[1]]
            opponent3_cards = hands[player_to_hand_index[2]]
        else:
            opponent1_cards = hands[player_to_hand_index[1]]
            opponent2_cards = hands[player_to_hand_index[2]]
            opponent3_cards = hands[player_to_hand_index[3]]
        socketio.emit('cards_updated4',
                      {'player_id': p_id, 'playerCards': player_cards, 'opponent1Cards': opponent1_cards,
                       'opponent2Cards': opponent2_cards, 'opponent3Cards': opponent3_cards, 'outCards': out_cards},
                      room=session_id)


@socketio.on('deal_cards4')
def handle_deal_cards4(data):
    dealt_cards = deal_cards4()  # 发牌逻辑
    for session_id, player_id in players.items():
        player_cards = dealt_cards[f'player{player_id}Cards']
        opponent1_cards = dealt_cards[f'player{(player_id % 4) + 1}Cards']
        opponent2_cards = dealt_cards[f'player{((player_id + 1) % 4) + 1}Cards']
        opponent3_cards = dealt_cards[f'player{(((player_id + 1) % 4) + 1) % 4 + 1}Cards']
        socketio.emit('cards_dealt4',
                      {'player_id': player_id, 'playerCards': player_cards, 'opponent1Cards': opponent1_cards,
                       'opponent2Cards': opponent2_cards, 'opponent3Cards': opponent3_cards}, room=session_id)


@socketio.on('play_switch_card4')
def handle_play_switch_card4(data):
    global is_switch_active, currentPlayerTurnId
    player_id = data['player_id']
    switch_card_index = data['card_index']  # 获取 switch 牌的索引
    # 将 switch 牌从玩家手牌移除并加入废牌堆
    switch_card = hands[player_to_hand_index[player_id]].pop(switch_card_index)
    out_cards.append(switch_card)
    # 更新 switch 状态
    is_switch_active = not is_switch_active
    # 广播更新到所有客户端
    for session_id, p_id in players.items():
        player_cards = hands[player_to_hand_index[p_id]]
        # 确保对手牌组被正确分配
        if p_id == 1:
            opponent1_cards = hands[player_to_hand_index[2]]
            opponent2_cards = hands[player_to_hand_index[3]]
            opponent3_cards = hands[player_to_hand_index[4]]
        elif p_id == 2:
            opponent1_cards = hands[player_to_hand_index[3]]
            opponent2_cards = hands[player_to_hand_index[4]]
            opponent3_cards = hands[player_to_hand_index[1]]
        elif p_id == 3:
            opponent1_cards = hands[player_to_hand_index[4]]
            opponent2_cards = hands[player_to_hand_index[1]]
            opponent3_cards = hands[player_to_hand_index[2]]
        else:
            opponent1_cards = hands[player_to_hand_index[1]]
            opponent2_cards = hands[player_to_hand_index[2]]
            opponent3_cards = hands[player_to_hand_index[3]]
        socketio.emit('cards_updated4',
                      {'player_id': p_id, 'playerCards': player_cards, 'opponent1Cards': opponent1_cards,
                       'opponent2Cards': opponent2_cards, 'opponent3Cards': opponent3_cards, 'outCards': out_cards},
                      room=session_id)
    emit('switch_status_changed4', {'isSwitchActive': is_switch_active}, broadcast=True)


@socketio.on('end_turn4')
def handle_end_turn4(data):
    global current_player_turn
    player_id = data['player_id']
    if player_id == current_player_turn:
        if is_switch_active == False:
            if current_player_turn == 1:
                current_player_turn = 4
                if not hands[3]:
                    current_player_turn = 3
                    if not hands[2]:
                        current_player_turn = 2
                        if not hands[1]:
                            print("over")
            elif current_player_turn == 4:
                current_player_turn = 3
                if not hands[2]:
                    current_player_turn = 2
                    if not hands[1]:
                        current_player_turn = 1
                        if not hands[0]:
                            print("over")
            elif current_player_turn == 2:
                current_player_turn = 1
                if not hands[0]:
                    current_player_turn = 4
                    if not hands[3]:
                        current_player_turn = 3
                        if not hands[2]:
                            print("over")
            else:
                current_player_turn = 2
                if not hands[1]:
                    current_player_turn = 1
                    if not hands[0]:
                        current_player_turn = 4
                        if not hands[3]:
                            print("over")
        else:
            if current_player_turn == 1:
                current_player_turn = 2
                if not hands[1]:
                    current_player_turn = 3
                    if not hands[2]:
                        current_player_turn = 4
                        if not hands[3]:
                            print("over")
            elif current_player_turn == 4:
                current_player_turn = 1
                if not hands[0]:
                    current_player_turn = 2
                    if not hands[1]:
                        current_player_turn = 3
                        if not hands[2]:
                            print("over")
            elif current_player_turn == 2:
                current_player_turn = 3
                if not hands[2]:
                    current_player_turn = 4
                    if not hands[3]:
                        current_player_turn = 1
                        if not hands[0]:
                            print("over")
            else:
                current_player_turn = 4
                if not hands[3]:
                    current_player_turn = 1
                    if not hands[0]:
                        current_player_turn = 2
                        if not hands[1]:
                            print("over")
            emit('update_turn4', {'currentPlayerTurn': current_player_turn}, broadcast=True)
    else:
        emit('error', {'message': '不是您的回合'}, room=request.sid)


def over4():
    global current_player_turn, player_scores
    update_player_cards_status4()  # 更新玩家手中牌的状态
    players_with_cards_count = sum(1 for cards in hands if cards)
    if players_with_cards_count <= 1:
        formatted_scores = calculate_scores4()
        emit('game_over4', {'playerScores': formatted_scores}, broadcast=True)


def update_player_cards_status4():
    global player_has_cards, hands
    for player_id, cards in enumerate(hands, start=1):
        player_has_cards[player_id] = bool(cards)  # 如果玩家手中还有牌，则为 True

def update_finish_order4(player_id):
    global finish_order4
    if player_id+1 not in finish_order4:
        player_id=player_id+1
        print(f"Player {player_id} finished")
        finish_order4.append(player_id)

def calculate_scores4():
    global player_scores, finish_order4

    score_values = [45, 30, 15, 0]  # 根据完成顺序的积分
    max_scores_idx = len(score_values) - 1  # 最大索引

    for idx, player_id in enumerate(finish_order4):
        score_idx = min(idx, max_scores_idx)  # 确保索引不会超出范围
        player_scores[player_id] = score_values[score_idx]

    # 如果有玩家没有在 finish_order 中，给他们最低分
    for player_id in range(1, 5):
        if player_id not in finish_order4:
            player_scores[player_id] = score_values[-1]

    print("游戏结束！玩家积分如下：")
    for player_id, score in player_scores.items():
        print(f"玩家 {player_id}: {score} 分")

    return player_scores



if __name__ == '__main__':
    socketio.run(app)
