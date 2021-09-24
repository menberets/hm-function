import numpy as np
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import spaDesigner
from matplotlib.animation import FuncAnimation
# from scipy.fft import fft, fftfreq
import scipy.fftpack
import condition
class DesignerMainWindow(QtWidgets.QMainWindow, spaDesigner.Ui_MainWindow):
    def __init__(self, parent=None):
        super(DesignerMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.btnPlot.clicked.connect(self.draw)

        self.btnClear.clicked.connect(self.clearPlot)
        self.gbPuls.setVisible(False)
        self.gbSqu.setVisible(False)
        self.gbTri.setVisible(False)
        self.gbSin.setVisible(True)
        self.cmbWaveForm.currentIndexChanged.connect(self.waveFromSelection)
    
        # self.ani = []
        # self.btnClear.setVisible(False)
    def waveFromSelection(self):
        if self.cmbWaveForm.currentIndex() == 0:
            self.gbPuls.setVisible(False)
            self.gbSqu.setVisible(False)
            self.gbTri.setVisible(False)
            self.gbSin.setVisible(True)
        if self.cmbWaveForm.currentIndex() == 1:
            self.gbPuls.setVisible(False)
            self.gbSqu.setVisible(True)
            self.gbTri.setVisible(False)
            self.gbSin.setVisible(False)
        if self.cmbWaveForm.currentIndex() == 2:
            self.gbPuls.setVisible(False)
            self.gbSqu.setVisible(False)
            self.gbTri.setVisible(True)
            self.gbSin.setVisible(False)
        if self.cmbWaveForm.currentIndex() == 3:
            self.gbPuls.setVisible(True)
            self.gbSqu.setVisible(False)
            self.gbTri.setVisible(False)
            self.gbSin.setVisible(False)
    def ploting(self, noise, fftSize, centerFrq, amp):
        fs = centerFrq * 32
        ts = 1/fs
        self.mpl.canvas.ax.set_xticks(np.linspace(0,centerFrq*2,17))
        if amp==0 or amp==1 or amp==2 or amp==3 or amp==4 or amp==5:
            self.mpl.canvas.ax.set_yticks(np.linspace(0,6, 5))
            self.mpl.canvas.ax.set_ylim(0.0,6+1.5)
            t1 = np.linspace(0, fftSize * ts, fftSize)
            xf = np.linspace(0.0, 1.0 / (2.0 * ts), fftSize//2)
            
            y = amp * np.sin(2 * np.pi * centerFrq * t1)  #+(amp * np.sin(2 * np.pi * 56 * t11))
            
            yf = np.fft.fft(y + noise)        
            self.mpl.canvas.ax.plot(xf, 2.0/fftSize * np.abs(yf[:fftSize//2]), 'c')
            self.mpl.canvas.ax.set_xlim(0.0, centerFrq*2)  #1.0 / (2.0 * ts))
        else:
            self.mpl.canvas.ax.set_yticks(np.linspace(0,amp, 5))
            self.mpl.canvas.ax.set_ylim(0.0,amp+1.5)
            t1 = np.linspace(0, fftSize * ts, fftSize)
            xf = np.linspace(0.0, 1.0 / (2.0 * ts), fftSize//2)

            y = amp * np.sin(2 * np.pi * centerFrq * t1)  #+(amp * np.sin(2 * np.pi * 56 * t11))
            
            yf = np.fft.fft(y + noise )        
            self.mpl.canvas.ax.plot(xf, 2.0/fftSize * np.abs(yf[:fftSize//2]), 'c')
            self.mpl.canvas.ax.set_xlim(0.0, centerFrq*2) # 1.0 / (2.0 * ts))        

    def animate(self, i):
        fftSize = 8192
        centerFrq = float(self.centerFrq.value())       
        amp = float(self.amplitude.value())
        # global noiseScl
        condition.condition.figProperty(self)
        noise = condition.condition.noiseScl(self, fftSize, centerFrq, amp)
        self.ploting(noise, fftSize, centerFrq, amp)
    def draw(self):
        self.ani = FuncAnimation(self.mpl.canvas.fig, self.animate, interval=80)   #, repeat=False
        # condition.condition.figProperty(self)
        self.mpl.canvas.draw()
        self.mpl.canvas.flush_events()
    def clearPlot(self):
        self.mpl.canvas.ax.cla()
        self.ani._stop()
        condition.condition.figProperty(self)
        self.mpl.canvas.draw()
        self.mpl.canvas.flush_events()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = DesignerMainWindow()
    form.show()
    app.exec_()