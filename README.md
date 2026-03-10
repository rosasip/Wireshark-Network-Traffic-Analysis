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


## Identifying Suspicious Patterns & Attack Signatures

In this section, I demonstrate how I identified specific "red flags" during my traffic analysis. By using Wireshark filters, I was able to isolate the following common attack signatures:

<details>
<summary><b>1. Detecting SYN Scans (Reconnaissance)</b></summary>

I identified a **SYN Scan** (often used by `nmap`) by looking for a high volume of TCP connection requests that never completed the "Three-Way Handshake."

* **What I did:** I applied the filter `tcp.flags.syn == 1 and tcp.flags.ack == 0`.
* **The Signature:** I observed a single Source IP hitting hundreds of different Destination Ports in a very short timeframe.
* **My Conclusion:** Since no `ACK` was sent back from the source to complete the connection, I confirmed this was an automated port discovery attempt.
</details>

<details>
<summary><b>2. Identifying ICMP Flooding (Ping Sweep)</b></summary>

I analyzed the traffic for **ICMP echo requests** (pings) used to map out which devices are "alive" on the network.

* **What I did:** I filtered by `icmp`.
* **The Signature:** I saw a rapid succession of "Echo Request" packets followed by "Echo Reply" packets.
* **My Conclusion:** An unusual amount of ICMP traffic from one source to many internal IPs suggests a "Ping Sweep" for network mapping.
</details>

<details>
<summary><b>3. spotting Clear-Text Credential Leaks</b></summary>

I checked for insecure protocols where sensitive data might be exposed to an attacker.

* **What I did:** I searched for `http` and `telnet` traffic.
* **The Signature:** By using the **"Follow TCP Stream"** feature in Wireshark, I was able to see data in plain text rather than encrypted ciphertext.
* **My Conclusion:** This highlighted the vulnerability of using non-encrypted protocols, as any attacker on the same network could intercept passwords or session tokens.
</details>

---
## Defense Recommendations

After identifying these attack signatures, I documented the following defensive strategies to harden the network.

<details>
<summary><b>Click to expand: How I would mitigate these threats</b></summary>

### 1. Defending against Reconnaissance (Nmap Scans)
* **Action:** Configure an **Intrusion Prevention System (IPS)** or a Firewall (like `iptables` or Windows Firewall).
* **Strategy:** Set up "Rate Limiting" to block any IP address that attempts to connect to too many ports in a short window of time.
* **Goal:** Make the network "quiet" so the scanner sees nothing but closed doors.

### 2. Preventing Data Leaks (Clear-Text Vulnerabilities)
* **Action:** Enforce the use of **TLS/SSL** for all web traffic.
* **Strategy:** Disable insecure protocols like HTTP (Port 80), Telnet (Port 23), and FTP (Port 21) in favor of their encrypted versions (HTTPS, SSH, SFTP).
* **Goal:** Ensure that even if a packet is captured in Wireshark, the "Follow TCP Stream" result is encrypted gibberish instead of private data.

### 3. Monitoring & Alerting
* **Action:** Use **Security Information and Event Management (SIEM)** tools.
* **Strategy:** Create custom alerts based on the Wireshark filters I used (e.g., alert if SYN-to-ACK ratios are abnormal).
* **Goal:** To be notified in real-time the moment a suspicious signature appears on the network.

</details>

---


# Skills Demonstrated

<details>
<summary><b>Click to expand: Core Technical Competencies</b></summary>

* **Network Protocol Analysis:** Performed deep-packet inspection of **TCP/IP, DNS, and HTTP** structures using [Wireshark](https://www.wireshark.org/).
* **Security Scripting & Automation:** Leveraged **Scapy** (Python) to programmatically craft custom packets, simulating specific network behaviors.
* **Operational Security (OPSEC):** Implemented data privacy workflows by using the **`editcap`** utility to sanitize `.pcapng` files before public sharing.
* **Linux Command Line Mastery:** Gained proficiency in terminal-based workflows, including package management with `pip` and text manipulation using the **`nano`** editor.
* **Threat Hunting & Pattern Recognition:** Identified attack signatures such as **TCP SYN Scans** and **ICMP Sweeps** using advanced display filters.
* **Network Hardening:** Developed actionable defense strategies, including **Rate Limiting** and **Protocol Encryption**, to mitigate discovered vulnerabilities.

</details>



## What I Learned

<details>
<summary><b>Click to expand: New Skills & Technical Workflow</b></summary>

### Command Line & Scripting
* **Terminal Navigation:** Mastered using `nano` for on-the-fly file editing. Learned essential shortcuts: `Ctrl+O` (Save) and `Ctrl+X` (Exit).
* **Package Management:** Used `pip install scapy` to set up specialized Python libraries for network analysis.
* **Packet Crafting:** Wrote custom Python scripts using **Scapy** to manually build and send Ethernet/IP/TCP layers.

### Security & Privacy (OPSEC)
* **Traffic Anonymization:** Used `editcap` to sanitize captures, ensuring Public IPs are mapped to `0.0.0.0` for safe GitHub sharing.
* **Reconnaissance Detection:** Learned to identify the difference between normal handshake traffic and automated SYN scans.

### Sample Scapy Script
```python
from scapy.all import IP, TCP, send

# Crafting a safe packet with a fake source IP
packet = IP(src="1.2.3.4", dst="127.0.0.1") / TCP(dport=80, flags="S")
send(packet)
