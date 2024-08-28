import sys
import re

def convert_hex_rgb(hex: str):
    """
    Takes in a hex string like #aabbcc and converts to 3 integers based on the 3 bytes
    """
    #1. convert to bytes
    bytes_rep = bytes.fromhex(hex.strip("#"))
    # can also do by splitting hex into 2 chars each then convert to int with base 16 conversion
    # add to bytes array and return the bytes from it

    #2. add the bytes rep to integers like we did in protobuf varint.
    r,g,b = 0,0,0
    r |= bytes_rep[0]
    g |= bytes_rep[1]
    b |= bytes_rep[2]

    return f"rgb({r} {g} {b})"

if __name__ == "__main__":
    hex = "#fe030a"
    print(convert_hex_rgb(hex))

    lines = sys.stdin.readlines()
    for line in lines:
        match = re.findall(r"#([0-9a-fA-F]{6})", line)
        if len(match) == 0:
            print(line)
        else:
            print(convert_hex_rgb(match[0]))