param(
    [int]$IntervalSeconds = 300
)

$ErrorActionPreference = 'Stop'

# Resolve paths
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ProjectRoot
$Python = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $Python)) {
    Write-Host "Python venv not found at $Python. Falling back to system 'python'." -ForegroundColor Yellow
    $Python = 'python'
}
$ScriptPath = Join-Path $ProjectRoot 'src\main.py'

$Action = New-ScheduledTaskAction -Execute $Python -Argument "`"$ScriptPath`" --interval $IntervalSeconds"
$Trigger1 = New-ScheduledTaskTrigger -AtLogOn
$Trigger2 = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Seconds $IntervalSeconds) -RepetitionDuration ([TimeSpan]::MaxValue)

$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Highest

$Task = New-ScheduledTask -Action $Action -Trigger @($Trigger1, $Trigger2) -Principal $Principal -Settings (New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries)

Register-ScheduledTask -TaskName 'BibleWallpaper' -InputObject $Task -Force | Out-Null
Write-Host "Scheduled task 'BibleWallpaper' installed." -ForegroundColor Green
