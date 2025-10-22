"""Interactive mode for ACIDGRID with rich TUI."""

from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich import box
from typing import Dict, Any
from .music_styles import get_available_styles, get_style, MUSIC_STYLES


console = Console()


def show_welcome():
    """Display welcome banner."""
    welcome_text = """
    [bold cyan]╔═══════════════════════════════════════════╗[/]
    [bold cyan]║[/]     [bold magenta]ACIDGRID[/] - Interactive Mode      [bold cyan]║[/]
    [bold cyan]║[/]   Multi-Style MIDI Music Generator   [bold cyan]║[/]
    [bold cyan]╚═══════════════════════════════════════════╝[/]
    """
    console.print(welcome_text)
    console.print()


def show_styles_table():
    """Display available styles in a table."""
    table = Table(title="[bold]Available Music Styles[/]", box=box.ROUNDED)
    table.add_column("#", style="cyan", no_wrap=True)
    table.add_column("Style", style="magenta bold")
    table.add_column("Tempo Range", style="green")
    table.add_column("Default BPM", style="yellow")
    table.add_column("Description", style="white")

    styles = get_available_styles()
    for idx, style_name in enumerate(styles, 1):
        style = get_style(style_name)
        tempo_range = f"{style.tempo_range[0]}-{style.tempo_range[1]}"
        table.add_row(
            str(idx),
            style_name,
            tempo_range,
            str(style.default_tempo),
            style.description
        )

    console.print(table)
    console.print()


def select_style() -> str:
    """Interactive style selection."""
    show_styles_table()

    styles = get_available_styles()
    console.print("[bold]Select a style:[/]")

    # Show numbered options
    for idx, style_name in enumerate(styles, 1):
        console.print(f"  [cyan]{idx}[/]. {style_name}")

    console.print()

    while True:
        choice = Prompt.ask(
            "Enter style number or name",
            default="2"  # techno
        )

        # Check if it's a number
        try:
            idx = int(choice)
            if 1 <= idx <= len(styles):
                selected = styles[idx - 1]
                console.print(f"[green]✓[/] Selected: [bold]{selected}[/]")
                return selected
        except ValueError:
            # Check if it's a style name
            if choice in styles:
                console.print(f"[green]✓[/] Selected: [bold]{choice}[/]")
                return choice

        console.print(f"[red]✗[/] Invalid choice. Please enter a number (1-{len(styles)}) or style name.")


def select_tempo(style_name: str) -> int:
    """Interactive tempo selection."""
    style = get_style(style_name)
    min_tempo, max_tempo = style.tempo_range
    default_tempo = style.default_tempo

    console.print()
    console.print(f"[bold]Tempo for {style_name}:[/]")
    console.print(f"  Range: [cyan]{min_tempo}-{max_tempo}[/] BPM")
    console.print(f"  Default: [yellow]{default_tempo}[/] BPM")
    console.print()

    while True:
        tempo = IntPrompt.ask(
            "Enter tempo (BPM)",
            default=default_tempo
        )

        if min_tempo <= tempo <= max_tempo:
            console.print(f"[green]✓[/] Tempo: [bold]{tempo}[/] BPM")
            return tempo
        else:
            console.print(f"[red]✗[/] Tempo must be between {min_tempo} and {max_tempo} BPM")


def select_measures() -> int:
    """Interactive measures selection."""
    console.print()
    console.print("[bold]Track Length:[/]")
    console.print("  [cyan]16[/] measures  = ~30 seconds")
    console.print("  [cyan]32[/] measures  = ~1 minute")
    console.print("  [cyan]64[/] measures  = ~2 minutes")
    console.print("  [cyan]128[/] measures = ~4 minutes")
    console.print("  [cyan]192[/] measures = ~6 minutes (default)")
    console.print()

    while True:
        measures = IntPrompt.ask(
            "Enter number of measures",
            default=192
        )

        if measures > 0 and measures <= 1000:
            console.print(f"[green]✓[/] Measures: [bold]{measures}[/]")
            return measures
        else:
            console.print("[red]✗[/] Please enter a value between 1 and 1000")


def select_swing(style_name: str) -> float:
    """Interactive swing selection."""
    style = get_style(style_name)
    default_swing = style.default_swing

    console.print()
    console.print("[bold]Swing/Groove Amount:[/]")
    console.print("  [cyan]0.0[/] = Straight (no swing)")
    console.print("  [cyan]0.3[/] = Light swing")
    console.print("  [cyan]0.5[/] = Triplet feel")
    console.print("  [cyan]0.7[/] = Heavy swing")
    console.print(f"  Style default: [yellow]{default_swing:.1f}[/]")
    console.print()

    use_default = Confirm.ask(
        f"Use default swing ({default_swing:.1f})?",
        default=True
    )

    if use_default:
        console.print(f"[green]✓[/] Swing: [bold]{default_swing:.1f}[/] (default)")
        return default_swing

    while True:
        try:
            swing_str = Prompt.ask(
                "Enter swing amount (0.0-1.0)",
                default=str(default_swing)
            )
            swing = float(swing_str)

            if 0.0 <= swing <= 1.0:
                console.print(f"[green]✓[/] Swing: [bold]{swing:.1f}[/]")
                return swing
            else:
                console.print("[red]✗[/] Swing must be between 0.0 and 1.0")
        except ValueError:
            console.print("[red]✗[/] Please enter a valid number")


def select_seed() -> int:
    """Interactive seed selection."""
    console.print()
    console.print("[bold]Random Seed:[/]")
    console.print("  Use a seed for reproducible generation")
    console.print("  Leave empty for random generation")
    console.print()

    use_seed = Confirm.ask("Use a specific seed?", default=False)

    if not use_seed:
        console.print("[green]✓[/] Using random seed")
        return None

    while True:
        seed = IntPrompt.ask("Enter seed (positive integer)")

        if seed >= 0:
            console.print(f"[green]✓[/] Seed: [bold]{seed}[/]")
            return seed
        else:
            console.print("[red]✗[/] Seed must be a positive integer")


def show_summary(config: Dict[str, Any]):
    """Display generation summary."""
    console.print()

    summary = f"""
[bold cyan]═══════════════════════════════════════[/]
[bold]Generation Configuration:[/]

  [bold]Style:[/]       [magenta]{config['style']}[/]
  [bold]Tempo:[/]       [yellow]{config['tempo']}[/] BPM
  [bold]Measures:[/]    [cyan]{config['measures']}[/]
  [bold]Swing:[/]       [green]{config.get('swing', 0.0):.1f}[/]
  [bold]Seed:[/]        [blue]{config.get('seed') if config.get('seed') is not None else 'random'}[/]

[bold cyan]═══════════════════════════════════════[/]
    """

    console.print(Panel(summary, border_style="cyan"))


def interactive_mode() -> Dict[str, Any]:
    """
    Run interactive mode and return configuration.

    Returns:
        Dictionary with user selections: style, tempo, measures, swing, seed
    """
    show_welcome()

    # Collect all parameters
    style = select_style()
    tempo = select_tempo(style)
    measures = select_measures()
    swing = select_swing(style)
    seed = select_seed()

    # Build configuration
    config = {
        'style': style,
        'tempo': tempo,
        'measures': measures,
        'swing': swing,
        'seed': seed
    }

    # Show summary
    show_summary(config)

    # Confirm generation
    console.print()
    if Confirm.ask("[bold]Proceed with generation?[/]", default=True):
        console.print()
        console.print("[bold green]Generating track...[/]")
        return config
    else:
        console.print("[yellow]Generation cancelled.[/]")
        return None
