import curses
from random import randint
import time
import logging as log

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
    state.frame_win = main_screen
    state = place_snake(state)
    state = place_food(state)
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
    stop = False

    try:
        while max_ticks > 0 and stop == False:
            max_ticks -= 1
            # Draw screen

            # Game loop until done
            # time.sleep(2)

            res = event_queue.get()

            if res.type() == event.EVENT_TICK:
                if not state.game_over:
                    state = run_turn(state)
                    ui_thread.draw_screen()
                else:
                    ui_thread.game_over()

            elif res.type() == event.EVENT_INPUT:
                ch = chr(res.data())
                if ch == 'q':
                    stop = True

    except KeyboardInterrupt:
        stop = True

    finally:
        # Clean up
        ui_thread.stop()
        tl.stop()


def run_turn(state):
    next_head = next_snake_head(state.snake[0], state.direction)
    state.previous = state.direction

    if loses(state, next_head):
        state.game_over = True
    elif hits_food(state, next_head):
        state = grow_snake(state, next_head)
        state = place_food(state)
        state = incr_score(state)
    else:
        state = move_snake(state, next_head)

    return state


def place_snake(state):
    state.snake.append((state.width // 2, state.height // 2))
    return state


def grow_snake(state, next_head):
    state.snake.insert(0, next_head)
    return state


def move_snake(state, next_head):
    state.snake.pop()
    state.snake.insert(0, next_head)
    return state


def place_food(state):
    done = False
    while not done:
        location = (
            randint(1, state.width - 2),
            randint(1, state.height - 3)
        )

        if not hits_food(state, location):
            log.debug('setting food to: {}'.format(location))
            state.food = location
            done = True

    return state


def incr_score(state):
    state.score += 1
    return state


def loses(state, next_head):
    return hits_wall(state, next_head) or hits_snake(state, next_head)


def hits_wall(state, next_head):
    x_next, y_next = next_head
    return (x_next == 0
            or y_next == 0
            or x_next == state.width - 1
            or y_next == state.height - 2)


def hits_snake(state, next_head):
    return False


def hits_food(state, next_head):
    if state.food:
        return state.food == next_head
    return False


def next_snake_head(current_head, direction):
    x_curr, y_curr = current_head
    x_delta = 0
    y_delta = 0
    match direction:
        case state_mod.DIRECTION_UP:
            y_delta -= 1
        case state_mod.DIRECTION_DOWN:
            y_delta += 1
        case state_mod.DIRECTION_LEFT:
            x_delta -= 1
        case state_mod.DIRECTION_RIGHT:
            x_delta += 1
        case _:
            raise Exception('Unexpected direction')
    return (x_curr + x_delta, y_curr + y_delta)
