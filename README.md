# Multi-Objective Optimization & Decision Making: A Worked Trip-Packing Example

This project demonstrates multi-objective optimization (MOO) and
multi-criteria decision making (MCDM) using a realistic suitcase-packing
problem, combining classical algorithms with an LLM-powered explainer.

The project combines:
- Exhaustive ground-truth Pareto analysis and theory explanation
- Multiple evolutionary multi-objective algorithms
- Post-Pareto decision-making techniques
- A LangChain-based RAG chatbot that explains results and guides users

## 🧳 Get out your suitcase!
We imagine a case where we've picked 20 items of clothing for our trip, just barely squeezing into our 
luggage. We don't want to risk that pesky $35 checked bagged fee after buying souvenirs, but we also still
want to have lots of different outfits to chose from. And if we're discarding any items, we'd still like to
keep our favorites if possible. We now have three objectives to balance:
- Minimize suitcase volume
- Maximize number of possible outfits
- Maximize how much we like the items we've brought
This situation is an everyday day conundrum as opposed to an industry-specific one,
and the objectives conflict in intuitive ways, and aren, making the problem ideal for:
- Demonstrating Pareto optimality
- Comparing algorithm behavior
- Applying decision-making methods
- Explaining results to non-experts
The decision variables are binary (include or exclude clothing items), making this a discrete, combinatorial MOO problem.

## What this repository contains
This project demonstrates knowledge and 
shows application of the full MOO/MCDM process from initial problem context 
to final solution(s):
### Part 1 (Problem Introduction)
Introduction to Pareto theory: explaination of concepts like dominence, optimality, the Pareto front
Ground-truth solution space: Because the problem size is manageable, all possible solutions are enumerated.
This allows us to compute the true Pareto front and use it as a reference when evaluating algorithms.
### Part 2 (MOO Algorithms)
Several MOEAs are implemented and compared, including:
- NSGA-II
- SPEA2
- MOEA/D
- SMS-EMOA
These are used to approximate the Pareto front and analyze how different algorithmic biases affect results.

### Part 3 (Decision-making methods (MCDM))
After generating Pareto-optimal solutions, multiple decision-making approaches are applied to select a final solution, including:
- Weighted sum methods
- TOPSIS
- Knee-point selection
This reflects how MOO is used in practice: optimize first, decide later.

### Part 4 (LLM-powered explainer chatbot):
A LangChain RAG chatbot is included that:
- Reads the project notebooks and reference material
- Answers conceptual questions about MOO/MCDM
- Explains why different algorithms behave differently
- Helps users decide what method to use for their own problems
The chatbot indexes:
- Project notebooks
- A conceptual MOO/MCDM reference
- External decision-making resources

# This project demonstrates
- Pareto optimality and tradeoffs
- Differences between MOO and MCDM
- Algorithmic bias in MOEAs
- Post-Pareto decision making
- Hybrid optimization + decision workflows
- Explainability using LLMs
as well as my ability to explain concepts,

## Example Pareto Front
![Pareto Front](screenshots/pareto_front.png)

## Quick start
```bash
pip install -r requirements.txt
python examples/run_nsga2.py
python examples/run_chatbot.py
