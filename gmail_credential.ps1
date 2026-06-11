$GmailCredentialTarget = "Codex.JobOutreach.Gmail.AppPassword"
$GmailCredentialUser = "172achyutananda@gmail.com"

function Initialize-GmailCredentialInterop {
    if ("CredentialManagerInterop.NativeMethods" -as [type]) {
        return
    }

    Add-Type @"
using System;
using System.Runtime.InteropServices;

namespace CredentialManagerInterop {
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    public struct FileTime {
        public uint LowDateTime;
        public uint HighDateTime;
    }

    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    public struct Credential {
        public uint Flags;
        public uint Type;
        public string TargetName;
        public string Comment;
        public FileTime LastWritten;
        public uint CredentialBlobSize;
        public IntPtr CredentialBlob;
        public uint Persist;
        public uint AttributeCount;
        public IntPtr Attributes;
        public string TargetAlias;
        public string UserName;
    }

    public class NativeMethods {
        [DllImport("Advapi32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
        public static extern bool CredRead(string target, uint type, uint reservedFlag, out IntPtr credentialPtr);

        [DllImport("Advapi32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
        public static extern bool CredWrite([In] ref Credential userCredential, uint flags);

        [DllImport("Advapi32.dll", SetLastError = true)]
        public static extern void CredFree([In] IntPtr cred);
    }
}
"@
}

function ConvertFrom-SecureStringToPlainText {
    param(
        [Parameter(Mandatory = $true)]
        [Security.SecureString] $SecureString
    )

    $Bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureString)
    try {
        [Runtime.InteropServices.Marshal]::PtrToStringBSTR($Bstr)
    }
    finally {
        if ($Bstr -ne [IntPtr]::Zero) {
            [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($Bstr)
        }
    }
}

function Normalize-GmailAppPassword {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Password
    )

    return ($Password -replace "\s", "")
}

function Save-GmailAppPassword {
    param(
        [Parameter(Mandatory = $true)]
        [Security.SecureString] $SecurePassword,

        [string] $Target = $GmailCredentialTarget,
        [string] $UserName = $GmailCredentialUser
    )

    Initialize-GmailCredentialInterop

    $PlainPassword = Normalize-GmailAppPassword (ConvertFrom-SecureStringToPlainText $SecurePassword)
    if ([string]::IsNullOrWhiteSpace($PlainPassword)) {
        throw "App password cannot be empty."
    }

    $PasswordBytes = [Text.Encoding]::Unicode.GetBytes($PlainPassword)
    $Blob = [Runtime.InteropServices.Marshal]::AllocHGlobal($PasswordBytes.Length)

    try {
        [Runtime.InteropServices.Marshal]::Copy($PasswordBytes, 0, $Blob, $PasswordBytes.Length)

        $Credential = New-Object CredentialManagerInterop.Credential
        $Credential.Type = 1
        $Credential.TargetName = $Target
        $Credential.UserName = $UserName
        $Credential.CredentialBlobSize = $PasswordBytes.Length
        $Credential.CredentialBlob = $Blob
        $Credential.Persist = 2

        $Success = [CredentialManagerInterop.NativeMethods]::CredWrite([ref] $Credential, 0)
        if (-not $Success) {
            $ErrorCode = [Runtime.InteropServices.Marshal]::GetLastWin32Error()
            throw "Could not save Gmail app password. Windows error: $ErrorCode"
        }
    }
    finally {
        if ($Blob -ne [IntPtr]::Zero) {
            $ZeroBytes = New-Object byte[] $PasswordBytes.Length
            [Runtime.InteropServices.Marshal]::Copy($ZeroBytes, 0, $Blob, $ZeroBytes.Length)
            [Runtime.InteropServices.Marshal]::FreeHGlobal($Blob)
        }
    }
}

function Get-SavedGmailAppPassword {
    param(
        [string] $Target = $GmailCredentialTarget
    )

    Initialize-GmailCredentialInterop

    $CredentialPointer = [IntPtr]::Zero
    $Success = [CredentialManagerInterop.NativeMethods]::CredRead($Target, 1, 0, [ref] $CredentialPointer)
    if (-not $Success) {
        return $null
    }

    try {
        $Credential = [Runtime.InteropServices.Marshal]::PtrToStructure(
            $CredentialPointer,
            [type] [CredentialManagerInterop.Credential]
        )

        if ($Credential.CredentialBlobSize -eq 0) {
            return $null
        }

        $PasswordBytes = New-Object byte[] $Credential.CredentialBlobSize
        [Runtime.InteropServices.Marshal]::Copy($Credential.CredentialBlob, $PasswordBytes, 0, $PasswordBytes.Length)

        return Normalize-GmailAppPassword ([Text.Encoding]::Unicode.GetString($PasswordBytes).TrimEnd([char] 0))
    }
    finally {
        if ($CredentialPointer -ne [IntPtr]::Zero) {
            [CredentialManagerInterop.NativeMethods]::CredFree($CredentialPointer)
        }
    }
}

function Read-GmailAppPassword {
    $SavedPassword = Get-SavedGmailAppPassword
    if (-not [string]::IsNullOrWhiteSpace($SavedPassword)) {
        Write-Host "Using saved Gmail app password from Windows Credential Manager."
        return $SavedPassword
    }

    $SecurePassword = Read-Host "Enter Gmail app password for $GmailCredentialUser" -AsSecureString
    return Normalize-GmailAppPassword (ConvertFrom-SecureStringToPlainText $SecurePassword)
}
