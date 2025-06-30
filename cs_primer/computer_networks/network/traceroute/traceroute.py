import socket
import struct

dst_ip = "172.217.167.110"

sock = socket.socket(
    socket.AF_INET, socket.SOCK_DGRAM
)  # send udp packets to the intermediate hops

rec_sock = socket.socket(
    socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP
)  # receive icmp packets
rec_sock.settimeout(1)  # if dont receieve response, move on

port_add = 0
for ttl in range(1, 64):
    # for hop in range(1, 4):
    sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    port_to_send = 33435 + port_add
    sock.sendto(b"\x00" * 24, (dst_ip, port_to_send))
    reached_dst = False
    while True:
        try:
            data, addr = rec_sock.recvfrom(1000)
        except socket.timeout:
            print("*")
            break

        protocol = data[9]
        assert data[9] == 1, f"Protocol is not ICMP: {protocol}"

        type = data[20]
        assert type in [11, 3], (
            f"Type is not TTL Exceeded or Port unreachable: {type}"
        )

        dst_port_sent_to = data[50:52]
        dst_port_sent_to = struct.unpack("!H", dst_port_sent_to)[0]
        assert dst_port_sent_to == port_to_send, (
            f"Destination port sent to is not the same: {dst_port_sent_to}"
        )

        intermediate_ip = data[12:16]
        intermediate_ip = ".".join(str(i) for i in intermediate_ip)
        print(f"{ttl}: {intermediate_ip}")

        if type == 3:
            print(f"Reached destination: {intermediate_ip}")
            reached_dst = True
        break

    if reached_dst:
        break
    port_add += 1
