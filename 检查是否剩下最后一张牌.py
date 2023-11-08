import random

# 定义一副扑克牌，包括4种花色（红桃、方块、梅花、黑桃）和13个点数（2-10、J、Q、K、A）
suits = ['红桃', '方块', '梅花', '黑桃']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# 创建一副扑克牌
deck = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]

# 添加一张乌龟牌
turtle_card = {'suit': '乌龟', 'rank': '乌龟'}
deck.append(turtle_card)

# 洗牌
random.shuffle(deck)

# 发牌给玩家
players = [[] for _ in range(4)]
for i in range(4):
    for _ in range(len(deck) // 4):
        card = deck.pop()
        players[i].append(card)

# 检查是否只剩下最后一张牌（乌龟牌）
if not deck:
    print("只剩下最后一张牌（乌龟牌）")
else:
    print("发牌错误")
    exit()
