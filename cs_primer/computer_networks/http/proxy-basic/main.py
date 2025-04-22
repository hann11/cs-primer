import random
import socket

PORT = random.randint(0, 0xFFFF)
OWN_ADDRESS = "0.0.0.0"
# 0.0.0.0 is a wildcard address, listens on all interfaces on the machine
UPSTREAM_ADDRESS = (
    "127.0.0.1",
    9000,
)  # designated loopback address, refers to local machine, outbound and mirrored back to the os


def proxy_server(port: int = PORT):
    proxy_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_s.bind((OWN_ADDRESS, PORT))
    proxy_s.listen()

    while True:
        try:
            print(f"Listening for new connections on port {port}")
            client_s, client_addr = proxy_s.accept()
            print(f"Accepted connection from client on address {client_addr}")
            client_s.settimeout(
                100
            )  # Set a timeout for the client socket, sometimes it hangs and wants to reconnect (marc.jpeg)

            while True:
                server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_s.connect(UPSTREAM_ADDRESS)

                # while True:
                print("AWAITING")
                # client_data = b""
                client_data = client_s.recv(4096)
                print("recv")

                if not client_data:
                    print("no data, closing")
                    server_s.close()
                    continue

                print(f"-> *     {len(client_data)}B")
                print(f"{client_data=}")

                req_headers, _ = client_data.split(b"\r\n\r\n", 1)
                _, headers = req_headers.split(b"\r\n", 1)
                print(_)

                for header in headers.split(b"\r\n"):
                    if header.startswith(b"Connection:"):
                        connection = header.split(b": ")[1].decode("utf-8")
                        print(f"Connection: {connection}")
                    if _.split(b"/")[2] == b"1.1":
                        connection = "keep-alive"
                    # todo else if http/1.1 then keepalive

                server_s.send(client_data)
                print(f"   * ->  {len(client_data)}B")

                proxy_resp = b""

                while True:
                    s_chunk = server_s.recv(4096)
                    print(f"   * <-  {len(s_chunk)}B")
                    proxy_resp += s_chunk

                    if not s_chunk:
                        proxy_resp = proxy_resp.replace(
                            b"HTTP/1.0", b"HTTP/1.1"
                        )
                        client_s.send(proxy_resp)
                        print(f"<- *     {len(proxy_resp)}B")
                        print(f"{proxy_resp[:50]=}")
                        break

                print("Closing server socket")
                server_s.close()

                if connection != "keep-alive":
                    print("Closing client socket")
                    client_s.close()  # TODO indent
                    break  # TODO INDENT

        except (
            ConnectionRefusedError
        ):  # if the server is down, we can't connect to it
            print("Connection to server refused")
            client_s.send(
                b"HTTP/1.1 502 Bad Gateway\r\n\r\n"  # 502 Bad Gateway
            )

        except OSError as e:
            print(f"An error occurred: {e}")
            client_s.send(
                b"HTTP/1.1 500 Internal Server Error\r\n\r\n"  # 500 Internal Server Error
            )


if __name__ == "__main__":
    proxy_server(PORT)
