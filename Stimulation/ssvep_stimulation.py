"""
SSVEP Visual Stimulation System with Frame-Locked Timing

This script presents multiple flickering stimuli at precise frequencies
for SSVEP (Steady-State Visual Evoked Potential) experiments.

Key features:
- Frame-locked timing for exact frequency accuracy
- Multiple simultaneous frequencies
- Timing validation and logging
- Keyboard controls for experiment management
"""

from psychopy import visual, core, event, monitors
import numpy as np
import pandas as pd
from datetime import datetime
import config


class SSVEPStimulator:
    """Manages SSVEP flickering stimulation with precise timing."""
    
    def __init__(self):
        """Initialize the stimulator with configuration from config.py"""
        self.frequencies = config.TARGET_FREQUENCIES
        self.setup_monitor()
        self.setup_window()
        self.calculate_frame_cycles()
        self.create_stimuli()
        self.frame_log = []
        self.paused = False
        self.frame_count = 0
        
    def setup_monitor(self):
        """Setup monitor configuration."""
        self.mon = monitors.Monitor(config.MONITOR_NAME)
        
    def setup_window(self):
        """Create the display window."""
        self.win = visual.Window(
            fullscr=config.FULLSCREEN,
            color=config.BACKGROUND_COLOR,
            units='pix',
            monitor=self.mon,
            allowGUI=not config.FULLSCREEN,
            waitBlanking=True  # Enable V-Sync to prevent screen tearing
        )
        
        # Get actual refresh rate
        self.refresh_rate = self.win.getActualFrameRate(nIdentical=60, nWarmUpFrames=10)
        
        if self.refresh_rate is None:
            print("Warning: Could not detect refresh rate. Using 60 Hz default.")
            self.refresh_rate = 60.0
        else:
            print(f"Detected refresh rate: {self.refresh_rate:.2f} Hz")
        
    def calculate_frame_cycles(self):
        """
        Calculate frame counts for each frequency.
        This is the key to exact timing - we use discrete frames, not time intervals.
        """
        self.frame_cycles = {}
        
        print("\nFrequency Configuration:")
        print("-" * 60)
        print(f"{'Target (Hz)':<12} {'Frames/Cycle':<15} {'Actual (Hz)':<12} {'Error':<10}")
        print("-" * 60)
        
        for freq in self.frequencies:
            # Calculate frames per full cycle (on + off)
            frames_per_cycle = self.refresh_rate / freq
            frames_per_cycle_int = round(frames_per_cycle)
            
            # Calculate actual achieved frequency
            actual_freq = self.refresh_rate / frames_per_cycle_int
            error = abs(actual_freq - freq)
            
            self.frame_cycles[freq] = frames_per_cycle_int
            
            # Print configuration
            error_str = f"±{error:.3f} Hz"
            print(f"{freq:<12.1f} {frames_per_cycle_int:<15} {actual_freq:<12.3f} {error_str:<10}")
        
        print("-" * 60)
        print()
        
    def create_stimuli(self):
        """Create visual stimuli for each frequency."""
        n_stim = len(self.frequencies)
        
        # Calculate grid positions if not specified
        if config.STIMULUS_POSITIONS is None:
            positions = self._calculate_grid_positions(n_stim)
        else:
            positions = config.STIMULUS_POSITIONS
        
        self.stimuli = []
        self.labels = []
        
        for i, (freq, pos) in enumerate(zip(self.frequencies, positions)):
            # Create stimulus
            if config.STIMULUS_SHAPE == 'circle':
                stim = visual.Circle(
                    self.win,
                    radius=config.STIMULUS_SIZE / 2,
                    pos=pos,
                    fillColor=config.STIMULUS_COLOR_OFF,
                    lineColor=None
                )
            else:  # square
                stim = visual.Rect(
                    self.win,
                    width=config.STIMULUS_SIZE,
                    height=config.STIMULUS_SIZE,
                    pos=pos,
                    fillColor=config.STIMULUS_COLOR_OFF,
                    lineColor=None
                )
            
            self.stimuli.append(stim)
            
            # Create label
            if config.SHOW_FREQUENCY_LABELS:
                label = visual.TextStim(
                    self.win,
                    text=f"{freq} Hz",
                    pos=(pos[0], pos[1] + config.STIMULUS_SIZE / 2 + 30),
                    height=20,
                    color=[1, 1, 1]
                )
                self.labels.append(label)
    
    def _calculate_grid_positions(self, n_stim):
        """Calculate grid positions for stimuli."""
        # Determine grid dimensions
        if n_stim <= 3:
            rows, cols = 1, n_stim
        elif n_stim <= 6:
            rows, cols = 2, (n_stim + 1) // 2
        else:
            rows, cols = 3, (n_stim + 2) // 3
        
        # Calculate spacing
        win_width, win_height = self.win.size
        spacing_x = win_width / (cols + 1)
        spacing_y = win_height / (rows + 1)
        
        # Generate positions
        positions = []
        for i in range(n_stim):
            row = i // cols
            col = i % cols
            
            # Center the grid
            x = spacing_x * (col + 1) - win_width / 2
            y = win_height / 2 - spacing_y * (row + 1)
            
            positions.append((x, y))
        
        return positions
    
    def should_flicker_on(self, freq, frame_num):
        """
        Determine if stimulus should be ON for this frame.
        Uses frame counting for exact timing.
        
        Args:
            freq: Target frequency
            frame_num: Current frame number
        
        Returns:
            True if stimulus should be ON, False if OFF
        """
        frames_per_cycle = self.frame_cycles[freq]
        
        # Position within cycle
        cycle_position = frame_num % frames_per_cycle
        
        # ON for first half of cycle, OFF for second half
        return cycle_position < frames_per_cycle / 2
    
    def update_stimuli(self):
        """Update all stimuli based on current frame."""
        for stim, freq in zip(self.stimuli, self.frequencies):
            if self.should_flicker_on(freq, self.frame_count):
                stim.fillColor = config.STIMULUS_COLOR_ON
            else:
                stim.fillColor = config.STIMULUS_COLOR_OFF
    
    def draw_all(self):
        """Draw all stimuli and labels."""
        for stim in self.stimuli:
            stim.draw()
        
        if config.SHOW_FREQUENCY_LABELS:
            for label in self.labels:
                label.draw()
    
    def show_instructions(self):
        """Display instruction screen."""
        instruction_text = visual.TextStim(
            self.win,
            text=config.INSTRUCTION_TEXT,
            height=30,
            color=[1, 1, 1],
            wrapWidth=self.win.size[0] * 0.8
        )
        
        instruction_text.draw()
        self.win.flip()
        
        # Wait for space bar
        event.waitKeys(keyList=['space'])
    
    def run(self):
        """Run the stimulation experiment."""
        print("\nStarting SSVEP Stimulation...")
        print("Press ESC to quit, SPACE to pause/resume\n")
        
        # Show instructions
        self.show_instructions()
        
        # Reset timing
        self.frame_count = 0
        start_time = core.getTime()
        
        # Main loop
        running = True
        while running:
            # Check for key presses
            keys = event.getKeys(['escape', 'space'])
            
            if 'escape' in keys:
                running = False
                break
            
            if 'space' in keys:
                self.paused = not self.paused
                if self.paused:
                    print("Paused")
                else:
                    print("Resumed")
            
            # Update and draw if not paused
            if not self.paused:
                self.update_stimuli()
                self.draw_all()
                
                # Flip and log timing
                flip_time = self.win.flip()
                
                if config.ENABLE_LOGGING:
                    self.frame_log.append({
                        'frame': self.frame_count,
                        'time': flip_time - start_time
                    })
                
                self.frame_count += 1
                
                # Check duration
                if config.EXPERIMENT_DURATION > 0:
                    if core.getTime() - start_time >= config.EXPERIMENT_DURATION:
                        running = False
            else:
                # Just maintain display when paused
                self.draw_all()
                self.win.flip()
        
        # Cleanup
        self.cleanup()
    
    def cleanup(self):
        """Save logs and close window."""
        print("\nExperiment finished!")
        
        # Save timing log
        if config.ENABLE_LOGGING and len(self.frame_log) > 0:
            df = pd.DataFrame(self.frame_log)
            df.to_csv(config.LOG_FILENAME, index=False)
            print(f"Timing log saved to: {config.LOG_FILENAME}")
        
        # Validate timing
        if config.VALIDATE_TIMING and len(self.frame_log) > 0:
            self.validate_timing()
        
        self.win.close()
    
    def validate_timing(self):
        """Validate actual achieved frequencies."""
        print("\n" + "=" * 60)
        print("TIMING VALIDATION REPORT")
        print("=" * 60)
        
        df = pd.DataFrame(self.frame_log)
        total_time = df['time'].iloc[-1] - df['time'].iloc[0]
        total_frames = len(df)
        
        print(f"Total duration: {total_time:.2f} seconds")
        print(f"Total frames: {total_frames}")
        print(f"Average frame rate: {total_frames / total_time:.2f} Hz")
        print()
        
        # Calculate actual frequencies achieved
        print("Frequency Accuracy:")
        print("-" * 60)
        print(f"{'Target (Hz)':<12} {'Expected Cycles':<15} {'Actual Cycles':<15} {'Status':<15}")
        print("-" * 60)
        
        for freq in self.frequencies:
            expected_cycles = freq * total_time
            
            # Count actual cycles by counting transitions
            frames_per_cycle = self.frame_cycles[freq]
            actual_cycles = total_frames / frames_per_cycle
            
            error = abs(actual_cycles - expected_cycles)
            status = "✓ PASS" if error < config.TIMING_TOLERANCE * total_time else "✗ FAIL"
            
            print(f"{freq:<12.1f} {expected_cycles:<15.1f} {actual_cycles:<15.1f} {status:<15}")
        
        print("=" * 60)
        print()


def main():
    """Main entry point."""
    try:
        stimulator = SSVEPStimulator()
        stimulator.run()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        core.quit()


if __name__ == "__main__":
    main()
