# Bible Wallpaper (Windows)

A small Python app that renders Bible verses onto images and sets them as your Windows desktop wallpaper. It can rotate verses every N minutes (2–5 min recommended). Optional guidance is provided for Windows lock screen background.

## Features
- Random or sequential Bible verse display
- Auto-fit text with wrapping and contrast outline
- Uses your screen resolution for crisp results
- Interval timer to update every N minutes
- Starts on logon via Task Scheduler (optional)

## Quick Start (Windows PowerShell)

1) Create a virtual environment and install dependencies:

```powershell
python -m venv .venv ; .\.venv\Scripts\Activate.ps1 ; pip install -r requirements.txt
```

2) Run once to generate and set a wallpaper:

```powershell
python src\main.py --once
```

3) Run with auto-rotate every 5 minutes:

```powershell
python src\main.py --interval 300
```

Tip: Use `--interval 120` for 2 minutes.

### Schedule on Logon (optional)
Use the helper script to create a scheduled task that runs on logon and repeats every 5 minutes:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\Install-ScheduledTask.ps1 -IntervalSeconds 300
```

Remove the task:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\Uninstall-ScheduledTask.ps1
```

## Lock Screen (optional, Windows Pro/Enterprise)
Windows Home does not allow programmatic lock screen changes reliably. On Pro/Enterprise, you can use Group Policy or registry-based policies. See `scripts/LockScreen-Notes.md` for steps and caveats.

## Configuration
- Edit `data/verses.json` to add your own verses.
- Fonts: By default uses `Segoe UI` which is present on Windows. You can put a .ttf in the `data/fonts` folder and pass `--font data/fonts/YourFont.ttf`.

## Troubleshooting
- If wallpaper doesn’t update immediately, try right-click desktop > Refresh, or wait 1–2 seconds; Windows caches wallpapers.
- Some corporate-managed devices block wallpaper changes via policy.
- If PowerShell execution policy blocks scripts, pass `-ExecutionPolicy Bypass` as above.

## License
Personal use only for scripture display. Verses in `data/verses.json` are user-editable.
