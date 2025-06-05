import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import cmath

# Constants 
hbar = 1.0
a = 2.0
m = 1.0    

# Wave function definition
def psi(r, t, a, hbar, m):
    """Compute the wave function for a given distance r and parameters."""
    gamma = cmath.sqrt(1 + (2j * hbar * a * t) / m)
    prefactor = (2 * a / np.pi)**0.25 / gamma
    exponent = -a * r**2 / gamma**2
    return prefactor * np.exp(exponent)

class DoubleSlitApp(tk.Tk):
    def __init__(self):
        """Initialize the Tkinter application window and its components."""
        super().__init__()
        self.title("Double-Slit Experiment")

        # Define the computational grid
        self.x_min, self.x_max = -10.0, 10.0
        self.y_min, self.y_max = 0.0, 5.0
        nx, ny = 500, 250
        self.x = np.linspace(self.x_min, self.x_max, nx)
        self.y = np.linspace(self.y_min, self.y_max, ny)
        self.X, self.Y = np.meshgrid(self.x, self.y, indexing='xy')

        # Set up the Matplotlib figure and axes
        self.fig = Figure(figsize=(10, 8))
        fig_width, fig_height = 10, 8  # Figure size in inches
        left_ax2, bottom_ax2, width_ax2, height_ax2 = 0.1, 0.1, 0.8, 0.4
        data_aspect = (self.x_max - self.x_min) / (self.y_max - self.y_min)  # 2.0

        # Calculate plotting area dimensions for alignment
        h_plot = height_ax2 * fig_height
        w_plot = h_plot * data_aspect
        axes_width = width_ax2 * fig_width
        left_margin = (axes_width - w_plot) / 2
        left_plot = left_ax2 + (left_margin / fig_width)
        width_plot = w_plot / fig_width

        # Create axes for heatmap, colorbar, and line plot
        self.ax2 = self.fig.add_axes((0.1, 0.1, 0.8, 0.4))  # Heatmap
        self.cbar_ax = self.fig.add_axes((0.85, 0.1, 0.05, 0.4))       # Colorbar
        self.ax1 = self.fig.add_axes((left_plot, 0.55, width_plot, 0.4))      # Line plot

        # Embed the figure into the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a frame for sliders 
        slider_frame = tk.Frame(self)
        slider_frame.pack(fill=tk.X)

        # Initialize sliders with default values
        s1_init, s2_init, s3_init, v_init, t_init = -3.0, 3.0, 0.0, 1.0, 0.0
        self.s1_scale = tk.Scale(slider_frame, from_=-5.0, to=5.0, resolution=0.1, 
                                label="slit 1 position", orient=tk.HORIZONTAL)
        self.s2_scale = tk.Scale(slider_frame, from_=-5.0, to=5.0, resolution=0.1, 
                                label="slit 2 position", orient=tk.HORIZONTAL)
        self.s3_scale = tk.Scale(slider_frame, from_=-5.0, to=5.0, resolution=0.1, 
                                label="slit 2 position", orient=tk.HORIZONTAL)
        self.v_scale = tk.Scale(slider_frame, from_=0.1, to=5.0, resolution=0.1, 
                                label="v (velocity)", orient=tk.HORIZONTAL)
        self.t_scale = tk.Scale(slider_frame, from_=0.0, to=5.0, resolution=0.1, 
                                label="t (time)", orient=tk.HORIZONTAL)
        self.s1_scale.set(s1_init)
        self.s2_scale.set(s2_init)
        self.s3_scale.set(s3_init)
        self.v_scale.set(v_init)
        self.t_scale.set(t_init)

        # Arrange sliders horizontally
        self.s1_scale.pack(side=tk.BOTTOM, expand=True, fill=tk.X)
        self.s2_scale.pack(side=tk.BOTTOM, expand=True, fill=tk.X)
        self.s3_scale.pack(side=tk.BOTTOM, expand=True, fill=tk.X)

        self.v_scale.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.t_scale.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Connect sliders to the update function
        self.s1_scale.config(command=lambda val: self.update_plots())
        self.s2_scale.config(command=lambda val: self.update_plots())
        self.s3_scale.config(command=lambda val: self.update_plots())
        self.v_scale.config(command=lambda val: self.update_plots())
        self.t_scale.config(command=lambda val: self.update_plots())

        # Draw initial plots
        self.update_plots()

    def compute_prob_density(self, s1_x, s2_x, s3_x, v, t):
        """Calculate the probability density based on current parameters."""

        # slits_midpoint = (s1_x + s2_x + 0.00006) / 2
        # s1_slope = 5 / (s1_x - slits_midpoint)
        # s2_slope = 5 / (slits_midpoint - s2_x)
        # print(s1_slope, s2_slope)
        s1_y = 0.0 + v*t
        s2_y = 0.0 + v*t
        s3_y = 0.0 + v*t
        r1 = np.sqrt((self.X - s1_x)**2 + (self.Y - s1_y)**2)
        r2 = np.sqrt((self.X - s2_x)**2 + (self.Y - s2_y)**2)
        r3 = np.sqrt((self.X - s3_x)**2 + (self.Y - s3_y)**2)

        psi_1 = psi(r1, t, a, hbar, m)
        psi_2 = psi(r2, t, a, hbar, m)
        psi_3 = psi(r3, t, a, hbar, m)

        psi_total = (psi_1 + psi_2 + psi_3) / np.sqrt(3)
        return np.abs(psi_total)**2

    def update_plots(self):
        """Update the heatmap and line plot based on slider values."""
        # Retrieve current slider values
        s1_x = float(self.s1_scale.get())
        s2_x = float(self.s2_scale.get())
        s3_x = float(self.s3_scale.get())
        v = float(self.v_scale.get())
        t = float(self.t_scale.get())

        # Compute the probability density
        prob_density = self.compute_prob_density(s1_x, s2_x, s3_x, v, t)

        # Update the heatmap
        self.ax2.clear()
        im = self.ax2.imshow(
            prob_density,
            origin='lower',
            extent=(self.x_min, self.x_max, self.y_min, self.y_max),
            cmap='gray',
            aspect='equal'
        )
        self.ax2.set_xlabel('x')
        self.ax2.set_ylabel('y')
        im.set_clim(0, 0.3)  # Set color limits

        # Update the colorbar
        self.fig.colorbar(im, cax=self.cbar_ax)
        self.cbar_ax.set_label('Probability Density')

        # Update the line plot (slice at y = 2.5, index 249)
        self.ax1.clear()
        self.ax1.plot(self.x, prob_density[0], 'b-')
        self.ax1.set_title(f'Double-Slit Probability Distribution at t={t:.2f}')
        self.ax1.set_xlabel('x')
        self.ax1.set_ylabel('Probability Density')
        self.ax1.set_ylim(0, 1)  # Fixed y-axis range for consistency

        # Refresh the canvas
        self.canvas.draw()

app = DoubleSlitApp()
app.mainloop()