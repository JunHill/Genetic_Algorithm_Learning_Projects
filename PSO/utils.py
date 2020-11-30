import math
import numpy as np

def Rastrigin(x):
    return np.sum(x**2 - 10 * np.cos(2 * np.pi * x)) + 10 * x.shape[0]

def Ackley(x):
    part_1 = -0.2 * math.sqrt(0.5 * (x[0] * x[0] + x[1] * x[1]))
    part_2 = 0.5 * (math.cos(2 * math.pi * x[0]) + math.cos(2 * math.pi * x[1]))
    value = math.exp(1) + 20 - 20 * math.exp(part_1) - math.exp(part_2)
    return value

def RosenBrock(x):
    return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)

def Eggholder(x):
    return (-(x[1] + 47) * np.sin(np.sqrt(abs(x[0]/2 + (x[1]  + 47)))) -x[0] * np.sin(np.sqrt(abs(x[0] - (x[1]  + 47)))))
