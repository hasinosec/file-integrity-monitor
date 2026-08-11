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
