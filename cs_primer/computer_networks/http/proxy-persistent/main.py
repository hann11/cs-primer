import random
import socket

from loguru import logger

PORT = random.randint(0, 0xFFFF)
OWN_ADDRESS = (
    "0.0.0.0",
    PORT,
)  # 0.0.0.0 is a wildcard address, listens on all interfaces on the machine
UPSTREAM_ADDRESS = (
    "127.0.0.1",
    9000,
)  # designated loopback address, refers to local machine, outbound and mirrored back to the os


if __name__ == "__main__":
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(OWN_ADDRESS)

    proxy_socket.listen()  # only one connection at a time
    logger.info(f"Listening for connections on {OWN_ADDRESS}")
    keepalive = False

    while True:
        try:  # avoid any errors that can crash your server, want it long running
            # while True:
            client_socket, client_address = proxy_socket.accept()

            logger.info(f"Accepted connection with address {client_address}")

            incoming_data = client_socket.recv(4096)

            req_headers, req_body = incoming_data.split(b"\r\n\r\n", 1)

            req, headers = req_headers.split(b"\r\n", 1)
            method, path, protocol = req.split(b" ")

            for header in headers.split(b"\r\n"):
                if header.startswith(b"Connection:"):
                    connection = header.split(b": ")[1].decode("utf-8")
                    if connection == "keep-alive":
                        keepalive = True
                    else:
                        keepalive = False

            logger.debug(
                f"Received request {method} {path} {protocol} with Connection: {connection}, total {len(incoming_data)} bytes from client"
            )

            upstream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            upstream_socket.connect(UPSTREAM_ADDRESS)

            upstream_socket.send(incoming_data)
            logger.debug(f"Sent {len(incoming_data)} bytes from client")

            response_to_proxy = b""

            while True:  # need to loop as packets might be split, in the case of response bodies governed by the content length header
                # curl (18): transfer closed with outstanding read data remaining
                # knows that server has to send content but connection is closed if we don't loop
                server_response_bytechunk = upstream_socket.recv(4096)
                logger.debug(
                    f"Received {len(server_response_bytechunk)} bytes from server"
                )
                response_to_proxy += server_response_bytechunk
                if not server_response_bytechunk:
                    client_socket.send(response_to_proxy)
                    logger.debug(
                        f"Sent {len(response_to_proxy)} bytes to client from server"
                    )
                    break

            # side note; one can open sockets in a context manager, with socket.socket() as s: as it is a file descriptor like object
            # that way, the socket is closed automatically when the block is exited

            # logger.debug(
            #     f"Closing client connection with address {client_address}"
            # )
            # client_socket.close()
            upstream_socket.close()
            logger.debug("Closed connection with server")

            if not keepalive:
                client_socket.close()
                logger.debug(
                    f"Closing client connection with address {client_address}"
                )

        except (
            ConnectionRefusedError
        ):  # if the server is down, we can't connect to it
            logger.error("Connection to server refused")
            resp_body = b"<html><body><h1>502 Bad Gateway</h1></body></html>"
            resp_req_headers = f"HTTP/1.1 502 Bad Gateway\r\nContent-Type: text/html\r\nContent-Length: {len(resp_body)}\r\n\r\n".encode(
                "utf-8"
            )
            client_socket.send(resp_req_headers + resp_body)

        except OSError as e:
            logger.error(f"An error occurred: {e}")
            resp_body = (
                b"<html><body><h1>500 Internal Server Error</h1></body></html>"
            )
            resp_req_headers = f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html\r\nContent-Length: {len(resp_body)}\r\n\r\n".encode(
                "utf-8"
            )
            client_socket.send(resp_req_headers + resp_body)

        finally:
            if upstream_socket:
                upstream_socket.close()
            if client_socket:
                client_socket.close()

    proxy_socket.close()
