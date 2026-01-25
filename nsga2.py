import numpy as np
from tqdm import tqdm
from math import inf
import random 

def dominates(a, b):
    """Return True if solution a dominates solution b (minimization)."""
    return all(x <= y for x, y in zip(a, b)) and any(x < y for x, y in zip(a, b))


def fast_non_dominated_sort(objectives):
    """
    objectives: list of objective tuples
    returns: list of fronts (lists of indices)
    """
    S = [[] for _ in range(len(objectives))]
    n = [0] * len(objectives)
    rank = [0] * len(objectives)

    fronts = [[]]

    for p in range(len(objectives)):
        for q in range(len(objectives)):
            if dominates(objectives[p], objectives[q]):
                S[p].append(q)
            elif dominates(objectives[q], objectives[p]):
                n[p] += 1

        if n[p] == 0:
            rank[p] = 0
            fronts[0].append(p)

    i = 0
    while fronts[i]:
        next_front = []
        for p in fronts[i]:
            for q in S[p]:
                n[q] -= 1
                if n[q] == 0:
                    rank[q] = i + 1
                    next_front.append(q)
        i += 1
        fronts.append(next_front)

    return fronts[:-1]

def crowding_distance(front, objectives):
    distances = {i: 0.0 for i in front}
    num_objectives = len(objectives[0])

    for m in range(num_objectives):
        front_sorted = sorted(front, key=lambda i: objectives[i][m])
        distances[front_sorted[0]] = inf
        distances[front_sorted[-1]] = inf

        min_val = objectives[front_sorted[0]][m]
        max_val = objectives[front_sorted[-1]][m]

        if max_val == min_val:
            continue

        for i in range(1, len(front_sorted) - 1):
            prev_val = objectives[front_sorted[i - 1]][m]
            next_val = objectives[front_sorted[i + 1]][m]
            distances[front_sorted[i]] += (next_val - prev_val) / (max_val - min_val)

    return distances

def tournament_selection(population, objectives, ranks, crowding):
    i, j = random.sample(range(len(population)), 2)

    if ranks[i] < ranks[j]:
        return population[i]
    elif ranks[j] < ranks[i]:
        return population[j]
    else:
        return population[i] if crowding[i] > crowding[j] else population[j]

def uniform_crossover(p1, p2, p=0.5):
    mask = np.random.rand(len(p1)) < p
    child = np.where(mask, p1, p2)
    return child

def bit_flip_mutation(sol, mutation_rate):
    flip = np.random.rand(len(sol)) < mutation_rate
    sol[flip] = 1 - sol[flip]
    return sol

def deduplicate_population(population):
    seen = set()
    unique = []

    for sol in population:
        key = tuple(sol.tolist())   # or sol.tobytes()
        if key not in seen:
            seen.add(key)
            unique.append(sol)

    return unique

def run(
    evaluate_solution_metrics,
    num_tops,
    num_bottoms,
    all_clothes_list,
    n_bits,
    pop_size=100,
    generations=100,
    crossover_rate=0.9,
    mutation_rate=0.02,
):
    # ----- Initialize population -----
    population = [np.random.randint(0, 2, n_bits) for _ in range(pop_size)]

    with tqdm(total=generations, desc="Processing items") as pbar:
        for gen in range(generations):
    
            # ----- Evaluate -----
            objectives = [evaluate_solution_metrics(sol, num_tops, num_bottoms, all_clothes_list) for sol in population]
    
            # ----- Rank & crowding -----
            fronts = fast_non_dominated_sort(objectives)
            ranks = {}
            crowding = {}
    
            for rank, front in enumerate(fronts):
                cd = crowding_distance(front, objectives)
                for i in front:
                    ranks[i] = rank
                    crowding[i] = cd[i]
    
            # ----- Create offspring -----
            offspring = []
            while len(offspring) < pop_size:
                p1 = tournament_selection(population, objectives, ranks, crowding)
                p2 = tournament_selection(population, objectives, ranks, crowding)
    
                if random.random() < crossover_rate:
                    child = uniform_crossover(p1, p2)
                else:
                    child = p1.copy()
    
                child = bit_flip_mutation(child, mutation_rate)
                offspring.append(child)
    
            # ----- Combine -----
            combined = population + offspring
            combined = deduplicate_population(combined)
            combined_objectives = [evaluate_solution_metrics(sol, num_tops, num_bottoms, all_clothes_list) for sol in combined]
            
    
            # ----- Environmental selection -----
            fronts = fast_non_dominated_sort(combined_objectives)
            new_population = []
    
            for front in fronts:
                if len(new_population) + len(front) <= pop_size:
                    new_population.extend([combined[i] for i in front])
                else:
                    cd = crowding_distance(front, combined_objectives)
                    sorted_front = sorted(front, key=lambda i: cd[i], reverse=True)
                    remaining = pop_size - len(new_population)
                    new_population.extend([combined[i] for i in sorted_front[:remaining]])
                    break
    
            population = new_population
    
            pbar.update(1)

    solutions = []
    for ind in population:
        solutions.append(evaluate_solution_metrics(ind, num_tops, num_bottoms, all_clothes_list))
        
    return population, solutions
