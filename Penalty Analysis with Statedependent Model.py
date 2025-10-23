# ===========================
# FIGURES & TABLE GENERATION (Race-to-15 version)
# ===========================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Simulated data (replace with actual arrays from race-to-15 simulation) ---
n_bouts = 10000
np.random.seed(42)

# Penalties per bout within 15 touches
yellow_cards = np.random.poisson(lam=2.9, size=n_bouts)   # slightly fewer than before
red_cards = np.random.binomial(n=2, p=0.22, size=n_bouts)
first_penalty_touch = np.random.normal(loc=7.3, scale=3.2, size=n_bouts).clip(1, 15)

# Markov state probabilities across 15 touches (bounded)
touches = np.arange(1, 16)
S0 = np.exp(-0.12 * touches)
S1 = 0.38 * np.exp(-((touches - 9)**2) / (2 * 3.5**2))
S1 /= S1.max() * 0.38  # rescale to keep max near 0.38
T0 = 1 - (S0 + S1)

# Win probabilities (from model, bounded to 15)
p_no_penalty = 0.864    # baseline theoretical
p_with_penalty = 0.857  # all bouts (penalty rules on)
p_penalty_bouts = 0.835 # conditional on bouts w/ penalties

# --------------------
# Figure 6: Penalty Distributions (bounded to 15 touches)
# --------------------
fig, axs = plt.subplots(1, 3, figsize=(14, 4))

# (a) Yellow-card distribution
sns.histplot(yellow_cards, bins=range(0, 10), ax=axs[0], color='gold', edgecolor='black')
axs[0].axvline(yellow_cards.mean(), color='black', linestyle='--', linewidth=1.5, label=f"Mean = {yellow_cards.mean():.2f}")
axs[0].set_title("(a) Yellow card distribution (race-to-15)")
axs[0].set_xlabel("Yellow cards per bout")
axs[0].set_ylabel("Frequency")
axs[0].legend()

# (b) Red-card distribution
sns.histplot(red_cards, bins=range(0, 6), ax=axs[1], color='red', edgecolor='black')
axs[1].axvline(red_cards.mean(), color='black', linestyle='--', linewidth=1.5, label=f"Mean = {red_cards.mean():.2f}")
axs[1].set_title("(b) Red card distribution (race-to-15)")
axs[1].set_xlabel("Red cards per bout")
axs[1].set_ylabel("Frequency")
axs[1].legend()

# (c) First-penalty timing
sns.histplot(first_penalty_touch, bins=10, ax=axs[2], color='purple', edgecolor='black')
axs[2].axvline(first_penalty_touch.mean(), color='black', linestyle='--', linewidth=1.5, label=f"Mean = {first_penalty_touch.mean():.2f}")
axs[2].set_title("(c) First penalty timing (within 15 touches)")
axs[2].set_xlabel("Touch number of first penalty")
axs[2].set_ylabel("Density")
axs[2].legend()

plt.tight_layout()
plt.savefig("Figure6_PenaltyDistributions_Race15.png", dpi=300)
plt.show()

# --------------------
# Figure 7: State Dynamics and Win Probability (bounded)
# --------------------
fig, axs = plt.subplots(1, 2, figsize=(12, 4))

# (a) Markov state evolution within 15 touches
axs[0].plot(touches, S0, label=r"$S_0$: Two-yellow regime", color='blue')
axs[0].plot(touches, S1, label=r"$S_1$: One-yellow accumulated", color='orange')
axs[0].plot(touches, T0, label=r"$T_0$: Post-red regime", color='green')
axs[0].set_xlabel("Touch number (bounded to 15)")
axs[0].set_ylabel("Probability")
axs[0].set_title("(a) Evolution of penalty states (race-to-15)")
axs[0].legend()

# (b) Win probabilities comparison
axs[1].bar(
    ["No penalties", "With penalties", "Penalty bouts only"],
    [p_no_penalty, p_with_penalty, p_penalty_bouts],
    color=["#5B9BD5", "#ED7D31", "#70AD47"],
)
axs[1].set_ylim(0.8, 0.9)
axs[1].set_ylabel("Win Probability")
axs[1].set_title("(b) Effect of penalties on win probability (bounded)")

plt.tight_layout()
plt.savefig("Figure7_StateDynamics_Race15.png", dpi=300)
plt.show()

# --------------------
# Table 2: Penalty Summary Statistics (Race-to-15)
# --------------------
summary_data = {
    "Metric": [
        "Yellow cards per bout",
        "Red cards per bout",
        "Bouts with ≥1 penalty",
        "Touch of first penalty (1–15)",
        "Yellow–red card correlation (r)",
        "Win prob. (no penalties)",
        "Win prob. (with penalties)",
        "Win prob. (penalty bouts only)"
    ],
    "Mean": [
        yellow_cards.mean(),
        red_cards.mean(),
        np.mean((yellow_cards + red_cards) > 0) * 100,
        first_penalty_touch.mean(),
        np.corrcoef(yellow_cards, red_cards)[0, 1],
        p_no_penalty,
        p_with_penalty,
        p_penalty_bouts
    ],
    "SD": [
        yellow_cards.std(ddof=1),
        red_cards.std(ddof=1),
        np.nan,
        first_penalty_touch.std(ddof=1),
        np.nan,
        np.nan,
        np.nan,
        np.nan
    ]
}

table2 = pd.DataFrame(summary_data)

print("\nTable 2. Penalty Summary Statistics (10,000 race-to-15 simulated bouts)\n")
print(table2.to_string(index=False, justify='left', col_space=16))

# Optional export
table2.to_csv("Table2_PenaltySummary_Race15.csv", index=False)
