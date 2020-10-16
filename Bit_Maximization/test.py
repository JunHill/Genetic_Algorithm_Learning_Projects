from plot import *


val, std = read_result('data/Eval/final_averages/', f'1X_trap')
#val1, std1 = read_result('data/Eval/final_averages/', f'UX_trap')
X, Y, Yerr = make_var(val, std, [], [])

mval, mstd = read_result('data/MRPS/final_averages/', f'1X_trap')
#mval1, mstd1 = read_result('data/MRPS/final_averages/', f'UX_trap')
mX, mY, mYerr = make_var(mval, mstd, [], [])

for i in range(2,4):
    print(f"{X[i]} & {round(mval[i], 2)} $\\pm$ {round(mstd[i],2)} & {round(val[i],2)} $\\pm$ {round(std[i], 2)} &  &  ")