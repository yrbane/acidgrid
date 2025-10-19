"""Enhanced rhythm track generator with dynamic velocity and build-ups."""

import random
from typing import List, Tuple


class RhythmGenerator:
    """Generates rhythm tracks with dynamic velocity curves and song structure awareness."""

    # MIDI note numbers for drum sounds - Standard GM Drum Map
    # Kicks and Snares
    BASS_DRUM = 36      # C2 - Acoustic Bass Drum
    BASS_DRUM_2 = 35    # B1 - Acoustic Bass Drum (alternative)
    SNARE_DRUM = 38     # D2 - Acoustic Snare
    SNARE_DRUM_2 = 40   # E2 - Electric Snare
    CLAP = 39           # D#2 - Hand Clap
    SIDE_STICK = 37     # C#2 - Side Stick / Rimshot

    # Toms
    LOW_TOM = 41        # F2 - Low Floor Tom
    LOW_TOM_2 = 43      # G2 - High Floor Tom
    MID_TOM = 47        # B2 - Low-Mid Tom
    MID_TOM_2 = 48      # C3 - Hi-Mid Tom
    HIGH_TOM = 50       # D3 - High Tom
    HIGH_TOM_2 = 45     # A2 - Low Tom (another variant)

    # Hi-hats
    HI_HAT = 42         # F#2 - Closed Hi-Hat
    PEDAL_HI_HAT = 44   # G#2 - Pedal Hi-Hat
    OPEN_HI_HAT = 46    # A#2 - Open Hi-Hat

    # Cymbals
    CRASH = 49          # C#3 - Crash Cymbal 1
    CRASH_2 = 57        # A3 - Crash Cymbal 2
    SPLASH = 55         # G3 - Splash Cymbal
    RIDE = 51           # D#3 - Ride Cymbal 1
    RIDE_BELL = 53      # F3 - Ride Bell
    CHINA = 52          # E3 - Chinese Cymbal

    # Latin Percussion
    COWBELL = 56        # G#3 - Cowbell
    TAMBOURINE = 54     # F#3 - Tambourine
    VIBRASLAP = 58      # A#3 - Vibraslap
    HIGH_BONGO = 60     # C4 - Hi Bongo
    LOW_BONGO = 61      # C#4 - Low Bongo
    MUTE_HI_CONGA = 62  # D4 - Mute Hi Conga
    OPEN_HI_CONGA = 63  # D#4 - Open Hi Conga
    LOW_CONGA = 64      # E4 - Low Conga
    HIGH_TIMBALE = 65   # F4 - High Timbale
    LOW_TIMBALE = 66    # F#4 - Low Timbale
    HIGH_AGOGO = 67     # G4 - High Agogo
    LOW_AGOGO = 68      # G#4 - Low Agogo
    CABASA = 69         # A4 - Cabasa
    MARACAS = 70        # A#4 - Maracas

    # Whistles and Effects
    SHORT_WHISTLE = 71  # B4 - Short Whistle
    LONG_WHISTLE = 72   # C5 - Long Whistle
    SHORT_GUIRO = 73    # C#5 - Short Guiro
    LONG_GUIRO = 74     # D5 - Long Guiro
    CLAVES = 75         # D#5 - Claves
    HI_WOOD_BLOCK = 76  # E5 - Hi Wood Block
    LOW_WOOD_BLOCK = 77 # F5 - Low Wood Block

    # Electronic/808 sounds
    MUTE_CUICA = 78     # F#5 - Mute Cuica
    OPEN_CUICA = 79     # G5 - Open Cuica
    MUTE_TRIANGLE = 80  # G#5 - Mute Triangle
    OPEN_TRIANGLE = 81  # A5 - Open Triangle
    SHAKER = 82         # A#5 - Shaker (often mapped here in modern kits)
    
    def __init__(self, song_structure=None, style=None):
        self.song_structure = song_structure
        self.style = style
        self.patterns = self._create_patterns()
        self.current_pattern_index = 0
    
    def _create_patterns(self) -> dict:
        """Create various rhythm patterns for different sections."""
        return {
            "minimal": {
                "bd": [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                "sd": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                "clap": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "hh": [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                "oh": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                "shaker": [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                "rim": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            },
            "driving": {
                "bd": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                "sd": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                "clap": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                "hh": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                "oh": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                "shaker": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                "tambourine": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                "ride": [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            },
            "complex": {
                "bd": [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0],
                "sd": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                "clap": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                "hh": [1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0],
                "oh": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                "shaker": [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
                "cowbell": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                "rim": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                "pedal_hh": [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0],
            },
            "breakbeat": {
                "bd": [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                "sd": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                "clap": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                "hh": [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                "oh": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                "shaker": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                "tambourine": [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                "ride": [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
                "crash": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            },
            "rolling": {
                "bd": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                "sd": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                "clap": [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                "hh": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                "oh": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "shaker": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                "tambourine": [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                "cowbell": [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                "ride_bell": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            }
        }
    
    def generate(self, measures: int, tempo: int) -> List[Tuple[float, int, int]]:
        """Generate a dynamic rhythm track with velocity automation."""
        events = []
        
        # Calculate timing
        beats_per_measure = 4
        sixteenth_notes_per_beat = 4
        steps_per_measure = beats_per_measure * sixteenth_notes_per_beat
        step_duration = 60.0 / (tempo * sixteenth_notes_per_beat)
        
        current_time = 0.0
        pattern_history = []
        
        for measure in range(measures):
            # Get section context
            if self.song_structure:
                section = self.song_structure.get_section(measure)
                intensity = self.song_structure.get_intensity(measure)
                should_play = self.song_structure.should_play_instrument(measure, "drums")
                
                if not should_play:
                    current_time += beats_per_measure * (60.0 / tempo)
                    continue
            else:
                section = None
                intensity = 0.7
            
            # Choose pattern based on section
            pattern = self._choose_pattern_for_section(section, intensity, measure)
            
            # Avoid repeating the same pattern too much
            if len(pattern_history) >= 4 and all(p == pattern for p in pattern_history[-4:]):
                pattern = random.choice([p for p in self.patterns.keys() if p != pattern])
            pattern_history.append(pattern)
            if len(pattern_history) > 8:
                pattern_history.pop(0)
            
            current_pattern = self.patterns[pattern]
            
            # Apply section-specific modifications
            modified_pattern = self._apply_section_modifications(current_pattern, section, measure, intensity)
            
            # Generate events for this measure
            for step in range(steps_per_measure):
                step_time = current_time + (step * step_duration)
                
                # Add crash on important transitions
                if step == 0 and self._should_add_crash(measure):
                    events.append((step_time, self.CRASH, random.randint(90, 127)))
                
                # Generate drum hits with dynamic velocity
                events.extend(self._generate_drum_hits(
                    modified_pattern, step, step_time, intensity, measure
                ))
            
            current_time += beats_per_measure * (60.0 / tempo)
        
        return events
    
    def _choose_pattern_for_section(self, section, intensity, measure):
        """Choose appropriate pattern based on section and style."""
        # Get style-preferred patterns
        if self.style and hasattr(self.style, 'rhythm_patterns'):
            preferred_patterns = self.style.rhythm_patterns
        else:
            preferred_patterns = list(self.patterns.keys())

        if section:
            if "intro" in section.name or "outro" in section.name:
                # Prefer minimal patterns for intro/outro
                options = [p for p in preferred_patterns if p in ["minimal", "driving"]]
                if not options:
                    options = ["minimal"]
                return random.choice(options + ["minimal"])  # Weight towards minimal
            elif "buildup" in section.name:
                # Progress from simple to complex
                if intensity < 0.4:
                    return "minimal"
                elif intensity < 0.6:
                    options = [p for p in preferred_patterns if p in ["driving", "minimal"]]
                    return random.choice(options) if options else "driving"
                else:
                    options = [p for p in preferred_patterns if p in ["complex", "rolling", "breakbeat"]]
                    return random.choice(options) if options else random.choice(["complex", "rolling"])
            elif "drop" in section.name or "main" in section.name or "verse" in section.name:
                # Use style-preferred patterns for main sections
                return random.choice(preferred_patterns)
            elif "breakdown" in section.name or "break" in section.name:
                # Minimal or breakbeat for breakdowns
                options = [p for p in preferred_patterns if p in ["minimal", "breakbeat"]]
                return random.choice(options) if options else random.choice(["minimal", "breakbeat"])

        # Default progression
        if measure < 8:
            return "minimal"
        elif measure < 32:
            options = [p for p in preferred_patterns if p in ["driving", "complex"]]
            return random.choice(options) if options else random.choice(preferred_patterns)
        else:
            return random.choice(preferred_patterns)
    
    def _apply_section_modifications(self, pattern, section, measure, intensity):
        """Apply modifications based on section."""
        modified = {key: list(value) for key, value in pattern.items()}
        
        # Build-up modifications
        if section and "buildup" in section.name:
            # Gradually add more hits
            progress = (measure - section.start_measure) / max(1, (section.end_measure - section.start_measure))
            
            # Snare/clap roll at the end
            if progress > 0.75:
                for i in range(12, 16):
                    if random.random() < progress:
                        modified["sd"][i] = 1
                        modified["clap"][i] = 1
            
            # Increase hi-hat density
            if progress > 0.5:
                for i in range(16):
                    if random.random() < progress * 0.3:
                        modified["hh"][i] = 1
        
        # Drop modifications - full energy
        elif section and "drop" in section.name:
            # Ensure strong kick pattern
            modified["bd"][0] = 1
            modified["bd"][4] = 1
            modified["bd"][8] = 1
            modified["bd"][12] = 1
        
        # Breakdown - sparse
        elif section and "breakdown" in section.name:
            # Remove most kicks
            for i in range(16):
                if random.random() < 0.7:
                    modified["bd"][i] = 0
                if random.random() < 0.5:
                    modified["sd"][i] = 0
        
        # Add toms for variation
        self._add_tom_patterns(modified, measure, intensity)
        
        return modified
    
    def _add_tom_patterns(self, pattern, measure, intensity):
        """Add tom patterns for fills and variations."""
        # Tom fills every 8 measures
        if measure % 8 == 7:
            # Clear pattern for fill
            for i in range(12, 16):
                pattern["hh"][i] = 0
                pattern["oh"][i] = 0

            # Add tom roll
            if random.random() < 0.7:
                pattern["high_tom"] = [0]*12 + [1, 0, 0, 0]
                pattern["mid_tom"] = [0]*12 + [0, 1, 1, 0]
                pattern["low_tom"] = [0]*12 + [0, 0, 0, 1]
        else:
            # Q&A pattern between toms and claps
            pattern["high_tom"] = [0] * 16
            pattern["mid_tom"] = [0] * 16
            pattern["low_tom"] = [0] * 16

            if measure % 2 == 0 and random.random() < 0.3:
                # Tom question
                pattern["low_tom"][4] = 1
                pattern["mid_tom"][6] = 1
                pattern["high_tom"][7] = 1

        # Add style-specific percussion layers
        self._add_style_percussion(pattern, measure, intensity)

    def _add_style_percussion(self, pattern, measure, intensity):
        """Add style-specific percussion layers."""
        if not self.style:
            return

        style_name = self.style.name if hasattr(self.style, 'name') else 'techno'

        # House: Latin percussion, congas, bongos
        if style_name == 'house':
            if measure % 2 == 0 and random.random() < 0.6:
                pattern["conga_low"] = [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
                pattern["conga_high"] = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
            if random.random() < 0.4:
                pattern["bongo_hi"] = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
                pattern["bongo_low"] = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0]
            if random.random() < 0.5:
                pattern["claves"] = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]

        # Techno: Industrial sounds, minimal percussion
        elif style_name == 'techno':
            if random.random() < 0.3:
                pattern["cowbell"] = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
            if measure % 4 == 3 and random.random() < 0.4:
                pattern["wood_block"] = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]

        # Hard-tekno: Maximum percussion density
        elif style_name == 'hard-tekno':
            pattern["cowbell"] = [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
            if random.random() < 0.6:
                pattern["wood_block"] = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
            if intensity > 0.7:
                pattern["claves"] = [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1]

        # Breakbeat: Funky percussion
        elif style_name == 'breakbeat':
            if random.random() < 0.5:
                pattern["cowbell"] = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
            if random.random() < 0.4:
                pattern["conga_high"] = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]

        # IDM: Glitchy, randomized percussion
        elif style_name == 'idm':
            if random.random() < 0.5:
                # Random glitchy percussion
                pattern["wood_block"] = [random.randint(0, 1) for _ in range(16)]
                pattern["claves"] = [random.randint(0, 1) if random.random() < 0.3 else 0 for _ in range(16)]

        # Jungle/DnB: Massive percussion density
        elif style_name in ['jungle', 'drum&bass']:
            if random.random() < 0.7:
                pattern["conga_low"] = [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
                pattern["conga_high"] = [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0]
            if random.random() < 0.5:
                pattern["agogo_hi"] = [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0]
                pattern["agogo_low"] = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]

        # Hip-hop: Minimal, boom bap style
        elif style_name == 'hip-hop':
            if measure % 4 == 0 and random.random() < 0.3:
                pattern["cowbell"] = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]

        # Trap: Hi-hat rolls and minimal percussion
        elif style_name == 'trap':
            # Trap hi-hat rolls
            if measure % 4 == 3 and random.random() < 0.7:
                # Hi-hat roll in last beat
                pattern["hh"] = pattern["hh"][:12] + [1, 1, 1, 1]
            if random.random() < 0.3:
                pattern["cowbell"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]

        # Ambient: Sparse, atmospheric percussion
        elif style_name == 'ambient':
            if random.random() < 0.3:
                pattern["triangle"] = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
            if random.random() < 0.2:
                pattern["chimes"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    
    def _generate_drum_hits(self, pattern, step, step_time, intensity, measure):
        """Generate individual drum hits with dynamic velocity."""
        events = []

        # Base velocities modified by intensity
        base_velocities = {
            "bd": 120,
            "sd": 105,
            "clap": 95,
            "hh": 75,
            "oh": 85,
            "pedal_hh": 70,
            "low_tom": 100,
            "mid_tom": 95,
            "high_tom": 90,
            "crash": 110,
            "ride": 80,
            "ride_bell": 85,
            "shaker": 65,
            "tambourine": 75,
            "cowbell": 85,
            "rim": 80,
            "conga_low": 85,
            "conga_high": 80,
            "bongo_hi": 75,
            "bongo_low": 80,
            "agogo_hi": 75,
            "agogo_low": 70,
            "wood_block": 80,
            "claves": 85,
            "triangle": 60,
            "chimes": 70,
        }

        # Velocity curves for different drums
        velocity_curves = {
            "bd": lambda i, m: 1.0 + (0.2 if step % 4 == 0 else -0.1),
            "sd": lambda i, m: i * 0.8 + 0.4,
            "clap": lambda i, m: i * 0.7 + 0.5,
            "hh": lambda i, m: 0.5 + i * 0.3 + random.uniform(-0.1, 0.1),
            "oh": lambda i, m: 0.6 + i * 0.2,
            "pedal_hh": lambda i, m: 0.4 + i * 0.3,
            "low_tom": lambda i, m: 0.8 + i * 0.2,
            "mid_tom": lambda i, m: 0.75 + i * 0.2,
            "high_tom": lambda i, m: 0.7 + i * 0.2,
            "crash": lambda i, m: 0.9 + i * 0.1,
            "ride": lambda i, m: 0.6 + i * 0.2,
            "ride_bell": lambda i, m: 0.7 + i * 0.2,
            "shaker": lambda i, m: 0.5 + i * 0.2 + random.uniform(-0.1, 0.1),
            "tambourine": lambda i, m: 0.6 + i * 0.2,
            "cowbell": lambda i, m: 0.7 + i * 0.2,
            "rim": lambda i, m: 0.6 + i * 0.2,
            "conga_low": lambda i, m: 0.7 + i * 0.2,
            "conga_high": lambda i, m: 0.65 + i * 0.2,
            "bongo_hi": lambda i, m: 0.6 + i * 0.2,
            "bongo_low": lambda i, m: 0.65 + i * 0.2,
            "agogo_hi": lambda i, m: 0.6 + i * 0.2,
            "agogo_low": lambda i, m: 0.55 + i * 0.2,
            "wood_block": lambda i, m: 0.65 + i * 0.2,
            "claves": lambda i, m: 0.7 + i * 0.2,
            "triangle": lambda i, m: 0.5 + i * 0.1,
            "chimes": lambda i, m: 0.55 + i * 0.1,
        }

        # Map pattern keys to MIDI notes
        drum_map = {
            "bd": self.BASS_DRUM,
            "sd": self.SNARE_DRUM,
            "clap": self.CLAP,
            "hh": self.HI_HAT,
            "oh": self.OPEN_HI_HAT,
            "pedal_hh": self.PEDAL_HI_HAT,
            "low_tom": self.LOW_TOM,
            "mid_tom": self.MID_TOM,
            "high_tom": self.HIGH_TOM,
            "crash": self.CRASH,
            "ride": self.RIDE,
            "ride_bell": self.RIDE_BELL,
            "shaker": self.SHAKER,
            "tambourine": self.TAMBOURINE,
            "cowbell": self.COWBELL,
            "rim": self.SIDE_STICK,
            "conga_low": self.LOW_CONGA,
            "conga_high": self.OPEN_HI_CONGA,
            "bongo_hi": self.HIGH_BONGO,
            "bongo_low": self.LOW_BONGO,
            "agogo_hi": self.HIGH_AGOGO,
            "agogo_low": self.LOW_AGOGO,
            "wood_block": self.HI_WOOD_BLOCK,
            "claves": self.CLAVES,
            "triangle": self.OPEN_TRIANGLE,
            "chimes": self.OPEN_TRIANGLE,  # Using triangle for chimes
        }
        
        for drum_name, midi_note in drum_map.items():
            if drum_name in pattern and len(pattern[drum_name]) > step and pattern[drum_name][step]:
                # Calculate velocity with curve
                base_vel = base_velocities[drum_name]
                curve_mod = velocity_curves[drum_name](intensity, measure)
                
                # Apply song structure velocity modification
                if self.song_structure:
                    final_vel = self.song_structure.get_velocity_curve(measure, int(base_vel * curve_mod))
                else:
                    final_vel = int(base_vel * curve_mod * intensity)
                
                # Add subtle random humanization
                final_vel += random.randint(-5, 5)
                final_vel = max(1, min(127, final_vel))
                
                events.append((step_time, midi_note, final_vel))
        
        return events
    
    def _should_add_crash(self, measure):
        """Determine if a crash should be added."""
        # Add crash at major transitions
        if self.song_structure:
            section = self.song_structure.get_section(measure)
            # Check if this is the first measure of a new section
            if measure > 0:
                prev_section = self.song_structure.get_section(measure - 1)
                if section != prev_section and "drop" in section.name:
                    return True
        
        # Default crash points
        return measure % 16 == 0 and measure > 0 and random.random() < 0.7