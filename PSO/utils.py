import math
import numpy as np

def Rastrigin_2_f(pos):
    return (pos[0]**2 - 10 * np.cos(2 * np.pi * pos[0])) + (pos[1]**2 - 10 * np.cos(2 * np.pi * pos[1])) + 20

def Rastrigin_10_f(pos):
    res = 100
    for i in range(10):
        res += (pos[i]**2 - 10 * np.cos(2 * np.pi * pos[i]))
    return res

def Ackley_f(pos):
    part_1 = -0.2*math.sqrt(0.5*(pos[0]*pos[0] + pos[1]*pos[1]))
    part_2 = 0.5*(math.cos(2*math.pi*pos[0]) + math.cos(2*math.pi*pos[1]))
    value = math.exp(1) + 20 -20*math.exp(part_1) - math.exp(part_2)
    return value

def RosenBrock(x):
    return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)

def Eggholder_f(x):
    return (-(x[1] + 47) * np.sin(np.sqrt(abs(x[0]/2 + (x[1]  + 47)))) -x[0] * np.sin(np.sqrt(abs(x[0] - (x[1]  + 47)))))