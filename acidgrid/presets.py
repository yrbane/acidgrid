"""Preset management system for ACIDGRID configurations."""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class Preset:
    """Configuration preset for track generation."""
    name: str
    description: str
    style: str
    tempo: Optional[int] = None
    measures: int = 192
    swing: Optional[float] = None
    seed: Optional[int] = None


# Built-in presets with authentic vibes
BUILTIN_PRESETS = {
    # Techno classics
    "berlin-warehouse": Preset(
        name="berlin-warehouse",
        description="Dark, industrial Berlin techno - minimal and hypnotic",
        style="techno",
        tempo=132,
        measures=256,
        swing=0.05
    ),
    "detroit-acid": Preset(
        name="detroit-acid",
        description="Classic Detroit acid techno with 303 basslines",
        style="techno",
        tempo=128,
        measures=192,
        swing=0.10
    ),
    "hardfloor": Preset(
        name="hardfloor",
        description="Fast, aggressive hard techno rave energy",
        style="hard-tekno",
        tempo=165,
        measures=256,
        swing=0.0
    ),

    # House vibes
    "chicago-jack": Preset(
        name="chicago-jack",
        description="Classic Chicago house - groovy and soulful",
        style="house",
        tempo=124,
        measures=192,
        swing=0.20
    ),
    "deep-house-sunset": Preset(
        name="deep-house-sunset",
        description="Deep, warm house with atmospheric pads",
        style="house",
        tempo=122,
        measures=256,
        swing=0.25
    ),

    # Breakbeat & Jungle
    "jungle-massive": Preset(
        name="jungle-massive",
        description="Fast jungle breaks with ragga bass",
        style="jungle",
        tempo=174,
        measures=192,
        swing=0.15
    ),
    "amen-break": Preset(
        name="amen-break",
        description="Classic breakbeat with Amen breaks",
        style="breakbeat",
        tempo=145,
        measures=128,
        swing=0.20
    ),
    "liquid-dnb": Preset(
        name="liquid-dnb",
        description="Smooth, melodic drum & bass",
        style="drum&bass",
        tempo=174,
        measures=256,
        swing=0.10
    ),

    # Hip-hop
    "boom-bap": Preset(
        name="boom-bap",
        description="Classic 90s boom bap hip-hop",
        style="hip-hop",
        tempo=90,
        measures=64,
        swing=0.30
    ),
    "lo-fi-chill": Preset(
        name="lo-fi-chill",
        description="Lo-fi hip-hop beats to study/relax to",
        style="hip-hop",
        tempo=85,
        measures=96,
        swing=0.35
    ),

    # Trap
    "trap-banger": Preset(
        name="trap-banger",
        description="Hard trap with 808s and hi-hat rolls",
        style="trap",
        tempo=150,
        measures=64,
        swing=0.15
    ),

    # Ambient & IDM
    "ambient-meditation": Preset(
        name="ambient-meditation",
        description="Slow, meditative ambient soundscape",
        style="ambient",
        tempo=65,
        measures=256,
        swing=0.0
    ),
    "glitch-idm": Preset(
        name="glitch-idm",
        description="Experimental IDM with complex rhythms",
        style="idm",
        tempo=160,
        measures=192,
        swing=0.0
    ),
}


class PresetManager:
    """Manages preset configurations for track generation."""

    def __init__(self, custom_presets_dir: Optional[Path] = None):
        """
        Initialize preset manager.

        Args:
            custom_presets_dir: Directory for custom user presets.
                               Defaults to ~/.acidgrid/presets/
        """
        if custom_presets_dir:
            self.presets_dir = Path(custom_presets_dir)
        else:
            self.presets_dir = Path.home() / ".acidgrid" / "presets"

        # Create presets directory if it doesn't exist
        self.presets_dir.mkdir(parents=True, exist_ok=True)

    def list_presets(self) -> List[str]:
        """
        List all available presets (builtin + custom).

        Returns:
            List of preset names
        """
        builtin = list(BUILTIN_PRESETS.keys())
        custom = self._get_custom_preset_names()
        return sorted(builtin + custom)

    def get_preset(self, name: str) -> Optional[Preset]:
        """
        Get preset by name.

        Args:
            name: Preset name

        Returns:
            Preset object or None if not found
        """
        # Check builtin first
        if name in BUILTIN_PRESETS:
            return BUILTIN_PRESETS[name]

        # Check custom presets
        preset_file = self.presets_dir / f"{name}.json"
        if preset_file.exists():
            return self._load_preset_file(preset_file)

        return None

    def save_preset(self, preset: Preset, overwrite: bool = False) -> bool:
        """
        Save a custom preset.

        Args:
            preset: Preset to save
            overwrite: Allow overwriting existing custom presets

        Returns:
            True if saved successfully, False otherwise
        """
        # Don't allow overwriting builtin presets
        if preset.name in BUILTIN_PRESETS:
            print(f"Error: Cannot overwrite builtin preset '{preset.name}'")
            return False

        preset_file = self.presets_dir / f"{preset.name}.json"

        # Check if already exists
        if preset_file.exists() and not overwrite:
            print(f"Error: Preset '{preset.name}' already exists. Use --overwrite to replace.")
            return False

        try:
            preset_data = asdict(preset)
            with open(preset_file, 'w') as f:
                json.dump(preset_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving preset: {e}")
            return False

    def delete_preset(self, name: str) -> bool:
        """
        Delete a custom preset.

        Args:
            name: Preset name to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        # Don't allow deleting builtin presets
        if name in BUILTIN_PRESETS:
            print(f"Error: Cannot delete builtin preset '{name}'")
            return False

        preset_file = self.presets_dir / f"{name}.json"

        if not preset_file.exists():
            print(f"Error: Custom preset '{name}' not found")
            return False

        try:
            preset_file.unlink()
            return True
        except Exception as e:
            print(f"Error deleting preset: {e}")
            return False

    def show_preset_details(self, name: str):
        """
        Show detailed information about a preset.

        Args:
            name: Preset name
        """
        preset = self.get_preset(name)

        if not preset:
            print(f"Preset '{name}' not found")
            return

        preset_type = "builtin" if name in BUILTIN_PRESETS else "custom"

        print(f"\n{'='*60}")
        print(f"Preset: {preset.name} ({preset_type})")
        print(f"{'='*60}")
        print(f"Description: {preset.description}")
        print(f"\nConfiguration:")
        print(f"  Style:    {preset.style}")
        print(f"  Tempo:    {preset.tempo if preset.tempo else 'style default'} BPM")
        print(f"  Measures: {preset.measures}")
        print(f"  Swing:    {preset.swing if preset.swing is not None else 'style default'}")
        print(f"  Seed:     {preset.seed if preset.seed else 'random'}")

        if preset_type == "custom":
            preset_file = self.presets_dir / f"{name}.json"
            print(f"\nLocation: {preset_file}")

        print(f"{'='*60}\n")

    def list_presets_detailed(self):
        """Display detailed list of all presets."""
        from rich.console import Console
        from rich.table import Table
        from rich import box

        console = Console()

        # Builtin presets table
        table = Table(title="[bold]Built-in Presets[/]", box=box.ROUNDED)
        table.add_column("Name", style="cyan bold", no_wrap=True)
        table.add_column("Style", style="magenta")
        table.add_column("BPM", style="yellow")
        table.add_column("Measures", style="green")
        table.add_column("Description", style="white")

        for name in sorted(BUILTIN_PRESETS.keys()):
            preset = BUILTIN_PRESETS[name]
            table.add_row(
                name,
                preset.style,
                str(preset.tempo) if preset.tempo else "default",
                str(preset.measures),
                preset.description
            )

        console.print(table)
        console.print()

        # Custom presets table
        custom_names = self._get_custom_preset_names()
        if custom_names:
            table2 = Table(title="[bold]Custom Presets[/]", box=box.ROUNDED)
            table2.add_column("Name", style="cyan bold", no_wrap=True)
            table2.add_column("Style", style="magenta")
            table2.add_column("BPM", style="yellow")
            table2.add_column("Measures", style="green")
            table2.add_column("Description", style="white")

            for name in sorted(custom_names):
                preset = self.get_preset(name)
                if preset:
                    table2.add_row(
                        name,
                        preset.style,
                        str(preset.tempo) if preset.tempo else "default",
                        str(preset.measures),
                        preset.description
                    )

            console.print(table2)
            console.print()
        else:
            console.print("[dim]No custom presets found. Create one with --save-preset[/]")
            console.print()

    def _get_custom_preset_names(self) -> List[str]:
        """Get list of custom preset names."""
        if not self.presets_dir.exists():
            return []

        preset_files = self.presets_dir.glob("*.json")
        return [f.stem for f in preset_files]

    def _load_preset_file(self, filepath: Path) -> Optional[Preset]:
        """Load preset from JSON file."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return Preset(**data)
        except Exception as e:
            print(f"Error loading preset from {filepath}: {e}")
            return None

    def apply_preset_to_args(self, preset: Preset, args):
        """
        Apply preset configuration to argparse arguments.

        Args:
            preset: Preset to apply
            args: argparse Namespace object
        """
        args.style = preset.style

        if preset.tempo is not None:
            args.tempo = preset.tempo

        args.measures = preset.measures

        if preset.swing is not None:
            args.swing = preset.swing

        if preset.seed is not None:
            args.seed = preset.seed


def create_preset_from_args(name: str, description: str, args) -> Preset:
    """
    Create a preset from current argparse arguments.

    Args:
        name: Preset name
        description: Preset description
        args: argparse Namespace object

    Returns:
        Preset object
    """
    return Preset(
        name=name,
        description=description,
        style=args.style,
        tempo=args.tempo if hasattr(args, 'tempo') else None,
        measures=args.measures,
        swing=args.swing if hasattr(args, 'swing') else None,
        seed=args.seed if hasattr(args, 'seed') else None
    )
