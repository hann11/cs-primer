# Oz notes:
# 1. construct the query

# pass hostname to command line

import random
import socket
import struct
import sys


def skip_name(i):
    while True:
        x = resp[i]
        if x & 0xC0:  # check if the first two bits are set, then it's a pointer
            i += 2
            break
        if x == 0:
            i += 1  # skip over the null byte
            break

        i += x + 1  # skip over the length byte and the domain name
    return i


if __name__ == "__main__":
    hostname = sys.argv[1]
    s = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM
    )  # UDP. don't we want DNS to be reliable? DNS queries and responses are small. Don't need to split
    # into multiple packets or re-try. UDP is fine. don't need sequence numbers or sliding windows etc.

    # don't need to bind given UDP.

    query = None

    # construct the query according to the RFC 1035

    # Query and response format, will have a bit on to tell.

    # construct the Header
    # ID is required because we are using UDP, want to match the response to the query. TCP wouldn't need this.
    xid = random.randint(0, 65535)

    # RD; we want recursion. If the server doesn't have the answer, make DNS queries itself to find the answer.

    # in the flags, we only need RD. Low order bit of the high order byte. 0x0100
    flags = 0x0100
    # qdcout = 1, ancount = 0, nscount = 0, arcount = 0

    query = struct.pack(
        "!HHHHHH", xid, flags, 1, 0, 0, 0
    )  # pack as 2 byte unsigned shorts

    # now, construct the question.
    # qtype = 1 for an A record. qclass = 1 for internet
    qname = (
        b"".join(
            struct.pack("B", len(part)) + part.encode("ascii")
            for part in hostname.split(".")
        )
        + b"\x00"
    )
    query += qname
    #

    query += struct.pack("!HH", 1, 1)
    s.sendto(query, ("8.8.8.8", 53))  # google public DNS server
    # note: before checking the response, he checks wireshark, listens on wifi, filters to DNS.

    # sends the xid, A record, and the domain name.
    # response has same xid, include the question, answer, including IP which is shown in wire shark.

    resp, sender = s.recvfrom(
        4096
    )  # max buffer size. this is flawed, we are ignoring the sender and proceeding as if response was to what we wanted
    # parse the header
    rxid, rflags, qdcount, ancount, nscount, arcount = struct.unpack(
        "!HHHHHH", resp[:12]
    )
    assert (
        rxid == xid
    ), (
        "xid does not match"
    )  # messages could arrive out of order, so we need to check the xid
    assert qdcount == 1, "qdcount does not match"

    # parse the question, variable length.
    i = 12
    i = skip_name(i)

    i += 4  # skip over the qtype and qclass

    # parse the answer
    # the dns uses a compresion scheme to stop repeating the domain name. replaced with a pointer (4.1.4 in RFC 1035)
    # if the first 2 bits are set to one, the number we looked at (len of the label i.e wikipieda),
    # if 2 bits are on, look at the next 14 bits and have that be an offset which is a pointer within the message.

    i = skip_name(i)  # skip over the name in the answer if applicable

    # type, class, ttl we can parse. type and class 2 bytes each, ttl is 4 bytes, rdlength is 2 bytes
    rtype, rclass, ttl, rdlength = struct.unpack(
        "!HHIH", resp[i : i + 10]
    )  # unpack in big endian (network byte order)
    i += 10

    rdata = resp[i : i + rdlength]

    # ipv4 address

    print(".".join(str(b) for b in rdata))
