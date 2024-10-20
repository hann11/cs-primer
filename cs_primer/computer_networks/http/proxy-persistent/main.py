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

    proxy_socket.listen(1)  # only one connection at a time
    logger.info(f"Listening for connections on {OWN_ADDRESS}")
    keepalive = False

    # while True:
    try:  # avoid any errors that can crash your server, want it long running
        while True:
            if not keepalive:
                client_socket, client_address = proxy_socket.accept()

                logger.info(
                    f"Accepted connection with address {client_address}"
                )

            incoming_data = client_socket.recv(4096)

            if not incoming_data:
                logger.debug("No more data from client")
                break

            logger.debug(f"Received {len(incoming_data)} bytes from client")
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
                f"Received request {req} with Connection: {connection}, total {len(incoming_data)} bytes from client"
            )

            upstream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            upstream_socket.connect(UPSTREAM_ADDRESS)

            upstream_socket.send(incoming_data)
            logger.debug(f"Sent {len(incoming_data)} bytes from client")

            response_to_proxy = b""

            while True:
                server_response_bytechunk = upstream_socket.recv(4096)
                logger.debug(
                    f"Received {len(server_response_bytechunk)} bytes from server"
                )
                response_to_proxy += server_response_bytechunk
                if not server_response_bytechunk:
                    response_to_proxy = response_to_proxy.replace(
                        b"HTTP/1.0", b"HTTP/1.1"
                    )
                    logger.debug(
                        "Modified response to client from HTTP/1.0 to HTTP/1.1"
                    )
                    logger.debug(response_to_proxy[:250])
                    client_socket.send(response_to_proxy)
                    logger.debug(
                        f"Sent {len(response_to_proxy)} bytes to client from server"
                    )
                    break

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
        logger.exception(f"An error occurred: {e}")
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
            logger.debug("Closed connection with server")
        if client_socket:
            client_socket.close()
            logger.debug(
                f"Closing client connection with address {client_address}"
            )

    proxy_socket.close()
