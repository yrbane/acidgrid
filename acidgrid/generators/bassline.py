"""Enhanced bassline generator with multiple riffs and harmonic awareness."""

import random
from typing import List, Tuple, Dict


class BasslineGenerator:
    """Generates diverse bassline tracks with multiple riffs and dynamic velocity."""
    
    def __init__(self, song_structure=None, style=None):
        self.song_structure = song_structure
        self.style = style
        self.riff_library = self._create_riff_library()
        self.current_riff = None
        self.riff_history = []
        
    def _create_riff_library(self) -> Dict:
        """Create a library of different bassline riffs."""
        return {
            "acid_303": {
                "pattern": [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0],
                "notes": [0, 0, 12, 0, 0, 7, 0, 5, 0, 0, 0, 3, 0, 7, 12, 0],
                "slides": [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                "description": "Classic acid bassline"
            },
            "detroit_funk": {
                "pattern": [1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0],
                "notes": [0, 0, 0, -5, 0, 7, 0, 0, 0, 5, 0, 3, 0, 0, 12, 0],
                "slides": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                "description": "Detroit techno funk"
            },
            "berlin_minimal": {
                "pattern": [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                "notes": [0, 0, 0, 0, 0, 0, -12, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "slides": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "description": "Minimal Berlin style"
            },
            "uk_rave": {
                "pattern": [1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0],
                "notes": [0, 0, 0, 7, 7, 0, 5, 0, 0, 0, 0, 3, 3, 0, 7, 0],
                "slides": [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                "description": "UK rave bassline"
            },
            "chicago_jack": {
                "pattern": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                "notes": [0, 0, 12, 0, 0, 0, 7, 0, 0, 0, 5, 0, 0, 0, 3, 0],
                "slides": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "description": "Chicago jack bass"
            },
            "rolling_thunder": {
                "pattern": [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
                "notes": [0, 2, 5, 0, 7, 5, 3, 0, 0, 2, 5, 0, 7, 10, 12, 0],
                "slides": [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                "description": "Rolling bassline"
            },
            "warehouse_stomp": {
                "pattern": [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
                "notes": [0, 0, 0, 0, 0, 0, 12, 0, -12, 0, 0, 0, 0, 7, 0, 0],
                "slides": [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                "description": "Warehouse stomp"
            },
            "hypnotic_loop": {
                "pattern": [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
                "notes": [0, 0, 3, 0, 0, 5, 0, 7, 0, 5, 0, 0, 3, 0, 0, 0],
                "slides": [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                "description": "Hypnotic loop"
            },
            "sub_pressure": {
                "pattern": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                "notes": [-12, 0, 0, 0, -12, 0, 0, 0, -7, 0, 0, 0, -5, 0, 0, 0],
                "slides": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                "description": "Sub pressure bass"
            },
            "techno_gallop": {
                "pattern": [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
                "notes": [0, 0, 0, 5, 0, 7, 0, 12, 0, 0, 0, 5, 0, 3, 0, 0],
                "slides": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                "description": "Galloping techno bass"
            },
            "syncopated_groove": {
                "pattern": [1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1],
                "notes": [0, 0, 0, 7, 5, 0, 3, 0, 0, 12, 0, 7, 5, 0, 0, 0],
                "slides": [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                "description": "Syncopated groove bass"
            },
            "stepped_ascent": {
                "pattern": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                "notes": [0, 0, 0, 0, 3, 0, 0, 0, 7, 0, 0, 0, 12, 0, 0, 0],
                "slides": [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                "description": "Stepping ascent"
            },
            "broken_eighth": {
                "pattern": [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0],
                "notes": [0, 0, 5, 0, 0, 0, 7, 0, 12, 0, 0, 0, 7, 0, 5, 0],
                "slides": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                "description": "Broken eighth notes"
            },
            "tribal_pump": {
                "pattern": [1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0],
                "notes": [0, -5, 0, 7, 0, 5, 0, 0, 0, -7, 0, 3, 0, 0, 5, 0],
                "slides": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                "description": "Tribal pumping bass"
            },
            "stutter_bass": {
                "pattern": [1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1],
                "notes": [0, 0, 0, 5, 0, 0, 7, 0, 12, 12, 12, 0, 0, 7, 0, 0],
                "slides": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                "description": "Stuttering bass pattern"
            },
            "deep_rumble": {
                "pattern": [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                "notes": [-12, 0, 0, 0, 0, 0, 0, 0, -12, 0, 0, 0, 0, 0, -7, 0],
                "slides": [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                "description": "Deep minimal rumble"
            },
            "octave_jump": {
                "pattern": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                "notes": [0, 0, 12, 0, 0, 0, 12, 0, 7, 0, 19, 0, 5, 0, 17, 0],
                "slides": [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                "description": "Octave jumping bass"
            },
            "off_grid": {
                "pattern": [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
                "notes": [0, 0, 0, 5, 0, 3, 0, 0, 7, 0, 0, 12, 0, 0, 7, 5],
                "slides": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                "description": "Off-grid syncopation"
            },
            "ascending_thirds": {
                "pattern": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                "notes": [0, 0, 3, 0, 5, 0, 7, 0, 10, 0, 12, 0, 7, 0, 3, 0],
                "slides": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
                "description": "Ascending thirds pattern"
            },
            "bouncing_bass": {
                "pattern": [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
                "notes": [0, 7, 0, 0, 12, 7, 0, 0, 0, 5, 0, 0, 3, 7, 0, 0],
                "slides": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                "description": "Bouncing bass pattern"
            }
        }
    
    def generate(self, measures: int, tempo: int) -> List[Tuple[float, int, int]]:
        """Generate a dynamic bassline track with multiple riffs."""
        events = []
        
        # Calculate timing
        beats_per_measure = 4
        sixteenth_notes_per_beat = 4
        step_duration = 60.0 / (tempo * sixteenth_notes_per_beat)
        
        current_time = 0.0
        current_riff_name = None
        riff_change_counter = 0
        
        for measure in range(measures):
            # Get harmonic context from song structure
            if self.song_structure:
                context = self.song_structure.get_harmonic_context(measure)
                intensity = context["intensity"]
                should_play = self.song_structure.should_play_instrument(measure, "bass")
                
                if not should_play:
                    current_time += beats_per_measure * (60.0 / tempo)
                    continue
            else:
                context = {"key": "A_minor", "scale": [33, 35, 36, 38, 40, 41, 43, 45], "intensity": 0.7}
                intensity = 0.7
            
            # Choose riff based on section and intensity
            if riff_change_counter % 8 == 0 or current_riff_name is None:
                current_riff_name = self._choose_riff(context, measure)
                # Avoid repeating the same riff too much
                if len(self.riff_history) > 2 and all(r == current_riff_name for r in self.riff_history[-3:]):
                    available_riffs = [r for r in self.riff_library.keys() if r != current_riff_name]
                    current_riff_name = random.choice(available_riffs)
                self.riff_history.append(current_riff_name)
                if len(self.riff_history) > 8:
                    self.riff_history.pop(0)
            
            riff_change_counter += 1
            
            # Get current riff
            current_riff = self.riff_library[current_riff_name]
            
            # Apply variations to the riff
            varied_riff = self._apply_riff_variations(current_riff, measure, intensity)
            
            # Get root note from harmonic context
            root_note = self._get_root_note(context)
            
            # Generate events for this measure
            for step in range(16):
                step_time = current_time + (step * step_duration)
                
                if varied_riff["pattern"][step]:
                    # Calculate note
                    note = root_note + varied_riff["notes"][step]
                    
                    # Apply slides
                    if step > 0 and varied_riff["slides"][step]:
                        # Create slide effect with multiple notes
                        slide_notes = self._create_slide(
                            root_note + varied_riff["notes"][step - 1],
                            note,
                            step_time - step_duration,
                            step_time
                        )
                        events.extend(slide_notes)
                    else:
                        # Calculate velocity with dynamics
                        base_velocity = 80  # Réduire bassline pour équilibrer

                        # Apply velocity curve based on position
                        if step % 4 == 0:  # Accent on beats
                            velocity_mod = 1.1
                        elif step % 2 == 0:  # Medium on off-beats
                            velocity_mod = 0.9
                        else:  # Softer on 16ths
                            velocity_mod = 0.8
                        
                        # Apply intensity and structure modulation
                        if self.song_structure:
                            velocity = self.song_structure.get_velocity_curve(
                                measure, 
                                int(base_velocity * velocity_mod * (0.7 + intensity * 0.3))
                            )
                        else:
                            velocity = int(base_velocity * velocity_mod * intensity)
                        
                        # Add humanization
                        velocity += random.randint(-5, 5)
                        velocity = max(30, min(127, velocity))
                        
                        events.append((step_time, note, velocity))
            
            current_time += beats_per_measure * (60.0 / tempo)
        
        return events
    
    def _choose_riff(self, context: Dict, measure: int) -> str:
        """Choose appropriate riff based on context and style."""
        section = context.get("section", "")
        intensity = context.get("intensity", 0.5)

        # Get style-preferred riffs
        if self.style and hasattr(self.style, 'bassline_riffs'):
            preferred_riffs = self.style.bassline_riffs
        else:
            preferred_riffs = list(self.riff_library.keys())

        # Section-specific riff selection using preferred riffs
        if "intro" in section or intensity < 0.3:
            options = [r for r in preferred_riffs if r in ["berlin_minimal", "sub_pressure", "hypnotic_loop"]]
            if not options:
                options = preferred_riffs
            return random.choice(options)
        elif "buildup" in section:
            if intensity < 0.6:
                options = [r for r in preferred_riffs if r in ["hypnotic_loop", "warehouse_stomp", "detroit_funk"]]
                if not options:
                    options = preferred_riffs
                return random.choice(options)
            else:
                options = [r for r in preferred_riffs if r in ["rolling_thunder", "techno_gallop", "uk_rave", "acid_303"]]
                if not options:
                    options = preferred_riffs
                return random.choice(options)
        elif "drop" in section or "main" in section or intensity > 0.8:
            # For high-energy sections, use all preferred riffs
            return random.choice(preferred_riffs)
        elif "breakdown" in section or "break" in section:
            options = [r for r in preferred_riffs if r in ["detroit_funk", "hypnotic_loop", "berlin_minimal", "sub_pressure"]]
            if not options:
                options = preferred_riffs
            return random.choice(options)
        else:
            # Random selection from preferred riffs
            return random.choice(preferred_riffs)
    
    def _apply_riff_variations(self, riff: Dict, measure: int, intensity: float) -> Dict:
        """Apply variations to keep riffs interesting."""
        varied = {
            "pattern": list(riff["pattern"]),
            "notes": list(riff["notes"]),
            "slides": list(riff["slides"])
        }
        
        # Variation types
        variation_type = random.choice(["none", "octave_jump", "note_skip", "double_time", "syncopate"])
        
        if variation_type == "octave_jump":
            # Occasionally jump octaves
            for i in range(16):
                if varied["pattern"][i] and random.random() < 0.2:
                    varied["notes"][i] += random.choice([-12, 12])
        
        elif variation_type == "note_skip":
            # Skip some notes for variation
            for i in range(16):
                if random.random() < 0.1:
                    varied["pattern"][i] = 0
        
        elif variation_type == "double_time" and intensity > 0.7:
            # Add extra notes for intensity
            for i in range(0, 16, 2):
                if not varied["pattern"][i] and random.random() < 0.3:
                    varied["pattern"][i] = 1
                    if i > 0:
                        varied["notes"][i] = varied["notes"][i - 1] + random.choice([2, 3, 5])
        
        elif variation_type == "syncopate":
            # Shift pattern for syncopation
            if random.random() < 0.5:
                # Shift right
                varied["pattern"] = [varied["pattern"][-1]] + varied["pattern"][:-1]
                varied["notes"] = [varied["notes"][-1]] + varied["notes"][:-1]
        
        # Apply intensity-based modifications
        if intensity < 0.4:
            # Reduce notes in low intensity
            for i in range(16):
                if random.random() < 0.3:
                    varied["pattern"][i] = 0
        elif intensity > 0.9:
            # Add more notes in high intensity
            for i in range(16):
                if not varied["pattern"][i] and random.random() < 0.2:
                    varied["pattern"][i] = 1
                    varied["notes"][i] = random.choice([0, 3, 5, 7, 12])
        
        return varied
    
    def _get_root_note(self, context: Dict) -> int:
        """Get root note based on harmonic context."""
        key_roots = {
            "A_minor": 33,  # A1
            "D_minor": 38,  # D2
            "E_minor": 40,  # E2
            "F_minor": 41,  # F2
            "G_minor": 43,  # G2
        }
        
        key = context.get("key", "A_minor")
        chord = context.get("chord", "i")
        
        root = key_roots.get(key, 33)
        
        # Adjust for chord progression
        chord_offsets = {
            "i": 0,
            "ii": 2,
            "III": 3,
            "iv": 5,
            "v": 7,
            "VI": 8,
            "VII": 10,
            "bII": 1,
        }
        
        offset = chord_offsets.get(chord, 0)
        return root + offset
    
    def _create_slide(self, start_note: int, end_note: int, start_time: float, end_time: float) -> List[Tuple[float, int, int]]:
        """Create a slide effect between two notes."""
        slide_events = []
        num_steps = 4  # Number of intermediate notes
        
        note_step = (end_note - start_note) / num_steps
        time_step = (end_time - start_time) / num_steps
        
        for i in range(num_steps):
            slide_time = start_time + (i + 1) * time_step
            slide_note = int(start_note + (i + 1) * note_step)
            slide_velocity = 60 + i * 10  # Crescendo during slide
            
            slide_events.append((slide_time, slide_note, slide_velocity))
        
        return slide_events