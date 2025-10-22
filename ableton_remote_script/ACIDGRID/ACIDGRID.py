"""
Main ACIDGRID Remote Script class for Ableton Live integration.
"""

from __future__ import absolute_import, print_function, unicode_literals
import Live
from .ClipCreator import ClipCreator
from .config import (
    STYLES,
    MIDI_MAPPING,
    TRACK_MAPPING,
    GENERATION_MODE_MAPPING,
    TRACK_NAMES,
    MEASURE_MAPPING
)


class ACIDGRID:
    """Main Remote Script class for ACIDGRID integration."""

    def __init__(self, c_instance):
        """Initialize ACIDGRID Remote Script.

        Args:
            c_instance: Ableton Live C++ instance (ControlSurface)
        """
        self.c_instance = c_instance
        self.song = c_instance.song()
        self.clip_creator = ClipCreator(self.song)

        # State
        self.current_style = "techno"
        self.measures = 32

        # Log initialization
        self.log_message("ACIDGRID Remote Script loaded!")
        self.log_message(f"Available styles: {', '.join(STYLES.keys())}")

        # Setup MIDI listeners
        self._setup_midi_listeners()

    def log_message(self, message):
        """Log message to Ableton's Log.txt."""
        self.c_instance.log_message(f"[ACIDGRID] {message}")

    def _setup_midi_listeners(self):
        """Setup MIDI note listeners for style selection."""
        # Listen to MIDI notes for style triggers
        self.c_instance.set_feedback_channels([0])  # Channel 1

    def disconnect(self):
        """Called when script is unloaded."""
        self.log_message("ACIDGRID Remote Script unloaded")

    def build_midi_map(self, midi_map_handle):
        """Build MIDI mapping for controllers.

        Args:
            midi_map_handle: Ableton's MIDI map handle
        """
        # Map MIDI notes to style selection
        script_handle = self.c_instance.handle()

        for style_name, note_config in MIDI_MAPPING.items():
            if style_name in STYLES:
                note = note_config["note"]
                channel = note_config["channel"]

                # Map note to generate action
                Live.MidiMap.map_midi_note(
                    midi_map_handle,
                    script_handle,
                    channel,
                    note,
                    Live.MidiMap.NoteType.NOTE_TYPE_IMMEDIATE
                )

    def receive_midi(self, midi_bytes):
        """Receive MIDI from controllers.

        Args:
            midi_bytes: Tuple of (status, data1, data2)
        """
        status, note, velocity = midi_bytes

        if velocity == 0:  # Note OFF
            return

        # Check if it's a Note ON message (0x90 + channel)
        if status >= 0x90 and status <= 0x9F:
            channel = status - 0x90

            # Check for full track generation (A5)
            if note == GENERATION_MODE_MAPPING["full_track"]["note"] and \
               channel == GENERATION_MODE_MAPPING["full_track"]["channel"]:
                self.generate_full_track()
                return

            # Check for measure preset selection (C5-E5)
            if note in MEASURE_MAPPING["note"] and channel == MEASURE_MAPPING["channel"]:
                self.set_measures(MEASURE_MAPPING["note"][note])
                return

            # Check for individual track generation (C3-E3)
            for track_type, note_config in TRACK_MAPPING.items():
                if note_config["note"] == note and note_config["channel"] == channel:
                    self.generate_single_track(track_type)
                    return

            # Check for style selection (C4-A4)
            for style_name, note_config in MIDI_MAPPING.items():
                if note_config["note"] == note and note_config["channel"] == channel:
                    self.generate_clip(style_name)
                    return

    def generate_clip(self, style=None):
        """Generate ACIDGRID clip in selected clip slot.

        Args:
            style: Music style (default: current_style)
        """
        if style is None:
            style = self.current_style
        else:
            self.current_style = style

        self.log_message(f"Generating {style} clip ({self.measures} measures)...")

        try:
            # Get selected track and clip slot
            selected_track = self.song.view.selected_track

            if not selected_track:
                self.log_message("ERROR: No track selected")
                return

            # Find first empty clip slot
            clip_slot = None
            for i, cs in enumerate(selected_track.clip_slots):
                if not cs.has_clip:
                    clip_slot = cs
                    break

            if not clip_slot:
                self.log_message("ERROR: No empty clip slots available")
                return

            # Create clip
            clip_slot.create_clip(self.measures * 4.0)  # 4 beats per measure
            clip = clip_slot.clip

            # Generate MIDI content
            self.clip_creator.generate_acidgrid_clip(
                clip=clip,
                style=style,
                measures=self.measures,
                tempo=self.song.tempo
            )

            # Set clip name
            clip.name = f"ACIDGRID - {style.upper()}"

            # Set clip color based on style
            clip.color = STYLES[style]["color"]

            self.log_message(f"✓ Generated {style} clip!")

            # Show success message in status bar
            self.c_instance.show_message(f"ACIDGRID: {style.upper()} generated!")

        except Exception as e:
            self.log_message(f"ERROR generating clip: {str(e)}")
            self.c_instance.show_message(f"ACIDGRID Error: {str(e)}")

    def set_measures(self, measures):
        """Set clip length in measures.

        Args:
            measures: Number of measures (16, 32, 64, 128, 192)
        """
        self.measures = measures
        self.log_message(f"Clip length set to {measures} measures")
        self.c_instance.show_message(f"ACIDGRID: {measures} measures")

    def generate_full_track(self):
        """Generate all 5 tracks on separate Ableton tracks.

        Creates 5 clips on 5 consecutive tracks:
        1. Rhythm (drums)
        2. Bassline
        3. Sub Bass
        4. Synth Accompaniment
        5. Synth Lead
        """
        self.log_message(f"Generating full track: {self.current_style} ({self.measures} measures)")

        try:
            # Get all tracks
            tracks = list(self.song.tracks)

            # Find selected track index
            selected_track = self.song.view.selected_track
            if selected_track not in tracks:
                self.log_message("ERROR: Please select a valid track")
                self.c_instance.show_message("ACIDGRID: Select a valid track")
                return

            selected_index = tracks.index(selected_track)

            # Track types to generate
            track_types = ['rhythm', 'bassline', 'sub_bass', 'synth_accomp', 'synth_lead']

            generated_count = 0

            # Generate on 5 consecutive tracks
            for i, track_type in enumerate(track_types):
                track_index = selected_index + i

                if track_index >= len(tracks):
                    self.log_message(f"Warning: Not enough tracks. Stopped at {track_type}")
                    break

                track = tracks[track_index]

                # Find first empty clip slot
                clip_slot = None
                for cs in track.clip_slots:
                    if not cs.has_clip:
                        clip_slot = cs
                        break

                if not clip_slot:
                    self.log_message(f"Warning: No empty clip slot on track {track_index + 1}")
                    continue

                # Create and generate clip
                clip_slot.create_clip(self.measures * 4.0)
                clip = clip_slot.clip

                # Generate content for specific track
                self.clip_creator.generate_acidgrid_clip(
                    clip=clip,
                    style=self.current_style,
                    measures=self.measures,
                    tempo=self.song.tempo,
                    track_type=track_type
                )

                # Set clip name and color
                clip.name = f"{TRACK_NAMES[track_type]} - {self.current_style.upper()}"
                clip.color = STYLES[self.current_style]["color"]

                # Set track name if it's generic
                if track.name.startswith("MIDI") or track.name.startswith(str(track_index + 1)):
                    track.name = TRACK_NAMES[track_type]

                generated_count += 1
                self.log_message(f"✓ Generated {track_type} on track {track_index + 1}")

            self.log_message(f"✓ Full track generation complete! ({generated_count} tracks)")
            self.c_instance.show_message(f"ACIDGRID: {generated_count} tracks generated!")

        except Exception as e:
            self.log_message(f"ERROR generating full track: {str(e)}")
            self.c_instance.show_message(f"ACIDGRID Error: {str(e)}")

    def generate_single_track(self, track_type):
        """Generate a single track type on the selected track.

        Args:
            track_type: Type of track to generate
                       ('rhythm', 'bassline', 'sub_bass', 'synth_accomp', 'synth_lead')
        """
        self.log_message(f"Generating {track_type} track: {self.current_style} ({self.measures} measures)")

        try:
            # Get selected track
            selected_track = self.song.view.selected_track

            if not selected_track:
                self.log_message("ERROR: No track selected")
                self.c_instance.show_message("ACIDGRID: Select a track first")
                return

            # Find first empty clip slot
            clip_slot = None
            for cs in selected_track.clip_slots:
                if not cs.has_clip:
                    clip_slot = cs
                    break

            if not clip_slot:
                self.log_message("ERROR: No empty clip slots available")
                self.c_instance.show_message("ACIDGRID: No empty clip slots")
                return

            # Create clip
            clip_slot.create_clip(self.measures * 4.0)
            clip = clip_slot.clip

            # Generate content for specific track
            self.clip_creator.generate_acidgrid_clip(
                clip=clip,
                style=self.current_style,
                measures=self.measures,
                tempo=self.song.tempo,
                track_type=track_type
            )

            # Set clip name and color
            clip.name = f"{TRACK_NAMES[track_type]} - {self.current_style.upper()}"
            clip.color = STYLES[self.current_style]["color"]

            # Set track name if it's generic
            if selected_track.name.startswith("MIDI") or selected_track.name.isdigit():
                selected_track.name = TRACK_NAMES[track_type]

            self.log_message(f"✓ Generated {track_type} track!")
            self.c_instance.show_message(f"ACIDGRID: {TRACK_NAMES[track_type]} generated!")

        except Exception as e:
            self.log_message(f"ERROR generating {track_type} track: {str(e)}")
            self.c_instance.show_message(f"ACIDGRID Error: {str(e)}")

    def update_display(self):
        """Called periodically by Ableton for display updates."""
        pass

    def refresh_state(self):
        """Called when script needs to refresh its state."""
        pass
