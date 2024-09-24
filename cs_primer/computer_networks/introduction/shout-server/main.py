import socket

if __name__ == "__main__":
    server = socket.socket()
    server.bind(("", 8081))
    server.listen()
    print("Server started")

    conn, addr = server.accept()

    while True:
        data = conn.recv(1000)
        data = data.decode("utf-8")
        print(f"Received: {data}")

        shout = data.upper()
        conn.send(shout.encode("utf-8"))
        print(f"Sent: {shout}")
