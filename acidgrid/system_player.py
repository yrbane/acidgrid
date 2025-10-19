"""System-based MIDI player using available system tools."""

import subprocess
import time
import threading
import signal
import sys
from pathlib import Path
from typing import Optional


def find_system_player() -> Optional[str]:
    """Find available system MIDI player."""
    players = [
        ('timidity', ['-c', '/home/seb/.config/timidity/timidity.cfg']),  # TiMidity with soundfont
        ('aplaymidi', ['-p', '128:0']),  # ALSA sequencer
        ('pmidi', ['-p', '128:0']),  # Another ALSA player
        ('fluidsynth', ['-a', 'pulse', '-i']),  # FluidSynth
        ('wildmidi', []),  # WildMIDI
    ]
    
    for player, default_args in players:
        try:
            result = subprocess.run(['which', player], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=1)
            if result.returncode == 0:
                return player, default_args
        except:
            continue
    
    return None


def play_with_system_player(midi_file: Path, duration: int = 30) -> bool:
    """Play MIDI file using system player."""
    player_info = find_system_player()
    if not player_info:
        return False
    
    player, default_args = player_info
    
    try:
        print(f"\n▶ Playing preview: {midi_file.name}")
        print(f"  Player: {player}")
        print(f"  Duration: {duration}s (Press Ctrl+C to stop)")
        print("  " + "=" * 40)
        
        # Start the player process
        cmd = [player] + default_args + [str(midi_file)]
        process = subprocess.Popen(cmd, 
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL)
        
        # Show progress and manage playback
        start_time = time.time()
        
        try:
            while process.poll() is None and (time.time() - start_time) < duration:
                elapsed = int(time.time() - start_time)
                progress = elapsed / duration
                bar_length = 40
                filled = int(bar_length * progress)
                bar = "█" * filled + "░" * (bar_length - filled)
                
                print(f"\r  [{bar}] {elapsed}/{duration}s", end="", flush=True)
                time.sleep(0.1)
            
            print()  # New line after progress
            
        except KeyboardInterrupt:
            print("\n⏹ Playback stopped")
        
        # Clean up process
        try:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=1)
        except:
            try:
                process.kill()
            except:
                pass
        
        return True
        
    except Exception as e:
        print(f"⚠ System player error: {e}")
        return False


def install_system_player_instructions():
    """Show instructions for installing system MIDI players."""
    print("\n" + "🎹 SYSTEM MIDI PLAYER SETUP" + "\n" + "=" * 40)
    
    print("\nInstall a system MIDI player:")
    print("\n**Ubuntu/Debian:**")
    print("  sudo apt install timidity timidity-interfaces-extra")
    print("  # OR")
    print("  sudo apt install fluidsynth fluid-soundfont-gm")
    
    print("\n**Arch Linux:**")
    print("  sudo pacman -S timidity++ soundfont-fluid")
    print("  # OR") 
    print("  sudo pacman -S fluidsynth soundfont-fluid")
    
    print("\n**MacOS:**")
    print("  brew install timidity")
    print("  # OR")
    print("  brew install fluidsynth")
    
    print("\n**After installation, start the MIDI daemon:**")
    print("  timidity -iA -Os  # TiMidity daemon mode")
    print("  # OR")
    print("  fluidsynth -a alsa -m alsa_seq -l -i /path/to/soundfont.sf2")
    
    print("\n" + "=" * 40)