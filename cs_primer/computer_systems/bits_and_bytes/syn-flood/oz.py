import struct

if __name__ == "__main__":
    with open("synflood.pcap", "rb") as f:
        # let's just iterate through the file

        (
            magic_number,
            major,
            minor,
            tz_offset,
            ts_accuracy,
            snap_len,
            link_layer,
        ) = struct.unpack("<IHHIIII", f.read(24))
        # < is little endian, I is unsigned int, H is unsigned short. I 4 bytes, H 2 bytes

        assert magic_number == 0xA1B2C3D4

        print(f"PCAP Protocol: {major}.{minor}")

        assert link_layer == 0  # loopback localhost

        packet_count = 0

        init_count = 0
        ack_count = 0

        while True:
            packet_header = f.read(16)  # 16 bytes per packet header

            if not packet_header:
                break

            packet_count += 1

            _, _, length, untrunc = struct.unpack("<IIII", packet_header)

            packet = f.read(length)

            link_layer = packet[:4]

            # this is little endian??? ll header

            # claude: Localhost/Loopback Traffic: Traffic captured on the loopback interface (localhost) often doesn't follow the usual network byte order conventions. This is because it doesn't actually go through the physical network stack.

            # Operating System Influence: The byte order of loopback traffic can be influenced by the host operating system's native byte order. Many modern systems are little-endian.

            # Capture Method: Some capture methods or drivers might store loopback traffic in the host's native byte order rather than converting it to network byte order.

            # PCAP on Linux: Particularly on Linux systems, PCAP files capturing loopback traffic often store the data in host byte order (typically little-endian) rather than network byte order.
            ll_version = struct.unpack("<I", link_layer)[0]

            assert (
                ll_version == 2
            )  # good to assert, ensure can debug later errors a bit easier as we are good up to this point

            # NETWORK PROTOCOLS ARE BIG ENDIAN.
            ip_tcp_bytes = packet[4:]

            version_ihl = ip_tcp_bytes[0]

            version = version_ihl >> 4

            ihl = version_ihl & 0xF
            ihl_len = ihl << 2  # fast way to multiply by 4

            assert version == 4
            assert ihl_len == 20  # no options

            tcp_bytes = ip_tcp_bytes[ihl_len:]

            # we want to check packets send and received from port 80, others are noise

            source_port, dest_port = struct.unpack("!HH", tcp_bytes[:4])

            # print(f"Packet {packet_count}: {source_port} -> {dest_port}")

            seq_num, ack_num = struct.unpack("<II", tcp_bytes[4:12])

            data_offset_reserved_flags = struct.unpack("!H", tcp_bytes[12:14])[
                0
            ]

            # every syn should be on
            # everything back from port 80 should be ack
            syn = (data_offset_reserved_flags & 0x02) > 0
            ack = (data_offset_reserved_flags & 0x10) > 0

            if dest_port == 80 and syn:
                init_count += 1

            if source_port == 80 and ack:
                ack_count += 1

            # print(f"SYN: {syn}, ACK: {ack}")

            # break

        print(f"SYN: {init_count}, ACK: {ack_count}, Total: {packet_count}")
        print(f"ACK Ratio: {round(ack_count / init_count, 2)}")
