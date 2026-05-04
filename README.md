# Honeypot + Wireshark Cybersecurity Lab

A hands-on cybersecurity home lab that combines a Cowrie SSH honeypot with Wireshark packet capture. The goal is to observe attack behavior at both the application layer and network layer, then analyze captured logs with Python.

## Project Overview

This lab demonstrates how a honeypot can capture suspicious SSH activity while Wireshark records the related packet traffic. The current implementation uses an isolated VirtualBox host-only network so attacks are simulated safely against a VM owned and controlled by the lab owner.

Core capabilities:

- Deploy a Cowrie SSH honeypot on Ubuntu Server
- Capture SSH connection attempts with Wireshark
- Save packet captures as `.pcap` files
- Record attacker usernames, passwords, sessions, and commands in Cowrie JSON logs
- Analyze Cowrie logs with a Python reporting script

## Repository Structure

```text
Honeypot-Wireshark-lab/
|-- analysis/
|   |-- logs/            # Sanitized Cowrie JSON logs for analysis
|   |-- alerts/          # Future alerting scripts
|   `-- reports/         # Python analysis scripts
|-- assets/
|   `-- screenshots/     # Lab setup and evidence screenshots
|-- capture/
|   |-- filters/         # Wireshark display filters
|   |-- pcaps/           # Saved demo packet captures
|   `-- scripts/         # Future tshark automation scripts
|-- docs/
|   |-- architecture.md
|   `-- setup.md
|-- honeypot/
|   |-- config/
|   |-- cowrie/
|   `-- dionaea/
|-- infra/
|-- tests/
|-- .env.example
|-- .gitignore
`-- README.md
```

## Tools Used

| Tool | Purpose |
| --- | --- |
| Cowrie | SSH/Telnet honeypot for logging credentials, sessions, and attacker commands |
| Wireshark | Packet capture and network traffic inspection |
| Python | Log parsing and analysis |
| VirtualBox | Isolated lab VM environment |
| Ubuntu Server | Honeypot host operating system |
| iptables | Port redirection from SSH port 22 to Cowrie port 2222 |

## Lab Architecture

```text
Windows host
  |
  | SSH test traffic
  v
VirtualBox host-only network
  |
  | tcp/2222
  v
Ubuntu honeypot VM
  |
  | Cowrie JSON logs
  v
Python analysis script

Wireshark runs on the Windows host and captures the network traffic between
the host machine and the honeypot VM.
```

## Current Evidence

Setup screenshots:

- [01 - Cowrie virtual environment active](assets/screenshots/01-cowrie-env-active.png)
- [02 - Cowrie service started](assets/screenshots/02-cowrie-start.png)
- [03 - Cowrie listening on port 2222](assets/screenshots/03-cowrie-listening-2222.png)
- [04 - iptables redirect configured](assets/screenshots/04-iptables-redirect.png)
- [05 - Wireshark interface selected](assets/screenshots/05-wireshark-interfaces.png)
- [06 - Wireshark capturing SSH traffic](assets/screenshots/06-wireshark-capturing.png)
- [07 - Cowrie JSON logs showing attack activity](assets/screenshots/07-cowrie-json-logs.png)
- [08 - Wireshark SYN filter applied](assets/screenshots/08-wireshark-syn-filter.png)

Packet capture:

- [Demo honeypot packet capture](capture/pcaps/honeypot-capture-demo.pcapng)

Wireshark filters:

- [Display filters used in the lab](capture/filters/wireshark-display-filters.txt)

## Python Log Analysis

The analyzer is located at:

```text
analysis/reports/analyze_logs.py
```

Expected input:

```text
analysis/logs/cowrie.json
```

Run from the repository root:

```powershell
py analysis\reports\analyze_logs.py analysis\logs\cowrie.json
```

The script summarizes:

- Top source IP addresses
- Usernames attempted
- Passwords attempted
- Credential pairs
- Successful and failed honeypot logins
- Commands entered after login
- Event type counts
- Command timeline by session

## Key Findings So Far

- Cowrie was successfully deployed and listened on TCP port 2222.
- The Windows host reached the honeypot through the VirtualBox host-only network.
- Wireshark captured the SSH handshake and traffic to the honeypot.
- Cowrie recorded failed login attempts, a successful honeypot login, and commands entered in the fake shell.

## Roadmap

- [x] Create GitHub repository and project structure
- [x] Deploy Ubuntu Server VM
- [x] Install and start Cowrie
- [x] Configure port redirection
- [x] Capture SSH traffic in Wireshark
- [x] Save demo `.pcap` file
- [x] Add Wireshark display filters
- [x] Add Python Cowrie log analyzer
- [ ] Add sanitized Cowrie JSON sample
- [ ] Run analyzer against real lab logs
- [ ] Add screenshot of Python analysis output
- [ ] Expand `docs/setup.md`
- [ ] Add architecture documentation
- [ ] Add automated tshark capture script
- [ ] Add alerting pipeline

## Security Notes

- This project is for education and portfolio demonstration only.
- All attack simulations are performed in an isolated lab environment on systems owned by the lab owner.
- Do not commit real credentials, private keys, public attacker IPs, or sensitive network information.
- Real-world packet captures can contain sensitive data. Only sanitized demo captures should be committed.

## Author

San Saad  
[GitHub](https://github.com/San-Saad)
