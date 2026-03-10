from scapy.all import *
from scapy.utils import PcapReader, PcapWriter
import hashlib
import os
import sys

# -------- CONFIG --------
INPUT_FILE = "network.capture.fixed.pcap"   # your PCAP file
OUTPUT_FILE = "network.capture.anonymized.pcap"
PRINT_INTERVAL = 1000
ANONYMIZE_DNS = True  # set False if you want to keep hostnames (less safe)

# -------- CHECK INPUT FILE --------
if not os.path.isfile(INPUT_FILE):
    print(f"Error: Input file '{INPUT_FILE}' not found!")
    sys.exit(1)

mac_map = {}
ipv4_map = {}
ipv6_map = {}
dns_map = {}

def anonymize_ipv4(ip):
    if ip not in ipv4_map:
        h = hashlib.sha256(ip.encode()).digest()
        ipv4_map[ip] = f"10.{h[0]}.{h[1]}.{h[2]}"
    return ipv4_map[ip]

def anonymize_ipv6(ip):
    if ip not in ipv6_map:
        h = hashlib.sha256(ip.encode()).digest()
        ipv6_map[ip] = "fd%02x:%02x:%02x:%02x::%02x:%02x" % (
            h[0], h[1], h[2], h[3], h[4], h[5]
        )
    return ipv6_map[ip]

def anonymize_mac(mac):
    if mac not in mac_map:
        mac_map[mac] = "02:00:00:%02x:%02x:%02x" % (
            len(mac_map), len(mac_map)+1, len(mac_map)+2
        )
    return mac_map[mac]

def anonymize_dns(name):
    if name not in dns_map:
        dns_map[name] = f"anon{len(dns_map)}.local"
    return dns_map[name]

# -------- PROCESS PACKETS --------
count = 0
with PcapReader(INPUT_FILE) as reader, PcapWriter(OUTPUT_FILE, append=False) as writer:
    for pkt in reader:
        if pkt.haslayer(Ether):
            pkt[Ether].src = anonymize_mac(pkt[Ether].src)
            pkt[Ether].dst = anonymize_mac(pkt[Ether].dst)
        if pkt.haslayer(IP):
            pkt[IP].src = anonymize_ipv4(pkt[IP].src)
            pkt[IP].dst = anonymize_ipv4(pkt[IP].dst)
            if hasattr(pkt[IP], "chksum"):
                del pkt[IP].chksum
        if pkt.haslayer(IPv6):
            pkt[IPv6].src = anonymize_ipv6(pkt[IPv6].src)
            pkt[IPv6].dst = anonymize_ipv6(pkt[IPv6].dst)
            if hasattr(pkt[IPv6], "fl"):
                del pkt[IPv6].fl
            if hasattr(pkt[IPv6], "plen"):
                del pkt[IPv6].plen
        if pkt.haslayer(TCP) and hasattr(pkt[TCP], "chksum"):
            del pkt[TCP].chksum
        if pkt.haslayer(UDP) and hasattr(pkt[UDP], "chksum"):
            del pkt[UDP].chksum
        if ANONYMIZE_DNS and pkt.haslayer(DNS):
            if pkt[DNS].qd:
                for i in range(pkt[DNS].qdcount):
                    if pkt[DNS].qd[i].qname:
                        pkt[DNS].qd[i].qname = anonymize_dns(pkt[DNS].qd[i].qname.decode()).encode()
            if pkt[DNS].an:
                for i in range(pkt[DNS].ancount):
                    if pkt[DNS].an[i].rrname:
                        pkt[DNS].an[i].rrname = anonymize_dns(pkt[DNS].an[i].rrname.decode()).encode()
        writer.write(pkt)
        count += 1
        if count % PRINT_INTERVAL == 0:
            print(f"Processed {count} packets...")

print("Done!")
print(f"Anonymized capture saved as '{OUTPUT_FILE}'")
