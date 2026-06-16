"""Parsing and normalization of job / requisition IDs from contact rows."""

from __future__ import annotations

import re

JOB_ID_COLUMNS = (
    "job_ids",
    "job ids",
    "job_id",
    "job id",
    "jobids",
    "jobid",
    "job id(s)",
    "opening_ids",
    "opening ids",
    "opening_id",
    "opening id",
    "requisition_ids",
    "requisition ids",
    "requisition_id",
    "requisition id",
    "req_ids",
    "req ids",
    "req_id",
    "req id",
)


def normalize_job_id(job_id: str) -> str:
    job_id = job_id.strip()
    if re.fullmatch(r"\d+\.0+", job_id):
        return job_id.split(".", 1)[0]
    return job_id


def parse_job_ids(*values: str) -> tuple[str, ...]:
    job_ids: list[str] = []
    seen: set[str] = set()

    for value in values:
        if not value:
            continue

        for raw_part in re.split(r"[,;\n|&]+|\band\b", value, flags=re.IGNORECASE):
            part = normalize_job_id(raw_part)
            if not part:
                continue

            if re.fullmatch(r"[A-Za-z0-9_.-]+(?:\s+[A-Za-z0-9_.-]+)+", part):
                candidates = part.split()
            else:
                candidates = [part]

            for candidate in candidates:
                candidate = normalize_job_id(candidate)
                if candidate and candidate not in seen:
                    job_ids.append(candidate)
                    seen.add(candidate)

    return tuple(job_ids)


def extract_job_ids(row: dict[str, str]) -> tuple[str, ...]:
    values = [row[column] for column in JOB_ID_COLUMNS if row.get(column)]
    return parse_job_ids(*values)
