import random
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='static', static_url_path='/static')

hands = []
special_cards = ["turtle", "swap", "switch","switch"]


def deal_cards():
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

    hands = [[] for _ in range(4)]

    player_count = len(hands)
    cards_per_player = len(all_cards) // player_count

    for i in range(cards_per_player):
        for j in range(player_count):
            card = all_cards.pop(0)
            hands[j].append(card)

    player_cards = hands[0]
    opponent1_cards = hands[1]
    opponent2_cards = hands[2]
    opponent3_cards = hands[3]

    return {
        'playerCards': player_cards,
        'opponent1Cards': opponent1_cards,
        'opponent2Cards': opponent2_cards,
        'opponent3Cards': opponent3_cards,
        'specialCards': special_cards
    }


@app.route('/')
def index():
    return render_template('game4player.html')


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
        'opponent2Cards': hands[2],
        'opponent4Cards': hands[3],
    })

if __name__ == '__main__':
    app.run()
