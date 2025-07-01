# Double‑Slit Experiment Visualization

A real‑time, interactive Flask app that simulates the quantum double‑(or multi‑) slit experiment. Adjust the number of slits, slit spacing, particle velocity, and time via sliders, and instantly see both:

- A heatmap of the probability density ⟮𝑥,𝑦⟯  
- A 1D line plot of the average probability density across 𝑦  

---

## ▶️ Live Demo

https://github.com/user-attachments/assets/e0be3a0e-9d17-4b1f-82d4-9953be12c06e


---

## Features

- **Multi‑slit support**: 1–5 slits  
- **Parameter sliders**:  
  - Number of slits (`n`)  
  - Distance between slits (`d`)  
  - Particle velocity (`v`)  
  - Time evolution (`t`)  
- **Real‑time updates** via client‑side debounced requests  
- **Combined plots**:  
  - Heatmap with colorbar  
  - Line plot of ⟮𝑥⟯‑averaged probability  

---

## Installation

1. Clone this repository  
   ```bash
   git clone https://github.com/desert-dweller/double-slit-experiment-visualization.git
   cd double-slit-experiment-visualization
   ```

2. (Optional) Create and activate a virtual environment
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```
   > Note: Requires Flask, NumPy, and Matplotlib.

---

## Usage

1. Run the app:
   ```
   python app.py
   ```
2. Open your browser at http://127.0.0.1:5000/
3. Move the sliders to explore how your choices affect the interference pattern in real time.
