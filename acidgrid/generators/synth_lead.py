"""Synth lead generator for techno tracks."""

import random
from typing import List, Tuple


class SynthLeadGenerator:
    """Generates synth lead tracks for techno music."""
    
    # Scales for lead melodies (MIDI note numbers)
    SCALES = {
        "A_minor": [57, 59, 60, 62, 64, 65, 67, 69, 71, 72],  # A3 to C5 natural minor
        "A_minor_pentatonic": [57, 60, 62, 64, 67, 69, 72],   # A minor pentatonic
        "D_minor": [62, 64, 65, 67, 69, 70, 72, 74, 76, 77],  # D4 to F5 natural minor  
    }
    
    def __init__(self, song_structure=None, style=None):
        self.song_structure = song_structure
        self.style = style
        self.current_scale = "A_minor"
        
    def generate(self, measures: int, tempo: int) -> List[Tuple[float, int, int]]:
        """
        Generate a synth lead track.
        
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
        
        # Generate lead melodies in phrases
        phrase_length = 8  # 8-measure phrases
        
        for phrase_start in range(0, measures, phrase_length):
            phrase_end = min(phrase_start + phrase_length, measures)
            
            # Get context from song structure
            if self.song_structure:
                context = self.song_structure.get_harmonic_context(phrase_start)
                intensity = context["intensity"]
                should_play = self.song_structure.should_play_instrument(phrase_start, "synth_lead")
                if not should_play:
                    continue
            else:
                intensity = 0.7
            
            # Determine if this phrase should have lead melody
            if self._should_have_lead(phrase_start, measures, intensity):
                melody_events = self._generate_lead_phrase(
                    phrase_start, phrase_end, current_time + phrase_start * beats_per_measure * beat_duration,
                    beat_duration
                )
                events.extend(melody_events)
        
        return events
    
    def _should_have_lead(self, phrase_start: int, total_measures: int, intensity: float = 0.7) -> bool:
        """Determine if a phrase should have lead melody."""
        # Use intensity to determine probability
        if intensity < 0.3:
            return random.random() < 0.2
        elif intensity < 0.5:
            return random.random() < 0.4
        elif intensity < 0.7:
            return random.random() < 0.6
        elif intensity < 0.9:
            return random.random() < 0.8
        else:
            return random.random() < 0.9
    
    def _generate_lead_phrase(self, start_measure: int, end_measure: int, 
                            start_time: float, beat_duration: float) -> List[Tuple[float, int, int]]:
        """Generate lead melody for a phrase."""
        events = []
        scale_notes = self.SCALES[self.current_scale]
        
        # Choose melody style for this phrase
        melody_style = self._choose_melody_style(start_measure)
        
        current_time = start_time
        
        for measure in range(start_measure, end_measure):
            measure_time = start_time + (measure - start_measure) * 4 * beat_duration
            
            if melody_style == "melodic_line":
                measure_events = self._create_melodic_line(scale_notes, measure_time, beat_duration)
            elif melody_style == "staccato_stabs":
                measure_events = self._create_staccato_stabs(scale_notes, measure_time, beat_duration)
            elif melody_style == "sustained_notes":
                measure_events = self._create_sustained_notes(scale_notes, measure_time, beat_duration)
            elif melody_style == "rapid_sequence":
                measure_events = self._create_rapid_sequence(scale_notes, measure_time, beat_duration)
            else:
                measure_events = []
            
            events.extend(measure_events)
        
        return events
    
    def _choose_melody_style(self, phrase_start: int) -> str:
        """Choose melody style based on track progression."""
        styles = ["melodic_line", "staccato_stabs", "sustained_notes", "rapid_sequence"]
        
        # Weight styles based on track position
        if phrase_start < 32:  # Intro
            weights = [0.4, 0.3, 0.3, 0.0]
        elif phrase_start < 96:  # Main section
            weights = [0.3, 0.3, 0.2, 0.2]
        else:  # Outro/breakdown
            weights = [0.5, 0.2, 0.3, 0.0]
        
        return random.choices(styles, weights=weights)[0]
    
    def _create_melodic_line(self, scale_notes: List[int], start_time: float, 
                           beat_duration: float) -> List[Tuple[float, int, int]]:
        """Create flowing melodic line."""
        events = []
        
        # Choose rhythm pattern
        rhythms = [
            [0, 0.5, 1.5, 2.5, 3],      # Syncopated
            [0, 1, 2, 3],               # On the beat
            [0.5, 1, 2.5, 3.5],         # Off-beat
        ]
        rhythm = random.choice(rhythms)
        
        # Generate melodic contour
        current_note_idx = random.randint(2, len(scale_notes) - 3)
        
        for i, beat_offset in enumerate(rhythm):
            if random.random() < 0.8:  # 80% chance for each note
                note_time = start_time + beat_offset * beat_duration
                
                # Melodic movement (small intervals mostly)
                if i > 0:
                    movement = random.choices([-2, -1, 0, 1, 2], weights=[0.1, 0.3, 0.2, 0.3, 0.1])[0]
                    current_note_idx = max(0, min(len(scale_notes) - 1, current_note_idx + movement))
                
                note = scale_notes[current_note_idx]
                base_velocity = random.randint(95, 125)
                
                if self.song_structure:
                    measure = int(note_time // (4 * beat_duration))
                    velocity = self.song_structure.get_velocity_curve(measure, base_velocity)
                else:
                    velocity = base_velocity
                
                events.append((note_time, note, velocity))
        
        return events
    
    def _create_staccato_stabs(self, scale_notes: List[int], start_time: float,
                             beat_duration: float) -> List[Tuple[float, int, int]]:
        """Create staccato stab pattern."""
        events = []
        
        # Sharp, rhythmic stabs
        stab_positions = [0.75, 2.25, 3.5]  # Syncopated positions
        
        for pos in stab_positions:
            if random.random() < 0.7:  # 70% chance for each stab
                note_time = start_time + pos * beat_duration
                note = random.choice(scale_notes[3:7])  # Mid-range notes
                velocity = random.randint(105, 127)
                events.append((note_time, note, velocity))
        
        return events
    
    def _create_sustained_notes(self, scale_notes: List[int], start_time: float,
                              beat_duration: float) -> List[Tuple[float, int, int]]:
        """Create sustained note pattern."""
        events = []
        
        # Long sustained notes
        if random.random() < 0.6:  # 60% chance for sustained note
            note = random.choice(scale_notes[4:8])  # Upper mid-range
            velocity = random.randint(75, 100)
            events.append((start_time, note, velocity))
        
        # Possible harmony note
        if random.random() < 0.3:  # 30% chance for harmony
            harmony_note = random.choice(scale_notes[6:])  # Higher notes
            velocity = random.randint(55, 80)
            events.append((start_time + beat_duration, harmony_note, velocity))
        
        return events
    
    def _create_rapid_sequence(self, scale_notes: List[int], start_time: float,
                             beat_duration: float) -> List[Tuple[float, int, int]]:
        """Create rapid sequence pattern."""
        events = []
        
        # 16th note sequences
        sixteenth_duration = beat_duration / 4
        
        # Choose sequence type
        if random.random() < 0.5:
            # Ascending run
            start_idx = random.randint(0, len(scale_notes) - 6)
            sequence_notes = scale_notes[start_idx:start_idx + 6]
        else:
            # Descending run  
            start_idx = random.randint(5, len(scale_notes) - 1)
            sequence_notes = scale_notes[start_idx-5:start_idx + 1]
            sequence_notes.reverse()
        
        # Place sequence in measure
        sequence_start = random.choice([0, 2]) * beat_duration  # Start on beat 1 or 3
        
        for i, note in enumerate(sequence_notes):
            note_time = start_time + sequence_start + i * sixteenth_duration
            velocity = random.randint(85, 110)
            events.append((note_time, note, velocity))
        
        return events