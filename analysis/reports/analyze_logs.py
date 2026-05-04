#!/usr/bin/env python3
"""Analyze Cowrie JSON logs from the honeypot lab."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


LOGIN_EVENTS = {"cowrie.login.failed", "cowrie.login.success"}
COMMAND_EVENTS = {"cowrie.command.input"}
CONNECT_EVENTS = {"cowrie.session.connect"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize Cowrie JSON events: source IPs, credentials, commands, and timeline."
    )
    parser.add_argument(
        "logfile",
        nargs="?",
        default="analysis/logs/cowrie.json",
        help="Path to Cowrie JSON log file. Default: analysis/logs/cowrie.json",
    )
    return parser.parse_args()


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    skipped = 0

    with path.open("r", encoding="utf-8-sig") as log_file:
        for line_number, line in enumerate(log_file, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                skipped += 1
                print(f"[warning] skipped invalid JSON on line {line_number}")

    if skipped:
        print(f"[warning] skipped {skipped} malformed log line(s)")

    return events


def event_time(event: dict[str, Any]) -> datetime | None:
    timestamp = event.get("timestamp")
    if not isinstance(timestamp, str):
        return None

    try:
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return None


def format_counter(counter: Counter[str], limit: int = 10) -> list[str]:
    if not counter:
        return ["  None observed"]

    return [f"  {value}: {count}" for value, count in counter.most_common(limit)]


def main() -> int:
    args = parse_args()
    log_path = Path(args.logfile)

    if not log_path.exists():
        print(f"Log file not found: {log_path}")
        print("Copy your Cowrie log to analysis/logs/cowrie.json or pass a path:")
        print("  python analysis/reports/analyze_logs.py path/to/cowrie.json")
        return 1

    events = load_events(log_path)
    if not events:
        print(f"No events found in {log_path}")
        return 1

    source_ips: Counter[str] = Counter()
    usernames: Counter[str] = Counter()
    passwords: Counter[str] = Counter()
    credentials: Counter[str] = Counter()
    commands: Counter[str] = Counter()
    event_types: Counter[str] = Counter()
    session_sources: dict[str, str] = {}
    commands_by_session: dict[str, list[str]] = defaultdict(list)
    login_successes = 0
    login_failures = 0
    first_seen: datetime | None = None
    last_seen: datetime | None = None

    for event in events:
        event_id = str(event.get("eventid", "unknown"))
        event_types[event_id] += 1

        timestamp = event_time(event)
        if timestamp is not None:
            first_seen = timestamp if first_seen is None else min(first_seen, timestamp)
            last_seen = timestamp if last_seen is None else max(last_seen, timestamp)

        session = str(event.get("session", "unknown"))
        source_ip = event.get("src_ip")
        if isinstance(source_ip, str) and source_ip:
            source_ips[source_ip] += 1
            session_sources[session] = source_ip

        if event_id in LOGIN_EVENTS:
            username = str(event.get("username", "<missing>"))
            password = str(event.get("password", "<missing>"))
            usernames[username] += 1
            passwords[password] += 1
            credentials[f"{username}:{password}"] += 1

            if event_id == "cowrie.login.success":
                login_successes += 1
            else:
                login_failures += 1

        if event_id in COMMAND_EVENTS:
            command = str(event.get("input", "")).strip()
            if command:
                commands[command] += 1
                commands_by_session[session].append(command)

    print("Cowrie Honeypot Log Analysis")
    print("=" * 29)
    print(f"Log file: {log_path}")
    print(f"Total events: {len(events)}")
    print(f"Unique source IPs: {len(source_ips)}")
    print(f"Failed logins: {login_failures}")
    print(f"Successful honeypot logins: {login_successes}")
    print(f"Commands captured: {sum(commands.values())}")

    if first_seen and last_seen:
        print(f"First event: {first_seen.isoformat()}")
        print(f"Last event: {last_seen.isoformat()}")

    print("\nTop Source IPs")
    print("-" * 14)
    print("\n".join(format_counter(source_ips)))

    print("\nTop Usernames")
    print("-" * 13)
    print("\n".join(format_counter(usernames)))

    print("\nTop Passwords")
    print("-" * 13)
    print("\n".join(format_counter(passwords)))

    print("\nTop Credential Pairs")
    print("-" * 20)
    print("\n".join(format_counter(credentials)))

    print("\nCommands Entered")
    print("-" * 16)
    print("\n".join(format_counter(commands)))

    print("\nEvent Types")
    print("-" * 11)
    print("\n".join(format_counter(event_types)))

    if commands_by_session:
        print("\nCommand Timeline By Session")
        print("-" * 27)
        for session, session_commands in commands_by_session.items():
            source = session_sources.get(session, "unknown")
            print(f"  {session} ({source})")
            for command in session_commands:
                print(f"    $ {command}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
