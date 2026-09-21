#imports
import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# parser arguments w/ inputs that can be added
# parser = argparse.ArgumentParser(description="Integration Calculator")
# parser.add_argument('--Lower Limit', type = float, required = True, help = 'Upper limit in the integral')
# parser.add_argument('--Upper Limit', type = float, required = False, help = 'Lower limit in the integral')
# parser.add_argument('--planet', type = str, required = False, help = "Optional: See how long it would take for your ")

# integration

x = np.linspace(0, 3, 300)

def integrand(t):
    return np.exp**(-t**2)

result = quad(integrand, x)

print(result)