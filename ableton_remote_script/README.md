# 🎹 ACIDGRID Remote Script for Ableton Live

**Native Ableton Live integration for ACIDGRID - Generate MIDI clips directly inside Live!**

## ✨ Features

- 🎨 **10 Music Styles** accessible via MIDI controller
- 🎵 **Direct Clip Generation** - Creates clips in selected track
- 🎛️ **Controller Mapping** - Works with Launchpad, Push, or any MIDI controller
- 🎨 **Color Coding** - Each style has its own clip color
- ⚡ **Instant Generation** - No file export needed
- 🔄 **Live Integration** - Respects project tempo and track selection

## 🚀 Installation

### Step 1: Install ACIDGRID Python Package

```bash
# In acidgrid directory
pip install -e .
```

### Step 2: Copy Remote Script to Ableton

**macOS:**
```bash
cp -r ableton_remote_script/ACIDGRID ~/Music/Ableton/User\ Library/Remote\ Scripts/
```

**Windows:**
```bash
xcopy /E /I ableton_remote_script\ACIDGRID "%USERPROFILE%\Documents\Ableton\User Library\Remote Scripts\ACIDGRID"
```

**Linux:**
```bash
cp -r ableton_remote_script/ACIDGRID ~/.local/share/Ableton/User\ Library/Remote\ Scripts/
```

### Step 3: Enable in Ableton Live

1. Open Ableton Live Preferences (Cmd/Ctrl + ,)
2. Go to **Link/Tempo/MIDI** tab
3. In **Control Surface** dropdown, select **ACIDGRID**
4. Set Input/Output to **None** (or your MIDI controller if using mapping)
5. Click **OK**

### Step 4: Restart Ableton Live

The script will load automatically on next startup.

## 🎮 Usage

### Method 1: MIDI Controller (Recommended)

**Setup:**
1. Connect your MIDI controller
2. In Ableton Preferences → Link/Tempo/MIDI:
   - Set ACIDGRID Input to your controller
3. Map controller pads to trigger styles

**MIDI Note Mapping:**
- **C4 (60)** → House
- **C#4 (61)** → Techno
- **D4 (62)** → Hard-Tekno
- **D#4 (63)** → Breakbeat
- **E4 (64)** → IDM
- **F4 (65)** → Jungle
- **F#4 (66)** → Hip-Hop
- **G4 (67)** → Trap
- **G#4 (68)** → Ambient
- **A4 (69)** → Drum & Bass

**Measure Length:**
- **C5 (72)** → 16 measures
- **C#5 (73)** → 32 measures
- **D5 (74)** → 64 measures
- **D#5 (75)** → 128 measures
- **E5 (76)** → 192 measures

**Workflow:**
1. Select a track in Ableton
2. Press a style pad on your controller (C4-A4)
3. ACIDGRID generates a clip in the first empty slot!

### Method 2: Python Console (Advanced)

Access the script via Ableton's Python console:

```python
# Get ACIDGRID instance
acidgrid = self.c_instance.song().view.selected_track

# Generate clip
from ACIDGRID import ACIDGRID
acidgrid.generate_clip("techno")

# Change measures
acidgrid.set_measures(64)
acidgrid.generate_clip("jungle")
```

## 🎨 Style Colors

Each style gets a unique color in Ableton:

| Style | Color | Ableton Index |
|-------|-------|---------------|
| house | 🟠 Orange | 9 |
| techno | 🟣 Purple | 5 |
| hard-tekno | 🔴 Red | 1 |
| breakbeat | 🟡 Yellow | 11 |
| idm | 🔵 Cyan | 16 |
| jungle | 🟢 Green | 18 |
| hip-hop | 🟤 Brown | 60 |
| trap | 🩷 Pink | 56 |
| ambient | 💙 Light Blue | 23 |
| drum&bass | 💚 Lime | 26 |

## 🎛️ Controller Layouts

### Launchpad Layout

```
[House  ][Techno ][Hard-T ][Break  ]
[IDM    ][Jungle ][Hip-Hop][Trap   ]
[Ambient][DnB    ][       ][       ]
[       ][       ][       ][       ]
[16 Bar ][32 Bar ][64 Bar ][128 Bar]
```

### Push Layout

Map the 8x8 pad grid:
- **Top Row**: 10 styles
- **Bottom Row**: Measure presets

## 🐛 Troubleshooting

### Script doesn't appear in Control Surface list

1. Check Remote Scripts folder path is correct
2. Ensure ACIDGRID folder contains all files:
   - `__init__.py`
   - `ACIDGRID.py`
   - `ClipCreator.py`
   - `config.py`
3. Restart Ableton Live
4. Check **Log.txt** for errors:
   - macOS: `~/Library/Preferences/Ableton/Live X.X/Log.txt`
   - Windows: `%APPDATA%\Ableton\Live X.X\Preferences\Log.txt`

### "Module not found" errors

Ensure ACIDGRID Python package is installed:
```bash
pip install -e /path/to/acidgrid
```

### Clips generate but are empty

1. Check Ableton's Log.txt for errors
2. Verify generators are working: `python -m acidgrid --style techno --measures 8`
3. Ensure track is not frozen/disabled

### MIDI mapping not working

1. Check MIDI controller is connected
2. Verify Input is set to your controller in Preferences
3. Monitor incoming MIDI notes (MIDI Monitor on macOS, MIDI-OX on Windows)
4. Check config.py MIDI_MAPPING matches your controller layout

## 📊 How It Works

```
MIDI Controller
    ↓
Ableton Live
    ↓
ACIDGRID Remote Script
    ↓
ACIDGRID Generators (rhythm, bassline, synth, etc.)
    ↓
MIDI Clip Creation
    ↓
Clip appears in Ableton Track
```

## 🔧 Technical Details

### File Structure

```
ACIDGRID/
├── __init__.py           # Entry point
├── ACIDGRID.py           # Main script class
├── ClipCreator.py        # Clip generation logic
└── config.py             # Styles & MIDI mapping
```

### Requirements

- Ableton Live 10.1+ (tested up to Live 12)
- Python 2.7 or 3.x (bundled with Ableton)
- ACIDGRID Python package installed

### Ableton API Usage

The script uses:
- `Live.Song` - Access project tempo, tracks
- `Live.Track` - Create clips in clip slots
- `Live.Clip` - Add MIDI notes programmatically
- `Live.MidiMap` - Map MIDI controllers

## 🎵 Workflow Examples

### Quick Sketch Session

1. Create 4 MIDI tracks
2. Select first track
3. Press **Techno** pad → Clip appears
4. Select second track
5. Press **House** pad → Clip appears
6. Jam!

### Build a Full Track

1. Generate 8 different style variations
2. Arrange clips in Session View
3. Record to Arrangement
4. Add effects, mix, master

### Live Performance

1. Pre-generate clips in multiple scenes
2. Map styles to controller pads
3. Trigger on-the-fly during performance
4. Ableton follows project tempo automatically

## 🚀 Pro Tips

1. **Batch Generation**: Select multiple tracks, generate clips sequentially
2. **Color Organization**: Use clip colors to identify styles quickly
3. **MIDI Routing**: Route generated clips to different instruments
4. **Resampling**: Record ACIDGRID output, process with effects
5. **Automation**: Use Ableton's automation on generated clips

## 📝 Changelog

### v1.0.0 (2025)
- Initial release
- 10 music styles
- MIDI controller mapping
- Direct clip generation
- Color-coded clips

## 🤝 Contributing

Submit issues or PRs to improve the Remote Script!

## 📜 License

MIT License - Same as ACIDGRID main project

---

**Enjoy generating infinite music directly in Ableton Live!** 🎉
