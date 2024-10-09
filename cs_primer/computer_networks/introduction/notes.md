## tcp vs udp

https://csprimer.com/watch/tcp-udp/

udp is like tcp without features

both use ports to get a message to a destination process
both have src and dest ports

have 16bit checksums

otherwise udp doesn't have much else
doesn't handshake
doesn't setup a connection
no protocols

udp sockets - no connection, no state, no handshake

```
def tcp_socket_server(port: int = 8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))
    server.listen()

    conn, addr = server.accept()

    print(f"Accepted connection: {conn} on address {addr}")

    try:
        while True:
            data = conn.recv(1000)
            data = data.decode(
                "utf-8"
            )  # binary encoding is sent over the network, decode it
            if not data:
                break
            print(f"Received: {data}")

            shout = data.upper()
            conn.send(
                shout.encode("utf-8")
            )  # encode to binary and send over the network
            print(f"Sent: {shout}")
    except ConnectionResetError:
        print("Connection dropped.")
        conn.close()
        server.close()


def udp_socket_server(port: int = 8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("", port))

    try:
        while True:
            data, address = server.recvfrom(1000)

            data = data.decode("utf-8")
            print(f"Received: {data}")

            shout = data.upper()

            server.sendto(shout.encode("utf-8"), address)
            print(f"Sent: {shout}")

    finally:
        server.close()
```

above, created 2 socket servers.

first one is tcp, which requires SOCK_STREAM to create a tcp socket - this is connection based, must accept connection.

udp server needs DGRAM, doesnt require a connection to send/receieve data. can terminate the server and restart and still receive. cant for tcp.

trying to send to dead tcp server:

```
s.send(b"hello")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
BrokenPipeError: [Errno 32] Broken pipe
```

udp works tho

## binding to a port

imagine a computer with 2 processes, a http server and a db server
the computer has an ip address

message hits computer, how does it know which process to send it to?

each process has a port number, sender sends message to port number

operating system has a table of port numbers and the process that is listening on that port

when a process binds to a port, it tells the os to send messages to that port to the process

process has a socket open and associated with a port

consider it like an apartment building, each apartment has a number, mailman delivers mail to the apartment number

## what is a socket?

an abstraction for syscalls to do with network stuff
returns a file descriptor
very operating system based, handles a lot of abstraction
user requests a socket via a syscall, OS handles it in kernel space and gives it back
socket socket.SOCK_STREAM, socket.AF_INET, sets up an ipv4, TCP connection
if you send data I think the ip and tcp parts are handled for you, probably the link/physical layer too

## network layer model

layer 7: application layer (http, dns)
layer 4: transport layer (tcp, udp)
layer 3: network layer (ip)
layer 1/2: link/physical layer (ethernet, wifi 802.11)

encapsulated and appended to eachother in a network packet
headers within each tell you info about it,
all in bytes

http has \r\n for newline b/w headers, \r\n\r\n for body after headers

## localhost

localhost is the hostname, what's interesting is that it uses the loopback interface. "virtual network" interface to sending something over the physical network
reflects back inside the operating system tcp/ip network stack

message addressed to localhost IP -> goes to network stack of OS, follows most same code paths, but doesn't go to a network card. Is reflected back, as if it arrived from the outside network.

## netcat

very useful utility

man nc

takes what you are typing into stdin, puts into socket. what comes back from the socket it cats to stdout.

```
nc -l 0.0.0.0 7777
```

```
nc 127.0.0.1 7777
```

^ loopback interface

above we are listening on all addresses so it should show up

ping on the bottom, receives on the top.
vice versa.

## what happens when you go to a browser and type wikipedia.org?

what's the first network protocol used, after pressing enter?

DNS: find host address of the webpage
we make a DNS query.

if maintaining a dns server, use tcp (for a zone transfer)

but usually for DNS, people use UDP.

need to go over the network to get DNS (in the past, had a local copy of hostnames to IP address)

IP is totally unusable for humans, Ipv4 has 32 bits, but Ipv6 has 128 bits - can't be used!
why don't we use hostnames for routing? good to have some hierachy for routing that ip address allows.

DNS is a binary encoded protocol (Http is not, has GET /)

Query:
Wikipedia.org, A record, type Internet.

which entity construct the DNS message?

OS usually constructs queries, it might feel like it does here for DNS, however it does not. The browser actually constructs it.

LAYER MODEL:
Layers utilise the underlying layers.

Application Layer (DNS, HTTP, SMTP, bittorrent, skype, whatever, so many of these). Layer 7

The APPLICATION (bitrrent client, browser etc,) must construct the query, parse, and implement the Application Layer protocol.

Transport Layer (Layer 4): TCP/UDP

back to the DNS Message. Chrome/The browser will construct it. It's a cstandard lib that can do it. It's not a system call.
"getaddrinfo" -> parse a hostname, formulate a struct.

not a syscall, but will underlying use syscalls.

No cstandard for HTTP, you need to construct yourself, or the browser.

aside:
TLS: open a socket (syscall), do a bunch of stuff in user space, to make the socket secure.
want to do https, you open a tls connection (socket from kernel, do user space stuff) then send encrypted over the socket.
why's that in user space?
whys tcp in the kernel?

say you had multiple apps on one machine, you need to get messages to the right port. better for OS to manage it.

takeaway: application implements the application layer protocol; byte packing. os won't support proprietary / whatever protocols.

DNS message is constructed.

what needs to be added on to get to the final destination?
you'd need a UDP header, and a destination port. (53 - pre-agreed for DNS). also a ones complement checksum

why is UDP good for DNS? TCP is meant to be reliable. We don't need reliable transport. Just retry if you want.
Why's TCP "reliable"? what's the ordering of a packet? generally send 1500 bytes per packet. DNS will easily fit into one packet.
UDP header is small. Doesn't require a handshake to establish a connection.
So many DNS queries. additional handshakes would be crazy.

If you want to send a video, want in order, without duplicates - TCP splits stuff up, gives them sequence numbers, retries based on failed packets. It gets difficult.

udp header; also has a source port. dns server then puts our port as the dest port when sending back.
port like an apt number after getting to the apt building.

which entity constructs the UDP header? the operating system.
man socket: browser constructs socket using socket syscall. uses an internet socket, SOCK_DGRAM.

what does the socket system call do with a tcp socket?

- socket.socket doesnt have an IP addres bound yet
- socket.send doesnt have an address.
- need the socket.connect syscall, it does the tcp handshake.

the browser constructs a socket (udp), send the dns message. KERNEL constructs the UDP header with ports etc.
how does it get to the dest port?!

Network LAYER (IP header) -> dest IP (8.8.8.8) google dns. source ip. ipv4 vs ipv6 diff headers.
ipv6 hopcount; no of machines/routers it can go along before its' dropped.
internet would fill up with bouncing packets if there wasn't a hopcount/ttl.

kernel does the IP header prepending. (socket.PF_INET).

ip address addresses a hostname, has lots of processes (port).
mac address is LOCAL. how to get the message to the router? to the physical device?

once it goes to internet, every router can forward to the dest address.

how to get it across? to router? to isp? etc?
src_mac address
dst_mac address for your router usually. send the message to the ROUTER.

what protocol can fill out mac address? ethernet is an example.

Link Layer (Layer 2) - Ethernet, 802.11 (wifi), Bluetooth, etc.

Primarily have a source and dest mac address.

Who constructs the ethernet header (and footer)? The network card.

source mac address comes from the network card, meant to be globally unique.
apple has assigned mac address space, give to you baked into network card.
network card computes footer (crc32)

OS gives destination mac.

Message (packet) goes to router. What does it do?

Router picks an exit to send messages to. Subnets / ranges of IP addresses.
If you have one ISP, it goes there. Depends on how many connections it has.

what's the next best hop to get closer to the destination?

Each router has a forwarding table -> want to get to 8.8.8.8.
8.x.x.x goes to a. 8.8.y.y goes to b.

8.8.y.y is better.

8.8.0.0/16 (first 16 bits - 65536 IP's) Subnet, sub network, logical grouping of IP addresses.

hardware has the algo to match.

what changes in the packet along the hop? UDP, DNS will stay the same. Src/Dst MAC are now different (before was for the router).

Diff Link layers between routers and devices etc.

Layered model is nice, can swap and change layers. Just stack bytes.

At each case, match the dest IP address against subnets at each routers.

IP layer will change - decrement the hopcount. Change the checksums.

Eventually, gets to the destination machine.
what happens?

the packet arrives with the stacked layers.
link layer -> network card, hands to OS.
unwrap IP and UDP header. bound dest port and a socket. the DNS server process.

DNS server looks up and gets the hostname back.
DNS server does it all in response, created a new packet. OS socket, UDP/IP header, Network card link layer.

IP address comes back to the original client.

Now, HTTP query, using a TCP socket, TCP header, dst port 80 for HTTP. IP header, ethernet header and footer.

same movement across the internet.
