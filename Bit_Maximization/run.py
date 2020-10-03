from bit_maximization import OneMaxProblem, TrappedOneMaxProblem
from bisection import bisection
import sys

POPULATION_SIZE = 10
RANDOM_SEED = 18520750
# DICTIONARY mode
# problem : normal or trap
# cross-over : single_point or uniform 
mode = {'cross-over': 'single_point', 'problem': 'trap'}
print(f'RUNNING BISECTION FOR POPULATION SIZE: {POPULATION_SIZE} with {mode}...')
evals, N, success = bisection(POPULATION_SIZE, RANDOM_SEED, mode)
if success:
	print(f'average eval: {evals} - average population size: {N}')
else:
	print(f'could not find upper bound!')