from flask import Flask, render_template, request, send_file
import matplotlib
matplotlib.use('Agg')   # ← Must come before importing pyplot!
import matplotlib.pyplot as plt
import numpy as np
import cmath
import io

app = Flask(__name__)

# Constants
hbar = 1.0
a = 2
m = 1.0

# Wave function Ψ(r,t) = (2a/π)^{1/4} / γ * exp(-a r²/γ²), 
def psi(r, t, a, hbar, m):
    gamma = cmath.sqrt(1 + (2j * hbar * a * t) / m)
    prefactor = (2 * a / np.pi)**0.25 / gamma
    exponent = -a * r**2 / gamma**2
    return prefactor * np.exp(exponent)

# Computational grid
x_min, x_max = -15, 15
y_min, y_max = 0.0, 15.0
nx, ny = 500, 250
x = np.linspace(x_min, x_max, nx)
y = np.linspace(y_min, y_max, ny)
X, Y = np.meshgrid(x, y, indexing='xy')

def compute_prob_density(n, d, v, t):
    # Compute equally spaced slit positions centered around x=0
    slit_positions = [-(n-1)*d / 2 + i*d for i in range(n)]
    y_slit = 0.0 + v * t

    psi_total = np.zeros_like(X, dtype=complex)

    for x_slit in slit_positions:
        r = np.sqrt((X - x_slit)**2 + (Y - y_slit)**2)
        psi_i = psi(r, t, a, hbar, m)

        psi_total += psi_i
    psi_total /= np.sqrt(n)  # Normalize by sqrt(n)
    return np.abs(psi_total)**2

@app.route('/')
def index():
    # Default values
    defaults = {'n': 2, 'd': 2.0, 'v': 1.0, 't': 0.0}
    return render_template('index.html', **defaults)

@app.route('/plot')
def plot():
    # Get parameters from request with defaults
    n = int(request.args.get('n', 2))
    d = float(request.args.get('d', 2.0))
    v = float(request.args.get('v', 1.0))
    t = float(request.args.get('t', 0.0))
    
    # Compute probability density
    prob_density = compute_prob_density(n, d, v, t)
    
    # Compute average probability density across all y-positions for each x
    average_prob = np.mean(prob_density, axis=0)

    # Create figure with GridSpec layout
    fig = plt.figure(figsize=(10, 10))
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 0.05], height_ratios=[1, 1])  # 2 rows, 2 cols; col 1 narrow for colorbar
    ax1 = fig.add_subplot(gs[0, 0])                         # Line plot in row 0, col 0
    ax2 = fig.add_subplot(gs[1, 0], sharex=ax1)             # Heatmap in row 1, col 0, shares x-axis with ax1
    cax = fig.add_subplot(gs[1, 1])                         # Colorbar in row 1, col 1, next to heatmap

    # Heatmap on ax2
    im = ax2.imshow(prob_density, origin='lower', extent=(x_min, x_max, y_min, y_max), 
                    cmap='gray')
    im.set_clim(0, 0.3)
    fig.colorbar(im, cax=cax, fraction=1.0, aspect=10, shrink=0.5)  # Add colorbar next to heatmap

    # Line plot on ax1
    ax1.plot(x, average_prob, 'b-')
    ax1.set_title(f'Probability Distribution at t={t:.2f}')
    ax1.set_ylabel('Probability Density')
    ax1.set_ylim(0, 0.3)

    # Set labels (x-label only on ax2 since x-axis is shared)
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Save to buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return send_file(buf, mimetype='image/png')

# app.run(debug=True)