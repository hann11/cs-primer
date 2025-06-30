import random
import socket
import struct
import sys

GOOGLE_PUBLIC_DNS = ("8.8.8.8", 53)


def parse_name(res, i, compressed=False, compressed_i=0, compressed_prename=""):
    while True:
        len_part = res[i]
        if len_part & 0b11000000:
            offset = ((len_part & 0b00111111) << 8) + res[i + 1]
            return parse_name(res, offset, True, i, compressed_prename)

        if len_part == 0x00:
            i += 1
            break
        if len(compressed_prename) > 0:
            compressed_prename += "."
        part = res[i : i + len_part + 1]
        compressed_prename += part.decode("ascii")
        i += len_part + 1
    if compressed:
        i = compressed_i + 2
    return compressed_prename, i, compressed


if __name__ == "__main__":
    ip = "1.1.1.1"
    xid = random.randint(0, 65535)
    flags = 0x0100  # qr = 0, opcode = 0, aa = 0, tc = 0, rd = 1
    query = struct.pack("!HHHHHH", xid, flags, 1, 0, 0, 0)

    # from wireshark

    # reverse the IP
    hostname = ".".join(ip.split(".")[::-1]) + ".in-addr.arpa"
    qname = (
        b"".join(
            len(p).to_bytes(1, "big") + p.encode("ascii")
            for p in hostname.split(".")
        )
        + b"\x00"
    )

    qtype = 12  # PTR
    qclass = 1
    query += qname
    query += struct.pack("!HH", qtype, qclass)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(query, GOOGLE_PUBLIC_DNS)

    while True:
        res, sender = s.recvfrom(4096)
        if sender != GOOGLE_PUBLIC_DNS:
            continue  # noise
        rxid, rflags, qdcount, ancount, nscount, arcount = struct.unpack(
            "!HHHHHH", res[:12]
        )
        if rxid == xid:
            break

    print(f"Answer count: {ancount}")
    print(f"Query: {query.hex()}")
    print(f"Response: {res.hex()}")

    i = 12
    qname, i, cpr = parse_name(res, i)
    print(f"qname: {qname}, i: {i}, cpr: {cpr}")
    i += 4  # skip qtype and qclass

    # parsing the answer
    name, i, cpr = parse_name(res, i)
    print(f"name: {name}, i: {i}, cpr: {cpr}")

    rtype, rclass, ttl, rdlength = struct.unpack("!HHIH", res[i : i + 10])
    print(f"rtype: {rtype}, rclass: {rclass}, ttl: {ttl}, rdlength: {rdlength}")

    i += 10

    rdata = res[i : i + rdlength]

    name, i, cpr = parse_name(res, i)
    print(f"name: {name}, i: {i}, cpr: {cpr}")
