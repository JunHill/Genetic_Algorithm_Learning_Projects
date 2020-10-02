import numpy as np
import random
import sys
from  matplotlib import pyplot as plt




def get_onemax_fitness_scores(chromosome):
    score = 0
    for bit in chromosome:
            score += bit | 0
    return score


def get_trap_fitness_scores(chromosome):
    score = 0
    for bit in chromosome:
        score += bit | 0
    if score != len(chromosome):
        score = len(chromosome) - score - 1
    return fitness_scores


def single_point_cross_over(parent_x, parent_y):
    cross_point = random.randint(0, len(parent_x)-1)
    offspring_1 = parent_x.copy()
    offspring_2 = parent_y.copy()
    
    for i in range(cross_point, len(parent_y)):
        offspring_1[i] = parent_y[i]
    for i in range(cross_point, len(parent_x)):
        offspring_2[i] = parent_x[i] 
    
    return [offspring_1,offspring_2]

def uniform_cross_over(parent_x, parent_y, rate):
    offspring_1 = parent_x.copy()
    offspring_2 = parent_y.copy()

    for i in range(len(parent_x)):
        if random.random() < rate:
            offspring_1[i] = parent_y[i]
            offspring_2[i] = parent_x[i]

def tournament_selection(tournament_size, pop_size, pool):
    selected_population = []
    for _ in range (pop_size):
        tournament = []
        for _ in range(tournament_size):
            x = random.choice(pool)
            tournament.append( (x, get_onemax_fitness_scores(x)) )
        tournament.sort(key=lambda x: x[1], reverse=True)
        selected_population.append(tournament[0])
    return selected_population





class OneMaxProblem:
    def __init__(self, problem_size, population_size):
        self.problem_size = problem_size
        self.population = []
        for _ in range(problem_size * population_size // 2):
            self.population += [0]
        for _ in range(problem_size * population_size // 2, problem_size * population_size):
            self.population += [1]
        self.population = np.resize(self.population, (population_size, problem_size))
        np.random.shuffle(self.population)

        self.number_of_eval = 0

    def get_fitness(self):
        scores = []
        for x in self.population:
            scores.append(get_onemax_fitness_scores(x))

        self.number_of_eval += 1
        return scores

    def maximize_single_point(self):
        while (self.number_of_eval < 10000 * self.problem_size):
            for x in range()


class TrappedOneMaxProblem:
    def __init__(self, problem_size, k):
        self.problem_size = problem_size
        self.k = k
        self.population = []
        for _ in range(problem_size * population_size // 2):
            self.population += [0]
        for _ in range(problem_size * population_size // 2, problem_size * population_size):
            self.population += [1]
        self.population = np.resize(self.population, (population_size, problem_size))
        np.random.shuffle(self.population)

        self.number_of_eval = 0

    def get_fitness(self):
        scores = []
        for x in self.population:
            temp = temp1 = 0
            for i in range(len(x)):
                if i%self.k == 0:
                    temp += get_trap_fitness_scores(x[temp1:i])
                    temp1 = i
            temp += get_trap_fitness_scores(x[temp1:len(x)])
            scores.append(temp)

        self.number_of_eval += 1
        return scores

    def maximize(self):