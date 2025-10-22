"""Synth accompaniment generator for techno tracks."""

import random
from typing import List, Tuple


class SynthAccompanimentGenerator:
    """Generates synth accompaniment tracks for techno music."""

    def __init__(self, song_structure=None, style=None):
        self.song_structure = song_structure
        self.style = style

    def _get_chord_notes(self, context: dict, enrichment: str = "auto") -> List[int]:
        """Build chord notes from harmonic context with optional enrichment.

        Args:
            context: Harmonic context with key, scale, chord
            enrichment: Type of chord enrichment:
                - "auto": Randomly choose enrichment
                - "triad": Basic 3-note chord
                - "7th": Add 7th
                - "9th": Add 7th and 9th
                - "sus2": Replace 3rd with 2nd
                - "sus4": Replace 3rd with 4th
                - "add9": Triad + 9th (no 7th)
        """
        scale = context.get("scale", [57, 59, 60, 62, 64, 65, 67, 69, 71, 72])
        chord_name = context.get("chord", "i")

        # Map chord symbols to scale degrees (0-indexed)
        # Base triads
        chord_patterns = {
            "i": [0, 2, 4],      # root, minor 3rd, 5th (e.g., Am: A, C, E)
            "ii": [1, 3, 5],     # supertonic minor
            "III": [2, 4, 6],    # mediant major
            "iv": [3, 5, 7],     # subdominant minor
            "V": [4, 6, 1],      # dominant major
            "VI": [5, 7, 2],     # submediant major
            "VII": [6, 1, 3],    # leading tone diminished
            "bVII": [5, 7, 2],   # subtonic major (flat 7)
        }

        pattern = list(chord_patterns.get(chord_name, [0, 2, 4]))

        # Auto-select enrichment with weighted probability
        if enrichment == "auto":
            enrichment = random.choices(
                ["triad", "7th", "9th", "sus2", "sus4", "add9"],
                weights=[0.3, 0.25, 0.15, 0.1, 0.1, 0.1]  # Favor triads and 7ths
            )[0]

        # Apply enrichment
        if enrichment == "7th":
            # Add 7th degree (6 steps above root)
            pattern.append((pattern[0] + 6) % len(scale))
        elif enrichment == "9th":
            # Add 7th and 9th
            pattern.append((pattern[0] + 6) % len(scale))
            pattern.append((pattern[0] + 8) % len(scale))  # 9th = octave + 2nd
        elif enrichment == "sus2":
            # Replace 3rd with 2nd
            pattern[1] = (pattern[0] + 1) % len(scale)
        elif enrichment == "sus4":
            # Replace 3rd with 4th
            pattern[1] = (pattern[0] + 3) % len(scale)
        elif enrichment == "add9":
            # Add 9th without 7th
            pattern.append((pattern[0] + 8) % len(scale))

        # Build chord using scale degrees
        chord_notes = []
        for degree in pattern:
            if degree < len(scale):
                chord_notes.append(scale[degree])
            else:
                # Wrap to next octave if needed
                wrapped_degree = degree % len(scale)
                chord_notes.append(scale[wrapped_degree] + 12)

        return chord_notes
        
    def generate(self, measures: int, tempo: int) -> List[Tuple[float, int, int]]:
        """
        Generate a synth accompaniment track.
        
        Args:
            measures: Number of measures to generate
            tempo: Tempo in BPM
            
        Returns:
            List of (time, note, velocity) tuples
        """
        events = []

        # Calculate timing
        beats_per_measure = 4
        current_time = 0.0
        beat_duration = 60.0 / tempo

        for measure in range(measures):
            # Get context from song structure
            if self.song_structure:
                context = self.song_structure.get_harmonic_context(measure)
                intensity = context["intensity"]
                should_play = self.song_structure.should_play_instrument(measure, "synth_accomp")
                if not should_play:
                    current_time += beats_per_measure * beat_duration
                    continue
            else:
                # Default context
                context = {
                    "key": "A_minor",
                    "scale": [57, 59, 60, 62, 64, 65, 67, 69, 71, 72],
                    "chord": "i",
                    "intensity": 0.7
                }
                intensity = 0.7

            # Get chord notes from harmonic context
            chord_notes = self._get_chord_notes(context)

            # Generate accompaniment pattern for this measure
            pattern_events = self._generate_accompaniment_pattern(
                chord_notes, current_time, beat_duration, measure, intensity
            )
            events.extend(pattern_events)

            current_time += beats_per_measure * beat_duration

        return events

    def _generate_accompaniment_pattern(self, chord_notes: List[int], start_time: float, 
                                      beat_duration: float, measure: int, intensity: float = 0.7) -> List[Tuple[float, int, int]]:
        """Generate accompaniment pattern for a single measure."""
        events = []
        
        # Different pattern styles
        pattern_type = self._choose_pattern_type(measure)
        
        if pattern_type == "stabs":
            events = self._create_stab_pattern(chord_notes, start_time, beat_duration, measure, intensity)
        elif pattern_type == "arpeggios":
            events = self._create_arpeggio_pattern(chord_notes, start_time, beat_duration, measure, intensity)
        elif pattern_type == "sustained":
            events = self._create_sustained_pattern(chord_notes, start_time, beat_duration, measure, intensity)
        elif pattern_type == "filtered":
            events = self._create_filtered_pattern(chord_notes, start_time, beat_duration, measure, intensity)
        
        return events
    
    def _choose_pattern_type(self, measure: int) -> str:
        """Choose accompaniment pattern type based on track progression and style."""
        # Adjust probabilities based on synth_density and style
        synth_density = self.style.synth_density if self.style else 0.7
        style_name = self.style.name if self.style and hasattr(self.style, 'name') else None

        # Techno loves arpeggios!
        if style_name == 'techno':
            if measure < 16:  # Intro
                return random.choices(
                    ["arpeggios", "filtered", "sustained", "stabs"],
                    weights=[0.5, 0.2, 0.2, 0.1]
                )[0]
            elif measure < 64:  # Build up
                return random.choices(
                    ["arpeggios", "filtered", "stabs", "sustained"],
                    weights=[0.6, 0.2, 0.15, 0.05]
                )[0]
            elif measure < 128:  # Main section - massif d'arpèges
                return random.choices(
                    ["arpeggios", "filtered", "stabs"],
                    weights=[0.7, 0.2, 0.1]
                )[0]
            else:  # Outro
                return random.choices(
                    ["arpeggios", "filtered", "sustained"],
                    weights=[0.5, 0.3, 0.2]
                )[0]

        # Other styles - original behavior with slight tweaks
        if measure < 16:  # Intro - minimal
            if synth_density > 0.8:  # Ambient/IDM - more active even in intro
                return random.choice(["sustained", "arpeggios", "stabs"])
            else:
                return random.choice(["stabs", "sustained"])
        elif measure < 64:  # Build up
            if synth_density < 0.6:  # Hip-hop/minimal styles
                return random.choice(["stabs", "sustained", "filtered"])
            else:
                return random.choice(["stabs", "arpeggios", "filtered"])
        elif measure < 128:  # Main section
            if synth_density > 0.8:  # Dense styles (ambient, IDM)
                return random.choice(["arpeggios", "filtered", "sustained", "stabs"])
            else:
                return random.choice(["arpeggios", "filtered", "stabs"])
        else:  # Outro/breakdown
            return random.choice(["sustained", "filtered"])
    
    def _create_stab_pattern(self, chord_notes: List[int], start_time: float, 
                           beat_duration: float, measure: int, intensity: float) -> List[Tuple[float, int, int]]:
        """Create synth stab pattern."""
        events = []
        
        # Stabs on off-beats typically
        stab_timings = [0.5, 2.5]  # Between beats 1-2 and 3-4
        
        for timing in stab_timings:
            if random.random() < 0.8:  # 80% chance for each stab
                stab_time = start_time + timing * beat_duration
                base_velocity = random.randint(40, 65)  # Augmenter légèrement
                
                # Play chord notes simultaneously with dynamic velocity
                for note in chord_notes:
                    if self.song_structure:
                        velocity = self.song_structure.get_velocity_curve(measure, base_velocity)
                    else:
                        velocity = int(base_velocity * intensity)
                    events.append((stab_time, note, velocity))
        
        return events
    
    def _create_arpeggio_pattern(self, chord_notes: List[int], start_time: float,
                               beat_duration: float, measure: int, intensity: float) -> List[Tuple[float, int, int]]:
        """Create arpeggiated pattern with multiple variations."""
        events = []

        # Choose arpeggio variation
        arp_type = random.choice([
            "classic_16th",      # Classic 16th note up
            "classic_down",      # Classic 16th note down
            "octave_up",         # Up with octave jump
            "octave_down",       # Down with octave jump
            "pingpong",          # Up-down pattern
            "broken",            # Broken chord pattern
            "triplet",           # Triplet feel
            "syncopated",        # Syncopated pattern
            "double_octave",     # Two octave range
            "sparse",            # Sparse arpeggio
        ])

        if arp_type == "classic_16th":
            events = self._arp_classic_16th(chord_notes, start_time, beat_duration, measure, intensity)
        elif arp_type == "classic_down":
            events = self._arp_classic_down(chord_notes, start_time, beat_duration, measure, intensity)
        elif arp_type == "octave_up":
            events = self._arp_octave_up(chord_notes, start_time, beat_duration, measure, intensity)
        elif arp_type == "octave_down":
            events = self._arp_octave_down(chord_notes, start_time, beat_duration, measure, intensity)
        elif arp_type == "pingpong":
            events = self._arp_pingpong(chord_notes, start_time, beat_duration, measure, intensity)
        elif arp_type == "broken":
            events = self._arp_broken(chord_notes, start_time, beat_duration, measure, intensity)
        elif arp_type == "triplet":
            events = self._arp_triplet(chord_notes, start_time, beat_duration, measure, intensity)
        elif arp_type == "syncopated":
            events = self._arp_syncopated(chord_notes, start_time, beat_duration, measure, intensity)
        elif arp_type == "double_octave":
            events = self._arp_double_octave(chord_notes, start_time, beat_duration, measure, intensity)
        elif arp_type == "sparse":
            events = self._arp_sparse(chord_notes, start_time, beat_duration, measure, intensity)

        return events

    def _arp_classic_16th(self, chord_notes, start_time, beat_duration, measure, intensity):
        """Classic ascending 16th note arpeggio."""
        events = []
        sixteenth_duration = beat_duration / 4
        arp_pattern = chord_notes + [chord_notes[0] + 12]

        for i in range(16):
            if random.random() < 0.85:
                note_time = start_time + i * sixteenth_duration
                note = arp_pattern[i % len(arp_pattern)]
                base_velocity = random.randint(30, 55)
                velocity = self._get_velocity(measure, base_velocity, intensity)
                events.append((note_time, note, velocity))
        return events

    def _arp_classic_down(self, chord_notes, start_time, beat_duration, measure, intensity):
        """Classic descending 16th note arpeggio."""
        events = []
        sixteenth_duration = beat_duration / 4
        arp_pattern = list(reversed(chord_notes + [chord_notes[0] + 12]))

        for i in range(16):
            if random.random() < 0.85:
                note_time = start_time + i * sixteenth_duration
                note = arp_pattern[i % len(arp_pattern)]
                base_velocity = random.randint(30, 55)
                velocity = self._get_velocity(measure, base_velocity, intensity)
                events.append((note_time, note, velocity))
        return events

    def _arp_octave_up(self, chord_notes, start_time, beat_duration, measure, intensity):
        """Arpeggio with octave jumps upward."""
        events = []
        sixteenth_duration = beat_duration / 4
        # Pattern: root, 3rd, 5th, root+octave
        arp_pattern = chord_notes + [chord_notes[0] + 12]

        for i in range(16):
            if random.random() < 0.8:
                note_time = start_time + i * sixteenth_duration
                idx = i % len(arp_pattern)
                note = arp_pattern[idx]
                # Add extra octave jump on beat 3
                if i >= 8 and i < 12:
                    note += 12
                base_velocity = random.randint(35, 60)
                velocity = self._get_velocity(measure, base_velocity, intensity)
                events.append((note_time, note, velocity))
        return events

    def _arp_octave_down(self, chord_notes, start_time, beat_duration, measure, intensity):
        """Arpeggio with octave jumps downward."""
        events = []
        sixteenth_duration = beat_duration / 4
        arp_pattern = [chord_notes[0] + 12] + list(reversed(chord_notes))

        for i in range(16):
            if random.random() < 0.8:
                note_time = start_time + i * sixteenth_duration
                note = arp_pattern[i % len(arp_pattern)]
                base_velocity = random.randint(35, 60)
                velocity = self._get_velocity(measure, base_velocity, intensity)
                events.append((note_time, note, velocity))
        return events

    def _arp_pingpong(self, chord_notes, start_time, beat_duration, measure, intensity):
        """Up-down ping-pong arpeggio."""
        events = []
        sixteenth_duration = beat_duration / 4
        # Up then down
        arp_up = chord_notes + [chord_notes[0] + 12]
        arp_down = list(reversed(chord_notes))
        arp_pattern = arp_up + arp_down

        for i in range(16):
            if random.random() < 0.85:
                note_time = start_time + i * sixteenth_duration
                note = arp_pattern[i % len(arp_pattern)]
                base_velocity = random.randint(30, 55)
                velocity = self._get_velocity(measure, base_velocity, intensity)
                events.append((note_time, note, velocity))
        return events

    def _arp_broken(self, chord_notes, start_time, beat_duration, measure, intensity):
        """Broken chord pattern (1-3-2-3 style)."""
        events = []
        sixteenth_duration = beat_duration / 4
        # Broken pattern: root, 5th, 3rd, 5th, root+octave, 5th, 3rd, 5th
        if len(chord_notes) >= 3:
            pattern = [chord_notes[0], chord_notes[2], chord_notes[1], chord_notes[2]]
        else:
            pattern = chord_notes + [chord_notes[0]]

        for i in range(16):
            if random.random() < 0.75:
                note_time = start_time + i * sixteenth_duration
                note = pattern[i % len(pattern)]
                base_velocity = random.randint(30, 55)
                velocity = self._get_velocity(measure, base_velocity, intensity)
                events.append((note_time, note, velocity))
        return events

    def _arp_triplet(self, chord_notes, start_time, beat_duration, measure, intensity):
        """Triplet feel arpeggio."""
        events = []
        # 12 triplets per measure (3 per beat)
        triplet_duration = beat_duration / 3
        arp_pattern = chord_notes + [chord_notes[0] + 12]

        for i in range(12):
            if random.random() < 0.8:
                note_time = start_time + i * triplet_duration
                note = arp_pattern[i % len(arp_pattern)]
                base_velocity = random.randint(30, 55)
                velocity = self._get_velocity(measure, base_velocity, intensity)
                events.append((note_time, note, velocity))
        return events

    def _arp_syncopated(self, chord_notes, start_time, beat_duration, measure, intensity):
        """Syncopated arpeggio pattern."""
        events = []
        sixteenth_duration = beat_duration / 4
        arp_pattern = chord_notes + [chord_notes[0] + 12]
        # Syncopated rhythm: play on off-beats
        syncopated_steps = [1, 3, 5, 6, 8, 10, 11, 13, 15]

        for i in syncopated_steps:
            if random.random() < 0.85:
                note_time = start_time + i * sixteenth_duration
                note = arp_pattern[i % len(arp_pattern)]
                base_velocity = random.randint(35, 60)
                velocity = self._get_velocity(measure, base_velocity, intensity)
                events.append((note_time, note, velocity))
        return events

    def _arp_double_octave(self, chord_notes, start_time, beat_duration, measure, intensity):
        """Two octave range arpeggio."""
        events = []
        sixteenth_duration = beat_duration / 4
        # Extend to two octaves
        arp_pattern = chord_notes + [n + 12 for n in chord_notes] + [chord_notes[0] + 24]

        for i in range(16):
            if random.random() < 0.8:
                note_time = start_time + i * sixteenth_duration
                note = arp_pattern[i % len(arp_pattern)]
                base_velocity = random.randint(30, 55)
                velocity = self._get_velocity(measure, base_velocity, intensity)
                events.append((note_time, note, velocity))
        return events

    def _arp_sparse(self, chord_notes, start_time, beat_duration, measure, intensity):
        """Sparse, minimal arpeggio."""
        events = []
        eighth_duration = beat_duration / 2
        arp_pattern = chord_notes + [chord_notes[0] + 12]

        for i in range(8):
            if random.random() < 0.6:
                note_time = start_time + i * eighth_duration
                note = arp_pattern[i % len(arp_pattern)]
                base_velocity = random.randint(30, 50)
                velocity = self._get_velocity(measure, base_velocity, intensity)
                events.append((note_time, note, velocity))
        return events

    def _get_velocity(self, measure, base_velocity, intensity):
        """Helper to get velocity with song structure."""
        if self.song_structure:
            return self.song_structure.get_velocity_curve(measure, base_velocity)
        else:
            return int(base_velocity * intensity)
    
    def _create_sustained_pattern(self, chord_notes: List[int], start_time: float,
                                beat_duration: float, measure: int, intensity: float) -> List[Tuple[float, int, int]]:
        """Create sustained chord pattern."""
        events = []
        
        # Long sustained chords
        if random.random() < 0.6:  # 60% chance for sustained chord
            base_velocity = random.randint(30, 50)  # Augmenter sustained
            for note in chord_notes:
                if self.song_structure:
                    velocity = self.song_structure.get_velocity_curve(measure, base_velocity)
                else:
                    velocity = int(base_velocity * intensity)
                events.append((start_time, note, velocity))
        
        return events
    
    def _create_filtered_pattern(self, chord_notes: List[int], start_time: float,
                               beat_duration: float, measure: int, intensity: float) -> List[Tuple[float, int, int]]:
        """Create filtered/modulated pattern."""
        events = []
        
        # Eighth note pattern with varying velocities (simulating filter sweep)
        eighth_duration = beat_duration / 2
        
        base_velocity = 45  # Augmenter filtered pattern
        for i in range(8):  # 8 eighth notes
            if random.random() < 0.8:
                note_time = start_time + i * eighth_duration
                # Simulate filter sweep with velocity changes
                velocity_mod = int(30 * abs(0.5 - (i / 8.0)))  # Creates sweep effect
                base_vel = max(25, min(65, base_velocity + velocity_mod))  # Augmenter plage
                
                # Play random chord notes
                selected_notes = random.sample(chord_notes, random.randint(1, 2))
                for note in selected_notes:
                    if self.song_structure:
                        velocity = self.song_structure.get_velocity_curve(measure, base_vel)
                    else:
                        velocity = int(base_vel * intensity)
                    events.append((note_time, note, velocity))
        
        return events