import socket
import struct
import sys

dst_ip = "172.217.167.110"

sock = socket.socket(
    socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP
)  # receive icmp packets
sock.settimeout(1)  # if dont receieve response, move on


def icmp_checksum(words: list[int]) -> int:
    sum_words = sum(words)

    while sum_words >> 16:
        sum_words = (sum_words & 0xFFFF) + (sum_words >> 16)

    return ~sum_words & 0xFFFF


# Plan
# Create ICMP socket with timeout 1
# For each TTL:
# Send a ping to the destination IP using ICMP with set TTL (setsockopt)
# set type 8 for ping
#    compute checksum
#    increase seq number in Big Endian
#    use a static identifier
# Receive response, check for type; TTL exceeded (11) and verify the message matches via the sequence number in the response
seq = 1
for ttl in range(1, 64):
    # for hop in range(1, 4):
    sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    # icmp header:
    type = 8  # echo request (8bit)
    code = 0
    # checksum = 0
    identifier = 0x89E3  # arbitrary identifier

    to_check = struct.pack("!BBHH", type, code, identifier, seq)

    checksum = icmp_checksum(list(struct.unpack("!HHH", to_check)))

    icmp_pack = (
        struct.pack("!BBHHH", type, code, checksum, identifier, seq)
        + b"\x00" * 24
    )

    sock.sendto(icmp_pack, (dst_ip, 0))
    reached_dst = False

    while True:
        try:
            data, addr = sock.recvfrom(1000)
        except socket.timeout:
            print("*")
            break

        protocol = data[9]
        assert data[9] == 1, f"Protocol is not ICMP: {protocol}"
        type = data[20]

        if type == 11:
            rec_seq = struct.unpack("!H", data[54:56])[0]

        elif type == 0:
            rec_seq = struct.unpack("!H", data[26:28])[0]  # TODO
            reached_dst = True

        assert rec_seq == seq, f"Rec seq is not the same: {rec_seq}"
        intermediate_ip = data[12:16]
        intermediate_ip = ".".join(str(i) for i in intermediate_ip)
        print(f"{ttl}: {intermediate_ip}")

        seq += 1
        break
    if reached_dst:
        break
