# sabre-fencing-model
This repository contains the Python code and data visualizations. The code validates the stochastic simulation model of sabre bouts against theoretical probabilities, performs sensitivity analysis, and generates all figures and tables, providing a reproducible foundation for probabilistic analysis in fencing.

## Project Overview
This project develops a probabilistic model for sabre fencing, treating bouts as a Poisson race between two fencers with integrated Markov chain penalty escalation.

## Files
- `wilson_confidence_interval.py` - Statistical validation and confidence intervals (Figure 2)
- `score_margin_distribution.py` - Victory margin analysis (Figure 3)  
- `penalty_analysis.py` - Penalty system modeling (Figures 4-7, Tables 2-3)
- `sensitivity_analysis.py` - Scoring rate sensitivity analysis (Table 1)

## Requirements
- Python 3.10+
- NumPy, Matplotlib, Seaborn

## Usage
Run any script to regenerate the corresponding figures/tables from the paper:
```bash
python penalty_analysis.py
