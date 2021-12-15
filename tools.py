
import matplotlib.pyplot as plt 
from phasors import phasor,versor
from numpy import linspace, pi, sin, cos, sqrt, arctan2
from utils import deg2rad
import numpy as np
from matplotlib.patches import FancyArrowPatch

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

