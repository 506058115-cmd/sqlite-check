#!/usr/bin/env python3
"""Check SQLite structure and foreign keys without changing the database."""

import argparse
import json
from pathlib import Path
import sqlite3
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Run SQLite quick_check and foreign_key_check in read-only mode."
    )
    parser.add_argument("database", help="SQLite database file")
    args = parser.parse_args()

    connection = None
    try:
        uri = Path(args.database).resolve().as_uri() + "?mode=ro"
        connection = sqlite3.connect(uri, uri=True)
        quick = [row[0] for row in connection.execute("PRAGMA quick_check")]
        foreign_keys = list(connection.execute("PRAGMA foreign_key_check"))
    except (OSError, sqlite3.Error, ValueError) as error:
        print(f"sqlite-check: unable to check database: {error}", file=sys.stderr)
        return 2
    finally:
        if connection is not None:
            connection.close()

    problems = [message for message in quick if message != "ok"]
    print(f"SQLite quick_check: {'ok' if not problems else f'{len(problems)} problem(s)'}")
    for message in problems:
        print("  " + json.dumps(message, ensure_ascii=True))
    print(f"Foreign key violations: {len(foreign_keys)}")
    for row in foreign_keys:
        print("  " + json.dumps(row, ensure_ascii=True))
    if not problems and not foreign_keys:
        print("Database checks passed; no row contents were read into output.")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
