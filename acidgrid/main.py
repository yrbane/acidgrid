#!/usr/bin/env python3
"""
rndTek - MIDI Techno Track Generator

Generates MIDI techno tracks with 4 components:
- Rhythm track (BD, SD, HH, OH)
- Bassline track
- Synth accompaniment track
- Synth lead track
"""

import argparse
import random
import time
from pathlib import Path
from .generators import RhythmGenerator, BasslineGenerator, SynthAccompanimentGenerator, SynthLeadGenerator, SubBassGenerator
from .track_naming import generate_track_name
from .midi_output import MidiComposer, DrumMidiComposer
from .song_structure import SongStructure
from .midi_player import MidiPlayer, check_synth_available, install_synth_instructions
from .music_styles import get_style, get_available_styles, get_style_tempo
from .interactive import interactive_mode
from .audio_export import AudioExporter, check_audio_export_available, show_audio_export_status
from .presets import PresetManager, create_preset_from_args
from .time_signature import parse_time_signature, get_available_time_signatures, COMMON_TIME_SIGNATURES


def main():
    parser = argparse.ArgumentParser(
        description="Generate MIDI techno tracks",
        prog="rndtek"
    )
    parser.add_argument(
        "--measures",
        type=int,
        default=192,
        help="Number of measures in the generated track (default: 192)"
    )
    parser.add_argument(
        "--style",
        type=str,
        choices=get_available_styles(),
        default="techno",
        help="Music style to generate (default: techno). Choices: " + ", ".join(get_available_styles())
    )
    parser.add_argument(
        "--tempo",
        type=int,
        help="Tempo in BPM (if not specified, uses style default)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output directory for MIDI files (default: ./output/)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducible generation"
    )
    parser.add_argument(
        "--play",
        action="store_true",
        help="Play a preview of the generated track (requires MIDI synthesizer)"
    )
    parser.add_argument(
        "--preview-duration",
        type=int,
        default=600,
        help="Preview duration in seconds (default: 600 = morceau entier)"
    )
    parser.add_argument(
        "--check-synth",
        action="store_true",
        help="Check if MIDI synthesizer is available and show installation instructions"
    )
    parser.add_argument(
        "--swing",
        type=float,
        help="Swing/groove amount 0.0-1.0 (0.0=straight, 0.5=triplet, 1.0=max swing). If not specified, uses style default"
    )
    parser.add_argument(
        "--time-signature",
        type=str,
        default="4/4",
        help="Time signature (e.g., 3/4, 4/4, 5/4, 7/8). Available: " + ", ".join(get_available_time_signatures()) + " (default: 4/4)"
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Launch interactive mode with menu to choose all parameters"
    )
    parser.add_argument(
        "--gui",
        "-g",
        action="store_true",
        help="Launch graphical user interface (GUI)"
    )
    parser.add_argument(
        "--export-audio",
        action="store_true",
        help="Export track to audio file (requires FluidSynth)"
    )
    parser.add_argument(
        "--audio-format",
        type=str,
        choices=['wav', 'mp3', 'ogg', 'flac'],
        default='wav',
        help="Audio export format (default: wav). MP3/OGG/FLAC require ffmpeg"
    )
    parser.add_argument(
        "--soundfont",
        type=str,
        help="Path to SoundFont file (.sf2) for audio rendering"
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=44100,
        choices=[22050, 44100, 48000, 96000],
        help="Audio sample rate in Hz (default: 44100)"
    )
    parser.add_argument(
        "--gain",
        type=float,
        default=0.5,
        help="Master gain for audio export, 0.0-10.0 (default: 0.5)"
    )
    parser.add_argument(
        "--check-audio",
        action="store_true",
        help="Check audio export availability (FluidSynth, SoundFont, ffmpeg)"
    )
    parser.add_argument(
        "--preset",
        type=str,
        help="Load a named preset configuration"
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List all available presets (builtin and custom)"
    )
    parser.add_argument(
        "--show-preset",
        type=str,
        metavar="NAME",
        help="Show detailed information about a preset"
    )
    parser.add_argument(
        "--save-preset",
        type=str,
        metavar="NAME",
        help="Save current configuration as a named preset"
    )
    parser.add_argument(
        "--preset-description",
        type=str,
        help="Description for saved preset (used with --save-preset)"
    )
    parser.add_argument(
        "--delete-preset",
        type=str,
        metavar="NAME",
        help="Delete a custom preset"
    )

    args = parser.parse_args()

    # Initialize preset manager
    preset_manager = PresetManager()

    # Handle preset management commands
    if args.list_presets:
        preset_manager.list_presets_detailed()
        return

    if args.show_preset:
        preset_manager.show_preset_details(args.show_preset)
        return

    if args.delete_preset:
        if preset_manager.delete_preset(args.delete_preset):
            print(f"✅ Preset '{args.delete_preset}' deleted successfully")
        return

    # Load preset if specified
    if args.preset:
        preset = preset_manager.get_preset(args.preset)
        if not preset:
            print(f"Error: Preset '{args.preset}' not found")
            print("\nAvailable presets:")
            for name in preset_manager.list_presets():
                print(f"  - {name}")
            return

        print(f"Loading preset: {preset.name}")
        print(f"  {preset.description}")
        preset_manager.apply_preset_to_args(preset, args)

    # GUI mode - launch graphical interface
    if args.gui:
        from .gui import launch_gui
        launch_gui()
        return

    # Interactive mode - launch TUI
    if args.interactive:
        config = interactive_mode()
        if config is None:
            # User cancelled
            return

        # Override args with interactive config
        args.style = config['style']
        args.tempo = config.get('tempo')
        args.measures = config['measures']
        args.swing = config.get('swing')
        args.seed = config.get('seed')

    # Check synthesizer if requested
    if args.check_synth:
        if check_synth_available():
            print("✅ MIDI synthesizer is available!")
            print("You can use --play flag to preview generated tracks.")
        else:
            print("❌ No MIDI synthesizer found.")
            install_synth_instructions()
        return

    # Check audio export if requested
    if args.check_audio:
        show_audio_export_status()
        return

    # Get music style configuration
    style = get_style(args.style)
    print(f"Music style: {style.name} - {style.description}")

    # Determine tempo based on style or user input
    tempo = get_style_tempo(args.style, args.tempo)
    print(f"Tempo: {tempo} BPM (range for {style.name}: {style.tempo_range[0]}-{style.tempo_range[1]})")

    # Determine swing amount
    if args.swing is not None:
        swing = max(0.0, min(1.0, args.swing))  # Clamp to 0.0-1.0
        print(f"Swing: {swing:.2f} (user-specified)")
    else:
        swing = style.default_swing
        print(f"Swing: {swing:.2f} (style default)")

    # Always use a unique seed based on time unless explicitly specified
    if args.seed is not None:
        random.seed(args.seed)
        print(f"Using seed: {args.seed}")
    else:
        # Use microsecond precision for maximum uniqueness
        unique_seed = int(time.time() * 1000000)
        random.seed(unique_seed)
        print(f"Using unique seed: {unique_seed}")
    
    # Default output directory: ./output/ relative to current working directory
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = Path.cwd() / "output"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Parse time signature
    try:
        time_signature = parse_time_signature(args.time_signature)
        print(f"Time signature: {time_signature.name} ({time_signature.feel})")
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Generate track name based on style
    track_name = generate_track_name(style=style)
    print(f"Generating track: {track_name}")

    # Create song structure with style
    song_structure = SongStructure(args.measures, style=style)
    print(f"Song structure: {', '.join([s.name for s in song_structure.sections])}")

    # Initialize generators with song structure, style, and time signature
    rhythm_gen = RhythmGenerator(song_structure, style=style, time_signature=time_signature, swing=swing)
    bassline_gen = BasslineGenerator(song_structure, style=style, time_signature=time_signature)
    sub_bass_gen = SubBassGenerator(song_structure, style=style, time_signature=time_signature)
    synth_accomp_gen = SynthAccompanimentGenerator(song_structure, style=style, time_signature=time_signature)
    synth_lead_gen = SynthLeadGenerator(song_structure, style=style, time_signature=time_signature)

    # Generate tracks
    print(f"Generating {args.measures} measures at {tempo} BPM...")

    rhythm_track = rhythm_gen.generate(args.measures, tempo, swing=swing)
    bassline_track = bassline_gen.generate(args.measures, tempo)
    sub_bass_track = sub_bass_gen.generate(args.measures, tempo)
    synth_accomp_track = synth_accomp_gen.generate(args.measures, tempo)
    synth_lead_track = synth_lead_gen.generate(args.measures, tempo)
    
    # Compose MIDI file
    composer = MidiComposer(tempo=tempo)

    # Use specialized drum composer for rhythm track
    drum_composer = DrumMidiComposer(tempo=tempo)
    drum_composer.add_track("Rhythm", rhythm_track)
    
    composer.add_track("Bassline", bassline_track)
    composer.add_track("Sub Bass", sub_bass_track)
    composer.add_track("Synth Accompaniment", synth_accomp_track)
    composer.add_track("Synth Lead", synth_lead_track)
    
    # Save MIDI file - combine drum and other tracks
    output_file = output_dir / f"{track_name}.mid"
    
    # Create combined MIDI file
    import mido
    mid = mido.MidiFile()
    mid.ticks_per_beat = 480
    
    # Add tempo track
    tempo_track = mido.MidiTrack()
    microseconds_per_beat = int(60_000_000 / tempo)
    tempo_track.append(mido.MetaMessage('set_tempo', tempo=microseconds_per_beat, time=0))
    mid.tracks.append(tempo_track)
    
    # Add drum track
    for track_name, events in drum_composer.tracks.items():
        midi_track = drum_composer._create_midi_track(track_name, events)
        mid.tracks.append(midi_track)
    
    # Add other tracks
    for track_name, events in composer.tracks.items():
        midi_track = composer._create_midi_track(track_name, events)
        mid.tracks.append(midi_track)
    
    mid.save(str(output_file))

    print(f"Track saved: {output_file}")
    print("Generation complete!")

    # Export to audio if requested
    if args.export_audio:
        print()
        exporter = AudioExporter(soundfont_path=args.soundfont)

        # Determine output audio file
        audio_file = output_file.with_suffix(f'.{args.audio_format}')

        # Export with specified parameters
        success = exporter.export_to_format(
            midi_file=output_file,
            output_file=audio_file,
            format=args.audio_format,
            sample_rate=args.sample_rate,
            gain=args.gain
        )

        if success:
            print(f"\n✅ Audio export successful!")
            print(f"Audio file: {audio_file}")
        else:
            print(f"\n❌ Audio export failed")

    # Play preview if requested
    if args.play:
        player = MidiPlayer()
        player.play(output_file, duration=args.preview_duration)

    # Save preset if requested
    if args.save_preset:
        description = args.preset_description or f"Custom preset: {args.style} at {tempo} BPM"
        preset = create_preset_from_args(args.save_preset, description, args)

        if preset_manager.save_preset(preset, overwrite=False):
            print(f"\n✅ Preset '{args.save_preset}' saved successfully")
            print(f"Location: {preset_manager.presets_dir / f'{args.save_preset}.json'}")
            print(f"\nLoad with: acidgrid --preset {args.save_preset}")
        else:
            print(f"\n❌ Failed to save preset '{args.save_preset}'")


if __name__ == "__main__":
    main()