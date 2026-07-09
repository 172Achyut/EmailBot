# EmailBot

EmailBot sends personalized job outreach emails from `contacts.xlsx` or `contacts.csv`, attaches your resume, and can run in preview, test, or real-send mode.

## Files

- `main.py` - entry point (`python main.py` or `python -m emailbot`)
- `emailbot/` - application package
  - `cli.py` - argument parsing and orchestration
  - `config.py` - defaults and shared paths
  - `models.py` - `Contact` data model
  - `services/contacts.py` - load/validate contacts from CSV or XLSX
  - `services/jobids.py` - parse and normalize job IDs
  - `services/templates.py` - load templates and build template context
  - `services/mailer.py` - build messages, preview, and SMTP delivery
- `templates/` - email bodies (`outreach.txt`, `frontend_outreach.txt`, `referral.txt`)
- `scripts/` - Windows PowerShell launchers and Gmail credential helper
- `samples/contacts_template.csv` - sample contact file format

Private files like `contacts.xlsx`, `contacts.csv`, and `__pycache__` are ignored by Git.

## Contact File

Create or edit `contacts.xlsx` in the same folder as the scripts.

Use these columns:

```csv
email,company,name,job_ids,frontend_outreach
recruiter@example.com,Ivanti,Shubhangi,,
frontend.recruiter@example.com,Example Company,Anu,,yes
hr@example.com,EXL,Palvika,"10656, 14884, 7312, 13879, 11568",
```

`name` is optional. If blank, the email starts with `Hi there,`.
`job_ids` is optional. If it has values, the script uses the referral request email with the IDs listed in the subject and body. Leave it blank for the normal outreach email.
`frontend_outreach` is optional. Put `yes` to use the frontend role outreach email from `templates/frontend_outreach.txt`. Leave it blank for the normal outreach/referral behavior.

If both `contacts.xlsx` and `contacts.csv` exist, the launcher uses `contacts.xlsx`.

## Resume Attachment

The script attaches this resume by default:

```text
D:\Resume\FE\Achyutananda_Nayak_Resume.pdf
```

## One-Time Password Setup

Gmail requires a 16-character app password for SMTP. Your normal Gmail browser password will not work.

Run this once:

```powershell
cd D:\Resume\scripts
powershell -ExecutionPolicy Bypass -File .\save_gmail_app_password.ps1
```

Paste the Gmail app password when asked. Spaces are okay; the script removes them automatically. The password is saved in Windows Credential Manager.

## Preview Only

Preview generated emails without sending:

```powershell
cd D:\Resume\scripts
powershell -ExecutionPolicy Bypass -File .\run_job_outreach.ps1
```

Choose:

```text
1
```

## Test Send

Send all generated emails only to your own Gmail address:

```powershell
cd D:\Resume\scripts
powershell -ExecutionPolicy Bypass -File .\test_job_outreach.ps1
```

Use this before sending to actual contacts.

## Send To Actual Contacts

After preview and test are successful:

```powershell
cd D:\Resume\scripts
powershell -ExecutionPolicy Bypass -File .\run_job_outreach.ps1
```

Choose:

```text
3
```
