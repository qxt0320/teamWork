# game_manager.py
from threading import Timer


class GameManager:
    def __init__(self, socketio):
        """
        初始化游戏管理器。
        :param socketio: Flask-SocketIO的实例，用于发射和处理事件。
        """
        self.socketio = socketio
        self.games = {}  # 存储每个游戏房间的状态

    def start_draw_timer(self, room_id, card, drawer):
        """
        开始一个计时器，等待5秒后下家可以决定是否锁定这张牌。
        :param room_id: 游戏房间的ID。
        :param card: 被抽的卡牌。
        :param drawer: 抽卡的玩家。
        """

        def time_is_up():
            # 计时器时间到，通知下一名玩家可以锁定卡牌
            self.socketio.emit('lock_decision', {'card': card, 'drawer': drawer}, room=room_id)

        # 设置5秒的计时器
        timer = Timer(5.0, time_is_up)
        timer.start()
        # 存储计时器以便后续可能需要取消
        self.games[room_id]['draw_timer'] = timer

    def cancel_draw_timer(self, room_id):
        """
        取消之前设置的抽牌计时器。
        :param room_id: 游戏房间的ID。
        """
        timer = self.games[room_id].get('draw_timer')
        if timer:
            timer.cancel()

    def lock_card(self, room_id, card, locker):
        """
        锁定卡牌，并通知所有玩家。
        :param room_id: 游戏房间的ID。
        :param card: 要锁定的卡牌。
        :param locker: 锁定卡牌的玩家。
        """
        self.cancel_draw_timer(room_id)  # 取消计时器
        self.games[room_id]['locked_card'] = card  # 设置锁定卡牌的状态
        self.socketio.emit('card_locked', {'card': card, 'locker': locker}, room=room_id)

    def keep_or_redraw(self, room_id, drawer, decision):
        """
        处理玩家决定保持卡牌或重新抽取的逻辑。
        :param room_id: 游戏房间的ID。
        :param drawer: 抽卡的玩家。
        :param decision: 玩家的决定，'keep' 或 'redraw'。
        """
        if decision == 'keep':
            # 如果玩家决定保持当前卡牌
            self.socketio.emit('kept_card', {'card': self.games[room_id]['locked_card'], 'drawer': drawer},
                               room=room_id)
        elif decision == 'redraw':
            # 如果玩家决定重抽，需要实现重抽逻辑
            # TODO: 添加重抽卡牌的逻辑
            pass

        # 无论决定如何，清除锁定卡牌的状态
        self.games[room_id].pop('locked_card', None)
