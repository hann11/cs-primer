conn, addr = server.accept()

conn is a new socket object that can be used to send and receive data on the connection. addr is the address bound to the socket on the other end of the connection. It is a tuple containing the IP address and port number of the other end of the connection.

oz: whenyou have a server, catch all exceptions to prevent someone crashing your server

you should constantly check recv() over and over to ensure you receive all the data
how to know when to stop? there should be a header content length that tells you how much data to expect, for a post request
get requests don't have a body, so you can just stop when you receive an empty string?
