'''
About: Python script to write the header required for the IAD program in batch.
Author: Iman Kafian-Attari
Date: 16.07.2021
Licence: MIT
version: 0.1
=========================================================
How to use:
1. Select the input folder
2. Select the parent folder containing the input folder.
3. For each file:
    3.1. Input the sample thickness
    3.2. Input its refractive index
4. If you have stored your input dataset in more than one folder, after completion press 'Y' to repeat the process.

NOTE. Your input samples should be of the form: multiple rows x 3 columns!
      1st col: wavelength, 2nd col: reflectance, 3rd col: transmittance. Reflectance and transmittance in [0, 1]
NOTE. The remaining parameters are set according to an 150-mm single integrating sphere
      and the default values in the IAD manual document. If you are certain about these parameters,
      change line 57 accordingly.
NOTE. If you are using a constant thickness and refractive index,
      you can save time by relocating lines 54-55 to above line 52.
=========================================================
'''

print(__doc__)

import os
import tkinter as tk
from tkinter import filedialog
import shutil

root = tk.Tk()
root.withdraw()

condition = True
while condition == True:

    input_directory = filedialog.askdirectory(parent=root, initialdir=f'{main_directory}',
                                              title='Select the input directory')

    main_directory = filedialog.askdirectory(parent=root, initialdir='C:\\', title='Select the parent directory')
    if not os.path.exists(f'{main_directory}\\IAD_ready'):
        os.mkdir(f'{main_directory}\\IAD_ready')

    input_files = os.listdir(input_directory)
    input_files = list(input_files)
    for file in input_files:
        shutil.copy2(f'{input_directory}\\{file}', f'{main_directory}\\IAD_ready')

    temp_files = list(os.listdir(f'{main_directory}\\IAD_ready\\'))
    for file in temp_files:

        thickness = float(input(f'{file[:len(file)-4]} thickness (mm) --> '))
        refractiveIndex = float(input(f'{file[:len(file)-4]} refractive index --> '))

        header = [refractiveIndex, 1.5, float(f'{thickness}'), 1, 2, 0.96, 1, 150, 25.4, 12.7, 1, 0.96, 150, 25.4,
                  12.7, 1, 0.96, 2]

        file_to_open = f'{input_directory}\\{file}'
        with open(file_to_open, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            for i in range(len(header)+1):
                if i == 0:
                    f.write('IAD1' + '\n')
                elif i > 0 and i < len(header):
                    f.write(str(header[i-1]) + '\n')
                elif i == len(header):
                    f.write(str(header[i-1]) + '\n' + content)
                else:
                    print('Error\nExiting...')
                    exit()

    #   SETTING THE CONDITION FOR CONTINUING THE PROGRAM FOR OTHER PATELLAS
    check = input('Do you want to continue?(Y/N) --> ')
    if check == 'Y':
        condition = True
    elif check == 'N':
        condition = False
    else:
        print('Wrong input --> Exiting...')
        exit()
