import asyncio
import socket

import friendly_async


async def hi():
    event_loop = asyncio.get_event_loop()

    listen_sock = None
    try:
        count = [3]

        print("Getting local address info")
        listen_addrs = await event_loop.getaddrinfo(
            "::",
            8008,
            family=socket.AF_INET6,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
            flags=socket.AI_PASSIVE,
        )
        assert len(listen_addrs) == 1, listen_addrs

        family, type_, proto, canonname, sockaddr = listen_addrs[0]
        print(f"Binding to {sockaddr} (family {family!r})")
        listen_sock = socket.socket(
            family=family,
            type=(type_ | socket.SOCK_NONBLOCK),
            proto=proto,
        )
        listen_sock.bind(sockaddr)
        listen_sock.listen(1)

        print("Ready to accept connections")
        while True:
            print("Waiting for a connection")
            sock, address = await event_loop.sock_accept(listen_sock)
            print(f"Accepted a connection from {address}")
            if count[0] == 0:
                await event_loop.sock_sendall(sock, b"\x00\x01\x03hi!")
                print("Closing connection")
                sock.close()
            else:
                print("Sending 'hi!'")
                await event_loop.sock_sendall(sock, b"\x00\x01\x03hi!")
                print("Waiting for peer to shutdown socket")
                while len(await event_loop.sock_recv(sock, 1024)) != 0:
                    print("Still waiting")
                print("Shutting down socket")
                sock.shutdown(socket.SHUT_WR)
                sock.close()

    finally:
        if listen_sock is not None:
            print("Closing listen socket")
            listen_sock.close()

    print("Returning 4")
    return 4


def main():
    thread = friendly_async.EventLoopThread()
    thread.start()
    try:
        f = friendly_async.loud_run(hi(), thread.event_loop)
        print(f.result())
    except:
        f.cancel()
        raise


if __name__ == "__main__":
    main()
