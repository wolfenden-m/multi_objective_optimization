# Multi-Objective Optimization & Decision Making: A Worked Suitcase Example

This repository demonstrates multi-objective optimization (MOO) and
multi-criteria decision making (MCDM) using a realistic suitcase-packing
problem, combining classical algorithms with an LLM-powered explainer.

## Why this project?
Choosing between conflicting objectives (e.g., weight vs outfits) is
common in real-world decision-making. This project shows:
- How Pareto fronts arise
- Why different MOEAs behave differently
- How to select a final solution using preferences
- How an LLM can explain and guide decisions

## What’s included
- Exhaustive solution generation (ground truth)
- Multiple MOEAs (NSGA-II, SPEA2, MOEA/D, SMS-EMOA)
- Post-Pareto decision-making methods (TOPSIS, weighted sum, knee points)
- A LangChain-based RAG chatbot that explains results and guides users

## Example Pareto Front
![Pareto Front](screenshots/pareto_front.png)

## Quick start
```bash
pip install -r requirements.txt
python examples/run_nsga2.py
python examples/run_chatbot.py
