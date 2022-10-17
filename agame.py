import asyncio
import contextlib
import termios
import sys


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


async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    # return f


async def key_handler():
    reader = asyncio.StreamReader()
    loop = asyncio.get_event_loop()
    await loop.connect_read_pipe(lambda: asyncio.StreamReaderProtocol(reader), sys.stdin)

    with raw_mode(sys.stdin):
        # Init game state and variables
        stop = False

        while stop == False:

            key = ord(await reader.read(1))

            print('key: {} - {}'.format(repr(key), type(key)))

            if chr(key) == 'q':
                stop = True



async def periodic(interval, func, *args, **kwargs):
    while True:
        await asyncio.gather(
            func(*args, **kwargs),
            asyncio.sleep(interval),
        )


async def tick():
    # global event_queue
    # event_queue.put(event.Event(event.EVENT_TICK, None))
    print('tick')


async def main():
    # Schedule three calls *concurrently*:
    # L = await asyncio.gather(
    #     factorial("A", 2),
    #     factorial("B", 3),
    #     factorial("C", 4),
    # )
    # print(L)

    # task1 = asyncio.create_task(factorial('A', 2))
    # task2 = asyncio.create_task(factorial('B', 3))
    # task3 = asyncio.create_task(factorial('C', 4))
    task = asyncio.create_task(key_handler())
    ticker = asyncio.create_task(periodic(1, tick))

    # print('0')
    # await task1
    # print('1')
    # await task2
    print('2')
    await task
    print('3')
    # await factorial('C', 4)
    # await ticker
    print('main is done')

asyncio.run(main())
