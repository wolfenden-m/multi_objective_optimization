import random
import math
import copy
import numpy as np
from moo_functions import evaluate_solution_metrics
from tqdm import tqdm


def dominates(a, b):
    """Return True if objective vector a dominates b (minimization)."""
    return all(x <= y for x, y in zip(a, b)) and any(x < y for x, y in zip(a, b))


def hamming_mutation(solution, mutation_rate):
    """Bit-flip mutation."""
    return np.array([
        bit if random.random() > mutation_rate else 1 - bit
        for bit in solution
    ], dtype=int)


def binary_tournament(pop):
    """Binary tournament selection based on fitness."""
    a, b = random.sample(pop, 2)
    return a if a["fitness"] < b["fitness"] else b


def compute_strength_and_raw_fitness(pop):
    """
    Compute strength S(i) and raw fitness R(i).
    """
    N = len(pop)
    strengths = [0] * N
    raw_fitness = [0] * N

    # Strength: number of solutions dominated
    for i in range(N):
        for j in range(N):
            if dominates(pop[i]["objectives"], pop[j]["objectives"]):
                strengths[i] += 1

    # Raw fitness: sum of strengths of dominators
    for i in range(N):
        for j in range(N):
            if dominates(pop[j]["objectives"], pop[i]["objectives"]):
                raw_fitness[i] += strengths[j]

    return raw_fitness


def compute_density(pop, k):
    """
    Density estimation using k-th nearest neighbor.
    """
    N = len(pop)
    distances = np.zeros((N, N))

    for i in range(N):
        for j in range(N):
            distances[i, j] = math.dist(
                pop[i]["objectives"], pop[j]["objectives"]
            )

    density = []
    for i in range(N):
        sorted_dist = np.sort(distances[i])
        sigma_k = sorted_dist[k]
        density.append(1.0 / (sigma_k + 2.0))

    return density


def environmental_selection(pop, archive_size):
    """
    Select archive using SPEA2 fitness and truncation.
    """
    # Step 1: Keep all fitness < 1
    archive = [ind for ind in pop if ind["fitness"] < 1]

    # Step 2: If too many, truncate using distance
    if len(archive) > archive_size:
        while len(archive) > archive_size:
            distances = np.zeros((len(archive), len(archive)))
            for i in range(len(archive)):
                for j in range(len(archive)):
                    distances[i, j] = math.dist(
                        archive[i]["objectives"],
                        archive[j]["objectives"]
                    )

            # Remove individual with minimum distance to others
            min_dist = float("inf")
            remove_idx = None
            for i in range(len(archive)):
                d = np.sort(distances[i])[1]
                if d < min_dist:
                    min_dist = d
                    remove_idx = i

            archive.pop(remove_idx)
    
    # Step 3: If too few, fill with best remaining
    elif len(archive) < archive_size:
        #remaining = [ind for ind in pop if ind not in archive]
        remaining = [ind for ind in pop if ind["fitness"] >= 1]
        remaining.sort(key=lambda x: x["fitness"])
        archive.extend(remaining[:archive_size - len(archive)])

    return archive


def run(
    n_bits,
    num_tops,
    num_bottoms,
    all_clothes_list,
    population_size,
    archive_size,
    generations,
    mutation_rate=0.01
):
    # --- Initialization ---
    population = []
    for _ in range(population_size):
        sol = np.random.randint(0, 2, size=n_bits)
        population.append({
            "solution": sol,
            "objectives": evaluate_solution_metrics(sol, num_tops, num_bottoms, all_clothes_list),
            "fitness": None
        })

    archive = []

    # --- Evolution loop ---
    with tqdm(total=generations, desc="Processing items") as pbar:
        for gen in range(generations):
            # Combine population and archive
            union = population + archive
    
            # Strength & raw fitness
            raw_fitness = compute_strength_and_raw_fitness(union)
    
            # Density estimation
            k = int(math.sqrt(len(union)))
            density = compute_density(union, k)
    
            # Final fitness
            for i in range(len(union)):
                union[i]["fitness"] = raw_fitness[i] + density[i]
    
            # Environmental selection
            archive = environmental_selection(union, archive_size)
    
            # --- Reproduction ---
            offspring = []
            while len(offspring) < population_size:
                parent = binary_tournament(archive)
                child_sol = hamming_mutation(parent["solution"], mutation_rate)
                offspring.append({
                    "solution": child_sol,
                    "objectives": evaluate_solution_metrics(child_sol, num_tops, num_bottoms, all_clothes_list),
                    "fitness": None
                })
    
            population = offspring
    
            pbar.update(1)

    solutions = [ind["solution"] for ind in archive]
    objectives = [ind["objectives"] for ind in archive]
    return solutions, objectives
