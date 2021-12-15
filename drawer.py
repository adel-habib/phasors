from matplotlib import patches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from phasors import phasor
from numpy import cos, sin, pi

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
    ax.axis('equal')
    return ax 

class drawer:
    def __init__(self) -> None:
        fig, ax = plt.subplots()
        self._fig = fig
        self._ax = set_axis(ax)
        self._xdata = list()
        self._ydata = list()
        #self._arrow = arrow = FancyArrowPatch(posA=(originx, originy), posB=(x[-1], y[-1]), fc=None, ec=col,arrowstyle='simple, head_width=10, head_length=10, tail_width=0.0',)
    
    def plot_vector(self,vec : phasor,from_last=False,label=None):
        if from_last:
            ox = self._xdata[-1]
            oy = self._ydata[-1]
        else:
            ox = 0
            oy = 0
        x = ox + vec._mag*cos(vec.phase)
        y = oy + vec._mag*sin(vec.phase)
        self._xdata.append(x)
        self._ydata.append(y)
        self._ax.plot([ox,x],[oy,y],alpha=1)
        col = self._ax.lines[-1].get_color()
        arrow = FancyArrowPatch(posA=(ox, oy), posB=(x, y), fc=col, ec=col,arrowstyle='simple, head_width=10, head_length=10, tail_width=0.0', shrinkA=0,  shrinkB=0)
        self._ax.add_patch(arrow)
    
    def draw(self,vec : phasor):
        self.plot_vector(vec)
    def drawf(self,vec : phasor):
        self.plot_vector(vec,from_last=True)


l1 = phasor(30,pi/4)
l2 = phasor(30,pi/3)
l3 = phasor (50,pi)
d = drawer()
d.draw(l1)
d.drawf(l2)
d.drawf(l3)
d.draw(l3)

plt.show()
