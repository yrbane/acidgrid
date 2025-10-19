"""Synth accompaniment generator for techno tracks."""

import random
from typing import List, Tuple


class SynthAccompanimentGenerator:
    """Generates synth accompaniment tracks for techno music."""
    
    # Chord progressions in different keys (MIDI note numbers)
    CHORD_PROGRESSIONS = {
        "A_minor": {
            "Am": [57, 60, 64],    # A3, C4, E4
            "F": [53, 57, 60],     # F3, A3, C4  
            "C": [48, 52, 55],     # C3, E3, G3
            "G": [55, 59, 62],     # G3, B3, D4
        },
        "D_minor": {
            "Dm": [62, 65, 69],    # D4, F4, A4
            "Bb": [58, 62, 65],    # Bb3, D4, F4
            "F": [53, 57, 60],     # F3, A3, C4
            "C": [48, 52, 55],     # C3, E3, G3
        }
    }
    
    def __init__(self, song_structure=None, style=None):
        self.song_structure = song_structure
        self.style = style
        self.current_key = "A_minor"
        
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
        
        # Generate chord progression
        chord_progression = self._generate_chord_progression(measures)
        
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
                intensity = 0.7
            
            chord_name = chord_progression[measure % len(chord_progression)]
            chord_notes = self.CHORD_PROGRESSIONS[self.current_key][chord_name]
            
            # Generate accompaniment pattern for this measure
            pattern_events = self._generate_accompaniment_pattern(
                chord_notes, current_time, beat_duration, measure, intensity
            )
            events.extend(pattern_events)
            
            current_time += beats_per_measure * beat_duration
        
        return events
    
    def _generate_chord_progression(self, measures: int) -> List[str]:
        """Generate chord progression for the track."""
        if self.current_key == "A_minor":
            # Common techno progressions in A minor
            progressions = [
                ["Am", "Am", "F", "G"],
                ["Am", "F", "C", "G"], 
                ["Am", "Am", "Am", "Am"],  # Minimal
                ["Am", "F", "Am", "G"],
            ]
        else:
            # D minor progressions
            progressions = [
                ["Dm", "Bb", "F", "C"],
                ["Dm", "Dm", "Bb", "C"],
                ["Dm", "Dm", "Dm", "Dm"],  # Minimal
            ]
        
        # Choose progression and extend for full track
        base_progression = random.choice(progressions)
        full_progression = []
        
        for measure in range(measures):
            # Every 16 measures, potentially change progression
            if measure > 0 and measure % 16 == 0 and random.random() < 0.4:
                base_progression = random.choice(progressions)
            
            full_progression.append(base_progression[measure % len(base_progression)])
        
        return full_progression
    
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
        # Adjust probabilities based on synth_density
        synth_density = self.style.synth_density if self.style else 0.7

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
                base_velocity = random.randint(35, 55)  # Beaucoup plus doux
                
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
        """Create arpeggiated pattern."""
        events = []
        
        # 16th note arpeggios
        sixteenth_duration = beat_duration / 4
        
        # Create arpeggio pattern
        arp_pattern = chord_notes + [chord_notes[0] + 12]  # Add octave
        
        for i in range(16):  # 16 sixteenth notes per measure
            if random.random() < 0.7:  # 70% probability for each note
                note_time = start_time + i * sixteenth_duration
                note = arp_pattern[i % len(arp_pattern)]
                base_velocity = random.randint(25, 45)  # Plus doux pour arpeggios
                
                if self.song_structure:
                    velocity = self.song_structure.get_velocity_curve(measure, base_velocity)
                else:
                    velocity = int(base_velocity * intensity)
                    
                events.append((note_time, note, velocity))
        
        return events
    
    def _create_sustained_pattern(self, chord_notes: List[int], start_time: float,
                                beat_duration: float, measure: int, intensity: float) -> List[Tuple[float, int, int]]:
        """Create sustained chord pattern."""
        events = []
        
        # Long sustained chords
        if random.random() < 0.6:  # 60% chance for sustained chord
            base_velocity = random.randint(20, 40)  # Très doux pour sustained
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
        
        base_velocity = 35  # Plus doux pour filtered pattern
        for i in range(8):  # 8 eighth notes
            if random.random() < 0.8:
                note_time = start_time + i * eighth_duration
                # Simulate filter sweep with velocity changes
                velocity_mod = int(30 * abs(0.5 - (i / 8.0)))  # Creates sweep effect
                base_vel = max(15, min(50, base_velocity + velocity_mod))  # Réduire plage velocity
                
                # Play random chord notes
                selected_notes = random.sample(chord_notes, random.randint(1, 2))
                for note in selected_notes:
                    if self.song_structure:
                        velocity = self.song_structure.get_velocity_curve(measure, base_vel)
                    else:
                        velocity = int(base_vel * intensity)
                    events.append((note_time, note, velocity))
        
        return events