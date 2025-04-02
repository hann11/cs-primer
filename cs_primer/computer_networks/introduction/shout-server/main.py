import socket


def tcp_socket_server(port: int = 8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))
    server.listen()

    try:
        while True:
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
            finally:
                conn.close()
                print("Connection closed.")
    except KeyboardInterrupt:
        print("Server shutting down.")
        server.close()

    finally:
        server.close()
        print("Server closed.")


def udp_socket_server(port: int = 8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("", port))

    # udp connection - don't need to receive connections and hold, no tcp handshake
    try:
        while True:
            data, address = server.recvfrom(1000)

            data = data.decode("utf-8")
            print(f"Received: {data} from {address}")

            shout = data.upper()

            server.sendto(shout.encode("utf-8"), address)
            print(f"Sent: {shout}")

    finally:
        server.close()


if __name__ == "__main__":
    tcp_socket_server()

# TCP
# >>> s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# >>> s.connect(("127.0.0.1", 8080))
# >>> s.send(b"hello")
# 5
# >>> s.recv(1000)
# b'HELLO'
# >>> s.fileno()

# UDP
# >>> s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# >>> s.sendto("hello".encode("utf-8"), ("127.0.0.1", 8080))
# >>> s.recvfrom(1000)
