# Wireshark Network Traffic Analysis

## Overview
This project demonstrates basic network traffic analysis using Wireshark. Network packets were captured from a local environment and analyzed to observe normal activity and detect suspicious patterns such as port scanning.

## Tools
- [Wireshark](https://www.wireshark.org/) – packet capture and analysis  
- [Nmap](https://nmap.org/) – network scanning


## Project Goals
- Capture live network traffic
- Analyze common network protocols
- Identify suspicious traffic patterns
- Detect reconnaissance activity such as port scans

---

# Lab Procedure

## 1. Start Packet Capture

1. Open Wireshark.
2. Select your active network interface (Wi-Fi or Ethernet).
3. Click **Start Capturing Packets**.

Allow the capture to run while generating traffic in the next steps.

---

## 2. Generate Normal Network Traffic

While Wireshark is capturing packets:

- Visit several websites
- Perform a Google search
- Watch a YouTube video
- Download a small file

This creates normal traffic such as DNS queries, TCP connections, and HTTPS sessions.

---

## 3. Simulate Suspicious Activity

Open a terminal or command prompt.

Find your local IP address.

### Windows
```
ipconfig
```

### Linux / Mac
```
ifconfig
```

Example IP address:

```
192.168.1.25
```

Run a SYN scan using Nmap:

```
nmap -sS 192.168.1.25
```

This generates scanning traffic that will appear in the Wireshark capture.

---

## 4. Stop and Save the Capture

After about 10 minutes:

1. Stop the packet capture.
2. Save the file as:

```
network_capture.pcap
```

Store the file in the **captures/** folder of this repository.

---

# Traffic Analysis

## Protocol Hierarchy

Navigate to:

Statistics → Protocol Hierarchy

This view shows the distribution of network protocols such as TCP, DNS, and TLS.

Take a screenshot and store it in the **screenshots/** folder.

---

## DNS Traffic

Apply the filter:

```
dns
```

This shows domain name lookups performed during browsing activity.

Take a screenshot of the DNS queries.

---

## TCP Traffic

Apply the filter:

```
tcp
```

This displays TCP connections between hosts.

---

## SYN Scan Detection

Apply the filter:

```
tcp.flags.syn == 1 && tcp.flags.ack == 0
```

Multiple SYN packets targeting different ports may indicate reconnaissance scanning behavior.

Take a screenshot showing these packets.

- To focus on your local IP:

```text
ip.addr == <your_local_IP>
```
---

# Findings

During the analysis the following activity was observed:

- DNS queries generated during normal browsing
- TCP connections between local and external hosts
- SYN packets produced by the Nmap scan indicating port scanning activity
- Protocol Hierarchy and Conversations views summarize traffic patterns and host interactions.


---

# Skills Demonstrated

- Packet capture using Wireshark
- Network protocol analysis
- Traffic filtering and inspection
- Detection of reconnaissance activity

---

# Repository Contents

captures
- network_capture.pcap

screenshots
- protocol-hierarchy.png
- dns-queries.png
- syn-scan-detection.png

report
- traffic-analysis-report.md
