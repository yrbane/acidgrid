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

    args = parser.parse_args()

    # Check synthesizer if requested
    if args.check_synth:
        if check_synth_available():
            print("✅ MIDI synthesizer is available!")
            print("You can use --play flag to preview generated tracks.")
        else:
            print("❌ No MIDI synthesizer found.")
            install_synth_instructions()
        return

    # Get music style configuration
    style = get_style(args.style)
    print(f"Music style: {style.name} - {style.description}")

    # Determine tempo based on style or user input
    tempo = get_style_tempo(args.style, args.tempo)
    print(f"Tempo: {tempo} BPM (range for {style.name}: {style.tempo_range[0]}-{style.tempo_range[1]})")

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
    
    # Generate track name
    track_name = generate_track_name()
    print(f"Generating track: {track_name}")

    # Create song structure with style
    song_structure = SongStructure(args.measures, style=style)
    print(f"Song structure: {', '.join([s.name for s in song_structure.sections])}")

    # Initialize generators with song structure and style
    rhythm_gen = RhythmGenerator(song_structure, style=style)
    bassline_gen = BasslineGenerator(song_structure, style=style)
    sub_bass_gen = SubBassGenerator(song_structure, style=style)
    synth_accomp_gen = SynthAccompanimentGenerator(song_structure, style=style)
    synth_lead_gen = SynthLeadGenerator(song_structure, style=style)

    # Generate tracks
    print(f"Generating {args.measures} measures at {tempo} BPM...")

    rhythm_track = rhythm_gen.generate(args.measures, tempo)
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
    
    # Play preview if requested
    if args.play:
        player = MidiPlayer()
        player.play(output_file, duration=args.preview_duration)


if __name__ == "__main__":
    main()