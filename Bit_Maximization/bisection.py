from bit_maximization import OneMaxProblem, TrappedOneMaxProblem

def run_multiple_times(times, problem_size, N, random_seed, mode):
	evals = 0
	for i in range(times):
		result = True
		x = 0
		#print(f"\t{i}. Maximizing with random_seed {random_seed}")
		if mode['problem'] == "normal":
			Problem = OneMaxProblem(problem_size, N, random_seed)
		elif mode['problem'] == "trap":
			Problem = TrappedOneMaxProblem(problem_size, N, random_seed)

		if mode['cross-over'] == "single_point":
			x, result = Problem.maximize_single_point()
		elif mode['cross-over'] == "uniform":
			x, result = Problem.maximize_uniform()
		if result == False:
			return 0, False
		evals += x
		random_seed += 1
	return evals/times, True


def get_MRPS_upper_bound(problem_size, random_seed, mode):
	N_upper = 4

	evals, success = run_multiple_times(10, problem_size, N_upper, random_seed, mode)
	while (not success and N_upper < 8192):

		N_upper = N_upper * 2
		print(f'  Running N_upper: {N_upper}')
		evals, success = run_multiple_times(10, problem_size, N_upper, random_seed, mode)
		print(f'  success: {success}')
	return N_upper, evals, success

def find_MRPS(N_upper, evals_upper, problem_size, random_seed, mode):
	N_lower = N_upper // 2
	evals = evals_upper
	while (N_upper - N_lower)/N_upper > 0.1:
		N = (N_upper + N_lower) // 2
		
		x, success = run_multiple_times(10, problem_size, N, random_seed, mode)

		print(f'  N_upper: {N_upper} - N_lower: {N_lower} - success: {success} - x: {x}')
		if success:
			N_upper = N
		else:
			N_lower = N
		
		if (N_upper - N_lower) <= 2:
			return evals, N_upper
		if success:
			evals = x
	return evals, N_upper

def bisection(problem_size, random_seed, mode, save=False):
	N_upper, evals_upper, success = get_MRPS_upper_bound(problem_size, random_seed, mode)
	if not success:
		return 0, 0, False
	evals, MRPS = find_MRPS(N_upper, evals_upper, problem_size, random_seed, mode)
	if save:
		with open(f'data/Eval/{mode["cross-over"]}_{mode["problem"]}_{problem_size}.txt', 'a') as f:
			f.write(str(evals) + " ")

		with open(f'data/MRPS/{mode["cross-over"]}_{mode["problem"]}_{problem_size}.txt', 'a') as f:
			f.write(str(MRPS) + " ")
	return evals, MRPS, True

def run_bisection_multiple_times(times, problem_size, random_seed, mode, save=False):
	evals = []
	MRPS = []
	for i in range(times):
		
		print(f'\nRUN BISECTION WITH RANDOM_SEED: {random_seed}')
		e, m, success = bisection(problem_size, random_seed, mode, save)
		if not success:
			return [], [], False
		evals.append(e)
		MRPS.append(m)
		random_seed += 10

	return evals, MRPS, True