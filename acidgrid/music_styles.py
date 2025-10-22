"""Music style configurations for ACIDGRID."""

from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class MusicStyle:
    """Configuration for a specific music style."""
    name: str
    tempo_range: Tuple[int, int]  # (min, max) BPM
    default_tempo: int
    rhythm_patterns: List[str]  # Preferred rhythm pattern names
    bassline_riffs: List[str]  # Preferred bassline riff names
    structure_type: str  # Type of song structure
    intensity_curve: str  # How intensity evolves
    synth_density: float  # 0.0 to 1.0 - how much synth activity
    default_swing: float  # 0.0 to 1.0 - groove/swing amount
    description: str


# Define all music styles
MUSIC_STYLES = {
    "house": MusicStyle(
        name="house",
        tempo_range=(120, 128),
        default_tempo=124,
        rhythm_patterns=["driving", "minimal"],
        bassline_riffs=["detroit_funk", "chicago_jack", "hypnotic_loop"],
        structure_type="classic",
        intensity_curve="smooth",
        synth_density=0.8,
        default_swing=0.3,  # Subtle swing for groove
        description="Classic house: four-on-the-floor, soulful, groovy"
    ),

    "techno": MusicStyle(
        name="techno",
        tempo_range=(128, 135),
        default_tempo=128,
        rhythm_patterns=["driving", "complex", "minimal"],
        bassline_riffs=["acid_303", "berlin_minimal", "warehouse_stomp", "rolling_thunder"],
        structure_type="progressive",
        intensity_curve="building",
        synth_density=0.7,
        default_swing=0.1,  # Minimal swing, mostly straight
        description="Techno: hypnotic, industrial, relentless energy"
    ),

    "hard-tekno": MusicStyle(
        name="hard-tekno",
        tempo_range=(150, 170),
        default_tempo=160,
        rhythm_patterns=["driving", "rolling", "complex"],
        bassline_riffs=["acid_303", "sub_pressure", "uk_rave", "techno_gallop"],
        structure_type="aggressive",
        intensity_curve="intense",
        synth_density=0.6,
        default_swing=0.0,  # Straight, no swing
        description="Hard tekno: fast, aggressive, distorted, peak-time energy"
    ),

    "breakbeat": MusicStyle(
        name="breakbeat",
        tempo_range=(130, 150),
        default_tempo=138,
        rhythm_patterns=["breakbeat", "complex"],
        bassline_riffs=["uk_rave", "rolling_thunder", "detroit_funk"],
        structure_type="breakbeat",
        intensity_curve="dynamic",
        synth_density=0.7,
        default_swing=0.2,  # Light swing for funkiness
        description="Breakbeat: syncopated drums, funky, energetic"
    ),

    "idm": MusicStyle(
        name="idm",
        tempo_range=(140, 180),
        default_tempo=160,
        rhythm_patterns=["complex", "breakbeat", "minimal"],
        bassline_riffs=["hypnotic_loop", "sub_pressure", "techno_gallop"],
        structure_type="experimental",
        intensity_curve="erratic",
        synth_density=0.9,
        default_swing=0.4,  # Variable swing for complexity
        description="IDM: intelligent, complex, glitchy, experimental"
    ),

    "jungle": MusicStyle(
        name="jungle",
        tempo_range=(160, 180),
        default_tempo=170,
        rhythm_patterns=["breakbeat", "complex", "rolling"],
        bassline_riffs=["sub_pressure", "rolling_thunder", "uk_rave"],
        structure_type="jungle",
        intensity_curve="frenetic",
        synth_density=0.6,
        default_swing=0.35,  # Moderate swing, reggae influence
        description="Jungle: fast breakbeats, heavy bass, reggae influence"
    ),

    "hip-hop": MusicStyle(
        name="hip-hop",
        tempo_range=(85, 95),
        default_tempo=90,
        rhythm_patterns=["minimal", "breakbeat"],
        bassline_riffs=["detroit_funk", "warehouse_stomp", "sub_pressure"],
        structure_type="hip-hop",
        intensity_curve="laid_back",
        synth_density=0.5,
        default_swing=0.5,  # Strong swing for boom-bap feel
        description="Hip-hop: laid back, boom bap, groovy"
    ),

    "trap": MusicStyle(
        name="trap",
        tempo_range=(140, 160),
        default_tempo=150,
        rhythm_patterns=["minimal", "rolling"],
        bassline_riffs=["sub_pressure", "warehouse_stomp", "hypnotic_loop"],
        structure_type="trap",
        intensity_curve="trap_wave",
        synth_density=0.7,
        default_swing=0.1,  # Minimal swing, modern feel
        description="Trap: 808 bass, hi-hat rolls, modern urban sound"
    ),

    "ambient": MusicStyle(
        name="ambient",
        tempo_range=(60, 90),
        default_tempo=75,
        rhythm_patterns=["minimal"],
        bassline_riffs=["berlin_minimal", "sub_pressure", "hypnotic_loop"],
        structure_type="ambient",
        intensity_curve="atmospheric",
        synth_density=0.9,
        default_swing=0.0,  # No swing, sparse and atmospheric
        description="Ambient: atmospheric, sparse, meditative, textural"
    ),

    "drum&bass": MusicStyle(
        name="drum&bass",
        tempo_range=(170, 180),
        default_tempo=174,
        rhythm_patterns=["breakbeat", "complex", "rolling"],
        bassline_riffs=["sub_pressure", "rolling_thunder", "techno_gallop", "acid_303"],
        structure_type="dnb",
        intensity_curve="energetic",
        synth_density=0.7,
        default_swing=0.2,  # Light swing for groove
        description="Drum & Bass: fast breakbeats, deep bass, high energy"
    ),
}


def get_style(style_name: str) -> MusicStyle:
    """Get a music style configuration by name."""
    return MUSIC_STYLES.get(style_name, MUSIC_STYLES["techno"])


def get_available_styles() -> List[str]:
    """Get list of available style names."""
    return list(MUSIC_STYLES.keys())


def get_style_tempo(style_name: str, custom_tempo: int = None) -> int:
    """Get tempo for a style, using custom if provided, otherwise default."""
    style = get_style(style_name)
    if custom_tempo is not None:
        # Validate custom tempo is within style range
        if style.tempo_range[0] <= custom_tempo <= style.tempo_range[1]:
            return custom_tempo
        else:
            print(f"Warning: Tempo {custom_tempo} outside {style_name} range "
                  f"{style.tempo_range}. Using default {style.default_tempo}.")
            return style.default_tempo
    return style.default_tempo
