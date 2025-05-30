from manim import *
import numpy as np

class DoubleSlitAnimation(Scene):
    def construct(self):
        # Create wall with two slits
        wall_part1 = Line((0, -4, 0), (0, -1, 0), color=WHITE)
        wall_part2 = Line((0, -0.5, 0), (0, 0.5, 0), color=WHITE)
        wall_part3 = Line((0, 1, 0), (0, 4, 0), color=WHITE)
        self.add(wall_part1, wall_part2, wall_part3)

        # Wave packet parameters
        sigma_x = 0.5  # Spread in x-direction
        sigma_y = 0.5  # Spread in y-direction
        v = 1.0        # Velocity along x-axis
        x0 = -3.0      # Initial x-position
        y1 = -0.75     # Center of slit 1 (between y=-1 and y=-0.5)
        y2 = 0.75      # Center of slit 2 (between y=0.5 and y=1)
        k = 10         # Wave number for interference pattern

        # Grid for probability density
        nx = 100
        ny = 60
        x_vals = np.linspace(-5, 5, nx)
        y_vals = np.linspace(3, -3, ny)  # Top to bottom
        X, Y = np.meshgrid(x_vals, y_vals)
        wavelength = 0.5  # Wavelength of the waves

        # Function to compute probability density
        def get_prob_array(t):
            array = np.zeros((ny, nx, 4), dtype=np.uint8)
            if t <= 3:
                # Before hitting the wall: Gaussian wave packet
                x_center = x0 + v * t
                prob = (1 / (2 * np.pi * sigma_x * sigma_y)) * np.exp(
                    - (X - x_center)**2 / (2 * sigma_x**2) - Y**2 / (2 * sigma_y**2)
                )
            
                # Normalize probability for consistent visualization
                prob_normalized = prob / np.max(prob) if np.max(prob) > 0 else prob
                # Create RGBA array: white with alpha based on probability
                array[:, :, 0] = 255  # Red channel
                array[:, :, 1] = 255  # Green channel
                array[:, :, 2] = 255  # Blue channel
                array[:, :, 3] = (255 * prob_normalized).astype(np.uint8)  # Alpha channel  
            return array

        # Semi-circular wavefronts after the slits
        def create_circular_wavefronts(t):
            wavefronts = VGroup()
            if t <= 3:
                return wavefronts  
            
            t_adjusted = t - 3  # Time since wave reaches the slits
            max_radius = v * t_adjusted  # Maximum radius at this time
            num_waves = int(max_radius / wavelength) + 1
            for i in range(num_waves):
                radius = v * t_adjusted - i * wavelength
                if radius > 0 and radius <= 5:  
                    # Arc from slit 1
                    arc1 = Arc(radius=radius, start_angle=-PI/2, angle=PI, color=WHITE, stroke_width=2)
                    arc1.shift(UP * y1)  
                    # Arc from slit 2
                    arc2 = Arc(radius=radius, start_angle=-PI/2, angle=PI, color=WHITE, stroke_width=2)
                    arc2.shift(UP * y2)  
                    wavefronts.add(arc1, arc2)
            return wavefronts
        
        # Animate the wave packet
        t_tracker = ValueTracker(0)
        wave = always_redraw(lambda: ImageMobject(get_prob_array(t_tracker.get_value())).set_height(6))
        circular_waves = always_redraw(lambda: create_circular_wavefronts(t_tracker.get_value()))

        
        self.add(wave, circular_waves)

        # Extend animation to show interference pattern
        self.play(t_tracker.animate.set_value(6), run_time=6, rate_func=linear)
        self.wait(1)

        