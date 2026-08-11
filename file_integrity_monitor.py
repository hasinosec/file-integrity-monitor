"""Create and compare SHA-256 file-integrity baselines."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(file_path: Path) -> str:
    """Return the SHA-256 hash of one file."""
    digest = hashlib.sha256()
    with file_path.open("rb") as file:
        for block in iter(lambda: file.read(8192), b""):
            digest.update(block)
    return digest.hexdigest()


def scan(directory: Path) -> dict[str, str]:
    """Hash all files below a directory, excluding the baseline itself."""
    return {
        str(file.relative_to(directory)): sha256(file)
        for file in sorted(directory.rglob("*"))
        if file.is_file() and file.name != "baseline.json"
    }


def create_baseline(directory: Path, baseline_path: Path) -> None:
    baseline_path.write_text(json.dumps(scan(directory), indent=2) + "\n", encoding="utf-8")
    print(f"Baseline created: {baseline_path}")


def check_baseline(directory: Path, baseline_path: Path) -> int:
    if not baseline_path.is_file():
        print("No baseline found. Run with the 'baseline' command first.")
        return 1

    expected = json.loads(baseline_path.read_text(encoding="utf-8"))
    current = scan(directory)
    changes = 0

    for name in sorted(expected.keys() - current.keys()):
        print(f"ALERT [HIGH] Deleted file: {name}")
        changes += 1
    for name in sorted(current.keys() - expected.keys()):
        print(f"ALERT [MEDIUM] New file: {name}")
        changes += 1
    for name in sorted(expected.keys() & current.keys()):
        if expected[name] != current[name]:
            print(f"ALERT [HIGH] Modified file: {name}")
            changes += 1

    if changes == 0:
        print("OK: no file-integrity changes detected.")
    else:
        print(f"SECURITY SUMMARY: {changes} integrity change(s) detected.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor files for integrity changes.")
    parser.add_argument("command", choices=("baseline", "check"), help="Create a baseline or check it")
    parser.add_argument("directory", type=Path, help="Directory to monitor")
    parser.add_argument("--baseline", type=Path, default=Path("baseline.json"), help="Baseline JSON path")
    args = parser.parse_args()

    if not args.directory.is_dir():
        parser.error(f"Directory not found: {args.directory}")
    baseline_path = args.baseline if args.baseline.is_absolute() else args.directory / args.baseline
    if args.command == "baseline":
        create_baseline(args.directory, baseline_path)
    else:
        check_baseline(args.directory, baseline_path)


if __name__ == "__main__":
    main()
