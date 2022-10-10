import snake.state as state_mod
import snake.ui as ui
import curses

import time

def init(state):
    state = ui.init(state)
    return state

def finish(state):
    ui.finish(state)


def run():
    curses.wrapper(run_wrapped)


def run_wrapped(stdscr):
    '''Entry point and main loop of the game'''

    # Init game state and variables
    state = state_mod.State()
    state = init(state)
    state.frame_win = stdscr
    interval = None
    reader = None

    try:
        # Draw screen
        state = ui.draw_screen(state)

        # Game loop until done

        time.sleep(2)

    finally:
        # Clean up
        finish(state)
