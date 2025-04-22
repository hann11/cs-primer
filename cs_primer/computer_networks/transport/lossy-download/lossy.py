import struct

DEBUG = False

if __name__ == "__main__":
    with open("lossy.pcap", "rb") as f:
        (
            magic_number,
            major,
            minor,
            tz_offset,
            ts_accuracy,
            snap_len,
            link_layer,
        ) = struct.unpack("<IHHIIII", f.read(24))

        assert magic_number == 0xA1B2C3D4

        assert major == 2
        assert minor == 4
        assert tz_offset == 0
        assert ts_accuracy == 0
        if DEBUG:
            print(f"PCAP Protocol: {major}.{minor}")
            print(f"Snap Length: {snap_len}")
            print(f"Link Layer: {link_layer}")

        packet_no = 0

        assert link_layer == 1  # Ethernet

        seq_data = {}
        raw_http = b""

        while True:
            packet_header = f.read(16)

            if not packet_header:
                break

            _, _, length, untrunc = struct.unpack("<IIII", packet_header)

            assert (
                length == untrunc
            ), f"Length {length} != Untruncated {untrunc}"

            if DEBUG:
                print(f"Packet {packet_no}: {length=}, {untrunc=}")
            packet_no += 1
            packet = f.read(length)

            # ethernet does not have preamble, sfd or fcs

            mac_dst = packet[:6].hex()
            mac_src = packet[6:12].hex()
            ethertype = packet[12:14].hex()

            if DEBUG:
                print(f"MAC DST: {mac_dst}")
                print(f"MAC SRC: {mac_src}")
                print(f"Ethertype: {ethertype}")
            assert ethertype == "0800"  # IPv4

            datagram = packet[14:]

            ver_ihl = datagram[0]
            ver = ver_ihl >> 4
            ihl = ver_ihl & 0x0F
            if DEBUG:
                print(f"Version: {ver}")
                print(f"IHL: {ihl}")

            ihl_len = ihl << 2  # mult by 4
            if DEBUG:
                print(f"IHL Len: {ihl_len}")

            total_datagram_len = struct.unpack(">H", datagram[2:4])[0]
            if DEBUG:
                print(f"Total Datagram Length: {total_datagram_len}")

            transport_protocol = datagram[9]
            if DEBUG:
                print(f"Transport Protocol: {transport_protocol}")
            assert transport_protocol == 6  # TCP

            src_ip = datagram[12:16]
            dst_ip = datagram[16:20]

            src_ip = ".".join(str(i) for i in src_ip)
            dst_ip = ".".join(str(i) for i in dst_ip)
            if DEBUG:
                print(f"Source IP: {src_ip}")
                print(f"Destination IP: {dst_ip}")

            trans_layer = datagram[ihl_len:]

            src_port, dst_port = struct.unpack("!HH", trans_layer[:4])
            # should do for port80 only from src

            if DEBUG:
                print(f"Source Port: {src_port}")
                print(f"Destination Port: {dst_port}")

            seq_num = struct.unpack(">I", trans_layer[4:8])[0]
            if DEBUG:
                print(f"Sequence Number: {seq_num}")

            # next get http and parse
            data_offset_reserved = trans_layer[12]

            data_offset = (data_offset_reserved >> 4) << 2

            http_data = trans_layer[data_offset:]

            seq_data[seq_num] = http_data  # just write TCP seq data (responses)

        ordered_seqs = sorted(seq_data.keys())
        print(f"Number of packets: {len(ordered_seqs)}")

        for seq in ordered_seqs:
            raw_http += seq_data[seq]

        header, body = raw_http.split(b"\r\n\r\n", 1)

        with open("reconstructed.jpg", "wb") as w:
            w.write(body)
        print(f"Wrote {len(body)} bytes to reconstructed.jpg")
