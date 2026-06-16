$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path $PSScriptRoot -Parent
$PythonExe = "C:\Users\172ac\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$ScriptPath = Join-Path $RepoRoot "main.py"
$ContactsXlsxPath = Join-Path $RepoRoot "contacts.xlsx"
$ContactsCsvPath = Join-Path $RepoRoot "contacts.csv"
$SenderEmail = "172achyutananda@gmail.com"

. (Join-Path $PSScriptRoot "gmail_credential.ps1")

if (Test-Path -LiteralPath $ContactsXlsxPath) {
    $ContactsPath = $ContactsXlsxPath
}
elseif (Test-Path -LiteralPath $ContactsCsvPath) {
    $ContactsPath = $ContactsCsvPath
}
else {
    throw "contacts.xlsx or contacts.csv not found. Create one with columns: email,company,name"
}

Write-Host "Test mode: generated emails will be sent only to $SenderEmail"
Write-Host "Using contacts file: $ContactsPath"

$PlainPassword = Read-GmailAppPassword

try {
    $env:SMTP_EMAIL = $SenderEmail
    $env:SMTP_APP_PASSWORD = $PlainPassword

    & $PythonExe $ScriptPath --contacts $ContactsPath --test-to $SenderEmail --send
    exit $LASTEXITCODE
}
finally {
    Remove-Item Env:\SMTP_EMAIL -ErrorAction SilentlyContinue
    Remove-Item Env:\SMTP_APP_PASSWORD -ErrorAction SilentlyContinue
}
