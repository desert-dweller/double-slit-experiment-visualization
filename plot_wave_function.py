import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

hbar = 1.0  # Natural units

def compute_gamma_squared(t, m, hbar=1.0):
    """Compute γ² = 1 + (2iħt)/m (more stable than computing sqrt first)."""
    return 1 + (2j * hbar * t) / m

def psi(x, t, a, m, x0=0.0, hbar=1.0):
    """Compute a Gaussian wave packet centered at x0."""
    gamma_squared = compute_gamma_squared(t, m, hbar)
    gamma = cmath.sqrt(gamma_squared)
    
    prefactor = (2 * a / math.pi) ** (1/4)
    gamma_term = 1 / gamma
    exponent = -a * (x - x0)**2 / gamma_squared
    exp_term = cmath.exp(exponent)
    
    return prefactor * gamma_term * exp_term

def psi_double_slit(x, t, a, m, d, hbar=1.0):
    """Compute the superposed wave function from two slits separated by 2d."""
    psi_1 = psi(x, t, a, m, x0=-d, hbar=hbar)  # Slit at -d
    psi_2 = psi(x, t, a, m, x0=d, hbar=hbar)   # Slit at +d
    return psi_1 + psi_2

# Parameters
a = 1.0      # Gaussian width parameter
m = 1.0      # Mass
d = 1.5      # Half-distance between slits (slits at x = ±d)
x_vals = np.linspace(-5, 5, 500)  # Position range
t_start = 0.0
t_end = 2.0
num_frames = 100
t_vals = np.linspace(t_start, t_end, num_frames)  # Time steps for animation

# Set up the figure and axis for animation
fig, ax = plt.subplots(figsize=(10, 6))
line_real, = ax.plot([], [], label='Real part')
line_imag, = ax.plot([], [], label='Imaginary part')
ax.set_xlabel("Position (x)")
ax.set_ylabel("ψ(x,t)")
ax.set_title("Wave Function Animation (Double Slit)")
ax.legend()
ax.grid(True)
ax.set_xlim(-5, 5)
ax.set_ylim(-1.5, 1.5)  # Adjust based on expected wave function amplitude

# Initialization function for the animation values
def init():
    line_real.set_data([], [])
    line_imag.set_data([], [])
    return line_real, line_imag

# Animation update function
def update(t):
    psi_vals = [psi_double_slit(x, t, a, m, d) for x in x_vals]
    line_real.set_data(x_vals, [z.real for z in psi_vals])
    line_imag.set_data(x_vals, [z.imag for z in psi_vals])
    ax.set_title(f"Wave Function at t = {t:.2f} (Double Slit)")
    return line_real, line_imag

ani = FuncAnimation(fig, update, frames=t_vals, init_func=init, blit=True, interval=50)
ani.save('wave_function_animation.mp4', writer='ffmpeg', fps=20)
plt.close()

# Plot probability density over time (static)
times = [0, 0.5, 1.0, 2.0]
plt.figure(figsize=(10, 6))
for t in times:
    psi_vals = [psi_double_slit(x, t, a, m, d) for x in x_vals]
    prob_density = [abs(z)**2 for z in psi_vals]
    plt.plot(x_vals, prob_density, label=f't = {t}')
plt.xlabel("Position (x)")
plt.ylabel("|ψ(x,t)|²")
plt.title("Probability Density at Different Times (Double Slit)")
plt.legend()
plt.grid(True)
plt.savefig('double_slit_probability_density.png')
plt.close()