"""Message construction, previewing, and SMTP delivery."""

from __future__ import annotations

import mimetypes
import smtplib
import ssl
import sys
import time
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
from pathlib import Path

from emailbot import config
from emailbot.models import Contact
from emailbot.services.templates import build_template_context, render_body


def add_attachment(message: EmailMessage, attachment_path: Path) -> None:
    content_type, _ = mimetypes.guess_type(attachment_path.name)
    maintype, subtype = (content_type or "application/octet-stream").split("/", 1)

    with attachment_path.open("rb") as file:
        message.add_attachment(
            file.read(),
            maintype=maintype,
            subtype=subtype,
            filename=attachment_path.name,
        )


def build_message(
    contact: Contact,
    *,
    from_email: str,
    sender_name: str,
    subject_template: str | None,
    resume_path: Path,
    test_to: str | None,
) -> EmailMessage:
    context = build_template_context(contact)
    if subject_template:
        effective_subject_template = subject_template
    elif contact.frontend_outreach:
        effective_subject_template = config.DEFAULT_FRONTEND_SUBJECT
    elif contact.job_ids:
        effective_subject_template = config.DEFAULT_REFERRAL_SUBJECT
    else:
        effective_subject_template = config.DEFAULT_SUBJECT
    subject = effective_subject_template.format(**context)
    body = render_body(contact, context)
    to_email = test_to or contact.email

    message = EmailMessage()
    message["From"] = formataddr((sender_name, from_email))
    message["To"] = to_email
    message["Subject"] = subject
    message["Message-ID"] = make_msgid()

    if test_to:
        message["X-Original-To"] = contact.email

    message.set_content(body)
    add_attachment(message, resume_path)
    return message


def normalize_smtp_password(password: str, smtp_host: str) -> str:
    if "gmail" in smtp_host.lower():
        return "".join(password.split())
    return password


def get_plain_text_body(message: EmailMessage) -> str:
    if not message.is_multipart():
        return message.get_content()

    for part in message.walk():
        if part.get_content_type() == "text/plain" and part.get_content_disposition() != "attachment":
            return part.get_content()

    return ""


def preview_message(contact: Contact, message: EmailMessage, resume_path: Path) -> None:
    print("=" * 72)
    print(f"Contact row: {contact.row_number}")
    print(f"To: {message['To']}")
    if message.get("X-Original-To"):
        print(f"Original To: {message['X-Original-To']}")
    print(f"Subject: {message['Subject']}")
    print(f"Attachment: {resume_path}")
    print("-" * 72)
    print(get_plain_text_body(message).strip())
    print()


def send_messages(
    contacts: list[Contact],
    messages: list[EmailMessage],
    *,
    smtp_host: str,
    smtp_port: int,
    from_email: str,
    password: str,
    delay: float,
) -> tuple[int, int]:
    """Send all messages over SMTP. Returns (sent, failed).

    Raises smtplib.SMTPAuthenticationError on login rejection (caller reports it).
    """
    context = ssl.create_default_context()
    sent = 0
    failed = 0

    with smtplib.SMTP(smtp_host, smtp_port) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.ehlo()
        smtp_password = normalize_smtp_password(password, smtp_host)
        smtp.login(from_email, smtp_password)

        for index, (contact, message) in enumerate(zip(contacts, messages), start=1):
            try:
                smtp.send_message(message)
                sent += 1
                print(f"[{index}/{len(messages)}] Sent to {message['To']} for {contact.company}")
            except Exception as exc:
                failed += 1
                print(f"[{index}/{len(messages)}] Failed for {contact.email}: {exc}", file=sys.stderr)

            if index < len(messages) and delay > 0:
                time.sleep(delay)

    return sent, failed
