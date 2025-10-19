"""Alternative MIDI player using pygame for better compatibility."""

import time
from pathlib import Path
from typing import Optional


def play_with_pygame(midi_file: Path, duration: int = 30) -> bool:
    """
    Play MIDI file using pygame (more compatible).
    
    Args:
        midi_file: Path to MIDI file
        duration: Maximum playback duration in seconds
        
    Returns:
        True if playback was successful
    """
    try:
        import pygame
        import pygame.mixer
        import os
        
        # Suppress pygame messages temporarily
        old_stdout = os.sys.stdout
        old_stderr = os.sys.stderr
        
        try:
            # Try to silence pygame mixer init errors
            os.sys.stdout = open(os.devnull, 'w')
            os.sys.stderr = open(os.devnull, 'w')
            
            # Initialize pygame mixer with different settings to avoid TiMidity issues
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
            
        except Exception:
            # Try alternative init
            try:
                pygame.mixer.quit()
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
            except Exception:
                return False
        finally:
            # Restore stdout/stderr
            if old_stdout != os.sys.stdout:
                os.sys.stdout.close()
                os.sys.stdout = old_stdout
            if old_stderr != os.sys.stderr:
                os.sys.stderr.close()  
                os.sys.stderr = old_stderr
        
        print(f"\n▶ Playing preview: {midi_file.name}")
        print(f"  Duration: {duration}s (Press Ctrl+C to stop)")
        print("  " + "=" * 40)
        
        # Load and play the MIDI file
        pygame.mixer.music.load(str(midi_file))
        pygame.mixer.music.play()
        
        # Show progress
        start_time = time.time()
        while pygame.mixer.music.get_busy() and (time.time() - start_time) < duration:
            # Calculate progress
            elapsed = int(time.time() - start_time)
            progress = elapsed / duration
            bar_length = 40
            filled = int(bar_length * progress)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            # Print progress bar
            print(f"\r  [{bar}] {elapsed}/{duration}s", end="", flush=True)
            
            time.sleep(0.1)
        
        print()  # New line after progress
        
        # Stop playback
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        
        return True
        
    except ImportError:
        print("⚠ pygame not installed. Install with: pip install pygame")
        return False
    except KeyboardInterrupt:
        print("\n⏹ Playback stopped")
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass
        return True
    except Exception as e:
        print(f"⚠ Playback error: {e}")
        return False