import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew
import matplotlib.patches as mpatches

# Set style for scientific paper
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def simulate_score_margins(lambda_a=12, lambda_b=8, n_bouts=10000, target_score=15):
    """
    Simulate sabre bouts and return score margins for wins and losses
    """
    win_margins = []
    loss_margins = []
    
    for _ in range(n_bouts):
        score_a, score_b = 0, 0
        
        while score_a < target_score and score_b < target_score:
            # Simulate touches using exponential waiting times
            time_next_touch_a = np.random.exponential(1/lambda_a)
            time_next_touch_b = np.random.exponential(1/lambda_b)
            
            if time_next_touch_a < time_next_touch_b:
                score_a += 1
            else:
                score_b += 1
        
        # Calculate margin from Fencer A's perspective
        if score_a == target_score:
            win_margins.append(score_a - score_b)
        else:
            loss_margins.append(score_b - score_a)  # Positive margin for loss
    
    return win_margins, loss_margins

def create_score_margin_figure(win_margins, loss_margins):
    """
    Create the score margin distribution figure with skewness annotations
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Calculate skewness
    skew_win = skew(win_margins)
    skew_loss = skew(loss_margins)
    
    # Calculate percentages for decisive/close wins
    decisive_wins = len([m for m in win_margins if m >= 4])
    close_wins = len([m for m in win_margins if m <= 3])
    close_losses = len([m for m in loss_margins if m <= 3])
    
    pct_decisive_wins = decisive_wins / len(win_margins) * 100
    pct_close_wins = close_wins / len(win_margins) * 100
    pct_close_losses = close_losses / len(loss_margins) * 100
    
    # Plot 1: Distribution of winning margins
    bins = np.arange(1, 16) - 0.5
    ax1.hist(win_margins, bins=bins, alpha=0.7, color='#2E8B57', edgecolor='black')
    ax1.axvline(x=3.5, color='red', linestyle='--', alpha=0.7, linewidth=1)
    ax1.text(3.5, max(np.histogram(win_margins, bins=bins)[0]) * 0.9, 
             'Close/Decisive\nThreshold', rotation=90, ha='right', va='top', fontsize=9)
    
    ax1.set_xlabel('Victory Margin (Touches)')
    ax1.set_ylabel('Frequency')
    ax1.set_title(f'Distribution of Winning Margins\n(λ_A = 12 vs λ_B = 8)', fontsize=12, fontweight='bold')
    ax1.set_xticks(range(1, 16))
    ax1.grid(True, alpha=0.3)
    
    # Add skewness annotation for wins
    ax1.text(0.02, 0.98, f'Skewness (γ₁) = {skew_win:.2f}', 
             transform=ax1.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Plot 2: Distribution of losing margins
    ax2.hist(loss_margins, bins=bins, alpha=0.7, color='#CD5C5C', edgecolor='black')
    ax2.axvline(x=3.5, color='red', linestyle='--', alpha=0.7, linewidth=1)
    ax2.text(3.5, max(np.histogram(loss_margins, bins=bins)[0]) * 0.9, 
             'Close/Decisive\nThreshold', rotation=90, ha='right', va='top', fontsize=9)
    
    ax2.set_xlabel('Defeat Margin (Touches)')
    ax2.set_ylabel('Frequency')
    ax2.set_title(f'Distribution of Losing Margins\n(λ_A = 12 vs λ_B = 8)', fontsize=12, fontweight='bold')
    ax2.set_xticks(range(1, 16))
    ax2.grid(True, alpha=0.3)
    
    # Add skewness annotation for losses
    ax2.text(0.02, 0.98, f'Skewness (γ₁) = {skew_loss:.2f}', 
             transform=ax2.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    
    # Print statistical summary
    print("="*50)
    print("SCORE MARGIN DISTRIBUTION ANALYSIS")
    print("="*50)
    print(f"Total bouts simulated: {len(win_margins) + len(loss_margins)}")
    print(f"Fencer A win rate: {len(win_margins)/(len(win_margins)+len(loss_margins))*100:.1f}%")
    print(f"Fencer A loss rate: {len(loss_margins)/(len(win_margins)+len(loss_margins))*100:.1f}%")
    print("\n--- Winning Margins ---")
    print(f"Mean victory margin: {np.mean(win_margins):.2f} touches")
    print(f"Median victory margin: {np.median(win_margins):.1f} touches")
    print(f"Skewness: {skew_win:.2f}")
    print(f"Decisive wins (margin ≥4): {pct_decisive_wins:.1f}%")
    print(f"Close wins (margin ≤3): {pct_close_wins:.1f}%")
    
    print("\n--- Losing Margins ---")
    print(f"Mean defeat margin: {np.mean(loss_margins):.2f} touches")
    print(f"Median defeat margin: {np.median(loss_margins):.1f} touches")
    print(f"Skewness: {skew_loss:.2f}")
    print(f"Close losses (margin ≤3): {pct_close_losses:.1f}%")
    
    return fig, (skew_win, skew_loss, pct_decisive_wins, pct_close_losses)

# Main execution
if __name__ == "__main__":
    # Set random seed for reproducible results
    np.random.seed(42)
    
    # Simulate bouts
    print("Simulating bouts...")
    win_margins, loss_margins = simulate_score_margins(lambda_a=12, lambda_b=8, n_bouts=10000)
    
    # Create figure
    fig, stats = create_score_margin_figure(win_margins, loss_margins)
    
    # Save figure in high resolution for paper
    plt.savefig('score_margin_distribution.png', dpi=300, bbox_inches='tight')
    plt.savefig('score_margin_distribution.pdf', bbox_inches='tight')  # For publication
    
    plt.show()
