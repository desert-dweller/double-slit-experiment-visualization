from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
import numpy as np
import cmath
import io

app = Flask(__name__)

# Constants
hbar = 1.0
a = 2.0
m = 1.0

# Wave function
def psi(r, t, a, hbar, m):
    gamma = cmath.sqrt(1 + (2j * hbar * a * t) / m)
    prefactor = (2 * a / np.pi)**0.25 / gamma
    exponent = -a * r**2 / gamma**2
    return prefactor * np.exp(exponent)

# Computational grid
x_min, x_max = -10, 10
y_min, y_max = 0.0, 5.0
nx, ny = 500, 250
x = np.linspace(x_min, x_max, nx)
y = np.linspace(y_min, y_max, ny)
X, Y = np.meshgrid(x, y, indexing='xy')

def compute_prob_density(n, d, v, t):
    # Compute equally spaced slit positions centered around x=0
    slit_positions = [-(n-1)*d / 2 + i*d for i in range(n)]
    print(slit_positions)
    y_slit = 0.0 + v * t 
    print(y_slit)
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

    # Create figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Heatmap
    im = ax2.imshow(prob_density, origin='lower', extent=(x_min, x_max, y_min, y_max), 
                    cmap='gray', )
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    im.set_clim(0, 0.3)
    fig.colorbar(im, ax=ax2)
    

    # Compute average probability density across all y-positions for each x
    average_prob = np.mean(prob_density, axis=0)
    
    # Line plot at y=5.0 (screen position)
    ax1.plot(x, average_prob, 'b-')
    ax1.set_title(f'Probability Distribution at y=5.0 and t={t:.2f}')
    ax1.set_xlabel('x')
    ax1.set_ylabel('Probability Density')
    ax1.set_ylim(0, 1)
    
    # Save to buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return send_file(buf, mimetype='image/png')

app.run(debug=True)