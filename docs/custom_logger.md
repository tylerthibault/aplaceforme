# Custom Logger Design Document

## Overview

This is a **generic Python logger** (not specific to any single project) that provides flexible logging for any application. It does **not** use Python’s built-in `logging` module. It supports three output targets:
- Print to the terminal (console)
- Write to a dated text log file
- Write to a database table (`log_entries`)

Logging can be enabled for any combination of these outputs.

---

## Features

- **Log Levels:** Supports at least `INFO`, `WARNING`, `ERROR`, and `DEBUG`.
- **Output Targets:** Configurable per log message or globally for the logger instance:
    - Terminal (stdout)
    - Dated text file (in a `/logs` directory, e.g., `logs/2025-07-04.log`)
    - Database table (default: `log_entries`)
- **Message Format:**  
  Each log message should include:
    - Timestamp (UTC)
    - Log level
    - Source (optional: e.g., module/function)
    - Message text
    - Code (short GUID for tracing log origin in code)
    - (Optional) User/session/request info if available

---

## Logger API

Basic interface methods:
- `log(level, message, code, **kwargs)` — Logs a message with level, code, and optional context.
- `info(message, code, **kwargs)`
- `warning(message, code, **kwargs)`
- `error(message, code, **kwargs)`
- `debug(message, code, **kwargs)`
- Configuration options for enabling/disabling output targets.

---

## File Output

- Log files are named by date: `YYYY-MM-DD.log`
- Stored in `/logs` directory at the project root.
- Each log entry is one line, formatted as:  
  `[2025-07-04 00:15:24][INFO][main.py:funcname][CODE:abc123] Message`

---

## Database Output

- Uses a dedicated table: `log_entries`
- Each log message is inserted as a new row with full metadata, including the `code` field.

---

## Usage Example

```python
logger = CustomLogger(to_terminal=True, to_file=True, to_db=True)
logger.info("User login succeeded", code="a1b2c", user_id=5, source="auth.py:login")
logger.error("File upload failed", code="d9e8f", filename="audio.mp3", source="upload.py:save_file")
```

---

## Additional Notes

- Consider adding rotation/cleanup for old log files.
- Database writes should be non-blocking or handled asynchronously if possible.
- Logger should handle its own errors gracefully (never crash the app if logging fails).
- The `code` (shortGUID) can be generated once per log call site and reused for consistent lookup.
- This logger can be adapted for any project by adjusting the database table and output settings.
