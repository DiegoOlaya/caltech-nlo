import pyvisa

class PowerMeter:
    def __init__(self, rm:pyvisa.ResourceManager, id:str):
        '''Initializes the VISA connection to the power meter and
        sets some default values. \n
        Inputs:
            rm: A pyvisa ResourceManager object.
            id: The VISA id string for the powermeter.
        '''
        self.instr = rm.open_resource(id)
        self.instr.read_termination = '\n'
        self.set_averaging(10)

    def set_averaging(self, num_meas):
        '''Sets the number of observations to average over. Argument num_meas 
        must be an integer.
        '''
        self.instr.write(":AVER " + str(num_meas))
    
    def read_pow(self):
        '''Reads a single power observation from the meter and 
        returns its value.
        '''
        self.instr.write('CONF:POW')
        self.instr.write(':INIT')
        pow = self.instr.query_ascii_values(':FETCH?')
        return pow

    def close(self):
        self.instr.close()