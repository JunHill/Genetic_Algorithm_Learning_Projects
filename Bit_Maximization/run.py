from bit_maximization import OneMaxProblem, TrappedOneMaxProblem
import sys

print(f'\nFINDING SOLUTION OF ONEMAXPROBLEM...')
Problem = OneMaxProblem(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
Problem.maximize_single_point()
Problem.reset()
Problem.maximize_uniform()

print(f'\nFINDING SOLITON OF TRAP ONEMAXPROBLEM...')
try: 
	assert int(sys.argv[1]) % 5 == 0
	TrapProblem = TrappedOneMaxProblem(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
	
	TrapProblem.maximize_single_point()
	TrapProblem.reset()
	TrapProblem.maximize_uniform()
except:
	print("Problem size should be multiple of 5 (k)")
