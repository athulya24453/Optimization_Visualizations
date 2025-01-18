import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class PNormVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("P-Norm Unit Sphere Visualization")
        
        self.p = 2.0
        
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.fig = Figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=8, padx=5, pady=5)
        
        controls_frame = ttk.Frame(self.main_frame)
        controls_frame.grid(row=1, column=0, columnspan=8, pady=5)
        
        self.decrease_button = ttk.Button(controls_frame, text="-", command=self.decrease_p)
        self.decrease_button.grid(row=0, column=0, padx=5)
        
        self.p_label = ttk.Label(controls_frame, text=f"p = {self.p:.1f}")
        self.p_label.grid(row=0, column=1, padx=5)
        
        ttk.Button(controls_frame, text="+", command=self.increase_p).grid(row=0, column=2, padx=5)
        
        ttk.Button(controls_frame, text="p=1", command=lambda: self.set_p(1)).grid(row=0, column=3, padx=5)
        ttk.Button(controls_frame, text="p=2", command=lambda: self.set_p(2)).grid(row=0, column=4, padx=5)
        ttk.Button(controls_frame, text="p=10", command=lambda: self.set_p(10)).grid(row=0, column=5, padx=5)
        
        ttk.Label(controls_frame, text="Enter p:").grid(row=0, column=6, padx=5)
        self.p_entry = ttk.Entry(controls_frame, width=8)
        self.p_entry.grid(row=0, column=7, padx=5)
        self.p_entry.bind('<Return>', self.handle_p_entry)
        
        explanation = ("The unit sphere for a p-norm shows all points (x, y) where:\n"
                      "| x |^p + | y |^p = 1\n\n"
                      "p = 1: Diamond shape (Manhattan distance)\n"
                      "p = 2: Circle (Euclidean distance)\n"
                      "p = ∞: Square (Chebyshev distance)")
        ttk.Label(self.main_frame, text=explanation, justify=tk.LEFT).grid(row=2, column=0, columnspan=8, padx=5, pady=5)
        
        self.update_plot()
        self.update_button_states()
    
    def generate_unit_sphere(self, p):
        t = np.linspace(0, 2*np.pi, 1000)
        
        if p == float('inf'):
            x = np.concatenate([
                np.ones(250), 
                np.linspace(1, -1, 250),
                -np.ones(250),
                np.linspace(-1, 1, 250)
            ])
            y = np.concatenate([
                np.linspace(1, -1, 250),
                -np.ones(250),
                np.linspace(-1, 1, 250),
                np.ones(250)
            ])
        else:
            x = np.sin(t) * np.abs(np.sin(t))**(2/p - 1)
            y = np.cos(t) * np.abs(np.cos(t))**(2/p - 1)
        
        return x, y
    
    def update_plot(self):
        self.ax.clear()
        
        x, y = self.generate_unit_sphere(self.p)
        p_display = "∞" if self.p == float("inf") else f"{self.p:.2f}"
        self.ax.plot(x, y, 'b-', label=f'p = {p_display}')
        
        self.ax.grid(True)
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-1.5, 1.5)
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title(f'Unit Sphere for p = {p_display}')
        self.ax.legend()
        
        self.canvas.draw()
    
    def update_button_states(self):
        if self.p <= 1:
            self.decrease_button['state'] = 'disabled'
        else:
            self.decrease_button['state'] = 'normal'
    
    def update_p_display(self):
        if self.p == float('inf'):
            self.p_label.config(text="p = ∞")
        else:
            self.p_label.config(text=f"p = {self.p:.2f}")
    
    def increase_p(self):
        if self.p < 10:
            self.p += 0.1
        elif self.p < float('inf'):
            self.p = float('inf')
        self.update_p_display()
        self.update_plot()
        self.update_button_states()
    
    def decrease_p(self):
        if self.p == float('inf'):
            self.p = 10
        elif self.p > 1:
            self.p -= 0.1
        self.update_p_display()
        self.update_plot()
        self.update_button_states()
    
    def set_p(self, value):
        self.p = float(value)
        self.update_p_display()
        self.update_plot()
        self.update_button_states()
    
    def handle_p_entry(self, event):
        try:
            value = self.p_entry.get().strip().lower()
            if value == 'inf' or value == '∞':
                new_p = float('inf')
            else:
                new_p = float(value)
            
            if new_p < 1:
                messagebox.showerror("Invalid Input", "p must be greater than or equal to 1")
                return
                
            self.p = new_p
            self.update_p_display()
            self.update_plot()
            self.update_button_states()
            self.p_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number or 'inf'")

def main():
    root = tk.Tk()
    app = PNormVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()