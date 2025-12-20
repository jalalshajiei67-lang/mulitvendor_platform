# 🔧 Fixing Line Ending Issues (Windows → Linux)

## What Happened?

The error `/bin/bash^M: bad interpreter` means:
- Your script was created/edited on **Windows** (uses `\r\n` line endings)
- Linux expects **Unix line endings** (`\n` only)
- The `^M` is the invisible Windows carriage return character

## Quick Fix (On Server)

Run these commands on your server:

```bash
# Fix line endings in the script
sed -i 's/\r$//' diagnose-db-connection.sh
sed -i 's/\r$//' restore-production-db.sh

# Make them executable
chmod +x diagnose-db-connection.sh restore-production-db.sh

# Now run it
./diagnose-db-connection.sh
```

## Understanding the Fix

- `sed -i 's/\r$//' filename` removes all `\r` (carriage return) characters from the end of lines
- This converts Windows line endings (CRLF) to Unix line endings (LF)

## Prevention for Future

### Option 1: Configure Git (Recommended)

Add this to your `.gitattributes` file:

```
*.sh text eol=lf
*.py text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
```

This tells Git to always use Unix line endings for these files.

### Option 2: Use VS Code Settings

Add to your VS Code settings (`.vscode/settings.json`):

```json
{
  "files.eol": "\n",
  "files.insertFinalNewline": true
}
```

### Option 3: Use dos2unix (if installed)

```bash
dos2unix diagnose-db-connection.sh restore-production-db.sh
```


