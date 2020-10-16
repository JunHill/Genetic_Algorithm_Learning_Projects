import numpy as np
import random
import sys
import math
import copy
from  matplotlib import pyplot as plt

def single_point_cross_over(parent_x, parent_y):
    cross_point = random.randint(0, len(parent_x)-1)
    offspring_1 = parent_x.copy()
    offspring_2 = parent_y.copy()
    
    for i in range(cross_point, len(parent_y)):
        offspring_1[i] = parent_y[i]
    for i in range(cross_point, len(parent_x)):
        offspring_2[i] = parent_x[i] 
    
    return np.array([offspring_1,offspring_2])

def uniform_cross_over(parent_x, parent_y, rate=0.5):
    offspring_1 = parent_x.copy()
    offspring_2 = parent_y.copy()

    for i in range(len(parent_x)):
        if random.random() < rate:
            offspring_1[i] = parent_y[i]
            offspring_2[i] = parent_x[i]

    return np.array([offspring_1,offspring_2])

def avg(l):
    if len(l) == 0:
        raise Exception("Divided by zero!")
    return sum(l)/len(l)

def get_onemax_fitness_score(chromosome):
    return np.sum(chromosome)

def get_trap_fitness_score(chromosome):
    num_trap = int(chromosome.shape[0]/5)
    s = chromosome.reshape(-1,5).sum(axis = 1)
    s[s == 5] = -1
    return 4*num_trap - s.sum()

def initilize_population(problem_size, population_size):
    a = np.zeros((population_size//2, problem_size))
    if population_size % 2 == 0:
        b = np.zeros((population_size//2, problem_size)) + 1
    else:
        b = np.zeros((population_size//2 +1, problem_size)) + 1
    c = np.concatenate((a,b)).T
    for i in range(len(c)):
        np.random.shuffle(c[i])
    return c.T

def fraud(population):
    a = np.sum(population, axis=0)
    for i in a:
        if i == 0:
            return True
    return False


class Problem:
    def __init__(self, problem_size, population_size, crossover, seed):

        self.seed = seed
        random.seed(self.seed)
        np.random.seed(self.seed)
        
        self.problem_size = problem_size
        self.population_size = population_size

        self.population = initilize_population(problem_size, population_size)

        self.tournament_size = 4
        self.number_of_eval = 0

        self.crossover = crossover
        if crossover == "1X":
            self.crossover = single_point_cross_over
        elif crossover == "UX":
            self.crossover = uniform_cross_over
        else:
            raise Exception(f"Invalid crossover method! {self.crossover}")
    
    def tournament_selection(self, pool):
        the_chosen_ones = []
        sample = np.random.choice(range(self.population_size*4),(self.population_size,4),False)
        self.number_of_eval += self.population_size * self.tournament_size
        sample[sample >= 2*self.population_size] -= 2*self.population_size
        for i in range(self.population_size):
            score_board = np.array([self.get_fitness(x) for x in pool[sample[i]]])
            max_index = np.argmax(score_board)
            self.population[i] = pool[sample[i]][max_index].copy()
        

    def maximize(self, steps = 10000):

        # simple Genetic Algorithm with PO(P+O)P model
        while (self.number_of_eval < steps * (self.problem_size+self.population_size) and not fraud(self.population)):

            # Solution found if all chromosomes become the fittest
            if self.population.all()==1:
                return self.number_of_eval, True

            pool = copy.deepcopy(self.population)
            # Take each pair of parents and crossover to generate offspring
            for i in range(1, self.population_size,2):
                offspring = self.crossover(self.population[i], self.population[i-1])
                pool = np.concatenate((pool, offspring),axis=0)
            # generate new population through tournament selection
            self.tournament_selection(pool)
        return self.number_of_eval, False

class OneMaxProblem(Problem):
    def __init__(self, problem_size=10, population_size=8, crossover="1X", seed=18520750):
        super().__init__(problem_size, population_size, crossover, seed)
        self.get_fitness = get_onemax_fitness_score

class TrappedOneMaxProblem(Problem):
    def __init__(self, problem_size=10, population_size=8, crossover="1X", seed=18520750):
        super().__init__(problem_size, population_size, crossover, seed)
        self.get_fitness = get_trap_fitness_score
