import pyvisa

class E36300:
    '''A control class for Keysight E36300 series Programmable DC Power Supplies.'''
    
    def __init__(self, rm:pyvisa.ResourceManager, id:str) -> None:
        '''This constructor initializes an instrument for remote control via Python.\n
        Arguments:
        - rm [`pyvisa.ResourceManager`]: The ResourceManager object that will establish a connection to the instrument.
        - id [`str`]: The VISA id of the instrument to connect to.
        '''
        self.dcps = rm.open_resource(id)

    # Voltage control functions.
    def set_voltage(self, volt:float, chnl:str):
        '''This function sets the voltage to be output from a specified channel or channels. Note that this function \
            does NOT prevent setting the voltage to be above the limits supported by the instrument.\n
        Arguments:
            - volt [`float`]: The voltage, in volts, to output.
            - chnl [`str`]: The channel specification. This is of form '(@1)' for channel 1, '(@1,3)' for channels 1 \
                and 3, or '(@1:3)' for channels 1-3. The single quotes should not be included in the argument.
        '''
        self.dcps.write("VOLT " + str(volt) + ", " + chnl)

    def get_set_voltage(self, chnl:str):
        '''Returns the user-defined voltage set-point for the given channel or channels.
        Arguments:
            - chnl [`str`]: The channel specification. This is of form '(@1)' for channel 1, '(@1,3)' for channels 1 \
                and 3, or '(@1:3)' for channels 1-3. The single quotes should not be included in the argument.
        '''
        return self.dcps.query_ascii_values("VOLT? " + chnl)

    def query_output_voltage(self, chnl:str):
        '''Returns the voltage currently being output for the given channel or channels.
        Arguments:
            - chnl [`str`]: The channel specification. This is of form '(@1)' for channel 1, '(@1,3)' for channels 1 \
                and 3, or '(@1:3)' for channels 1-3. The single quotes should not be included in the argument.
        '''
        return self.dcps.query_ascii_values("MEAS:VOLT? " + chnl)

    # Current control functions.
    def set_current(self, curr:float, chnl:str):
        '''This function sets the current to be output from a specified channel or channels. Note that this function \
            does NOT prevent setting the current to be above the limits supported by the instrument.\n
        Arguments:
            - curr [`float`]: The current, in amps, to output.
            - chnl [`str`]: The channel specification. This is of form '(@1)' for channel 1, '(@1,3)' for channels 1 \
                and 3, or '(@1:3)' for channels 1-3. The single quotes should not be included in the argument.
        '''
        self.dcps.write("CURRENT " + str(curr) + ", " + chnl)

    def get_set_current(self, chnl):
        '''Returns the user-defined current set-point for the given channel or channels.
        Arguments:
            - chnl [`str`]: The channel specification. This is of form '(@1)' for channel 1, '(@1,3)' for channels 1 \
                and 3, or '(@1:3)' for channels 1-3. The single quotes should not be included in the argument.
        '''
        return self.dcps.query_ascii_values("CURRENT? " + chnl)

    def query_output_current(self, chnl):
        '''Returns the current currently being output for the given channel or channels.
        Arguments:
            - chnl [`str`]: The channel specification. This is of form '(@1)' for channel 1, '(@1,3)' for channels 1 \
                and 3, or '(@1:3)' for channels 1-3. The single quotes should not be included in the argument.
        '''
        return self.dcps.query_ascii_values("MEAS:CURRENT? " + chnl)

    #Output control function.
    def set_chnl_output(self, chnl='(@1:3)', on=False):
        '''This function determines the output state of the given channels. The default state of the function is to \
            turn all output channels off.\n
        Arguments:
            - chnl [`str`]: The channel specification. This is of form '(@1)' for channel 1, '(@1,3)' for channels 1 \
                and 3, or '(@1:3)' for channels 1-3. The single quotes should not be included in the argument.
            - on [`bool`]: Defaults to `False`. Enables output if set to `True`, disables otherwise.
        '''
        if on:
            self.dcps.write("OUTPUT ON, " + chnl)
        else:
            self.dcps.write("OUTPUT OFF, " + chnl)

    def close(self):
        '''Closes VISA connection to device.'''
        self.dcps.close()