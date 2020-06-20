import asyncio

import friendly_async


async def hi():
    print("hi!")
    return 4


def main():
    thread = friendly_async.EventLoopThread()
    thread.start()
    f = asyncio.run_coroutine_threadsafe(hi(), thread.event_loop)
    print(f.result())


if __name__ == "__main__":
    main()
