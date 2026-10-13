# imports
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import argparse


# star : TIC0000091961

# opening/assignment fits file
hdul = fits.open('tic0000091961.fits')
times = hdul[1].data['times']
fluxes = hdul[1].data['fluxes']
ferrs = hdul[1].data['ferrs']

parser = argparse.ArgumentParser(description="Investigating TESS Light Curves")
parser.add_argument('--epoch', type = int, required = False, default = 2, help = 'Two available epochs to investigate choose 1 or 2 (default is 2)')

args = parser.parse_args()


# plotting light curve
plt.figure(figsize=(12,5))
plt.scatter(times, fluxes,s=1.9)
plt.xlabel('Time (BJD)')
plt.ylabel('Flux')
plt.title('TIC 0000091961 Light Curve')
plt.show()


# using discrete fourier transform
def dft_star(y):
    N = len(y)
    N_real = N // 2+1
    c = np.zeros(N_real, dtype='complex')
    for k in range(N_real):
        for n in range(N):
            c[k] += y[n] * np.exp(-2j * np.pi * k * n / N) # DFT equation
    return c


# parse argument for epoch
if args.epoch == 2:
    mask = (times >= 2300) & (times <= 2400)
elif args.epoch == 1:
    mask = (times >= 1600) & (times <= 1630)


# new variables due to masking
times_mask = times[mask]
fluxes_masked = fluxes[mask]
ferrs_masked = ferrs[mask]

c = dft_star(fluxes_masked)

plt.figure(figsize=(12,5))
plt.plot(times_mask, fluxes_masked, color = 'dodgerblue')
plt.xlabel('Time (BJD)')
plt.ylabel('Flux')
plt.title('TIC 0000091961 Direct Fourier Transform')
plt.grid(True, alpha=0.3)
plt.show()


# plotting power spectrum
abs_c = abs(c)**2 # power spectrum equation
k = np.arange(len(c))
abs_c[0]=0

plt.figure(figsize=(10,5))
plt.ylabel('$|c|^2$')
plt.xlabel('k')
plt.title('TIC 0000091961 Power Spectrum')
plt.plot(k, abs_c, color = 'dodgerblue')
plt.show()


times_new = times[mask]
fluxes_new = fluxes[mask]
ferrs_new = ferrs[mask]
N = len(fluxes_new)
N_real = len(c)

# inverse direct fourier transform
c = dft_star(fluxes_new)  # this is N//2 + 1 coefficients
c_full = np.zeros(N, dtype='complex')
c_full[:N_real] = c
c_full[N_real:] = np.conj(c[1:N_real-1][::-1])

def inverse_dft(c_full, N):
    y = np.zeros(N, dtype='complex')
    for k in range(N):
        for n in range(N):
            y[n] += c_full[k] * np.exp(2j * np.pi * k * n / N)
    return (y / N).real

inverse_flux = inverse_dft(c_full, N)

# plotting DFT
plt.figure(figsize=(14, 5))
plt.plot(times_new, inverse_flux, color = 'dodgerblue')
plt.xlabel('Time (BJD)')
plt.ylabel('Flux')
plt.title('TIC 0000091961 Inverse Transform')
plt.grid(True, alpha=0.3)
plt.show()

# plotting normal fourier transform vs direct fourier transform
plt.figure(figsize=(14, 5))
plt.scatter(times_new, fluxes_new, s=0.5, color = 'dodgerblue', label = 'Original data')
plt.plot(times_new, inverse_flux, color = 'crimson', alpha = 0.7, label='Inverse DFT')
plt.xlabel('Time (BJD)')
plt.ylabel('Flux')
plt.title('TIC 0000091961 Inverse Transform Comparison')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()