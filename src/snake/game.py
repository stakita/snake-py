import curses
import time

import snake.state as state_mod

from snake.ui import UiThread
import snake.event as event

import queue

# TODO: add import checks
from timeloop import Timeloop
from datetime import timedelta

def run():
    curses.wrapper(run_wrapped)

tl = Timeloop()
event_queue = queue.Queue()

@tl.job(interval=timedelta(seconds=0.2))
def tick():
    global event_queue
    event_queue.put(event.Event(event.EVENT_TICK, None))


def init(state, main_screen):
    state = place_snake(state)
    state.frame_win = main_screen
    return state


def run_wrapped(stdscr):
    '''Entry point and main loop of the game'''

    # Init game state and variables
    state = state_mod.State()
    state = init(state, stdscr)


    ui_thread = UiThread(event_queue, state)
    ui_thread.start()
    ui_thread.draw_screen()

    tl.start()

    max_ticks = 100

    try:
        while max_ticks > 0:
            max_ticks -= 1
            # Draw screen
            ui_thread.draw_screen()

            # Game loop until done
            # time.sleep(2)

            res = event_queue.get()

            if res.type() == event.EVENT_TICK:
                state = run_turn(state)

            elif res.type() == event.EVENT_INPUT:
                ch = chr(res.data())
                print('got: {}'.format(ch))
                if ch == 'q':
                    break


    finally:
        # Clean up
        ui_thread.stop()
        tl.stop()


def run_turn(state):
    state.score += 1
    return state


def place_snake(state):
    state.snake.append((state.width // 2, state.height // 2))
    return state
