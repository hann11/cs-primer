import json
import socket


def echo_tcp(port: int = 8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))
    server.listen()

    print(f"Listening for new connections on port {port}")

    while True:
        conn, addr = server.accept()  # conn is another socket
        print(f"Accepted connection from address {addr}")

        while True:
            data = conn.recv(1000)
            if not data:  # connection not closed
                break
            conn.send(data)
            print(f"Sent: {data}")

        conn.close()


def echo_http_headers(port: int = 8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))
    server.listen()

    print(f"Listening for new connections on port {port}")

    while True:
        conn, addr = server.accept()  # conn is another socket
        print(f"Accepted connection from address {addr}")

        while True:
            request = conn.recv(
                1000
            )  # request might be in more than one packet, this wont work. how do you know when you have the full request?
            # for post you need content length!!!!
            if not request:  # connection not closed
                break

            decoded_request = request.decode("utf-8")
            request_lines = decoded_request.split("\r\n")

            request_info = request_lines[0]
            print(f"Received request with topline info: {request_info}")
            headers = request_lines[1:-2]

            header_dict = {}

            for header in headers:
                if len(header) > 0:
                    key, val = header.split(": ")
                    header_dict[key] = val

            json_headers = json.dumps(header_dict)

            response = f"""
            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: {len(json_headers)}

            {json_headers}
            """.encode("utf-8")

            conn.send(json_headers.encode("utf-8"))
            print(f"Sent: {response}")

        conn.close()


if __name__ == "__main__":
    echo_http_headers(8081)
