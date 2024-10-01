import json
import socket


def echo_tcp(port: int = 8080):
    """
    Part 1: Just echo anything that comes back from a TCP connection
    """
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
                print("CLOSED CONNECTION")
                break  # curl closes the connection after sending the request
            # chrome does not close the connection after sending the request
            # print("CLOSED CONNECTION")

            decoded_request = request.decode("utf-8")
            request_lines = decoded_request.split("\r\n")

            request_info = request_lines[0]
            print(f"Received request with topline info: {request_info}")
            headers = request_lines[1:-2]

            # note, we dont receive the ip/tcp headers here, as socket abstracts it
            # in tcp syn flood, no data was sent, just tcp handshake attempts (encapsulating ip)

            header_dict = {}

            for header in headers:
                if len(header) > 0:
                    key, val = header.split(": ")
                    header_dict[key] = val

            json_headers = json.dumps(header_dict)

            # note, http requires carriage return line feed at the end of the headers
            # and before the body, doubled
            response = f"""HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(json_headers)}\r\n\r\n{json_headers}""".encode(
                "utf-8"
            )

            # sometimes the connection stays open, blocking others.

            # response_no_body = f"""HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(json_headers)}\r\n\r\n""".encode(
            #     "utf-8"
            # )

            to_send = response
            # to_send = json_headers.encode("utf-8")

            conn.send(to_send)
            print(f"Sent: {to_send}")

        conn.close()


if __name__ == "__main__":
    echo_http_headers(8080)
