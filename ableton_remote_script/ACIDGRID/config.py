"""
Configuration for ACIDGRID Remote Script.
"""

# Style definitions with colors
STYLES = {
    "house": {
        "color": 9,  # Orange
        "description": "Soulful, groovy, four-on-the-floor"
    },
    "techno": {
        "color": 5,  # Purple
        "description": "Hypnotic, industrial, relentless"
    },
    "hard-tekno": {
        "color": 1,  # Red
        "description": "Fast, aggressive, distorted"
    },
    "breakbeat": {
        "color": 11,  # Yellow
        "description": "Syncopated, funky, energetic"
    },
    "idm": {
        "color": 16,  # Cyan
        "description": "Intelligent, glitchy, experimental"
    },
    "jungle": {
        "color": 18,  # Green
        "description": "Fast breaks, heavy bass, ragga"
    },
    "hip-hop": {
        "color": 60,  # Brown
        "description": "Laid back, boom bap, groovy"
    },
    "trap": {
        "color": 56,  # Pink
        "description": "808 bass, hi-hat rolls, modern"
    },
    "ambient": {
        "color": 23,  # Light Blue
        "description": "Atmospheric, sparse, meditative"
    },
    "drum&bass": {
        "color": 26,  # Lime
        "description": "Fast breaks, deep bass, high energy"
    }
}

# MIDI mapping for controller integration
# Maps MIDI notes to styles (compatible with Launchpad, Push, etc.)
MIDI_MAPPING = {
    "house": {"note": 60, "channel": 0},      # C4
    "techno": {"note": 61, "channel": 0},     # C#4
    "hard-tekno": {"note": 62, "channel": 0}, # D4
    "breakbeat": {"note": 63, "channel": 0},  # D#4
    "idm": {"note": 64, "channel": 0},        # E4
    "jungle": {"note": 65, "channel": 0},     # F4
    "hip-hop": {"note": 66, "channel": 0},    # F#4
    "trap": {"note": 67, "channel": 0},       # G4
    "ambient": {"note": 68, "channel": 0},    # G#4
    "drum&bass": {"note": 69, "channel": 0},  # A4
}

# Measure presets mapping
MEASURE_MAPPING = {
    "note": {
        72: 16,   # C5 = 16 measures
        73: 32,   # C#5 = 32 measures
        74: 64,   # D5 = 64 measures
        75: 128,  # D#5 = 128 measures
        76: 192,  # E5 = 192 measures
    },
    "channel": 0
}

# Track selection mapping (for individual track generation)
TRACK_MAPPING = {
    "rhythm": {"note": 48, "channel": 0},         # C3 - Rhythm track
    "bassline": {"note": 49, "channel": 0},       # C#3 - Bassline track
    "sub_bass": {"note": 50, "channel": 0},       # D3 - Sub Bass track
    "synth_accomp": {"note": 51, "channel": 0},   # D#3 - Synth Accompaniment
    "synth_lead": {"note": 52, "channel": 0},     # E3 - Synth Lead
}

# Generation mode mapping
GENERATION_MODE_MAPPING = {
    "full_track": {"note": 81, "channel": 0},     # A5 - Generate all 5 tracks separately
}

# Track names for Ableton
TRACK_NAMES = {
    "rhythm": "Rhythm",
    "bassline": "Bassline",
    "sub_bass": "Sub Bass",
    "synth_accomp": "Synth Accompaniment",
    "synth_lead": "Synth Lead",
}

# Default settings
DEFAULT_MEASURES = 32
DEFAULT_STYLE = "techno"
