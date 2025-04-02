import json
import socket


def echo_http_headers(port: int = 8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))
    server.listen()

    try:
        while True:
            print(f"Listening for new connections on port {port}")

            conn, addr = server.accept()
            print(f"Accepted connection: {conn} on address {addr}")

            try:
                while True:
                    data = conn.recv(1000)
                    if not data:
                        break
                    data = data.decode("utf-8")

                    request_lines = data.split("\r\n")
                    request_info = request_lines[0]
                    print(f"Received request with topline info: {request_info}")
                    headers = request_lines[1:]

                    header_dict = {}
                    header_dict["http_method"] = request_info.split(" ")[0]
                    header_dict["http_path"] = request_info.split(" ")[1]
                    header_dict["http_version"] = request_info.split(" ")[2]
                    for header in headers:
                        if len(header) > 0:
                            key, val = header.split(": ")
                            header_dict[key] = val
                    json_headers = json.dumps(header_dict)
                    response = f"""HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(json_headers)}\r\n\r\n{json_headers}""".encode(
                        "utf-8"
                    )

                    conn.send(response)
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


if __name__ == "__main__":
    echo_http_headers(8080)
