import socket

PORT = 8082
ADDRESS = ""


def multiplex_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ADDRESS, PORT))
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.listen()

    try:
        while True:
            print(f"Listening for new connections on port {PORT}")

            conn, addr = server.accept()
            print(f"Accepted connection: {conn} on address {addr}")

            while True:
                data = conn.recv(1000)
                if not data:
                    print("No data received, closing connection.")
                    conn.close()
                    break

                print(f"Received: {data}")

                resp_body = b"<html><body><h1>Hello, World!</h1></body></html>"
                resp_line = b"HTTP/1.1 200 OK\r\n"
                resp_headers = b"Content-Type: text/html\r\n"
                resp_headers += (
                    b"Content-Length: "
                    + str(len(resp_body)).encode("utf-8")
                    + b"\r\n"
                )
                resp_headers += b"\r\n"
                resp = resp_line + resp_headers + resp_body

                print(f"sending resp {resp}")
                conn.send(resp)

    except KeyboardInterrupt:
        print("Server shutting down.")
        server.close()

    finally:
        server.close()
        print("Server closed.")


if __name__ == "__main__":
    multiplex_server()
