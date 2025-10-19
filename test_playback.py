#!/usr/bin/env python3
"""Quick test of MIDI playback with current audio setup."""

import subprocess
import time
from pathlib import Path

def test_midi_playback():
    midi_file = Path("Pure Fucking Chaos.mid")
    
    if not midi_file.exists():
        print("❌ MIDI file not found")
        return
    
    print(f"🎵 Testing playback of: {midi_file}")
    
    # Test with aplaymidi (ALSA sequencer player)
    try:
        print("▶ Trying aplaymidi...")
        result = subprocess.run(['aplaymidi', '-p', '128:0', str(midi_file)], 
                               capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ aplaymidi worked!")
            return True
    except Exception as e:
        print(f"❌ aplaymidi failed: {e}")
    
    # Test with timidity direct playback
    try:
        print("▶ Trying timidity direct...")
        process = subprocess.Popen(['timidity', str(midi_file)], 
                                  stdout=subprocess.DEVNULL, 
                                  stderr=subprocess.DEVNULL)
        time.sleep(5)
        process.terminate()
        print("✅ timidity direct worked!")
        return True
    except Exception as e:
        print(f"❌ timidity direct failed: {e}")
    
    print("❌ All playback methods failed")
    return False

if __name__ == "__main__":
    test_midi_playback()