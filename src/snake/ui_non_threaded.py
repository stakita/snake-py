import sys
import curses
import queue
import logging

log = logging.getLogger(__name__)


commands = {'STOP', 'DRAW_SCREEN', 'GAME_OVER'}


def init(state):
    log.debug('init')

    state.frame_win = curses.initscr()
    state.game_win = curses.newwin(state.height - 1, state.width, 1, 0)

    hide_cursor()
    state.frame_win.clear()
    state.game_win.clear()

    log.debug('init - done')
    return state


def finish():
    log.debug('finish')
    show_cursor()
    curses.endwin()


# Refs:
#   - https://en.wikipedia.org/wiki/ANSI_escape_code
#   - https://realpython.com/lessons/ansi-escape-sequences/

HIDE_CURSOR_SEQUENCE = '\x1b[?25l'
SHOW_CURSOR_SEQUENCE = '\x1b[?25h'


def hide_cursor():
    sys.stdout.write(HIDE_CURSOR_SEQUENCE)
    sys.stdout.flush()


def show_cursor():
    sys.stdout.write(SHOW_CURSOR_SEQUENCE)
    sys.stdout.flush()



def draw_screen(state):
    log.debug('draw_screen')
    state.frame_win.erase()
    state.frame_win.addstr(0, 2, 'Snake')
    update_score(state)
    state.game_win.erase()
    state.game_win.border('|', '|', '-', '-', '+', '+', '+', '+')

    draw_snake(state)
    draw_food(state)

    state.frame_win.refresh()
    state.game_win.refresh()

    return state


def game_over(state):
    center_text(state, ' GAME OVER ')
    state.frame_win.refresh()
    state.game_win.refresh()


def draw_snake(state):
    for x, y in state.snake:
        state.game_win.move(y, x)
        state.game_win.addstr('#')


def draw_food(state):
    if state.food:
        log.debug('state.food: {}'.format(state.food))
        x, y = state.food
        state.game_win.move(y, x)
        state.game_win.addstr('*')


def center_text(state, text):
    y = state.height // 2
    x = (state.width - len(text)) // 2
    state.game_win.move(y, x)
    state.game_win.addstr(text)


def update_score(state):
    state.frame_win.addstr(0, state.width - 20, str(state.score))


if __name__ == '__main__':
    import state as state_mod
    import time

    state = state_mod.State()
    state.frame_win = curses.initscr()

    input_queue = queue.Queue()

    state = init(state)
    state = draw_screen(state)

    time.sleep(5)

    finish()

