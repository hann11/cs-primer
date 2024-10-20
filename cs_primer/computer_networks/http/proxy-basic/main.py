import socket

from loguru import logger

PORT = 8037
OWN_ADDRESS = (
    "0.0.0.0",
    PORT,
)  # 0.0.0.0 is a wildcard address, listens on all interfaces on the machine
UPSTREAM_ADDRESS = (
    "127.0.0.1",
    9000,
)  # designated loopback address, refers to local machine, outbound and mirrored back to the os

# TODO: implement a proxy socket, that forwards and returns responses from a server

# the server is hosted at localhost:9000

# plan:
# create a tcp socket, listening on a given PORT
# while True, wait for connection
# accept the connection
# listen for data, when it arrives:
# connect to the server using a socket
# While True, send data to server, receive response in parts, send response back to client
# close connection when no longer receiving data, or keyboard interrupt


if __name__ == "__main__":
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(OWN_ADDRESS)

    proxy_socket.listen()  # only one connection at a time
    logger.info(f"Listening for connections on {OWN_ADDRESS}")

    # while True:
    try:  # avoid any errors that can crash your server, want it long running
        while True:
            client_socket, client_address = proxy_socket.accept()

            logger.info(f"Accepted connection with address {client_address}")

            incoming_data = client_socket.recv(4096)
            # assuming the entire request is just one packet and fits in 4096 bytes
            # don't need recvfrom, because we are not using UDP, we are using TCP
            # 4096 is the buffer the OS can fill with data it's received
            # doesn't mean the packet is as large as 4096, just that the buffer can hold that much
            # might need to call it multiple times depending on the size of the packet

            # if not incoming_data: # don't need this atm just assuming one packet
            #     break

            logger.debug(f"Received {len(incoming_data)} bytes from client")

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

            logger.debug(
                f"Closing client connection with address {client_address}"
            )
            client_socket.close()
            upstream_socket.close()

    except (
        ConnectionRefusedError
    ):  # if the server is down, we can't connect to it
        logger.error("Connection to server refused")
        client_socket.send(
            b"HTTP/1.1 502 Bad Gateway\r\n\r\n"  # 502 Bad Gateway
        )

    except OSError as e:
        logger.error(f"An error occurred: {e}")
        client_socket.send(
            b"HTTP/1.1 500 Internal Server Error\r\n\r\n"  # 500 Internal Server Error
        )

    finally:
        client_socket.close()
        upstream_socket.close()

    proxy_socket.close()
