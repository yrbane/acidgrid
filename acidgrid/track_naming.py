"""Creative and audacious track naming system for generated techno tracks."""

import random
from datetime import datetime


def generate_track_name() -> str:
    """Generate a creative, audacious name for a techno track."""
    
    # Different naming strategies with more attitude
    strategies = [
        _generate_dystopian_name,
        _generate_psychedelic_name,
        _generate_underground_name,
        _generate_futuristic_name,
        _generate_raw_energy_name,
        _generate_dark_poetry_name,
        _generate_rebel_name,
        _generate_cosmic_horror_name,
        _generate_machine_soul_name,
        _generate_chaos_name,
    ]
    
    strategy = random.choice(strategies)
    name = strategy()
    
    # Sometimes add special formatting
    if random.random() < 0.15:
        name = _add_special_format(name)
    
    # Clean the name for filesystem compatibility
    name = _clean_filename(name)
    
    return name


def _clean_filename(name: str) -> str:
    """Clean track name to be filesystem-safe."""
    import re
    
    # Replace problematic characters with safe alternatives
    replacements = {
        '/': '-',
        '\\': '-',
        ':': ' -',
        '*': 'x',
        '?': '',
        '"': "'",
        '<': '(',
        '>': ')',
        '|': 'I',
        '\0': '',
    }
    
    cleaned = name
    for bad_char, replacement in replacements.items():
        cleaned = cleaned.replace(bad_char, replacement)
    
    # Remove multiple consecutive spaces and trim
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Ensure the name isn't empty
    if not cleaned:
        cleaned = f"Track_{random.randint(1000, 9999)}"
    
    # Limit length for filesystem compatibility
    if len(cleaned) > 100:
        cleaned = cleaned[:97] + "..."
    
    return cleaned


def _generate_dystopian_name() -> str:
    """Generate dystopian/apocalyptic names."""
    prefixes = [
        "Death of", "Fall of", "Last", "Final", "Burning", "Toxic", "Radioactive",
        "Abandoned", "Corrupted", "Destroyed", "Forgotten", "Lost", "Dead"
    ]
    subjects = [
        "Paradise", "Utopia", "Tomorrow", "Dreams", "Hope", "Humanity", "Gods",
        "Angels", "Heaven", "Earth", "Reality", "Future", "Civilization"
    ]
    
    patterns = [
        lambda: f"{random.choice(prefixes)} {random.choice(subjects)}",
        lambda: f"When {random.choice(subjects)} Dies",
        lambda: f"After the {random.choice(subjects)}",
        lambda: f"No More {random.choice(subjects)}",
    ]
    
    return random.choice(patterns)()


def _generate_psychedelic_name() -> str:
    """Generate trippy, psychedelic names."""
    concepts = [
        "Acid Rain", "DMT Dreams", "Ego Death", "Third Eye", "Astral Projection",
        "Lucid Nightmare", "Chemical Romance", "Neural Meltdown", "Synaptic Overload",
        "Hallucination Engine", "Reality Dissolves", "Consciousness Leak", "Mind Virus"
    ]
    
    modifiers = [
        "Infinite", "Fractal", "Liquid", "Melting", "Twisted", "Warped", "Bleeding",
        "Pulsating", "Morphing", "Kaleidoscopic", "Transcendent", "Hyperdimensional"
    ]
    
    patterns = [
        lambda: random.choice(concepts),
        lambda: f"{random.choice(modifiers)} {random.choice(concepts).split()[1] if len(random.choice(concepts).split()) > 1 else random.choice(concepts)}",
        lambda: f"{random.choice(concepts)} {random.randint(1, 999):03d}",
    ]
    
    return random.choice(patterns)()


def _generate_underground_name() -> str:
    """Generate raw underground/rave names."""
    locations = [
        "Warehouse", "Bunker", "Tunnel", "Basement", "Squat", "Factory", 
        "Powerplant", "Sewers", "Catacombs", "Ruins", "Wasteland", "Underworld"
    ]
    
    actions = [
        "Rave", "Riot", "Revolution", "Resistance", "Rampage", "Ritual",
        "Massacre", "Mayhem", "Madness", "Meltdown", "Mutation", "Insurrection"
    ]
    
    patterns = [
        lambda: f"{random.choice(locations)} {random.choice(actions)}",
        lambda: f"Illegal {random.choice(actions)}",
        lambda: f"{random.randint(3, 6)}AM {random.choice(locations)}",
        lambda: f"Underground {random.choice(actions)} {random.randint(1, 99)}",
    ]
    
    return random.choice(patterns)()


def _generate_futuristic_name() -> str:
    """Generate cyberpunk/futuristic names."""
    tech = [
        "Cyborg", "Android", "AI", "Quantum", "Neural", "Cyber", "Digital",
        "Virtual", "Holographic", "Synthetic", "Bionic", "Nanotech", "Matrix"
    ]
    
    concepts = [
        "Uprising", "Singularity", "Apocalypse", "Revolution", "Extinction",
        "Evolution", "Transcendence", "Awakening", "Insurgency", "Prophecy"
    ]
    
    patterns = [
        lambda: f"{random.choice(tech)} {random.choice(concepts)}",
        lambda: f"Year {random.randint(2077, 3000)}",
        lambda: f"Sector {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}-{random.randint(100, 999)}",
        lambda: f"Protocol {random.randint(1, 999):03d}: {random.choice(concepts)}",
    ]
    
    return random.choice(patterns)()


def _generate_raw_energy_name() -> str:
    """Generate high-energy, aggressive names."""
    power = [
        "Voltage", "Overdrive", "Turbo", "Nitro", "Nuclear", "Atomic",
        "Explosive", "Volcanic", "Seismic", "Thunder", "Lightning", "Inferno"
    ]
    
    intensity = [
        "Overload", "Meltdown", "Breakdown", "Burnout", "Blackout", "Whiteout",
        "Surge", "Blast", "Impact", "Collision", "Detonation", "Eruption"
    ]
    
    patterns = [
        lambda: f"{random.choice(power)} {random.choice(intensity)}",
        lambda: f"Maximum {random.choice(power)}",
        lambda: f"{random.randint(1000, 9999)} {random.choice(['Volts', 'BPM', 'Hz', 'dB'])}",
        lambda: f"Critical {random.choice(intensity)}",
    ]
    
    return random.choice(patterns)()


def _generate_dark_poetry_name() -> str:
    """Generate dark, poetic names."""
    dark_concepts = [
        "Shadows Dance", "Darkness Falls", "Black Mirror", "Void Whispers",
        "Silent Scream", "Broken Wings", "Shattered Dreams", "Bleeding Stars",
        "Frozen Tears", "Dead Flowers", "Ghost Protocol", "Phantom Pain",
        "Soul Crusher", "Heart Eater", "Dream Killer", "Hope Destroyer"
    ]
    
    patterns = [
        lambda: random.choice(dark_concepts),
        lambda: f"The {random.choice(dark_concepts)}",
        lambda: f"{random.choice(dark_concepts)} (Remix from Hell)",
    ]
    
    return random.choice(patterns)()


def _generate_rebel_name() -> str:
    """Generate rebellious, anti-establishment names."""
    rebellious = [
        "Fuck the System", "Anarchy", "No Gods No Masters", "Riot Mode",
        "Revolution Calling", "Burn It Down", "Destroy Everything", "Total Chaos",
        "System Crash", "Rules Are Dead", "Authority Zero", "State of Emergency",
        "Martial Law", "Insurgent", "Sabotage", "Vandalism"
    ]
    
    patterns = [
        lambda: random.choice(rebellious),
        lambda: f"{random.choice(rebellious)} {datetime.now().year}",
        lambda: f"Operation: {random.choice(rebellious).split()[0]}",
    ]
    
    return random.choice(patterns)()


def _generate_cosmic_horror_name() -> str:
    """Generate cosmic horror inspired names."""
    cosmic = [
        "Event Horizon", "Black Hole Sun", "Stellar Collapse", "Cosmic Dread",
        "Void Crawler", "Space Madness", "Alien Frequency", "Unknown Signal",
        "Dark Matter", "Entropy Rising", "Heat Death", "Universal Decay",
        "Quantum Nightmare", "Dimensional Rift", "Time Collapse", "Reality Break"
    ]
    
    patterns = [
        lambda: random.choice(cosmic),
        lambda: f"Signal from {random.choice(['Proxima', 'Andromeda', 'Sagittarius', 'Cygnus'])} {random.choice(['A', 'B', 'X', 'Prime'])}",
        lambda: f"Transmission {random.randint(1, 999):03d}: {random.choice(['Contact', 'Warning', 'S.O.S', 'DANGER'])}",
    ]
    
    return random.choice(patterns)()


def _generate_machine_soul_name() -> str:
    """Generate machine/industrial names."""
    machine = [
        "Machine God", "Steel Heart", "Iron Will", "Chrome Dreams",
        "Mechanical Soul", "Digital Blood", "Silicon Brain", "Carbon Ghost",
        "Metal Fatigue", "Rust Never Sleeps", "Gears of War", "Engine Failure",
        "System Malfunction", "Core Breach", "Memory Leak", "Stack Overflow"
    ]
    
    patterns = [
        lambda: random.choice(machine),
        lambda: f"Unit {random.randint(1, 9999):04d} - {random.choice(['Online', 'Offline', 'Rogue', 'Awakened'])}",
        lambda: f"Error {random.randint(100, 999)}: {random.choice(['Critical', 'Fatal', 'Unknown', 'Recursive'])}",
    ]
    
    return random.choice(patterns)()


def _generate_chaos_name() -> str:
    """Generate pure chaos names."""
    chaos = [
        "Pure Fucking Chaos", "Absolute Madness", "Total Destruction",
        "Complete Annihilation", "Ultimate Violence", "Perfect Storm",
        "Savage Beauty", "Brutal Elegance", "Violent Delight", "Beautiful Disaster",
        "Organized Chaos", "Controlled Explosion", "Calculated Risk", "Measured Insanity"
    ]
    
    patterns = [
        lambda: random.choice(chaos),
        lambda: f"{random.choice(chaos)} v{random.randint(1, 9)}.{random.randint(0, 9)}",
        lambda: f"WARNING: {random.choice(chaos)}",
    ]
    
    return random.choice(patterns)()


def _add_special_format(name: str) -> str:
    """Add special formatting to make names more striking."""
    formats = [
        lambda n: f"[{n}]",
        lambda n: f"{{{n}}}",
        lambda n: f"///{n}///",
        lambda n: f"<{n}>",
        lambda n: f"!!! {n} !!!",
        lambda n: f"▓▓▓ {n} ▓▓▓",
        lambda n: f"◼◼◼ {n} ◼◼◼",
        lambda n: f"⚠ {n} ⚠",
        lambda n: f"☢ {n} ☢",
        lambda n: f"▶ {n} ◀",
        lambda n: n.upper(),
        lambda n: n.lower(),
        lambda n: n.replace(" ", "_"),
        lambda n: n.replace(" ", "."),
        lambda n: n.replace(" ", "-"),
        lambda n: n + " [UNMASTERED]",
        lambda n: n + " (LIVE RECORDING)",
        lambda n: n + " [BOOTLEG]",
        lambda n: n + " (WAREHOUSE DUB)",
        lambda n: n + " [303 ACID MIX]",
    ]
    
    return random.choice(formats)(name)