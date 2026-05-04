# Cowrie Logs

Place sanitized Cowrie JSON logs here for analysis.

Expected filename:

```text
cowrie.json
```

Run the analyzer from the repository root:

```powershell
python analysis\reports\analyze_logs.py analysis\logs\cowrie.json
```

Do not commit logs that contain public IP addresses, real usernames, real passwords, or sensitive network details.
