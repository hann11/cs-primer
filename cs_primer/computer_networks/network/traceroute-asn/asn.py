ips = [
    "192.168.88.1",
    "180.150.0.245",
    "142.250.165.14",
    "192.178.244.29",
    "209.85.253.181",
    "172.217.167.110",
]

# ips = [
#     "1.0.0.202",  # Cloudflare
#     "1.0.5.3",  # GTelecom
# ]

# Goal:
# Map an IP to the ASN it belongs to

# Plan:
# Convert ip2asn IP's to strings
# For each IP:
# Iterate over the list and find the first start IP that is greater than the IP
# Choose the prior IP and get it's ASN

# How to open a .tsv:
# open file as f for writing
# split by tab


def ip_to_bits(ip: str) -> int:
    """
    Convert an IP address to a 32-bit integer.
    """
    parts = ip.split(".")
    return (
        int(parts[0]) << 24
        | int(parts[1]) << 16
        | int(parts[2]) << 8
        | int(parts[3])
    )


with open("ip2asn-v4.tsv", "r") as f:
    lines = f.readlines()
    lines = [line.strip("\n").split("\t") for line in lines]
    lines = [
        (
            ip_to_bits(line[0]),
            ip_to_bits(line[1]),
            int(line[2]),
            line[3],
            line[4],
        )
        for line in lines
    ]  # Convert to int


def find_asn(ip: str) -> tuple[str, str, str]:
    """
    Find ASN ID, Country, Name"""
    bit_ip = ip_to_bits(ip)
    for i in range(len(lines)):
        if lines[i][0] > bit_ip:
            asn = lines[i - 1]
            return asn[2], asn[3], asn[4]


if __name__ == "__main__":
    for ip in ips:
        id, country, name = find_asn(ip)
        print(f"IP: {ip} | ASN ID: {id} | Country: {country} | Name: {name}")
