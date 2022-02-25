# caltech-nlo
# Purpose
This repository contains the instrument control code for several instruments used by the group, including optical spectrum analyzers, power meters, and motors. It also contains a subdirectory with the user manuals, and where applicable, programming guides for a selection of the instruments controlled here. Currently, there are classes to control
- ThorLabs PM100 Series Powermeters (`PowerMeter.py`)
- ThorLabs ELL14 Rotation Mount (`RotaryStage.py`)
- Yokogawa AQ6376 and AQ6374 Optical Spectrum Analyzers (`OSA.py`)
- Agilent 33220A Arbitrary Waveform Generator (`AWG_33220A.py`)
- Rigol DG4000 Series Arbitrary Waveform Generator (`AWG_DG4000.py`)

There are also small test scripts designed to confirm the functionality of the libraries for some instruments. The code is written using PyVISA to interface with all of the instruments, and commands are sourced from the respective manuals or, in the case of the powermeter, from ThorLabs technical support. To run the code, you will need the PyVISA and NumPy packages. The OSA test script additionaly requires MatPlotLib.
