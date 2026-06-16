"""Command-line interface and orchestration for EmailBot."""

from __future__ import annotations

import argparse
import os
import smtplib
import sys
from pathlib import Path

from emailbot import config
from emailbot.services.contacts import load_contacts
from emailbot.services.mailer import build_message, preview_message, send_messages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send personalized job outreach emails.")
    parser.add_argument(
        "--contacts",
        type=Path,
        default=Path("contacts.csv"),
        help="CSV or XLSX file with email, company, and optional name columns.",
    )
    parser.add_argument(
        "--resume",
        type=Path,
        default=config.DEFAULT_RESUME_PATH,
        help="Resume PDF path to attach.",
    )
    parser.add_argument("--send", action="store_true", help="Actually send the emails.")
    parser.add_argument("--limit", type=int, default=None, help="Only process the first N valid contacts.")
    parser.add_argument("--delay", type=float, default=2.0, help="Seconds to wait between sent emails.")
    parser.add_argument("--test-to", default=None, help="Send every generated email to this address for testing.")
    parser.add_argument(
        "--subject",
        default=None,
        help="Subject template. You can use {company}, {name}, {job_ids}, {job_ids_inline}, and {job_id_label}.",
    )
    parser.add_argument("--smtp-host", default=os.getenv("SMTP_HOST", config.DEFAULT_SMTP_HOST))
    parser.add_argument("--smtp-port", type=int, default=int(os.getenv("SMTP_PORT", config.DEFAULT_SMTP_PORT)))
    parser.add_argument("--from-email", default=os.getenv("SMTP_EMAIL"), help="Sender email address.")
    parser.add_argument(
        "--password",
        default=os.getenv("SMTP_APP_PASSWORD") or os.getenv("SMTP_PASSWORD"),
        help="SMTP password or Gmail app password. Prefer setting SMTP_APP_PASSWORD instead of typing it here.",
    )
    parser.add_argument("--sender-name", default=os.getenv("SENDER_NAME", config.DEFAULT_SENDER_NAME))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    contacts_path = args.contacts.expanduser()
    resume_path = args.resume.expanduser()

    if not contacts_path.exists():
        print(f"Contacts file not found: {contacts_path}", file=sys.stderr)
        return 1

    if not resume_path.exists():
        print(f"Resume attachment not found: {resume_path}", file=sys.stderr)
        return 1

    try:
        contacts = load_contacts(contacts_path)
    except Exception as exc:
        print(f"Could not load contacts: {exc}", file=sys.stderr)
        return 1
    if args.limit is not None:
        contacts = contacts[: args.limit]

    if not contacts:
        print("No valid contacts found.", file=sys.stderr)
        return 1

    messages = [
        build_message(
            contact,
            from_email=args.from_email or "preview@example.com",
            sender_name=args.sender_name,
            subject_template=args.subject,
            resume_path=resume_path,
            test_to=args.test_to,
        )
        for contact in contacts
    ]

    if not args.send:
        print("Preview mode only. Add --send when you are ready to send.\n")
        for contact, message in zip(contacts, messages):
            preview_message(contact, message, resume_path)
        print(f"Prepared {len(messages)} email(s). Nothing was sent.")
        return 0

    if not args.from_email:
        print("Missing sender email. Set SMTP_EMAIL or pass --from-email.", file=sys.stderr)
        return 1

    if not args.password:
        print("Missing SMTP password. Set SMTP_APP_PASSWORD or pass --password.", file=sys.stderr)
        return 1

    try:
        sent, failed = send_messages(
            contacts,
            messages,
            smtp_host=args.smtp_host,
            smtp_port=args.smtp_port,
            from_email=args.from_email,
            password=args.password,
            delay=args.delay,
        )
    except smtplib.SMTPAuthenticationError:
        print("Gmail rejected the login.", file=sys.stderr)
        print("Use a 16-character Gmail app password, not your normal Gmail password.", file=sys.stderr)
        print("Create one here: https://myaccount.google.com/apppasswords", file=sys.stderr)
        return 1

    print(f"Done. Sent: {sent}. Failed: {failed}.")
    return 0 if failed == 0 else 2
