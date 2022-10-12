from concurrent.futures import thread
import curses
import time

import snake.state as state_mod
import snake.ui as ui
import snake.thread_input as thread_input

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


def run_wrapped(stdscr):
    '''Entry point and main loop of the game'''

    # Init game state and variables
    state = state_mod.State()
    state.frame_win = stdscr

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
            if res.type() == event.EVENT_INPUT:
                ch = chr(res.data())
                print('got: {}'.format(ch))

            elif res.type() == event.EVENT_TICK:
                print('tick')
                state.score += 1



    finally:
        # Clean up
        ui_thread.stop()
        tl.stop()
