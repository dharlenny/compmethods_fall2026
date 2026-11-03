# imports
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Photon Path through Slab")
parser.add_argument('--slab_width', type = int, required = False, default = 1000, help = 'Width of the Slab (m)')
parser.add_argument('--random_seed', type = int, required = False, default = 1, help = 'Pseudo-random Generator for the Monte-Carlo Integration')
args = parser.parse_args()

# constants
mfp = 150.0 # meat free path
L = args.slab_width # slab width in m
# %%
def photon():
    z = 0.0 # movement with z-axis
    photon_path = [z]
    mu = 1.0
    while 0 <= z <= L:
        step = -mfp * np.log(np.random.rand()) # random step
        z += step * mu  # moving along the slab
        photon_path.append(z) # stores the move
        mu = np.random.uniform(-1, 1) # where to move next
    return np.array(photon_path)
# %%
np.random.seed(args.random_seed) # "random" number generator
path = photon() # creates your path
# %%
fig = plt.figure(figsize=(6,5))
plt.xlim(0, len(path))
plt.ylim(-100, L + 100)
plt.axhline(0, color = 'dodgerblue')
plt.axhline(L, color = 'dodgerblue')
plt.grid()
plt.xlabel("Step Number")
plt.ylabel("Z (m)")
plt.title("Photon Moving within a Slab")
line, = plt.plot([], [], 'o-')
# %%
def init():
    line.set_data([], [])
    return line,

def animate(i):
    line.set_data(range(i + 1), path[:i + 1]) # x and y, length of paths
    return line,
# %%
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(path), interval=500, blit=True)
# %%
writergif = animation.PillowWriter(fps=2)
anim.save('photon_slab.gif',writer=writergif)