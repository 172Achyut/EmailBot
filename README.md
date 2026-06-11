# EmailBot

EmailBot sends personalized job outreach emails from `contacts.xlsx` or `contacts.csv`, attaches your resume, and can run in preview, test, or real-send mode.

## Files

- `send_job_outreach.py` - main Python email sender
- `run_job_outreach.ps1` - menu launcher: preview, test, or send
- `test_job_outreach.ps1` - test-only launcher that sends generated emails to your own Gmail
- `save_gmail_app_password.ps1` - saves your Gmail app password in Windows Credential Manager
- `contacts_template.csv` - sample contact file format

Private files like `contacts.xlsx`, `contacts.csv`, and `__pycache__` are ignored by Git.

## Contact File

Create or edit `contacts.xlsx` in the same folder as the scripts.

Use these columns:

```csv
email,company,name
recruiter@example.com,Ivanti,Shubhangi
hr@example.com,Example Company,
```

`name` is optional. If blank, the email starts with `Hi there,`.

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
