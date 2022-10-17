import asyncio
import contextlib
import curses
import logging
from random import randint
import sys
import termios

import snake.state as state_mod

from snake.ui import UiThread
import snake.event as event

import queue

# TODO: add import checks
from timeloop import Timeloop
from datetime import timedelta

log = logging.getLogger(__name__)


KEY_UP = '_KEY_UP'
KEY_DOWN = '_KEY_DOWN'
KEY_LEFT = '_KEY_LEFT'
KEY_RIGHT = '_KEY_RIGHT'


@contextlib.contextmanager
def raw_mode(file):
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)


# Ref: https://stackoverflow.com/a/55505152
async def periodic(interval, func, *args, **kwargs):
    print('periodic - start')
    while True:
        print('periodic - loop')
        await asyncio.gather(
            func(*args, **kwargs),
            asyncio.sleep(interval),
        )


<<<<<<< HEAD
def init(state):
    state = place_snake(state)
    state = place_food(state)
    return state
=======
async def tick(state):
    print('tick')

    if not state.game_over:
        state = run_turn(state)
        # ui_thread.draw_screen()
        print('draw_screen')
    if state.game_over:
        # ui_thread.game_over()
        print('game_over')


async def keyboard_handler(state):
    reader = asyncio.StreamReader()
    loop = asyncio.get_event_loop()
    await loop.connect_read_pipe(lambda: asyncio.StreamReaderProtocol(reader), sys.stdin)

    with raw_mode(sys.stdin):
        stop = False
        escape_seq = False
        escape_state_1 = False

        while stop == False:

            key = chr(ord(await reader.read(1)))

            print('key: {} - {}'.format(repr(key), type(key)))

            # Ref: https://stackoverflow.com/a/69065464
            if not escape_seq and key == chr(27):
                print('esc 0')
                escape_seq == True
            else:

                if escape_state_1:
                    print('esc 1c')
                    match key:
                        case 'A':
                            handle_key(state, KEY_UP)
                        case 'B':
                            handle_key(state, KEY_DOWN)
                        case 'C':
                            handle_key(state, KEY_RIGHT)
                        case 'D':
                            handle_key(state, KEY_LEFT)
                    escape_seq = False
                    escape_state_1 = False
                else:
                    if key == '[':
                        print('esc 1a')
                        escape_state_1 = True
                    else:
                        print('esc 1b')
                        escape_seq = False
                        escape_state_1 = False

            if key == 'q':
                stop = True
>>>>>>> Synchronize implementations


async def run():
    # Init game state and variables
    state = state_mod.State()
    state = init(state)

    task = asyncio.create_task(keyboard_handler(state))
    asyncio.create_task(periodic(0.2, tick, state))

    await task


# async def run_core():
#     '''Entry point and main loop of the game'''
#     print('run_core - start')

#     with raw_mode(sys.stdin):

<<<<<<< HEAD
        # Timeloop has a default logging handler, remove it, so we only use our own handlers (avoids duplicate logs) logging.getLogger('timeloop').handlers.clear()
        logging.getLogger('timeloop').handlers.clear()

        tl.start()
        # ticker = asyncio.ensure_future(periodic(1, tick, event_queue))
        # await ticker
=======
#         # Init game state and variables
#         state = state_mod.State()
#         state = init(state)
>>>>>>> Synchronize implementations



#         # ui_thread = UiThread(event_queue, state)
#         # ui_thread.start()
#         # ui_thread.draw_screen()
#         # reader = asyncio.StreamReader()
#         # loop = asyncio.get_event_loop()
#         # await loop.connect_read_pipe(lambda: asyncio.StreamReaderProtocol(reader), sys.stdin)

#         # Timeloop has a default logging handler, remove it, so we only use our own handlers (avoids duplicate logs) logging.getLogger('timeloop').handlers.clear()
#         # logging.getLogger('timeloop').handlers.clear()

#         # tl.start()
#         # ticker = asyncio.ensure_future(periodic(1, tick, event_queue))
#         # await ticker

#         stop = False

#         try:
#             while stop == False:
#                 print('run_core - event_queue.get()')
#                 res = event_queue.get()
#                 print('run_core - got it')

#                 if res.type() == event.EVENT_TICK:
#                     if not state.game_over:
#                         state = run_turn(state)
#                         # ui_thread.draw_screen()
#                         print('draw_screen')
#                     if state.game_over:
#                         # ui_thread.game_over()
#                         print('game_over')
#                 elif res.type() == event.EVENT_INPUT:
#                     key = res.data()
#                     handle_key(state, key)
#                     if chr(key) == 'q':
#                         stop = True

#         except KeyboardInterrupt:
#             stop = True

#         finally:
#             # Clean up
#             # tl.stop()
#             # ui_thread.stop()
#             # ui_thread.join()
#             pass


def handle_key(state, key):
    log.debug('handle_key: {}'.format(key))
    print('handle_key: {}'.format(key))
    if key == KEY_UP and not state.previous in (state_mod.DIRECTION_DOWN, state_mod.DIRECTION_UP):
        log.debug('go up')
        state.direction = state_mod.DIRECTION_UP
    elif key == KEY_DOWN and not state.previous in (state_mod.DIRECTION_DOWN, state_mod.DIRECTION_UP):
        log.debug('go down')
        state.direction = state_mod.DIRECTION_DOWN
    elif key == KEY_LEFT and not state.previous in (state_mod.DIRECTION_LEFT, state_mod.DIRECTION_RIGHT):
        log.debug('go left')
        state.direction = state_mod.DIRECTION_LEFT
    elif key == KEY_RIGHT and not state.previous in (state_mod.DIRECTION_LEFT, state_mod.DIRECTION_RIGHT):
        log.debug('go right')
        state.direction = state_mod.DIRECTION_RIGHT
    return state


def init(state):
    state = place_snake(state)
    state = place_food(state)
    return state


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
    return next_head in state.snake


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
