import curses


def init(state):
    state.game_win = curses.newwin(state.height - 1, state.width, 1, 0)
    curses.raw()
    curses.cbreak()
    curses.noecho()
    state.game_win.keypad(True)
    # curses.curs_set(0)

    return state


def finish(state):
    curses.nocbreak()
    state.game_win.keypad(False)
    curses.echo()
    curses.endwin()


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
