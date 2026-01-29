"""
Configuration file for SSVEP Stimulation
Modify these settings to customize your experiment
"""

# Target frequencies in Hz (modify these to your desired frequencies)
# Common SSVEP frequencies: 6-15 Hz range
TARGET_FREQUENCIES = [6, 7, 8, 10, 12, 13, 15]  # 7 frequencies

# Display settings
FULLSCREEN = True  # Set to False for windowed mode (useful for testing)
BACKGROUND_COLOR = [0, 0, 0]  # RGB values from -1 to 1 (black background)
MONITOR_NAME = 'testMonitor'  # Name for monitor configuration

# Stimulus properties
STIMULUS_SIZE = 200  # Size of each flickering square in pixels
STIMULUS_COLOR_ON = [1, 1, 1]  # White when ON
STIMULUS_COLOR_OFF = [-1, -1, -1]  # Black when OFF
STIMULUS_SHAPE = 'square'  # 'square' or 'circle'

# Stimulus positions (will be arranged in a grid)
# You can customize positions here if needed
# Format: list of (x, y) coordinates in pixels from center
# None = auto-arrange in grid
STIMULUS_POSITIONS = None

# Experiment settings
EXPERIMENT_DURATION = 60  # Duration in seconds (0 = run until ESC pressed)
SHOW_FREQUENCY_LABELS = True  # Show frequency labels above each stimulus

# Logging settings
ENABLE_LOGGING = True  # Log frame times for validation
LOG_FILENAME = 'ssvep_timing_log.csv'  # Output log file

# Timing validation
VALIDATE_TIMING = True  # Print timing report after experiment
TIMING_TOLERANCE = 0.05  # Acceptable deviation in Hz (±0.05 Hz)

# Instructions text
INSTRUCTION_TEXT = """SSVEP Flickering Stimulation

Focus on one of the flickering squares.

Controls:
- SPACE: Pause/Resume
- ESC: Quit

Press SPACE to begin..."""
