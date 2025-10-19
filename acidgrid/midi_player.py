"""MIDI player for track preview."""

import time
import threading
from pathlib import Path
from typing import Optional
import mido
import sys


class MidiPlayer:
    """Simple MIDI player for previewing generated tracks."""
    
    def __init__(self):
        self.port = None
        self.playing = False
        self.stop_event = threading.Event()
        
    def get_output_port(self) -> Optional[mido.ports.BaseOutput]:
        """Get available MIDI output port."""
        try:
            # Try to find a software synthesizer first
            port_names = mido.get_output_names()
            
            # Preferred ports (software synths)
            preferred = ['FluidSynth', 'TiMidity', 'Microsoft GS Wavetable Synth', 
                        'MIDI Through', 'IAC Driver', 'loopMIDI']
            
            for pref in preferred:
                for port_name in port_names:
                    if pref.lower() in port_name.lower():
                        return mido.open_output(port_name)
            
            # If no preferred port found, use the first available
            if port_names:
                print(f"Using MIDI port: {port_names[0]}")
                return mido.open_output(port_names[0])
            
            # Try to open virtual port as last resort
            return mido.open_output('rndTek Preview', virtual=True)
            
        except Exception as e:
            print(f"⚠ Could not open MIDI port: {e}")
            return None
    
    def play(self, midi_file: Path, duration: int = 30):
        """
        Play MIDI file for preview.
        
        Args:
            midi_file: Path to MIDI file
            duration: Maximum playback duration in seconds (default 30s for preview)
        """
        try:
            # Try multiple playback methods in order of preference
            
            # 1. Try system MIDI players first (most reliable)
            try:
                from .system_player import play_with_system_player
                if play_with_system_player(midi_file, duration):
                    return
            except Exception as e:
                pass
            
            # 2. Try pygame (good compatibility but TiMidity issues)
            try:
                from .pygame_player import play_with_pygame
                if play_with_pygame(midi_file, duration):
                    return
            except Exception as e:
                if "timidity" not in str(e).lower():
                    pass  # Only ignore TiMidity errors
            
            # Fallback to MIDI port method
            # Load MIDI file
            mid = mido.MidiFile(str(midi_file))
            
            # Get output port
            self.port = self.get_output_port()
            if not self.port:
                print("⚠ All MIDI playback methods failed.")
                
                # Show OS-specific install instructions
                from .os_detection import print_install_instructions
                print_install_instructions()
                
                print(f"\n🎛️ **Alternative: Use with DAW**")
                print(f"   Import the MIDI file: {midi_file}")
                return
            
            print(f"\n▶ Playing preview: {midi_file.name}")
            print(f"  Duration: {duration}s (Press Ctrl+C to stop)")
            print("  " + "=" * 40)
            
            # Start playback in thread
            self.playing = True
            self.stop_event.clear()
            
            playback_thread = threading.Thread(
                target=self._playback_loop,
                args=(mid, duration)
            )
            playback_thread.daemon = True
            playback_thread.start()
            
            # Show progress
            self._show_progress(duration)
            
            # Wait for playback to finish
            playback_thread.join(timeout=duration + 1)
            
        except KeyboardInterrupt:
            print("\n⏹ Playback stopped")
        except Exception as e:
            print(f"⚠ Playback error: {e}")
        finally:
            self.stop()
    
    def _playback_loop(self, mid: mido.MidiFile, max_duration: float):
        """Main playback loop."""
        start_time = time.time()
        
        try:
            for msg in mid.play():
                if self.stop_event.is_set():
                    break
                
                if not msg.is_meta and self.port:
                    self.port.send(msg)
                
                # Check duration limit
                if time.time() - start_time > max_duration:
                    break
                    
        except Exception as e:
            print(f"\n⚠ Playback error: {e}")
        finally:
            # Send all notes off
            if self.port:
                for channel in range(16):
                    self.port.send(mido.Message('control_change', 
                                               channel=channel, 
                                               control=123, 
                                               value=0))
    
    def _show_progress(self, duration: int):
        """Show playback progress bar."""
        try:
            for i in range(duration):
                if self.stop_event.is_set():
                    break
                
                # Calculate progress
                progress = (i + 1) / duration
                bar_length = 40
                filled = int(bar_length * progress)
                bar = "█" * filled + "░" * (bar_length - filled)
                
                # Print progress bar
                sys.stdout.write(f"\r  [{bar}] {i+1}/{duration}s")
                sys.stdout.flush()
                
                time.sleep(1)
            
            print()  # New line after progress
            
        except KeyboardInterrupt:
            self.stop_event.set()
            raise
    
    def stop(self):
        """Stop playback."""
        self.playing = False
        self.stop_event.set()
        
        if self.port:
            # Send all notes off on all channels
            for channel in range(16):
                try:
                    self.port.send(mido.Message('control_change', 
                                               channel=channel, 
                                               control=123, 
                                               value=0))
                except:
                    pass
            
            # Close port
            try:
                self.port.close()
            except:
                pass
            
            self.port = None


def check_synth_available() -> bool:
    """Check if a software synthesizer is available."""
    try:
        import subprocess
        
        # Check for common software synths
        synths = ['fluidsynth', 'timidity']
        
        for synth in synths:
            try:
                result = subprocess.run(['which', synth], 
                                      capture_output=True, 
                                      text=True,
                                      timeout=1)
                if result.returncode == 0:
                    return True
            except:
                pass
        
        # Check if we have MIDI ports available
        port_names = mido.get_output_names()
        return len(port_names) > 0
        
    except:
        return False


def install_synth_instructions():
    """Print instructions for installing a software synthesizer."""
    from .os_detection import print_install_instructions
    print_install_instructions()