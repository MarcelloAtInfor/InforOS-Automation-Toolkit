[CmdletBinding()]
param(
    [string]$WindowTitleContains = 'Infor RPA Studio',
    [int]$SettleDelayMs = 750,
    [int]$ActivationRetries = 3,
    [switch]$PassThru
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;

public static class CodexWindowInterop {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);

    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
}
"@

function Get-ForegroundWindowTitle {
    $handle = [CodexWindowInterop]::GetForegroundWindow()
    if ($handle -eq [IntPtr]::Zero) {
        return ''
    }

    $builder = New-Object System.Text.StringBuilder 1024
    [void][CodexWindowInterop]::GetWindowText($handle, $builder, $builder.Capacity)
    return $builder.ToString()
}

$target = Get-Process |
    Where-Object {
        $_.MainWindowHandle -ne 0 -and
        $_.MainWindowTitle -like "*$WindowTitleContains*"
    } |
    Sort-Object StartTime -Descending |
    Select-Object -First 1

if (-not $target) {
    throw "No open window matched title fragment '$WindowTitleContains'."
}

$wshell = New-Object -ComObject WScript.Shell
$activated = $false
$foregroundTitle = Get-ForegroundWindowTitle

for ($attempt = 1; $attempt -le $ActivationRetries; $attempt++) {
    [void][CodexWindowInterop]::ShowWindowAsync([IntPtr]$target.MainWindowHandle, 9)
    $null = $wshell.AppActivate($target.Id)
    Start-Sleep -Milliseconds $SettleDelayMs

    $foregroundTitle = Get-ForegroundWindowTitle
    if ($foregroundTitle -eq $target.MainWindowTitle) {
        $activated = $true
        break
    }
}

if (-not $activated) {
    throw "Failed to focus Studio window '$($target.MainWindowTitle)'. Foreground window was '$foregroundTitle'."
}

[System.Windows.Forms.SendKeys]::SendWait('^({F5})')
Start-Sleep -Milliseconds 250
$sentVia = 'System.Windows.Forms.SendKeys'

if ($PassThru) {
    [pscustomobject]@{
        ProcessName = $target.ProcessName
        Id = $target.Id
        MainWindowTitle = $target.MainWindowTitle
        ForegroundWindowTitle = $foregroundTitle
        SentKeys = 'Ctrl+F5'
        SentVia = $sentVia
        ActivationRetries = $ActivationRetries
        Timestamp = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
    }
}
