import numpy as np
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import spaDesigner
from matplotlib.animation import FuncAnimation
# from scipy.fft import fft, fftfreq
import pyvisa as visa
import scipy.fftpack
import condition
class DesignerMainWindow(QtWidgets.QMainWindow, spaDesigner.Ui_MainWindow):
    def __init__(self, parent=None):
        super(DesignerMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.ani = [] 
        # button clicking events 
        self.btnPlot.clicked.connect(self.draw)
        self.btnClear.clicked.connect(self.clearPlot)
        
        self.btnClear.setEnabled(False) # disabling clear button on the start

        # hiding all waveform properties except sine wave
        self.gbPuls.setVisible(False)
        self.gbSqu.setVisible(False)
        self.gbTri.setVisible(False)
        self.gbSin.setVisible(True)
        # setting comboBox default value to sine
        self.cmbWaveForm.currentIndexChanged.connect(self.waveFromSelection)

    def deviceConneParam(self, waveForm):
        rm = visa.ResourceManager()
        dev_ice = rm.open_resource('ASRL1::INSTR')
        dev_ice.baud_rate = 19200
        dev_ice.timeout = 65
        # dev_ice.query('*IDN?') 
        dev_ice.write('func {}'.format(waveForm))
    """ setting up waveform navigation in between 
        -sine, 
        -square, 
        -triangle, 
        -pulse and 
        -arbitrary waveforms.
    """
    def waveFromSelection(self):
        if self.cmbWaveForm.currentIndex() == 0:
            self.gbPuls.setVisible(False)
            self.gbSqu.setVisible(False)
            self.gbTri.setVisible(False)
            self.gbSin.setVisible(True)
            self.deviceConneParam('sin')
        if self.cmbWaveForm.currentIndex() == 1:
            self.gbPuls.setVisible(False)
            self.gbSqu.setVisible(True)
            self.gbTri.setVisible(False)
            self.gbSin.setVisible(False)
            self.deviceConneParam('squ')
        if self.cmbWaveForm.currentIndex() == 2:
            self.gbPuls.setVisible(False)
            self.gbSqu.setVisible(False)
            self.gbTri.setVisible(True)
            self.gbSin.setVisible(False)
            self.deviceConneParam('ramp')
        if self.cmbWaveForm.currentIndex() == 3:
            self.gbPuls.setVisible(True)
            self.gbSqu.setVisible(False)
            self.gbTri.setVisible(False)
            self.gbSin.setVisible(False)
            self.deviceConneParam('puls')
        if self.cmbWaveForm.currentIndex() == 4:
            self.gbPuls.setVisible(True)
            self.gbSqu.setVisible(False)
            self.gbTri.setVisible(False)
            self.gbSin.setVisible(False)
            self.deviceConneParam('arb')

    """ Setting up Visualization property
    - setting x-axis and y-axis canvas number of ticks,
    - setting x-axis and y-axis minimum and amaximum limits
    - generating continues time using some ranges
    - generating sine wave 
    - based on the generated sine wave create fft for the center frequency and add noise to it
    """        
    def ploting(self, noise, fftSize, centerFrq, amp):
        fs = centerFrq * 32 # sampling frequency 32 times of the center frequency
        ts = 1/fs
        # setting seventeen x-axis ticks(grids) from 0 to twise of the center frequency
        self.mpl.canvas.ax.set_xticks(np.linspace(0,centerFrq*2,17)) 
        # adjusting noise amplitude based on center frequency aplitude
        if amp==0 or amp==1 or amp==2 or amp==3 or amp==4 or amp==5:
            # setting five y-axis ticks(grids) from 0 to the input amplitude/depends on
            #  the amplitude of the center frequency 
            self.mpl.canvas.ax.set_yticks(np.linspace(0,6, 5))
            # setting y-axis limit from 0 to input amplitude plus 1.5
            self.mpl.canvas.ax.set_ylim(0.0,6+1.5)
            # creating list of continues time from zero to fft size
            contTime = np.linspace(0, fftSize * ts, fftSize)
            xf = np.linspace(0.0, 1.0 / (2.0 * ts), fftSize//2)
            # creating sine wave with amplitude (amp)
            sinWave = amp * np.sin(2 * np.pi * centerFrq * contTime) 
            # frequency domain of sine wave and add noise to it
            FFTWaveForm = np.fft.fft(sinWave + noise)  
            # plot/ draw FFT on canvas with 'y'/Yellow color      
            self.mpl.canvas.ax.plot(xf, 2.0/fftSize * np.abs(FFTWaveForm[:fftSize//2]), 'y')
            # setting x-axis limit from 0 to twis of the center frequency
            self.mpl.canvas.ax.set_xlim(0.0, centerFrq*2) 
        else:
            # setting five y-axis ticks(grids) from 0 to the input amplitude/depends on
            #  the amplitude of the center frequency 
            self.mpl.canvas.ax.set_yticks(np.linspace(0,amp, 5))
            # setting y-axis limit from 0 to input amplitude plus 1.5
            self.mpl.canvas.ax.set_ylim(0.0,amp+1.5)
            # creating list of continues time from zero to fft size
            contTime = np.linspace(0, fftSize * ts, fftSize)
            xf = np.linspace(0.0, 1.0 / (2.0 * ts), fftSize//2)
            # creating sine wave with amplitude (amp)
            sinWave = amp * np.sin(2 * np.pi * centerFrq * contTime) 
            # frequency domain of sine wave and add noise to it
            FFTWaveForm = np.fft.fft(sinWave + noise )   
            # plot/ draw FFT on canvas with 'y'/Yellow color      
            self.mpl.canvas.ax.plot(xf, 2.0/fftSize * np.abs(FFTWaveForm[:fftSize//2]), 'y')
            # setting x-axis limit from 0 to twis of the center frequency
            self.mpl.canvas.ax.set_xlim(0.0, centerFrq*2)         

    def animate(self, i):
        fftSize = 8192
        centerFrq = float(self.centerFrq.value())       
        amp = float(self.amplitude.value())
        # global noiseScl
        condition.condition.figProperty(self) #  setup the canvas property
        # adjusting the noise scale based on the inputed center frequency
        noise = condition.condition.noiseScl(self, fftSize, centerFrq, amp) 
        # passing noise, FFT size, Frequency amd aplitude for plotting fubction
        self.ploting(noise, fftSize, centerFrq, amp)
    def draw(self):
        # enabling and disabling button plot and button clear
        self.btnPlot.setEnabled(False)
        self.btnClear.setEnabled(True)
        # moving the plot/image based on the given time interval
        self.ani = FuncAnimation(self.mpl.canvas.fig, self.animate, interval=90) 
        # condition.condition.figProperty(self)
        self.mpl.canvas.draw()
        self.mpl.canvas.flush_events()
    def clearPlot(self):
        # disable clear button and enabling plotting button
        self.btnClear.setEnabled(False)
        self.btnPlot.setEnabled(True)
        self.mpl.canvas.ax.cla() # clearing the canvas/ the fft plot
        self.ani._stop() # stoping the animating plot
        condition.condition.figProperty(self) # setup the canvas property
        # implmenting the property on the canvas
        self.mpl.canvas.draw()
        self.mpl.canvas.flush_events()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = DesignerMainWindow()
    form.show()
    sys.exit(app.exec_())