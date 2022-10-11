import sys
import curses


def init(state):
    state.game_win = curses.newwin(state.height - 1, state.width, 1, 0)
    curses.raw()
    curses.cbreak()
    curses.noecho()
    state.game_win.keypad(True)
    hide_cursor()

    return state


def finish(state):
    show_cursor()
    curses.nocbreak()
    state.game_win.keypad(False)
    curses.echo()
    curses.endwin()


# Refs:
#   - https://en.wikipedia.org/wiki/ANSI_escape_code
#   - https://realpython.com/lessons/ansi-escape-sequences/

hide_cursor_sequence = '\x1b[?25l'
show_cursor_sequence = '\x1b[?25l'


def hide_cursor():
    sys.stdout.write(hide_cursor_sequence)
    sys.stdout.flush()


def show_cursor():
    sys.stdout.write(show_cursor_sequence)
    sys.stdout.flush()


def draw_screen(state):
    state.frame_win.clear()
    state.frame_win.addstr(0, 2, 'Snake')
    update_score(state)
    state.game_win.clear()
    state.game_win.border('|', '|', '-', '-', '+', '+', '+', '+')

    draw_snake(state)
    draw_food(state)

    state.frame_win.refresh()
    state.game_win.refresh()


def draw_snake(state):
    for x, y in state.snake:
        state.game_win.move(y, x)
        state.game_win.addstr('#')


def draw_food(state):
    x, y = state.food
    state.game_win.move(y, x)
    state.game_win.addstr('*')


def update_score(state):
    state.frame_win.addstr(0, state.width - 20, str(state.score))
