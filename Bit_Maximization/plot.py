import numpy as np
import matplotlib.pyplot as plt


def read_result(location, filename):
	values = []
	std = []
	file = location + filename
	with open(file+'.txt') as f:
		values = [float(x) for x in next(f).split()]
	with open(file+'(std).txt') as f:
		std = [float(x) for x in next(f).split()]
	return values, std

def make_var(val1, std1, val2, std2):
	Y = [None, None]
	Yerr = [None, None]
	Y[0] = np.log(val1)
	Y[1] = np.log(val2)
	Yerr[0] = np.log(std1)
	Yerr[1] = np.log(std2)
	return np.log([10,20,40,80,160]), Y, Yerr
  
def plot_result(X, Y, yerr, plot_name, y_name):
	fig, ax = plt.subplots()
	ax.errorbar(X[0:len(Y[0])], Y[0], yerr=yerr[0], fmt='-o', color='limegreen', label = 'Single Point Cross-over')
	ax.errorbar(X[0:len(Y[1])], Y[1], yerr=yerr[1], fmt='-o', color='crimson', label = 'Uniform Cross-over')
	ax.set_title(plot_name)
	ax.set_xlabel('Problem Size')
	ax.set_ylabel(y_name)
	plt.xscale('log')
	plt.yscale('log')
	plt.legend()
	plt.savefig(f'plot/{plot_name}.png')

def plot_(type):
	val, std = read_result('data/Eval/final_averages/', f'1X_{type}')
	val1, std1 = read_result('data/Eval/final_averages/', f'UX_{type}')
	X, Y, Yerr = make_var(val, std, val1, std1)
	if type == 'normal':
		plot_result(X, Y, Yerr, 'OneMaxProblem (#Evals)', '#Evals')
	else:
		plot_result(X, Y, Yerr, 'Trapped OneMaxProblem (#Evals)', '#Evals')

	val, std = read_result('data/MRPS/final_averages/', f'1X_{type}')
	val1, std1 = read_result('data/MRPS/final_averages/', f'UX_{type}')
	X, Y, Yerr = make_var(val, std, val1, std1)
	if type == 'normal':
		plot_result(X, Y, Yerr, 'OneMaxProblem (MRPS)', 'MRPS')
	else:
		plot_result(X, Y, Yerr, 'Trapped OneMaxProblem (MRPS)', 'MRPS')

