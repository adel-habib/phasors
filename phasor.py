import numpy as np 
from numpy import cos, sin, pi, angle
from numpy.lib.arraysetops import isin 
from typing import List
from utils.utils import * 

class Phasor(object):
    
    instances = []
    instances_num = 0

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
                mag = abs(z)
                phase = angle(z)
        else:
            if round(abs(mag),10) ==0:
                mag = 0
                phase = 0
                
            if phase > 2*pi:
                phase -= 2*pi
            elif phase < 0:
                phase += 2*pi
            
                
        self._mag = abs(mag)
        self._phase = phase 
        self._angle = round(phase*180/pi,3)
        if z:
            self._cartesian = z
        else:
            self._cartesian = self.get_cartesian()
        self._real = self._cartesian.real
        self._imag = self._cartesian.imag

        Phasor.instances.append(self)
        Phasor.instances_num += 1

    def __str__(self):
         return str(round(self._mag,2)) + '∠' + str(round(self._angle)) + "°"
    def __repr__(self):
         return str(round(self._mag,2)) + '∠' + str(round(self._angle)) + "°"

    def __imag__(self):
        return self._imag
    
    def __real__(self):
        return self._real

    def __conjugate__(self):
        return self.conjugate()


    def __or__(self,other):
        """[Returns the reduced value of two parallel loads]

        Args:
            other ([phasor]): [load / impedance by it's phasor representation]

        Returns:
            [phasor]: [equivalent phasor]
        """

        return (self * other / (self + other))
    
    def __ror__(self,other):
        """[Returns the reduced value of two parallel loads]

        Args:
            other ([phasor]): [load / impedance by it's phasor representation]

        Returns:
            [phasor]: [equivalent phasor]
        """

        return self | other   


    def __add__(self,other):
        if isinstance(other,(int,float,complex)):
            z = self._cartesian + other
            mag, phase = cart2pol(z)
            return Phasor(mag,phase)
        elif isinstance(other,Phasor):
            z = self._cartesian + other._cartesian
            mag, phase = cart2pol(z)
            return Phasor(mag,phase)
    
    def __radd__(self,other):
        return self + other

    def __sub__(self,other):
        if isinstance(other,(int,float,complex)):
            z = self._cartesian - other
            mag, phase = cart2pol(z)
            return Phasor(mag,phase)

        elif isinstance(other,Phasor):
            z = self._cartesian - other._cartesian
            mag, phase = cart2pol(z)
            return Phasor(mag,phase)

    def __rsub__(self,other):
        return -self + other

    def __neg__(self):
        """[Rotates a phasor 180°]

        Returns:
            [phasor]: [a phasor pointing to the opposite direction of the original phasor]
        """
        return Phasor(self._mag,self._phase+pi)

    def __mul__(self,other):
        if isinstance(other, (int, float)) and not isinstance(other, bool):
            if other >= 0:
                return Phasor(other*self._mag,self._phase)
            else:
                return Phasor(abs(other)*self._mag,self._phase+pi)
        elif isinstance(other, Phasor):
            return Phasor(self._mag*other._mag,self._phase+other._phase)
        elif isinstance(other,complex):
            z = self._cartesian * other
            return cart2pol(z)

        
    def __rmul__(self,other):
        return self*other    

    def __truediv__(self,other):
        if isinstance(other,(int,float)):
            if other <0:
                return(self/Phasor(abs(other),pi))
            return Phasor(self._mag/other,self._phase)
        elif isinstance(other,complex):
            div = cart2pol(other)
            return Phasor(self._mag/div._mag,self._phase-div._phase)
        elif isinstance(other,Phasor):
            return Phasor(self._mag/other._mag,self._phase-other._phase)

    def __rtruediv__(self,other):
        if isinstance(other,(int,float)):
            return Phasor(other/self._mag,-self._phase)
        elif isinstance(other,complex):
            div = cart2pol(other)
            return Phasor(div._mag/self._mag,div._phase-self._phase)
        elif isinstance(other,Phasor):
            return Phasor(other._mag/self._mag,other._phase-self._phase)


    def __abs__(self):
        return self._mag
    
    def __eq__(self,other):
        if (self._mag == other.mag) and (self._phase == other.phase):
            return True
        else:
            return False

    def __pow__(self,other):
        if(other,isinstance(other,int)):
            return Phasor(self._mag**other,self._phase*other)


    def get_cartesian(self):
        m = self._mag
        p = self._phase
        return m*(cos(p) + 1j*sin(p))
    
    def conjugate(self):
        return Phasor(self._mag,-self._phase)

    def rotate(self,angle):
        """[Rotates a phasor by an angle]

        Args:
            angle ([numeric]): [Angle in radians]

        Returns:
            [Phasor]: [A rotated Phasor]
        """        
        return Phasor(self._mag,self._phase+angle)

    def scale(self,scalar):
        return Phasor(scalar*self._mag,self._phase)

    @property
    def mag(self):
        return self._mag
    @property
    def real(self):
        return self._real
    @property
    def imag(self):
        return self._imag

    @property
    def complex(self):
        return self._cartesian

    @property
    def angle(self):
        return self._angle

    @property
    def phase(self):
        return self._phase
    

class versor(Phasor):
        def __init__(self,phase : float = 0):
            """[Forms a unit phasor with an angle 'phase' in radians]

            Args:
                phase ([numeric]): [angle in radians]
            """            
            self.mag = 1
            self.phase = phase 
            self.angle = round(phase*180/pi,3)
            self.cartesian = self.get_cartesian()
            self.real = self.cartesian.real
            self.imag = self.cartesian.imag




