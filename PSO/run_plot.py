
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from core import *
from function_list import *

def init():
    ax.set_xlim(-func['search_domain'], func['search_domain'])
    ax.set_ylim(-func['search_domain'], func['search_domain'])
    return ln,

def update(frame):
    res = []
    with open(f'result/star/gen{frame}.csv') as fi:
        for line in fi:
            li = np.array([0,0], dtype='float64')
            li[0],li[1] = map(float,line.split())
            res.append(li)
        res = np.array(res)
    xdata = res[:,0]
    ydata = res[:,1]
    ax.set_title(f'GEN {frame + 1}')
    ln.set_data(xdata, ydata)
    return ln,

function_list = [Eggholder]
for func in function_list:
    random.seed(18520751)
    np.random.seed(18520751)
    solver = PSO_Star(32, 50, func)
    a,b,c = solver.solve(track=True)
    print(b)
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

    ani = FuncAnimation(fig, update, frames=np.arange(50, step=4),
                        init_func=init, blit=True,interval=500)
    ani.save(f"plot/{func['name']}_Star.gif")