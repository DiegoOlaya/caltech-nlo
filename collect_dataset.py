# Import Python packages.
import pyvisa
import numpy as np
import wx
import datetime
# Import instrument control classes.
from OSA import OSA
from PowerMeter import PowerMeter
from RotaryStage import RotaryStage

def get_path(wildcard:str, msg:str):
    '''Returns the path to a user selected file of type given by
    the argument wildcard. \n
    Arguments:
        wildcard: A string of form "*.txt" or similar, where * is a wildcard symbol, specifying
            the kind of file to look for.
        msg: A message to display to the user as the title of the dialog.
    Returns:
        (str): The path to the selected file. Returns None if cancelled.
    '''
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, msg, wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

def get_dir(msg:str):
    '''Returns the path to a user selected directory.
    '''
    app = wx.App(None)
    style = wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
    dialog = wx.DirDialog(None, msg, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

def get_usr_text(msg:str):
    '''Prompts the user for text input with the message passed as an argument.
    Returns a string with what the user typed.
    '''
    app = wx.App(None)
    dialog = wx.TextEntryDialog(None, msg)
    if dialog.ShowModal() == wx.ID_OK:
        ans = dialog.GetValue()
    else:
        ans = None
    dialog.Destroy()
    return ans

def sweepline(sweep_arr, osa:OSA):
    '''Performs the set of sweeps defined by the array sweep_arr on the specified OSA. \n
    Arguments:
        sweep_arr: An array of length 3n specifiying the parameters of each subsweep to take.
        osa: The OSA on which the sweeps are to be performed.
    Returns:
        (numpy array): The collected data of all of the sweeps in a numpy array (2xN array).
    '''
    num_sweeps = int(len(sweep_arr)/3)
    sweep_dat = np.array([[],[]])
    for i in range(num_sweeps):
        osa.config_scan(int(num_sweeps[i]), int(num_sweeps[i+1]), num_sweeps[i+2])
        data = osa.sweep()
        sweep_dat = np.hstack((sweep_dat, data))
    return sweep_dat

def write_to_file(data: np.ndarray, startPow, endPow, folder_path, header: str = None):
    '''Writes the collected data to a text file with extension .dat, and puts the
    starting and ending power in the header of the data file. \n
    Arguments:
        data: A 2xN numpy array of the sweep data to write. X is in nm and in the 0 row position, Y in dBm in the 1 row position.
        startPow: The power at which the measurement began.
        endPow: The power read by the meter after the measurement ended.
        folder_path: The file path to the folder in which the data should be saved.
        header (optional): A header to write to the beginning of the data file.
    Returns:
        (boolean): True on success.
    '''
    t_stamp = datetime.datetime.now()
    f_name = "sweep_" + str(t_stamp).replace(' ', '_') + ".dat"
    # Create file to write data to.
    file = open(folder_path + "\\" + f_name, "a")
    # Write a header to that file.
    file.writelines(["# Power at measurement start: " + startPow + "\n", "# Power at measurement end: " + endPow + "\n"])
    file.write("# Wavelength [nm]\tPower [dBm]\n")
    if header != None:
        header = header.splitlines()
        for line in header:
            file.write('# ' + line + '\n')
    # Write the data to the file.
    data = data.transpose()
    for pt in data:
        file.write(str(pt[0]) + "\t" + str(pt[1]) + "\n")
    # Close file and exit.
    file.close()
    return True

if __name__ ==  "__main__":
    # Set up connections to all instruments.
    rm = pyvisa.ResourceManager()
    rotStg = RotaryStage(rm, "ASRL3::INSTR") # TODO: Check this address before running.
    pwrMeter = PowerMeter(rm, 'USB::1::INSTR') # TODO: Change address to correct one before running.
    # Ask what OSA to use to collect data.
    osa_spec = get_usr_text("Specify what OSA to use. Type '1' for 1 um OSA, and '2' for 2 um OSA.")
    osa = None
    if int(osa_spec) == 1:
        osa = OSA(rm, 'GPIB0::1::INSTR') # TODO: Check the GPIB address (1um OSA) before running.
    else:
        osa = OSA(rm, "GPIB::30::INSTR") # TODO: Check the GPIB address (2um OSA) before running.

    # Define the set of motor positions to iterate over.
    pos_params = get_usr_text("Enter the motor start position, end position, \
        and number of steps between the two. Separate values by commas.")
    pos_params = ''.join(pos_params.split()).split(",") # Removes whitespace, then splits into array.
    positions_to_take = np.linspace(int(pos_params[0]), int(pos_params[1]), int(pos_params[2]))

    # Get the list of sweeps to perform.
    path = get_path(".txt", 'Open Sweep Config File')
    file = open(path, 'r')
    sweeps = file.readlines()
    file.close()

    #Get folder to write data files to.
    write_folder = get_dir("Select Folder to Save Data To")

    # Take the sweeps and write to files.
    if len(sweeps) == 1:
        sweep = ''.join(sweeps[0].split()).split(",")
        for pos in positions_to_take:
            rotStg.move_to_pos(pos)
            startPow = pwrMeter.read_pow() #Record laser power at start of sweep.
            data = sweepline(sweep, osa)
            endPow = pwrMeter.read_pow() #Record laser power at end of sweep.
            write_to_file(data, startPow, endPow, write_folder)
        pass
    else:
        for i in range(len(sweeps)):
            sweep = ''.join(sweeps[i].split()).split(',')
            rotStg.move_to_pos(positions_to_take[i])
            startPow = pwrMeter.read_pow() #Record laser power at start of sweep.
            data = sweepline(sweep, osa)
            endPow = pwrMeter.read_pow() #Record laser power at end of sweep.
            write_to_file(data, startPow, endPow, write_folder)
            
