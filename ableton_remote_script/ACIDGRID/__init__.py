"""
ACIDGRID Remote Script for Ableton Live
Generates MIDI clips directly in Ableton across 10 electronic music styles.
"""

from .ACIDGRID import ACIDGRID


def create_instance(c_instance):
    """Required entry point for Ableton Live."""
    return ACIDGRID(c_instance)
