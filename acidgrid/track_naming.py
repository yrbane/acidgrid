"""Creative and audacious track naming system for generated music tracks."""

import random
from datetime import datetime


def generate_track_name(style=None) -> str:
    """Generate a creative name for a track based on musical style.

    Args:
        style: MusicStyle object or None. If None, defaults to techno style.

    Returns:
        A creative track name appropriate for the style.
    """

    # Get style name
    style_name = style.name if style and hasattr(style, 'name') else 'techno'

    # Choose naming strategies based on style
    if style_name == 'house':
        strategies = _get_house_strategies()
    elif style_name == 'techno':
        strategies = _get_techno_strategies()
    elif style_name == 'hard-tekno':
        strategies = _get_hard_tekno_strategies()
    elif style_name == 'breakbeat':
        strategies = _get_breakbeat_strategies()
    elif style_name == 'idm':
        strategies = _get_idm_strategies()
    elif style_name == 'jungle':
        strategies = _get_jungle_strategies()
    elif style_name == 'hip-hop':
        strategies = _get_hiphop_strategies()
    elif style_name == 'trap':
        strategies = _get_trap_strategies()
    elif style_name == 'ambient':
        strategies = _get_ambient_strategies()
    elif style_name == 'drum&bass':
        strategies = _get_dnb_strategies()
    else:
        strategies = _get_techno_strategies()  # Default to techno

    strategy = random.choice(strategies)
    name = strategy()

    # Add special formatting based on style
    if random.random() < 0.15:
        name = _add_special_format(name, style_name)

    # Clean the name for filesystem compatibility
    name = _clean_filename(name)

    return name


def _get_house_strategies():
    """Get naming strategies for house music."""
    return [
        _generate_house_soulful,
        _generate_house_groovy,
        _generate_house_classic,
        _generate_house_disco,
    ]


def _get_techno_strategies():
    """Get naming strategies for techno music."""
    return [
        _generate_dystopian_name,
        _generate_underground_name,
        _generate_futuristic_name,
        _generate_machine_soul_name,
    ]


def _get_hard_tekno_strategies():
    """Get naming strategies for hard-tekno."""
    return [
        _generate_hard_tekno_aggressive,
        _generate_hard_tekno_distorted,
        _generate_chaos_name,
        _generate_raw_energy_name,
    ]


def _get_breakbeat_strategies():
    """Get naming strategies for breakbeat."""
    return [
        _generate_breakbeat_funky,
        _generate_breakbeat_urban,
        _generate_breakbeat_oldschool,
    ]


def _get_idm_strategies():
    """Get naming strategies for IDM."""
    return [
        _generate_idm_glitch,
        _generate_idm_complex,
        _generate_idm_experimental,
    ]


def _get_jungle_strategies():
    """Get naming strategies for jungle."""
    return [
        _generate_jungle_ragga,
        _generate_jungle_massive,
        _generate_jungle_classic,
    ]


def _get_hiphop_strategies():
    """Get naming strategies for hip-hop."""
    return [
        _generate_hiphop_boombap,
        _generate_hiphop_street,
        _generate_hiphop_classic,
    ]


def _get_trap_strategies():
    """Get naming strategies for trap."""
    return [
        _generate_trap_modern,
        _generate_trap_street,
        _generate_trap_808,
    ]


def _get_ambient_strategies():
    """Get naming strategies for ambient."""
    return [
        _generate_ambient_poetic,
        _generate_ambient_atmospheric,
        _generate_ambient_meditative,
    ]


def _get_dnb_strategies():
    """Get naming strategies for drum&bass."""
    return [
        _generate_dnb_liquid,
        _generate_dnb_neurofunk,
        _generate_dnb_jungle,
    ]


# ============= HOUSE NAMING STRATEGIES =============

def _generate_house_soulful() -> str:
    """Generate soulful house names."""
    feelings = ["Love", "Joy", "Soul", "Heart", "Spirit", "Feel", "Vibe", "Groove"]
    subjects = ["Music", "Rhythm", "Dance", "Night", "Day", "Life", "Dreams", "Paradise"]

    patterns = [
        lambda: f"{random.choice(feelings)} & {random.choice(subjects)}",
        lambda: f"Can You {random.choice(feelings)} It",
        lambda: f"{random.choice(subjects)} of {random.choice(feelings)}",
        lambda: f"Deep {random.choice(feelings)}",
    ]
    return random.choice(patterns)()


def _generate_house_groovy() -> str:
    """Generate groovy house names."""
    grooves = ["Funky", "Groovin", "Movin", "Shakin", "Bumpin", "Jumpin"]
    times = ["All Night", "Til Dawn", "Forever", "Right Now", "Tonight", "Today"]

    patterns = [
        lambda: f"{random.choice(grooves)} {random.choice(times)}",
        lambda: f"Let's Get {random.choice(grooves)}",
        lambda: f"{random.choice(grooves)} Sensation",
        lambda: f"Keep On {random.choice(grooves)}",
    ]
    return random.choice(patterns)()


def _generate_house_classic() -> str:
    """Generate classic house names."""
    classics = [
        "Music Is the Answer", "House Nation", "Move Your Body", "Can You Feel It",
        "Promised Land", "Show Me Love", "Strings of Life", "The Choice Is Yours",
        "Finally", "Lady", "Gypsy Woman", "Good Life"
    ]

    patterns = [
        lambda: random.choice(classics),
        lambda: f"{random.choice(classics)} (ACIDGRID Mix)",
        lambda: f"{random.choice(['Deep', 'Soulful', 'Jackin'])} House Anthem {random.randint(1, 99)}",
    ]
    return random.choice(patterns)()


def _generate_house_disco() -> str:
    """Generate disco-influenced house names."""
    disco = ["Disco", "Boogie", "Funk", "Rhythm", "Dancefloor", "Studio"]
    numbers = [54, 77, 84, 87, 88, 91, 94, 95, 97, 98, 99]

    patterns = [
        lambda: f"{random.choice(disco)} {random.choice(numbers)}",
        lambda: f"Le Freak (C'est {random.choice(['Chic', 'House', 'Deep'])})",
        lambda: f"{random.choice(disco)} Fever",
    ]
    return random.choice(patterns)()


# ============= HARD-TEKNO NAMING STRATEGIES =============

def _generate_hard_tekno_aggressive() -> str:
    """Generate aggressive hard-tekno names."""
    aggressive = [
        "DESTROY", "ANNIHILATE", "OBLITERATE", "DEVASTATE", "PULVERIZE", "DEMOLISH",
        "MUTILATE", "TERMINATE", "EXTERMINATE", "ERADICATE"
    ]
    targets = [
        "EVERYTHING", "ALL", "REALITY", "EXISTENCE", "THE SYSTEM", "THE WORLD",
        "SANITY", "LIMITS", "BOUNDARIES", "CONTROL"
    ]

    patterns = [
        lambda: f"{random.choice(aggressive)} {random.choice(targets)}",
        lambda: f"{random.randint(150, 200)} BPM {random.choice(aggressive)}",
        lambda: f"MAXIMUM {random.choice(aggressive)}",
    ]
    return random.choice(patterns)()


def _generate_hard_tekno_distorted() -> str:
    """Generate distorted hard-tekno names."""
    prefixes = ["X", "XXX", "XXXXX", "###", "*****", ">>", "<<", "//", "\\\\"]
    core = ["KICK", "BASS", "NOISE", "STATIC", "ERROR", "GLITCH", "CRASH", "BREAK"]
    suffixes = ["OVERLOAD", "DISTORTION", "SATURATION", "COMPRESSION", "CRUSH"]

    patterns = [
        lambda: f"{random.choice(prefixes)}{random.choice(core)}{random.choice(prefixes)}",
        lambda: f"{random.choice(core)} {random.choice(suffixes)} {random.randint(100, 999)}",
        lambda: f"[{random.choice(core)}] x{random.randint(3, 9)}",
    ]
    return random.choice(patterns)()


# ============= BREAKBEAT NAMING STRATEGIES =============

def _generate_breakbeat_funky() -> str:
    """Generate funky breakbeat names."""
    funky = ["Funky", "Groovy", "Jazzy", "Smooth", "Fresh", "Fly"]
    elements = ["Breaks", "Beats", "Drums", "Session", "Vibe", "Flow"]

    patterns = [
        lambda: f"{random.choice(funky)} {random.choice(elements)}",
        lambda: f"Amen Brother {random.randint(1, 99)}",
        lambda: f"Apache {random.choice(['Remix', 'Break', 'Flip', 'Edit'])}",
    ]
    return random.choice(patterns)()


def _generate_breakbeat_urban() -> str:
    """Generate urban breakbeat names."""
    urban = ["Block", "Street", "City", "Urban", "Underground", "Concrete"]
    actions = ["Bounce", "Move", "Roll", "Rock", "Shake", "Swing"]

    patterns = [
        lambda: f"{random.choice(urban)} {random.choice(actions)}",
        lambda: f"{random.choice(actions)} the {random.choice(urban)}",
        lambda: f"{random.choice(urban)} Beats Vol. {random.randint(1, 9)}",
    ]
    return random.choice(patterns)()


def _generate_breakbeat_oldschool() -> str:
    """Generate old school breakbeat names."""
    classics = [
        "Incredible Bongo Band", "Think Break", "Funky Drummer", "Cold Sweat",
        "Rockit", "Planet Rock", "Looking for the Perfect Beat"
    ]

    patterns = [
        lambda: f"{random.choice(classics)} (Flip)",
        lambda: f"90s {random.choice(['Jungle', 'Breakbeat', 'Big Beat'])} Style",
        lambda: f"Vintage Breaks {random.randint(91, 99)}",
    ]
    return random.choice(patterns)()


# ============= IDM NAMING STRATEGIES =============

def _generate_idm_glitch() -> str:
    """Generate glitchy IDM names."""
    glitches = ["glitch", "buffer", "overflow", "underflow", "null", "void", "NaN"]
    processes = ["process", "thread", "loop", "recursion", "iteration", "function"]

    patterns = [
        lambda: f"{random.choice(glitches)}.{random.choice(processes)}",
        lambda: f"[{random.choice(glitches)}:{random.randint(0, 99)}]",
        lambda: f"{random.choice(processes)}({random.choice(glitches)})",
    ]
    return random.choice(patterns)()


def _generate_idm_complex() -> str:
    """Generate complex IDM names."""
    math = ["fibonacci", "fractal", "algorithm", "polynomial", "matrix", "vector"]
    concepts = ["consciousness", "perception", "reality", "dimension", "infinity"]

    patterns = [
        lambda: f"{random.choice(math)}_{random.choice(concepts)}",
        lambda: f"{random.choice(concepts)}.{random.choice(['mp3', 'wav', 'flac', 'ogg'])}",
        lambda: f"{random.choice(math)}[{random.randint(1, 16)}]",
    ]
    return random.choice(patterns)()


def _generate_idm_experimental() -> str:
    """Generate experimental IDM names."""
    prefixes = ["exp", "test", "prototype", "alpha", "beta", "dev"]
    numbers = lambda: f"{random.randint(0, 9)}.{random.randint(0, 9)}.{random.randint(0, 99)}"

    patterns = [
        lambda: f"{random.choice(prefixes)}_{numbers()}",
        lambda: f"untitled_{random.randint(1, 999):03d}",
        lambda: f"draft_{random.randint(1, 99)}_{random.choice(['a', 'b', 'c', 'd'])}",
    ]
    return random.choice(patterns)()


# ============= JUNGLE NAMING STRATEGIES =============

def _generate_jungle_ragga() -> str:
    """Generate ragga jungle names."""
    ragga = ["Bun Dem", "Champion Sound", "Original", "Wicked", "Junglist", "Rude Boy"]
    massive = ["Massive", "Heavyweight", "Thunder", "Sound Boy", "Big Up"]

    patterns = [
        lambda: f"{random.choice(ragga)} {random.choice(massive)}",
        lambda: f"Inna {random.choice(['Jungle', 'Dancehall', 'Sound System'])}",
        lambda: f"{random.choice(massive)} Business",
    ]
    return random.choice(patterns)()


def _generate_jungle_massive() -> str:
    """Generate massive jungle names."""
    descriptors = ["Super Sharp", "Incredible", "The Original", "Deadly"]
    elements = ["Shooter", "Killa", "Murderer", "Destroyer"]

    patterns = [
        lambda: f"{random.choice(descriptors)} {random.choice(elements)}",
        lambda: f"Pulp Fiction (Jungle {random.choice(['VIP', 'Remix', 'Mix'])})",
        lambda: f"Valley of the Shadows {random.randint(1, 9)}",
    ]
    return random.choice(patterns)()


def _generate_jungle_classic() -> str:
    """Generate classic jungle names."""
    classics = [
        "Atlantis", "Terrorist", "Pulp Fiction", "Incredible", "Original Nuttah",
        "Super Sharp Shooter", "Renegade Snares", "Music"
    ]

    patterns = [
        lambda: random.choice(classics),
        lambda: f"{random.choice(classics)} (Remix)",
        lambda: f"Sound of the {random.choice(['Jungle', 'Drums', 'Underground'])}",
    ]
    return random.choice(patterns)()


# ============= HIP-HOP NAMING STRATEGIES =============

def _generate_hiphop_boombap() -> str:
    """Generate boom bap hip-hop names."""
    descriptors = ["Raw", "Rough", "Rugged", "Hard", "Heavy", "Dirty"]
    elements = ["Beats", "Rhymes", "Drums", "Bass", "Loops", "Samples"]

    patterns = [
        lambda: f"{random.choice(descriptors)} {random.choice(elements)}",
        lambda: f"Boom Bap {random.choice(['Session', 'Chronicles', 'Files', 'Vol'])} {random.randint(1, 9)}",
        lambda: f"{random.choice(descriptors)} & {random.choice(descriptors)}",
    ]
    return random.choice(patterns)()


def _generate_hiphop_street() -> str:
    """Generate street hip-hop names."""
    locations = ["Brooklyn", "Queens", "Bronx", "Harlem", "Southside", "Westside"]
    vibes = ["State of Mind", "Story", "Dreams", "Nights", "Days", "Life"]

    patterns = [
        lambda: f"{random.choice(locations)} {random.choice(vibes)}",
        lambda: f"Straight Outta {random.choice(locations)}",
        lambda: f"The {random.choice(vibes)}",
    ]
    return random.choice(patterns)()


def _generate_hiphop_classic() -> str:
    """Generate classic hip-hop references."""
    classics = [
        "93 Til Infinity", "The World Is Yours", "It Was a Good Day",
        "C.R.E.A.M.", "Shook Ones", "Electric Relaxation", "Award Tour"
    ]

    patterns = [
        lambda: random.choice(classics),
        lambda: f"Golden Era {random.randint(88, 99)}",
        lambda: f"SP-1200 {random.choice(['Sessions', 'Beats', 'Files'])}",
    ]
    return random.choice(patterns)()


# ============= TRAP NAMING STRATEGIES =============

def _generate_trap_modern() -> str:
    """Generate modern trap names."""
    modern = ["Flex", "Sauce", "Wave", "Mood", "Vibe", "Energy", "Drip"]
    intensifiers = ["Too", "So", "Real", "Big", "Hard", "Different"]

    patterns = [
        lambda: f"{random.choice(intensifiers)} {random.choice(modern)}",
        lambda: f"{random.choice(modern)} Mode",
        lambda: f"No {random.choice(['Cap', 'Limit', 'Chill', 'Sleep'])}",
    ]
    return random.choice(patterns)()


def _generate_trap_street() -> str:
    """Generate street trap names."""
    elements = ["Bankroll", "Traphouse", "Mob", "Gang", "Squad", "Crew"]
    actions = ["Run It", "Get It", "Stack It", "Count It", "Flip It"]

    patterns = [
        lambda: f"{random.choice(elements)} {random.choice(actions)}",
        lambda: f"{random.choice(actions)} Up",
        lambda: f"In the {random.choice(['Trap', 'Lab', 'Studio', 'Streets'])}",
    ]
    return random.choice(patterns)()


def _generate_trap_808() -> str:
    """Generate 808-focused trap names."""
    descriptors = ["Knockin", "Bangin", "Slappin", "Bumpin", "Hittin"]
    elements = ["808", "Bass", "Sub", "Kick", "Beat"]

    patterns = [
        lambda: f"{random.choice(descriptors)} {random.choice(elements)}s",
        lambda: f"{random.choice(elements)} {random.choice(['God', 'Mafia', 'Cartel'])}",
        lambda: f"808s & {random.choice(['Heartbreak', 'Hi-Hats', 'Snares'])}",
    ]
    return random.choice(patterns)()


# ============= AMBIENT NAMING STRATEGIES =============

def _generate_ambient_poetic() -> str:
    """Generate poetic ambient names."""
    atmospheres = ["Distant", "Fading", "Drifting", "Floating", "Suspended", "Dissolving"]
    subjects = ["Memories", "Horizons", "Echoes", "Reflections", "Dreams", "Stars"]

    patterns = [
        lambda: f"{random.choice(atmospheres)} {random.choice(subjects)}",
        lambda: f"The {random.choice(subjects)} of {random.choice(['Time', 'Space', 'Light', 'Silence'])}",
        lambda: f"Between {random.choice(subjects)}",
    ]
    return random.choice(patterns)()


def _generate_ambient_atmospheric() -> str:
    """Generate atmospheric ambient names."""
    environments = ["Ocean", "Sky", "Forest", "Mountain", "Desert", "Tundra"]
    times = ["Dawn", "Dusk", "Midnight", "Twilight", "Morning", "Evening"]

    patterns = [
        lambda: f"{random.choice(environments)} at {random.choice(times)}",
        lambda: f"Alone in the {random.choice(environments)}",
        lambda: f"{random.choice(times)} {random.choice(['Meditation', 'Contemplation', 'Reverie'])}",
    ]
    return random.choice(patterns)()


def _generate_ambient_meditative() -> str:
    """Generate meditative ambient names."""
    states = ["Peace", "Calm", "Serenity", "Stillness", "Tranquility", "Silence"]
    concepts = ["Within", "Beyond", "Eternal", "Infinite", "Deep", "Pure"]

    patterns = [
        lambda: f"{random.choice(concepts)} {random.choice(states)}",
        lambda: f"Journey to {random.choice(states)}",
        lambda: f"The Sound of {random.choice(states)}",
    ]
    return random.choice(patterns)()


# ============= DRUM & BASS NAMING STRATEGIES =============

def _generate_dnb_liquid() -> str:
    """Generate liquid drum & bass names."""
    liquid = ["Liquid", "Smooth", "Silky", "Velvet", "Crystal", "Pure"]
    feelings = ["Soul", "Emotions", "Dreams", "Thoughts", "Memories", "Love"]

    patterns = [
        lambda: f"{random.choice(liquid)} {random.choice(feelings)}",
        lambda: f"{random.choice(feelings)} in Motion",
        lambda: f"Floating {random.choice(feelings)}",
    ]
    return random.choice(patterns)()


def _generate_dnb_neurofunk() -> str:
    """Generate neurofunk drum & bass names."""
    neuro = ["Neuro", "Tech", "Dark", "Deep", "Heavy", "Complex"]
    descriptors = ["Synthesis", "Algorithm", "Protocol", "Function", "Process", "System"]

    patterns = [
        lambda: f"{random.choice(neuro)} {random.choice(descriptors)}",
        lambda: f"{random.choice(descriptors)} {random.randint(1, 999):03d}",
        lambda: f"Deep {random.choice(neuro)}",
    ]
    return random.choice(patterns)()


def _generate_dnb_jungle() -> str:
    """Generate jungle-influenced drum & bass names."""
    jungle = ["Amen", "Reese", "Hoover", "Mentasm", "Breakbeat"]
    actions = ["Pressure", "Power", "Energy", "Force", "Impact"]

    patterns = [
        lambda: f"{random.choice(jungle)} {random.choice(actions)}",
        lambda: f"{random.choice(actions)} Drop",
        lambda: f"Rolling {random.choice(jungle)}",
    ]
    return random.choice(patterns)()


# ============= UTILITY FUNCTIONS =============

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


def _add_special_format(name: str, style_name: str = 'techno') -> str:
    """Add special formatting to make names more striking based on style."""

    # Style-specific formatting
    style_formats = {
        'house': [
            lambda n: f"♫ {n} ♫",
            lambda n: f"★ {n} ★",
            lambda n: n + " (Extended Mix)",
            lambda n: n + " (Club Mix)",
            lambda n: n + " (Dub)",
        ],
        'techno': [
            lambda n: f"[{n}]",
            lambda n: f"▶ {n} ◀",
            lambda n: n + " [UNMASTERED]",
            lambda n: n + " [303 ACID MIX]",
        ],
        'hard-tekno': [
            lambda n: f"!!! {n} !!!",
            lambda n: f"▓▓▓ {n} ▓▓▓",
            lambda n: f"☢ {n} ☢",
            lambda n: n.upper(),
        ],
        'breakbeat': [
            lambda n: f"[{n}]",
            lambda n: n + " (Breaks)",
            lambda n: n + " - Original",
        ],
        'idm': [
            lambda n: n.lower().replace(" ", "_"),
            lambda n: n.lower().replace(" ", "."),
            lambda n: f"[{n.lower()}]",
        ],
        'jungle': [
            lambda n: f">>> {n} <<<",
            lambda n: n + " (Jungle Mix)",
            lambda n: n + " VIP",
        ],
        'hip-hop': [
            lambda n: n + " (Instrumental)",
            lambda n: n + " [SP-1200]",
            lambda n: f"** {n} **",
        ],
        'trap': [
            lambda n: f"💎 {n}",
            lambda n: f"🔥 {n} 🔥",
            lambda n: n + " [BANGER]",
        ],
        'ambient': [
            lambda n: f"~ {n} ~",
            lambda n: f"∞ {n}",
            lambda n: n + " (Meditation)",
        ],
        'drum&bass': [
            lambda n: f"▶▶ {n}",
            lambda n: n + " (Liquid)",
            lambda n: n + " (Neurofunk)",
        ],
    }

    # Get formats for this style or use default
    formats = style_formats.get(style_name, style_formats['techno'])

    return random.choice(formats)(name)