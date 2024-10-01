import random
import socket
import struct

# idea:

# send via UDP to 8.8.8.8:53 (google DNS) a DNS query

# need to construct the DNS query appropriately into bytes
# and unpack the response to get the IP address from socket calls

# socket.sendto, socket.recv

# DNS query format:

# 1. Header
# 16 bit ID, which is an

random_id = random.randint(0, 65535)
print(f"{random_id=}")
packed_id = struct.pack("!H", random_id)


# flags (16bit)
# qr: 0 for query, 1 for response (1bit)
# opcode: 0 for standard query (4 bits)
# aa: authoritative answer (1 bit)
# tc: truncated message (1 bit)
# rd: recursion desired (1 bit)
# ra: recursion available (1 bit)
# z: reserved (3 bits)
# rcode: response code (4 bits)

# we only set the qr, opcode, rd flags
# qr = 0 because we are sending a query
# opcode = 0 for standard query
# rd = 1 because we want the response to be recursive

# this is in hex 0x0100 (0b0000000100000000)

flags = 0x0100
packed_flags = struct.pack("!H", flags)

# qdcount: number of entries in the question section ( 16 bits)
# ancount: number of entries in the answer section (16 bits)
# nscount: number of entries in the authority section (16 bits)
# arcount: number of entries in the additional section (16 bits)

# we only set qdcount to 1 because we are only asking one question

packed_rest_of_header = struct.pack("!HHHH", 1, 0, 0, 0)

# 2. Question
# qname: domain name we are querying (variable length)
# qtype: type of the query (16 bits)
# qclass: class of the query (16 bits)

# A record is a record that maps a domain name to an IP address
# qtype for A record is 1

qtype = 1
packed_qtype = struct.pack("!H", qtype)

# qclass for internet is 1
qclass = 1
packed_qclass = struct.pack("!H", qclass)

# qname: how is a domain name represented in a DNS query and how is it encoded?

# QNAME           a domain name represented as a sequence of labels, where
# each label consists of a length octet followed by that
# number of octets.  The domain name terminates with the
# zero length octet for the null label of the root.  Note
# that this field may be an odd number of octets; no
# padding is used.

# encoding google.com:
address = "google.com"
address_parts = address.split(".")

qname = b""

for part in address_parts:
    qname += struct.pack("B", len(part))
    qname += part.encode("ascii")

qname += b"\x00"

question_total = qname + packed_qtype + packed_qclass
print(f"{question_total=}")

q_len = len(question_total)

dns_query = (
    packed_id
    + packed_flags
    + packed_rest_of_header
    + qname
    + packed_qtype
    + packed_qclass
)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(dns_query, ("8.8.8.8", 53))

response, address = sock.recvfrom(1024)

print(response)

header = response[:12]


id, flags, qdcount, ancount, nscount, arcount = struct.unpack("!HHHHHH", header)

print(f"ID: {id}")
print(f"Flags: {flags}")
print(f"qdcount: {qdcount}")
print(f"ancount: {ancount}")
print(f"nscount: {nscount}")
print(f"arcount: {arcount}")

qr = (flags >> 15) & 0x1  # 1 bit
opcode = (flags >> 11) & 0xF  # 4 bits
aa = (flags >> 10) & 0x1  # 1 bit
tc = (flags >> 9) & 0x1  # 1 bit
rd = (flags >> 8) & 0x1  # 1 bit
ra = (flags >> 7) & 0x1  # 1 bit
z = (flags >> 4) & 0x7  # 3 bits
rcode = flags & 0xF  # 4 bits

print(f"qr: {qr}")
print(f"opcode: {opcode}")
print(f"aa: {aa}")
print(f"tc: {tc}")
print(f"rd: {rd}")
print(f"ra: {ra}")
print(f"z: {z}")
print(f"rcode: {rcode}")

question = response[12 : 12 + q_len]

print(f"Question: {question}")

qname = question[:-4]
qtype, qclass = struct.unpack("!HH", question[-4:])

print(f"QNAME: {qname}")
print(f"QTYPE: {qtype}")
print(f"QCLASS: {qclass}")

# 3. Answer
# rname: domain name that was queried (variable length)
# rtype: type of the answer (16 bits)
# rclass: class of the answer (16 bits)
# ttl: time to live (32 bits)
# rdlength: length of the rdata field (16 bits)
# rdata: data of the answer (variable length)

answer = response[12 + q_len :]
print(f"Answer: {answer}")
