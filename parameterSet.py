from matplotlib.pyplot import cla
import pyvisa as visa
class parameters_():
    def __init__(self):
        self.dev_ice = []
    def settingParameter(self, index_, ceter_frequency, amplitude, high_level, low_level, offSet, hign_width = 0,low_width = 0,duty_cycle =0, rise_time = 0, fall_time = 0, symmetry = 0, edge_time = 0):#
        if index_ == 1:
            if high_level-low_level ==amplitude:                
                self.dev_ice.write('FREQ {}'.format(ceter_frequency))
                self.dev_ice.write('VOLT {}'.format(amplitude))
                # self.dev_ice.write('PER {}'.format(per))
                self.dev_ice.write('VOLT:HIGH {}'.format(high_level))
                self.dev_ice.write('VOLT:LOW {}'.format(low_level))
                self.dev_ice.write('VOLT:OFFS {}'.format(offSet))
            else:
                compensation = amplitude/2
                high_level = compensation
                low_level = -(compensation)                 
                self.dev_ice.write('FREQ {}'.format(ceter_frequency))
                self.dev_ice.write('VOLT {}'.format(amplitude))
                # self.dev_ice.write('PER {}'.format(per))
                self.dev_ice.write('VOLT:HIGH {}'.format(high_level))
                self.dev_ice.write('VOLT:LOW {}'.format(low_level))
                self.dev_ice.write('VOLT:OFFS {}'.format(offSet))
        elif index_ == 2:
            if high_level-low_level ==amplitude:                
                self.dev_ice.write('FREQ {}'.format(ceter_frequency))
                self.dev_ice.write('VOLT {}'.format(amplitude))
                # self.dev_ice.write('PER {}'.format(per))
                self.dev_ice.write('VOLT:HIGH {}'.format(high_level))
                self.dev_ice.write('VOLT:LOW {}'.format(low_level))
                self.dev_ice.write('VOLT:OFFS {}'.format(offSet))
                self.dev_ice.write('FUNCtion:SQUare:WIDTh:HIGH {}'.format(hign_width))
                self.dev_ice.write('FUNCtion:SQUare:WIDTh:LOW {}'.format(low_width))
                self.dev_ice.write('FUNCtion:SQUare:DCYCle {}'.format(duty_cycle))
            else:
                compensation = amplitude/2
                high_level = compensation
                low_level = -(compensation)                 
                self.dev_ice.write('FREQ {}'.format(ceter_frequency))
                self.dev_ice.write('VOLT {}'.format(amplitude))
                # self.dev_ice.write('PER {}'.format(per))
                self.dev_ice.write('VOLT:HIGH {}'.format(high_level))
                self.dev_ice.write('VOLT:LOW {}'.format(low_level))
                self.dev_ice.write('VOLT:OFFS {}'.format(offSet))
                self.dev_ice.write('FUNCtion:SQUare:WIDTh:HIGH {}'.format(hign_width))
                self.dev_ice.write('FUNCtion:SQUare:WIDTh:LOW {}'.format(low_width))
                self.dev_ice.write('FUNCtion:SQUare:DCYCle {}'.format(duty_cycle))
        elif index_ == 3:
            if high_level-low_level ==amplitude:                
                self.dev_ice.write('FREQ {}'.format(ceter_frequency))
                self.dev_ice.write('VOLT {}'.format(amplitude))
                # self.dev_ice.write('PER {}'.format(per))
                self.dev_ice.write('VOLT:HIGH {}'.format(high_level))
                self.dev_ice.write('VOLT:LOW {}'.format(low_level))
                self.dev_ice.write('VOLT:OFFS {}'.format(offSet))
                self.dev_ice.write('FUNCtion:RAMP:TIMe:RISe {}'.format(rise_time))
                self.dev_ice.write('FUNCtion:RAMP:TIMe:FALL {}'.format(fall_time))
                self.dev_ice.write('FUNCtion:RAMP:SYMMetry {}'.format(symmetry))
            else:
                compensation = amplitude/2
                high_level = compensation
                low_level = -(compensation)                 
                self.dev_ice.write('FREQ {}'.format(ceter_frequency))
                self.dev_ice.write('VOLT {}'.format(amplitude))
                # self.dev_ice.write('PER {}'.format(per))
                self.dev_ice.write('VOLT:HIGH {}'.format(high_level))
                self.dev_ice.write('VOLT:LOW {}'.format(low_level))
                self.dev_ice.write('VOLT:OFFS {}'.format(offSet))
                self.dev_ice.write('FUNCtion:RAMP:TIMe:RISe {}'.format(rise_time))
                self.dev_ice.write('FUNCtion:RAMP:TIMe:FALL {}'.format(fall_time))
                self.dev_ice.write('FUNCtion:RAMP:SYMMetry {}'.format(symmetry))
        elif index_ == 4:
            if high_level-low_level ==amplitude:                
                self.dev_ice.write('FREQ {}'.format(ceter_frequency))
                self.dev_ice.write('VOLT {}'.format(amplitude))
                # self.dev_ice.write('PER {}'.format(per))
                self.dev_ice.write('VOLT:HIGH {}'.format(high_level))
                self.dev_ice.write('VOLT:LOW {}'.format(low_level))
                self.dev_ice.write('VOLT:OFFS {}'.format(offSet))
                self.dev_ice.write('FUNCtion:PULSe:WIDTh:HIGH {}'.format(hign_width))
                self.dev_ice.write('FUNCtion:PULSe:WIDTh:LOW {}'.format(low_width))
                self.dev_ice.write('FUNCtion:PULSe:DCYCle {}'.format(duty_cycle))
                self.dev_ice.write('FUNCtion:PULSe:ETIMe {}'.format(edge_time))
            else:
                compensation = amplitude/2
                high_level = compensation
                low_level = -(compensation)                 
                self.dev_ice.write('FREQ {}'.format(ceter_frequency))
                self.dev_ice.write('VOLT {}'.format(amplitude))
                # self.dev_ice.write('PER {}'.format(per))
                self.dev_ice.write('VOLT:HIGH {}'.format(high_level))
                self.dev_ice.write('VOLT:LOW {}'.format(low_level))
                self.dev_ice.write('VOLT:OFFS {}'.format(offSet))
                self.dev_ice.write('FUNCtion:PULSe:WIDTh:HIGH {}'.format(hign_width))
                self.dev_ice.write('FUNCtion:PULSe:WIDTh:LOW {}'.format(low_width))
                self.dev_ice.write('FUNCtion:PULSe:DCYCle {}'.format(duty_cycle))
                self.dev_ice.write('FUNCtion:PULSe:ETIMe {}'.format(edge_time))
        else:
            if high_level-low_level ==amplitude:                
                self.dev_ice.write('FREQ {}'.format(ceter_frequency))
                self.dev_ice.write('VOLT {}'.format(amplitude))
                # self.dev_ice.write('PER {}'.format(per))
                self.dev_ice.write('VOLT:HIGH {}'.format(high_level))
                self.dev_ice.write('VOLT:LOW {}'.format(low_level))
                self.dev_ice.write('VOLT:OFFS {}'.format(offSet))
            else:
                compensation = amplitude/2
                high_level = compensation
                low_level = -(compensation)                 
                self.dev_ice.write('FREQ {}'.format(ceter_frequency))
                self.dev_ice.write('VOLT {}'.format(amplitude))
                # self.dev_ice.write('PER {}'.format(per))
                self.dev_ice.write('VOLT:HIGH {}'.format(high_level))
                self.dev_ice.write('VOLT:LOW {}'.format(low_level))
                self.dev_ice.write('VOLT:OFFS {}'.format(offSet))