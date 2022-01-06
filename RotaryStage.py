import pyvisa

class RotaryStage:  
    def __init__(self, rm:pyvisa.ResourceManager, address) -> None:
        '''Initializes the VISA connection to the rotary stage and
        sets some default values. \n
        Inputs:
            rm: A pyvisa ResourceManager object.
            id: The VISA id string for the powermeter.
        '''
        self.stage = rm.open_resource(address)
        self.stepPerRev = 262144
        self.stage.read_termination = '\r\n'
        self.stage.write('0ho0') #Home the motor.