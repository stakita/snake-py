import sys
import curses
from threading import Thread
import queue
import logging

import snake.event as event

log = logging.getLogger(__name__)


commands = {'STOP', 'DRAW_SCREEN', 'GAME_OVER'}

'''
    UiThread provides single threaded access to the curses library infrastructure.

'''

class UiThread(Thread):

    def __init__(self, event_queue, state):
        log.debug('__init__')
        Thread.__init__(self)
        self.stop_flag = False
        self.control_queue = queue.Queue()
        self.user_input_queue = event_queue
        self.state = state


    def stop(self):
        log.debug('stop')
        # self.stop_flag = True
        self.control_queue.put('STOP')


    def draw_screen(self):
        log.debug('draw_screen')
        self.control_queue.put('DRAW_SCREEN')


    def game_over(self):
        self.control_queue.put('GAME_OVER')


    def run(self):
        log.debug('run')

        self.init(self.state)

        done = False
        while not done:
            # log.debug('run - loop start')

            try:
                command = self.control_queue.get(block=False, timeout=0)

                if command == 'STOP':
                    done = True

                elif command == 'DRAW_SCREEN':
                    self._draw_screen(self.state)

                elif command == 'GAME_OVER':
                    self._game_over(self.state)

                else:
                    raise Exception('Unexpected command: {}'.format(command))

            except queue.Empty:

                # log.debug('run - call wait_for_input')
                ch = self.wait_for_input(self.state)
                if ch == curses.ERR:
                    # log.debug('run - returned curses.ERR')
                    pass
                else:
                    log.debug('run - queuing input {}'.format(ch))
                    self.user_input_queue.put(event.Event(event.EVENT_INPUT, ch))

        log.debug('run - call finish')
        self.finish(self.state)


    def init(self, state):
        log.debug('init')
        state.frame_win = curses.initscr()
        state.game_win = curses.newwin(state.height - 1, state.width, 1, 0)
        curses.raw()
        curses.cbreak()
        curses.noecho()
        state.frame_win.keypad(True)
        state.frame_win.nodelay(True)
        state.game_win.keypad(True)
        state.game_win.nodelay(True)
        self.hide_cursor()
        state.frame_win.clear()
        state.game_win.clear()

        return state


    def finish(self, state):
        log.debug('finish')
        self.show_cursor()
        curses.nocbreak()
        state.frame_win.keypad(False)
        state.frame_win.nodelay(False)
        state.game_win.keypad(False)
        state.game_win.nodelay(False)
        curses.echo()
        curses.endwin()


    # Refs:
    #   - https://en.wikipedia.org/wiki/ANSI_escape_code
    #   - https://realpython.com/lessons/ansi-escape-sequences/

    hide_cursor_sequence = '\x1b[?25l'
    show_cursor_sequence = '\x1b[?25h'


    def hide_cursor(self):
        sys.stdout.write(self.hide_cursor_sequence)
        sys.stdout.flush()


    def show_cursor(self):
        sys.stdout.write(self.show_cursor_sequence)
        sys.stdout.flush()


    def _draw_screen(self, state):
        state.frame_win.erase()
        state.frame_win.addstr(0, 2, 'Snake')
        self.update_score(state)
        state.game_win.erase()
        state.game_win.border('|', '|', '-', '-', '+', '+', '+', '+')

        self.draw_snake(state)
        self.draw_food(state)

        state.frame_win.refresh()
        state.game_win.refresh()

        return state


    def _game_over(self, state):
        self.center_text(state, ' GAME OVER ')
        state.frame_win.refresh()
        state.game_win.refresh()


    def draw_snake(self, state):
        for x, y in state.snake:
            state.game_win.move(y, x)
            state.game_win.addstr('#')


    def draw_food(self, state):
        if state.food:
            log.debug('state.food: {}'.format(state.food))
            x, y = state.food
            state.game_win.move(y, x)
            state.game_win.addstr('*')


    def center_text(self, state, text):
        y = state.height // 2
        x = (state.width - len(text)) // 2
        state.game_win.move(y, x)
        state.game_win.addstr(text)


    def update_score(self, state):
        state.frame_win.addstr(0, state.width - 20, str(state.score))


    def wait_for_input(self, state):
        return state.frame_win.getch()

if __name__ == '__main__':
    import state as state_mod
    import time

    state = state_mod.State()
    state.frame_win = curses.initscr()

    input_queue = queue.Queue()

    ui_thread = UiThread(input_queue, state)
    ui_thread.start()
    ui_thread.draw_screen()

    time.sleep(5)

    ui_thread.stop()

