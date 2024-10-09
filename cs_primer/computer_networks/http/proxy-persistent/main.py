import socket

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
    PORT = 8026
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_socket.bind(("", PORT))

    listening_socket.listen(1)  # only one connection at a time
    print(f"Listening for connections on port {PORT}")

    try:
        while True:
            incoming_connection, address = listening_socket.accept()

            print(f"Accepted connection with address {address}")

            while True:
                incoming_data = incoming_connection.recv(1000)

                print(f"Received {len(incoming_data)} bytes from client")

                # parse the incoming data for the Connection header. If it is keep-alive, then we will NOT break when no data is sent.

                decoded_data = incoming_data.decode("utf-8")
                info_header, body = decoded_data.split("\r\n\r\n")
                info_header = info_header.split("\r\n")
                info = info_header[0]
                for header in info_header[1:]:
                    key, val = header.split(": ")
                    if key == "Connection":
                        keepalive_str = val

                if not incoming_data and keepalive_str != "keep-alive":
                    print("No more incoming data, but keepalive connection")
                    break

                server_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM
                )
                server_socket.connect(("127.0.0.1", 9000))

                server_socket.send(incoming_data)
                print(f"Sent {len(incoming_data)} bytes from client")

                response_to_proxy = b""

                while True:
                    server_response_bytechunk = server_socket.recv(4096)
                    print(
                        f"Received {len(server_response_bytechunk)} bytes from server"
                    )
                    response_to_proxy += server_response_bytechunk
                    if not server_response_bytechunk:
                        # I think we need to send back to connection keep alive header here to prevent new conns
                        print(response_to_proxy)
                        incoming_connection.send(response_to_proxy)
                        print(
                            f"Sent {len(response_to_proxy)} bytes to client from server"
                        )
                        break

            # print(f"Closing connection with address {address}")
            # incoming_connection.close()

    except KeyboardInterrupt:
        incoming_connection.close()
