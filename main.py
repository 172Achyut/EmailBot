#!/usr/bin/env python3
"""Entry point for EmailBot.

Send personalized job outreach emails from a CSV or Excel contacts file.

Contact file columns:
  email, company, name, job_ids

The "name" and "job_ids" columns are optional. If job_ids is present, the
referral request email template is used. Emails are previewed by default;
add --send only when you are ready to actually send them.
"""

from emailbot.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
