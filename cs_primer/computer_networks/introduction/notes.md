## tcp vs udp

https://csprimer.com/watch/tcp-udp/

udp is like tcp without features

both use ports to get a message to a destination process
both have src and dest ports

have 16bit checksums

otherwise udp doesn't have much else
doesn't handshake
doesn't setup a connection
no protocols

udp sockets - no connection, no state, no handshake

```
def tcp_socket_server(port: int = 8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))
    server.listen()

    conn, addr = server.accept()

    print(f"Accepted connection: {conn} on address {addr}")

    try:
        while True:
            data = conn.recv(1000)
            data = data.decode(
                "utf-8"
            )  # binary encoding is sent over the network, decode it
            if not data:
                break
            print(f"Received: {data}")

            shout = data.upper()
            conn.send(
                shout.encode("utf-8")
            )  # encode to binary and send over the network
            print(f"Sent: {shout}")
    except ConnectionResetError:
        print("Connection dropped.")
        conn.close()
        server.close()


def udp_socket_server(port: int = 8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("", port))

    try:
        while True:
            data, address = server.recvfrom(1000)

            data = data.decode("utf-8")
            print(f"Received: {data}")

            shout = data.upper()

            server.sendto(shout.encode("utf-8"), address)
            print(f"Sent: {shout}")

    finally:
        server.close()
```

above, created 2 socket servers.

first one is tcp, which requires SOCK_STREAM to create a tcp socket - this is connection based, must accept connection.

udp server needs DGRAM, doesnt require a connection to send/receieve data. can terminate the server and restart and still receive. cant for tcp.

trying to send to dead tcp server:

```
s.send(b"hello")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
BrokenPipeError: [Errno 32] Broken pipe
```

udp works tho