# Packet Captures

This folder contains demo packet captures from the honeypot lab.

## Files

- `honeypot-capture-demo.pcapng` - Wireshark packet capture showing SSH traffic between the Windows host and Cowrie honeypot VM.

## How to View

GitHub cannot preview `.pcapng` packet capture files directly. To inspect the capture:

1. Download the `.pcapng` file.
2. Open it in Wireshark.
3. Apply a display filter such as:

```text
tcp.port == 2222
```
