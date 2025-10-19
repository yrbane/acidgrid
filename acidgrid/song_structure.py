"""Song structure manager for creating dynamic techno tracks."""

import random
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class Section:
    """Represents a section of the track."""
    name: str
    start_measure: int
    end_measure: int
    intensity: float  # 0.0 to 1.0
    key: str
    scale: str
    description: str


class SongStructure:
    """Manages the overall structure and progression of a techno track."""
    
    # Available keys with their relative minors/majors
    KEYS = {
        "A_minor": {"notes": [57, 59, 60, 62, 64, 65, 67, 69], "relative": "C_major"},
        "D_minor": {"notes": [62, 64, 65, 67, 69, 70, 72, 74], "relative": "F_major"},
        "E_minor": {"notes": [64, 66, 67, 69, 71, 72, 74, 76], "relative": "G_major"},
        "F_minor": {"notes": [65, 67, 68, 70, 72, 73, 75, 77], "relative": "Ab_major"},
        "G_minor": {"notes": [67, 69, 70, 72, 74, 75, 77, 79], "relative": "Bb_major"},
    }
    
    # Chord progressions for different moods
    PROGRESSIONS = {
        "dark": ["i", "iv", "i", "v"],
        "uplifting": ["i", "VI", "III", "VII"],
        "driving": ["i", "i", "i", "i"],
        "emotional": ["i", "v", "VI", "iv"],
        "tension": ["i", "bII", "i", "v"],
    }
    
    def __init__(self, total_measures: int, style=None):
        self.total_measures = total_measures
        self.style = style
        self.sections = self._create_structure()
        self.current_key = random.choice(list(self.KEYS.keys()))
        self.mood = self._choose_mood_for_style()

    def _choose_mood_for_style(self) -> str:
        """Choose appropriate mood based on music style."""
        if not self.style:
            return random.choice(list(self.PROGRESSIONS.keys()))

        style_moods = {
            "house": ["uplifting", "emotional", "dark"],
            "techno": ["dark", "driving", "tension"],
            "hard-tekno": ["driving", "tension", "dark"],
            "breakbeat": ["uplifting", "driving"],
            "idm": ["tension", "dark", "emotional"],
            "jungle": ["dark", "driving", "tension"],
            "hip-hop": ["emotional", "dark"],
            "trap": ["dark", "tension"],
            "ambient": ["emotional", "uplifting"],
            "drum&bass": ["dark", "driving", "tension"],
        }

        moods = style_moods.get(self.style.name, list(self.PROGRESSIONS.keys()))
        return random.choice(moods)

    def _create_structure(self) -> List[Section]:
        """Create a dynamic song structure based on total measures and style."""
        sections = []

        # Style-specific structure templates
        if self.style and self.style.structure_type == "ambient":
            # Ambient: minimal structure, slow evolution
            sections = self._create_ambient_structure()
        elif self.style and self.style.structure_type == "hip-hop":
            # Hip-hop: verse/chorus structure
            sections = self._create_hiphop_structure()
        elif self.style and self.style.structure_type == "trap":
            # Trap: drop-focused structure
            sections = self._create_trap_structure()
        elif self.style and self.style.structure_type in ["breakbeat", "jungle", "dnb"]:
            # Breakbeat/Jungle/DnB: high-energy with breaks
            sections = self._create_breakbeat_structure()
        elif self.style and self.style.structure_type == "aggressive":
            # Hard-tekno: relentless energy
            sections = self._create_aggressive_structure()
        else:
            # Default: progressive techno/house structure
            sections = self._create_default_structure()

        return sections

    def _create_default_structure(self) -> List[Section]:
        """Default progressive structure for techno/house."""
        if self.total_measures <= 32:
            return [
                Section("intro", 0, 4, 0.3, "A_minor", "minor", "Minimal intro"),
                Section("main", 4, 24, 0.8, "A_minor", "minor", "Main groove"),
                Section("outro", 24, self.total_measures, 0.4, "A_minor", "minor", "Fade out"),
            ]
        elif self.total_measures <= 64:
            return [
                Section("intro", 0, 8, 0.2, "A_minor", "minor", "Atmospheric intro"),
                Section("buildup", 8, 16, 0.5, "A_minor", "minor", "Energy building"),
                Section("drop", 16, 32, 0.9, "A_minor", "minor", "Main drop"),
                Section("breakdown", 32, 40, 0.4, "D_minor", "minor", "Melodic breakdown"),
                Section("buildup2", 40, 48, 0.6, "A_minor", "minor", "Second build"),
                Section("drop2", 48, 56, 1.0, "A_minor", "minor", "Peak energy"),
                Section("outro", 56, self.total_measures, 0.3, "A_minor", "minor", "Cool down"),
            ]
        else:
            section_length = self.total_measures // 8
            return [
                Section("intro", 0, section_length, 0.2, "A_minor", "minor", "Atmospheric opening"),
                Section("verse1", section_length, section_length*2, 0.5, "A_minor", "minor", "First verse"),
                Section("buildup1", section_length*2, section_length*3, 0.7, "A_minor", "minor", "Rising tension"),
                Section("drop1", section_length*3, section_length*4, 0.95, "A_minor", "minor", "First drop"),
                Section("breakdown", section_length*4, section_length*5, 0.3, "D_minor", "minor", "Ambient breakdown"),
                Section("buildup2", section_length*5, section_length*6, 0.8, "A_minor", "minor", "Final build"),
                Section("drop2", section_length*6, section_length*7, 1.0, "A_minor", "minor", "Climax"),
                Section("outro", section_length*7, self.total_measures, 0.2, "A_minor", "minor", "Fade out"),
            ]

    def _create_ambient_structure(self) -> List[Section]:
        """Ambient structure: slow, evolving, minimal intensity changes."""
        section_length = max(16, self.total_measures // 4)
        return [
            Section("intro", 0, section_length, 0.2, "A_minor", "minor", "Atmospheric opening"),
            Section("evolution", section_length, section_length*2, 0.4, "D_minor", "minor", "Textural evolution"),
            Section("plateau", section_length*2, section_length*3, 0.5, "E_minor", "minor", "Sustained plateau"),
            Section("outro", section_length*3, self.total_measures, 0.3, "A_minor", "minor", "Gentle fade"),
        ]

    def _create_hiphop_structure(self) -> List[Section]:
        """Hip-hop structure: verse/hook alternation."""
        if self.total_measures <= 32:
            return [
                Section("intro", 0, 4, 0.3, "A_minor", "minor", "Beat intro"),
                Section("verse1", 4, 12, 0.6, "A_minor", "minor", "First verse"),
                Section("hook", 12, 20, 0.8, "A_minor", "minor", "Hook"),
                Section("verse2", 20, 28, 0.7, "A_minor", "minor", "Second verse"),
                Section("outro", 28, self.total_measures, 0.4, "A_minor", "minor", "Fade out"),
            ]
        else:
            section_length = self.total_measures // 8
            return [
                Section("intro", 0, section_length, 0.3, "A_minor", "minor", "Beat intro"),
                Section("verse1", section_length, section_length*2, 0.6, "A_minor", "minor", "First verse"),
                Section("hook1", section_length*2, section_length*3, 0.8, "A_minor", "minor", "Hook"),
                Section("verse2", section_length*3, section_length*4, 0.7, "D_minor", "minor", "Second verse"),
                Section("bridge", section_length*4, section_length*5, 0.5, "E_minor", "minor", "Bridge"),
                Section("verse3", section_length*5, section_length*6, 0.7, "A_minor", "minor", "Third verse"),
                Section("hook2", section_length*6, section_length*7, 0.9, "A_minor", "minor", "Final hook"),
                Section("outro", section_length*7, self.total_measures, 0.3, "A_minor", "minor", "Outro"),
            ]

    def _create_trap_structure(self) -> List[Section]:
        """Trap structure: buildup/drop focused."""
        section_length = max(8, self.total_measures // 6)
        return [
            Section("intro", 0, section_length, 0.3, "A_minor", "minor", "Minimal intro"),
            Section("buildup1", section_length, section_length*2, 0.6, "A_minor", "minor", "First buildup"),
            Section("drop1", section_length*2, section_length*3, 0.95, "A_minor", "minor", "Hard drop"),
            Section("break", section_length*3, section_length*4, 0.4, "D_minor", "minor", "Break section"),
            Section("buildup2", section_length*4, section_length*5, 0.8, "A_minor", "minor", "Final buildup"),
            Section("drop2", section_length*5, self.total_measures, 1.0, "A_minor", "minor", "Peak drop"),
        ]

    def _create_breakbeat_structure(self) -> List[Section]:
        """Breakbeat/Jungle/DnB structure: high energy with breakdowns."""
        section_length = max(8, self.total_measures // 6)
        return [
            Section("intro", 0, section_length, 0.4, "A_minor", "minor", "Drum intro"),
            Section("main1", section_length, section_length*2, 0.85, "A_minor", "minor", "Main section"),
            Section("breakdown", section_length*2, section_length*3, 0.3, "D_minor", "minor", "Atmospheric break"),
            Section("buildup", section_length*3, section_length*4, 0.7, "A_minor", "minor", "Tension build"),
            Section("main2", section_length*4, section_length*5, 0.95, "A_minor", "minor", "Peak energy"),
            Section("outro", section_length*5, self.total_measures, 0.5, "A_minor", "minor", "Outro"),
        ]

    def _create_aggressive_structure(self) -> List[Section]:
        """Hard-tekno structure: relentless high-energy."""
        section_length = max(8, self.total_measures // 5)
        return [
            Section("intro", 0, section_length, 0.7, "A_minor", "minor", "Aggressive intro"),
            Section("main1", section_length, section_length*2, 0.95, "A_minor", "minor", "Peak intensity"),
            Section("breakdown", section_length*2, section_length*3, 0.6, "D_minor", "minor", "Brief respite"),
            Section("main2", section_length*3, section_length*4, 1.0, "A_minor", "minor", "Maximum energy"),
            Section("outro", section_length*4, self.total_measures, 0.8, "A_minor", "minor", "Intense outro"),
        ]
    
    def get_section(self, measure: int) -> Section:
        """Get the current section for a given measure."""
        for section in self.sections:
            if section.start_measure <= measure < section.end_measure:
                return section
        return self.sections[-1]  # Default to last section
    
    def get_intensity(self, measure: int) -> float:
        """Get the intensity level for a given measure with smooth transitions."""
        section = self.get_section(measure)
        
        # Add gradual transitions between sections
        position_in_section = (measure - section.start_measure) / max(1, (section.end_measure - section.start_measure))
        
        # Find next section for smooth transition
        next_section = None
        for i, s in enumerate(self.sections):
            if s == section and i < len(self.sections) - 1:
                next_section = self.sections[i + 1]
                break
        
        if next_section and position_in_section > 0.75:
            # Smooth transition to next section
            transition_progress = (position_in_section - 0.75) * 4
            return section.intensity + (next_section.intensity - section.intensity) * transition_progress
        
        return section.intensity
    
    def get_velocity_curve(self, measure: int, base_velocity: int) -> int:
        """Apply velocity curves based on song position."""
        intensity = self.get_intensity(measure)
        section = self.get_section(measure)
        
        # Apply section-specific velocity modulation
        if section.name.startswith("buildup"):
            # Gradually increase velocity during buildups
            progress = (measure - section.start_measure) / max(1, (section.end_measure - section.start_measure))
            modifier = 0.7 + (0.3 * progress)
        elif section.name.startswith("drop"):
            # High energy in drops
            modifier = 1.0 + random.uniform(-0.1, 0.1)
        elif section.name == "breakdown":
            # Softer in breakdowns
            modifier = 0.6 + random.uniform(-0.1, 0.1)
        else:
            modifier = intensity
        
        # Add subtle random variation
        modifier += random.uniform(-0.05, 0.05)
        
        final_velocity = int(base_velocity * modifier)
        return max(1, min(127, final_velocity))
    
    def should_play_instrument(self, measure: int, instrument: str) -> bool:
        """Determine if an instrument should play based on section."""
        section = self.get_section(measure)
        
        rules = {
            "intro": {
                "drums": random.random() < 0.3,
                "bass": random.random() < 0.2,
                "sub_bass": False,
                "synth_accomp": random.random() < 0.4,
                "synth_lead": random.random() < 0.1,
            },
            "buildup": {
                "drums": True,
                "bass": True,
                "sub_bass": random.random() < 0.7,
                "synth_accomp": True,
                "synth_lead": random.random() < 0.5,
            },
            "drop": {
                "drums": True,
                "bass": True,
                "sub_bass": True,
                "synth_accomp": True,
                "synth_lead": random.random() < 0.8,
            },
            "breakdown": {
                "drums": random.random() < 0.4,
                "bass": random.random() < 0.6,
                "sub_bass": random.random() < 0.3,
                "synth_accomp": True,
                "synth_lead": random.random() < 0.7,
            },
            "outro": {
                "drums": random.random() < 0.5,
                "bass": random.random() < 0.4,
                "sub_bass": False,
                "synth_accomp": random.random() < 0.6,
                "synth_lead": random.random() < 0.3,
            },
        }
        
        # Get base rule for section type
        section_type = section.name.rstrip("0123456789")  # Remove numbers
        if section_type not in rules:
            section_type = "buildup" if "build" in section_type else "drop"
        
        return rules.get(section_type, rules["drop"]).get(instrument, True)
    
    def get_harmonic_context(self, measure: int) -> Dict:
        """Get harmonic context for a measure (key, scale, chord)."""
        section = self.get_section(measure)
        progression = self.PROGRESSIONS[self.mood]
        
        # Get current chord in progression
        measures_in_section = measure - section.start_measure
        chord_index = (measures_in_section // 4) % len(progression)
        current_chord = progression[chord_index]
        
        return {
            "key": section.key,
            "scale": self.KEYS[section.key]["notes"],
            "chord": current_chord,
            "section": section.name,
            "intensity": self.get_intensity(measure),
        }