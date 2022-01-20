import pyvisa
import time
from RotaryStage import RotaryStage

rm = pyvisa.ResourceManager()
stage = RotaryStage(rm, "ASRL3::INSTR")

stage.move_to_pos(0)
print(stage.get_pos())
time.sleep(3)
stage.move_to_pos(135)
print(stage.get_pos())
time.sleep(3)
stage.move_to_pos(90)
print(stage.get_pos())
time.sleep(5)
stage.move_to_pos(45)
print(stage.get_pos())


stage.close()