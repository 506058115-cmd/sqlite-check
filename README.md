# sqlite-check

Run SQLite's structural quick check and foreign-key check against a database opened in read-only mode. Diagnostic identifiers are JSON-escaped; row data is not printed and the database is never changed.

## Use

Requires Python 3.8+; no packages to install.

```sh
python sqlite_check.py app.db
```

Exit status is `0` when both checks pass, `1` when either check reports problems, and `2` when the database cannot be opened or checked. SQLite may still need read access to related WAL files for databases using write-ahead logging.

## License

MIT
