"""
Monitor Refresh Rate Checker and Frequency Compatibility Tool

This script detects your monitor's refresh rate and calculates
which SSVEP frequencies will be exactly achievable.
"""

from psychopy import visual, core
import numpy as np


def detect_refresh_rate(duration=1.0):
    """
    Detect monitor refresh rate by measuring actual frame times.
    
    Args:
        duration: How long to measure (seconds)
    
    Returns:
        Detected refresh rate in Hz
    """
    print("Detecting monitor refresh rate...")
    print("Please wait, this will take a few seconds...\n")
    
    # Create a window
    win = visual.Window(
        size=[800, 600],
        fullscr=False,
        color=[0, 0, 0],
        units='pix'
    )
    
    # Measure frame times
    frame_times = []
    start_time = core.getTime()
    
    while core.getTime() - start_time < duration:
        win.flip()
        frame_times.append(core.getTime())
    
    win.close()
    
    # Calculate refresh rate
    frame_intervals = np.diff(frame_times)
    mean_interval = np.mean(frame_intervals)
    refresh_rate = 1.0 / mean_interval
    
    return refresh_rate


def calculate_achievable_frequencies(refresh_rate, target_frequencies):
    """
    Calculate which frequencies are exactly achievable and what
    the actual achieved frequency will be.
    
    Args:
        refresh_rate: Monitor refresh rate in Hz
        target_frequencies: List of desired frequencies
    
    Returns:
        List of tuples (target_freq, frames_per_cycle, actual_freq, is_exact)
    """
    results = []
    
    for target_freq in target_frequencies:
        # Calculate frames per full cycle (on + off)
        frames_per_cycle = refresh_rate / target_freq
        
        # Round to nearest integer
        frames_per_cycle_int = round(frames_per_cycle)
        
        # Calculate actual achieved frequency
        actual_freq = refresh_rate / frames_per_cycle_int
        
        # Check if it's exact (within 0.01 Hz)
        is_exact = abs(actual_freq - target_freq) < 0.01
        
        results.append((
            target_freq,
            frames_per_cycle_int,
            actual_freq,
            is_exact
        ))
    
    return results


def print_compatibility_report(refresh_rate, results):
    """Print a formatted report of frequency compatibility."""
    
    print("=" * 70)
    print(f"MONITOR REFRESH RATE: {refresh_rate:.2f} Hz")
    print("=" * 70)
    print()
    print("FREQUENCY COMPATIBILITY REPORT")
    print("-" * 70)
    print(f"{'Target (Hz)':<12} {'Frames/Cycle':<15} {'Actual (Hz)':<12} {'Status':<15}")
    print("-" * 70)
    
    for target, frames, actual, is_exact in results:
        status = "✓ EXACT" if is_exact else f"✗ OFF by {abs(actual - target):.2f} Hz"
        print(f"{target:<12.1f} {frames:<15} {actual:<12.2f} {status:<15}")
    
    print("-" * 70)
    print()
    
    # Summary
    exact_count = sum(1 for _, _, _, is_exact in results if is_exact)
    print(f"Summary: {exact_count}/{len(results)} frequencies are exactly achievable")
    print()
    
    if exact_count < len(results):
        print("RECOMMENDATIONS:")
        print("- For exact frequencies, consider a monitor with refresh rate:")
        
        # Suggest ideal refresh rates
        target_freqs = [r[0] for r in results]
        ideal_rates = []
        for rate in [60, 75, 120, 144, 165, 240]:
            exact_at_rate = sum(1 for freq in target_freqs 
                              if abs(rate / round(rate / freq) - freq) < 0.01)
            if exact_at_rate > exact_count:
                ideal_rates.append((rate, exact_at_rate))
        
        for rate, count in sorted(ideal_rates, key=lambda x: x[1], reverse=True)[:3]:
            print(f"  • {rate} Hz ({count}/{len(results)} exact)")
        print()


def suggest_optimal_frequencies(refresh_rate, freq_range=(6, 15), count=7):
    """
    Suggest optimal frequencies that will be exactly achievable
    with the current refresh rate.
    
    Args:
        refresh_rate: Monitor refresh rate
        freq_range: Tuple of (min, max) frequency range
        count: Number of frequencies to suggest
    
    Returns:
        List of optimal frequencies
    """
    optimal = []
    
    # Find all exactly achievable frequencies in range
    for frames in range(2, 100):
        freq = refresh_rate / frames
        if freq_range[0] <= freq <= freq_range[1]:
            optimal.append(freq)
    
    # Sort and return closest to evenly spaced
    optimal.sort()
    
    if len(optimal) <= count:
        return optimal
    
    # Select evenly spaced frequencies
    indices = np.linspace(0, len(optimal) - 1, count, dtype=int)
    return [optimal[i] for i in indices]


if __name__ == "__main__":
    # Import config to check target frequencies
    try:
        from config import TARGET_FREQUENCIES
    except ImportError:
        TARGET_FREQUENCIES = [6, 7, 8, 10, 12, 13, 15]
    
    print("\n" + "=" * 70)
    print("SSVEP REFRESH RATE CHECKER")
    print("=" * 70)
    print()
    
    # Detect refresh rate
    refresh_rate = detect_refresh_rate(duration=2.0)
    
    # Calculate compatibility
    results = calculate_achievable_frequencies(refresh_rate, TARGET_FREQUENCIES)
    
    # Print report
    print_compatibility_report(refresh_rate, results)
    
    # Suggest optimal frequencies
    print("SUGGESTED OPTIMAL FREQUENCIES (exactly achievable):")
    optimal = suggest_optimal_frequencies(refresh_rate, count=7)
    print(f"{[f'{f:.2f}' for f in optimal]}")
    print()
    print("You can update these in config.py as TARGET_FREQUENCIES")
    print("=" * 70)
