import socket
import struct
import sys
from typing import Optional

from loguru import logger


class ReliableDelivery:
    def __init__(self, port: Optional[int] = None):
        self.seq = 0
        self.buff = []
        if port:
            self.port = int(port)
            # we are a client
            assert self.port == 7000, "Sending to port 7000"
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.port = 8000
            # we are a server
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(("", self.port))
            logger.trace(f"Listening on port {self.port}")

    def send(self, data: bytes):
        """
        Send data to the server.
        """
        self.seq += 1
        seq = struct.pack("!B", self.seq)  # seq number
        adj_data = seq + b"0" + data  # seq, 0 ack, data
        self.sock.sendto(adj_data, ("localhost", self.port))
        logger.trace(f"rd.send: Sent {adj_data} to localhost:{self.port}")

        # set timeout to 1 if no response
        self.sock.settimeout(1)
        try:
            resp, addr = self.sock.recvfrom(1024)
            ack = resp[1:2]
            logger.trace(f"rd.send: Received {resp} from {addr}")
            if ack == seq:
                logger.trace(f"rd.send: ACK received, {ack=}, {seq=}")
            else:
                logger.trace(
                    f"rd.send: ACK not received, {ack=}, {seq=}"
                )  # wrong ack, resend and ask for another
                self.seq -= 1
                self.send(data)
        except socket.timeout:
            logger.trace(f"rd.send: Timeout, resending {data}")
            self.seq -= 1  # didnt receive ACK, resend
            self.send(data)

        # wait for resp

    def receive(self) -> bytes:
        """
        Receive data from the server.
        """
        # if self.seq == int(to_ack.decode("ascii")), resend but dont return

        if len(self.buff) > 0:  # buff data
            logger.trace(f"rd.receive: Buff has {len(self.buff)} items")
            seq, to_rec = self.buff.pop(0)
            self.seq = seq
            return to_rec

        data, addr = self.sock.recvfrom(1024)
        logger.trace(f"rd.receive: Received {data} from {addr}")
        to_ack = data[0:1]
        to_seq = b"0"

        self.sock.sendto(to_seq + to_ack, addr)
        logger.trace(f"rd.receive: sent back ack {to_ack}")

        seq_rec = struct.unpack("!B", to_ack)[0]

        if seq_rec == self.seq:  # duplicate
            return None
        elif seq_rec - 2 >= self.seq:
            # out of order
            logger.trace(
                f"rd.receive: Out of order {seq_rec=}, {self.seq=}, {data=}"
            )
            self.buff.append((seq_rec, data[2:]))
            self.receive()
        else:
            self.seq = seq_rec
            return data[2:]


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    if len(sys.argv) > 1:
        rd = ReliableDelivery(port=int(sys.argv[1]))
        while True:
            data = input("Enter message to send: ").encode("utf-8")
            rd.send(data)
            logger.success(f"main: Sent {data}")
    else:
        rd = ReliableDelivery()
        while True:
            data = rd.receive()
            if data:
                logger.success(f"main: Received: {data}")
