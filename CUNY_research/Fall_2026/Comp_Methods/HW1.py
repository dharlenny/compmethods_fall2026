import argparse
import numpy as np

parser = argparse.ArgumentParser(description="Calculate the free fall time")
parser.add_argument('--height', type = float, required = True, help = 'Height of object above the ground in m')
parser.add_argument('--gravity', type = float, required = False, help = f"Gravity acting on your object in m/s²")
parser.add_argument('--planet', type = str, required = False, help = "Optional: See how long it would take for your "
                                                                     "object to fall on your chosen planet")

planet_gravity = {"Earth": 9.8,
           "Mars": 3.7,
           "Venus": 8.9,
           "Neptune": 11.1,
           "Saturn": 10.4,
           "Jupiter": 24.8,
           "Mercury": 3.7,
           "Uranus": 8.7}

args = parser.parse_args()

print("Welcome to the Free Fall Time Calculator!\n")

if args.planet:
    planet = args.planet
    gravity = planet_gravity[args.planet]
    print("Planet: " + planet)
    print("Gravity: " + str(planet_gravity[args.planet]) + " m/s²")

else:
    gravity = args.gravity
    print("Gravity: " + str(args.gravity) + " m/s²")

time = np.sqrt((2 * args.height) / gravity)

print("Height: " + str(args.height) + " m\n")
print(f"Your object took {time:.2f} seconds to fall!")


