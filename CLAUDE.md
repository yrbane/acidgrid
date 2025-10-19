# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ACIDGRID is a Python CLI tool that generates MIDI acid techno tracks. Each generated track consists of 5 tracks:

1. **Rhythm track**: Bass drum (BD), Snare drum (SD), Hi-hat (HH), Open hi-hat (OH), toms, crash, ride
2. **Bassline track**: Bass synthesizer line with 10 different riff styles (Acid 303, Detroit Funk, etc.)
3. **Sub-bass track**: Deep fundamental frequencies (C0-B0)
4. **Synth accompaniment track**: Supporting synthesizer elements (chords, arpeggios, stabs)
5. **Synth lead track**: Lead synthesizer melodies

## CLI Parameters

- `--style` (default: techno): Music style to generate
  - Available styles: **house**, **techno**, **hard-tekno**, **breakbeat**, **idm**, **jungle**, **hip-hop**, **trap**, **ambient**, **drum&bass**
  - Each style has its own tempo range, rhythm patterns, bassline riffs, and song structure
- `--measures` (default: 192): Number of measures in the generated track
- `--tempo` (optional): BPM (beats per minute). If not specified, uses the default tempo for the selected style
  - house: 120-128 BPM (default: 124)
  - techno: 128-135 BPM (default: 128)
  - hard-tekno: 150-170 BPM (default: 160)
  - breakbeat: 130-150 BPM (default: 138)
  - idm: 140-180 BPM (default: 160)
  - jungle: 160-180 BPM (default: 170)
  - hip-hop: 85-95 BPM (default: 90)
  - trap: 140-160 BPM (default: 150)
  - ambient: 60-90 BPM (default: 75)
  - drum&bass: 170-180 BPM (default: 174)
- `--seed` (optional): Random seed for reproducible generation
- `--output` (optional): Output directory for MIDI files (default: ./output/)
- `--play`: Play a preview of the generated track (requires MIDI synthesizer)
- `--preview-duration` (default: 600): Preview duration in seconds
- `--check-synth`: Check if MIDI synthesizer is available
- Each generated track receives an original/creative name

## Development Commands

Since this is a Python project, common development commands will likely include:

```bash
# Run the CLI tool
python -m acidgrid [options]
# or after installation:
acidgrid [options]

# Install dependencies
pip install -r requirements.txt
# or install in editable mode:
pip install -e .

# Run tests (when test framework is set up)
python -m pytest
# or
python -m unittest discover
```

## Project Structure

The project has the following structure:

```
acidgrid/
├── generators/          # Track generators
│   ├── rhythm.py       # 5 drum patterns (style-aware)
│   ├── bassline.py     # 10 bassline riff styles (style-aware)
│   ├── sub_bass.py     # Deep bass generator (style-aware)
│   ├── synth_accompaniment.py  # 4 chord patterns (style-aware)
│   └── synth_lead.py   # 4 melody styles (style-aware)
├── music_styles.py      # Music style configurations (10 styles)
├── song_structure.py    # Dynamic song arrangement engine (style-aware)
├── track_naming.py      # Creative name generator (10 categories)
├── midi_output.py       # MIDI file composition
├── midi_player.py       # MIDI playback system
└── main.py             # CLI entry point
```

**Output:** All generated MIDI files are saved to `./output/` by default.

## Architecture Notes

The project is designed around:
- **Music Style System**: 10 distinct music styles (house, techno, hard-tekno, breakbeat, idm, jungle, hip-hop, trap, ambient, drum&bass)
  - Each style has unique characteristics: tempo range, rhythm patterns, bassline riffs, song structure, intensity curves
  - Style-aware generators adapt their behavior based on the selected style
  - Defined in `acidgrid/music_styles.py`
- **Modular track generators** for each of the 5 track types:
  - Each generator accepts a `style` parameter to adapt its output
  - Rhythm generator: chooses patterns based on style preferences
  - Bassline generator: selects riffs appropriate for the style
  - Synth generators: adjust density and activity based on style
- **Dynamic song structure** with sections (intro, buildup, drop, breakdown, outro, etc.)
  - Structure templates vary by style (e.g., ambient has slow evolution, trap is drop-focused)
  - Hip-hop uses verse/hook structure, breakbeat/jungle use high-energy with breaks
- **Configurable parameters**:
  - Style (10 options), measures (default: 192), tempo (style-dependent defaults)
  - Random seed for reproducibility
- **MIDI library integration** (mido, python-rtmidi)
- **Creative naming system** with 10 categories and special formatting
- **Harmonic coherence**: all tracks respect key, scale, and chord progressions
- **Intensity curves**: 0.2-1.0 based on song sections and style
- **Microsecond-precision random seeding** for uniqueness