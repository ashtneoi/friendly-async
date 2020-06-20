import friendly_async


async def hi():
    print("hi!")
    raise Exception("oh noooo")
    return 4


def main():
    thread = friendly_async.EventLoopThread()
    thread.start()
    f = friendly_async.loud_run(hi(), thread.event_loop)
    print(f.result())


if __name__ == "__main__":
    main()
