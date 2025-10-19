"""Sub-bass generator for deep, long fundamental notes."""

import random
from typing import List, Tuple


class SubBassGenerator:
    """Generates sub-bass tracks with long, deep fundamental notes."""
    
    # Sub-bass note range (very low frequencies)
    SUB_BASS_NOTES = {
        "C": 12,   # C0 - 16.35 Hz
        "D": 14,   # D0 - 18.35 Hz
        "E": 16,   # E0 - 20.60 Hz
        "F": 17,   # F0 - 21.83 Hz
        "G": 19,   # G0 - 24.50 Hz
        "A": 21,   # A0 - 27.50 Hz
        "Bb": 22,  # Bb0 - 29.14 Hz
        "B": 23,   # B0 - 30.87 Hz
    }
    
    def __init__(self, song_structure=None, style=None):
        self.song_structure = song_structure
        self.style = style
        self.current_key = "A"
        
    def generate(self, measures: int, tempo: int) -> List[Tuple[float, int, int]]:
        """
        Generate a sub-bass track with long, sustained notes.
        
        Args:
            measures: Number of measures to generate
            tempo: Tempo in BPM
            
        Returns:
            List of (time, note, velocity) tuples
        """
        events = []
        
        # Calculate timing
        beats_per_measure = 4
        beat_duration = 60.0 / tempo
        measure_duration = beats_per_measure * beat_duration
        
        current_time = 0.0
        
        for measure in range(measures):
            # Get context from song structure if available
            if self.song_structure:
                context = self.song_structure.get_harmonic_context(measure)
                intensity = context["intensity"]
                should_play = self.song_structure.should_play_instrument(measure, "sub_bass")
                if not should_play:
                    current_time += measure_duration
                    continue
            else:
                intensity = 0.7
            
            # Determine sub-bass behavior based on track section
            if self._should_play_sub_bass(measure):
                pattern = self._generate_sub_bass_pattern(measure)
                
                for beat_offset, duration_beats, note_key, velocity in pattern:
                    note_time = current_time + beat_offset * beat_duration
                    note = self.SUB_BASS_NOTES[note_key]
                    
                    # Apply velocity dynamics
                    if self.song_structure:
                        final_velocity = self.song_structure.get_velocity_curve(measure, velocity)
                    else:
                        final_velocity = velocity
                    
                    # Add note with long sustain
                    events.append((note_time, note, final_velocity))
                    
                    # Note off after duration
                    # Sub-bass notes are typically longer
                    note_off_time = note_time + duration_beats * beat_duration
                    events.append((note_off_time, note, 0))
            
            current_time += measure_duration
        
        return events
    
    def _should_play_sub_bass(self, measure: int) -> bool:
        """Determine if sub-bass should play in this measure."""
        # Sub-bass doesn't play during breaks
        if measure % 8 == 7:  # Break measure
            return random.random() < 0.3
        if measure % 16 == 15:  # Major break
            return False
        if measure % 32 == 31:  # Big break
            return False
        
        # Intro - gradually introduce sub-bass
        if measure < 8:
            return random.random() < 0.2
        elif measure < 16:
            return random.random() < 0.5
        elif measure < 32:
            return random.random() < 0.7
        
        # Main sections - mostly present
        return random.random() < 0.9
    
    def _generate_sub_bass_pattern(self, measure: int) -> List[Tuple[float, float, str, int]]:
        """
        Generate sub-bass pattern for a measure.
        Returns list of (beat_offset, duration_beats, note_key, velocity).
        """
        patterns = []
        
        # Choose pattern style based on section
        if measure < 32:  # Intro - simple, long notes
            patterns = self._create_simple_pattern()
        elif measure < 128:  # Main section - more movement
            if random.random() < 0.7:
                patterns = self._create_pumping_pattern()
            else:
                patterns = self._create_movement_pattern()
        else:  # Outro/breakdown
            patterns = self._create_sparse_pattern()
        
        return patterns
    
    def _create_simple_pattern(self) -> List[Tuple[float, float, str, int]]:
        """Create simple sub-bass pattern with long notes."""
        patterns = [
            # Single long note per measure
            [(0, 4, self.current_key, 90)],
            
            # Two notes per measure
            [(0, 2, self.current_key, 95), (2, 2, self.current_key, 85)],
            
            # Sustained with slight variation
            [(0, 3.5, self.current_key, 90), (3.75, 0.25, self.current_key, 70)],
        ]
        return random.choice(patterns)
    
    def _create_pumping_pattern(self) -> List[Tuple[float, float, str, int]]:
        """Create pumping sub-bass pattern (sidechain effect simulation)."""
        # Simulate sidechain compression with velocity changes
        base_note = self.current_key
        
        patterns = [
            # Pumping on every beat
            [
                (0, 0.75, base_note, 100),
                (1, 0.75, base_note, 100),
                (2, 0.75, base_note, 100),
                (3, 0.75, base_note, 100),
            ],
            
            # Pumping on kicks with variation
            [
                (0, 0.5, base_note, 110),
                (0.75, 0.25, base_note, 60),
                (1, 0.5, base_note, 100),
                (2, 0.5, base_note, 105),
                (2.75, 0.25, base_note, 65),
                (3, 0.5, base_note, 95),
            ],
            
            # Long note with velocity automation
            [
                (0, 1, base_note, 100),
                (1, 1, base_note, 80),
                (2, 1, base_note, 90),
                (3, 1, base_note, 75),
            ],
        ]
        return random.choice(patterns)
    
    def _create_movement_pattern(self) -> List[Tuple[float, float, str, int]]:
        """Create sub-bass pattern with note movement."""
        # Add some harmonic movement
        root = self.current_key
        fifth = self._get_fifth(root)
        octave_down = root  # Already very low
        
        patterns = [
            # Root to fifth movement
            [(0, 2, root, 95), (2, 2, fifth, 90)],
            
            # More complex movement
            [(0, 1, root, 100), (1, 0.5, fifth, 85), (1.5, 0.5, root, 80), (2, 2, root, 95)],
            
            # Rhythmic pattern
            [(0, 0.5, root, 110), (0.5, 0.5, root, 70), (2, 0.5, fifth, 100), (2.5, 1.5, root, 85)],
        ]
        return random.choice(patterns)
    
    def _create_sparse_pattern(self) -> List[Tuple[float, float, str, int]]:
        """Create sparse sub-bass pattern for breakdowns."""
        patterns = [
            # Single hit
            [(0, 1, self.current_key, 85)],
            
            # Two sparse hits
            [(0, 0.5, self.current_key, 90), (3, 1, self.current_key, 80)],
            
            # Very long sustain
            [(0, 8, self.current_key, 70)],  # Extends beyond measure
        ]
        return random.choice(patterns)
    
    def _get_fifth(self, root: str) -> str:
        """Get the fifth of a given root note."""
        fifths = {
            "C": "G",
            "D": "A", 
            "E": "B",
            "F": "C",
            "G": "D",
            "A": "E",
            "Bb": "F",
            "B": "F",
        }
        return fifths.get(root, root)