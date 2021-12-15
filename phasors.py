import matplotlib.pyplot as plt 
import numpy as np 
from numpy import linspace, cos, sin, pi
from numpy.lib.arraysetops import isin 
from typing import List
from utils import *


class phasor(object):
    def __init__(self,mag : float =1,phase : float =0,z : complex = None,):
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
            
                
        self._mag = abs(mag)
        self.phase = phase 
        self.angle = round(phase*180/pi,3)
        if z:
            self.cartesian = z
        else:
            self.cartesian = self.get_cartesian()
        self.real = self.cartesian.real
        self.imag = self.cartesian.imag



    def __str__(self):
         return str(round(self._mag,2)) + '∠' + str(round(self.angle)) + "°"
    def __repr__(self):
         return str(round(self._mag,2)) + '∠' + str(round(self.angle)) + "°"

    def __add__(self,other):
        if isinstance(other,(int,float,complex)):
            z = self.cartesian + other
            return cart2pol(z)
        elif isinstance(other,phasor):
            z = self.cartesian + other.cartesian
            return cart2pol(z)
    
    def __radd__(self,other):
        return self + other

    def __sub__(self,other):
        if isinstance(other,(int,float,complex)):
            z = self.cartesian - other
            return cart2pol(z)
        elif isinstance(other,phasor):
            z = self.cartesian - other.cartesian
            return cart2pol(z)
    def __rsub__(self,other):
        return -self + other

    def __neg__(self):
        return phasor(self._mag,self.phase+pi)

    def __mul__(self,other):
        if isinstance(other, (int, float)) and not isinstance(other, bool):
            if other >= 0:
                return phasor(other*self._mag,self.phase)
            else:
                return phasor(abs(other)*self._mag,self.phase+pi)
        elif isinstance(other, phasor):
            return phasor(self._mag*other._mag,self.phase+other.phase)
        elif isinstance(other,complex):
            z = self.cartesian * other
            return cart2pol(z)

        
    def __rmul__(self,other):
        return self*other    

    def __truediv__(self,other):
        if isinstance(other,(int,float)):
            if other <0:
                return(self/phasor(abs(other),pi))
            return phasor(self._mag/other,self.phase)
        elif isinstance(other,complex):
            div = cart2pol(other)
            return phasor(self._mag/div._mag,self.phase-div.phase)
        elif isinstance(other,phasor):
            return phasor(self._mag/other._mag,self.phase-other.phase)

    def __rtruediv__(self,other):
        if isinstance(other,(int,float)):
            return phasor(other/self._mag,-self.phase)
        elif isinstance(other,complex):
            div = cart2pol(other)
            return phasor(div._mag/self._mag,div.phase-self.phase)
        elif isinstance(other,phasor):
            return phasor(other._mag/self._mag,other.phase-self.phase)


    def __abs__(self):
        return self._mag
    
    def __eq__(self,other):
        if (self._mag == other.mag) and (self.phase == other.phase):
            return True
        else:
            return False

    def __pow__(self,other):
        if(other,isinstance(other,int)):
            return phasor(self._mag**other,self.phase*other)


    def get_cartesian(self):
        m = self._mag
        p = self.phase
        return m*(cos(p) + 1j*sin(p))
    
    def conjugate(self):
        return phasor(self._mag,-self.phase)

    def rotate(self,angle):
        """[Rotates a phasor by an angle]

        Args:
            angle ([numeric]): [Angle in radians]

        Returns:
            [Phasor]: [A rotated Phasor]
        """        
        return phasor(self._mag,self.phase+angle)

    def scale(self,scalar):
        return phasor(scalar*self._mag,self.phase)

    @property
    def mag(self):
        return self._mag

class versor(phasor):
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
    mag = sqrt(x**2 + y**2)
    phi = arctan2(y, x)
    return phasor(mag,phi)