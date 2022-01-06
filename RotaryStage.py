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
        self.stepPerDeg = 262144/360 #Conversion constant.
        self.stage.read_termination = '\r\n'
        self.stage.write('0ho0') #Home the motor.

    def move_to_pos(self, pos):
        '''Moves the motor to a set absolute position in degrees. \n
        Inputs:
            pos: The position in degrees to move the stage to.
        '''
        pass

    def get_pos(self):
        '''Returns current position, in degrees, of the motor.
        '''
        pass

    def close(self):
        '''Closes VISA connection.'''
        self.stage.close()