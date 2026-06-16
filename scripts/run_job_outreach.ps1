$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path $PSScriptRoot -Parent
$PythonExe = "C:\Users\172ac\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$ScriptPath = Join-Path $RepoRoot "main.py"
$ContactsXlsxPath = Join-Path $RepoRoot "contacts.xlsx"
$ContactsCsvPath = Join-Path $RepoRoot "contacts.csv"
$SenderEmail = "172achyutananda@gmail.com"

. (Join-Path $PSScriptRoot "gmail_credential.ps1")

if (-not (Test-Path -LiteralPath $PythonExe)) {
    throw "Python runtime not found: $PythonExe"
}

if (-not (Test-Path -LiteralPath $ScriptPath)) {
    throw "Sender script not found: $ScriptPath"
}

if (Test-Path -LiteralPath $ContactsXlsxPath) {
    $ContactsPath = $ContactsXlsxPath
}
elseif (Test-Path -LiteralPath $ContactsCsvPath) {
    $ContactsPath = $ContactsCsvPath
}
else {
    $TemplatePath = Join-Path $RepoRoot "samples\contacts_template.csv"
    if (Test-Path -LiteralPath $TemplatePath) {
        Copy-Item -LiteralPath $TemplatePath -Destination $ContactsCsvPath
        Write-Host "Created contacts.csv from contacts_template.csv. Edit contacts.csv with real emails, then run this again."
        exit 0
    }

    throw "contacts.xlsx or contacts.csv not found. Create one with columns: email,company,name"
}

Write-Host "Using contacts file: $ContactsPath"
Write-Host ""
Write-Host "Choose mode:"
Write-Host "1. Preview only"
Write-Host "2. Send test emails to yourself"
Write-Host "3. Send to actual contacts"
$Mode = Read-Host "Enter 1, 2, or 3"

if ($Mode -eq "1") {
    & $PythonExe $ScriptPath --contacts $ContactsPath
    exit $LASTEXITCODE
}

if ($Mode -ne "2" -and $Mode -ne "3") {
    throw "Invalid mode selected."
}

$PlainPassword = Read-GmailAppPassword

try {
    $env:SMTP_EMAIL = $SenderEmail
    $env:SMTP_APP_PASSWORD = $PlainPassword

    if ($Mode -eq "2") {
        & $PythonExe $ScriptPath --contacts $ContactsPath --test-to $SenderEmail --send
    }
    else {
        & $PythonExe $ScriptPath --contacts $ContactsPath --send
    }

    exit $LASTEXITCODE
}
finally {
    Remove-Item Env:\SMTP_EMAIL -ErrorAction SilentlyContinue
    Remove-Item Env:\SMTP_APP_PASSWORD -ErrorAction SilentlyContinue
}
