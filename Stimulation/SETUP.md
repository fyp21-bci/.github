# SSVEP Stimulation Setup Guide

This guide will help you install and configure the PsychoPy-based SSVEP stimulation system.

## Prerequisites

- **Python 3.8 or higher** (Python 3.9-3.11 recommended)
- **Windows, macOS, or Linux**
- **Monitor with known refresh rate** (60 Hz, 120 Hz, or 144 Hz common)

## Installation Steps

### 1. Install Python (if not already installed)

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"
- Verify: Open PowerShell and type `python --version`

**macOS:**
```bash
brew install python@3.11
```

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2. Install Dependencies

Open terminal/PowerShell in the `Stimulation` directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- PsychoPy (stimulus presentation)
- NumPy (numerical computations)
- Pandas (data logging)

**Note:** PsychoPy installation may take several minutes as it has many dependencies.

### 3. Verify Installation

Test that PsychoPy is installed correctly:

```bash
python -c "from psychopy import visual, core; print('PsychoPy installed successfully!')"
```

## Configuration

### 1. Check Your Monitor Refresh Rate

**Windows:**
1. Right-click Desktop → Display Settings
2. Advanced Display Settings
3. Look for "Refresh rate"

**macOS:**
1. System Preferences → Displays
2. Hold Option key and click "Scaled"
3. Look for refresh rate

**Linux:**
```bash
xrandr | grep "*"
```

### 2. Run Refresh Rate Checker

Verify your monitor's refresh rate and check frequency compatibility:

```bash
python refresh_rate_checker.py
```

This will:
- Detect your actual refresh rate
- Show which of your target frequencies are exactly achievable
- Suggest optimal frequencies for your monitor

### 3. Configure Your Experiment

Edit `config.py` to customize:

```python
# Your 7 target frequencies (in Hz)
TARGET_FREQUENCIES = [6, 7, 8, 10, 12, 13, 15]

# Experiment duration (0 = run until ESC pressed)
EXPERIMENT_DURATION = 60  # seconds

# Stimulus appearance
STIMULUS_SIZE = 200  # pixels
STIMULUS_SHAPE = 'square'  # or 'circle'

# Display settings
FULLSCREEN = True  # Set False for testing
```

## Running the Stimulation

### Basic Usage

```bash
python ssvep_stimulation.py
```

**Controls:**
- `SPACE` - Start/Pause/Resume
- `ESC` - Quit experiment

### Workflow

1. **Test first**: Set `FULLSCREEN = False` in `config.py` for testing
2. **Check timing**: Run for 60 seconds and review the timing report
3. **Validate**: Run `python validate_timing.py` to analyze accuracy
4. **Adjust if needed**: Modify frequencies based on compatibility report
5. **Run experiment**: Set `FULLSCREEN = True` for actual use

## Timing Validation

After running the stimulation, validate timing accuracy:

```bash
python validate_timing.py
```

This analyzes the log file and reports:
- Actual frequencies achieved
- Frame interval statistics
- Frame drops (if any)
- Timing accuracy vs. targets

## Troubleshooting

### Issue: "Could not detect refresh rate"

**Solution:** 
- Manually set in code: Edit `ssvep_stimulation.py`, find `self.refresh_rate = 60.0` and set your known rate
- Try running in fullscreen mode
- Update graphics drivers

### Issue: Frequencies not exact

**Cause:** Monitor refresh rate incompatible with target frequencies

**Solution:**
1. Run `refresh_rate_checker.py`
2. Use suggested optimal frequencies
3. Or get a monitor with compatible refresh rate (120 Hz ideal for most SSVEP frequencies)

### Issue: Frame drops detected

**Causes:**
- Other programs running (close unnecessary apps)
- Insufficient graphics performance
- Background processes

**Solutions:**
- Close all other applications
- Disable antivirus during experiment
- Use dedicated graphics card (not integrated)
- Reduce `STIMULUS_SIZE` in config.py

### Issue: PsychoPy installation fails

**Windows specific:**
```bash
pip install --upgrade pip setuptools wheel
pip install psychopy
```

**If still failing:**
- Install Microsoft Visual C++ Redistributable
- Try installing in a virtual environment:
  ```bash
  python -m venv venv
  venv\Scripts\activate  # Windows
  # source venv/bin/activate  # macOS/Linux
  pip install -r requirements.txt
  ```

## Monitor Recommendations

For best results with SSVEP frequencies (6-15 Hz):

| Refresh Rate | Best For | Exact Frequencies (examples) |
|--------------|----------|------------------------------|
| **60 Hz** | Budget | 6, 10, 12, 15 Hz |
| **120 Hz** | Recommended | 6, 8, 10, 12, 15 Hz (most flexible) |
| **144 Hz** | High-end | 6, 8, 9, 12 Hz |

**Note:** 7 Hz requires 140 Hz or 70 Hz monitor for perfect accuracy. On 60 Hz, it will be ~7.5 Hz or ~6.67 Hz.

## Next Steps

1. ✅ Install Python and dependencies
2. ✅ Run `refresh_rate_checker.py`
3. ✅ Configure `config.py` with optimal frequencies
4. ✅ Test with `FULLSCREEN = False`
5. ✅ Validate timing with `validate_timing.py`
6. ✅ Run full experiment

## Support

For issues specific to:
- **PsychoPy**: [PsychoPy Forum](https://discourse.psychopy.org/)
- **This implementation**: Check the README.md or create an issue

## References

- [PsychoPy Documentation](https://www.psychopy.org/documentation.html)
- [SSVEP BCI Overview](https://en.wikipedia.org/wiki/Steady_state_visually_evoked_potential)
