import matplotlib.pyplot as plt 
import numpy as np 
from numpy import linspace, cos, sin, pi
from numpy.lib.arraysetops import isin 
from typing import List

def cart2pol(z : complex):
    """[Forms a Phasor from a complex number]

    Args:
        z ([complex]): [a complex number i,e 2+4j]

    Returns:
        [Phasor]: [A phasor i.e 1∠30°]
    """    
    if isinstance(z,(int,float)):
        z = complex(z)
    x = z.real
    y = z.imag
    mag = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return Phasor(mag,phi)

def pol2cart(mag : float, phi : float) -> complex:
    x = mag * np.cos(phi)
    y = mag * np.sin(phi)
    return(x + 1j*y)     

def deg2rad(angle : float) ->float:
    return angle*pi/180

def rad2deg(angle : float) -> float:
    return angle * 180/pi







def sym_com(l1,l2,l3):
    """[Calculates the symmetrical components of a power system, the line currents, voltages or impedences can be passed as phasors, or complex numbers ]

    Args:
        l1 ([Phasor, complex]): [Line 1]
        l2 ([Phasor, complex]): [Line 2]
        l3 ([Phasor, complex]): [Line 3]

    Returns:
        [ndarray]: [The symmetrical components as Phasors inside a np array]
    """    
    cnt = 0 

    a = Versor(deg2rad(120))
    a2 = a**2
    s =  np.array([[1,1,1],[1,a,a2],[1,a2,a]])
    L =  np.array([l1,l2,l3])
            
    Ls = 1/3 * np.matmul(s,L)
    for i in range(3):
        if isinstance(Ls[i],complex):
            Ls[i] = cart2pol(Ls[i])

    return Ls


class Phasor:
    def __init__(self,mag : float =1,phase : float =0,z : complex = None):
        """[Forms a Phasor with magnitude and angle or using a complex number z.]

        Args:
            mag ([numeric]): [The magnitude of the phasor]
            phase ([numeric]): [The angle of the phasor in radians]
        """ 
        if z:
            if(isinstance(z,(int,float))):
                z = complex(z)
            if(isinstance(z,complex)):
                x = z.real
                y = z.imag
                mag = np.sqrt(x**2 + y**2)
                phase = np.arctan2(y, x)
        else:
            if round(abs(mag),10) ==0:
                mag = 0
                phase = 0

            
            if phase > 2*pi:
                phase -= 2*pi
            elif phase < 0:
                phase += 2*pi
                
        self.mag = abs(mag)
        self.phase = phase 
        self.angle = round(phase*180/pi,3)
        if z:
            self.cartesian = z
        else:
            self.cartesian = self.get_cartesian()
        self.real = self.cartesian.real
        self.imag = self.cartesian.imag



    def __str__(self):
         return str(round(self.mag,2)) + '∠' + str(round(self.angle)) + "°"
    def __repr__(self):
         return str(round(self.mag,2)) + '∠' + str(round(self.angle)) + "°"

    def __add__(self,other):
        if isinstance(other,(int,float,complex)):
            z = self.cartesian + other
            return cart2pol(z)
        elif isinstance(other,Phasor):
            z = self.cartesian + other.cartesian
            return cart2pol(z)
    def __radd__(self,other):
        return self + other

    def __sub__(self,other):
        if isinstance(other,(int,float,complex)):
            z = self.cartesian - other
            return cart2pol(z)
        elif isinstance(other,Phasor):
            z = self.cartesian - other.cartesian
            return cart2pol(z)

    def __neg__(self):
        return Phasor(self.mag,self.phase+pi)

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


    def __abs__(self):
        return self.mag
    
    def __eq__(self,other):
        if (self.mag == other.mag) and (self.phase == other.phase):
            return True
        else:
            return False

    def __pow__(self,other):
        if(other,isinstance(other,int)):
            return Phasor(self.mag**other,self.phase*other)


    def get_cartesian(self):
        m = self.mag
        p = self.phase
        return m*(cos(p) + 1j*sin(p))
    
    def conjugate(self):
        return Phasor(self.mag,-self.phase)

    def rotate(self,angle):
        """[Rotates a phasor by an angle]

        Args:
            angle ([numeric]): [Angle in radians]

        Returns:
            [Phasor]: [A rotated Phasor]
        """        
        return Phasor(self.mag,self.phase+angle)

    def scale(self,scalar):
        return Phasor(scalar*self.mag,self.phase)

class Versor(Phasor):
        def __init__(self,phase : float = 0):
            """[Forms a units phasor with an angle 'phase' in radians]

            Args:
                phase ([numeric]): [angle in radians]
            """            
            self.mag = 1
            self.phase = phase 
            self.angle = round(phase*180/pi,3)
            self.cartesian = self.get_cartesian()
            self.real = self.cartesian.real
            self.imag = self.cartesian.imag


def set_axis(ax):
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
    ax.set_xlabel(r'$\Re(z)$', size=14, labelpad=-24, x=1.05)
    ax.set_ylabel('$\Im(z)$', size=14, labelpad=-21, y=1.02, rotation=0)
    return ax 


def init_axis():
        fig, ax = plt.subplots(figsize=(10,8))
        # Set bottom and left spines as x and y axes of coordinate system
        ax = set_axis(ax)

        return (fig, ax)






def plot_phasors(phasors):
    """[Plots a list of phasors or complex numbers in the complex cartesian plane]

    Args:
        phasors ([list]): [A list or numpy array of Phasors / complex numbers or both]

    Returns:
        [Figure, Axis]: [Returns a Figure and Axis Objects]
    """    
    fig, ax = init_axis()
    for phasor in phasors:
        if isinstance(phasor,(complex,int,float)):
            phasor = cart2pol(phasor)
        plot_vector(phasor)
    plt.show()
    return (fig,ax)

def plot_vector(vector,Line=None):
    x = linspace(0,vector.mag*cos(vector.phase),2)
    y = linspace(0,vector.mag*sin(vector.phase),2)
    plt.plot(x,y,lw=2,alpha=0,label=str(vector))
    col = plt.gca().lines[-1].get_color()
    plt.plot(x,y,lw=2,alpha=0,label=str(vector))
    col = plt.gca().lines[-1].get_color()
    plt.annotate('', xy=(0, 0),xycoords='data',xytext=(x[1],y[1]),textcoords='data',arrowprops=dict(arrowstyle='<|-',color=col,mutation_scale=25,lw=2)) 
    if round(y[1]) == 0:
        offset = 0.3
    else:
        offset = 0
    if Line:
        lab = str(vector) + ", L" + str(Line)
    else:
        lab = str(vector)
    plt.text(x[1],y[1]+offset,lab)
    plt.plot(-x,-y,alpha=0,color=col)

def plot_sc(sym_com):
    fig, axes = plt.subplots(nrows=1,ncols=3,sharey=True,sharex=True,figsize=(12,6))
    fig.suptitle("Symmetrische Komponenten")
    a = Versor(pi*2/3)
    for i in range(0,3):
        axes[i] = set_axis(axes[i])
    for i in range(0,3):
        plt.sca(axes[i])
        if i == 0:
            plot_vector(sym_com[i],Line="1,2,3")
        elif i==1:
            plot_vector(sym_com[i],1)
            plot_vector(sym_com[i]*(a**2),2)
            plot_vector(sym_com[i]*a,3)
        else:
            plot_vector(sym_com[i],1)
            plot_vector(sym_com[i]*a,2)
            plot_vector(sym_com[i]*(a**2),3)