"""Sub-bass generator for deep, long fundamental notes with harmonic coherence."""

import random
from typing import List, Tuple, Dict


class SubBassGenerator:
    """Generates sub-bass tracks with long, deep fundamental notes harmonically coherent with other instruments."""

    def __init__(self, song_structure=None, style=None):
        self.song_structure = song_structure
        self.style = style

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
        patterns = [
            # Single long note per measure
            [(0, 4, root, 65)],

            # Two notes per measure
            [(0, 2, root, 70), (2, 2, root, 60)],

            # Sustained with slight variation
            [(0, 3.5, root, 65), (3.75, 0.25, root, 50)],

            # Root and fifth
            [(0, 2, root, 70), (2, 2, fifth, 65)],
        ]
        return random.choice(patterns)

    def _create_pumping_pattern(self, root: int) -> List[Tuple[float, float, int, int]]:
        """Create pumping sub-bass pattern (sidechain effect simulation)."""
        patterns = [
            # Pumping on every beat
            [
                (0, 0.75, root, 75),
                (1, 0.75, root, 75),
                (2, 0.75, root, 75),
                (3, 0.75, root, 75),
            ],

            # Pumping on kicks with variation
            [
                (0, 0.5, root, 85),
                (0.75, 0.25, root, 45),
                (1, 0.5, root, 75),
                (2, 0.5, root, 80),
                (2.75, 0.25, root, 50),
                (3, 0.5, root, 70),
            ],

            # Long note with velocity automation
            [
                (0, 1, root, 75),
                (1, 1, root, 60),
                (2, 1, root, 65),
                (3, 1, root, 55),
            ],
        ]
        return random.choice(patterns)

    def _create_movement_pattern(self, root: int, fifth: int) -> List[Tuple[float, float, int, int]]:
        """Create sub-bass pattern with note movement."""
        patterns = [
            # Root to fifth movement
            [(0, 2, root, 70), (2, 2, fifth, 65)],

            # More complex movement
            [(0, 1, root, 75), (1, 0.5, fifth, 60), (1.5, 0.5, root, 55), (2, 2, root, 70)],

            # Rhythmic pattern
            [(0, 0.5, root, 85), (0.5, 0.5, root, 50), (2, 0.5, fifth, 75), (2.5, 1.5, root, 60)],

            # Alternating root and fifth
            [(0, 1, root, 70), (1, 1, fifth, 65), (2, 1, root, 70), (3, 1, fifth, 65)],
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
