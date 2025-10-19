#!/usr/bin/env python3
"""Create a simple test MIDI file with basic instruments."""

import mido
from pathlib import Path

def create_test_midi():
    # Create a new MIDI file
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Set tempo
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))
    
    # Use piano (program 0)
    track.append(mido.Message('program_change', channel=0, program=0))
    
    # Play a simple melody
    notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C major scale
    
    for note in notes:
        track.append(mido.Message('note_on', channel=0, note=note, velocity=80, time=0))
        track.append(mido.Message('note_off', channel=0, note=note, velocity=80, time=240))  # Quarter note
    
    # End of track
    track.append(mido.MetaMessage('end_of_track', time=0))
    
    # Save file
    filename = "test_simple.mid"
    mid.save(filename)
    print(f"✅ Created test MIDI file: {filename}")
    
    return Path(filename)

if __name__ == "__main__":
    midi_file = create_test_midi()
    
    # Test playback
    import subprocess
    import time
    
    print(f"🎵 Playing test file...")
    try:
        process = subprocess.Popen(['timidity', str(midi_file)])
        time.sleep(5)
        process.terminate()
        print("✅ Test playback completed")
    except Exception as e:
        print(f"❌ Playback error: {e}")