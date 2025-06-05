import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cmath
from scipy.constants import hbar
import tkinter as tk
from tkinter import ttk

x_min, x_max = -5.0, 5.0
y_min, y_max = 0.0, 5.0
nx, ny = 500, 250
x = np.linspace(x_min, x_max, nx)
y = np.linspace(y_min, y_max, ny)
X, Y = np.meshgrid(x, y, indexing='xy')

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

# Compute probability density
def compute_prob_density(s1_x, s2_x, v, t):
    s1_y = 0.0 + v*t
    s2_y = 0.0 + v*t

    r1 = np.sqrt((X - s1_x)**2 + (Y - s1_y)**2)
    r2 = np.sqrt((X - s2_x)**2 + (Y - s2_y)**2)

    psi_1 = psi(r1, t, a, hbar, m)
    psi_2 = psi(r2, t, a, hbar, m)
    psi_total = (psi_1 + psi_2) / np.sqrt(2)
    return np.abs(psi_total)**2, x

# Update function
def update():
    s1_x = float(s1_slider.get())
    s2_x = float(s2_slider.get())

    v = float(v_slider.get())
    t = float(t_slider.get())
    prob_density, _ = compute_prob_density(s1_x, s2_x, v, t)
    
    # Update line plot
    line[0].set_ydata(prob_density[249])  # Detector at y=5
    ax1.set_title(f'Double-Slit Probability Distribution at t={t:.2f}')
    ax1.relim()
    ax1.autoscale_view()
    
    # Update heatmap
    im.set_array(prob_density)
    canvas.draw()

# Create main window
root = tk.Tk()
root.title("Double-Slit Experiment")
root.geometry("800x600")

# Initial parameters
s1_init, s2_init, v_init, t_init = -1, 1, 1, 0.0
hbar = 1.0

# Initial data
prob_density, x = compute_prob_density(s1_init, s2_init, v_init, t_init)

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
line = ax1.plot(x, prob_density[249])
ax1.set_ylabel('Probability Density')
ax1.set_ylim(0, 0.17)

# Embed figure in tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

# Create sliders
tk.Label(root, text="Adjust Parameters:").pack()

s1_slider = ttk.Scale(root, from_=0.1, to=5.0, orient=tk.HORIZONTAL, length=300, value=s1_init, command=lambda x: update())
s1_slider.set(s1_init)
tk.Label(root, text="slit 1 position").pack()
s1_slider.pack()

s2_slider = ttk.Scale(root, from_=0.1, to=5.0, orient=tk.HORIZONTAL, length=300, value=s2_init, command=lambda x: update())
s2_slider.set(s2_init)
tk.Label(root, text="slit 2 position").pack()
s2_slider.pack()

v_slider = ttk.Scale(root, from_=0.1, to=20.0, orient=tk.HORIZONTAL, length=300, value=v_init, command=lambda x: update())
v_slider.set(v_init)
tk.Label(root, text="v (velocity)").pack()
v_slider.pack()

t_slider = ttk.Scale(root, from_=0.0, to=5.0, orient=tk.HORIZONTAL, length=300, value=t_init, command=lambda x: update())
t_slider.set(t_init)
tk.Label(root, text="t (time)").pack()
t_slider.pack()


# Start the application
root.mainloop()