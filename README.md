# Honeypot-Wireshark-lab
Honeypot + Wireshark integration lab for capturing, analyzing, and responding to real attack traffic
# 🛡️ Honeypot + Wireshark Cybersecurity Lab

A hands-on cybersecurity home lab featuring honeypot deployment with live traffic capture and analysis. Built to simulate real-world attack scenarios, capture attacker behavior, and analyze malicious traffic at both the application and network layer.

---

## 📌 Project Overview

This lab combines two powerful tools:

- **Cowrie** — an SSH/Telnet honeypot that emulates a vulnerable server, logs every login attempt, credential used, and command executed by an attacker
- **Wireshark / tshark** — captures raw network packets so every connection, scan, and data transfer is recorded at the packet level

Together they give a complete picture of an attack: from the first port scan all the way to commands the attacker runs inside the fake shell.

---

## 🗂️ Repository Structure

```
Honeypot-Wireshark-lab/
├── honeypot/
│   ├── cowrie/          # Cowrie SSH honeypot config and setup
│   ├── dionaea/         # Dionaea malware honeypot (planned)
│   └── config/          # Shared honeypot configuration files
├── capture/
│   ├── scripts/         # tshark automation scripts for packet capture
│   ├── pcaps/           # Saved packet capture files (.pcap)
│   └── filters/         # Wireshark display and capture filter profiles
├── analysis/
│   ├── logs/            # Normalized Cowrie JSON logs
│   ├── alerts/          # Alerting scripts (Slack/email notifications)
│   └── reports/         # Python analysis scripts and findings reports
├── infra/
│   └── Dockerfile       # Container setup for isolated deployment
├── docs/
│   ├── setup.md         # Full step-by-step setup guide
│   └── architecture.md  # Lab architecture and design decisions
├── tests/               # Scripts to simulate attack traffic and verify capture
├── .env.example         # Environment variable template (no real credentials)
├── docker-compose.yml   # Spin up the full lab environment
└── requirements.txt     # Python dependencies for analysis scripts
```

---

## 🧰 Tools & Technologies

| Tool | Purpose |
|------|---------|
| **Cowrie** | SSH/Telnet honeypot — logs credentials and attacker commands |
| **Wireshark / tshark** | Packet capture and network traffic analysis |
| **Python** | Log parsing, IP correlation, and attack analysis scripts |
| **VirtualBox** | Isolated VM environment for safe honeypot deployment |
| **Ubuntu Server 22.04** | Honeypot host operating system |
| **Docker** | Containerized deployment (in progress) |
| **iptables** | Port redirection (port 22 → 2222) |

---

## 🏗️ Architecture

```
[ Attacker ]
     |
     | SSH / Telnet connection attempt
     ▼
[ iptables ] → redirects port 22 → port 2222
     |
     ▼
[ Cowrie Honeypot ] ←─────────────────────────────┐
  - Emulates real SSH server                       │
  - Logs: credentials, commands, file downloads    │
  - Outputs structured JSON logs                   │
     |                                             │
     ▼                                             │
[ Cowrie JSON Logs ]                               │
     |                                             │
     ▼                                        [ Python ]
[ Wireshark / tshark ] ──────────────────→  Correlation
  - Captures raw packets on network interface      │
  - Saves to .pcap files                          │
  - Filters: SYN scans, brute force, DNS, exfil   │
     |                                             │
     ▼                                             │
[ .pcap Files ] ──────────────────────────────────┘
     |
     ▼
[ Analysis Reports ]
  - Top attacking IPs
  - Credential lists tried
  - Commands executed post-auth
  - Attack timeline
```

---

## 🚀 Setup

Full setup guide is in [`docs/setup.md`](docs/setup.md). High level steps:

1. Create an isolated VM in VirtualBox (Ubuntu Server 22.04)
2. Install and configure Cowrie on the VM
3. Redirect port 22 → 2222 via iptables
4. Run Wireshark/tshark on the host machine capturing the VM's interface
5. Simulate attacks from a second VM to verify capture
6. Run the Python analysis script to correlate logs and packets

---

## 📊 Sample Findings

> *(Screenshots and findings will be added as the lab runs)*

- **Cowrie logs** — attacker IPs, passwords attempted, shell commands run
- **Wireshark captures** — TCP handshakes, SYN scan patterns, brute force timing
- **Python output** — top attacking IPs ranked by attempt count, credential analysis

---

## 📸 Screenshots

> *(To be added)*

- [ ] Cowrie running and listening on port 2222
- [ ] Wireshark capturing live traffic
- [ ] SSH brute force attack hitting the honeypot
- [ ] Cowrie JSON log showing attacker commands
- [ ] Python analysis script output

---

## 🔐 Security Notes

- This lab runs in a fully isolated VirtualBox host-only network
- No real credentials, keys, or sensitive data are stored in this repo
- `.pcap` files containing real attack traffic are excluded via `.gitignore`
- `.env` files with real values are excluded — use `.env.example` as a template

---

## 📚 What I Learned

- How honeypots work at the application layer and why attackers can't tell they're fake
- How to correlate application-layer logs (Cowrie JSON) with network-layer packet captures (Wireshark)
- How to identify attack tool fingerprints — Nmap vs Masscan produce different TCP SYN patterns
- How brute force attacks look at the packet level vs the log level
- Practical use of `tshark` filters, `iptables` NAT rules, and Python log parsing

---

## 🗺️ Roadmap

- [x] Ubuntu Server VM setup
- [x] Cowrie honeypot installed and configured
- [x] GitHub repo and folder structure
- [ ] Port redirect and Wireshark capture running
- [ ] First simulated attack captured end-to-end
- [ ] Python correlation script complete
- [ ] Dionaea malware honeypot added
- [ ] Docker Compose deployment
- [ ] Alerting pipeline (Slack webhook on attack detection)
- [ ] ELK stack / Grafana dashboard for log visualization

---

## 👤 Author

**San Saad**  
[GitHub](https://github.com/San-Saad) 

---

> ⚠️ This project is for educational purposes only. All attack simulations are performed in an isolated lab environment on systems I own.
