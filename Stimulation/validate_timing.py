"""
Timing Validation Tool

Analyzes the timing log from SSVEP stimulation to verify
frequency accuracy and detect timing issues.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config import TARGET_FREQUENCIES, LOG_FILENAME, TIMING_TOLERANCE


def analyze_timing_log(log_file=LOG_FILENAME):
    """
    Analyze timing log and generate detailed report.
    
    Args:
        log_file: Path to CSV log file
    """
    try:
        df = pd.read_csv(log_file)
    except FileNotFoundError:
        print(f"Error: Log file '{log_file}' not found.")
        print("Please run ssvep_stimulation.py first to generate timing data.")
        return
    
    print("\n" + "=" * 70)
    print("DETAILED TIMING ANALYSIS")
    print("=" * 70)
    print()
    
    # Basic statistics
    total_frames = len(df)
    total_time = df['time'].iloc[-1] - df['time'].iloc[0]
    
    print(f"Total frames recorded: {total_frames}")
    print(f"Total duration: {total_time:.3f} seconds")
    print()
    
    # Frame interval analysis
    frame_intervals = df['time'].diff().dropna()
    mean_interval = frame_intervals.mean()
    std_interval = frame_intervals.std()
    
    print("Frame Interval Statistics:")
    print(f"  Mean: {mean_interval * 1000:.3f} ms")
    print(f"  Std Dev: {std_interval * 1000:.3f} ms")
    print(f"  Min: {frame_intervals.min() * 1000:.3f} ms")
    print(f"  Max: {frame_intervals.max() * 1000:.3f} ms")
    print(f"  Estimated refresh rate: {1 / mean_interval:.2f} Hz")
    print()
    
    # Detect frame drops
    expected_interval = mean_interval
    frame_drops = frame_intervals[frame_intervals > expected_interval * 1.5]
    
    if len(frame_drops) > 0:
        print(f"⚠ WARNING: Detected {len(frame_drops)} potential frame drops!")
        print(f"  Frames affected: {frame_drops.index.tolist()}")
        print()
    else:
        print("✓ No frame drops detected")
        print()
    
    # Frequency accuracy analysis
    print("Frequency Accuracy Analysis:")
    print("-" * 70)
    
    # Try to import refresh rate from a recent run
    try:
        # This is a simplified analysis - actual frequency depends on refresh rate
        refresh_rate = 1 / mean_interval
        
        for freq in TARGET_FREQUENCIES:
            # Calculate expected and actual cycles
            expected_cycles = freq * total_time
            
            # Estimate frames per cycle
            frames_per_cycle = round(refresh_rate / freq)
            actual_cycles = total_frames / frames_per_cycle
            actual_freq = actual_cycles / total_time
            
            error_hz = abs(actual_freq - freq)
            error_pct = (error_hz / freq) * 100
            
            status = "✓ PASS" if error_hz < TIMING_TOLERANCE else "✗ FAIL"
            
            print(f"{freq} Hz target:")
            print(f"  Actual frequency: {actual_freq:.3f} Hz")
            print(f"  Error: ±{error_hz:.3f} Hz ({error_pct:.2f}%)")
            print(f"  Status: {status}")
            print()
    
    except Exception as e:
        print(f"Could not complete frequency analysis: {e}")
    
    print("=" * 70)
    
    # Offer to plot
    plot_choice = input("\nGenerate timing plots? (y/n): ").lower()
    if plot_choice == 'y':
        plot_timing_analysis(df, frame_intervals)


def plot_timing_analysis(df, frame_intervals):
    """Generate visualization plots of timing data."""
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # Plot 1: Frame intervals over time
    axes[0].plot(frame_intervals.index, frame_intervals * 1000, linewidth=0.5)
    axes[0].axhline(y=frame_intervals.mean() * 1000, color='r', linestyle='--', 
                    label=f'Mean: {frame_intervals.mean() * 1000:.2f} ms')
    axes[0].set_xlabel('Frame Number')
    axes[0].set_ylabel('Frame Interval (ms)')
    axes[0].set_title('Frame Interval Over Time')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Frame interval distribution
    axes[1].hist(frame_intervals * 1000, bins=50, edgecolor='black', alpha=0.7)
    axes[1].axvline(x=frame_intervals.mean() * 1000, color='r', linestyle='--',
                    label=f'Mean: {frame_intervals.mean() * 1000:.2f} ms')
    axes[1].set_xlabel('Frame Interval (ms)')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('Frame Interval Distribution')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    plot_filename = 'timing_analysis.png'
    plt.savefig(plot_filename, dpi=150)
    print(f"\nPlot saved to: {plot_filename}")
    
    plt.show()


if __name__ == "__main__":
    analyze_timing_log()
