import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def wilson_confidence_interval(p_hat, n, confidence=0.95):
    """
    Calculate Wilson score interval for binomial proportion
    
    Parameters:
    p_hat: sample proportion (0.8612)
    n: sample size (10000)
    confidence: confidence level (0.95 for 95%)
    
    Returns:
    tuple: (lower_bound, upper_bound)
    """
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    
    denominator = 1 + z**2 / n
    center = (p_hat + z**2 / (2 * n)) / denominator
    margin = (z * np.sqrt(p_hat * (1 - p_hat) / n + z**2 / (4 * n**2))) / denominator
    
    lower_bound = center - margin
    upper_bound = center + margin
    
    return lower_bound, upper_bound

def create_confidence_interval_plot(p_hat, n, theoretical_p):
    """Create publication-ready confidence interval visualization"""
    
    # Calculate intervals
    ci_90 = wilson_confidence_interval(p_hat, n, 0.90)
    ci_95 = wilson_confidence_interval(p_hat, n, 0.95) 
    ci_99 = wilson_confidence_interval(p_hat, n, 0.99)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot confidence intervals
    confidence_levels = [90, 95, 99]
    intervals = [ci_90, ci_95, ci_99]
    colors = ['lightblue', 'blue', 'darkblue']
    
    for i, (ci, color) in enumerate(zip(intervals, colors)):
        ax.plot(ci, [i, i], color=color, linewidth=8, label=f'{confidence_levels[i]}% CI')
        
        # Shift only the 99% interval text downward
        if i == 2:  # 99% interval (index 2)
            text_y_position = i + 0.25  # Shift 99% text further down
        else:
            text_y_position = i + 0.15  # Normal position for 90% and 95%
            
        ax.text(np.mean(ci), text_y_position, f'[{ci[0]:.3f}, {ci[1]:.3f}]', 
                ha='center', fontsize=11, fontweight='bold')
    
    # Add theoretical value line
    ax.axvline(x=theoretical_p, color='red', linestyle='--', linewidth=2, 
               label=f'Theoretical value: {theoretical_p:.3f}')
    
    # Add sample proportion
    ax.axvline(x=p_hat, color='green', linestyle=':', linewidth=2, 
               label=f'Sample proportion: {p_hat:.3f}')
    
    # Customize plot
    ax.set_yticks(range(3))
    ax.set_yticklabels(['90% CI', '95% CI', '99% CI'])
    ax.set_xlabel('Win Probability', fontsize=12)
    ax.set_title('Wilson Score Confidence Intervals for Simulated Win Probability', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # Set x-axis limits for better visualization
    margin = 0.01
    ax.set_xlim(p_hat - margin, p_hat + margin)
    
    # Adjust y-axis to accommodate the shifted text
    ax.set_ylim(-0.5, 3.2)
    
    plt.tight_layout()
    plt.savefig('confidence_intervals.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return {
        '90%_CI': ci_90,
        '95%_CI': ci_95, 
        '99%_CI': ci_99
    }

# Main analysis for your paper
if __name__ == "__main__":
    # Your simulation results
    p_hat = 0.8612      # Simulated win probability
    n = 10000           # Number of simulations
    theoretical_p = 0.8638  # Theoretical value
    
    print("=== Confidence Interval Analysis ===")
    print(f"Sample proportion (p̂): {p_hat:.4f}")
    print(f"Sample size (n): {n}")
    print(f"Theoretical value: {theoretical_p:.4f}")
    print()
    
    # Calculate and display intervals
    confidence_levels = [0.90, 0.95, 0.99]
    
    for confidence in confidence_levels:
        lower, upper = wilson_confidence_interval(p_hat, n, confidence)
        width = upper - lower
        contains_theoretical = lower <= theoretical_p <= upper
        
        print(f"{confidence:.0%} Confidence Interval:")
        print(f"  Interval: [{lower:.4f}, {upper:.4f}]")
        print(f"  Width: {width:.4f}")
        print(f"  Contains theoretical: {'Yes' if contains_theoretical else 'No'}")
        print()
    
    # Create visualization
    intervals = create_confidence_interval_plot(p_hat, n, theoretical_p)
