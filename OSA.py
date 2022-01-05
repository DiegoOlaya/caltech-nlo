import pyvisa
import numpy as np

class OSA:
    def __init__(self, resourceMan: pyvisa.ResourceManager, visa_id) :
        '''Connects to OSA with VISA and sets data format to ASCII.
        Also specifies timeout as infinite and sets correct read termination
        character.
        '''
        self.osa = resourceMan.open_resource(visa_id)
        self.osa.timeout = float('+inf')
        self.osa.read_termination = '\n'
        self.osa.write(':FORMAT:DATA ASCII') # Sets output format.

    def switch_trace(self, new_trace) :
        '''Switches active trace to new_trace.\n
        Fixes the old active trace, then sets new_trace to the active trace and
        allows it to be written to.
        '''

        self.osa.write(':TRACE:ATTRIBUTE FIX') #Fix active trace
        self.osa.write('TRACE:STATE:' + new_trace + ' ON')
        self.osa.write(':TRACE:ATTRIBUTE:' + new_trace + ' WRITE') #Sets new_trace to active.

    def config_scan(self, lower: float, upper: float, sens) :
        '''Sets parameters for a wavelength scan.\n
        Inputs:
            lower: lower wavelength bound of scan in nm.
            upper: upper wavelength bound of scan in nm.
            sens: The scan sensitivity. Ex. 'HIGH3'
        '''
        
        self.osa.write(':SENSE:SENSE ' + sens) # Sets sensitivity.
        #Set wavelength bounds.
        self.osa.write(':SENSE:WAV:START ' + str(lower) + 'NM')
        self.osa.write(':SENSE:WAV:STOP ' + str(upper) + 'NM')

    def sweep(self) :
        '''Get sweep data from active trace using current sweep parameters and return the data.\n
        This method DOES NOT set sweep parameters. Those must be set prior to running this command.
        The required input is the OSA to sweep. Note that this method may take a long time
        to evaluate. Consider putting in a thread. \n
        Returns: 
            A numpy array containing the x,y data of the sweep. Assume dBm y scale. x is first row,
            y is second row.
        '''
        self.osa.write(':INIT:SMODE SINGLE') #Sets sweep mode to single.
        self.osa.write('*CLS') # Clears status buffer.
        self.osa.write(':INIT') # Starts sweep.
        # Collect and return data.
        trace = self.osa.query(':TRACE:ACTIVE?')
        dat_x = self.osa.query_ascii_values(':TRACE:X? ' + trace)
        print('Done x')
        dat_y = self.osa.query_ascii_values(':TRACE:y? ' + trace)
        print('Done y')
        return np.array([dat_x, dat_y])

    def abort(self) :
        '''Halts a sweep in progress.'''
        self.osa.write(':ABORT')    