import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors

class GradientVisualizer:
    def __init__(self):
        plt.rcParams['figure.figsize'] = [15, 7]
        plt.rcParams['figure.dpi'] = 100
        self.fig = plt.figure()
        
        gs = self.fig.add_gridspec(1, 2, width_ratios=[1, 1])
        self.ax1 = self.fig.add_subplot(gs[0], projection='3d')
        self.ax2 = self.fig.add_subplot(gs[1])
        
        x = np.linspace(-4, 4, 100)
        y = np.linspace(-4, 4, 100)
        self.X, self.Y = np.meshgrid(x, y)
        
        self.Z = self.X**2 + self.Y**2 * np.sin(self.X)
        
        self.dx = 2*self.X + self.Y**2 * np.cos(self.X)
        self.dy = 2*self.Y * np.sin(self.X)
        
        self.current_point = np.array([-2.0, -2.0])
        self.points_history = [self.current_point.copy()]
        
        self.surface_cmap = plt.cm.viridis
        self.vector_cmap = plt.cm.autumn
        
        self.xlim = (-4, 4)
        self.ylim = (-4, 4)
        self.zlim = (np.min(self.Z), np.max(self.Z))
        
    def plot_surface(self):
        surf = self.ax1.plot_surface(self.X, self.Y, self.Z, 
                                   cmap=self.surface_cmap,
                                   alpha=0.8,
                                   linewidth=0,
                                   antialiased=True)
        
        self.ax1.set_xlim(self.xlim)
        self.ax1.set_ylim(self.ylim)
        self.ax1.set_zlim(self.zlim)
        
        if not hasattr(self, 'colorbar'):
            self.colorbar = self.fig.colorbar(surf, ax=self.ax1, shrink=0.5, aspect=5)
        
        self.ax1.set_xlabel('X')
        self.ax1.set_ylabel('Y')
        self.ax1.set_zlabel('Z')
        self.ax1.set_title('3D Surface with Gradient Path')
        
    def plot_contour(self):
        contours = self.ax2.contour(self.X, self.Y, self.Z, 20, 
                                  cmap=self.surface_cmap)
        self.ax2.clabel(contours, inline=True, fontsize=8)
        
        skip = 8
        self.ax2.quiver(self.X[::skip, ::skip], 
                       self.Y[::skip, ::skip],
                       self.dx[::skip, ::skip], 
                       self.dy[::skip, ::skip],
                       color='red', alpha=0.3)
        
        self.ax2.set_xlim(self.xlim)
        self.ax2.set_ylim(self.ylim)
        
        self.ax2.set_xlabel('X')
        self.ax2.set_ylabel('Y')
        self.ax2.set_title('Contour Plot with Gradient Field')
        
    def update(self, frame):
        self.ax1.cla()
        self.ax2.cla()
        
        self.plot_surface()
        self.plot_contour()
        
        gradient = np.array([
            float(self.dx[int(self.current_point[1]*12.5 + 50), 
                         int(self.current_point[0]*12.5 + 50)]),
            float(self.dy[int(self.current_point[1]*12.5 + 50), 
                         int(self.current_point[0]*12.5 + 50)])
        ])
        
        learning_rate = 0.1
        self.current_point -= learning_rate * gradient
        self.points_history.append(self.current_point.copy())
        
        points = np.array(self.points_history)
        z_points = points[:,0]**2 + points[:,1]**2 * np.sin(points[:,0])
        self.ax1.plot(points[:,0], points[:,1], z_points, 
                     'r-', linewidth=2, label='Gradient Path')
        
        z_current = (self.current_point[0]**2 + 
                    self.current_point[1]**2 * 
                    np.sin(self.current_point[0]))
        self.ax1.scatter([self.current_point[0]], 
                        [self.current_point[1]], 
                        [z_current],
                        color='red', s=100)
        
        self.ax2.plot(points[:,0], points[:,1], 
                     'r.-', linewidth=2, label='Gradient Path')
        
        self.ax1.legend()
        self.ax2.legend()
        
        self.ax1.view_init(elev=30, azim=45)
        
        return self.ax1, self.ax2

    def animate(self):
        self.fig.set_size_inches(15, 7, forward=True)
        
        anim = FuncAnimation(self.fig, self.update, 
                           frames=50, interval=100, blit=False)
        
        plt.tight_layout()
        plt.show()

visualizer = GradientVisualizer()
visualizer.animate()