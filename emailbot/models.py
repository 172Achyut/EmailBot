"""Data models shared across EmailBot."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Contact:
    email: str
    company: str
    name: str
    job_ids: tuple[str, ...]
    frontend_outreach: bool
    row_number: int
