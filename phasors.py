import matplotlib.pyplot as plt 
import numpy as np 
from numpy import linspace, cos, sin, pi 


def cart2pol(z):
    """[Forms a Phasor from a complex number]

    Args:
        z ([type]): [description]

    Returns:
        [type]: [description]
    """    
    x = z.real
    y = z.imag
    mag = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return Phasor(mag,phi)

def pol2cart(mag, phi):
    x = mag * np.cos(phi)
    y = mag * np.sin(phi)
    return(x + 1j*y)     

def deg2rad(angle):
    return angle*pi/180

def rad2deg(angle):
    return angle * 180/pi



class Phasor:
    def __init__(self,mag,phase):
        """[Forms a Phasor]

        Args:
            mag ([numeric]): [The magnitude of the phasor]
            phase ([numeric]): [The angle of the phasor in radians]
        """ 
               
        self.mag = abs(mag)
        if phase > 2*pi:
            phase -= 2*pi
        elif phase < 0:
            phase += 2*pi
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
        if isinstance(other, (int, float)) and not isinstance(other, bool):
            if other >= 0:
                return Phasor(other*self.mag,self.phase)
            else:
                return Phasor(abs(other)*self.mag,self.phase+pi)
        elif isinstance(other, Phasor):
            return Phasor(self.mag*other.mag,self.phase+other.phase)
        elif isinstance(other,complex):
            z = self.cartesian * other
            return cart2pol(z)

        
    def __rmul__(self,other):
        return self*other
    
    def __abs__(self):
        return self.mag
    
    def __eq__(self,other):
        if (self.mag == other.mag) and (self.phase == other.phase):
            return True
        else:
            return False

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
            if other <0:
                return(self/Phasor(abs(other),pi))
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

    
    def __neg__(self):
        return Phasor(self.mag,self.phase+pi)
    def get_cartesian(self):
        m = self.mag
        p = self.phase
        return m*(cos(p) + 1j*sin(p))
    
    def conjugate(self):
        return Phasor(self.mag,-self.phase)

    def rotate(self,angle):
        return Phasor(self.mag,self.phase+angle)

    def scale(self,scalar):
        return Phasor(scalar*self.mag,self.phase)

class Versor(Phasor):
        def __init__(self,phase):
            mag = 1
            self.mag = mag
            self.phase = phase 
            self.angle = round(phase*180/pi,3)
            self.cartesian = self.get_cartesian()
            self.real = self.cartesian.real
            self.imag = self.cartesian.imag


def init_axis():
        fig, ax = plt.subplots(figsize=(10,8))
        # Set bottom and left spines as x and y axes of coordinate system
        ax.spines['bottom'].set_position('zero')
        ax.spines['left'].set_position('zero')
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        arrow_fmt = dict(markersize=4, color='black', clip_on=False)
        ax.plot((1), (0), marker='>', transform=ax.get_yaxis_transform(), **arrow_fmt)
        ax.plot((0), (1), marker='^', transform=ax.get_xaxis_transform(), **arrow_fmt)
        ax.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)
        # Create 'x' and 'y' labels placed at the end of the axes
        ax.set_xlabel(r'$\Re(z)$', size=14, labelpad=-24, x=1.03)
        ax.set_ylabel('$\Im(z)$', size=14, labelpad=-21, y=1.02, rotation=0)

        return (fig, ax)


def plot_phasors(phasors):
    """[Plots a list of phasors or complex numbers in the complex cartesian plane]

    Args:
        phasors ([list]): [A list or numpy array of Phasors / complex numbers or both]

    Returns:
        [Figure, Axis]: [Returns a Figure and Axis Objects]
    """    
    fig, ax = init_axis()
    cnt = 1
    for phasor in phasors:
        if isinstance(phasor,complex):
            phasor = cart2pol(phasor)
        x = linspace(0,phasor.mag*cos(phasor.phase),2)
        y = linspace(0,phasor.mag*sin(phasor.phase),2)
        line = plt.plot(x,y,lw=2,alpha=0,label=str(phasor))
        col = plt.gca().lines[-1].get_color()
        plt.annotate('', xy=(0, 0),xycoords='data',xytext=(x[1],y[1]),textcoords='data',arrowprops=dict(arrowstyle='<|-',color=col,mutation_scale=25,lw=2)) 
        if round(y[1]) == 0:
            offset = 0.3
        else:
            offset = 0
        plt.text(x[1],y[1]+offset,str(phasor))
        plt.plot(-x,-y,alpha=0)
        cnt +=1
    plt.show()
    return (fig,ax)


v = Phasor(4,pi/6)
i = Phasor(2,pi/3)
p = v * i.conjugate()
z = 1 +2j
print(type(z))