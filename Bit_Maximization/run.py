from bit_maximization import OneMaxProblem, TrappedOneMaxProblem
from bisection import run_bisection_multiple_times 
import numpy as np
import sys

PROBLEM_SIZE = 10
RANDOM_SEED = 18520750
# DICTIONARY mode
# problem : normal or trap
# cross-over : single_point or uniform 
mode = {'cross-over': 'single_point', 'problem': 'normal'}

evals, MRPS, success = run_bisection_multiple_times(10, PROBLEM_SIZE, RANDOM_SEED, mode)

print(f"evals: {evals}")
eval_std = np.std(evals)
print(f'----> avg evals: {np.mean(evals)} with std of {eval_std}')

print(f"MRPS: {MRPS}")
mrps_std = np.std(MRPS)
print(f'----> avg MRPS: {np.mean(MRPS)} with std of {mrps_std}')
