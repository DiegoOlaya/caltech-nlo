import numpy as np
import pyvisa

class AWG_33220A:
    def __init__(self, rm: pyvisa.ResourceManager, id:str) -> None:
        self.awg = rm.open_resource(id)
        self.awg.write("VOLT:UNIT VPP")
        self.awg.timeout = 10000
    
    def calc_time(self, freq1:int, freq2:int) -> float:
        '''Returns the time period necessary for the sum of the frequencies to complete 
        one repeatable oscillation.\n
        Arguments:
            freq1: The frequency (in Hz) of the first sine wave.
            freq2: The frequency (in Hz) of the second sine wave.
        Return:
            (float): The time (in s) corresponding to one period.
        '''
        (m1, m2) = (float(freq1)/freq2).as_integer_ratio()
        return m1 / freq1

    def calc_points(self, freq1, freq2):
        '''Calculates the amplitudes and the required frequency for periodicity \
        given two frequencies.\n
        This method also sets two state variables, self.pts, which contains the amplitudes, \
        and self.freq which contains the frequency of oscillation of the arbitrary waveform.\n
        Arguments:
            freq1: The frequency (in Hz) of the first sine wave.
            freq2: The frequency (in Hz) of the second sine wave.
        Return:
            (float tuple): First argument is the set of amplitude points, second is \
            the frequency of the arbitrary waveform.
        '''
        t_end = self.calc_time(freq1, freq2)
        t = np.linspace(0, t_end, 65536)
        self.pts = 0.5*(np.sin(2*np.pi*freq1*t)+np.sin(2*np.pi*freq2*t))
        self.freq = 1/t_end
        return (self.pts, self.freq)
    
    def write_pts(self, pts=None, name="LASER_REF"):
        '''Writes the data points to the AWG's non-volatile memory under the provided name. \n
        Arguments:
            pts (optional): The points to load into memory. If not provided, the system will use \
                the points stored as an instance variable.
            name (optional): The name of the waveform. Defaults to 'LASER_REF' if no name \
                is provided.
        '''
        if pts == None:
            pts = self.pts
        pass
        pts_str = ', '.join(map(str, pts))
        self.awg.write("DATA VOLATILE, " + pts_str)
        self.awg.write("DATA:COPY " + name)

    def output_waveform(self, name="LASER_REF"):
        self.awg.write("FUNC:USER " + name)
        self.awg.write("FUNC USER")
        self.awg.write("OUTPUT ON")

    def stop_output(self):
        self.awg.write("OUTPUT OFF")

    def set_wave_params(self, voltage, freq=None, offset=0, fUnits="Hz"):
        '''Set all the parameters at once in a single method.
        '''
        if freq == None:
            freq = self.freq
        self.set_freq(freq, fUnits)
        self.set_volt_offset(offset)
        self.set_voltage(voltage)
    
    def set_voltage(self, voltage):
        '''Set the voltage of the AWG in V_pp.
        '''
        self.awg.write("VOLT " + str(voltage) + " VPP")
    
    def get_voltage(self):
        return self.query_ascii_values("VOLT?")
    
    def set_freq(self, freq, units="Hz"):
        '''Sets the frequency of oscillation for the waveform. Default units are Hz.
        Arguments:
            freq: The frequency of oscillation for the waveform.
            units: The units for frequency. Can be 'Hz', 'KHz', or 'MHz'. 'Hz' is default.
        '''
        self.awg.write("FREQ " + str(freq) + " " + units)
    
    def get_freq(self):
        self.awg.query_ascii_values("FREQ?")

    def set_volt_offset(self, offset=0):
        '''Define a voltage offset in volts. Default is 0.
        '''
        self.awg.write("VOLT:OFFSET " + str(offset))
    
    def get_volt_offset(self):
        return self.awg.query_ascii_values("VOLT:OFFSET?")

    def close(self):
        self.awg.close()
