
from re import S


class State:

    def __init__(self, width = 80, height= 24):
        self.width = width
        self.height = height
        self.frame_win = None
        self.game_win = None
        self.score = 0

        # TODO: remove
        self.snake = [(20, 20), (20, 21), (19, 21)]
        self.food = (16, 16)