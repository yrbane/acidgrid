"""
Clip Creator module - Generates MIDI content directly in Ableton Live clips.
"""

from __future__ import absolute_import, print_function, unicode_literals
import sys
import os

# Import ACIDGRID generators
# Add parent directory to path to import acidgrid package
script_dir = os.path.dirname(os.path.abspath(__file__))
acidgrid_root = os.path.join(script_dir, '..', '..', '..')
sys.path.insert(0, acidgrid_root)

try:
    from acidgrid.generators import (
        RhythmGenerator,
        BasslineGenerator,
        SubBassGenerator,
        SynthAccompanimentGenerator,
        SynthLeadGenerator
    )
    from acidgrid.music_styles import get_style
    from acidgrid.song_structure import SongStructure
except ImportError as e:
    # Fallback if import fails
    RhythmGenerator = None
    print(f"[ACIDGRID] Warning: Could not import generators: {e}")


class ClipCreator:
    """Creates MIDI clips with ACIDGRID content."""

    def __init__(self, song):
        """Initialize ClipCreator.

        Args:
            song: Ableton Live Song object
        """
        self.song = song

    def generate_acidgrid_clip(self, clip, style, measures, tempo, track_type=None):
        """Generate ACIDGRID content in an Ableton Live clip.

        Args:
            clip: Ableton Live Clip object
            style: Music style name (str)
            measures: Number of measures
            tempo: Tempo in BPM
            track_type: Specific track to generate (None = all tracks mixed)
                       Options: 'rhythm', 'bassline', 'sub_bass', 'synth_accomp', 'synth_lead'
        """
        # Get style configuration
        style_config = get_style(style)

        # Create song structure
        song_structure = SongStructure(measures, style=style_config)

        # Generate specific track or all tracks
        if track_type == 'rhythm':
            rhythm_gen = RhythmGenerator(song_structure, style=style_config)
            rhythm_events = rhythm_gen.generate(measures, tempo)
            self._add_events_to_clip(clip, rhythm_events, is_drums=True)

        elif track_type == 'bassline':
            bassline_gen = BasslineGenerator(song_structure, style=style_config)
            bassline_events = bassline_gen.generate(measures, tempo)
            self._add_events_to_clip(clip, bassline_events, is_drums=False)

        elif track_type == 'sub_bass':
            sub_bass_gen = SubBassGenerator(song_structure, style=style_config)
            sub_bass_events = sub_bass_gen.generate(measures, tempo)
            self._add_events_to_clip(clip, sub_bass_events, is_drums=False)

        elif track_type == 'synth_accomp':
            synth_accomp_gen = SynthAccompanimentGenerator(song_structure, style=style_config)
            synth_accomp_events = synth_accomp_gen.generate(measures, tempo)
            self._add_events_to_clip(clip, synth_accomp_events, is_drums=False)

        elif track_type == 'synth_lead':
            synth_lead_gen = SynthLeadGenerator(song_structure, style=style_config)
            synth_lead_events = synth_lead_gen.generate(measures, tempo)
            self._add_events_to_clip(clip, synth_lead_events, is_drums=False)

        else:
            # Generate all tracks mixed (legacy mode)
            rhythm_gen = RhythmGenerator(song_structure, style=style_config)
            bassline_gen = BasslineGenerator(song_structure, style=style_config)
            sub_bass_gen = SubBassGenerator(song_structure, style=style_config)
            synth_accomp_gen = SynthAccompanimentGenerator(song_structure, style=style_config)
            synth_lead_gen = SynthLeadGenerator(song_structure, style=style_config)

            # Generate events
            rhythm_events = rhythm_gen.generate(measures, tempo)
            bassline_events = bassline_gen.generate(measures, tempo)
            sub_bass_events = sub_bass_gen.generate(measures, tempo)
            synth_accomp_events = synth_accomp_gen.generate(measures, tempo)
            synth_lead_events = synth_lead_gen.generate(measures, tempo)

            # Add all tracks
            self._add_events_to_clip(clip, rhythm_events, is_drums=True)
            self._add_events_to_clip(clip, bassline_events, is_drums=False)
            self._add_events_to_clip(clip, sub_bass_events, is_drums=False)
            self._add_events_to_clip(clip, synth_accomp_events, is_drums=False)
            self._add_events_to_clip(clip, synth_lead_events, is_drums=False)

    def _add_events_to_clip(self, clip, events, is_drums=False):
        """Add MIDI events to Ableton clip.

        Args:
            clip: Ableton Live Clip object
            events: List of (time, note, velocity) tuples
            is_drums: Whether these are drum events
        """
        if not events:
            return

        # Get clip length in beats
        clip_length = clip.length

        # Group events into note on/off pairs
        note_data = []
        active_notes = {}  # {(note, channel): start_time}

        for time, note, velocity in sorted(events, key=lambda x: x[0]):
            # Convert time from seconds to beats
            beat_time = self._time_to_beats(time, self.song.tempo)

            if beat_time >= clip_length:
                continue

            if velocity > 0:  # Note ON
                # Store note start time
                key = (note, 0)  # Channel 0 for now
                active_notes[key] = beat_time
            else:  # Note OFF (velocity == 0)
                # Find matching note ON and create note
                key = (note, 0)
                if key in active_notes:
                    start_time = active_notes[key]
                    duration = beat_time - start_time

                    # Ensure minimum duration
                    if duration < 0.1:
                        duration = 0.1

                    # Create note: (pitch, start_time, duration, velocity, muted)
                    # Use velocity from original note ON event
                    note_data.append((note, start_time, duration, 100, False))

                    del active_notes[key]

        # Add notes to clip
        if note_data:
            try:
                # Clear existing notes first
                clip.remove_notes(0, 0, clip_length, 128)

                # Add all notes at once
                clip.add_new_notes(tuple(note_data))
            except Exception as e:
                print(f"[ACIDGRID] Error adding notes to clip: {e}")

    def _time_to_beats(self, time_seconds, tempo):
        """Convert time in seconds to beats.

        Args:
            time_seconds: Time in seconds
            tempo: Tempo in BPM

        Returns:
            Time in beats
        """
        # beats = (time_seconds * tempo) / 60
        return (time_seconds * tempo) / 60.0

    def _get_clip_notes(self, clip):
        """Get all notes from a clip.

        Args:
            clip: Ableton Live Clip object

        Returns:
            Tuple of note data
        """
        try:
            notes = clip.get_notes(0, 0, clip.length, 128)
            return notes
        except Exception as e:
            print(f"[ACIDGRID] Error getting clip notes: {e}")
            return tuple()
