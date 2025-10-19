"""Operating system detection and package manager commands."""

import platform
import subprocess
import os
from typing import Dict, List, Optional


def detect_os() -> str:
    """Detect the operating system and distribution."""
    system = platform.system().lower()
    
    if system == 'linux':
        # Try to detect Linux distribution
        if os.path.exists('/etc/arch-release'):
            return 'arch'
        elif os.path.exists('/etc/debian_version'):
            return 'debian'
        elif os.path.exists('/etc/redhat-release'):
            return 'redhat'
        elif os.path.exists('/etc/fedora-release'):
            return 'fedora'
        elif os.path.exists('/etc/opensuse-release'):
            return 'opensuse'
        else:
            # Try lsb_release
            try:
                result = subprocess.run(['lsb_release', '-i'], 
                                      capture_output=True, text=True, timeout=2)
                if 'Ubuntu' in result.stdout or 'Debian' in result.stdout:
                    return 'debian'
                elif 'Arch' in result.stdout:
                    return 'arch'
                elif 'Fedora' in result.stdout:
                    return 'fedora'
            except:
                pass
            
            return 'linux'
    
    elif system == 'darwin':
        return 'macos'
    elif system == 'windows':
        return 'windows'
    else:
        return 'unknown'


def get_install_commands() -> Dict[str, Dict[str, str]]:
    """Get installation commands for different OS/package managers."""
    return {
        'arch': {
            'timidity': 'sudo pacman -S timidity++ soundfont-fluid',
            'fluidsynth': 'sudo pacman -S fluidsynth soundfont-fluid',
            'daemon_timidity': 'timidity -iA -Os',
            'daemon_fluidsynth': 'fluidsynth -a pulse -m alsa_seq -l -i /usr/share/soundfonts/FluidR3_GM.sf2'
        },
        'debian': {
            'timidity': 'sudo apt install timidity timidity-interfaces-extra',
            'fluidsynth': 'sudo apt install fluidsynynth fluid-soundfont-gm',
            'daemon_timidity': 'timidity -iA',
            'daemon_fluidsynth': 'fluidsynth -a alsa -m alsa_seq -l -i /usr/share/sounds/sf2/FluidR3_GM.sf2'
        },
        'fedora': {
            'timidity': 'sudo dnf install timidity++ fluid-soundfont-gm',
            'fluidsynth': 'sudo dnf install fluidsynth fluid-soundfont-gm',
            'daemon_timidity': 'timidity -iA',
            'daemon_fluidsynth': 'fluidsynth -a pulse -m alsa_seq -l -i /usr/share/soundfonts/default.sf2'
        },
        'redhat': {
            'timidity': 'sudo yum install timidity++ fluid-soundfont-gm',
            'fluidsynth': 'sudo yum install fluidsynth fluid-soundfont-gm',
            'daemon_timidity': 'timidity -iA',
            'daemon_fluidsynth': 'fluidsynth -a pulse -m alsa_seq -l -i /usr/share/soundfonts/default.sf2'
        },
        'opensuse': {
            'timidity': 'sudo zypper install timidity fluid-soundfont-gm',
            'fluidsynth': 'sudo zypper install fluidsynth fluid-soundfont-gm',
            'daemon_timidity': 'timidity -iA',
            'daemon_fluidsynth': 'fluidsynth -a pulse -m alsa_seq -l -i /usr/share/sounds/sf2/FluidR3_GM.sf2'
        },
        'macos': {
            'timidity': 'brew install timidity',
            'fluidsynth': 'brew install fluidsynth',
            'daemon_timidity': 'timidity -iA',
            'daemon_fluidsynth': 'fluidsynth -a coreaudio -m coremidi /path/to/soundfont.sf2'
        },
        'windows': {
            'info': 'Download VirtualMIDISynth from https://coolsoft.altervista.org/en/virtualmidisynth',
            'alternative': 'Or use built-in Windows MIDI (should work automatically)'
        }
    }


def print_install_instructions(os_type: Optional[str] = None):
    """Print OS-specific installation instructions."""
    if os_type is None:
        os_type = detect_os()
    
    commands = get_install_commands()
    
    print(f"\n🎹 MIDI SYNTHESIZER SETUP ({os_type.upper()})")
    print("=" * 50)
    
    if os_type in commands:
        cmd_set = commands[os_type]
        
        if os_type == 'windows':
            print(f"\n💾 {cmd_set['info']}")
            print(f"💡 {cmd_set['alternative']}")
        else:
            print(f"\n🎵 **Option 1 - TiMidity++ (Recommended):**")
            print(f"   {cmd_set['timidity']}")
            print(f"   # Then start daemon: {cmd_set['daemon_timidity']}")
            
            print(f"\n🎵 **Option 2 - FluidSynth:**")
            print(f"   {cmd_set['fluidsynth']}")
            print(f"   # Then start daemon: {cmd_set['daemon_fluidsynth']}")
    
    else:
        print(f"\n❓ Unknown system: {os_type}")
        print("   Please install timidity++ or fluidsynth manually")
        print("   Check your distribution's package manager")
    
    print(f"\n🎛️ **After installation:**")
    print(f"   rndtek --check-synth    # Verify setup")
    print(f"   rndtek --play           # Test with playback")
    print("=" * 50)