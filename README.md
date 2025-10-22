# ⚡ ACIDGRID - Multi-Style Electronic Music Generator

**Enter the grid. Generate any style. Unleash the sound.**

ACIDGRID is a powerful Python CLI tool that generates unique, professional-quality MIDI tracks across **10 different electronic music styles**. Every track is a one-of-a-kind creation with its own personality, structure, and authentic sonic character - from soulful house to aggressive hard-tekno.

## 🎛️ Features

### 🎨 10 Music Styles
Generate authentic tracks in any electronic music style:

| Style | BPM | Character | Signature Elements |
|-------|-----|-----------|-------------------|
| **house** | 120-128 | Soulful, groovy, four-on-the-floor | Latin percussion, congas, bongos |
| **techno** | 128-135 | Hypnotic, industrial, relentless | Minimal percussion, cowbell |
| **hard-tekno** | 150-170 | Fast, aggressive, distorted | Maximum percussion density |
| **breakbeat** | 130-150 | Syncopated, funky, energetic | Complex breaks, funky percussion |
| **idm** | 140-180 | Intelligent, glitchy, experimental | Randomized percussion, complex |
| **jungle** | 160-180 | Fast breaks, heavy bass, ragga | Massive percussion, congas, agogos |
| **hip-hop** | 85-95 | Laid back, boom bap, groovy | Minimal percussion, boom bap drums |
| **trap** | 140-160 | 808 bass, hi-hat rolls, modern | Hi-hat rolls, sparse cowbell |
| **ambient** | 60-90 | Atmospheric, sparse, meditative | Triangle, chimes, minimal |
| **drum&bass** | 170-180 | Fast breaks, deep bass, high energy | Dense percussion, rolling breaks |

### 🎵 5-Track Architecture
Every generated track contains:
- **Rhythm Track**: 20+ percussion instruments including BD, snare, claps, toms, hi-hats, shakers, congas, bongos, cowbell, tambourine, and style-specific percussion layers
- **Bassline**: 10+ different riff styles (Acid 303, Detroit Funk, Berlin Minimal, UK Rave, Chicago Jack, Rolling Thunder, Warehouse Stomp, Hypnotic Loop, Sub Pressure, Techno Gallop)
- **Sub-Bass**: Deep, earth-shaking fundamental frequencies (C0-B0)
- **Synth Accompaniment**: Chords, arpeggios, stabs, and filtered sweeps
- **Synth Lead**: Melodic lines, sequences, and hypnotic patterns

### 🥁 Professional Percussion System
Massive 20+ instrument percussion with style-specific layering:
- **Core drums**: Multiple kicks, snares (acoustic + electric), claps, side stick
- **Hi-hats**: Closed, open, pedal hi-hat
- **Cymbals**: Crash 1 & 2, splash, ride, ride bell, china
- **Latin**: Congas (high/low), bongos (high/low), timbales, agogos, claves
- **Shakers**: Maracas, shaker, tambourine, cabasa
- **Effects**: Cowbell, vibraslap, wood blocks, triangle
- **Toms**: 6 tom variations for fills and transitions

Each style gets authentic percussion:
- **House**: Latin grooves (congas, bongos, claves)
- **Hard-tekno**: Maximum density (cowbell + wood blocks + claves)
- **Jungle**: Ragga vibes (congas, agogos)
- **Trap**: Hi-hat rolls on beat 4

### 🌀 Dynamic Song Structure
Intelligent track progression with style-specific arrangements:
- **House/Techno**: Classic intro → buildup → drop → breakdown → buildup → drop → outro
- **Trap**: Drop-focused with intense buildups
- **Hip-hop**: Verse/hook structure
- **Ambient**: Slow evolution with minimal intensity changes
- **Breakbeat/Jungle/DnB**: High-energy with atmospheric breaks
- **Hard-tekno**: Relentless high-intensity progression

Features:
- Progressive intensity curves from 0.2 to 1.0
- Automatic breaks and fills
- Velocity automation and volume dynamics
- Harmonic coherence between all instruments

### 🎲 Infinite Variation
- **Never the same track twice** - microsecond-precision unique seeds
- **10 bassline riffs** with style-aware selection
- **5+ rhythm patterns** per style with style-specific percussion layers
- **Multiple melody algorithms**: Staccato, flowing, sustained, rapid sequences
- **Question-answer patterns** between instruments
- **Automatic fills and transitions**

### 💀 Style-Aware Track Names
Every track gets an authentic name matching its style:
- **House**: "Night of Groove", "Can You Feel It", "Disco 88"
- **Techno**: "Unit 1808 - Rogue", "Android Apocalypse", "Dead Civilization"
- **Hard-tekno**: "!!! DESTROY EVERYTHING !!!", "165 BPM ANNIHILATE"
- **Jungle**: "Champion Sound Massive", "Deadly Shooter"
- **Hip-hop**: "Brooklyn State of Mind (Instrumental)", "Boom Bap Chronicles"
- **Trap**: "💎 No Cap", "🔥 Wave Mode 🔥"
- **Ambient**: "Dissolving Reflections", "Ocean at Dusk"
- **IDM**: "draft_20_c", "buffer.overflow", "untitled_042"

### 🎛️ Interactive Mode & Audio Export
- **🎨 Interactive TUI**: Beautiful terminal interface with rich styling for easy parameter selection
- **🔊 Audio Export**: Render MIDI to audio files (WAV, MP3, OGG, FLAC) using FluidSynth
- **🎹 Custom SoundFonts**: Use any .sf2 SoundFont for personalized sounds
- **⚡ High-Quality Rendering**: Up to 96kHz sample rate, configurable gain
- **🎧 Instant Preview**: Play tracks directly in terminal with MIDI synthesizer

## 🚀 Installation

### Standard Installation

```bash
# Clone the repository
git clone https://github.com/yrbane/acidgrid.git
cd acidgrid

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### 🔊 Audio Export Setup (Optional)

To export tracks to audio files (WAV/MP3/OGG/FLAC), install FluidSynth:

**Linux (Debian/Ubuntu):**
```bash
sudo apt install fluidsynth fluid-soundfont-gm ffmpeg
```

**Linux (Arch):**
```bash
sudo pacman -S fluidsynth soundfont-fluid ffmpeg
```

**macOS:**
```bash
brew install fluidsynth ffmpeg
```

**Windows:**
1. Download FluidSynth from [GitHub releases](https://github.com/FluidSynth/fluidsynth/releases)
2. Download ffmpeg from [ffmpeg.org](https://ffmpeg.org/)
3. Add both to your PATH
4. Download a SoundFont (.sf2) file

**Check installation:**
```bash
acidgrid --check-audio
```

### 🎹 Ableton Live Integration (Optional)

**Generate MIDI clips directly inside Ableton Live!**

ACIDGRID includes a native Remote Script for seamless Ableton integration:

```bash
# Install Remote Script
cd ableton_remote_script
./install.sh  # macOS/Linux

# Or manually copy
cp -r ACIDGRID ~/Music/Ableton/User\ Library/Remote\ Scripts/
```

Then in Ableton:
1. Preferences → Link/Tempo/MIDI
2. Control Surface → **ACIDGRID**
3. Restart Ableton

**Features:**
- 🎵 Generate clips directly in Ableton tracks
- 🎛️ MIDI controller mapping (Launchpad/Push compatible)
- 🎨 Color-coded clips by style
- ⚡ Instant generation, no file export needed

See **[ableton_remote_script/README.md](ableton_remote_script/README.md)** for full integration guide.

## 💣 Usage

### Quick Start
```bash
# Generate house track (default: 192 measures)
acidgrid --style house

# Generate 64-measure trap banger
acidgrid --style trap --measures 64

# Generate ambient meditation (custom tempo)
acidgrid --style ambient --measures 96 --tempo 70

# Generate drum&bass roller at 174 BPM
acidgrid --style drum&bass --measures 128
```

### Parameters

#### Generation
- `--style`: Music style (choices: house, techno, hard-tekno, breakbeat, idm, jungle, hip-hop, trap, ambient, drum&bass) - **default: techno**
- `--measures`: Track length in measures - **default: 192**
- `--tempo`: BPM (if not specified, uses style default)
- `--swing`: Swing/groove amount 0.0-1.0 (0.0=straight, 0.5=triplet, 1.0=max swing)
- `--seed`: Force specific seed for reproducible generation (optional)
- `--output`: Output directory for MIDI files - **default: ./output/**

#### Interactive Mode
- `--interactive`, `-i`: Launch interactive mode with menu to choose all parameters

#### Audio Export (requires FluidSynth)
- `--export-audio`: Export track to audio file (WAV/MP3/OGG/FLAC)
- `--audio-format`: Audio format (choices: wav, mp3, ogg, flac) - **default: wav**
- `--soundfont`: Path to custom SoundFont (.sf2) file
- `--sample-rate`: Sample rate in Hz (choices: 22050, 44100, 48000, 96000) - **default: 44100**
- `--gain`: Master gain for audio export, 0.0-10.0 - **default: 0.5**
- `--check-audio`: Check audio export availability (FluidSynth, SoundFont, ffmpeg)

#### Preview
- `--play`: Play a preview of the generated track (requires MIDI synthesizer)
- `--preview-duration`: Preview length in seconds - **default: 600**
- `--check-synth`: Check MIDI synthesizer availability and show setup instructions

### Examples

#### Basic Generation
```bash
# Quick 32-bar house loop
acidgrid --style house --measures 32

# Full 256-measure hard-tekno destroyer at 165 BPM
acidgrid --style hard-tekno --measures 256 --tempo 165

# Hip-hop beat at 90 BPM with instant preview
acidgrid --style hip-hop --measures 64 --tempo 90 --play

# Ambient soundscape (slow tempo)
acidgrid --style ambient --measures 128 --tempo 65

# Jungle track with 10-second preview
acidgrid --style jungle --measures 64 --play --preview-duration 10

# Reproduce a specific track
acidgrid --style techno --seed 1756577066200374

# Generate trap with custom output location
acidgrid --style trap --measures 64 --output ~/Music/ACIDGRID
```

#### Interactive Mode
```bash
# Launch beautiful interactive menu
acidgrid --interactive

# Or use shorthand
acidgrid -i
```

#### Audio Export
```bash
# Check if audio export is available
acidgrid --check-audio

# Export techno track to WAV
acidgrid --style techno --measures 64 --export-audio

# Export house track to MP3 (320kbps)
acidgrid --style house --export-audio --audio-format mp3

# Export to high-quality FLAC
acidgrid --style ambient --export-audio --audio-format flac --sample-rate 48000

# Export with custom SoundFont
acidgrid --style drum&bass --export-audio --soundfont ~/soundfonts/MyCustom.sf2

# Export with higher gain for louder output
acidgrid --style hard-tekno --export-audio --gain 0.8

# Generate, export to MP3, and preview
acidgrid --style trap --measures 32 --export-audio --audio-format mp3 --play
```

### Style Tempo Ranges

Each style has an authentic tempo range:
- **house**: 120-128 BPM (default: 124)
- **techno**: 128-135 BPM (default: 128)
- **hard-tekno**: 150-170 BPM (default: 160)
- **breakbeat**: 130-150 BPM (default: 138)
- **idm**: 140-180 BPM (default: 160)
- **jungle**: 160-180 BPM (default: 170)
- **hip-hop**: 85-95 BPM (default: 90)
- **trap**: 140-160 BPM (default: 150)
- **ambient**: 60-90 BPM (default: 75)
- **drum&bass**: 170-180 BPM (default: 174)

The system validates custom tempos and warns if outside the style's authentic range.

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
│   ├── rhythm.py       # 20+ percussion instruments with style-specific layers
│   ├── bassline.py     # 10 bassline riffs with style selection
│   ├── sub_bass.py     # Sub-bass generator
│   ├── synth_accompaniment.py  # Style-aware density
│   └── synth_lead.py   # Melodic generation
├── music_styles.py      # Style configurations (10 styles)
├── song_structure.py    # Dynamic arrangement engine (style-aware)
├── track_naming.py      # Style-aware name generator (30+ functions)
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
  - 35-36: Bass Drums
  - 37-40: Snares, Clap, Side Stick
  - 41-50: Toms
  - 42-46: Hi-Hats (closed, pedal, open)
  - 49-57: Cymbals (crash, ride, splash, bell, china)
  - 54-70: Latin percussion (cowbell, tambourine, congas, bongos, timbales, agogos, maracas, claves)
  - 71-82: Effects (whistles, wood blocks, triangle, shaker)
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

1. **10 distinct music styles** with authentic characteristics
2. **Style-specific percussion** - 20+ instruments with intelligent layering
3. **Microsecond seed generation** - truly random initialization
4. **Style-aware bassline selection** from 10 different personalities
5. **Dynamic velocity curves** that respond to song sections and style
6. **Intelligent pattern switching** to avoid repetition
7. **Harmonic awareness** - all instruments play in key
8. **Structural dynamics** - builds, drops, and breakdowns adapted to style
9. **Authentic track naming** - 30+ naming functions across 10 styles

## ⚡ Performance

- Generates a 192-measure track in ~1 second
- File sizes: 20-100KB depending on complexity and percussion density
- Zero external API calls - fully offline
- No sample libraries required

## 🎭 Track Name Generation

The name generator creates authentic titles for each style:

### House Names
- Soulful: "Love & Music", "Can You Feel It"
- Groovy: "Keep On Groovin", "Funky All Night"
- Classic: "Music Is the Answer (ACIDGRID Mix)"
- Disco: "Disco 88", "Studio 54"

### Techno Names
- Dystopian: "Death of Paradise", "When Heaven Dies"
- Underground: "Warehouse Riot", "3AM Powerplant"
- Futuristic: "Year 2847", "Protocol 141: Apocalypse"
- Machine: "Unit 9999 - Rogue", "Error 404: Fatal"

### Hard-Tekno Names
- Aggressive: "DESTROY EVERYTHING", "165 BPM ANNIHILATE"
- Distorted: "!!!XXXNOISEXXX!!!", "[KICK] x7"

### Jungle Names
- Ragga: "Champion Sound Massive", "Bun Dem Thunder"
- Classic: "Atlantis", "Super Sharp Shooter (Jungle VIP)"

### Hip-Hop Names
- Boom Bap: "Raw Beats", "Rough & Rugged"
- Street: "Brooklyn State of Mind", "Southside Dreams"
- Classic: "93 Til Infinity", "SP-1200 Sessions"

### Trap Names
- Modern: "💎 Too Wave", "Big Flex", "No Cap"
- Street: "Traphouse Get It", "Bankroll Stack It"
- 808: "Knockin 808s", "808s & Heartbreak"

### Ambient Names
- Poetic: "Dissolving Reflections", "Drifting Memories"
- Atmospheric: "Ocean at Dusk", "Forest at Dawn"
- Meditative: "Eternal Peace", "Journey to Serenity"

### IDM Names
- Glitchy: "buffer.overflow", "[null:42]", "loop(glitch)"
- Experimental: "untitled_042", "draft_20_c", "beta_1.4.7"

## 🛠️ Development

```bash
# Run in development mode
python -m acidgrid.main --style idm --measures 16

# Generate all styles for testing
for style in house techno hard-tekno breakbeat idm jungle hip-hop trap ambient drum\&bass; do
    python -m acidgrid --style $style --measures 8
done

# Run tests (when available)
python -m pytest

# Check code style
python -m flake8 acidgrid/
```

## 📜 License

MIT License - Go wild, make noise, destroy dancefloors.

## 🤝 Contributing

Pull requests welcome. Add more styles, more percussion, more chaos.

## ⚠️ Warning

Generated tracks may cause:
- Involuntary body movement
- Sudden urge to rave
- Temporary loss of reality
- Permanent bass addiction
- Style-specific side effects

---

**Built with precision, powered by chaos, crafted for every style.**

*Remember: Every track is unique. Every style is authentic. Every beat is a weapon. Use responsibly.*

## 🎵 Style Showcase

```bash
# House - soulful and groovy
acidgrid --style house --measures 64 --play

# Techno - hypnotic and industrial
acidgrid --style techno --measures 128 --play

# Hard-tekno - aggressive peak-time energy
acidgrid --style hard-tekno --measures 96 --tempo 165 --play

# Hip-hop - laid back boom bap
acidgrid --style hip-hop --measures 64 --tempo 90 --play

# Ambient - atmospheric meditation
acidgrid --style ambient --measures 128 --tempo 70 --play

# Drum&Bass - rolling high-energy
acidgrid --style drum&bass --measures 96 --play
```
