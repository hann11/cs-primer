SYN Flood: TCP handshakes initiated, but not completed.

There are SYN and ACK flags in the TCP header. The SYN flag is used to initiate a connection, and the ACK flag is used to acknowledge a connection. The SYN Flood attack is a type of Denial of Service (DoS) attack that exploits the TCP handshake process. The attacker sends a large number of SYN packets to the target server, but does not respond to the SYN-ACK packets sent by the server. This causes the server to keep the connection half-open, consuming resources and preventing legitimate connections from being established.

We have .pcap files (packet capture files).

These are network packets, that have the layered model.

Layer 7: Application - we don't have this here.
Layer 4: Transport: TCP headers, we will need to dig into these.
Layer 3: Network: IP headers, we will need to dig into these.
Layer 2: Link: Placeholder, due to localhost loopback.

For some reason, network packets are in little-endian format.

There is a pcap header, which is 24 bytes long.
magic number: first 4 bytes
major version number: next 2 bytes
minor version number: next 2 bytes
timezone offset: next 4 bytes
timestamp accuracy: next 4 bytes
snapshot length: next 4 bytes
link layer type: next 4 bytes

In our case the link layer type is 0.

Then, we have packets.

Packets have a packet header. basically oly want the packet length here, bytes 8-12.

Then, we have the packet data.

Maintain an offset and move through that, based on packet length.

The packet has IP headers.

Most important here is the IP header length, which is the first byte of the IP header.

Note each packet has 4bytes of Link layer to skip.

version_ihl = packet[4]

ihl = version_ihl & 0x0F (the last 4 bits)
bytes_ihl = ihl \* 4

tcp: packet[4+bytes_ihl:]
