import spaDesigner
import main
import numpy as np
class condition(spaDesigner.Ui_MainWindow):
    def __init__(self):
        self.setupUi(self)

    def figProperty(self):

        self.mpl.canvas.ax.cla()
        self.mpl.canvas.ax.get_yaxis().grid(True)
        self.mpl.canvas.ax.get_xaxis().grid(True)
        
        self.mpl.canvas.ax.set_ylabel("Power in dB", color="white")
        self.mpl.canvas.ax.set_xlabel("Frequency in MHz", color="white")

        self.mpl.canvas.fig.set_facecolor('black')
        self.mpl.canvas.ax.set_facecolor('black')
        self.mpl.canvas.ax.tick_params(axis='x', colors='white')
        self.mpl.canvas.ax.tick_params(axis='y', colors='white')


        self.mpl.canvas.ax.set_xticks(np.linspace(0, 16, 17))
        self.mpl.canvas.ax.set_yticks(np.linspace(0, 5, 6))

        self.mpl.canvas.ax.spines['bottom'].set_color('white')
        self.mpl.canvas.ax.spines['top'].set_color('white') 
        self.mpl.canvas.ax.spines['right'].set_color('white')
        self.mpl.canvas.ax.spines['left'].set_color('white')
    
    def noiseScl(self, fftSize, centerFrq, amp):
        
        if amp>=0 and amp<=10:
            noiseScl = 6+4
            noise = np.random.normal(0.0, noiseScl, fftSize)
            return noise
            
        elif amp>=10 and amp<=25:
            noiseScl = 13+4
            noise = np.random.normal(0.0, noiseScl, fftSize)
            return noise
        
        elif amp>=25 and amp<=50:
            noiseScl = 25+4
            noise = np.random.normal(0.0, noiseScl, fftSize)
            return noise
        elif amp>=50 and amp<=70:
            noiseScl = 36+15
            noise = np.random.normal(0.0, noiseScl, fftSize)
            return noise

        elif amp>=70 and amp<=100:
            noiseScl = 50#43+15
            noise = np.random.normal(0.0, noiseScl, fftSize)
            return noise
        elif amp>=100 and amp<=150:
            noiseScl = 55+8
            noise = np.random.normal(0.0,noiseScl, fftSize)
            return noise
        else:
            print("error")

