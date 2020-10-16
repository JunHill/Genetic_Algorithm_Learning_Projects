from bit_maximization import *
p = TrappedOneMaxProblem(10,1000, crossover="1X", seed = 18520750)
print(p.maximize())
