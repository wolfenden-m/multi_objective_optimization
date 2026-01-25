import numpy as np
import random
from tqdm import tqdm
from moo_functions import evaluate_solution_metrics

class MOEAD:
    def __init__(
        self,
        n_vars,
        n_objectives,
        num_tops,
        num_bottoms,
        all_clothes_list,
        population_size=100,
        neighborhood_size=20,
        crossover_prob=0.9,
        mutation_prob=0.01,
        max_generations=200
    ):
        self.n_vars = n_vars
        self.M = n_objectives
        self.num_tops = num_tops
        self.num_bottoms = num_bottoms
        self.all_clothes_list = all_clothes_list
        self.N = population_size
        self.T = neighborhood_size
        self.pc = crossover_prob
        self.pm = mutation_prob
        self.max_gen = max_generations

        # Weight vectors
        self.weights = self._generate_weights()

        # Neighborhoods
        self.neighbors = self._compute_neighbors()

        # Population
        self.population = self._init_population()
        self.objectives = np.array(
            [evaluate_solution_metrics(ind, num_tops, num_bottoms, all_clothes_list) for ind in self.population]
        )

        # Ideal point
        self.z = np.min(self.objectives, axis=0)
        #self.z = np.zeros(3)


    def _generate_weights(self):
        weights = np.random.rand(self.N, self.M)
        weights /= np.sum(weights, axis=1, keepdims=True)
        return weights

    def _compute_neighbors(self):
        dist = np.linalg.norm(
            self.weights[:, None, :] - self.weights[None, :, :], axis=2
        )
        return np.argsort(dist, axis=1)[:, :self.T]

    def _init_population(self):
        return np.random.randint(0, 2, size=(self.N, self.n_vars))

    
    def _crossover(self, p1, p2):
        if random.random() > self.pc:
            return p1.copy()

        point = random.randint(1, self.n_vars - 1)
        return np.concatenate([p1[:point], p2[point:]])

    def _mutation(self, child):
        for i in range(self.n_vars):
            if random.random() < self.pm:
                child[i] ^= 1
        return child

    # Decomposition function
    def _tchebycheff(self, f, weight):
        return np.max(weight * np.abs(f - self.z))

    # Main loop
    def run(self):
        with tqdm(total=self.max_gen, desc="Processing items") as pbar:
            for gen in range(self.max_gen):
                for i in range(self.N):
                    # Select parents from neighborhood
                    p_idx = np.random.choice(self.neighbors[i], size=2, replace=False)
                    p1, p2 = self.population[p_idx[0]], self.population[p_idx[1]]
    
                    # Generate offspring
                    child = self._mutation(self._crossover(p1, p2))
                    f_child = np.array(evaluate_solution_metrics(child, self.num_tops, self.num_bottoms, self.all_clothes_list))
    
                    # Update ideal point
                    self.z = np.minimum(self.z, f_child)
    
                    # Update neighbors
                    for j in self.neighbors[i]:
                        f_j = self.objectives[j]
                        if (
                            self._tchebycheff(f_child, self.weights[j])
                            <= self._tchebycheff(f_j, self.weights[j])
                        ):
                            self.population[j] = child.copy()
                            self.objectives[j] = f_child.copy()
                pbar.update(1)

        return self.population, self.objectives
