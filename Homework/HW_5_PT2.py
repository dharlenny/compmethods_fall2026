# imports
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse
import time

parser = argparse.ArgumentParser(description="Photon Path through Slab")
parser.add_argument('--slab_width', type = int, required = False, default = 1000, help = 'Width of the Slab (m)')
parser.add_argument('--mfp', type = float, required = False, default = 150.0, help = 'Mean Free Path in the Slab (m)')
parser.add_argument('--n_photons', type = int, required = False, default = 20, help = 'Number of Photons for the Sun Escape Time')
parser.add_argument('--n_runs', type = int, required = False, default = 1000, help = 'Number of Part A Runs for the Exit-Time')
args = parser.parse_args()

# constants
sigma_T = 6.652e-25
Rsun = 6.963e10
c = 2.99e10
r_max = 0.9 * Rsun
D_chunk = 1e7
n_runs = args.n_runs
events = np.zeros((n_runs, 2))
n_photons = args.n_photons
D_table = 10.0
frac = 0.01
H = 0.096 * Rsun
yr = 3.15e7 # seconds
L = args.slab_width # slab width in m
mfp = args.mfp # mean free path


rng = np.random.default_rng() # random event generator


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


path = photon() # creates your path


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


def init():
    line.set_data([], [])
    return line,

def animate(i):
    line.set_data(range(i + 1), path[:i + 1]) # x and y, length of paths
    return line,


anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(path), interval=500, blit=True)
writergif = animation.PillowWriter(fps=2)
anim.save('photon_slab.gif',writer=writergif)


# The Sun

def exit_event(D = 10.0):
    z, t = 0, 0
    mu = rng.uniform(-1, 1)
    while abs(z) < D:
        step = -np.log(rng.random())
        z += step *  mu
        t += step
        mu = rng.uniform(-1, 1)
    return t, np.sign(z)

def ne(r):
    return 2.5e26 * np.exp(-r / (0.096 * Rsun))

for i in range(n_runs):
    events[i, 0], events[i, 1] = exit_event(10)

def escape_time(events, D, rng):
    r, t = 0.0, 0.0
    while r < r_max:
        lmfp = 1.0 / (ne(r) * sigma_T)
        D_chunk = frac * H / lmfp
        tau, side = events[rng.integers(len(events))]
        t += tau * (D_chunk / D) ** 2 * 1 /c
        r += side * D_chunk * lmfp
        r = abs(r)
    return t

escape = np.zeros(n_photons)
t0 = time.perf_counter()
for i in range(n_photons):
    escape[i] = escape_time(events, D_table, rng)

stride = 1000

def sun_photon():
    r = 0.0
    sun_path = [r / Rsun]
    step = 0
    while r < r_max:
        lmfp = 1.0 / (ne(r) * sigma_T)
        D_chunk = frac * H / lmfp
        tau, side = events[rng.integers(len(events))]
        r += side * D_chunk * lmfp
        r = abs(r)
        step += 1
        if step % stride == 0:
            sun_path.append(r / Rsun)
    sun_path.append(r / Rsun)
    return np.array(sun_path)

sun_path = sun_photon()

fig2 = plt.figure(figsize = (6,5))
plt.xlim(0, len(sun_path))
plt.ylim(0, 1.0)
plt.grid()
plt.xlabel('Step Number')
plt.ylabel('r / R_sun')
plt.title('Photon Moving in the Sun')
line2, = plt.plot([], [], 'o-', markersize = 3)

def init2():
    line2.set_data([], [])
    return line2,

def animate2(i):
    line2.set_data(range(i + 1), sun_path[:i + 1])
    return line2,

anim2 = animation.FuncAnimation(fig2, animate2, init_func = init2, frames = len(sun_path), interval = 50, blit = True)
writergif2 = animation.PillowWriter(fps = 20)
anim2.save('photon_sun.gif', writer = writergif2)