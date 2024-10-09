import random
import socket
import struct

"""
Constructs a DNS Query according to RFC 1035
"""


def construct_dns_query(hostname: str) -> bytes:
    random_id = random.randint(0, 65535)

    flags = 0x0100  # qr 0, opcode 0, rd 1

    qdcount = 1
    ancount = 0
    nscount = 0
    arcount = 0

    packed_header = struct.pack(
        "!HHHHHH", random_id, flags, qdcount, ancount, nscount, arcount
    )

    hostname_parts = hostname.split(".")

    qname = b""

    for part in hostname_parts:
        qname += struct.pack("B", len(part))
        qname += part.encode("ascii")

    qname += b"\x00"

    qtype = 1
    qclass = 1

    packed_question = qname + struct.pack("!HH", qtype, qclass)

    dns_query = packed_header + packed_question

    return dns_query, random_id, len(packed_question)


def parse_response_from_dns_server(
    hostname: str, response: bytes, q_len: int, random_id: int
) -> str:
    header = response[:12]

    id, _, _, ancount, _, _ = struct.unpack("!HHHHHH", header)

    assert id == random_id, "Random id does not match"

    assert ancount == 1, "Only one answer is supported"

    question = response[12 : 12 + q_len]

    qname = question[:-4]

    hostname_resp = ""
    pointer = 0

    while True:
        length = qname[pointer]
        part = qname[pointer + 1 : pointer + 1 + length]
        part_decoded = part.decode("ascii")
        hostname_resp += part_decoded
        pointer += length + 1
        if pointer < len(qname) and qname[pointer] != 0:
            hostname_resp += "."
        if pointer >= len(qname) or qname[pointer] == 0:
            break

    assert hostname == hostname_resp, "Hostname does not match"

    answer = response[12 + q_len :]

    name_len = 0
    for byte_piece in answer:
        if byte_piece == 0x00:
            break
        name_len += 1

    _, _, _, rdlength = struct.unpack("!HHLH", answer[name_len:12])

    rdata = answer[12 : 12 + rdlength]

    ip = ".".join([str(byte) for byte in rdata])

    return ip


dns_query, random_id, q_len = construct_dns_query("google.com")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(dns_query, ("8.8.8.8", 53))

response, address = sock.recvfrom(1024)

ip = parse_response_from_dns_server("google.com", response, q_len, random_id)

print(f"IP: {ip}")
