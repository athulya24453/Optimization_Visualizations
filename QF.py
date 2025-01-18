import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_QF(A):
    x_range = (-10, 10)
    y_range = (-10, 10)
    resolution = 100

    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)

    Z = A[0, 0] * X**2 + (A[0, 1] + A[1, 0]) * X * Y + A[1, 1] * Y**2

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    surface = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.9)

    ax.set_title("3D Surface Plot of Quadratic Form Q(x)")
    ax.set_xlabel("x-axis")
    ax.set_ylabel("y-axis")
    ax.set_zlabel("Q(x, y)")
    fig.colorbar(surface, shrink=0.5, aspect=10)

    plt.show()

def on_plot():
    try:
        a11 = float(entry_a11.get())
        a12 = float(entry_a12.get())
        a21 = float(entry_a21.get())
        a22 = float(entry_a22.get())

        A = np.array([[a11, a12], [a21, a22]])
        plot_QF(A)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for the matrix elements.")

def on_reset():
    entry_a11.delete(0, tk.END)
    entry_a12.delete(0, tk.END)
    entry_a21.delete(0, tk.END)
    entry_a22.delete(0, tk.END)

root = tk.Tk()
root.title("Quadratic Form Plotter")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="Matrix A:", font=("Arial", 16)).grid(row=0, column=0, columnspan=5, pady=20)

tk.Label(root, text="[", font=("Arial", 18)).grid(row=1, column=0, rowspan=2, sticky="nsew", padx=5)
tk.Label(root, text="]", font=("Arial", 18)).grid(row=1, column=3, rowspan=2, sticky="nsew", padx=5)

entry_a11 = tk.Entry(root, width=8, font=("Arial", 14))
entry_a11.grid(row=1, column=1, padx=10, pady=5)

entry_a12 = tk.Entry(root, width=8, font=("Arial", 14))
entry_a12.grid(row=1, column=2, padx=10, pady=5)

entry_a21 = tk.Entry(root, width=8, font=("Arial", 14))
entry_a21.grid(row=2, column=1, padx=10, pady=5)

entry_a22 = tk.Entry(root, width=8, font=("Arial", 14))
entry_a22.grid(row=2, column=2, padx=10, pady=5)

btn_plot = tk.Button(root, text="Plot", command=on_plot, font=("Arial", 14), bg="lightblue", width=8)
btn_plot.grid(row=3, column=1, pady=20)

btn_reset = tk.Button(root, text="Reset", command=on_reset, font=("Arial", 14), bg="lightcoral", width=8)
btn_reset.grid(row=3, column=2, pady=20)

root.mainloop()
