# Multi-Objective Optimization & Decision Making: A Worked Trip-Packing Example 👕👖

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
2D Representation of the full solution space w/ the true Pareto front 
(split across three plots due to 3 objectives -> 2 dimensions, 3D Plotly plots in notebook):  
<img src="images/all_solns_with_pf.png" width="800" />

### Part 2 (MOO Algorithms)
Explanation of why algorithms are necessary for complex MOO problems, and the principles of evolutioary programming.  
Several algorithms are implemented and compared, including:  
- NSGA-II
- SPEA2
- MOEA/D
- SMS-EMOA
    
These are used to approximate the Pareto front and analyze how different algorithmic biases affect results.
We want to approximate as much of the true Pareto front as possible, as fast as possible, and 
comparison involves visual inspection of solution space:  
<img src="images/algo_comp_img.png" width="600" />  
  
and numerical metrics:  
<img src="images/algo_comp_table.png" width="600" />  
### Part 3 (Decision-making methods (MCDM))
After generating Pareto-optimal solutions, multiple decision-making approaches are applied to select a final solution, including:
- Weighted sum methods
- TOPSIS
- Knee-point selection
  
This reflects how MOO is used in practice: optimize first, decide later.  
When applicable, visuals showing how the method selects its point are displayed, like for example the Epsilon Constraint method.    
First you constrain one objective, e.g. saying any solution where you lose a max of 40 outfits:  
<img src="images/modm_example.png" width="400" />  
We can now treat this as a two objective problem:  
<img src="images/modm_example_2.png" width="400" />  
Then we can set a second constraint, like a max volume of 20, and since 3-2 = 1 we only have one solution remaining:  
<img src="images/modm_example_3.png" width="400" />  

### Part 4 (LLM-powered explainer chatbot):
A LangChain RAG chatbot is included that:
- Reads the project notebooks and reference material
- Answers conceptual questions about MOO/MCDM
- Explains why different algorithms behave differently
- Helps users decide what method to use for their own problems
utilizing the Qwen3-32b model through Groq and the nomic-embed-text model with Ollama for the embeddings.
  
The chatbot indexes:
- Project notebooks
- A conceptual MOO/MCDM reference
- External decision-making resources
  
For example:
```
================================ Human Message =================================

Why did MOPSO-CD underperform in our suitcase example problem? In what circumstance would MOPSO-CD outperform other algorithms?

================================== Ai Message ==================================
Tool Calls:
  retrieve_context (7zh1kr58x)
 Call ID: 7zh1kr58x
  Args:
    query: MOPSO-CD algorithm design, suitcase example, multi-objective tradeoffs
================================= Tool Message =================================
Name: retrieve_context

================================== Ai Message ==================================

The underperformance of **MOPSO-CD** in the suitcase example stems from its design trade-offs compared to other multi-objective algorithms like **NSGA-II**. Let’s break this down:

---

### 1. **Algorithm Design Biases**
- **MOPSO-CD**:  
  - Uses **particle swarm dynamics**, where particles (solutions) are guided by personal and global "best" solutions.  
  - Relies on **crowding distance** to maintain diversity in the Pareto front.  
  - **Bias**: Emphasizes convergence speed and local search but may struggle to maintain diversity in complex, multi-modal landscapes.

- **NSGA-II**:  
  - Uses **non-dominated sorting** and **crowding distance** for both selection and diversity.  
  - **Bias**: Prioritizes maintaining a well-distributed Pareto front through explicit diversity pressure and elitism.

### 2. **Why MOPSO-CD Underperformed in the Suitcase Example**
In the suitcase problem (maximize volume while minimizing weight), the solution space is likely **multi-modal** (e.g., many local optima with overlapping trade-offs). MOPSO-CD’s swarm dynamics may **converge prematurely** to suboptimal clusters, especially if:  
- The swarm’s global best dominates the search, reducing exploration.  
- Crowding distance fails to counteract local optima, leading to a **narrowed Pareto front**.  

NSGA-II, in contrast, systematically explores the front by sorting solutions into non-dominated layers and using crowding distance to spread them out. This makes it more robust for problems requiring **balanced diversity and convergence**.

### 3. **When MOPSO-CD Would Outperform Others**
MOPSO-CD excels in problems with:  
- **Smooth, continuous objective landscapes** (e.g., engineering design where trade-offs are predictable).  
- **Low computational budgets** (e.g., when rapid convergence is more critical than exhaustive exploration).  
- **High-dimensional decision spaces** (e.g., optimizing parameters with many variables), where swarm dynamics adapt better to complex interactions.  

For example, in a scenario where the suitcase problem’s items have **strongly correlated weight and volume** (e.g., all items are dense), MOPSO-CD might converge faster to a narrower but useful subset of solutions.

### 4. **Key Takeaway: Trade-offs, Not Errors**
There is **no universally superior algorithm**—only **algorithm preferences** for different problem structures. MOPSO-CD’s underperformance in the suitcase example reflects a **mismatch** between its design (rapid convergence, moderate diversity) and the problem’s need for **robust exploration**. In contrast, NSGA-II’s explicit non-dominated sorting better addresses the suitcase problem’s multi-modality.  

To optimize performance, always align algorithm choice with the problem’s **dominance structure**, **diversity requirements**, and **computational constraints**.
```

# This project demonstrates
- Pareto optimality and tradeoffs
- Differences between MOO and MCDM
- Algorithmic bias in MOEAs
- Post-Pareto decision making
- Hybrid optimization + decision workflows
- Explainability using LLMs
  
as well as my ability to apply these concepts and relay them to a non-technical audience.

## Project Structure
```
multi_objective_optimization/
│
├── moo_functions.py                   # Utility functions
├── prompt.py                          # Custom prompt templates
├── chatbot.py                         # RAG Agent Generator
├── requirements.txt                   # Python dependencies
├── algorithms/                        # Custom MOO Algorithm Codes
│   └── moaed.py
│   └── nsga2.py
│   └── spea2.py
│
├── data/
│   └── processed/
│       └── all_solns.npy              # Objective metrics for all possible solutions
│       └── best_algo_solns.npy        # PF approximated by best algorithm
│       └── full_pareto_front_df.npy   # True, full PF
│   └── raw/
│       └── tops.csv                   # Tops info
│       └── bottoms.csv                # Bottoms info
│
├── docs/
│   └── mcdm_moo_reference_for_rag.md  # MOO knowledge for RAG agent
│
└── README.md                          # Project documentation
```

## Contact

**Maeve Wolfenden**
- email: wolfenden.maeve@gmail.com
- GitHub: [@wolfenden-m](https://github.com/wolfenden-m)
- Project Link: [MOO Project Repository](https://github.com/wolfenden-m/multi_objective_optimization)
