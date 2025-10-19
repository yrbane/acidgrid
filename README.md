# ⚡ ACIDGRID - Underground Techno Generator

**Enter the grid. Unleash the acid.**

ACIDGRID is an audacious Python CLI tool that generates unique, hard-hitting MIDI acid techno tracks with zero human intervention. Every track is a one-of-a-kind sonic assault forged in the underground grid with its own personality, structure, and raw energy.

## 🎛️ Features

### 🎵 5-Track Architecture
Every generated track contains:
- **Rhythm Track**: Bass drum, snare, claps, 3 toms, hi-hats - with dynamic patterns, breaks, and fills
- **Bassline**: 10+ different riff styles from acid 303 to warehouse stomp
- **Sub-Bass**: Deep, earth-shaking fundamental frequencies
- **Synth Accompaniment**: Chords, arpeggios, stabs, and filtered sweeps
- **Synth Lead**: Melodic lines, sequences, and hypnotic patterns

### 🌀 Dynamic Song Structure
Intelligent track progression with:
- **Intro** → **Build-up** → **Drop** → **Breakdown** → **Build-up 2** → **Drop 2** → **Outro**
- Progressive intensity curves from 0.2 to 1.0
- Automatic breaks every 4, 8, 16, 32, 64 measures
- Velocity automation and volume dynamics
- Harmonic coherence between all instruments

### 🎲 Infinite Variation
- **Never the same track twice** - microsecond-precision unique seeds
- **10 bassline riffs**: Acid 303, Detroit Funk, Berlin Minimal, UK Rave, Chicago Jack, and more
- **5 rhythm patterns**: Minimal, Driving, Complex, Breakbeat, Rolling
- **Multiple melody algorithms**: Staccato, flowing, sustained, rapid sequences
- **Question-answer patterns** between instruments
- **Automatic fills and transitions**

### 💀 Audacious Track Names
Every track gets a bold, memorable name:
- `Black Hole Sun`
- `Fuck the System`
- `Warehouse Massacre 50`
- `!!! Complete Annihilation !!!`
- `Signal from Sagittarius A`
- `⚠ Underground Riot ⚠`
- `Error 666: Fatal`

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/acidgrid.git
cd acidgrid

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

## 💣 Usage

### Quick Start
```bash
# Generate with defaults (192 measures, 128 BPM)
acidgrid

# Custom parameters
acidgrid --measures 64 --tempo 140

# Specific output directory (default is ./output/)
acidgrid --output ~/Music/ACIDGRID --measures 128 --tempo 135
```

### Parameters
- `--measures`: Track length in measures (default: 192)
- `--tempo`: BPM between 120-150 (default: 128)
- `--output`: Output directory for MIDI files (default: ./output/)
- `--seed`: Force specific seed for reproducible generation (optional)
- `--play`: Play a preview of the generated track (requires MIDI synthesizer)
- `--preview-duration`: Preview length in seconds (default: 600)
- `--check-synth`: Check MIDI synthesizer availability and show setup instructions

### Examples
```bash
# Quick 32-bar loop for testing
acidgrid --measures 32 --tempo 145

# Full club destroyer
acidgrid --measures 256 --tempo 135

# Generate with instant preview
acidgrid --measures 64 --tempo 140 --play

# Short 10-second preview
acidgrid --measures 32 --tempo 135 --play --preview-duration 10

# Check if MIDI playback is available
acidgrid --check-synth

# Reproduce a specific track
acidgrid --seed 1756577066200374
```

## 🎚️ Technical Details

### Dependencies
- Python 3.7+
- mido (MIDI file handling)  
- python-rtmidi (MIDI backend)
- pygame (MIDI playback, optional)

### Architecture
```
acidgrid/
├── generators/          # Track generators
│   ├── rhythm.py       # Drum patterns with velocity curves
│   ├── bassline.py     # 10+ bassline riff algorithms
│   ├── sub_bass.py     # Sub-bass generator
│   ├── synth_accompaniment.py
│   └── synth_lead.py
├── song_structure.py    # Dynamic arrangement engine
├── track_naming.py      # Audacious name generator
├── midi_output.py       # MIDI file composition
├── midi_player.py       # MIDI playback system
└── main.py             # CLI entry point
```

**Output Directory:**
- All generated MIDI files are saved to `./output/` by default
- The directory is created automatically if it doesn't exist
- Files are ignored by git (see `.gitignore`)
- Custom output location: `acidgrid --output /path/to/your/folder`

### MIDI Mapping
- **Channel 10**: Drums (GM standard)
  - 36: Bass Drum
  - 38: Snare
  - 39: Clap
  - 41-45: Toms
  - 42: Hi-Hat
  - 46: Open Hi-Hat
  - 49: Crash
- **Channel 1**: Bassline (Synth Bass)
- **Channel 2**: Sub-Bass (Deep Bass)
- **Channel 3**: Synth Accompaniment (Square Lead)
- **Channel 4**: Synth Lead (Saw Lead)

## 🔊 Output & Preview

Generated MIDI files can be:
- Imported into any DAW (Ableton, FL Studio, Logic, etc.)
- Played with hardware synthesizers
- Rendered with software instruments
- Used as starting points for production
- **Previewed instantly** with `--play` flag

### 🎧 MIDI Playback Setup

For instant preview, install a MIDI synthesizer:

**Linux:**
```bash
sudo apt install fluidsynth fluid-soundfont-gm
# Run: fluidsynth -a alsa -m alsa_seq -l -i /usr/share/sounds/sf2/FluidR3_GM.sf2
```

**MacOS:**
```bash
brew install fluidsynth
# Download a soundfont and run: fluidsynth -a coreaudio -m coremidi soundfont.sf2
```

**Windows:**
- Download VirtualMIDISynth from https://coolsoft.altervista.org/en/virtualmidisynth
- Or use built-in Windows MIDI (works automatically)

## 🌟 What Makes Each Track Unique

1. **Microsecond seed generation** - truly random initialization
2. **10 different bassline personalities** with variations
3. **Dynamic velocity curves** that respond to song sections
4. **Intelligent pattern switching** to avoid repetition
5. **Harmonic awareness** - all instruments play in key
6. **Structural dynamics** - builds, drops, and breakdowns

## ⚡ Performance

- Generates a 192-measure track in ~1 second
- File sizes: 20-70KB depending on complexity
- Zero external API calls - fully offline
- No sample libraries required

## 🎭 Track Name Categories

The name generator creates titles in 10 categories:
- **Dystopian**: "Death of Paradise", "When Heaven Dies"
- **Psychedelic**: "DMT Dreams", "Ego Death 303"
- **Underground**: "Warehouse Riot", "3AM Bunker"
- **Futuristic**: "Year 2847", "Cyborg Uprising"
- **Raw Energy**: "Maximum Voltage", "7000 BPM"
- **Dark Poetry**: "Bleeding Stars", "Silent Scream"
- **Rebel**: "Fuck the System", "No Gods No Masters"
- **Cosmic Horror**: "Event Horizon", "Reality Break"
- **Machine Soul**: "Unit 9999 - Rogue", "Error 404: Fatal"
- **Pure Chaos**: "Complete Annihilation", "Beautiful Disaster"

## 🛠️ Development

```bash
# Run in development mode
python -m acidgrid.main --measures 16 --tempo 140

# Run tests (when available)
python -m pytest

# Check code style
python -m flake8 acidgrid/
```

## 📜 License

MIT License - Go wild, make noise, destroy dancefloors.

## 🤝 Contributing

Pull requests welcome. Make it harder, faster, more chaotic.

## ⚠️ Warning

Generated tracks may cause:
- Involuntary body movement
- Sudden urge to rave
- Temporary loss of reality
- Permanent bass addiction

---

**Built with chaos, for chaos.**

*Remember: Every track is unique. Every track is a weapon. Use responsibly.*

```bash
# Generate and preview a demonic track
acidgrid --measures 666 --tempo 150 --play --preview-duration 60

# Quick preview workflow
acidgrid --measures 32 --tempo 140 --play --preview-duration 15
```

## 🎵 Preview Features

The integrated MIDI player provides:
- **Instant playback** after generation
- **Progress bar** with time display  
- **Ctrl+C to stop** during playback
- **Automatic fallback** (pygame → MIDI ports)
- **Cross-platform** compatibility
- **No external dependencies** required (uses pygame)