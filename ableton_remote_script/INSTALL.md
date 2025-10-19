# 📦 Quick Installation Guide - ACIDGRID for Ableton Live

## Prerequisites

✅ Ableton Live 10.1 or newer
✅ ACIDGRID Python package installed
✅ Python with pip

## Installation Steps

### 1. Install ACIDGRID Package

```bash
cd /path/to/acidgrid
pip install -e .
```

Verify installation:
```bash
acidgrid --help
```

### 2. Locate Remote Scripts Folder

**macOS:**
```
~/Music/Ableton/User Library/Remote Scripts/
```

**Windows:**
```
%USERPROFILE%\Documents\Ableton\User Library\Remote Scripts\
```

**Linux:**
```
~/.local/share/Ableton/User Library/Remote Scripts/
```

If folder doesn't exist, create it:
```bash
mkdir -p "~/Music/Ableton/User Library/Remote Scripts/"  # macOS/Linux
```

### 3. Copy ACIDGRID Remote Script

**macOS/Linux:**
```bash
cd /path/to/acidgrid
cp -r ableton_remote_script/ACIDGRID ~/Music/Ableton/User\ Library/Remote\ Scripts/
```

**Windows (PowerShell):**
```powershell
cd C:\path\to\acidgrid
xcopy /E /I ableton_remote_script\ACIDGRID "$env:USERPROFILE\Documents\Ableton\User Library\Remote Scripts\ACIDGRID"
```

### 4. Verify Files

Check that these files exist:
```
Remote Scripts/
└── ACIDGRID/
    ├── __init__.py
    ├── ACIDGRID.py
    ├── ClipCreator.py
    └── config.py
```

### 5. Enable in Ableton Live

1. **Open Ableton Live**
2. **Preferences** (Cmd+, or Ctrl+,)
3. **Link/Tempo/MIDI** tab
4. **Control Surface** dropdown → Select **ACIDGRID**
5. **Input/Output** → Set to **None** (or your MIDI controller)
6. **Click OK**

### 6. Restart Ableton Live

Close and reopen Ableton for the script to load.

### 7. Test Installation

1. Open Ableton Live
2. Create a MIDI track
3. Check **Log.txt** for confirmation:
   ```
   [ACIDGRID] ACIDGRID Remote Script loaded!
   [ACIDGRID] Available styles: house, techno, hard-tekno, breakbeat, idm, jungle, hip-hop, trap, ambient, drum&bass
   ```

**Log.txt Location:**
- macOS: `~/Library/Preferences/Ableton/Live X.X/Log.txt`
- Windows: `%APPDATA%\Ableton\Live X.X\Preferences\Log.txt`
- Linux: `~/.config/ableton/live/Log.txt`

## ✅ Verification

Open Log.txt and look for:
```
[ACIDGRID] ACIDGRID Remote Script loaded!
```

If you see this, **installation successful!** 🎉

## 🎮 Quick Test

### Using MIDI Controller

1. Connect MIDI controller
2. In Preferences → Link/Tempo/MIDI:
   - Set **ACIDGRID Input** to your controller
3. Create a MIDI track
4. Press **C4** (60) on your controller
5. A **House** clip should appear!

### Using Python Console (Advanced)

In Ableton's Python console:
```python
# This will be available in future versions
# For now, use MIDI controller method
```

## 🐛 Troubleshooting

### "ACIDGRID doesn't appear in Control Surface list"

**Solution:**
- Verify folder structure is correct
- Check all 4 files are present
- Restart Ableton completely

### "Module 'acidgrid' not found"

**Solution:**
```bash
pip install -e /path/to/acidgrid
python -c "import acidgrid; print('OK')"
```

### "Script loads but clips are empty"

**Solution:**
- Check Log.txt for errors
- Verify ACIDGRID CLI works: `acidgrid --style techno --measures 8`
- Ensure track is not frozen

### Still having issues?

1. Check Log.txt for detailed error messages
2. Verify Python path in Ableton
3. Try reinstalling ACIDGRID package
4. Open an issue on GitHub with Log.txt contents

## 📁 File Paths Reference

| OS | Remote Scripts Folder |
|----|----------------------|
| macOS | `~/Music/Ableton/User Library/Remote Scripts/` |
| Windows | `%USERPROFILE%\Documents\Ableton\User Library\Remote Scripts\` |
| Linux | `~/.local/share/Ableton/User Library/Remote Scripts/` |

## 🎵 Next Steps

Once installed, check out:
- **README.md** for usage guide
- **Controller mapping** for your device
- **Workflow examples** for inspiration

---

**Happy generating!** 🚀
