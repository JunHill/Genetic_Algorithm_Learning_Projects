import numpy as np
import matplotlib.pyplot as plt


def plot_result(X, Y, xerr, yerr, plot_name):
	fig, ax = plt.subplots()
	ax.errorbar(X, Y, xerr=xerr, yerr=yerr, fmt='-o')
	ax.set_title(plot_name)
	ax.set_xlabel('MRPS')
	ax.set_ylabel('Number of evaluations')
	plt.xscale('log')
	plt.yscale('log')
	plt.savefig(f'/plot/{plot_name}.png')
