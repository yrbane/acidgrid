"""MIDI file output functionality for rndTek."""

import mido
from typing import List, Tuple
from pathlib import Path


class MidiComposer:
    """Composes and saves MIDI files from generated track data."""
    
    def __init__(self, tempo: int = 128):
        self.tempo = tempo
        self.tracks = {}
        self.ticks_per_beat = 480  # Standard MIDI resolution
        
    def add_track(self, name: str, events: List[Tuple[float, int, int]]):
        """
        Add a track to the composition.
        
        Args:
            name: Track name
            events: List of (time_seconds, midi_note, velocity) tuples
        """
        self.tracks[name] = events
        
    def save(self, filename: Path):
        """Save the composition as a MIDI file."""
        # Create new MIDI file
        mid = mido.MidiFile()
        mid.ticks_per_beat = self.ticks_per_beat
        
        # Add tempo track
        tempo_track = mido.MidiTrack()
        mid.tracks.append(tempo_track)
        
        # Set tempo (microseconds per beat)
        microseconds_per_beat = int(60_000_000 / self.tempo)
        tempo_track.append(mido.MetaMessage('set_tempo', tempo=microseconds_per_beat, time=0))
        
        # Add each instrument track
        for track_name, events in self.tracks.items():
            midi_track = self._create_midi_track(track_name, events)
            mid.tracks.append(midi_track)
        
        # Save file
        mid.save(str(filename))
        
    def _create_midi_track(self, name: str, events: List[Tuple[float, int, int]]) -> mido.MidiTrack:
        """Convert event list to MIDI track."""
        track = mido.MidiTrack()
        
        # Add track name
        track.append(mido.MetaMessage('track_name', name=name, time=0))
        
        # Set program (instrument) based on track type
        program = self._get_program_for_track(name)
        track.append(mido.Message('program_change', program=program, time=0))
        
        # Convert events to MIDI messages
        if not events:
            return track
            
        # Sort events by time
        sorted_events = sorted(events, key=lambda x: x[0])
        
        # Group simultaneous note-ons and create note-offs
        midi_events = self._create_midi_events(sorted_events)
        
        # Convert to MIDI messages with proper timing
        current_time_ticks = 0
        
        for event_time, event_type, note, velocity in midi_events:
            # Convert time to ticks
            event_time_ticks = int(event_time * self.ticks_per_beat * self.tempo / 60)
            delta_time = max(0, event_time_ticks - current_time_ticks)

            if event_type == 'note_on':
                track.append(mido.Message('note_on', note=note, velocity=velocity, time=delta_time))
            elif event_type == 'note_off':
                # Use calculated release velocity for natural sound
                track.append(mido.Message('note_off', note=note, velocity=velocity, time=delta_time))

            current_time_ticks = event_time_ticks
            
        return track
        
    def _get_program_for_track(self, track_name: str) -> int:
        """Get MIDI program number for track type."""
        programs = {
            "Rhythm": 0,           # Acoustic Grand Piano (will be drums on channel 10)
            "Bassline": 38,        # Synth Bass 1
            "Synth Accompaniment": 90,  # Pad 3 (polysynth) - plus doux
            "Synth Lead": 81,      # Saw Lead
        }
        return programs.get(track_name, 0)
        
    def _create_midi_events(self, events: List[Tuple[float, int, int]]) -> List[Tuple[float, str, int, int]]:
        """Create note_on and note_off events with proper timing and natural release velocity."""
        midi_events = []

        # Default note length based on track context
        default_note_length = 0.1  # Short notes for most sounds

        for time, note, velocity in events:
            # Note on
            midi_events.append((time, 'note_on', note, velocity))

            # Note off - calculate appropriate length and release velocity
            note_length = self._calculate_note_length(note, velocity)
            release_velocity = self._calculate_release_velocity(velocity, note_length)
            midi_events.append((time + note_length, 'note_off', note, release_velocity))

        # Sort by time
        midi_events.sort(key=lambda x: x[0])
        return midi_events
        
    def _calculate_note_length(self, note: int, velocity: int) -> float:
        """Calculate appropriate note length based on note and velocity."""
        # Drum sounds (lower notes) - shorter
        if note < 50:
            return 0.05 + (velocity / 127.0) * 0.1

        # Bass notes - medium length
        elif note < 60:
            return 0.2 + (velocity / 127.0) * 0.3

        # Higher notes - can be longer
        else:
            return 0.1 + (velocity / 127.0) * 0.4

    def _calculate_release_velocity(self, attack_velocity: int, note_length: float) -> int:
        """Calculate natural release velocity for note off events.

        Args:
            attack_velocity: Original note on velocity
            note_length: Duration of the note in seconds

        Returns:
            Release velocity (40-80 for natural sound, 0 for very short notes)
        """
        # Very short notes (< 0.1s) - use traditional 0 velocity
        if note_length < 0.1:
            return 0

        # Short notes (0.1-0.3s) - gentle release
        elif note_length < 0.3:
            # Scale from 40-60 based on attack velocity
            return int(40 + (attack_velocity / 127.0) * 20)

        # Medium notes (0.3-0.6s) - moderate release
        elif note_length < 0.6:
            # Scale from 50-70 based on attack velocity
            return int(50 + (attack_velocity / 127.0) * 20)

        # Long notes (>= 0.6s) - fuller release
        else:
            # Scale from 60-80 based on attack velocity
            return int(60 + (attack_velocity / 127.0) * 20)


class DrumMidiComposer(MidiComposer):
    """Specialized MIDI composer for drum tracks."""
    
    def _create_midi_track(self, name: str, events: List[Tuple[float, int, int]]) -> mido.MidiTrack:
        """Create drum track on channel 10 (MIDI channel 9, 0-indexed)."""
        track = mido.MidiTrack()
        
        # Add track name
        track.append(mido.MetaMessage('track_name', name=name, time=0))
        
        # Convert events to MIDI messages
        if not events:
            return track
            
        # Sort events by time
        sorted_events = sorted(events, key=lambda x: x[0])
        
        current_time_ticks = 0
        
        for event_time, note, velocity in sorted_events:
            # Convert time to ticks
            event_time_ticks = int(event_time * self.ticks_per_beat * self.tempo / 60)
            delta_time = max(0, event_time_ticks - current_time_ticks)
            
            # Note on (channel 9 for drums)
            track.append(mido.Message('note_on', channel=9, note=note, velocity=velocity, time=delta_time))
            
            # Short note off for drums
            track.append(mido.Message('note_off', channel=9, note=note, velocity=0, time=5))
                
            current_time_ticks = event_time_ticks + 5
            
        return track