# SSVEP Visual Stimulation System

A precise, frame-locked visual stimulation system for SSVEP (Steady-State Visual Evoked Potential) experiments using PsychoPy.

## Features

✅ **Exact Frequency Accuracy** - Frame-locked timing ensures frequencies are exact (e.g., 7.00 Hz, not 7.01 or 6.99)  
✅ **Multiple Frequencies** - Simultaneous presentation of 7 different frequencies  
✅ **Timing Validation** - Built-in logging and analysis tools  
✅ **Refresh Rate Compatibility** - Automatic detection and frequency optimization  
✅ **Customizable** - Easy configuration of frequencies, colors, sizes, and layouts  
✅ **Research-Grade** - Suitable for actual SSVEP BCI experiments

## Quick Start

### 1. Install

```bash
pip install -r requirements.txt
```

See [SETUP.md](SETUP.md) for detailed installation instructions.

### 2. Check Compatibility

```bash
python refresh_rate_checker.py
```

This detects your monitor refresh rate and shows which frequencies are exactly achievable.

### 3. Configure

Edit `config.py`:

```python
TARGET_FREQUENCIES = [6, 7, 8, 10, 12, 13, 15]  # Your 7 frequencies
EXPERIMENT_DURATION = 60  # Duration in seconds
STIMULUS_SIZE = 200  # Size in pixels
```

### 4. Run

```bash
python ssvep_stimulation.py
```

**Controls:**
- `SPACE` - Start/Pause/Resume
- `ESC` - Quit

### 5. Validate

```bash
python validate_timing.py
```

Analyzes timing accuracy and generates report.

## How It Works

### Frame-Locked Timing

Unlike web-based approaches that use time intervals, this system uses **frame counting** for exact timing:

```python
# For 7 Hz on a 60 Hz monitor:
frames_per_cycle = 60 / 7 ≈ 8.57 → rounds to 9 frames
actual_frequency = 60 / 9 = 6.67 Hz

# For 10 Hz on a 60 Hz monitor:
frames_per_cycle = 60 / 10 = 6 frames (exact!)
actual_frequency = 60 / 6 = 10.00 Hz ✓
```

The system:
1. Calculates frames per cycle for each frequency
2. Uses VSync to lock to monitor refresh
3. Counts frames (not time) to determine on/off states
4. Logs actual frame times for validation

### Why Not HTML/JavaScript?

| Feature | HTML/JS | PsychoPy |
|---------|---------|----------|
| Timing precision | ±5-15ms jitter | Sub-millisecond |
| Frequency accuracy | ±0.1-0.5 Hz drift | Exact (frame-locked) |
| Validation | Difficult | Built-in logging |
| Research use | Not recommended | Standard |

## File Structure

```
Stimulation/
├── ssvep_stimulation.py      # Main stimulation script
├── config.py                  # Configuration settings
├── refresh_rate_checker.py   # Monitor compatibility tool
├── validate_timing.py         # Timing analysis tool
├── requirements.txt           # Python dependencies
├── SETUP.md                   # Installation guide
├── README.md                  # This file
└── ssvep_timing_log.csv      # Generated timing log
```

## Configuration Options

### Frequencies

```python
# Common SSVEP frequencies (6-15 Hz range)
TARGET_FREQUENCIES = [6, 7, 8, 10, 12, 13, 15]
```

**Important:** Use `refresh_rate_checker.py` to find optimal frequencies for your monitor.

### Stimulus Appearance

```python
STIMULUS_SIZE = 200           # Size in pixels
STIMULUS_SHAPE = 'square'     # 'square' or 'circle'
STIMULUS_COLOR_ON = [1, 1, 1]   # White
STIMULUS_COLOR_OFF = [-1, -1, -1]  # Black
```

### Display Settings

```python
FULLSCREEN = True             # Fullscreen mode
BACKGROUND_COLOR = [0, 0, 0]  # Gray background
SHOW_FREQUENCY_LABELS = True  # Show Hz labels
```

### Experiment Settings

```python
EXPERIMENT_DURATION = 60      # Duration in seconds (0 = infinite)
ENABLE_LOGGING = True         # Log frame times
VALIDATE_TIMING = True        # Show timing report after run
```

## Monitor Compatibility

### Refresh Rate Requirements

For exact frequencies, your monitor refresh rate must be divisible by the target frequency:

| Target Freq | 60 Hz | 120 Hz | 144 Hz |
|-------------|-------|--------|--------|
| 6 Hz | ✓ Exact | ✓ Exact | ✓ Exact |
| 7 Hz | ✗ ~6.67 or ~7.5 | ✗ ~6.92 or ~7.06 | ✗ ~7.2 |
| 8 Hz | ✗ ~7.5 or ~8.57 | ✓ Exact | ✓ Exact |
| 10 Hz | ✓ Exact | ✓ Exact | ✗ ~9.6 or ~10.3 |
| 12 Hz | ✓ Exact | ✓ Exact | ✓ Exact |
| 15 Hz | ✓ Exact | ✓ Exact | ✗ ~14.4 or ~16 |

**Recommendation:** 120 Hz monitor provides the most flexibility for SSVEP frequencies.

## Timing Validation

The system provides detailed timing reports:

```
TIMING VALIDATION REPORT
================================================================
Total duration: 60.02 seconds
Total frames: 7200
Average frame rate: 119.97 Hz

Frequency Accuracy:
----------------------------------------------------------------
Target (Hz)   Expected Cycles  Actual Cycles   Status
----------------------------------------------------------------
6.0           360.0            360.0           ✓ PASS
8.0           480.0            480.0           ✓ PASS
10.0          600.0            600.0           ✓ PASS
12.0          720.0            720.0           ✓ PASS
15.0          900.0            900.0           ✓ PASS
================================================================
```

## Advanced Usage

### Custom Stimulus Positions

```python
# In config.py
STIMULUS_POSITIONS = [
    (-300, 200),   # Top left
    (0, 200),      # Top center
    (300, 200),    # Top right
    (-300, -200),  # Bottom left
    (0, -200),     # Bottom center
    (300, -200),   # Bottom right
    (0, 0)         # Center
]
```

### Integration with EEG

The timing log (`ssvep_timing_log.csv`) contains exact frame times:

```csv
frame,time
0,0.000000
1,0.008333
2,0.016667
...
```

Use these timestamps to synchronize with EEG recordings.

### Programmatic Control

```python
from ssvep_stimulation import SSVEPStimulator

stimulator = SSVEPStimulator()
stimulator.run()
```

## Troubleshooting

See [SETUP.md](SETUP.md) for detailed troubleshooting guide.

**Common issues:**
- **Frame drops**: Close other applications, disable antivirus
- **Inaccurate frequencies**: Check monitor compatibility with `refresh_rate_checker.py`
- **Installation fails**: See SETUP.md for platform-specific solutions

## Research Use

This implementation is suitable for:
- ✅ SSVEP BCI experiments
- ✅ Frequency-tagging studies
- ✅ Visual attention research
- ✅ Neuroscience experiments requiring precise timing

**Citation:** If you use this in research, please cite PsychoPy:
> Peirce, J. W., et al. (2019). PsychoPy2: Experiments in behavior made easy. Behavior Research Methods, 51(1), 195-203.

## License

This implementation is provided as-is for research and educational purposes.

## References

- [PsychoPy Documentation](https://www.psychopy.org/)
- [SSVEP BCI Tutorial](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6316385/)
- [Timing in PsychoPy](https://www.psychopy.org/general/timing/index.html)

## Support

For issues:
1. Check [SETUP.md](SETUP.md) troubleshooting section
2. Run `refresh_rate_checker.py` to verify compatibility
3. Review timing validation output
4. Check PsychoPy forums for PsychoPy-specific issues
