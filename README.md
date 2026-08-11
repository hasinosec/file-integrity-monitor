# File Integrity Monitor

A Python security-monitoring tool that uses SHA-256 hashes to detect files that have been modified, added, or deleted. Unexpected changes to important configuration files can be a sign of unauthorised activity.

## Why I built this

Security Operations teams investigate signals that systems may have been changed without authorisation. This project demonstrates file-integrity monitoring: recording a trusted baseline and comparing the current files against it.

## Features

- Creates a trusted SHA-256 hash baseline for a directory
- Detects modified, new, and deleted files
- Assigns a severity level to detected changes
- Uses only Python's built-in libraries

## Run it

You need Python 3.10 or later. No external packages are required.

Create a baseline of the example files:

```bash
python3 file_integrity_monitor.py baseline demo_files
```

Check the files later:

```bash
python3 file_integrity_monitor.py check demo_files
```

Initially, the result is:

```text
OK: no file-integrity changes detected.
```

To test an alert, edit `demo_files/important_config.txt`, then run the `check` command again. The tool will report a high-severity modified-file alert.

## Security note

The `demo_files` directory contains fictional data only. Never upload real passwords, API keys, personal data, or company files to GitHub.

## Industry context

This is a learning project that recreates a basic File Integrity Monitoring (FIM) workflow: establish a trusted hash baseline, scan monitored files later, and alert when a file has changed, appeared, or disappeared.

Professional security teams often use endpoint-security and FIM tools such as **Microsoft Defender for Cloud**, **Tripwire**, or **Wazuh** to monitor many systems centrally. This script is not a replacement for those platforms; it demonstrates the fundamental hashing and comparison method behind file-integrity alerts.

- Microsoft Defender for Cloud provides File Integrity Monitoring for detecting changes to operating-system files, registries, applications, and Linux system files: [Microsoft FIM documentation](https://learn.microsoft.com/en-us/azure/defender-for-cloud/file-integrity-monitoring-enable-defender-endpoint).
- MITRE ATT&CK documents that adversaries may modify files and directories to manipulate or hide activity: [MITRE ATT&CK: File and Directory Permissions Modification](https://attack.mitre.org/techniques/T1222/).

## What I would improve in production

In a real environment, I would protect the baseline from unauthorised changes, monitor carefully selected sensitive paths, record the process and user responsible for a change, send events to a central SIEM, and tune severity rules with the security team.
