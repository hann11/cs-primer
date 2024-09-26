with open("synflood.pcap", "rb") as f:
    file = f.read()


def convert_le_to_int(byte_input: bytes) -> int:
    """
    Convert little endian bytes to int
    """
    num = 0

    for b in reversed(byte_input):
        num <<= 8
        num |= b

    return num


if __name__ == "__main__":
    with open("synflood.pcap", "rb") as f:
        file = f.read()
        # print(f.read(24).hex())

    magic_number = file[:4]
    major_version = file[4:6]
    minor_version = file[6:8]
    tz_offset = file[8:12]
    ts_accuracy = file[12:16]
    snapshot_len = file[16:20]
    link_layer_type = file[20:24]

    print(f"{magic_number=}")
    print(f"{convert_le_to_int(magic_number)=}")
    print(f"{convert_le_to_int(major_version)=}")
    print(f"{convert_le_to_int(minor_version)=}")
    print(f"{convert_le_to_int(tz_offset)=}")
    print(f"{convert_le_to_int(ts_accuracy)=}")
    print(f"{convert_le_to_int(snapshot_len)=}")
    print(f"{convert_le_to_int(link_layer_type)=}")

    offset = 24

    syn_count = 0
    ack_count = 0
    packet_count = 0
    while offset < len(file):
        header = file[offset : offset + 16]
        packet_length = convert_le_to_int(header[8:12])

        packet = file[offset + 16 : offset + 16 + packet_length]

        version_ihl = packet[4]
        ihl = version_ihl & 0x0F
        ihl_bytes = ihl * 32 // 8

        tcp_header = packet[4 + ihl_bytes :]
        flags = tcp_header[12:14]

        syn = (flags[0] & 0x02) >> 1
        ack = (flags[0] & 0x10) >> 4

        syn_count += syn
        ack_count += ack
        packet_count += 1

        offset += 16 + packet_length

    print(f"{syn_count=}")
    print(f"{ack_count=}")
    print(f"{packet_count=}")
    print(f"{round(ack_count / packet_count,2)=}")


# first_packet_header = file[24:40]

# first_packet_ts_sec = first_packet_header[:4]
# first_packet_ts_usec = first_packet_header[4:8]
# first_packet_incl_len = first_packet_header[8:12]
# first_packet_orig_len = first_packet_header[12:16]

# print(f"{convert_le_to_int(first_packet_ts_sec)=}")
# print(f"{convert_le_to_int(first_packet_ts_usec)=}")
# print(f"{convert_le_to_int(first_packet_incl_len)=}")
# print(f"{convert_le_to_int(first_packet_orig_len)=}")

# first_packet = file[40 : 40 + convert_le_to_int(first_packet_incl_len)]

# print(f"{first_packet=}")
# print(f"{len(first_packet)=}")

# protocol = first_packet[:4]  # comment: sits where link layer header would be
# print(f"{protocol=}")
# if protocol == b"\x02\x00\x00\x00":
#     print("protocol=IPv4")

# version_ihl = first_packet[4]
# print(f"{version_ihl=}")
# version = version_ihl >> 4
# ihl = version_ihl & 0x0F
# dscp_ecn = first_packet[5]
# dscp = dscp_ecn >> 2
# ecn = dscp_ecn & 0x03
# total_length = first_packet[6:8]
# identification = first_packet[8:10]
# flags_fragment_offset = first_packet[10:12]
# flags = flags_fragment_offset[0] >> 5
# fragment_offset = (
#     flags_fragment_offset[0] & 0x1F
# ) << 8 | flags_fragment_offset[1]
# ttl = first_packet[12]
# protocol = first_packet[13]
# header_checksum = first_packet[14:16]
# source_ip = first_packet[16:20]
# destination_ip = first_packet[20:24]

# print(f"{version=}")
# print(f"{ihl=}")
# ihl_bytes = ihl * 32 // 8
# print(f"{ihl_bytes=}")
# print(f"{total_length=}")
# print(f"{ttl=}")
# print(f"{protocol=}")
# print(f"{source_ip=}")
# print(f"{destination_ip=}")

# tcp_header = first_packet[4 + ihl_bytes :]

# print(f"{tcp_header=}")
# print(f"{len(tcp_header)=}")

# source_port = tcp_header[:2]
# destination_port = tcp_header[2:4]
# sequence_number = tcp_header[4:8]
# acknowledgment_number = tcp_header[8:12]
# flags = tcp_header[12:14]

# syn = (flags[0] & 0x02) >> 1
# ack = (flags[0] & 0x10) >> 4

# print(f"{convert_le_to_int(source_port)=}")
# print(f"{convert_le_to_int(destination_port)=}")
# print(f"{convert_le_to_int(sequence_number)=}")
# print(f"{convert_le_to_int(acknowledgment_number)=}")
# print(f"{syn=}")
# print(f"{ack=}")
