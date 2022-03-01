import pyvisa

class MDT693B:
    '''A control class for the ThorLabs MDT693B Open-Loop Piezo Controller'''
    
    def __init__(self, rm:pyvisa.ResourceManager, id:str) -> None:
        '''This constructor initializes an instrument for remote control via Python.\n
        Arguments:
        - rm [`pyvisa.ResourceManager`]: The ResourceManager object that will establish a connection to the instrument.
        - id [`str`]: The VISA id of the instrument to connect to.
        '''
        self.pc = rm.open_resource(id)

    def set_all_volts(self, volt=0.0):
        '''This command will set the output voltage of all axes to the specified value, in volts.'''
        self.pc.write("allvoltage=" + str(volt))

    def set_voltage(self, channel:str, volt=0.0):
        '''Sets the output voltage of a specified channel to a given voltage.\n
        Arguments:
            - channel [`str`]: The axis to set the voltage of. This must be one of 'x', 'y', or 'z'.
            - volt [`float`]: The voltage (in volts) to output. The program will not check if this value is within\
                the range that the device can output.
        '''
        if channel not in ['x','y','z']:
            # Handles invalid channel input by doing nothing.
            pass
        else:
            self.pc.write(channel + "voltage=" + str(volt))
    
    def get_voltage(self, channel:str):
        '''Get the current voltage of a specific axis.\n
        Arguments:
            - channel [`str`]: The axis to set the voltage of. This must be one of 'x', 'y', or 'z'.
        '''
        if channel not in ['x','y','z']:
            # Handles invalid channel input by doing nothing.
            pass
        else:
            return self.pc.query_ascii_values(channel + "voltage?")

    def close(self):
        '''End pyvisa connection to instrument.'''
        self.pc.close()