# Lock Screen Background (Windows Pro/Enterprise)

Windows Home restricts programmatic lock screen customization. On Pro/Enterprise you can use policy to point the lock screen to a single image that we update.

## Approach
1. Choose a path to a BMP/JPG that our app will refresh, e.g. `C:\\Users\\%USERNAME%\\Pictures\\LockScreen\\lock.bmp`.
2. Configure policy to use that image for the lock screen.

### Local Group Policy Editor
- Run `gpedit.msc`.
- User Configuration > Administrative Templates > Control Panel > Personalization
- Enable: "Force a specific default lock screen image"
- Set the path to the image (use a local absolute path)

### Registry (Advanced)
- Set the following values under `HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Personalization` (create the key if missing):
  - `LockScreenImage` (REG_SZ) = full path to image
  - `NoLockScreen` (REG_DWORD) = 0

Notes:
- The image must be accessible to SYSTEM at lock time; user profile paths usually work, but a shared location may be more robust.
- Windows caches lock screen images; changes may not appear instantly.
- This area is sensitive to corporate policies; proceed only on personal devices.
