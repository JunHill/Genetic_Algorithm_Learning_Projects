import numpy as np
import matplotlib.pyplot as plt


def read_result(location, filename):
	values = []
	std = []
	file = location + filename
	with open(file) as f:
		values = [float(x) for x in next(f).split()]
		std = [float(x) for x in next(f).split()]
	return values, std


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

