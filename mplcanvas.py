from PyQt5 import QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class Mpl(FigureCanvas):
    '''
    both y and x axis ticks property like- color, its width, the direction and 
    it length
    '''
    def __init__(self):
        
        self.fig = Figure()
        # self.fig, self.ax = plt.subplots(nrows=1)
        plt.subplots_adjust(hspace=0.1)
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        
        # plt.style.use('dark_background')
        self.ax.cla()
        self.ax.get_yaxis().grid(True)
        self.ax.get_xaxis().grid(True)
        self.ax.set_ylim(ymin=0)
        self.ax.set_xlim(xmin=0)
        
        self.ax.set_ylabel("Power in dB", color="white")
        self.ax.set_xlabel("Frequency in MHz", color="white")


        self.fig.set_facecolor('black')
        self.ax.set_facecolor('black')
        self.ax.set_xticks(np.linspace(0, 16, 17))
        self.ax.set_yticks(np.linspace(0, 5, 6))
        # plt.locator_params(tight=True, nbins=1)
        # plt.locator_params(axis='x', nbins=25)
        self.ax.tick_params(axis='both', colors='white', width=2.5, tickdir='inout', length=7)
        # self.ax.tick_params(axis='y', colors='white')

        self.fig.tight_layout(rect=[-1.0, 0.07, 1.033, 1.01])

        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white') 
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')

        self.fig.tight_layout(rect=[0.0, 0.05, 1.02, 1.0])
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

class mplcanvas(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # super(MplWidget, self).__init__(parent)
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = Mpl()
        self.vlb = QtWidgets.QVBoxLayout()
        self.vlb.addWidget(self.canvas)
        self.setLayout(self.vlb)
        # self.vbl = QtWidgets.QVBoxLayout()
        # self.vbl.addWidget(self.canvas)
        # self.setLayout(self.vbl)