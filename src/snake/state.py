
from re import S

DIRECTION_UP = 'direction_up'
DIRECTION_DOWN = 'direction_down'
DIRECTION_LEFT = 'direction_left'
DIRECTION_RIGHT = 'direction_right'

class State:

    def __init__(self, width = 80, height= 24):
        self.width = width
        self.height = height
        self.frame_win = None
        self.game_win = None
        self.snake = []
        self.direction = DIRECTION_DOWN
        self.previous = DIRECTION_DOWN
        self.score = 0

        # TODO: remove
        self.food = (16, 16)