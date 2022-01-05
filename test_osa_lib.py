"""An example of using the OSA.py functions to collect traces from OSA."""

import OSA as osa
import pyvisa
import numpy as np
import matplotlib.pyplot as plt

rm = pyvisa.ResourceManager()

# 1 um GPIB address is 1. Can also check w/ VISA resource manager.
osa_1um = osa(rm, 'GPIB0::1::INSTR')
test_params = np.array([[1550, 1560, 'HIGH1'],[1560,1562,'HIGH3']])
# Set OSA to scan on trace A.
all_dat = np.array([[],[]])
for arr in test_params:
    osa.switch_trace('TRA')
    osa.config_scan(arr[0], arr[1], arr[2])
    dat = osa.sweep()
    all_dat = np.hstack((all_dat, dat))
# Plot the scan results.
plt.plot(all_dat[0], all_dat[1])
plt.show()