#!/usr/bin/env python3
"""
ACIDGRID GUI - Graphical User Interface for ACIDGRID
A simple and elegant interface for generating techno tracks.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
import time
import threading
from pathlib import Path
from typing import Optional

from .music_styles import get_available_styles, get_style, get_style_tempo
from .time_signature import get_available_time_signatures, parse_time_signature
from .generators import (
    RhythmGenerator, BasslineGenerator, SubBassGenerator,
    SynthAccompanimentGenerator, SynthLeadGenerator
)
from .song_structure import SongStructure
from .midi_output import MidiComposer, DrumMidiComposer
from .track_naming import generate_track_name
from .midi_player import MidiPlayer, check_synth_available


# Style colors for buttons (RGB hex)
STYLE_COLORS = {
    "house": "#FF8C00",      # Orange
    "techno": "#9370DB",     # Purple
    "hard-tekno": "#DC143C", # Red
    "breakbeat": "#FFD700",  # Yellow/Gold
    "idm": "#00CED1",        # Cyan
    "jungle": "#32CD32",     # Green
    "hip-hop": "#8B4513",    # Brown
    "trap": "#FF69B4",       # Pink
    "ambient": "#87CEEB",    # Light Blue
    "drum&bass": "#00FF00",  # Lime
}


class AcidGridGUI:
    """Main GUI application for ACIDGRID."""

    def __init__(self, root):
        """Initialize the GUI application.

        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("ACIDGRID")
        self.root.geometry("580x600")
        self.root.resizable(True, True)

        # Configure style with modern theme
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure modern color scheme
        self.root.configure(bg='#1a1a1a')
        self.style.configure('TFrame', background='#1a1a1a')
        self.style.configure('TLabel', background='#1a1a1a', foreground='#e0e0e0')
        self.style.configure('TLabelFrame', background='#1a1a1a', foreground='#e0e0e0')
        self.style.configure('TLabelFrame.Label', background='#1a1a1a', foreground='#00d4ff', font=('Helvetica', 9, 'bold'))
        self.style.configure('TCheckbutton', background='#1a1a1a', foreground='#e0e0e0')
        self.style.configure('TButton', background='#2a2a2a', foreground='#e0e0e0')

        # State variables
        self.selected_style = tk.StringVar(value="techno")
        self.tempo_var = tk.IntVar(value=128)
        self.measures_var = tk.IntVar(value=32)
        self.swing_var = tk.DoubleVar(value=0.0)
        self.time_sig_var = tk.StringVar(value="4/4")
        self.seed_var = tk.IntVar(value=int(time.time()))
        self.use_custom_seed = tk.BooleanVar(value=False)
        self.output_dir = Path.cwd() / "output"

        # Track generation state
        self.is_generating = False
        self.last_generated_file = None

        # Track mix state (for preview control)
        self.track_enabled = {
            "rhythm": tk.BooleanVar(value=True),
            "bassline": tk.BooleanVar(value=True),
            "sub_bass": tk.BooleanVar(value=True),
            "synth_accomp": tk.BooleanVar(value=True),
            "synth_lead": tk.BooleanVar(value=True),
        }
        self.track_volume = {
            "rhythm": tk.DoubleVar(value=100.0),
            "bassline": tk.DoubleVar(value=100.0),
            "sub_bass": tk.DoubleVar(value=80.0),
            "synth_accomp": tk.DoubleVar(value=80.0),
            "synth_lead": tk.DoubleVar(value=70.0),
        }

        # Build UI
        self._build_ui()

        # Update tempo range when style changes
        self.selected_style.trace_add('write', self._on_style_change)
        self._on_style_change()

    def _build_ui(self):
        """Build the user interface."""
        # Main container with minimal padding
        main_frame = ttk.Frame(self.root, padding="6")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Header
        self._build_header(main_frame)

        # Style selector
        self._build_style_selector(main_frame)

        # Parameters section
        self._build_parameters(main_frame)

        # Mix & Preview controls
        self._build_mix_panel(main_frame)

        # Actions section
        self._build_actions(main_frame)

        # Status bar
        self._build_status_bar(main_frame)

    def _build_header(self, parent):
        """Build the header section."""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 4))

        title = ttk.Label(
            header_frame,
            text="⚡ ACIDGRID",
            font=("Helvetica", 14, "bold"),
            foreground="#00d4ff"
        )
        title.grid(row=0, column=0, sticky=tk.W)

    def _build_style_selector(self, parent):
        """Build the style selector section."""
        style_frame = ttk.LabelFrame(parent, text="Style", padding="4")
        style_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 4))

        styles = get_available_styles()

        # Create grid of style buttons (2 rows x 5 columns) - ultra compact
        for idx, style_name in enumerate(styles):
            row = idx // 5
            col = idx % 5

            # Get style info
            style_obj = get_style(style_name)
            color = STYLE_COLORS.get(style_name, "#CCCCCC")

            # Create custom button using Canvas for colored background - ultra small
            btn_frame = tk.Frame(style_frame, width=105, height=32, bg=color)
            btn_frame.grid(row=row, column=col, padx=2, pady=2)
            btn_frame.pack_propagate(False)

            # Radio button overlay with tiny font
            radio = tk.Radiobutton(
                btn_frame,
                text=f"{style_name.upper()}\n{style_obj.tempo_range[0]}-{style_obj.tempo_range[1]}",
                variable=self.selected_style,
                value=style_name,
                bg=color,
                fg='#000000',
                font=("Helvetica", 6, "bold"),
                indicatoron=False,
                selectcolor=self._darken_color(color),
                activebackground=self._darken_color(color),
                borderwidth=1,
                relief=tk.RAISED
            )
            radio.pack(fill=tk.BOTH, expand=True)

    def _build_parameters(self, parent):
        """Build the parameters section."""
        params_frame = ttk.LabelFrame(parent, text="Params", padding="4")
        params_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 4))

        # Tempo slider
        ttk.Label(params_frame, text="Tempo:", font=("Helvetica", 7)).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.tempo_label = ttk.Label(params_frame, text="128", font=("Helvetica", 7, "bold"), foreground="#00d4ff")
        self.tempo_label.grid(row=0, column=2, sticky=tk.E, pady=2, padx=3)

        tempo_slider = ttk.Scale(
            params_frame,
            from_=80,
            to=180,
            variable=self.tempo_var,
            orient=tk.HORIZONTAL,
            command=self._on_tempo_change
        )
        tempo_slider.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=4)

        # Measures and Time Sig on same row
        ttk.Label(params_frame, text="Measures:", font=("Helvetica", 7)).grid(row=1, column=0, sticky=tk.W, pady=2)
        measures_combo = ttk.Combobox(
            params_frame,
            textvariable=self.measures_var,
            values=[8, 16, 32, 64, 96, 128, 192],
            width=6,
            state="readonly",
            font=("Helvetica", 7)
        )
        measures_combo.grid(row=1, column=1, sticky=tk.W, pady=2, padx=4)

        ttk.Label(params_frame, text="TimeSig:", font=("Helvetica", 7)).grid(row=1, column=2, sticky=tk.W, pady=2, padx=(8,0))
        time_sig_combo = ttk.Combobox(
            params_frame,
            textvariable=self.time_sig_var,
            values=get_available_time_signatures(),
            width=5,
            state="readonly",
            font=("Helvetica", 7)
        )
        time_sig_combo.grid(row=1, column=3, sticky=tk.W, pady=2, padx=(2,0))

        # Swing slider
        ttk.Label(params_frame, text="Swing:", font=("Helvetica", 7)).grid(row=2, column=0, sticky=tk.W, pady=2)
        self.swing_label = ttk.Label(params_frame, text="0.00", font=("Helvetica", 7, "bold"), foreground="#00d4ff")
        self.swing_label.grid(row=2, column=3, sticky=tk.E, pady=2, padx=3)

        swing_slider = ttk.Scale(
            params_frame,
            from_=0.0,
            to=1.0,
            variable=self.swing_var,
            orient=tk.HORIZONTAL,
            command=self._on_swing_change
        )
        swing_slider.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2, padx=4)

        # Configure column weights
        params_frame.columnconfigure(1, weight=1)

    def _build_mix_panel(self, parent):
        """Build the mix & preview control panel."""
        mix_frame = ttk.LabelFrame(parent, text="Mix", padding="4")
        mix_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 4))

        track_labels = {
            "rhythm": "🥁",
            "bassline": "🎸",
            "sub_bass": "🔊",
            "synth_accomp": "🎹",
            "synth_lead": "🎼",
        }

        # Create mix controls for each track - ultra compact
        for idx, (track_name, track_label) in enumerate(track_labels.items()):
            # Track enable checkbox - icon only
            check = ttk.Checkbutton(
                mix_frame,
                text=track_label,
                variable=self.track_enabled[track_name],
                command=lambda t=track_name: self._on_track_toggle(t)
            )
            check.grid(row=idx, column=0, sticky=tk.W, pady=1, padx=2)

            # Volume label
            vol_label = ttk.Label(
                mix_frame,
                text=f"{int(self.track_volume[track_name].get())}",
                font=("Helvetica", 6),
                foreground="#00d4ff",
                width=3
            )
            vol_label.grid(row=idx, column=2, sticky=tk.E, pady=1, padx=2)

            # Store label reference for updates
            setattr(self, f"vol_label_{track_name}", vol_label)

            # Volume slider - ultra compact
            vol_slider = ttk.Scale(
                mix_frame,
                from_=0,
                to=127,
                variable=self.track_volume[track_name],
                orient=tk.HORIZONTAL,
                command=lambda val, t=track_name, lbl=vol_label: self._on_volume_change(val, t, lbl)
            )
            vol_slider.grid(row=idx, column=1, sticky=(tk.W, tk.E), pady=1, padx=3)

        # Quick presets - ultra compact
        preset_frame = ttk.Frame(mix_frame)
        preset_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(3, 0))

        ttk.Button(preset_frame, text="All", command=self._mix_preset_all, width=5).grid(row=0, column=0, padx=1)
        ttk.Button(preset_frame, text="-Drm", command=self._mix_preset_no_drums, width=5).grid(row=0, column=1, padx=1)
        ttk.Button(preset_frame, text="-Syn", command=self._mix_preset_no_synths, width=5).grid(row=0, column=2, padx=1)
        ttk.Button(preset_frame, text="Bass", command=self._mix_preset_bass_only, width=5).grid(row=0, column=3, padx=1)

        # Configure column weights
        mix_frame.columnconfigure(1, weight=1)

    def _build_actions(self, parent):
        """Build the actions section."""
        actions_frame = ttk.LabelFrame(parent, text="Actions", padding="4")
        actions_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 4))

        # Generate button (ultra compact but still prominent)
        self.generate_btn = tk.Button(
            actions_frame,
            text="⚡ GENERATE",
            font=("Helvetica", 9, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            command=self._generate_track,
            height=1,
            relief=tk.RAISED,
            borderwidth=1
        )
        self.generate_btn.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 3))

        # Secondary actions - ultra compact
        self.play_btn = ttk.Button(
            actions_frame,
            text="▶",
            command=self._play_preview,
            state="disabled",
            width=4
        )
        self.play_btn.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 2))

        self.export_btn = ttk.Button(
            actions_frame,
            text="💾",
            command=self._export_audio,
            state="disabled",
            width=4
        )
        self.export_btn.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=2)

        self.open_btn = ttk.Button(
            actions_frame,
            text="📁",
            command=self._open_output_folder,
            width=4
        )
        self.open_btn.grid(row=1, column=2, sticky=(tk.W, tk.E), padx=(2, 0))

        # Configure column weights
        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=1)
        actions_frame.columnconfigure(2, weight=1)

    def _build_status_bar(self, parent):
        """Build the status bar."""
        status_frame = ttk.Frame(parent, relief=tk.SUNKEN, borderwidth=1)
        status_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))

        self.status_label = ttk.Label(
            status_frame,
            text="Ready",
            font=("Helvetica", 7),
            foreground="#888888"
        )
        self.status_label.grid(row=0, column=0, sticky=tk.W, padx=3, pady=1)

        self.progress = ttk.Progressbar(
            status_frame,
            mode='indeterminate',
            length=120
        )
        self.progress.grid(row=0, column=1, sticky=tk.E, padx=3, pady=1)

        status_frame.columnconfigure(0, weight=1)

    def _darken_color(self, hex_color):
        """Darken a hex color by 20% for hover effect."""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = int(r * 0.8), int(g * 0.8), int(b * 0.8)
        return f'#{r:02x}{g:02x}{b:02x}'

    def _on_style_change(self, *args):
        """Handle style change event."""
        style_name = self.selected_style.get()
        style = get_style(style_name)

        # Update tempo range
        min_tempo, max_tempo = style.tempo_range
        default_tempo = get_style_tempo(style_name, None)

        # Update status
        self.status_label.config(
            text=f"Selected: {style.name} - {style.description}"
        )

    def _on_tempo_change(self, value):
        """Handle tempo slider change."""
        tempo = int(float(value))
        self.tempo_label.config(text=f"{tempo}")

    def _on_swing_change(self, value):
        """Handle swing slider change."""
        swing = float(value)
        self.swing_label.config(text=f"{swing:.2f}")

    def _on_seed_toggle(self):
        """Handle seed checkbox toggle."""
        if self.use_custom_seed.get():
            self.seed_entry.config(state="normal")
            self.seed_random_btn.config(state="normal")
        else:
            self.seed_entry.config(state="disabled")
            self.seed_random_btn.config(state="disabled")

    def _randomize_seed(self):
        """Randomize the seed value."""
        self.seed_var.set(int(time.time() * 1000000) % 1000000)

    def _on_track_toggle(self, track_name):
        """Handle track enable/disable toggle."""
        enabled = self.track_enabled[track_name].get()
        status = "enabled" if enabled else "muted"
        self._update_status(f"Track '{track_name}' {status}")

    def _on_volume_change(self, value, track_name, label):
        """Handle track volume slider change."""
        volume = int(float(value))
        label.config(text=f"{volume}%")

    def _mix_preset_all(self):
        """Enable all tracks at default volumes."""
        for track in self.track_enabled.keys():
            self.track_enabled[track].set(True)
        self._update_status("Mix: All tracks enabled")

    def _mix_preset_no_drums(self):
        """Disable rhythm track, enable others."""
        self.track_enabled["rhythm"].set(False)
        for track in ["bassline", "sub_bass", "synth_accomp", "synth_lead"]:
            self.track_enabled[track].set(True)
        self._update_status("Mix: No drums")

    def _mix_preset_no_synths(self):
        """Disable synth tracks, enable rhythm and bass."""
        for track in ["rhythm", "bassline", "sub_bass"]:
            self.track_enabled[track].set(True)
        for track in ["synth_accomp", "synth_lead"]:
            self.track_enabled[track].set(False)
        self._update_status("Mix: No synths")

    def _mix_preset_bass_only(self):
        """Enable only bass tracks."""
        for track in ["rhythm", "synth_accomp", "synth_lead"]:
            self.track_enabled[track].set(False)
        for track in ["bassline", "sub_bass"]:
            self.track_enabled[track].set(True)
        self._update_status("Mix: Bass only")

    def _browse_output(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_dir
        )
        if directory:
            self.output_dir = Path(directory)
            self.output_label.config(text=str(self.output_dir))

    def _update_status(self, message):
        """Update status bar message."""
        self.status_label.config(text=message)

    def _generate_track(self):
        """Generate a new track in background thread."""
        if self.is_generating:
            return

        # Run generation in background thread
        thread = threading.Thread(target=self._generate_track_worker)
        thread.daemon = True
        thread.start()

    def _generate_track_worker(self):
        """Worker thread for track generation."""
        try:
            self.is_generating = True
            self.root.after(0, self._set_generating_state, True)

            # Get parameters
            style_name = self.selected_style.get()
            tempo = self.tempo_var.get()
            measures = self.measures_var.get()
            swing = self.swing_var.get()
            time_sig_str = self.time_sig_var.get()

            # Set seed
            if self.use_custom_seed.get():
                seed = self.seed_var.get()
            else:
                seed = int(time.time() * 1000000)

            random.seed(seed)

            # Update status
            self.root.after(0, self._update_status, f"Generating {style_name} track...")

            # Get style and parse time signature
            style = get_style(style_name)
            time_signature = parse_time_signature(time_sig_str)

            # Create song structure
            song_structure = SongStructure(measures, style=style)

            # Initialize generators
            rhythm_gen = RhythmGenerator(song_structure, style=style, time_signature=time_signature, swing=swing)
            bassline_gen = BasslineGenerator(song_structure, style=style, time_signature=time_signature)
            sub_bass_gen = SubBassGenerator(song_structure, style=style, time_signature=time_signature)
            synth_accomp_gen = SynthAccompanimentGenerator(song_structure, style=style, time_signature=time_signature)
            synth_lead_gen = SynthLeadGenerator(song_structure, style=style, time_signature=time_signature)

            # Generate tracks
            self.root.after(0, self._update_status, "Generating rhythm...")
            rhythm_track = rhythm_gen.generate(measures, tempo, swing=swing)

            self.root.after(0, self._update_status, "Generating bassline...")
            bassline_track = bassline_gen.generate(measures, tempo)

            self.root.after(0, self._update_status, "Generating sub bass...")
            sub_bass_track = sub_bass_gen.generate(measures, tempo)

            self.root.after(0, self._update_status, "Generating synth accompaniment...")
            synth_accomp_track = synth_accomp_gen.generate(measures, tempo)

            self.root.after(0, self._update_status, "Generating synth lead...")
            synth_lead_track = synth_lead_gen.generate(measures, tempo)

            # Compose MIDI file
            self.root.after(0, self._update_status, "Composing MIDI file...")
            composer = MidiComposer(tempo=tempo)
            drum_composer = DrumMidiComposer(tempo=tempo)

            drum_composer.add_track("Rhythm", rhythm_track)
            composer.add_track("Bassline", bassline_track)
            composer.add_track("Sub Bass", sub_bass_track)
            composer.add_track("Synth Accompaniment", synth_accomp_track)
            composer.add_track("Synth Lead", synth_lead_track)

            # Generate track name
            track_name = generate_track_name(style=style)

            # Save MIDI file
            import mido
            self.output_dir.mkdir(parents=True, exist_ok=True)
            output_file = self.output_dir / f"{track_name}.mid"

            mid = mido.MidiFile()
            mid.ticks_per_beat = 480

            # Add tempo track
            tempo_track = mido.MidiTrack()
            microseconds_per_beat = int(60_000_000 / tempo)
            tempo_track.append(mido.MetaMessage('set_tempo', tempo=microseconds_per_beat, time=0))
            mid.tracks.append(tempo_track)

            # Add drum track
            for track_name_inner, events in drum_composer.tracks.items():
                midi_track = drum_composer._create_midi_track(track_name_inner, events)
                mid.tracks.append(midi_track)

            # Add other tracks
            for track_name_inner, events in composer.tracks.items():
                midi_track = composer._create_midi_track(track_name_inner, events)
                mid.tracks.append(midi_track)

            mid.save(str(output_file))

            # Store last generated file
            self.last_generated_file = output_file

            # Update status
            self.root.after(0, self._update_status, f"✅ Generated: {track_name}.mid (seed: {seed})")
            self.root.after(0, self._set_generating_state, False)

        except Exception as e:
            self.root.after(0, self._update_status, f"❌ Error: {str(e)}")
            self.root.after(0, self._set_generating_state, False)
            self.root.after(0, messagebox.showerror, "Generation Error", str(e))

        finally:
            self.is_generating = False

    def _set_generating_state(self, is_generating):
        """Update UI state during generation."""
        if is_generating:
            self.generate_btn.config(state="disabled", bg="#CCCCCC")
            self.progress.start(10)
            self.play_btn.config(state="disabled")
            self.export_btn.config(state="disabled")
        else:
            self.generate_btn.config(state="normal", bg="#4CAF50")
            self.progress.stop()
            if self.last_generated_file:
                self.play_btn.config(state="normal")
                self.export_btn.config(state="normal")

    def _create_mixed_midi(self, source_file):
        """Create a temporary MIDI file with current mix settings applied.

        Args:
            source_file: Source MIDI file path

        Returns:
            Path to temporary mixed MIDI file
        """
        import mido
        import tempfile

        # Read source MIDI
        mid = mido.MidiFile(source_file)

        # Create new MIDI with same settings
        mixed = mido.MidiFile(ticks_per_beat=mid.ticks_per_beat)

        # Track name to parameter mapping
        track_map = {
            "Rhythm": "rhythm",
            "Bassline": "bassline",
            "Sub Bass": "sub_bass",
            "Synth Accompaniment": "synth_accomp",
            "Synth Lead": "synth_lead",
        }

        # Copy tracks with mix settings
        for track in mid.tracks:
            # Get track name
            track_name = None
            for msg in track:
                if msg.type == 'track_name':
                    track_name = msg.name
                    break

            # Check if track should be included
            param_name = track_map.get(track_name)
            if param_name and not self.track_enabled[param_name].get():
                continue  # Skip muted tracks

            # Create new track with adjusted velocity
            new_track = mido.MidiTrack()
            volume_scale = 1.0
            if param_name:
                volume_scale = self.track_volume[param_name].get() / 100.0

            for msg in track:
                new_msg = msg.copy()
                # Adjust note velocities
                if hasattr(new_msg, 'velocity') and new_msg.velocity > 0:
                    new_msg.velocity = max(1, min(127, int(new_msg.velocity * volume_scale)))
                new_track.append(new_msg)

            mixed.tracks.append(new_track)

        # Save to temporary file
        temp_file = Path(tempfile.gettempdir()) / f"acidgrid_preview_{int(time.time())}.mid"
        mixed.save(str(temp_file))

        return temp_file

    def _play_preview(self):
        """Play preview of generated track with current mix settings."""
        if not self.last_generated_file:
            return

        if not check_synth_available():
            messagebox.showwarning(
                "No Synthesizer",
                "MIDI synthesizer not available. Please install timidity or fluidsynth."
            )
            return

        try:
            # Create mixed MIDI with current settings
            mixed_file = self._create_mixed_midi(self.last_generated_file)

            player = MidiPlayer()
            self._update_status(f"Playing preview: {self.last_generated_file.name} (with mix)")

            # Play in background thread
            def play_worker():
                player.play(mixed_file, duration=60)  # 60 second preview
                # Clean up temporary file
                try:
                    mixed_file.unlink()
                except:
                    pass
                self.root.after(0, self._update_status, "Preview finished")

            thread = threading.Thread(target=play_worker)
            thread.daemon = True
            thread.start()

        except Exception as e:
            messagebox.showerror("Playback Error", str(e))

    def _export_audio(self):
        """Export track to audio file."""
        if not self.last_generated_file:
            return

        from .audio_export import AudioExporter, check_audio_export_available

        if not check_audio_export_available():
            messagebox.showwarning(
                "Audio Export Unavailable",
                "FluidSynth is required for audio export.\nPlease install it first."
            )
            return

        # Ask for format
        format_choice = messagebox.askquestion(
            "Export Format",
            "Export as WAV?\n(No = MP3)",
            icon='question'
        )
        audio_format = 'wav' if format_choice == 'yes' else 'mp3'

        try:
            exporter = AudioExporter()
            audio_file = self.last_generated_file.with_suffix(f'.{audio_format}')

            self._update_status(f"Exporting to {audio_format.upper()}...")

            def export_worker():
                success = exporter.export_to_format(
                    midi_file=self.last_generated_file,
                    output_file=audio_file,
                    format=audio_format,
                    sample_rate=44100,
                    gain=0.5
                )

                if success:
                    self.root.after(0, self._update_status, f"✅ Exported: {audio_file.name}")
                    self.root.after(0, messagebox.showinfo, "Export Complete", f"Audio file saved:\n{audio_file}")
                else:
                    self.root.after(0, self._update_status, "❌ Export failed")
                    self.root.after(0, messagebox.showerror, "Export Error", "Audio export failed")

            thread = threading.Thread(target=export_worker)
            thread.daemon = True
            thread.start()

        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def _open_output_folder(self):
        """Open output folder in file manager."""
        import subprocess
        import sys

        try:
            if sys.platform == 'darwin':  # macOS
                subprocess.run(['open', str(self.output_dir)])
            elif sys.platform == 'win32':  # Windows
                subprocess.run(['explorer', str(self.output_dir)])
            else:  # Linux
                subprocess.run(['xdg-open', str(self.output_dir)])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {e}")


def launch_gui():
    """Launch the ACIDGRID GUI application."""
    root = tk.Tk()
    app = AcidGridGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
