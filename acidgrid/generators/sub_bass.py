"""Sub-bass generator for deep, long fundamental notes with harmonic coherence."""

import random
from typing import List, Tuple, Dict
from ..time_signature import TimeSignature, COMMON_TIME_SIGNATURES


class SubBassGenerator:
    """Generates sub-bass tracks with long, deep fundamental notes harmonically coherent with other instruments."""

    def __init__(self, song_structure=None, style=None, time_signature=None):
        self.song_structure = song_structure
        self.style = style
        self.time_signature = time_signature or COMMON_TIME_SIGNATURES["4/4"]

    def _get_root_note(self, context: Dict) -> int:
        """Get root note (sub-bass range) based on harmonic context."""
        key_roots = {
            "A_minor": 21,  # A0 - very low
            "D_minor": 26,  # D1
            "E_minor": 28,  # E1
            "F_minor": 29,  # F1
            "G_minor": 31,  # G1
        }

        key = context.get("key", "A_minor")
        chord = context.get("chord", "i")

        root = key_roots.get(key, 21)

        # Adjust for chord progression (same offsets as bassline but lower register)
        chord_offsets = {
            "i": 0,
            "ii": 2,
            "III": 3,
            "iv": 5,
            "V": 7,
            "VI": 8,
            "VII": 10,
            "bVII": 10,
        }

        offset = chord_offsets.get(chord, 0)
        return root + offset

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

        # Calculate timing based on time signature
        beats_per_measure = self.time_signature.beats_per_measure
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
                context = {"key": "A_minor", "chord": "i", "intensity": 0.7}
                intensity = 0.7

            # Get root note from harmonic context
            root_note = self._get_root_note(context)
            fifth_note = root_note + 7

            # Determine sub-bass behavior based on track section
            if self._should_play_sub_bass(measure):
                pattern = self._generate_sub_bass_pattern(measure, root_note, fifth_note)

                for beat_offset, duration_beats, note, velocity in pattern:
                    note_time = current_time + beat_offset * beat_duration

                    # Apply velocity dynamics
                    if self.song_structure:
                        final_velocity = self.song_structure.get_velocity_curve(measure, velocity)
                    else:
                        final_velocity = velocity

                    # Add note with long sustain
                    events.append((note_time, note, final_velocity))

                    # Note off after duration with natural release velocity
                    # Sub-bass has long releases, use 60-80 range
                    note_off_time = note_time + duration_beats * beat_duration
                    release_velocity = int(60 + (final_velocity / 127.0) * 20)  # Scale 60-80
                    events.append((note_off_time, note, release_velocity))

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

    def _generate_sub_bass_pattern(self, measure: int, root: int, fifth: int) -> List[Tuple[float, float, int, int]]:
        """
        Generate sub-bass pattern for a measure.
        Returns list of (beat_offset, duration_beats, note, velocity).
        """
        patterns = []

        # Choose pattern style based on section
        if measure < 32:  # Intro - simple, long notes
            patterns = self._create_simple_pattern(root, fifth)
        elif measure < 128:  # Main section - more movement
            if random.random() < 0.7:
                patterns = self._create_pumping_pattern(root)
            else:
                patterns = self._create_movement_pattern(root, fifth)
        else:  # Outro/breakdown
            patterns = self._create_sparse_pattern(root)

        return patterns

    def _create_simple_pattern(self, root: int, fifth: int) -> List[Tuple[float, float, int, int]]:
        """Create simple sub-bass pattern with long notes."""
        beats = self.time_signature.beats_per_measure

        if beats == 3:
            # 3/4 patterns
            patterns = [
                [(0, 3, root, 65)],  # Full measure
                [(0, 1.5, root, 70), (1.5, 1.5, root, 60)],  # Two halves
                [(0, 2, root, 70), (2, 1, fifth, 65)],  # Root and fifth
            ]
        elif beats == 5:
            # 5/4 patterns
            patterns = [
                [(0, 5, root, 65)],  # Full measure
                [(0, 3, root, 70), (3, 2, root, 60)],  # 3+2 grouping
                [(0, 2, root, 70), (2, 3, fifth, 65)],  # 2+3 grouping
            ]
        elif beats == 7:
            # 7/4 or 7/8 patterns
            patterns = [
                [(0, 7, root, 65)],  # Full measure
                [(0, 2, root, 70), (2, 2, root, 65), (4, 3, fifth, 60)],  # 2+2+3
                [(0, 3, root, 70), (3, 2, root, 65), (5, 2, fifth, 60)],  # 3+2+2
            ]
        else:
            # 4/4 and other patterns (default)
            patterns = [
                [(0, beats, root, 65)],  # Full measure
                [(0, beats/2, root, 70), (beats/2, beats/2, root, 60)],  # Two halves
                [(0, beats*0.875, root, 65), (beats*0.9375, beats*0.0625, root, 50)],  # Sustained with variation
                [(0, beats/2, root, 70), (beats/2, beats/2, fifth, 65)],  # Root and fifth
            ]
        return random.choice(patterns)

    def _create_pumping_pattern(self, root: int) -> List[Tuple[float, float, int, int]]:
        """Create pumping sub-bass pattern (sidechain effect simulation)."""
        beats = self.time_signature.beats_per_measure

        # Create pumping on each beat
        simple_pump = [(i, 0.75, root, 75) for i in range(beats)]

        # Create varied pumping (works for any beat count)
        varied_pump = []
        for i in range(beats):
            varied_pump.append((i, 0.5, root, 85 - i * 5))
            if i < beats - 1:
                varied_pump.append((i + 0.75, 0.25, root, 45))

        # Long notes with velocity automation
        velocity_pump = [(i, 1, root, 75 - i * 5) for i in range(beats)]

        patterns = [simple_pump, varied_pump, velocity_pump]
        return random.choice(patterns)

    def _create_movement_pattern(self, root: int, fifth: int) -> List[Tuple[float, float, int, int]]:
        """Create sub-bass pattern with note movement."""
        beats = self.time_signature.beats_per_measure
        half = beats / 2

        patterns = [
            # Root to fifth movement
            [(0, half, root, 70), (half, half, fifth, 65)],

            # Alternating root and fifth
            [(i, 1, root if i % 2 == 0 else fifth, 70 - i * 2) for i in range(beats)],
        ]
        return random.choice(patterns)

    def _create_sparse_pattern(self, root: int) -> List[Tuple[float, float, int, int]]:
        """Create sparse sub-bass pattern for breakdowns."""
        patterns = [
            # Single hit
            [(0, 1, root, 60)],

            # Two sparse hits
            [(0, 0.5, root, 65), (3, 1, root, 55)],

            # Very long sustain
            [(0, 8, root, 50)],  # Extends beyond measure
        ]
        return random.choice(patterns)
