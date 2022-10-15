#!/usr/bin/env python3
'''main.py
Run snake game

Usage:
    main.py [-h | --help]

Options:
    None
'''
import logging
import sys

try:
    from docopt import docopt
except ImportError as e:
    installs = ['docopt']
    sys.stderr.write('Error: %s\nTry:\n    pip install --user %s\n' % (e, ' '.join(installs)))
    sys.exit(1)

import snake.game

def main():
    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    args = docopt(__doc__)
    snake.game.run()


if __name__ == '__main__':
    main()
