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
        self.pos = 0 #State variable for motor position.

    def move_to_pos(self, pos):
        '''Moves the motor to a set absolute position in degrees. \n
        Inputs:
            pos: The position in degrees to move the stage to.
        '''
        pos_in_steps = int(self.stepPerDeg * (pos/2))
        hex_pos = "{0:0{1}x}".format(pos_in_steps, 8) #Converts decimal position to 8-digit hexadecimal.
        stPos = self.stage.query("0ma" + hex_pos)
        #Convert position hex string to degrees. Motor seems to be off by factor of 2.
        self.pos = 2 * self.calc_pos(stPos[2:])

    def calc_pos(self, posHex, bits=32):
        '''Calculates the position in degrees from the hexadecimal step number
        returned by the motor after it finishes moving.'''
        value = int(posHex, 16)
        if value & (1 << (bits-1)):
            value -= 1 << bits
        return value / self.stepPerDeg

    def get_pos(self):
        '''Returns current position, in degrees, of the motor.
        '''
        return self.pos

    def close(self):
        '''Closes VISA connection.'''
        self.stage.close()