# caltech-nlo
# Purpose
This repository contains the instrument control code for several instruments used by the group, including optical spectrum analyzers, power meters, and motors. It also contains a subdirectory with the user manuals, and where applicable, programming guides for a selection of the instruments controlled here. Currently, there are classes to control
- ThorLabs PM100 Series Powermeters (`PowerMeter.py`)
- ThorLabs ELL14 Rotation Mount (`RotaryStage.py`)
- Yokogawa AQ6376 and AQ6374 Optical Spectrum Analyzers (`OSA.py`)
- Agilent 33220A Arbitrary Waveform Generator (`AWG_33220A.py`)
- Rigol DG4000 Series Arbitrary Waveform Generator (`AWG_DG4000.py`)
- Agilent E36300 DC Power Supply (`DCPS_E36300.py`)
- ThorLabs MDT693B Piezo Controller (`PC_MDT693B.py`)

There are also small test scripts designed to confirm the functionality of the libraries for some instruments. The code is written using PyVISA to interface with all of the instruments, and commands are sourced from the respective manuals or, in the case of the powermeter, from ThorLabs technical support. To run the code, you will need the PyVISA and NumPy packages. The OSA test script additionaly requires MatPlotLib.

# Using the Library
## Installation of Required Packages
In order to use the library, you will need an active Python installation, and the following packages:
- [PyVISA](https://pyvisa.readthedocs.io/en/latest/introduction/getting.html): A library allowing communication with instruments through the VISA library.
- [numpy](https://numpy.org/install/): Scientific computing with python.
- [matplotlib](https://matplotlib.org/stable/users/index.html): Data visualization with python.
- [wxPython](https://www.wxpython.org/pages/downloads/): Widgets and GUI with python.

It is also convenient to have the [iPython](https://ipython.org) package installed for running an interactive python interpreter in the command line.

## Finding the Device VISA Addresses
When using the library, all instruments are organized as classes with a common constructor that takes as arguments a PyVISA ResoueceManager object and a device ID, which is a string. This ID can vary between devices and can depend on the type of connection to the computer. The ResourceManager can list the IDs of all VISA resources with the following command
```python
import pyvisa
rm = pyvisa.ResourceManager()
rm.list_resources()
```
`list_resources()` returns a tuple of strings with the IDs of each connected instrument. Make a note of the addresses of each instrument you wish to control, and so long as you don't change their connections, their addresses will not change.

## Using an Instrument
We will use controlling the Rigol DG4000 Arbitrary Waveform Generator as an example. Once we know the VISA address of the instrument and have an active ResourceManager object, we can run the following code.
```python
from AWG_DG4000 import DG4000
dg_awg = DG4000(rm, "VISA_Address_Here")
```
Each instrument is designed to be used as a class, so once an instance has been assigned, we can run the methods as we would run them for any class. For instance, if we wanted to set the peak-to-peak voltage of the AWG to 3 Vpp, we would run
```python
dg_awg.set_voltage(3)
```
The methods for each instrument are documented in each class. When one is finished controlling the instrument, one should run the `close()` method for each active instrument. This will end the VISA connection between the instrument and the computer.
