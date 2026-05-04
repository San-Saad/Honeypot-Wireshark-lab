# Setup Guide

This document explains how the Honeypot + Wireshark Cybersecurity Lab was built and validated.

## Lab Environment

Host machine:

- Windows
- VirtualBox
- Wireshark
- VS Code
- Git
- Python

Honeypot VM:

- Ubuntu Server
- Cowrie SSH honeypot
- Host-only network adapter
- Honeypot IP: `192.168.56.101`
- Cowrie listening port: `2222`

## 1. Start the Ubuntu Honeypot VM

Open VirtualBox and start the honeypot VM.

Log in with the lab admin account.

## 2. Start Cowrie

Switch to the Cowrie user:

```bash
sudo su - cowrie
```

Go to the Cowrie directory:

```bash
cd cowrie
```

Activate the Cowrie virtual environment:

```bash
source cowrie-env/bin/activate
```

Start Cowrie:

```bash
cowrie-env/bin/cowrie start
```

## 3. Verify Cowrie Is Listening

Check that Cowrie is listening on port `2222`:

```bash
ss -tlnp | grep 2222
```

Expected result:

```text
0.0.0.0:2222
```

## 4. Configure Port Redirection

Cowrie listens on port `2222`, but attackers usually target SSH on port `22`. iptables can redirect port `22` traffic to port `2222`.

Exit back to the admin user:

```bash
exit
```

Add the redirect:

```bash
sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222
```

Verify the rule:

```bash
sudo iptables -t nat -L
```

## 5. Configure Wireshark

Open Wireshark on the Windows host.

Select the VirtualBox host-only interface. In this lab, the interface appeared as:

```text
Ethernet 3
```

Useful Wireshark display filters:

```text
tcp.port == 2222
tcp.flags.syn == 1 && tcp.flags.ack == 0
ip.addr == 192.168.56.1 && ip.addr == 192.168.56.101
```

## 6. Simulate SSH Activity

From Windows PowerShell, connect to the honeypot:

```powershell
ssh root@192.168.56.101 -p 2222
```

Use fake credentials when prompted. The login attempt is captured by Cowrie and appears in Wireshark.

## 7. Save the Packet Capture

In Wireshark:

1. Stop the live capture.
2. Save the capture to:

```text
capture/pcaps/honeypot-capture-demo.pcapng
```

## 8. Copy and Sanitize Cowrie Logs

On the Ubuntu VM, create a sanitized log copy:

```bash
sed -e 's/<lab-password>/<redacted>/g' -e 's/192\.168\.56\.101/LAB_HONEYPOT/g' -e 's/192\.168\.56\.1/LAB_HOST/g' var/log/cowrie/cowrie.json > /tmp/cowrie-sanitized.json
```

Copy the sanitized log to the Windows repo:

```powershell
scp -P 2200 <vm-user>@127.0.0.1:/tmp/cowrie-sanitized.json analysis\logs\cowrie.json
```

## 9. Run the Python Analyzer

From the repository root:

```powershell
py analysis\reports\analyze_logs.py analysis\logs\cowrie.json
```

The script outputs:

- Total Cowrie events
- Unique source IPs
- Failed and successful login attempts
- Captured commands
- Top usernames and passwords
- Event type counts
- Command timeline by session

## 10. Publish Evidence to GitHub

Stage and commit the final artifacts:

```powershell
git add .
git commit -m "Add sanitized Cowrie log analysis output"
git push origin main
```

## Notes

Only sanitized logs and demo packet captures should be committed to GitHub. Avoid committing real credentials, private keys, public attacker IPs, or sensitive network details.
