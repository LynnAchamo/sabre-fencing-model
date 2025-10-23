import math
import numpy as np
import matplotlib.pyplot as plt

def theoretical_win_probability(lambda_A, lambda_B, target=15):
    """Calculate theoretical win probability using negative binomial distribution"""
    p = lambda_A / (lambda_A + lambda_B)
    win_prob = 0
    for k in range(0, target):
        comb = math.comb(target - 1 + k, k)
        win_prob += comb * (p ** target) * ((1 - p) ** k)
    return win_prob

def create_sensitivity_table_figure():
    """Create a visual table as a matplotlib figure"""
    
    # Define the lambda combinations for analysis
    lambda_combinations = [
        (10, 10),   # Equal strength
        (11, 10),   # Small advantage
        (12, 10),   # Moderate advantage  
        (12, 8),    # Your main case
        (14, 10),   # Clear advantage
        (15, 9),    # Strong advantage
        (8, 12),    # Disadvantage
        (9, 11),    # Small disadvantage
    ]
    
    # Calculate data
    table_data = []
    for lamA, lamB in lambda_combinations:
        win_prob = theoretical_win_probability(lamA, lamB)
        lambda_ratio = lamA / lamB
        advantage = f"+{(lambda_ratio - 1) * 100:.0f}%" if lambda_ratio > 1 else f"{(lambda_ratio - 1) * 100:.0f}%"
        
        table_data.append([
            f"{lamA}", f"{lamB}", f"{lambda_ratio:.2f}", 
            advantage, f"{win_prob:.3f}", f"{win_prob:.1%}"
        ])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('tight')
    ax.axis('off')
    
    # Define column headers
    columns = ['λ_A', 'λ_B', 'λ_A/λ_B', 'Advantage', 'Theoretical P(A wins)', 'Win Probability']
    
    # Create table
    table = ax.table(
        cellText=table_data,
        colLabels=columns,
        cellLoc='center',
        loc='center',
        bbox=[0, 0, 1, 1]
    )
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.5)
    
    # Style header row
    for i in range(len(columns)):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Alternate row colors for readability
    for i in range(len(table_data)):
        for j in range(len(columns)):
            if i % 2 == 0:
                table[(i+1, j)].set_facecolor('#f0f0f0')

    
    return fig

# Create and save the table figure
fig = create_sensitivity_table_figure()
plt.tight_layout()
plt.savefig('sensitivity_analysis_table.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.show()
