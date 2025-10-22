# ACIDGRID Remote Script for Ableton Live

Native Ableton Live integration for ACIDGRID - Generate MIDI clips directly in Ableton with MIDI controller support.

## Features

- **3 Generation Modes**:
  - Single mixed clip (all 5 tracks combined)
  - Full track generation (5 separate clips on 5 tracks)
  - Individual track generation (select specific track)

- **10 Music Styles**: House, Techno, Hard-Tekno, Breakbeat, IDM, Jungle, Hip-Hop, Trap, Ambient, Drum&Bass

- **5 Track Types**:
  1. Rhythm (20+ percussion instruments)
  2. Bassline (10 riff styles including 303 acid)
  3. Sub Bass (deep fundamental frequencies)
  4. Synth Accompaniment (chords, arpeggios, stabs)
  5. Synth Lead (4 melody styles)

- **MIDI Controller Mapping**: Works with any MIDI controller (Launchpad, Push, keyboard, etc.)

## Installation

1. Copy the entire `ACIDGRID` folder to your Ableton Remote Scripts directory:

   **macOS**:
   ```
   ~/Music/Ableton/User Library/Remote Scripts/ACIDGRID/
   ```

   **Windows**:
   ```
   %USERPROFILE%\Documents\Ableton\User Library\Remote Scripts\ACIDGRID\
   ```

   **Linux**:
   ```
   ~/Ableton/User Library/Remote Scripts/ACIDGRID/
   ```

2. Make sure the ACIDGRID Python package is accessible:
   - Install ACIDGRID: `pip install -e /path/to/acidgrid`
   - Or ensure the ACIDGRID repository is in a location accessible by Ableton

3. Restart Ableton Live

4. Enable the Remote Script:
   - Open Preferences → Link/Tempo/MIDI
   - Under "Control Surface", select "ACIDGRID" from the dropdown
   - Set Input/Output to your MIDI controller (or leave blank for keyboard input)

## MIDI Mapping Reference

### Style Selection (C4-A4)
Generate a single mixed clip with the selected style:

| Note | Style      | Color  |
|------|------------|--------|
| C4   | House      | Orange |
| C#4  | Techno     | Purple |
| D4   | Hard-Tekno | Red    |
| D#4  | Breakbeat  | Yellow |
| E4   | IDM        | Cyan   |
| F4   | Jungle     | Green  |
| F#4  | Hip-Hop    | Brown  |
| G4   | Trap       | Pink   |
| G#4  | Ambient    | Blue   |
| A4   | Drum&Bass  | Lime   |

### Individual Track Generation (C3-E3)
Generate a single track type on the selected Ableton track:

| Note | Track Type           | Description                    |
|------|---------------------|--------------------------------|
| C3   | Rhythm              | Drums and percussion           |
| C#3  | Bassline            | Bass riffs (including 303)     |
| D3   | Sub Bass            | Deep fundamental bass          |
| D#3  | Synth Accompaniment | Chords, arpeggios, stabs       |
| E3   | Synth Lead          | Melody and lead lines          |

### Full Track Generation (A5)
| Note | Action              | Description                              |
|------|---------------------|------------------------------------------|
| A5   | Generate Full Track | Creates 5 clips on 5 consecutive tracks  |

### Measure Presets (C5-E5)
Set the clip length in measures:

| Note | Measures |
|------|----------|
| C5   | 16       |
| C#5  | 32       |
| D5   | 64       |
| D#5  | 128      |
| E5   | 192      |

## Usage Workflows

### Workflow 1: Quick Single Clip Generation

1. Select an empty clip slot on any track
2. Press a style note (C4-A4, e.g., C#4 for Techno)
3. A mixed clip with all 5 tracks is generated in that slot

**Use case**: Quick jamming, sketching ideas

### Workflow 2: Full Track Generation

1. Optionally press a measure preset (C5-E5) to set length (default: 32 measures)
2. Select the first track where you want generation to start
3. Press **A5** to generate full track
4. 5 clips are created on 5 consecutive tracks:
   - Track 1: Rhythm
   - Track 2: Bassline
   - Track 3: Sub Bass
   - Track 4: Synth Accompaniment
   - Track 5: Synth Lead

**Use case**: Complete production workflow, separate track control

### Workflow 3: Individual Track Regeneration

1. Select the track you want to regenerate (e.g., Synth Lead)
2. Press the corresponding track note (e.g., E3 for Synth Lead)
3. Only that track is regenerated

**Use case**: Variation creation, A/B testing different basslines/leads

## Advanced Tips

### Creating Variations
1. Generate a full track (A5)
2. If you don't like the bassline, select the bassline track
3. Press C#3 to generate a new bassline variation
4. Repeat for any track until you find the perfect combination

### Building Complex Arrangements
1. Generate a full track at 16 measures (C5, then A5)
2. Create another variation by pressing A5 again
3. Arrange clips in Session View for a complete song structure
4. Use different styles for breakdown sections (e.g., Ambient for breakdown)

### Live Performance
1. Map your controller pads to different styles (C4-A4)
2. Use individual track generation (C3-E3) to create variations on-the-fly
3. Trigger different combinations for dynamic live sets

## MIDI Controller Setup Examples

### Launchpad
```
Row 1 (top):    A5 (full track), E5-C5 (measures)
Row 2:          A4-C4 (styles: Drum&Bass → House)
Row 3:          E3-C3 (tracks: Synth Lead → Rhythm)
```

### MIDI Keyboard
- Use C3-E3 for individual tracks
- Use C4-A4 for styles
- Use C5-E5 for measure presets
- Use A5 for full track generation

### Push/APC
Map the pads to the note ranges above for instant access to all functions.

## Troubleshooting

### "No module named 'acidgrid'" error
- Ensure ACIDGRID package is installed: `pip install -e /path/to/acidgrid`
- Check that Python environment is accessible to Ableton
- See Ableton's Log.txt for detailed error messages

### Clips not generating
- Check that you have an empty clip slot selected
- Verify the Remote Script is enabled in Preferences
- Look in Log.txt (Ableton menu → Help → Show Log.txt)

### MIDI notes not triggering
- Verify MIDI controller is connected in Preferences
- Check that the correct input is selected for ACIDGRID
- Test with computer keyboard (ensure track is armed with MIDI input)

## Technical Details

- **Harmonic Coherence**: All tracks share the same key, scale, and chord progression
- **Time Signatures**: Supports 3/4, 4/4, 5/4, 7/4, 6/8, 7/8, 9/8 (set via CLI, default: 4/4)
- **Song Structure**: Dynamic arrangement with intro, buildup, drop, breakdown, outro
- **Note Velocity**: Natural velocity curves with proper note-off velocities
- **303 Glide**: Authentic TB-303 portamento on acid basslines

## File Locations

- **Log file**: Check `Log.txt` in Ableton's preferences folder for debug output
- **Remote Script**: `~/Music/Ableton/User Library/Remote Scripts/ACIDGRID/`

## Support

For issues, feature requests, or contributions:
- GitHub: https://github.com/yrbane/acidgrid
- Check Log.txt for detailed error messages
- All MIDI messages are logged with `[ACIDGRID]` prefix

---

**Version**: 2.0
**Compatible with**: Ableton Live 10+
**License**: Same as ACIDGRID package
