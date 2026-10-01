import argparse
from astropy.constants import G, M_earth

# parser arguments
parser = argparse.ArgumentParser(description="Calculates the L1 distance"
                                             "using the secant method")
parser.add_argument('--r0', type = float, required = False, default = 3.0e8, help = 'First starting value for r in meters'
                                                                   '(default is 3.0e8)')
parser.add_argument('--r1', type = float, required = False, default = 3.4e8, help = 'Second starting value for r in meters'
                                                                   '(default is 3.4e8)')
parser.add_argument('--tolerance', type = float, required = False, default = 1e-6, help = 'Tolerance of convergence'
                                                                                           '(default: 1e-6)')
parser.add_argument('--iterations', type = int, required = False, default = 10, help = 'Number of iterations (default: 100)')

args = parser.parse_args()


# constants
G = G.value
M = M_earth.value
m = 7.348e22 # mass of moon in kg
R = 3.844e8 # Earth-Moon distance in meters
w = 2.662e-6 # angular velocity


# main function
def f(r):
    return (G * M / r ** 2) - (G * m / (R - r) ** 2) - ((w ** 2) * r )


# second function
r0 = args.r0
r1 = args.r1
for i in range(args.iterations):
    r2 = r1 - f(r1) * (r1 - r0) / (f(r1) - f(r0))
    if f(r1) == f(r0):
        break
    if abs(r2 - r1) < args.tolerance * abs(r2):
        break
    r0 = r1
    r1 = r2

print(f"L1 distance from Earth is {r2:.6e} meters.")

