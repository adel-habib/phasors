
from numpy import cos, sin, pi, sqrt, arctan2, angle
import numpy as np

def cart2pol(z : complex):

    if isinstance(z,(int,float)):
        z = complex(z)

    mag = abs(z)
    phi = angle(z)
    return mag, phi

def pol2cart(mag : float, phi : float) -> complex:
    x = mag * cos(phi)
    y = mag * sin(phi)
    return(x + 1j*y)     

def deg2rad(angle : float) ->float:
    return angle*pi/180

def rad2deg(angle : float) -> float:
    return angle * 180/pi

# def cart2pol(z : complex):
#     """[Forms a Phasor from a complex number]

#     Args:
#         z ([complex]): [a complex number i,e 2+4j]

#     Returns:
#         [Phasor]: [A phasor i.e 1∠30°]
#     """    
#     if isinstance(z,(int,float)):
#         z = complex(z)
#     x = z.real
#     y = z.imag
#     mag = sqrt(x**2 + y**2)
#     phi = arctan2(y, x)
#     return phasor(mag,phi)



# def symmetrical_components(l1,l2,l3,polar=False):
#     """[Calculates the symmetrical components of a power system, the line currents, voltages or impedences can be passed as phasors, or complex numbers ]

#     Args:
#         l1 ([Phasor, complex]): [Line 1]
#         l2 ([Phasor, complex]): [Line 2]
#         l3 ([Phasor, complex]): [Line 3]

#     Returns:
#         [ndarray]: [The symmetrical components as Phasors inside a np array]
#     """    

#     a = versor(deg2rad(120))
#     a2 = a**2
#     s =  np.array([[1,1,1],[1,a,a2],[1,a2,a]])
#     L =  np.array([l1,l2,l3])
            
#     Ls = 1/3 * np.matmul(s,L)
#     for i in range(3):
#         if isinstance(Ls[i],complex):
#             Ls[i] = cart2pol(Ls[i])

#     return Ls

