import matplotlib.pyplot as plt 
import numpy as np 
from numpy import linspace, cos, sin, pi 

class Phasor:
    def __init__(self,mag,phase):
        self.mag = mag
        self.phase = phase 
        self.angle = round(phase*180/pi,3)
        self.cartesian = self.get_cartesian()
        self.real = self.cartesian.real
        self.imag = self.cartesian.imag
        
    def __str__(self):
         return str(self.mag) + '∠' + str(self.angle)
    def __repr__(self):
         return str(self.mag) + '∠' + str(self.angle)
    def __mul__(self,other):
        if isinstance(other, (int, float, complex)) and not isinstance(x, bool):
            return Phasor(other*self.mag,self.phase)
        elif isinstance(other, Phasor):
            return Phasor(self.mag*other.mag,self.phase+other.phase)
        
    def __rmul__(self,other):
        if isinstance(other, (int, float, complex)) and not isinstance(x, bool):
            return Phasor(other*self.mag,self.phase)
        elif isinstance(other, Phasor):
            return Phasor(self.mag*other.mag,self.phase+other.phase)
        
    def get_cartesian(self):
        m = self.mag
        p = self.phase
        return (m*cos(p) + 1j*sin(p))
    
    def get_conjugate(self):
        return Phasor(self.mag,-self.phase)
    def init_axis(self):
        fig, ax = plt.subplots(figsize=(10,8))
        # Set bottom and left spines as x and y axes of coordinate system
        ax.spines['bottom'].set_position('zero')
        ax.spines['left'].set_position('zero')
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)
        # Create 'x' and 'y' labels placed at the end of the axes
        ax.set_xlabel(r'$\Re(z)$', size=14, labelpad=-24, x=1.03)
        ax.set_ylabel('$\Im(z)$', size=14, labelpad=-21, y=1.02, rotation=0)
    
    def plot(self):
        x = linspace(0,self.mag*cos(self.phase),2)
        y = linspace(0,self.mag*sin(self.phase),2)
        line = plt.plot(x,y,lw=2,alpha=0)
        col = plt.gca().lines[-1].get_color()
        plt.annotate('', xy=(0, 0),xycoords='data',xytext=(x[1],y[1]),textcoords='data',arrowprops=dict(arrowstyle='<|-',color=col,mutation_scale=25,lw=2))
        plt.plot(-x,-y,alpha=0)