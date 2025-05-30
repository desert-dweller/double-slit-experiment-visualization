import numpy as np
import matplotlib.pyplot as plt
import cmath
from scipy.constants import hbar

# Wave function
def psi(r, t, a, hbar, m):
    """Compute the wave function value at distance r and time t."""
    gamma = cmath.sqrt(1 + (2j * hbar * a * t) / m)
    prefactor = (2 * a / np.pi)**0.25 / gamma
    exponent = -a * r**2 / gamma**2
    return prefactor * np.exp(exponent)

def waveplot(t):
    # Parameters
    a = 2                     # Controls initial width of the wave packet
    hbar = 1                  # Reduced Planck's constant 6.626e-34/(2*np.pi)
    m = 1                     # Particle mass 9.1093837e-31  
    x_min, x_max = -5.0, 5.0  # x-range of the box
    y_min, y_max = 0, 5.0     # y-range of the box
    nx = 500                  # Number of pixels along x
    ny = 250                  # Number of pixels along y

    # Create 2D grid of coordinates
    x = np.linspace(x_min, x_max, nx)
    y = np.linspace(y_min, y_max, ny)
    X, Y = np.meshgrid(x, y, indexing='xy')
    s1_x, s1_y = 1 + 1 * t, 0.0 + 2 * t
    s2_x, s2_y = -1 - 1 * t, 0.0 + 2 * t

    # Compute distances from each slit to every pixel
    r1 = np.sqrt((X - s1_x)**2 + (Y - s1_y)**2)
    r2 = np.sqrt((X - s2_x)**2 + (Y - s2_y)**2)

    # Compute wave function contributions from each slit
    psi_1 = psi(r1, t, a, hbar, m)
    psi_2 = psi(r2, t, a, hbar, m)

    # Total wave function (superposition)
    psi_total = (psi_1 + psi_2) / np.sqrt(2)

    # Probability density
    prob_density = np.abs(psi_total)**2

    # Create the figure
    fig = plt.figure(figsize=(10, 8))

    # Define the bottom subplot (heatmap) with a fixed position
    ax2 = fig.add_axes((0.1, 0.1, 0.8, 0.4))  # [left, bottom, width, height]
    im = ax2.imshow(
        prob_density,
        origin='lower',
        extent=(x_min, x_max, y_min, y_max),
        cmap='gray',
        aspect='equal'
    )
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    im.set_clim(0, 0.3)

    # Add colorbar in a separate axes
    cbar_ax = fig.add_axes((0.85, 0.1, 0.05, 0.4))  # [left, bottom, width, height]
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.set_label('Probability Density')

    # Calculate the plotting area of the heatmap (ax2)
    fig_width, fig_height = fig.get_size_inches()
    axes_height = 0.4 * fig_height  
    data_aspect = (x_max - x_min) / (y_max - y_min)  # 10 / 5 = 2
    H_plot = axes_height  
    W_plot = H_plot * data_aspect  
    axes_width = 0.8 * fig_width  
    left_margin = (axes_width - W_plot) / 2  
    left_plot = 0.1 + left_margin / fig_width 
    width_plot = W_plot / fig_width 

    # Define the top subplot (line plot) to match the heatmap's plotting area
    ax1 = fig.add_axes((left_plot, 0.55, width_plot, 0.4))
    ax1.plot(x, prob_density[249])
    ax1.set_title(f'Double-Slit Probability Distribution at t={t}')
    ax1.set_ylabel('Probability Density')
    ax1.set_ylim(0, 0.17)

    # Save and close the figure
    plt.savefig(f'frames/double_slit_2d_c{t:06.3f}.png')
    plt.close()

for t in range(0, 500, 1):
    waveplot(t/100)