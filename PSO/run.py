import numpy as np
import matplotlib.pyplot as plt
from core import *
from function_list import *

SEED = 18520750

for N in [512, 1024, 2048]:
    fi = open(f'log/rastrigin_{N}.txt', 'w')
    avg = np.zeros((10,1))
    for i in range(10):
        print(f'Seeding... ({SEED})')
        
        random.seed(SEED)
        np.random.seed(SEED)

        solver = PSO_Ring(N, 150000, Rastrigin_10)
        res, val, pos = solver.solve()
        print(f'{pos} - {val} - (SEED: {SEED})')
        avg[i] = val
        fi.write(f'{pos} - {val} - (SEED: {SEED})\n')
        SEED += 1
    fi.close()
    print(f'average: {round(avg.mean(), 3)}({round(avg.std(), 3)})')
    fin = open(f'log/rastrigin_final.txt', 'a+')
    fin.write(f'N = {N} - average: {round(avg.mean(), 3)}({round(avg.std(), 3)})\n')
    fin.close()
