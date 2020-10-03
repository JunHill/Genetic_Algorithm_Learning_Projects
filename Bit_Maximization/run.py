from bit_maximization import OneMaxProblem, TrappedOneMaxProblem
import sys

Problem = OneMaxProblem(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
print(f'\nFINDING SOLUTION OF ONEMAXPROBLEM...')
Problem.maximize_single_point()
Problem.reset()
Problem.maximize_uniform()

TrapProblem = TrappedOneMaxProblem(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
print(f'\nFINDING SOLITON OF TRAP ONEMAXPROBLEM...')
TrapProblem.maximize_single_point()
TrapProblem.reset()
TrapProblem.maximize_uniform()