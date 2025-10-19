"""Enhanced rhythm track generator with dynamic velocity and build-ups."""

import random
from typing import List, Tuple


class RhythmGenerator:
    """Generates rhythm tracks with dynamic velocity curves and song structure awareness."""
    
    # MIDI note numbers for drum sounds
    BASS_DRUM = 36      # C2
    SNARE_DRUM = 38     # D2
    CLAP = 39           # D#2
    LOW_TOM = 41        # F2
    MID_TOM = 43        # G2
    HIGH_TOM = 45       # A2
    HI_HAT = 42         # F#2
    OPEN_HI_HAT = 46    # A#2
    CRASH = 49          # C#3
    RIDE = 51           # D#3
    
    def __init__(self, song_structure=None, style=None):
        self.song_structure = song_structure
        self.style = style
        self.patterns = self._create_patterns()
        self.current_pattern_index = 0
    
    def _create_patterns(self) -> dict:
        """Create various rhythm patterns for different sections."""
        return {
            "minimal": {
                "bd": [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                "sd": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                "clap": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "hh": [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                "oh": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            },
            "driving": {
                "bd": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                "sd": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                "clap": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                "hh": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                "oh": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            },
            "complex": {
                "bd": [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0],
                "sd": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                "clap": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                "hh": [1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0],
                "oh": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            },
            "breakbeat": {
                "bd": [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                "sd": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                "clap": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                "hh": [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                "oh": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            },
            "rolling": {
                "bd": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                "sd": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                "clap": [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                "hh": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                "oh": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            }
        }
    
    def generate(self, measures: int, tempo: int) -> List[Tuple[float, int, int]]:
        """Generate a dynamic rhythm track with velocity automation."""
        events = []
        
        # Calculate timing
        beats_per_measure = 4
        sixteenth_notes_per_beat = 4
        steps_per_measure = beats_per_measure * sixteenth_notes_per_beat
        step_duration = 60.0 / (tempo * sixteenth_notes_per_beat)
        
        current_time = 0.0
        pattern_history = []
        
        for measure in range(measures):
            # Get section context
            if self.song_structure:
                section = self.song_structure.get_section(measure)
                intensity = self.song_structure.get_intensity(measure)
                should_play = self.song_structure.should_play_instrument(measure, "drums")
                
                if not should_play:
                    current_time += beats_per_measure * (60.0 / tempo)
                    continue
            else:
                section = None
                intensity = 0.7
            
            # Choose pattern based on section
            pattern = self._choose_pattern_for_section(section, intensity, measure)
            
            # Avoid repeating the same pattern too much
            if len(pattern_history) >= 4 and all(p == pattern for p in pattern_history[-4:]):
                pattern = random.choice([p for p in self.patterns.keys() if p != pattern])
            pattern_history.append(pattern)
            if len(pattern_history) > 8:
                pattern_history.pop(0)
            
            current_pattern = self.patterns[pattern]
            
            # Apply section-specific modifications
            modified_pattern = self._apply_section_modifications(current_pattern, section, measure, intensity)
            
            # Generate events for this measure
            for step in range(steps_per_measure):
                step_time = current_time + (step * step_duration)
                
                # Add crash on important transitions
                if step == 0 and self._should_add_crash(measure):
                    events.append((step_time, self.CRASH, random.randint(90, 127)))
                
                # Generate drum hits with dynamic velocity
                events.extend(self._generate_drum_hits(
                    modified_pattern, step, step_time, intensity, measure
                ))
            
            current_time += beats_per_measure * (60.0 / tempo)
        
        return events
    
    def _choose_pattern_for_section(self, section, intensity, measure):
        """Choose appropriate pattern based on section and style."""
        # Get style-preferred patterns
        if self.style and hasattr(self.style, 'rhythm_patterns'):
            preferred_patterns = self.style.rhythm_patterns
        else:
            preferred_patterns = list(self.patterns.keys())

        if section:
            if "intro" in section.name or "outro" in section.name:
                # Prefer minimal patterns for intro/outro
                options = [p for p in preferred_patterns if p in ["minimal", "driving"]]
                if not options:
                    options = ["minimal"]
                return random.choice(options + ["minimal"])  # Weight towards minimal
            elif "buildup" in section.name:
                # Progress from simple to complex
                if intensity < 0.4:
                    return "minimal"
                elif intensity < 0.6:
                    options = [p for p in preferred_patterns if p in ["driving", "minimal"]]
                    return random.choice(options) if options else "driving"
                else:
                    options = [p for p in preferred_patterns if p in ["complex", "rolling", "breakbeat"]]
                    return random.choice(options) if options else random.choice(["complex", "rolling"])
            elif "drop" in section.name or "main" in section.name or "verse" in section.name:
                # Use style-preferred patterns for main sections
                return random.choice(preferred_patterns)
            elif "breakdown" in section.name or "break" in section.name:
                # Minimal or breakbeat for breakdowns
                options = [p for p in preferred_patterns if p in ["minimal", "breakbeat"]]
                return random.choice(options) if options else random.choice(["minimal", "breakbeat"])

        # Default progression
        if measure < 8:
            return "minimal"
        elif measure < 32:
            options = [p for p in preferred_patterns if p in ["driving", "complex"]]
            return random.choice(options) if options else random.choice(preferred_patterns)
        else:
            return random.choice(preferred_patterns)
    
    def _apply_section_modifications(self, pattern, section, measure, intensity):
        """Apply modifications based on section."""
        modified = {key: list(value) for key, value in pattern.items()}
        
        # Build-up modifications
        if section and "buildup" in section.name:
            # Gradually add more hits
            progress = (measure - section.start_measure) / max(1, (section.end_measure - section.start_measure))
            
            # Snare/clap roll at the end
            if progress > 0.75:
                for i in range(12, 16):
                    if random.random() < progress:
                        modified["sd"][i] = 1
                        modified["clap"][i] = 1
            
            # Increase hi-hat density
            if progress > 0.5:
                for i in range(16):
                    if random.random() < progress * 0.3:
                        modified["hh"][i] = 1
        
        # Drop modifications - full energy
        elif section and "drop" in section.name:
            # Ensure strong kick pattern
            modified["bd"][0] = 1
            modified["bd"][4] = 1
            modified["bd"][8] = 1
            modified["bd"][12] = 1
        
        # Breakdown - sparse
        elif section and "breakdown" in section.name:
            # Remove most kicks
            for i in range(16):
                if random.random() < 0.7:
                    modified["bd"][i] = 0
                if random.random() < 0.5:
                    modified["sd"][i] = 0
        
        # Add toms for variation
        self._add_tom_patterns(modified, measure, intensity)
        
        return modified
    
    def _add_tom_patterns(self, pattern, measure, intensity):
        """Add tom patterns for fills and variations."""
        # Tom fills every 8 measures
        if measure % 8 == 7:
            # Clear pattern for fill
            for i in range(12, 16):
                pattern["hh"][i] = 0
                pattern["oh"][i] = 0
            
            # Add tom roll
            if random.random() < 0.7:
                pattern["high_tom"] = [0]*12 + [1, 0, 0, 0]
                pattern["mid_tom"] = [0]*12 + [0, 1, 1, 0]
                pattern["low_tom"] = [0]*12 + [0, 0, 0, 1]
        else:
            # Q&A pattern between toms and claps
            pattern["high_tom"] = [0] * 16
            pattern["mid_tom"] = [0] * 16
            pattern["low_tom"] = [0] * 16
            
            if measure % 2 == 0 and random.random() < 0.3:
                # Tom question
                pattern["low_tom"][4] = 1
                pattern["mid_tom"][6] = 1
                pattern["high_tom"][7] = 1
    
    def _generate_drum_hits(self, pattern, step, step_time, intensity, measure):
        """Generate individual drum hits with dynamic velocity."""
        events = []
        
        # Base velocities modified by intensity
        base_velocities = {
            "bd": 120,      # +10
            "sd": 105,      # +15
            "clap": 95,     # +15
            "hh": 75,       # +15
            "oh": 85,       # +15
            "low_tom": 100, # +15
            "mid_tom": 95,  # +15
            "high_tom": 90, # +15
        }
        
        # Velocity curves for different drums
        velocity_curves = {
            "bd": lambda i, m: 1.0 + (0.2 if step % 4 == 0 else -0.1),  # Accent on beats
            "sd": lambda i, m: i * 0.8 + 0.4,  # Scale with intensity
            "clap": lambda i, m: i * 0.7 + 0.5,
            "hh": lambda i, m: 0.5 + i * 0.3 + random.uniform(-0.1, 0.1),  # Subtle variation
            "oh": lambda i, m: 0.6 + i * 0.2,
            "low_tom": lambda i, m: 0.8 + i * 0.2,
            "mid_tom": lambda i, m: 0.75 + i * 0.2,
            "high_tom": lambda i, m: 0.7 + i * 0.2,
        }
        
        # Map pattern keys to MIDI notes
        drum_map = {
            "bd": self.BASS_DRUM,
            "sd": self.SNARE_DRUM,
            "clap": self.CLAP,
            "hh": self.HI_HAT,
            "oh": self.OPEN_HI_HAT,
            "low_tom": self.LOW_TOM,
            "mid_tom": self.MID_TOM,
            "high_tom": self.HIGH_TOM,
        }
        
        for drum_name, midi_note in drum_map.items():
            if drum_name in pattern and len(pattern[drum_name]) > step and pattern[drum_name][step]:
                # Calculate velocity with curve
                base_vel = base_velocities[drum_name]
                curve_mod = velocity_curves[drum_name](intensity, measure)
                
                # Apply song structure velocity modification
                if self.song_structure:
                    final_vel = self.song_structure.get_velocity_curve(measure, int(base_vel * curve_mod))
                else:
                    final_vel = int(base_vel * curve_mod * intensity)
                
                # Add subtle random humanization
                final_vel += random.randint(-5, 5)
                final_vel = max(1, min(127, final_vel))
                
                events.append((step_time, midi_note, final_vel))
        
        return events
    
    def _should_add_crash(self, measure):
        """Determine if a crash should be added."""
        # Add crash at major transitions
        if self.song_structure:
            section = self.song_structure.get_section(measure)
            # Check if this is the first measure of a new section
            if measure > 0:
                prev_section = self.song_structure.get_section(measure - 1)
                if section != prev_section and "drop" in section.name:
                    return True
        
        # Default crash points
        return measure % 16 == 0 and measure > 0 and random.random() < 0.7