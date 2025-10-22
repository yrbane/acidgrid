"""Enhanced rhythm track generator with dynamic velocity and build-ups."""

import random
from typing import List, Tuple
from ..time_signature import TimeSignature, COMMON_TIME_SIGNATURES


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
    
    def __init__(self, song_structure=None, style=None, time_signature=None, swing=0.0):
        self.song_structure = song_structure
        self.style = style
        self.time_signature = time_signature or COMMON_TIME_SIGNATURES["4/4"]
        self.swing = swing
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
    
    def generate(self, measures: int, tempo: int, swing=None) -> List[Tuple[float, int, int]]:
        """Generate a dynamic rhythm track with velocity automation and optional swing."""
        events = []

        # Use provided swing or instance swing
        swing_amount = swing if swing is not None else self.swing

        # Calculate timing
        beats_per_measure = self.time_signature.beats_per_measure
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

                # Apply swing to off-beat notes (odd-numbered steps)
                if swing_amount > 0 and step % 2 == 1:
                    # Swing delay: shift off-beats later by swing_amount
                    # At swing=0.5, off-beats move to triplet position
                    # At swing=1.0, off-beats move to maximum shuffle
                    swing_delay = (step_duration * swing_amount) * 0.5
                    step_time += swing_delay

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
        # Check if we're at a section transition
        is_transition = self._is_section_transition(measure)

        # Different fill strategies
        if is_transition:
            # Major transition fill (section change)
            fill_type = self._choose_fill_type(measure, intensity)
            self._generate_fill(pattern, fill_type, intensity, measure)
        elif measure % 8 == 7:
            # Regular 8-bar fill
            fill_type = self._choose_fill_type(measure, intensity, major=False)
            self._generate_fill(pattern, fill_type, intensity, measure)
        elif measure % 4 == 3 and random.random() < 0.4:
            # Light 4-bar variation
            self._add_light_fill(pattern, intensity)
        else:
            # Initialize tom patterns
            pattern["high_tom"] = [0] * 16
            pattern["mid_tom"] = [0] * 16
            pattern["low_tom"] = [0] * 16

            # Occasional tom accents
            if measure % 2 == 0 and random.random() < 0.3:
                pattern["low_tom"][4] = 1
                pattern["mid_tom"][6] = 1
                pattern["high_tom"][7] = 1

        # Add style-specific percussion layers
        self._add_style_percussion(pattern, measure, intensity)

    def _is_section_transition(self, measure):
        """Check if this measure is at a section boundary."""
        if not self.song_structure:
            return False

        if measure == 0:
            return False

        current_section = self.song_structure.get_section(measure)
        prev_section = self.song_structure.get_section(measure - 1)

        # Check if we're transitioning to a new section
        if current_section != prev_section:
            return True

        # Check if we're one measure before section change (pre-fill)
        if measure + 1 < self.song_structure.total_measures:
            next_section = self.song_structure.get_section(measure + 1)
            if current_section != next_section:
                return True

        return False

    def _choose_fill_type(self, measure, intensity, major=True):
        """Choose appropriate fill type based on style, intensity, and context."""
        style_name = self.style.name if self.style and hasattr(self.style, 'name') else 'techno'

        # Style-specific fill preferences
        fill_styles = {
            'house': ['tom_roll', 'snare_build', 'light_percussion'],
            'techno': ['tom_roll', 'snare_build', 'crash_accent'],
            'hard-tekno': ['aggressive_roll', 'double_snare', 'crash_accent'],
            'breakbeat': ['snare_roll', 'tom_cascade', 'light_percussion'],
            'idm': ['glitch_fill', 'tom_scatter', 'sparse_accent'],
            'jungle': ['snare_roll', 'tom_cascade', 'aggressive_roll'],
            'hip-hop': ['snare_triplet', 'light_percussion', 'sparse_accent'],
            'trap': ['snare_roll', 'crash_accent', 'sparse_accent'],
            'ambient': ['sparse_accent', 'light_percussion', 'cymbal_swell'],
            'drum&bass': ['snare_roll', 'aggressive_roll', 'tom_cascade'],
        }

        available_fills = fill_styles.get(style_name, ['tom_roll', 'snare_build', 'crash_accent'])

        # Intensity affects fill choice
        if major and intensity > 0.7:
            # Prefer more intense fills for high-energy transitions
            intense_fills = ['aggressive_roll', 'snare_roll', 'tom_cascade', 'double_snare']
            available_fills = [f for f in available_fills if f in intense_fills] or intense_fills
        elif intensity < 0.4:
            # Subtle fills for low intensity
            subtle_fills = ['light_percussion', 'sparse_accent', 'cymbal_swell']
            available_fills = [f for f in available_fills if f in subtle_fills] or subtle_fills

        return random.choice(available_fills)

    def _generate_fill(self, pattern, fill_type, intensity, measure):
        """Generate specific fill pattern based on type."""
        # Clear last beat for fill space
        for i in range(12, 16):
            pattern["hh"][i] = 0
            pattern["oh"][i] = 0

        # Initialize tom patterns
        pattern["high_tom"] = [0] * 16
        pattern["mid_tom"] = [0] * 16
        pattern["low_tom"] = [0] * 16

        if fill_type == 'tom_roll':
            # Classic descending tom roll
            pattern["high_tom"][12] = 1
            pattern["high_tom"][13] = 1
            pattern["mid_tom"][13] = 1
            pattern["mid_tom"][14] = 1
            pattern["low_tom"][14] = 1
            pattern["low_tom"][15] = 1

        elif fill_type == 'tom_cascade':
            # Cascading toms (jungle/dnb style)
            pattern["high_tom"] = [0]*10 + [1, 0, 1, 1, 0, 1]
            pattern["mid_tom"] = [0]*11 + [1, 0, 1, 0, 1]
            pattern["low_tom"] = [0]*12 + [0, 1, 1, 1]

        elif fill_type == 'snare_roll':
            # Fast snare roll (16th notes)
            pattern["sd"] = pattern["sd"][:12] + [1, 1, 1, 1]

        elif fill_type == 'snare_build':
            # Building snare pattern
            pattern["sd"] = pattern["sd"][:12] + [1, 0, 1, 1]
            pattern["clap"] = pattern["clap"][:12] + [0, 1, 1, 1]

        elif fill_type == 'aggressive_roll':
            # Intense snare + tom roll (hard-tekno/dnb)
            pattern["sd"] = pattern["sd"][:10] + [1, 1, 1, 1, 1, 1]
            pattern["high_tom"] = [0]*12 + [1, 0, 1, 0]
            pattern["low_tom"] = [0]*13 + [0, 1, 1]

        elif fill_type == 'double_snare':
            # Double snare hits
            pattern["sd"] = pattern["sd"][:12] + [1, 1, 0, 1]
            pattern["clap"] = pattern["clap"][:12] + [1, 1, 0, 1]

        elif fill_type == 'snare_triplet':
            # Triplet feel snare (hip-hop)
            pattern["sd"] = pattern["sd"][:12] + [1, 0, 1, 0]

        elif fill_type == 'light_percussion':
            # Subtle percussion fill
            pattern["rim"] = [0]*12 + [1, 0, 1, 0]
            pattern["tambourine"] = [0]*13 + [0, 1, 1]

        elif fill_type == 'crash_accent':
            # Crash cymbal accent
            pattern["crash"] = [0]*15 + [1]
            pattern["sd"] = pattern["sd"][:14] + [1, 0]

        elif fill_type == 'sparse_accent':
            # Minimal accent (ambient/minimal)
            pattern["rim"] = [0]*14 + [1, 0]

        elif fill_type == 'cymbal_swell':
            # Cymbal-based fill (ambient)
            pattern["crash"] = [0]*12 + [0, 0, 1, 0]
            pattern["ride"] = [0]*13 + [1, 0, 1]

        elif fill_type == 'glitch_fill':
            # Randomized glitchy fill (IDM)
            for i in range(12, 16):
                if random.random() < 0.6:
                    choice = random.choice(['sd', 'rim', 'high_tom'])
                    pattern[choice][i] = 1

        elif fill_type == 'tom_scatter':
            # Scattered tom hits
            pattern["high_tom"][12] = 1
            pattern["mid_tom"][13] = 1 if random.random() < 0.7 else 0
            pattern["low_tom"][14] = 1
            pattern["high_tom"][15] = 1 if random.random() < 0.5 else 0

    def _add_light_fill(self, pattern, intensity):
        """Add subtle fill variation for 4-bar phrases."""
        pattern["high_tom"] = [0] * 16
        pattern["mid_tom"] = [0] * 16
        pattern["low_tom"] = [0] * 16

        # Light accent on last beat
        if random.random() < 0.6:
            pattern["rim"] = pattern.get("rim", [0]*16)
            pattern["rim"][14] = 1

        # Occasional tom accent
        if random.random() < 0.4:
            pattern["low_tom"][15] = 1

    def _add_hihat_rolls(self, pattern, measure, intensity, style_name):
        """Add sophisticated hi-hat rolls for trap and drum&bass."""
        # Determine if this measure should have a roll
        should_roll = False
        roll_type = "short"

        if style_name == 'trap':
            # Trap: rolls on measure 4, 8, 12, 16 (every 4 bars, on last bar)
            if measure % 4 == 3:
                should_roll = random.random() < 0.8  # 80% chance
                roll_type = random.choice(["short", "medium", "long"])
            # Occasional surprise rolls
            elif random.random() < 0.15:
                should_roll = True
                roll_type = "short"

        elif style_name in ['jungle', 'drum&bass']:
            # DnB: more frequent, faster rolls
            if measure % 2 == 1:
                should_roll = random.random() < 0.6  # 60% chance every 2 bars
                roll_type = random.choice(["medium", "long", "ultra"])
            elif intensity > 0.7 and random.random() < 0.3:
                should_roll = True
                roll_type = "short"

        if not should_roll:
            return

        # Generate roll pattern based on type
        if roll_type == "short":
            # Last beat only: 1/16 notes
            # Pattern: [0,0,0,0, 0,0,0,0, 0,0,0,0, 1,1,1,1]
            for i in range(12, 16):
                pattern["hh"][i] = 1

        elif roll_type == "medium":
            # Last 2 beats: increasing density
            # Pattern: [0,0,0,0, 0,0,0,0, 1,0,1,0, 1,1,1,1]
            pattern["hh"][8] = 1
            pattern["hh"][10] = 1
            for i in range(12, 16):
                pattern["hh"][i] = 1

        elif roll_type == "long":
            # Last 3 beats: progressive build
            # Pattern: [0,0,0,0, 1,0,0,1, 1,0,1,0, 1,1,1,1]
            pattern["hh"][4] = 1
            pattern["hh"][7] = 1
            pattern["hh"][8] = 1
            pattern["hh"][10] = 1
            for i in range(12, 16):
                pattern["hh"][i] = 1

        elif roll_type == "ultra":
            # Full bar roll (DnB style): maximum density
            # Pattern: fills entire second half with 1/16 notes
            for i in range(8, 16):
                pattern["hh"][i] = 1

        # Mark that this pattern has a roll (for velocity ramping)
        pattern["_hihat_roll"] = {
            "type": roll_type,
            "start": 12 if roll_type == "short" else (8 if roll_type == "medium" else 4)
        }

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

        # Jungle/DnB: Massive percussion density + hi-hat rolls
        elif style_name in ['jungle', 'drum&bass']:
            if random.random() < 0.7:
                pattern["conga_low"] = [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
                pattern["conga_high"] = [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0]
            if random.random() < 0.5:
                pattern["agogo_hi"] = [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0]
                pattern["agogo_low"] = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
            # DnB hi-hat rolls
            self._add_hihat_rolls(pattern, measure, intensity, style_name)

        # Hip-hop: Minimal, boom bap style
        elif style_name == 'hip-hop':
            if measure % 4 == 0 and random.random() < 0.3:
                pattern["cowbell"] = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]

        # Trap: Hi-hat rolls and minimal percussion
        elif style_name == 'trap':
            # Advanced trap hi-hat rolls
            self._add_hihat_rolls(pattern, measure, intensity, style_name)
            if random.random() < 0.3:
                pattern["cowbell"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]

        # Ambient: Sparse, atmospheric percussion
        elif style_name == 'ambient':
            if random.random() < 0.3:
                pattern["triangle"] = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
            if random.random() < 0.2:
                pattern["chimes"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    
    def _generate_drum_hits(self, pattern, step, step_time, intensity, measure):
        """Generate individual drum hits with advanced velocity modulation."""
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

        # Accent patterns - which steps get emphasized
        accent_pattern = self._get_accent_pattern(step)

        # Ghost note probability by instrument
        ghost_note_instruments = {"sd", "hh", "rim"}  # Instruments that can have ghost notes

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
                # Calculate base velocity with curve
                base_vel = base_velocities[drum_name]
                curve_mod = velocity_curves[drum_name](intensity, measure)

                # Start with base velocity
                final_vel = base_vel * curve_mod * intensity

                # Check for hi-hat roll velocity ramp
                if drum_name == "hh" and "_hihat_roll" in pattern:
                    roll_info = pattern["_hihat_roll"]
                    if step >= roll_info["start"]:
                        # Progressive velocity ramp for rolls
                        steps_in_roll = step - roll_info["start"]
                        max_roll_steps = 16 - roll_info["start"]
                        ramp_factor = 0.5 + (steps_in_roll / max_roll_steps) * 0.7  # 0.5 → 1.2
                        final_vel *= ramp_factor

                # Apply accent boost (only if not in a roll)
                elif accent_pattern['strong_accent']:
                    final_vel *= 1.25  # +25% for strong accents (downbeats)
                elif accent_pattern['medium_accent']:
                    final_vel *= 1.12  # +12% for medium accents (beats 2 and 4)

                # Ghost notes for specific instruments (style-dependent)
                if drum_name in ghost_note_instruments and accent_pattern['ghost_note_candidate']:
                    if self._should_add_ghost_note(drum_name):
                        final_vel *= 0.35  # Very low velocity for ghost notes

                # Apply song structure velocity modification
                if self.song_structure:
                    final_vel = self.song_structure.get_velocity_curve(measure, int(final_vel))
                else:
                    final_vel = int(final_vel)

                # Advanced humanization based on style
                humanization = self._get_humanization_amount()
                final_vel += random.randint(-humanization, humanization)

                # Clamp to valid MIDI range
                final_vel = max(1, min(127, final_vel))

                events.append((step_time, midi_note, final_vel))

        return events

    def _get_accent_pattern(self, step):
        """Determine accent type for a given step position."""
        # 16th note grid: 0-15
        # Strong accents: steps 0, 4, 8, 12 (downbeats)
        # Medium accents: steps 2, 6, 10, 14 (backbeats)
        # Ghost note candidates: steps 1, 3, 5, 7, 9, 11, 13, 15 (off-beats)

        return {
            'strong_accent': step % 4 == 0,  # Every quarter note
            'medium_accent': step % 4 == 2,  # On the "and" of each beat
            'ghost_note_candidate': step % 2 == 1,  # All off-beats
        }

    def _should_add_ghost_note(self, drum_name):
        """Determine if a ghost note should be added based on style."""
        if not self.style:
            return False

        style_name = self.style.name if hasattr(self.style, 'name') else 'techno'

        # Style-specific ghost note probabilities
        ghost_note_probs = {
            'hip-hop': 0.6,  # Lots of ghost notes for groove
            'jungle': 0.5,
            'drum&bass': 0.4,
            'breakbeat': 0.5,
            'house': 0.2,
            'techno': 0.1,  # Minimal ghost notes
            'hard-tekno': 0.0,  # No ghost notes
            'idm': 0.3,
            'trap': 0.2,
            'ambient': 0.0,
        }

        prob = ghost_note_probs.get(style_name, 0.2)
        return random.random() < prob

    def _get_humanization_amount(self):
        """Get humanization amount based on style."""
        if not self.style:
            return 5

        style_name = self.style.name if hasattr(self.style, 'name') else 'techno'

        # Style-specific humanization (velocity variation)
        humanization_amounts = {
            'hip-hop': 12,  # High variation for organic feel
            'jungle': 10,
            'drum&bass': 8,
            'breakbeat': 10,
            'idm': 15,  # Very high variation for glitchy feel
            'house': 7,
            'techno': 5,  # Low variation, more mechanical
            'hard-tekno': 3,  # Very low, machine-like
            'trap': 6,
            'ambient': 8,
        }

        return humanization_amounts.get(style_name, 5)
    
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