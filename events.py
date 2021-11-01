
import matplotlib.pyplot as plt 
import random
import sys
import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from phasors import set_axis



class LineBuilder:
    def __init__(self, event_name='button_press_event'):
        (self.figure, self.axes) = plt.subplots()
        self.axes = set_axis(self.axes)
        plt.xlim([-5, 5])
        plt.ylim([-5, 5])
        (self.xs, self.ys) = ([0,1], [0,1])
        (self.line,) = self.axes.plot(self.xs, self.ys,lw=3)
        self.canvas = self.figure.canvas
        self.conn_id = self.canvas.mpl_connect(event_name, self.callback)
        self.conn_id = self.canvas.mpl_connect(event_name, self.callback)

    def start(self):
        plt.show()

    def update_line(self, event):
        self.xs[1] = event.xdata
        self.ys[1] = event.ydata
        self.line.set_data(self.xs, self.ys)

    def callback(self, event):
        cont, ind = self.line.contains(event)
        if(cont):
            print(cont)
        if event.inaxes != self.line.axes:
            return
        self.update_line(event)
        self.canvas.draw()

lb = LineBuilder()
lb.start()