import numpy as np
import matplotlib.pyplot as plt
from core import *
from function_list import *
from scipy.stats import ttest_ind
import re
# SEED = 18520750

# for N in [512, 1024, 2048]:
#     fi = open(f'log/rastrigin_{N}.txt', 'w')
#     avg = np.zeros((10,1))
#     for i in range(10):
#         print(f'Seeding... ({SEED})')
        
#         random.seed(SEED)
#         np.random.seed(SEED)

#         solver = PSO_Ring(N, 150000, Rastrigin_10)
#         res, val, pos = solver.solve()
#         print(f'{pos} - {val} - (SEED: {SEED})')
#         avg[i] = val
#         fi.write(f'{pos} - {val} - (SEED: {SEED})\n')
#         SEED += 1
#     fi.close()
#     print(f'average: {round(avg.mean(), 3)}({round(avg.std(), 3)})')
#     fin = open(f'log/rastrigin_final.txt', 'a+')
#     fin.write(f'N = {N} - average: {round(avg.mean(), 3)}({round(avg.std(), 3)})\n')
#     fin.close()

for N in [128, 256, 512, 1024, 2048]:
    res_rosen = []
    with open(f'log/star/rastrigin_{N}.txt', 'r') as fi:
        for line in fi:
            try:
                res_rosen.append(float(re.search(r'(?<= - )(.*?)(?= - )', line).group(1).strip()))
            except:
                pass

    res_rastri = []
    with open(f'log/rastrigin_{N}.txt', 'r') as fi:
        for line in fi:
            try:
                res_rastri.append(float(re.search(r'(?<= - )(.*?)(?= - )', line).group(1).strip()))
            except:
                pass
    #print(res_rosen)
    #print(res_rastri)
    print(ttest_ind(res_rosen, res_rastri))

