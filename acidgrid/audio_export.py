"""Audio export functionality using FluidSynth for MIDI rendering."""

import subprocess
import os
from pathlib import Path
from typing import Optional
import platform


class AudioExporter:
    """Handles audio export from MIDI files using FluidSynth."""

    DEFAULT_SOUNDFONTS = {
        'linux': [
            '/usr/share/soundfonts/FluidR3_GM.sf2',
            '/usr/share/soundfonts/default.sf2',
            '/usr/share/sounds/sf2/FluidR3_GM.sf2',
            '/usr/share/sounds/sf2/default.sf2',
        ],
        'darwin': [  # macOS
            '/usr/local/share/soundfonts/FluidR3_GM.sf2',
            '/System/Library/Components/CoreAudio.component/Contents/Resources/gs_instruments.dls',
        ],
        'windows': [
            'C:\\soundfonts\\FluidR3_GM.sf2',
            'C:\\Windows\\System32\\drivers\\gm.dls',
        ]
    }

    def __init__(self, soundfont_path: Optional[str] = None):
        """
        Initialize audio exporter.

        Args:
            soundfont_path: Path to SoundFont file (.sf2). If None, tries to find system default.
        """
        self.soundfont_path = soundfont_path or self._find_default_soundfont()

    def _find_default_soundfont(self) -> Optional[str]:
        """Find default SoundFont file on the system."""
        system = platform.system().lower()

        # Get potential paths based on OS
        if 'linux' in system:
            candidates = self.DEFAULT_SOUNDFONTS['linux']
        elif 'darwin' in system:
            candidates = self.DEFAULT_SOUNDFONTS['darwin']
        elif 'win' in system:
            candidates = self.DEFAULT_SOUNDFONTS['windows']
        else:
            candidates = []

        # Find first existing soundfont
        for path in candidates:
            if os.path.exists(path):
                return path

        return None

    def check_fluidsynth_available(self) -> bool:
        """Check if FluidSynth is installed and available."""
        try:
            result = subprocess.run(
                ['fluidsynth', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def export_to_wav(self, midi_file: Path, output_file: Path,
                      sample_rate: int = 44100, gain: float = 0.5) -> bool:
        """
        Export MIDI file to WAV using FluidSynth.

        Args:
            midi_file: Path to input MIDI file
            output_file: Path to output WAV file
            sample_rate: Sample rate in Hz (default: 44100)
            gain: Master gain 0.0-10.0 (default: 0.5)

        Returns:
            True if successful, False otherwise
        """
        if not self.soundfont_path:
            print("Error: No SoundFont file found. Please specify --soundfont path.")
            return False

        if not self.check_fluidsynth_available():
            print("Error: FluidSynth is not installed.")
            self.print_install_instructions()
            return False

        try:
            # FluidSynth command for WAV rendering
            cmd = [
                'fluidsynth',
                '-ni',  # Non-interactive mode
                '-g', str(gain),  # Master gain
                '-r', str(sample_rate),  # Sample rate
                '-F', str(output_file),  # Output file
                str(self.soundfont_path),  # SoundFont
                str(midi_file)  # Input MIDI
            ]

            print(f"Rendering MIDI to WAV with FluidSynth...")
            print(f"SoundFont: {self.soundfont_path}")
            print(f"Sample rate: {sample_rate} Hz")
            print(f"Gain: {gain}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode != 0:
                print(f"FluidSynth error: {result.stderr}")
                return False

            print(f"WAV exported: {output_file}")
            return True

        except subprocess.TimeoutExpired:
            print("Error: FluidSynth rendering timed out (>5 minutes)")
            return False
        except Exception as e:
            print(f"Error during audio export: {e}")
            return False

    def export_to_format(self, midi_file: Path, output_file: Path,
                        format: str = 'wav', **kwargs) -> bool:
        """
        Export MIDI to audio in specified format.

        Args:
            midi_file: Path to input MIDI file
            output_file: Path to output audio file
            format: Audio format ('wav', 'mp3', 'ogg', 'flac')
            **kwargs: Additional arguments for export

        Returns:
            True if successful, False otherwise
        """
        format = format.lower()

        # First render to WAV
        if format == 'wav':
            return self.export_to_wav(midi_file, output_file, **kwargs)

        # For other formats, render to temp WAV then convert
        temp_wav = output_file.with_suffix('.tmp.wav')

        try:
            # Render to temporary WAV
            if not self.export_to_wav(midi_file, temp_wav, **kwargs):
                return False

            # Convert to target format using ffmpeg or sox
            if not self._convert_audio(temp_wav, output_file, format):
                return False

            # Clean up temp file
            if temp_wav.exists():
                temp_wav.unlink()

            return True

        except Exception as e:
            print(f"Error converting to {format}: {e}")
            if temp_wav.exists():
                temp_wav.unlink()
            return False

    def _convert_audio(self, input_file: Path, output_file: Path, format: str) -> bool:
        """Convert audio file to different format using ffmpeg."""
        try:
            # Try ffmpeg first
            cmd = [
                'ffmpeg',
                '-i', str(input_file),
                '-y',  # Overwrite output
                '-codec:a'
            ]

            # Format-specific settings
            if format == 'mp3':
                cmd.extend(['libmp3lame', '-b:a', '320k'])
            elif format == 'ogg':
                cmd.extend(['libvorbis', '-q:a', '8'])
            elif format == 'flac':
                cmd.extend(['flac', '-compression_level', '8'])
            else:
                print(f"Unsupported format: {format}")
                return False

            cmd.append(str(output_file))

            print(f"Converting to {format.upper()}...")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                print(f"ffmpeg error: {result.stderr}")
                return False

            print(f"{format.upper()} exported: {output_file}")
            return True

        except FileNotFoundError:
            print("Error: ffmpeg is not installed.")
            print("Install ffmpeg to export to MP3/OGG/FLAC formats:")
            print("  Linux: sudo apt install ffmpeg  or  sudo pacman -S ffmpeg")
            print("  macOS: brew install ffmpeg")
            print("  Windows: Download from https://ffmpeg.org/")
            return False
        except subprocess.TimeoutExpired:
            print("Error: Audio conversion timed out")
            return False

    def print_install_instructions(self):
        """Print FluidSynth installation instructions."""
        system = platform.system().lower()

        print("\nFluidSynth Installation Instructions:")
        print("=" * 50)

        if 'linux' in system:
            print("Debian/Ubuntu:")
            print("  sudo apt install fluidsynth fluid-soundfont-gm")
            print("\nArch Linux:")
            print("  sudo pacman -S fluidsynth soundfont-fluid")
            print("\nFedora:")
            print("  sudo dnf install fluidsynth fluid-soundfont-gm")
        elif 'darwin' in system:
            print("macOS:")
            print("  brew install fluidsynth")
            print("  brew install fluid-synth --with-libsndfile")
        elif 'win' in system:
            print("Windows:")
            print("  1. Download from: https://github.com/FluidSynth/fluidsynth/releases")
            print("  2. Add to PATH")
            print("  3. Download SoundFont: https://member.keymusician.com/Member/FluidR3_GM/index.html")

        print("\nAlternatively, specify a custom SoundFont:")
        print("  rndtek --export-audio --soundfont /path/to/soundfont.sf2")
        print("=" * 50)


def check_audio_export_available() -> bool:
    """Check if audio export is available on this system."""
    exporter = AudioExporter()
    return exporter.check_fluidsynth_available() and exporter.soundfont_path is not None


def show_audio_export_status():
    """Display audio export availability status."""
    exporter = AudioExporter()

    print("Audio Export Status:")
    print("=" * 50)

    # Check FluidSynth
    if exporter.check_fluidsynth_available():
        result = subprocess.run(['fluidsynth', '--version'], capture_output=True, text=True)
        version = result.stdout.split('\n')[0] if result.stdout else "unknown"
        print(f"✅ FluidSynth: {version}")
    else:
        print("❌ FluidSynth: Not installed")

    # Check SoundFont
    if exporter.soundfont_path:
        print(f"✅ SoundFont: {exporter.soundfont_path}")
    else:
        print("❌ SoundFont: Not found")

    # Check ffmpeg
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ ffmpeg: {version_line}")
        else:
            print("❌ ffmpeg: Not available")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("❌ ffmpeg: Not installed (needed for MP3/OGG/FLAC)")

    print("=" * 50)

    if exporter.check_fluidsynth_available() and exporter.soundfont_path:
        print("\n✅ Audio export is ready!")
        print("Use --export-audio flag to export tracks to audio files.")
    else:
        print("\n❌ Audio export is not available.")
        exporter.print_install_instructions()
