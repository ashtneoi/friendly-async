import asyncio
import concurrent.futures
import sys
import threading
import traceback


class EventLoopThread(threading.Thread):
    def __init__(self):
        self.event_loop = asyncio.new_event_loop()
        super().__init__()

    def run(self):
        asyncio.set_event_loop(self.event_loop)

        self.event_loop_closed = threading.Event()

        try:
            self.event_loop.run_forever()
        finally:
            self.event_loop.run_until_complete(
                self.event_loop.shutdown_asyncgens()
            )
            self.event_loop.close()
            self.event_loop_closed.set()

    def join(self, timeout=None):
        self.event_loop.call_soon_threadsafe(self.event_loop.stop)
        self.event_loop_closed.wait(timeout)
        return super().join(timeout=0.2)


async def loud_call(coro):
    try:
        return await coro
    except Exception as e:
        # if not isinstance(e, concurrent.futures.CancelledError):
        traceback.print_exc(file=sys.stderr)
        raise


def loud_run(coro, loop):
    return asyncio.run_coroutine_threadsafe(loud_call(coro), loop)
