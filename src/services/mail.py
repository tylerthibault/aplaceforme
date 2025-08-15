import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Iterable


DEV_MAIL_DIR = Path(__file__).resolve().parents[2] / "data" / "outbox"
DEV_MAIL_DIR.mkdir(parents=True, exist_ok=True)


def _smtp_client():
    host = os.environ.get("SMTP_HOST")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASSWORD")
    if not host:
        return None
    client = smtplib.SMTP(host, port)
    client.starttls()
    if user and password:
        client.login(user, password)
    return client


def send_email(subject: str, html: str, text: str, to_addrs: Iterable[str]):
    from_addr = os.environ.get("MAIL_FROM", "no-reply@example.com")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addrs)
    if text:
        msg.set_content(text)
    if html:
        msg.add_alternative(html, subtype="html")

    client = _smtp_client()
    if client is None:
        # Dev mode: write .eml to disk
        fname = (DEV_MAIL_DIR / f"{subject.replace(' ', '_')}.eml").with_suffix(".eml")
        fname.write_bytes(msg.as_bytes())
        return

    with client as c:
        c.send_message(msg)
