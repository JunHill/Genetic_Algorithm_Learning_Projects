import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from core import *
from config import *
from scipy.stats import ttest_ind
import re

SEED = 18520206

#---------------------------------------
#            Task 1
#---------------------------------------

def init():
    ax.set_xlim(-func['search_domain'], func['search_domain'])
    ax.set_ylim(-func['search_domain'], func['search_domain'])
    return ln,

def update(frame, func_name, topo):
    res = []
    with open(f'result/{topo}/{func_name}/gen{frame}.txt') as fi:
        for line in fi:
            li = np.array([0,0], dtype='float64')
            li[0],li[1] = map(float,line.split())
            res.append(li)
        res = np.array(res)
    xdata = res[:,0]
    ydata = res[:,1]
    print(xdata)
    ax.set_title(f'GEN {frame + 1}')
    ln.set_data(xdata, ydata)
    return ln,

random.seed(SEED)
np.random.seed(SEED)
function_list = [Rastrigin_2, Rosenbrock_2, Ackley, Eggholder]
function_name = ['Rastrigin_2', 'Rosenbrock_2', 'Ackley', 'Eggholder']
for func, name in zip(function_list, function_name):
    for topo in ['star','ring']:
        solver = PSO(32, 50, func, topo)
        res, val, pos = solver.solve() #(track = True)
        print(f'{pos} - {val} - (TOPO: {topo}) - (FUNC: {name})\n')
        xlist = np.linspace(-func['search_domain'], func['search_domain'], 100)
        ylist = np.linspace(-func['search_domain'], func['search_domain'], 100)
        X, Y = np.meshgrid(xlist, ylist)
        if func == Rastrigin_2:
            Z = (X**2 - 10 * np.cos(2 * 3.14 * X)) + \
                (Y**2 - 10 * np.cos(2 * 3.14 * Y)) + 20
        elif func == Rosenbrock_2:
            Z = (1.-X)**2 + 100.*(Y-X*X)**2
        elif func == Ackley:
            a = 20
            b = 0.2
            c = 2 * np.pi
            sum_sq_term = -a * np.exp(-b * np.sqrt(X*X + Y*Y) / 2)
            cos_term = -np.exp((np.cos(c*X) + np.cos(c*Y)) / 2)
            Z = a + np.exp(1) + sum_sq_term + cos_term
        elif func == Eggholder:
            Z = -(Y + 47) * np.sin(np.sqrt(abs(X/2 + (Y + 47)))) -X * np.sin(np.sqrt(abs(X - (Y + 47))))
        fig,ax=plt.subplots(1,1)
        cp = ax.contourf(X, Y, Z)
        xdata, ydata = [], []
        ln, = plt.plot([], [], 'ro')

        ani = FuncAnimation(fig, lambda frame,func_name=name,topo=topo: update(frame, func_name, topo), \
            frames=np.arange(50, step=4), init_func=init, blit=True,interval=500)
        ani.save(f"plot/{func['name']}_{topo}.gif")

#---------------------------------------
#            Task 2
#---------------------------------------
function_list = [Rastrigin_10, Rosenbrock_10]
function_name = ['Rastrigin_10', 'Rosenbrock_10']
for N in [128, 256, 512, 1024, 2048]:
    print(f'Using pop size {N}')
    regex = '-\s' + '[0-9]+' + '.' + '[0-9]+' + '\s' + '-'
    regex_ = '-\s' + '[0-9]+' + '.' + '[0-9]+' + 'e-' + '[0-9]+' + '\s' + '-'
    for func, name in zip(function_list, function_name):
        print('   Applying on ', name)
        for topo in ['star','ring']:
            SEED = 18520206
            fi = open(f'log/{topo}/{name[:-3]}_{N}.txt', 'w')
            avg = np.zeros((10,1))
            for i in range(10):
                print(f'Seeding... ({SEED})')
                random.seed(SEED)
                np.random.seed(SEED)

                solver = PSO(N, 150000, func, topo)
                res, val, pos = solver.solve()
                print(f'{pos} - {val} - (SEED: {SEED}) (FUNC: {name[:-3]}) (TOPO: {topo})')
                avg[i] = val
                fi.write(f'{pos} - {val} - (SEED: {SEED})\n')
                SEED += 1
            fi.close()
            print(f'average: {round(avg.mean(), 3)}({round(avg.std(), 3)})')
            fin = open(f'log/{topo}/{name[:-3]}_{N}_final.txt', 'a+')
            fin.write(f'N = {N} - average: {round(avg.mean(), 3)}({round(avg.std(), 3)})\n')
            fin.close()

        res_star = []
        with open(f'log/star/{name[:-3]}_{N}.txt', 'r') as fi:
            fi = fi.read().split('\n')
            for line in fi:
                search = re.findall(regex, line)
                if len(search):
                    res_star.append(float(search[0][2:-2]))
                search = re.findall(regex_, line)
                if len(search):
                    res_star.append(float(search[0][2:-2]))
        res_ring = []
        with open(f'log/ring/{name[:-3]}_{N}.txt', 'r') as fi:
            fi = fi.read().split('\n')
            for line in fi:
                search = re.findall(regex, line)
                if len(search):
                    res_ring.append(float(search[0][2:-2]))
                search = re.findall(regex_, line)
                if len(search):
                    res_ring.append(float(search[0][2:-2]))
        print('star ', res_star)
        print('ring ', res_ring)
        print(ttest_ind(res_star, res_ring))
