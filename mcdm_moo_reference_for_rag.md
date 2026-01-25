Multi-Objective Optimization (MOO) and Multi-Criteria Decision Making (MCDM): Concepts, Methods, and Practical Guidance
1. Core Distinction: MOO vs MCDM

Multi-objective problems fall into two closely related but distinct categories:

Multi-Objective Optimization (MOO)

Goal: Search a large solution space to discover tradeoffs.

The set of possible solutions is large, continuous, combinatorial, or implicit.

The objective is to approximate the Pareto front.

Preferences are often unknown or deferred.

Typical outputs:

A set of non-dominated solutions

Tradeoff curves or surfaces

Examples:

Packing a suitcase with binary decisions (item included or not)

Scheduling, portfolio design, resource allocation

Typical methods:

NSGA-II

SPEA2

MOEA/D

SMS-EMOA

Bayesian multi-objective optimization

Multi-Criteria Decision Making (MCDM / MODM)

Goal: Choose among known alternatives using preferences.

Alternatives are known or enumerated.

Preferences are applied to rank or select solutions.

Often applied after MOO.

Typical outputs:

One “best” solution

Ranked list of alternatives

Examples:

Selecting one suitcase configuration from a Pareto set

Choosing a supplier, plan, or design

Typical methods:

Weighted Sum

TOPSIS

PROMETHEE

ELECTRE

Analytic Hierarchy Process (AHP)

Relationship Between the Two

In practice, MOO generates options, and MCDM selects among them.

Search → Pareto Front → Preference Application → Final Choice

2. Pareto Optimality and Tradeoffs

A solution is Pareto optimal if no objective can be improved without worsening at least one other objective.

In the suitcase example:

Less weight usually means fewer outfits.

More outfits usually means more weight.

The Pareto front represents these tradeoffs.

Important consequences:

There is rarely a single “best” solution.

“Better” depends on preferences.

3. Why Different MOEAs Produce Different Pareto Sets

Different algorithms emphasize different properties of the Pareto front.

NSGA-II

Uses non-dominated sorting and crowding distance

Encourages diversity

Often produces well-spread fronts

May include slightly weaker extreme solutions

SPEA2

Uses strength-based fitness

Strong selection pressure

Often favors high-quality interior solutions

Can prune extremes if dominated early

MOEA/D

Decomposes MOO into scalar subproblems

Optimizes weighted combinations of objectives

Biases solutions toward specific tradeoff directions

Why MOEA/D might have higher “outfits lost” than SPEA2:

Weight vectors emphasize certain objectives

Poor alignment between decomposition weights and true front

Neighborhood bias limits exploration of certain regions

This is not a bug—it's a design choice.

4. Scalarization and Preference Encoding

When preferences are known or partially known, scalarization can be used.

Weighted Sum
minimize: w1 * f1(x) + w2 * f2(x)


Pros:

Simple

Interpretable

Cons:

Misses non-convex Pareto regions

Sensitive to scaling

Use when:

Preferences are stable

One solution is needed

ε-Constraint Method

Optimize one objective

Treat others as constraints

Example:

Minimize weight subject to outfits ≥ 7

Pros:

Good for regulated or threshold-based problems

Finds extreme solutions

Lexicographic Optimization

Objectives ranked by priority

Secondary objectives only considered when higher priorities tie

Use when:

One objective is clearly dominant

5. Decision Making After Optimization (Post-Pareto MCDM)

Once a Pareto front is available, MCDM helps select a final solution.

TOPSIS

Chooses solution closest to ideal, farthest from worst

Sensitive to normalization

PROMETHEE

Pairwise outranking

Good for qualitative or ordinal preferences

Knee-Point Selection

Identifies solutions with best tradeoff “bang for buck”

No explicit weights required

6. How to Answer “What Should I Do?” Questions
Example 1

“Benefits are slightly more important than payroll cost.”

Recommended approach:

Run MOO to generate Pareto front

Apply:

Weighted sum with slightly higher weight on benefits, or

TOPSIS using benefit importance

Inspect sensitivity by varying weights slightly

Example 2

“Why does algorithm A give worse results on metric X?”

Answer structure:

Explain algorithm bias (selection pressure, decomposition, diversity)

Explain metric interaction (tradeoffs)

Clarify that “worse” may be relative to preference, not dominance

7. Suitcase Packing as a Canonical Example

Suitcase packing illustrates:

Binary decision variables

Conflicting objectives

Discrete Pareto fronts

Clear human intuition for tradeoffs

This makes it ideal for:

Teaching Pareto optimality

Demonstrating MOEA behavior

Showing post-hoc decision making

8. When to Use Bayesian Multi-Objective Optimization

Use Bayesian MOO when:

Evaluations are expensive

Simulation-based objectives

Small evaluation budgets

Examples:

Manufacturing simulations

Financial stress testing

Hyperparameter tuning

9. Hybrid and Interactive Approaches

Advanced workflows:

MOEA + user preference feedback

Reference-point guided NSGA-II

LLM-assisted mutation or selection

Interactive MCDM during optimization

These are useful when:

Preferences evolve

Tradeoffs are hard to articulate upfront

10. Key Takeaways for Users

Optimization finds tradeoffs; decision making chooses among them

No MOEA is universally best

Algorithm behavior reflects design priorities

Preferences should guide final selection, not raw objective values

Combining methods is standard practice

11. References and Further Reading (Good for RAG Crawling)

Foundational

Deb, K. Multi-Objective Optimization Using Evolutionary Algorithms

Miettinen, K. Nonlinear Multiobjective Optimization

MOEAs

NSGA-II: https://ieeexplore.ieee.org/document/996017

SPEA2: https://link.springer.com/chapter/10.1007/3-540-45356-3_83

MOEA/D: https://ieeexplore.ieee.org/document/4358754

Decision Making

TOPSIS: https://doi.org/10.1016/0377-2217(81)90133-4

PROMETHEE: https://www.sciencedirect.com/science/article/pii/037722179090010D

Practical Tutorials

PyMoo documentation: https://pymoo.org

BoTorch MOO tutorials: https://archive.botorch.org