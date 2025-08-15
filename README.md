# Marla Baily — A Place For Me (MVP)

Quickstart (dev):

1. Create virtual env and install deps
2. Run the app

Dev env variables (optional):
- SECRET_KEY (default dev-secret-change-me)
- DATABASE_URL (defaults to ./data/app.db)
- ADMIN_USERNAME (default admin)
- ADMIN_PASSWORD (default change-me)
- SMTP_HOST/SMTP_PORT/SMTP_USER/SMTP_PASSWORD (optional; when omitted, emails are written to ./data/outbox)

Notes:
- Media is stored as base64 strings in SQLite (MVP convenience). Suitable for small content; not optimal at scale.
- Rich text fields are sanitized before rendering.

---

MIT License
