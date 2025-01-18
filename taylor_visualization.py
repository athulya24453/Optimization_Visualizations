import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from scipy.special import factorial

class TaylorSeriesVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Taylor Series Visualizer")
        
        self.order = tk.IntVar(value=1)
        self.x0 = tk.DoubleVar(value=0)
        self.delta_x = tk.DoubleVar(value=1)
        
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.formula_var = tk.StringVar()
        formula_label = ttk.Label(main_frame, textvariable=self.formula_var, 
                                font=('Courier', 12), wraplength=600)
        formula_label.grid(row=0, column=0, columnspan=4, pady=10)
        
        ttk.Label(main_frame, text="Center point (x₀):").grid(row=1, column=0)
        ttk.Entry(main_frame, textvariable=self.x0, width=10).grid(row=1, column=1)
        
        ttk.Label(main_frame, text="Δx:").grid(row=1, column=2)
        ttk.Entry(main_frame, textvariable=self.delta_x, width=10).grid(row=1, column=3)
        
        ttk.Button(main_frame, text="Decrease Order", 
                  command=self.decrease_order).grid(row=2, column=0)
        ttk.Label(main_frame, textvariable=self.order).grid(row=2, column=1)
        ttk.Button(main_frame, text="Increase Order", 
                  command=self.increase_order).grid(row=2, column=2)
        
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=4, pady=10)
        
        self.value_var = tk.StringVar()
        value_label = ttk.Label(main_frame, textvariable=self.value_var, 
                              font=('Courier', 10))
        value_label.grid(row=4, column=0, columnspan=4)
        
        self.x0.trace_add('write', self.update_plot)
        self.delta_x.trace_add('write', self.update_plot)
        self.order.trace_add('write', self.update_plot)
        
        self.update_plot()
    
    def f(self, x):
        return np.exp(x)
    
    def derivative(self, x, n):
        return np.exp(x)
    
    def taylor_series(self, x, x0, order):
        result = 0
        for n in range(order + 1):
            derivative = self.derivative(x0, n)
            result += derivative * (x - x0)**n / factorial(n)
        return result
    
    def update_formula(self):
        terms = []
        x0 = self.x0.get()
        for n in range(self.order.get() + 1):
            derivative = self.derivative(x0, n)
            
            if abs(derivative) > 1e-10:
                term = f"{derivative:.3f}"
                if n > 0:
                    term += f"(x-{x0:.2f})^{n}"
                if n < self.order.get():
                    term += " + "
                terms.append(term)
        
        self.formula_var.set("T(x) = " + "".join(terms))
    
    def update_plot(self, *args):
        try:
            self.ax.clear()
            
            x0 = self.x0.get()
            dx = self.delta_x.get()
            order = self.order.get()
            
            x = np.linspace(x0 - abs(dx), x0 + abs(dx), 200)
            
            self.ax.plot(x, self.f(x), 'b-', label='f(x) = exp(x)')
            
            y_taylor = self.taylor_series(x, x0, order)
            self.ax.plot(x, y_taylor, 'r--', 
                        label=f'Taylor series (order {order})')
            
            self.ax.plot([x0], [self.f(x0)], 'ko', label='Center point')
            
            eval_x = x0 + dx
            eval_y = self.taylor_series(eval_x, x0, order)
            self.ax.plot([eval_x], [eval_y], 'go', label='Evaluation point')
            
            actual_value = self.f(eval_x)
            self.value_var.set(
                f"At x = {eval_x:.2f}:\n"
                f"Actual value: {actual_value:.6f}\n"
                f"Approximation: {eval_y:.6f}\n"
                f"Error: {abs(actual_value - eval_y):.6f}"
            )
            
            self.update_formula()
            
            self.ax.grid(True)
            self.ax.legend()
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.ax.set_title('Taylor Series Approximation of exp(x)')
            
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error updating plot: {e}")
    
    def increase_order(self):
        self.order.set(self.order.get() + 1)
    
    def decrease_order(self):
        if self.order.get() > 0:
            self.order.set(self.order.get() - 1)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaylorSeriesVisualizer(root)
    root.mainloop()