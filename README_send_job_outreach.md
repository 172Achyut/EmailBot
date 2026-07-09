# Job Outreach Email Sender

This folder contains a Python script that reads contacts from a CSV, writes the email in your sample format, and attaches:

`D:\Resume\FE\Achyutananda_Nayak_Resume.pdf`

## 1. Prepare contacts

Edit `contacts.xlsx` or `contacts.csv` with columns:

```csv
email,company,name,job_ids,frontend_outreach
shubhangi.joshi@example.com,Ivanti,Shubhangi,,
frontend.recruiter@example.com,Example Company,Anu,,yes
recruiter@example.com,EXL,Palvika,"10656, 14884, 7312, 13879, 11568",
```

`name` is optional. If it is blank, the email starts with `Hi there,`.
`job_ids` is optional. If it has values, the script sends the referral request format. Leave it blank for the normal outreach email.
`frontend_outreach` is optional. Put `yes` to send the frontend role outreach email from `templates/frontend_outreach.txt`.

If both `contacts.xlsx` and `contacts.csv` are present, `run_job_outreach.ps1` uses `contacts.xlsx`.

## 2. Preview emails

Simplest option:

```powershell
cd D:\Resume\outputs
powershell -ExecutionPolicy Bypass -File .\run_job_outreach.ps1
```

Choose:

- `1` for preview only
- `2` to send test emails to `172achyutananda@gmail.com`
- `3` to send to actual contacts

The launcher uses `172achyutananda@gmail.com` and asks for the Gmail app password only when sending.

To save the Gmail app password securely in Windows Credential Manager, run once:

```powershell
cd D:\Resume\scripts
powershell -ExecutionPolicy Bypass -File .\save_gmail_app_password.ps1
```

After that, `test_job_outreach.ps1` and `run_job_outreach.ps1` will use the saved password automatically. Spaces in the app password are removed automatically.

To send only a test email to yourself:

```powershell
cd D:\Resume\scripts
powershell -ExecutionPolicy Bypass -File .\test_job_outreach.ps1
```

Manual option:

Run this first:

```powershell
cd C:\Users\172ac\Documents\Codex\2026-06-11\files-mentioned-by-the-user-codex\outputs
python .\send_job_outreach.py --contacts .\contacts.csv
```

If PowerShell says `python` is not recognized, use the bundled Python available on this machine:

```powershell
& "C:\Users\172ac\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\send_job_outreach.py --contacts .\contacts.csv
```

The script previews every email and sends nothing unless `--send` is added.

## 3. Configure Gmail SMTP

For Gmail, create an app password, then set these in PowerShell:

```powershell
$env:SMTP_EMAIL="yourgmail@gmail.com"
$env:SMTP_APP_PASSWORD="your 16 character app password"
```

## 4. Send

After checking the preview:

```powershell
python .\send_job_outreach.py --contacts .\contacts.csv --send
```

Bundled Python version:

```powershell
& "C:\Users\172ac\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\send_job_outreach.py --contacts .\contacts.csv --send
```

Useful options:

```powershell
python .\send_job_outreach.py --contacts .\contacts.csv --limit 1
python .\send_job_outreach.py --contacts .\contacts.csv --test-to yourgmail@gmail.com --send
python .\send_job_outreach.py --contacts .\contacts.csv --resume "D:\Resume\FE\Achyutananda_Nayak_Resume.pdf" --send
```
