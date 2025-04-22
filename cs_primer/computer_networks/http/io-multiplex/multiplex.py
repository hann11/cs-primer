import select
import socket

PORT = 8080
ADDRESS = ""


def multiplex_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ADDRESS, PORT))
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.listen()
    server.setblocking(0)

    sockets = [server]

    print(f"{sockets=}")

    try:
        while True:
            readable, _, _ = select.select(
                sockets, [], []
            )  # block until one of the sockets is ready
            print(f"{readable=}")

            for sock in readable:  # loop through all sockets that are ready
                if (
                    sock == server
                ):  # if the server socket is ready, it means a new connection
                    print(f"Listening for new connections on port {PORT}")
                    conn, addr = server.accept()
                    conn.setblocking(0)
                    sockets.append(conn)
                    print(f"Accepted connection: {conn} on address {addr}")
                else:  # if it's not the server socket, it's a client socket
                    data = sock.recv(1000)
                    if not data:
                        print("No data received, closing connection.")
                        sock.close()
                        sockets.remove(sock)
                        break

                    print(f"Received: {data}")
                    resp_line = b"HTTP/1.1 200 OK\r\n\r\n"

                    sock.send(resp_line)

    except KeyboardInterrupt:
        print("Server shutting down.")
        for sock in sockets:
            sock.close()

    finally:
        for sock in sockets:
            sock.close()
        print("Server closed.")


if __name__ == "__main__":
    multiplex_server()
