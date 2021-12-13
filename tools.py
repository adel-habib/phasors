
import matplotlib.pyplot as plt 
from phasors import phasor,versor
from numpy import linspace, pi, sin, cos 
from utils import cart2pol, deg2rad
import numpy as np

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
    plt.axis('equal')
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
    if(isinstance(vector,(complex,float))):
        vector = phasor(z=vector)
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
    a = versor(pi*2/3)
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


def plot_phasor(mag,angle,radian = True):
    if not radian:
        angle = deg2rad(angle)
    x = np.array([0, mag * np.cos(angle)])
    y = np.array([0,mag * np.sin(angle)])
    plt.plot(x,y,marker=(3,0,0),markevery=[-1])
    plt.plot(-x,-y,color='k',alpha=0)

