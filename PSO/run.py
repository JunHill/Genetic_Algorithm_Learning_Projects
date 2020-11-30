import numpy as np
import matplotlib.pyplot as plt
from core import *
from function_list import *
from scipy.stats import ttest_ind
import re
SEED = 18520750



for N in [128, 256, 512, 1024, 2048]:
    res_star = []
    with open(f'log/star/rastrigin_{N}.txt', 'r') as fi:
        for line in fi:
            try:
                res_rosen.append(float(re.search(r'(?<= - )(.*?)(?= - )', line).group(1).strip()))
            except:
                pass

    res_ring = []
    with open(f'log/ring/rastrigin_{N}.txt', 'r') as fi:
        for line in fi:
            try:
                res_rastri.append(float(re.search(r'(?<= - )(.*?)(?= - )', line).group(1).strip()))
            except:
                pass

    print(ttest_ind(res_rosen, res_rastri))

for N in [128, 256, 512, 1024, 2048]:
    res_star = []
    with open(f'log/star/rosenbrock_{N}.txt', 'r') as fi:
        for line in fi:
            try:
                res_rosen.append(float(re.search(r'(?<= - )(.*?)(?= - )', line).group(1).strip()))
            except:
                pass

    res_ring = []
    with open(f'log/ring/rosenbrock_{N}.txt', 'r') as fi:
        for line in fi:
            try:
                res_rastri.append(float(re.search(r'(?<= - )(.*?)(?= - )', line).group(1).strip()))
            except:
                pass

    print(ttest_ind(res_rosen, res_rastri))

