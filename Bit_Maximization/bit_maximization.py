import numpy as np
import random
import sys
import math
import itertools
from  matplotlib import pyplot as plt


def get_onemax_fitness_scores(chromosome):
	return np.sum(chromosome)


def get_trap_fitness_scores(chromosome):
	score = np.sum(chromosome)
	if score != len(chromosome):
		score = len(chromosome) - score - 1
	return score


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
	return [offspring_1,offspring_2]

def calculate_num_pair_of_children(parent_num):
	return parent_num * (parent_num - 1) / 2

def get_parent_num(population_size):
	parent_num = 2
	while (calculate_num_pair_of_children(parent_num) < population_size):
		parent_num += 1
	return parent_num

def generate_pair(parent_num, population_size):
	return list(itertools.combinations(np.arange(parent_num-1),2))[0:population_size]

def print_population(population):
	population_str = []
	for chromosome in population:
		s = ""
		for bit in chromosome:
			s += str(bit)
		population_str.append(s)
	print(set(population_str))

def print_best(population):
	s = ""
	for bit in population[0]:
		s += str(bit)
	print(s)

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

def avg(l):
	return sum(l)/len(l)
class OneMaxProblem:
	def __init__(self, problem_size, population_size, seed):
		self.seed = seed
		random.seed(self.seed)
		np.random.seed(self.seed)
		self.problem_size = problem_size
		self.population = initilize_population(problem_size, population_size)
		
		self.population_size = population_size
		self.variation = np.unique(self.population, axis=0)
		self.tournament_size = 4
		self.current_fitness = []
		self.number_of_eval = 0
		self.cnt = 0

	def calculate_fitness(self):
		self.current_fitness = []
		for x in self.population:
			self.current_fitness.append(get_onemax_fitness_scores(x))
			self.number_of_eval += 1


	def tournament_selection(self, pool):
		selected_population = []
		buff = pool.copy()
		for _ in range (self.population_size):
			tournament = []
			for _ in range(self.tournament_size):
				if (len(buff) == 0):
					buff = pool.copy()
				random.shuffle(buff)
				x = buff.pop()
				tournament.append( (x, get_onemax_fitness_scores(x)) )
				self.number_of_eval += 1
			tournament.sort(key=lambda x: x[1], reverse=True)
			selected_population.append(tournament[0][0])
		return selected_population


	def maximize_single_point(self):
		# simple Genetic Algorithm with PO(P+O)P model
		while (self.number_of_eval < 100000 * self.problem_size):
			# get suitable number of parents
			parent_num = get_parent_num(self.population_size)
			# generate pair of parent index for mating
			pairs = generate_pair(parent_num, self.population_size)
			# calculate current fitness of the whole population
			last_fitness = self.current_fitness
			self.calculate_fitness()
			self.variation = np.unique(self.population, axis=0)
			if (sum(last_fitness) >= sum(self.current_fitness)) and len(self.variation) <= 2:
				self.cnt += 1
				if (self.cnt > 20):
					self.cnt = 0
					return self.number_of_eval, False
			# sort the population such that the fittest one comes first
			self.population = np.array([x for _, x in sorted(zip(self.current_fitness, self.population), key=lambda x: -x[0])])
			# Solution found if all chromosomes become the fittest
			if all(x == self.problem_size for x in self.current_fitness):
				#print(f"solution found using single point crossover! number of evaluations: {self.number_of_eval}")
				return self.number_of_eval, True
			# pool (P+O)
			pool = []
			# Take each pair of parents and crossover to generate Offspring
			for (x,y) in pairs:
				pool += single_point_cross_over(self.population[x], self.population[y])
			# Add parents to pool
			pool += list(self.population[0:self.population_size])
			# generate new population through tournament selection
			new_generation = self.tournament_selection(pool)
			#print('-----------------------')
			#print(avg(self.current_fitness))
			#print_best(self.population)
			self.population = np.array(new_generation)
		#print(f"Could not find solution! (after {self.number_of_eval} evaluations)")
		return self.number_of_eval, False

	def maximize_uniform(self):
		# simple Genetic Algorithm with PO(P+O)P model
		while (self.number_of_eval < 100000 * self.problem_size):
			# get suitable number of parents
			parent_num = get_parent_num(self.population_size)
			# generate pair of parent index for mating
			pairs = generate_pair(parent_num, self.population_size)
			# calculate current fitness of the whole population
			last_fitness = self.current_fitness
			self.calculate_fitness()
			self.variation = np.unique(self.population, axis=0)
			if (sum(last_fitness) >= sum(self.current_fitness)) and len(self.variation) <= 2:
				self.cnt += 1
				if (self.cnt > 20):
					self.cnt = 0
					return self.number_of_eval, False
			# sort the population such that the fittest one comes first
			self.population = np.array([x for _, x in sorted(zip(self.current_fitness, self.population), key=lambda x: -x[0])])
			# Solution found if all chromosomes become the fittest
			if all(x == self.problem_size for x in self.current_fitness):
				#print(f"solution found using uniform cross over! number of evaluations: {self.number_of_eval}")
				return self.number_of_eval, True

			# pool (P+O)
			pool = []
			# Take each pair of parents and crossover to generate Offspring
			for (x,y) in pairs:
				pool += uniform_cross_over(self.population[x], self.population[y], 0.5)
			# Add parents to pool
			pool += list(self.population[0:self.population_size])
			# generate new population through tournament selection
			new_generation = self.tournament_selection(pool)
			self.population = np.array(new_generation)
		#print(f"Could not find solution! (after {self.number_of_eval} evaluations)")
		return self.number_of_eval, False

class TrappedOneMaxProblem:
	def __init__(self, problem_size, population_size, seed):
		self.seed = seed
		random.seed(self.seed)
		np.random.seed(self.seed)
		self.problem_size = problem_size
		self.population = initilize_population(problem_size, population_size)
		self.population_size = population_size
		self.tournament_size = 4
		self.current_fitness = []
		self.number_of_eval = 0
		self.cnt = 0
		self.variation = np.unique(self.population, axis=0)


	def calculate_fitness(self):
		self.current_fitness = []
		for x in self.population:
			score = 0
			current_index = 0
			for i in range(int(self.problem_size/5)):
				score += get_trap_fitness_scores(x[current_index:(i+1)*5])
				current_index = (i+1)*5
				self.number_of_eval += 1
			self.current_fitness.append(score)
			

	def tournament_selection(self, pool):
		selected_population = []
		buff = pool.copy()
		for _ in range (self.population_size):
			tournament = []
			for _ in range(self.tournament_size):
				if (len(buff) == 0):
					buff = pool.copy()
				random.shuffle(buff)
				x = buff.pop()
				tournament.append( (x, get_onemax_fitness_scores(x)) )
				self.number_of_eval += 1
			tournament.sort(key=lambda x: x[1], reverse=True)
			selected_population.append(tournament[0][0])
		return selected_population

	def maximize_single_point(self):
		# simple Genetic Algorithm with PO(P+O)P model
		while (self.number_of_eval < 100000 * (self.problem_size+self.population_size)):
			# get suitable number of parents
			parent_num = get_parent_num(self.population_size)
			# generate pair of parent index for mating
			pairs = generate_pair(parent_num, self.population_size)
			# calculate current fitness of the whole population
			last_fitness = self.current_fitness
			self.calculate_fitness()
			self.variation = np.unique(self.population, axis=0)
			if (sum(last_fitness) >= sum(self.current_fitness)) and len(self.variation) <= 2:
				self.cnt += 1
				if (self.cnt > 20):
					self.cnt = 0
					return self.number_of_eval, False
			# sort the population such that the fittest one comes first
			self.population = np.array([x for _, x in sorted(zip(self.current_fitness, self.population), key=lambda x: -x[0])])
			#print('-----------------------')
			#print(avg(self.current_fitness))
			#if len(set(self.current_fitness)) > 2:	
			#	print_best(self.population)
			#else: 
			#	print_population(self.population)
			# Solution found if all chromosomes become the fittest
			if all(x == self.problem_size for x in self.current_fitness):
				#print(f"solution found using single point crossover! number of evaluations: {self.number_of_eval}")
				return self.number_of_eval, True
			# pool (P+O)
			pool = []
			# Take each pair of parents and crossover to generate Offspring
			for (x,y) in pairs:
				pool += single_point_cross_over(self.population[x], self.population[y])
			# Add parents to pool
			pool += list(self.population[0:self.population_size])
			# generate new population through tournament selection
			new_generation = self.tournament_selection(pool)
			self.population = np.array(new_generation)
		#print(f"Could not find solution! (after {self.number_of_eval} evaluations)")
		return self.number_of_eval, False

	def maximize_uniform(self):
		# simple Genetic Algorithm with PO(P+O)P model
		while (self.number_of_eval < 100000 * (self.problem_size+self.population_size)):
			# get suitable number of parents
			parent_num = get_parent_num(self.population_size)
			# generate pair of parent index for mating
			pairs = generate_pair(parent_num, self.population_size)
			# calculate current fitness of the whole population
			last_fitness = self.current_fitness
			self.calculate_fitness()
			self.variation = np.unique(self.population, axis=0)
			if (sum(last_fitness) >= sum(self.current_fitness)) and len(self.variation) <= 2:
				self.cnt += 1
				if (self.cnt > 20):
					self.cnt = 0
					return self.number_of_eval, False
			# sort the population such that the fittest one comes first
			self.population = np.array([x for _, x in sorted(zip(self.current_fitness, self.population), key=lambda x: -x[0])])
			#print('-----------------------')
			#print(avg(self.current_fitness))
			#print_best(self.population)
			# Solution found if all chromosomes become the fittest
			if all(x == self.problem_size for x in self.current_fitness):
				#print(f"solution found using uniform cross over! number of evaluations: {self.number_of_eval}")
				return self.number_of_eval, True

			# pool (P+O)
			pool = []
			# Take each pair of parents and crossover to generate Offspring
			for (x,y) in pairs:
				pool += uniform_cross_over(self.population[x], self.population[y], 0.5)
			# Add parents to pool
			pool += list(self.population[0:self.population_size])
			# generate new population through tournament selection
			new_generation = self.tournament_selection(pool)
			self.population = np.array(new_generation)
		#print(f"Could not find solution! (after {self.number_of_eval} evaluations)")
		return self.number_of_eval, False