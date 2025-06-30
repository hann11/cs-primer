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


def pack_query(hostname: str, qtype: int, xid: int) -> bytes:
    flags = 0x0100  # qr = 0, opcode = 0, aa = 0, tc = 0, rd = 1
    query = struct.pack("!HHHHHH", xid, flags, 1, 0, 0, 0)
    query += b"".join(
        len(p).to_bytes(1, "big") + p.encode("ascii")
        for p in hostname.split(".")
    )
    query += b"\x00"

    qclass = 1
    query += struct.pack("!HH", qtype, qclass)
    return query


if __name__ == "__main__":
    hostname = "google.com"
    qtype = 2
    xid = random.randint(0, 65535)
    query = pack_query(hostname, qtype, xid)

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
    i = 12

    qname, i, cpr = parse_name(res, i)
    print(f"qname: {qname}, i: {i}, cpr: {cpr}")
    i += 4  # skip qtype and qclass
    print(res)

    for x in range(ancount):
        name, i, cpr = parse_name(res, i)
        print(f"name: {name}, i: {i}, cpr: {cpr}")
        rtype, rclass, ttl, rdlength = struct.unpack("!HHIH", res[i : i + 10])
        i += 10  # skip rtype, rclass, ttl, rdlength

        rdata = res[i : i + rdlength]
        if rtype == 1:
            print(".".join(str(x) for x in rdata))
        elif rtype == 2:
            ns_name, _, cpr = parse_name(res, i)
            print(f"ns_name: {ns_name}, i: {_}, cpr: {cpr}")
        i += rdlength
