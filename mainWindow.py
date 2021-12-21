import sys
import numpy as np
from PyQt5 import QtWidgets
import spaDesigner
from matplotlib.animation import FuncAnimation
import pyvisa as visa
import ctypes
import condition
import parameterSet
from decimal import *
class DesignerMainWindow(QtWidgets.QMainWindow, spaDesigner.Ui_MainWindow):
    def __init__(self, parent=None):
        super(DesignerMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.cotrlCommand = []  # controlling command ready to send
        self.ani = [] 
        # self.dev_ice = None
        ''''button clicking events '''
        self.switchToAni = True
        self.btnPlot.clicked.connect(self.waveForms_param)
        self.btnClear.clicked.connect(self.clearPlot)
        self.MessageBox = ctypes.windll.user32.MessageBoxW
        self.rm = visa.ResourceManager()

        ''' checking whether the port is busy or not'''

        try:
            self.dev_ice = self.rm.open_resource('ASRL1::INSTR')
        except visa.VisaIOError:
            self.MessageBox(0,"port is in use by another program /n clear the port and run the program again!","Warnning",64)
            sys.exit()
        
        self.deviceConneParam()
        # self.deviceConneParam('sin') # setting the default wave from to sine
        self.btnClear.setEnabled(False) # disabling clear button on the start
        self.gbPuls.setVisible(False)
        self.gbTri.setVisible(False)
        self.high_level.setEnabled(False)
        self.low_level.setEnabled(False)
        self.offSet.setEnabled(False)
        # setting comboBox default value to sine
        self.cmbWaveForm.currentIndexChanged.connect(self.waveFromSelection)
    

    """ setting the device parameter and check if something is 
    wrong with the device
    like cheking if the device is on or off and cheking if the port is 
    used by another program
    """
    
    def deviceConneParam(self):
        try:
            self.dev_ice.baud_rate = 19200
            self.dev_ice.timeout = 65
            self.dev_ice.query('*IDN?')
            # self.dev_ice.write('func {}'.format(waveForm))
            
        except visa.VisaIOError:
            self.MessageBox(0,"Something is wrong with the device!!! \nEither the device is not on.\n Or there is bad connection in between the device and the computer!!!", 'Warnning',64)
            sys.exit()

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
            self.gbTri.setVisible(False)
            
        if self.cmbWaveForm.currentIndex() == 1:
            self.gbPuls.setVisible(False)
            self.gbTri.setVisible(False)
            self.dev_ice.write('func {}'.format("sin")) # setting the device waveform to the sin waveform
            
        elif self.cmbWaveForm.currentIndex() == 2:
            self.gbPuls.setVisible(True)
            self.lblAdge.setVisible(False)
            self.adgeTime.setVisible(False)
            self.gbTri.setVisible(False)
            self.dev_ice.write('func {}'.format('squ')) # setting the device waveform to the square waveform
            
        elif self.cmbWaveForm.currentIndex() == 3:
            self.gbPuls.setVisible(False)
            self.gbTri.setVisible(True)
            self.dev_ice.write('func {}'.format('ramp')) # setting the device waveform to the sawtoose/ramp/thriangle waveform
           
        elif self.cmbWaveForm.currentIndex() == 4:
            self.gbPuls.setVisible(True)
            self.gbTri.setVisible(False)
            self.lblAdge.setVisible(True)
            self.adgeTime.setVisible(True)
            self.dev_ice.write('func {}'.format('puls')) # setting the device waveform to the Pulse waveform
            
        elif self.cmbWaveForm.currentIndex() == 5:
            self.gbPuls.setVisible(False)
            self.gbTri.setVisible(False)
            self.dev_ice.write('func {}'.format('arb')) # setting the device waveform to the Arbitrary waveform
            
    """ Setting up Visualization property
    - setting x-axis and y-axis canvas number of ticks,
    - setting x-axis and y-axis minimum and amaximum limits
    - generating continues time using some ranges
    - generating sine wave 
    - based on the generated sine wave create fft for the center frequency and add noise to it
    """        

    def ploting(self):
        fftSize = 8192
        centerFrq = self.centerFrq.value()
        amp = self.amplitude.value()
        fs = centerFrq * 32 # sampling frequency 32 times of the center frequency
        ts = 1/fs
        noise = condition.condition.noiseScl(self, fftSize, centerFrq, amp)
        # setting seventeen x-axis ticks(grids) from 0 to twise of the center frequency
        self.mpl.canvas.ax.set_xticks(np.linspace(0,centerFrq*2,17)) 
        # adjusting noise amplitude based on center frequency aplitude
        if amp==0 or amp==1 or amp==2 or amp==3 or amp==4 or amp==5:
            # setting five y-axis ticks(grids) from 0 to the input amplitude/depends on
            #  the amplitude of the center frequency 
            self.mpl.canvas.ax.set_yticks(np.linspace(0, 6, 5))
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
        
        # global noiseScl
        condition.condition.figProperty(self) #  setup the canvas property
        # adjusting the noise scale based on the inputed center frequency
        # noise = condition.condition.noiseScl(self, fftSize, centerFrq, amp) 
        # passing noise, FFT size, Frequency amd aplitude for plotting fubction
        self.ploting()

    '''
    variable setting sine wave form parameter setting

    '''
    def waveForms_param(self):
        Frequency = self.centerFrq.value() * 10**6
        Amplitude = self.amplitude.value()
        offSet = 0
        dutyCycle = self.dcycle.value()
        symmetryRam = self.symmetry.value()
        adgeTime = self.adgeTime.value()/10**9
        waveListIndex_ = self.cmbWaveForm.currentIndex()

        ''' for some reasone high_level and low_level of the power is must be equal'''
       

        high_low_level = Amplitude/2
        highLevel = high_low_level
        lowLevel = high_low_level

        self.high_level.setValue(highLevel)
        self.low_level.setValue(-(lowLevel))

        self.validation(waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet, dutyCycle, symmetryRam, adgeTime)

    '''validating each input based on their upper and lower values'''


    def validation(self, waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet, dutyCycle, symmetryRam, adgeTime):
        if waveListIndex_ == 0:
            self.MessageBox(0, "please select the proper waveform", 'Warnning',64)
        else:
            if waveListIndex_ == 1:
                if Amplitude >= 1E-2 and Amplitude <= 20:
                    if Frequency >= 10E-5 and Frequency <= 5E7:
                        self.transmitter_(waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet, dutyCycle, symmetryRam, adgeTime)   
                    else:
                        self.MessageBox(0,"Invalid input!!! Frequency range is between 1E-5 and 5E7 MHz.", 'Warnning',64)
                else:
                    self.MessageBox(0,"Amplitude is in range of 0.01 and 20 Volt!!!", 'Warnning',64)
                    
            elif waveListIndex_ == 2:
                if Amplitude >= 1E-2 and Amplitude <= 20:
                    if (Frequency >= 10E-5 and Frequency <= 5E7):
                        if dutyCycle >= 20 and dutyCycle <= 80:
                            self.transmitter_(waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet,
                                            dutyCycle, symmetryRam, adgeTime)
                        else:
                            self.MessageBox(0,"Invalid input!!! high Dutycycle range is between 20 and 80 % .", 'Warnning',64)
                    else:
                        self.MessageBox(0,"Invalid input!!! Frequency range is between 1E-5 and 5E7 MHz.", 'Warnning',64)
                else:
                    self.MessageBox(0,"Amplitude is in range of 0.01 and 16 Volt!!!", 'Warnning',64)
                
            elif waveListIndex_ == 3:
                if Amplitude >= 1E-2 and Amplitude <= 20:
                    if Frequency >= 10E-5 and Frequency <= 1E7:
                        if symmetryRam >= 0 and symmetryRam <= 100:
                            self.transmitter_(waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet, dutyCycle, symmetryRam, adgeTime)
                        else:
                            self.MessageBox(0,"Invalid input!!! symmetry range is between 0 and 100.", 'Warnning',64)
                    else:
                        self.MessageBox(0,"Invalid input!!! Frequency range is between 1E-5 and 5E7 MHz.", 'Warnning',64)
                else:
                    self.MessageBox(0,"Amplitude is in range of 0.01 and 20 Volt!!!", 'Warnning',64)
                
            elif waveListIndex_ == 4:
                if Amplitude >= 1E-2 and Amplitude <= 10:
                    if Frequency >= 1E-5 and Frequency <= 2.5E7:
                        if dutyCycle >= 0.999 and dutyCycle <= 99.999:
                            if adgeTime >= 8E-09 and adgeTime <= 5E-08:  
                                self.transmitter_(waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet, 
                                    dutyCycle, symmetryRam, adgeTime)
                            else:
                                self.MessageBox(0,"Invalid input!!! adgeTime range is between 8E-09 and 5E-08 .", 'Warnning',64)
                        else:
                            self.MessageBox(0,"Invalid input!!! Dutycyle range is between 0.999 and 99.999 % .", 'Warnning',64)
                    else:
                        self.MessageBox(0,"Invalid input!!! Frequency range is between 1E-5 and 2.5E7 MHz.", 'Warnning',64)
                else:
                    self.MessageBox(0,"Amplitude is in range of 0.01 and 10 Volt!!!", 'Warnning',64)

            else:
                if Frequency >= 1E-5 and Frequency <= 2.5E7:
                    self.transmitter_(waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet,
                                        dutyCycle, symmetryRam, adgeTime)  
                else:
                    self.MessageBox(0,"Invalid input!!! Frequency range is between 1E-5 and 2.5E7 MHz.", 'Warnning',64)         
        
    '''
        changing the parameter of each wave forms and showing/visualizing 
        the fft of output frequency / center frequency

    '''
    
    def transmitter_(self, waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet, dutycycle, symmetryRam, adgeTime):

        period_ = (1 / Frequency)*10**9
        self.period.setValue(period_)

        if waveListIndex_ == 1:
            parameterSet.parameters_.settingParameter(self, waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet)
            self.play_visualizaton()
        
        elif waveListIndex_ == 2:
            '''
            basic formla for calculating dutycycle, highWidth and lowWidth is 
            if Dutycycle = (highWidth/periode)*100 there for 
            highWidth = (Dutycycle *period)/100
            lowWidth = period-highWidth
            '''
            pulseWidth = (dutycycle * period_)/100
            pulsePeriod = period_ - pulseWidth
            if pulseWidth > 10 and pulsePeriod >10:

                self.highWidth.setValue(pulseWidth)
                self.lowWidth.setValue(pulsePeriod)

                parameterSet.parameters_.settingParameter(self, waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet=0,
                                                hign_width = pulseWidth, low_width=pulsePeriod, duty_cycle = dutycycle)
                self.play_visualizaton()
            else: 
                '''
                set the dutycycle to 50 % to avoid the highwidth and the lowwidth minimum value limite
                errors
                '''
                dcycle_ = 50
                pulseWidth = (dcycle_ * period_)/100
                pulsePeriod = period_ - pulseWidth

                self.highWidth.setValue(pulseWidth)
                self.lowWidth.setValue(pulsePeriod)
                self.dcycle.setValue(dcycle_)

                parameterSet.parameters_.settingParameter(self, waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet=0,
                                                hign_width = pulseWidth, low_width=pulsePeriod, duty_cycle = dcycle_)
                self.play_visualizaton()

        elif waveListIndex_ == 3:
            '''
            basic formla for calculating Symmetry, fallTime and riseTime is 
            if Symmetry = (riseTime/periode)*100 there for 
            RiseTime = (Symmetry *period)/100
            FallTime = period-RiseTime
            '''
            raisTime = (symmetryRam * period_)/100
            fallTime = period_ - raisTime

            self.raisTime.setValue(raisTime)
            self.fallTime.setValue(fallTime)

            parameterSet.parameters_.settingParameter(self, waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet= 0,
                                            rise_time = raisTime, fall_time = fallTime, symmetry = symmetryRam)
            self.play_visualizaton() 
        
        elif waveListIndex_ == 4:
            pulseWidthPulse = (dutycycle * period_)/100
            pulsePeriodPulse = period_ - pulseWidthPulse

            self.high_level.setValue(Amplitude)
            self.low_level.setValue(offSet)

            if pulseWidthPulse > 20 and pulsePeriodPulse >20:

                self.highWidth.setValue(pulseWidthPulse)
                self.lowWidth.setValue(pulsePeriodPulse)

                parameterSet.parameters_.settingParameter(self, waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet=0,
                                                hign_width = pulseWidthPulse, low_width=pulsePeriodPulse, duty_cycle = dutycycle, edge_time = (8)/10**9)
                self.play_visualizaton()
            else:
                '''
                set the dutycycle to 50 % to avoid the highwidth and the lowwidth minimum value limite
                errors
                '''
                dcycle_ = 50
                pulseWidth = (dcycle_ * period_)/100
                pulsePeriod = period_ - pulseWidth

                self.highWidth.setValue(pulseWidth)
                self.lowWidth.setValue(pulsePeriod)
                self.dcycle.setValue(dcycle_)

                parameterSet.parameters_.settingParameter(self, waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet=0,
                                                hign_width = pulseWidth, low_width=pulsePeriod, duty_cycle = dcycle_, edge_time = (8)/10**9)
                self.play_visualizaton()

        else:
            parameterSet.parameters_.settingParameter(self, waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet)
            self.play_visualizaton()

    def draw(self, Frequency, Amplitude, highLevel, lowLevel, offSet, highWidth,
             lowWidth, dutyCycle, raisTime, fallTime, symmetryRam, adgeTime, waveListIndex_):
        if waveListIndex_ == 0:
            self.MessageBox(0, "please select the proper waveform", 'Warnning',64)
        else:
            if Amplitude >= 1E-2 and Amplitude <= 20:
                if waveListIndex_ == 1:
                    if Frequency >= 10E-5 and Frequency <= 5E7:
                        parameterSet.parameters_.settingParameter(self, waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet)
                        self.play_visualizaton() 
                    else:
                        self.MessageBox(0,"Invalid input!!! Frequency range is between 1E-5 and 5E7 MHz.", 'Warnning',64)
                elif waveListIndex_ == 2:
                    if (Frequency >= 10E-5 and Frequency <= 5E7 and Amplitude >= 1E-2 and Amplitude <= 16 and highWidth >= 1.69E-3 and
                        highWidth <= 6.77E-3 and  lowWidth >= 1.69E-3 and lowWidth <= 6.77 and dutyCycle >= 20 and dutyCycle <= 80):
                        parameterSet.parameters_.settingParameter(self, waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet,
                                            hign_width = highWidth, low_width=lowWidth, duty_cycle = dutyCycle)
                        self.play_visualizaton() 
                    else:
                        self.MessageBox(0,"Invalid input!!! Frequency range is between 1E-5 and 5E7 MHz.", 'Warnning',64)
                elif waveListIndex_ == 3:
                    if (Frequency >= 10E-5 and Frequency <= 1E7 and fallTime>=0 and fallTime <= 8.47E-3 and raisTime >= 0 and raisTime <=8.47E-3
                        and symmetryRam >= 0 and symmetryRam <= 100):
                        parameterSet.parameters_.settingParameter(self, waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet,
                                            rise_time = raisTime, fall_time = fallTime, symmetry = symmetryRam)
                        self.play_visualizaton() 
                    else:
                        self.MessageBox(0,"Invalid input!!! Frequency range is between 1E-5 and 5E7 MHz.", 'Warnning',64)
                elif waveListIndex_ == 4:
                    if (Frequency >= 1E-5 and Frequency <= 2.5E7 and highWidth >= 2E-08 and highWidth <= 8.473E-03 and lowWidth >= 2E-08 
                        and lowWidth <= 8.473E-03 and dutyCycle >= 1E-03 and dutyCycle <= 9.9999E+01 and adgeTime >= 8E-09 and adgeTime <= 5E-08):
                        parameterSet.parameters_.settingParameter(self, waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet,
                                            hign_width = highWidth, low_width = lowWidth, duty_cycle = dutyCycle, edge_time = adgeTime)
                        self.play_visualizaton() 
                    else:
                        self.MessageBox(0,"Invalid input!!! Frequency range is between 1E-5 and 2.5E7 MHz.", 'Warnning',64)
                else:
                    if Frequency >= 1E-5 and Frequency <= 2.5E7:
                        parameterSet.parameters_.settingParameter(self, waveListIndex_, Frequency, Amplitude, highLevel, lowLevel, offSet)
                        self.play_visualizaton()   
                    else:
                        self.MessageBox(0,"Invalid input!!! Frequency range is between 1E-5 and 2.5E7 MHz.", 'Warnning',64)         
            else:
                self.MessageBox(0,"Amplitude is in range of 0.01 and 20 Volt!!!", 'Warnning',64)

    def play_visualizaton(self):
      
                
        # self.dev_ice.write("OUTP {}".format("1"))
        # enabling and disabling button plot and button clear
        self.btnPlot.setEnabled(False)
        self.btnClear.setEnabled(True)
        # moving the plot/image based on the given time interval
        self.ani = FuncAnimation(self.mpl.canvas.fig, self.animate, interval=90) 
        # condition.condition.figProperty(self)
        self.mpl.canvas.draw()
        self.mpl.canvas.flush_events()
        
        # self.clearPlot()          
    
    def clearPlot(self):
        self.switchToAni = False
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