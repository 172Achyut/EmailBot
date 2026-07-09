"""Email body templates and template-context construction."""

from __future__ import annotations

from functools import lru_cache

from emailbot import config
from emailbot.models import Contact

OUTREACH_TEMPLATE = "outreach.txt"
FRONTEND_OUTREACH_TEMPLATE = "frontend_outreach.txt"
REFERRAL_TEMPLATE = "referral.txt"


@lru_cache(maxsize=None)
def load_template(name: str) -> str:
    return (config.TEMPLATE_DIR / name).read_text(encoding="utf-8")


def format_job_ids_inline(job_ids: tuple[str, ...]) -> str:
    if len(job_ids) <= 1:
        return "".join(job_ids)
    return f"{', '.join(job_ids[:-1])} & {job_ids[-1]}"


def format_job_id_bullets(job_ids: tuple[str, ...]) -> str:
    return "\n".join(f"- {job_id}" for job_id in job_ids)


def build_template_context(contact: Contact) -> dict[str, str]:
    return {
        "company": contact.company,
        "name": contact.name,
        "job_id_label": "Job ID" if len(contact.job_ids) == 1 else "Job IDs",
        "job_ids": ", ".join(contact.job_ids),
        "job_ids_inline": format_job_ids_inline(contact.job_ids),
        "job_id_bullets": format_job_id_bullets(contact.job_ids),
    }


def render_body(contact: Contact, context: dict[str, str]) -> str:
    if contact.frontend_outreach:
        template_name = FRONTEND_OUTREACH_TEMPLATE
    elif contact.job_ids:
        template_name = REFERRAL_TEMPLATE
    else:
        template_name = OUTREACH_TEMPLATE
    return load_template(template_name).format(**context)
