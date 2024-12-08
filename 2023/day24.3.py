import re
from sympy import Eq, solve
from sympy.abc import x, y, z, a, b, c, t, u, v

# This is the simplest solution, but relies on sympy's ability to solve a set of non-linear equations.  9 equations with 9 unknowns.

hails = [[int(n) for n in re.split('[,@]', hail)] for hail in open(0)]
solution = solve([Eq(hails[0][0] + t * hails[0][3], x + t * a), Eq(hails[0][1] + t * hails[0][4], y + t * b), Eq(hails[0][2] + t * hails[0][5], z + t * c),
                  Eq(hails[1][0] + u * hails[1][3], x + u * a), Eq(hails[1][1] + u * hails[1][4], y + u * b), Eq(hails[1][2] + u * hails[1][5], z + u * c),
                  Eq(hails[2][0] + v * hails[2][3], x + v * a), Eq(hails[2][1] + v * hails[2][4], y + v * b), Eq(hails[2][2] + v * hails[2][5], z + v * c)])
print(solution[0][x] + solution[0][y] + solution[0][z])
