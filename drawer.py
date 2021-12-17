import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from numpy.lib.type_check import imag
from phasor import Phasor
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
    #ax.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)
    # Create 'x' and 'y' labels placed at the end of the axes
    ax.set_xlabel(r'$\Re(z)$', size=14, labelpad=-24, x=1.05)
    ax.set_ylabel('$\Im(z)$', size=14, labelpad=-21, y=1.02, rotation=0)
    ax.axis('equal')
    return ax 



class drawer:
    instances = []
    instances_num = 0

    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots()
        
        self._xdata = list()
        self._ydata = list()

        self._xdata_aux = list()
        self._ydata_aux = list()

        drawer.instances.append(self)
        drawer.instances_num+=1

    
    def plot_vector(self,vec : Phasor,from_last=False,label=None,ls=None):

        if from_last:
            ox = self._xdata[-1]
            oy = self._ydata[-1]
        else:
            ox = 0
            oy = 0
        x = ox + vec.real

        y = oy + vec.imag

        self._xdata.append(x)

        self._ydata.append(y)

        self.ax.plot([ox,x],[oy,y],alpha=0)

        style="Simple,head_width=10,head_length=10"
        #kw = dict(arrowstyle=style, linestyle=None, lw=1,color="k",shrinkA=0,  shrinkB=0)
        kw = dict(arrowstyle='simple, head_width=10, head_length=10, tail_width=0.0', shrinkA=0,  shrinkB=0,lw=1,color="k")
        arrow = FancyArrowPatch((ox, oy), (x, y),**kw)
        self.ax.add_patch(arrow)
        #split_arrow(arrow,color_tail="k",color_head="k", ls_tail="--", lw_tail=2)
    
    def reduce_vector(self, vec : Phasor):
        self.plot_vector(vec)
        self.ax.plot([vec.real,0],[vec.imag,vec.imag],"k",ls="--")
        self.ax.plot([vec.real,vec.real],[vec.imag,0],"k",ls="--")
    
    def aux_vector(self,vec : Phasor,from_last=False,label=None,ls=None,col="k"):
        if from_last:
            ox = self._xdata[-1]
            oy = self._ydata[-1]
        else:
            ox = 0
            oy = 0
        x = ox + vec._mag*cos(vec._phase)

        y = oy + vec._mag*sin(vec._phase)

        self._xdata_aux.append(x)

        self._ydata_aux.append(y)
        self.ax.plot([ox,x],[oy,y],col,ls="--")

    
    def draw(self,vec):
        if isinstance(vec, list):
            for v in vec:
                self.draw(v)
            return
        self.plot_vector(vec)

    def drawf(self,vec : Phasor):
        self.plot_vector(vec,from_last=True)

    def draw_triangle(self,v : Phasor):
        real = v.real
        imag = v.imag
        phi = pi 
        phi2 = pi / 2 
        if v.phase > pi:
            phi2 = -phi2
        if v.phase < pi/2 or v.phase > 3*pi/2:
            phi = 0

        self.plot_vector(Phasor(real,phi))
        self.plot_vector(Phasor(imag,phi2),from_last=True)
        self.plot_vector(v)

            
    
    def draw_parallelogram(self,v : Phasor ,w : Phasor):
        """[Plots the vectorial sum of two phasors]

        Args:
            v ([phasor]): [fist phasor]
            w ([phasor]): [second phasor]
        """

        self.plot_vector(v)
        self.aux_vector(w,from_last=True)
        self.plot_vector(w)
        self.aux_vector(v,from_last=True)
        self.plot_vector(v+w)

    def draw_tiptotail(self,v : Phasor ,w : Phasor):
        self.plot_vector(v)
        self.plot_vector(w,from_last=True)
        self.plot_vector(v+w)
    def sub(self,v,w):
        """[Plots the vectorial substraction of two phasors, v - w]

        Args:
            v ([type]): [description]
            w ([type]): [description]
        """
        self.plot_vector(v)
        self.aux_vector(-w,from_last=True)
        self.plot_vector(w)
        self.plot_vector(v-w)
    


def instance_exist():
    """[Checks if an instance of the class drawer exists, creates an instance if none exists]
    """
    if drawer.instances_num == 0:
       drawer()



def draw(v):
    instance_exist()
    drawer.instances[0].draw(v)
def drawf(v):
    instance_exist()
    drawer.instances[0].drawf(v)
def draw_parallelogram(v1 : Phasor, v2 : Phasor):
    instance_exist()
    drawer.instances[0].draw_parallelogram(v1,v2)
def draw_tip2tail(v1 : Phasor, v2 : Phasor):
    instance_exist()
    drawer.instances[0].draw_tiptotail(v1,v2)

def draw_components(v):
    instance_exist()
    drawer.instances[0].reduce_vector(v)

def draw_triag(v):
    instance_exist()
    drawer.instances[0].draw_triangle(v)

def draw_all():
    """[Draws all existing phasors i.e all instances of class Phasor]
    """
    for v in Phasor.instances:
        draw(v)

def gca():
    if drawer.instances_num > 0:
        return drawer.instances[0].ax
def gcf():
    if drawer.instances_num > 0:
        return drawer.instances[0].fig




v1 = Phasor(2,pi/4)
draw_triag(v1)
plt.show()
