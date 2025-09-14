$ErrorActionPreference = 'SilentlyContinue'
Unregister-ScheduledTask -TaskName 'BibleWallpaper' -Confirm:$false | Out-Null
Write-Host "Scheduled task 'BibleWallpaper' removed (if it existed)." -ForegroundColor Yellow
