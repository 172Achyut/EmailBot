"""Default values and shared paths for EmailBot."""

from __future__ import annotations

from pathlib import Path

# Repository root (parent of the emailbot package) and template location.
ROOT_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT_DIR / "templates"

DEFAULT_RESUME_PATH = Path(r"D:\Resume\FE\Achyutananda_Nayak_Resume.pdf")
DEFAULT_SUBJECT = "Interest in Full Stack Opportunities at {company}"
DEFAULT_REFERRAL_SUBJECT = "Request for Referral - {job_id_label} {job_ids_inline} ({company})"
DEFAULT_SENDER_NAME = "Achyutananda Nayak"
DEFAULT_SMTP_HOST = "smtp.gmail.com"
DEFAULT_SMTP_PORT = 587
