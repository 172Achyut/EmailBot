$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "gmail_credential.ps1")

$SecurePassword = Read-Host "Paste Gmail app password for $GmailCredentialUser" -AsSecureString
Save-GmailAppPassword -SecurePassword $SecurePassword

Write-Host "Saved Gmail app password in Windows Credential Manager."
Write-Host "Now run test_job_outreach.ps1 or run_job_outreach.ps1."
