import numpy as np 
from numpy import cos, sin, pi, angle
from numpy.lib.arraysetops import isin 
from typing import List
from utils.utils import * 
from array import array

class Phasor(object):

    typecode = 'd'
    instances = []
    instances_num = 0

    def __init__(self,mag : float =1,phase : float =0,):
        """[Forms a Phasor with magnitude and angle]

        Args:
            mag ([numeric]): [The magnitude of the phasor]
            phase ([numeric]): [The angle of the phasor in radians]
        """ 
        
        if round(abs(mag),10) ==0:
                mag = 0
                phase = 0
                
        if  phase >= 2*pi:
                phase -= 2*pi
        elif phase < 0:
                phase += 2*pi
            
                
        self.__mag = abs(mag)
        self.__phase = round_phase(phase) 


        Phasor.instances.append(self)
        Phasor.instances_num += 1

    def __str__(self):
         return str(round(self.mag,6)) + '∠' + str(round(self.angle)) + "°"
    def __repr__(self):
         return str(round(self.mag,6)) + '∠' + str(round(self.angle)) + "°"

    def __imag__(self):
        return self.imag
    
    def __real__(self):
        return self.real
    
    def __complex__(self):
         return self.mag*(cos(self.phase) + 1j*sin(self.phase))


    def __conjugate__(self):
        return self.conjugate()

    def __bool__(self):
        return bool(self.mag)

    

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
            z = complex(self) + other
            mag, phase = cart2pol(z)
            return Phasor(mag,phase)
        elif isinstance(other,Phasor):
            z = complex(self) + complex(other)
            mag, phase = cart2pol(z)
            return Phasor(mag,phase)
    
    def __radd__(self,other):
        return self + other

    def __sub__(self,other):
        if isinstance(other,(int,float,complex)):
            z = complex(self) - other
            mag, phase = cart2pol(z)
            return Phasor(mag,phase)

        elif isinstance(other,Phasor):
            z = complex(self) - complex(other)
            mag, phase = cart2pol(z)
            return Phasor(mag,phase)

    def __rsub__(self,other):
        return -self + other

    def __neg__(self):
        """[Rotates a phasor 180°]

        Returns:
            [phasor]: [a phasor pointing to the opposite direction of the original phasor]
        """
        return Phasor(self.mag,self.phase+pi)

    def __mul__(self,other):
        if isinstance(other, (int, float)) and not isinstance(other, bool):
            if other >= 0:
                return Phasor(other*self.mag,self.phase)
            else:
                return Phasor(abs(other)*self.mag,self.phase+pi)
        elif isinstance(other, Phasor):
            return Phasor(self.__mag*other.__mag,self.phase+other.phase)
        elif isinstance(other,complex):
            z = self.__cartesian * other
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
            return Phasor(div._mag/self.mag,div.phase-self.phase)
        elif isinstance(other,Phasor):
            return Phasor(other.mag/self.mag,other.phase-self.phase)


    def __abs__(self):
        return self.__mag
    
    def __eq__(self,other):
        dif = self.mag - other.mag
        if (self.mag == other.mag) and (self.phase == other.phase):
            return True
        elif (dif < 0.001) and (self.phase == other.phase):
            return True
        else:
            return False

    def __pow__(self,other):
        if(other,isinstance(other,int)):
            return Phasor(self.mag**other,self.phase*other)

    def __iter__(self):
        return (i for i in (self.mag,self.phase))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))

    def __hash__(self):
        return hash(self.mag) ^ hash(self.phase)

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

    @property
    def mag(self):
        return self.__mag
    @property
    def real(self):
        return complex(self).real
    @property
    def imag(self):
        return complex(self).imag
    @property
    def complex(self):
        return self.get_cartesian()

    @property
    def angle(self):
        return self.__phase * 180 / pi

    @property
    def phase(self):
        return self.__phase
    

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



