import matplotlib.pyplot as plt 
import numpy as np 
from numpy import linspace, cos, sin, pi 


def cart2pol(z):
    x = z.real
    y = z.imag
    mag = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return Phasor(mag,phi)

def pol2cart(mag, phi):
    x = mag * np.cos(phi)
    y = mag * np.sin(phi)
    return(x + 1j*y)     

class Phasor:
    def __init__(self,mag,phase):
        self.mag = mag
        self.phase = phase 
        self.angle = round(phase*180/pi,3)
        self.cartesian = self.get_cartesian()
        self.real = self.cartesian.real
        self.imag = self.cartesian.imag
    
    # Overloading + - * / ** operators 
    def __str__(self):
         return str(round(self.mag)) + '∠' + str(round(self.angle)) + "°"
    def __repr__(self):
         return str(round(self.mag)) + '∠' + str(round(self.angle)) + "°"
    def __mul__(self,other):
        if isinstance(other, (int, float)) and not isinstance(x, bool):
            return Phasor(other*self.mag,self.phase)
        elif isinstance(other, Phasor):
            return Phasor(self.mag*other.mag,self.phase+other.phase)
        elif isinstance(other,complex):
            z = self.cartesian * other
            return cart2pol(z)

        
    def __rmul__(self,other):
        if isinstance(other, (int, float)) and not isinstance(x, bool):
            return Phasor(other*self.mag,self.phase)
        elif isinstance(other, Phasor):
            return Phasor(self.mag*other.mag,self.phase+other.phase)
        elif isinstance(other,complex):
            z = self.cartesian * other
            return cart2pol(z)
    
    def __add__(self,other):
        if isinstance(other,(int,float,complex)):
            z = self.cartesian + other
            return cart2pol(z)
        elif isinstance(other,Phasor):
            z = self.cartesian + other.cartesian
            return cart2pol(z)

    def __pow__(self,other):
        if(other,isinstance(other,int)):
            return Phasor(self.mag**other,self.phase*other)

    def __truediv__(self,other):
        if isinstance(other,(int,float)):
            return Phasor(self.mag/other,self.phase)
        elif isinstance(other,complex):
            div = cart2pol(other)
            return Phasor(self.mag/div.mag,self.phase-div.phase)
        elif isinstance(other,Phasor):
            return Phasor(self.mag/other.mag,self.phase-other.phase)
    def __rtruediv__(self,other):
        if isinstance(other,(int,float)):
            return Phasor(other/self.mag,-self.phase)
        elif isinstance(other,complex):
            div = cart2pol(other)
            return Phasor(div.mag/self.mag,div.phase-self.phase)
        elif isinstance(other,Phasor):
            return Phasor(other.mag/self.mag,other.phase-self.phase)

    def __sub__(self,other):
        if isinstance(other,(int,float,complex)):
            z = self.cartesian - other
            return cart2pol(z)
        elif isinstance(other,Phasor):
            z = self.cartesian - other.cartesian
            return cart2pol(z)

    def pol2cart(rho, phi):
        x = rho * np.cos(phi)
        y = rho * np.sin(phi)
        return(x + 1j*y)     


    def get_cartesian(self):
        m = self.mag
        p = self.phase
        return m*(cos(p) + 1j*sin(p))
    
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

class Versor(Phasor):
        def __init__(self,phase):
            mag = 1
            self.mag = mag
            self.phase = phase 
            self.angle = round(phase*180/pi,3)
            self.cartesian = self.get_cartesian()
            self.real = self.cartesian.real
            self.imag = self.cartesian.imag


v = Phasor(10,pi/3)
a = Versor(2*pi/3)
v2 = v *a
v.init_axis()
v.plot()
v2.plot()
v3 = v2 * a

v3.plot()
plt.show()
print(type(v3))