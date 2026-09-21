# import
import matplotlib.pyplot as plt
import argparse
import numpy as np

# parser arguments w/ inputs that can be added
parser = argparse.ArgumentParser(description="Integration Solver")
parser.add_argument('--upper_limit', type = int, required = False, default = 3, help = 'Upper limit for the integral '
                                                                                       'with a default value of 3')
parser.add_argument('--lower_limit', type = int, required = False, default = 0, help = 'Lower limit for the integral '
                                                                                       'with a default value of 0')
parser.add_argument('--num_point', type = int, required = False, default = 300, help = 'Number of points for the integral'
                                                                                       'calculation with a default '
                                                                                       'value of 300')
parser.add_argument('--index', type = int, required = False, default = 30, help = "Index element to view")

args = parser.parse_args()

# integration function
def integrand(t):
    return np.exp(-t**(2))

# step sizing and array creation
x_values = np.arange(args.lower_limit, args.upper_limit + 0.1 , 0.1)
E_x = []

# integration method
for x in x_values:
    t = np.linspace(args.lower_limit, x, args.num_point)
    E_values = np.trapezoid(integrand(t), t)
    E_x.append(E_values)

print(f"E({x_values[args.index]}) = {E_x[args.index]:.6f}")

# plotting
plt.plot(x_values, E_x, color="dodgerblue")
plt.title(r'$E(x) = \int_{0}^{x} e^{-t^2} dt$')
plt.ylabel("E(x)")
plt.xlabel("x")

# plots the index point
mark_x = x_values[args.index]
mark_y = E_x[args.index]
plt.plot(mark_x, mark_y, marker = 'x', markersize = 10, markeredgewidth = 3, color = 'darkviolet', label = f'E({x_values[args.index]:.1f})')
plt.legend()
plt.grid()
plt.show()