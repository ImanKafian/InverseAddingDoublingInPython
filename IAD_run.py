'''
About: Python script to run the IAD in batch.
Author: Iman Kafian-Attari
Date: 16.07.2021
Licence: MIT >> Check the IAD licence too.
version: 0.1
=========================================================
How to use:
1. Select the folder containing the executable IAD file.
2. Select a temporary folder to move your input files and run the IAD on them.
3. Select the output folder, it is better to be a folder other than your input and temp folders.
4. Select the input folder (for knowing how to make the header for IAD input files, check IAD_header_maker.py)
5. Specify the anisotropy scattering factor; it should be in the range of [-1, 1].
6. Now everything is set, set back, relax, and enjoy.
=========================================================
'''

print(__doc__)

import subprocess as sp
import os
import tkinter as tk
from tkinter import filedialog
import time
import shutil

root = tk.Tk()
root.withdraw()

iad_address = filedialog.askdirectory(parent=root, initialdir='C:\\', title='Select the folder containing iad.exe')
os.chdir(iad_address)
processing_dir_path = filedialog.askdirectory(parent=root, initialdir='C:\\', title='Select a temp folder for intermediate processing')

iad_output_dir = filedialog.askdirectory(parent=root, initialdir='C:\\', title='Select the output directory')
if not os.path.exists(f'{iad_output_dir}\\IAD-Output'):
    os.mkdir(f'{iad_output_dir}\\IAD-Output')

iad_input_dir = filedialog.askdirectory(parent=root, initialdir='C:\\', title='Select the input directory')
iad_input_files = sorted(os.listdir(iad_input_dir), key=lambda x: int("".join([i for i in x if i.isdigit()])))

g = float(input('Input the anisotropy scattering factor, g --> '))

for file in iad_input_files:
    shutil.copy2(f'{iad_input_dir}\\{file}', processing_dir_path)
    main_call = f'iad -M 100 -g {g} -p 100000 {processing_dir_path}\\{file}'
    proc_handle = sp.Popen(main_call)
    time.sleep(420.0)

for file in list(os.listdir(processing_dir_path)):
    if file.endswith('.rxt'):
        os.remove(f'{processing_dir_path}\\{file}')

for file in list(os.listdir(processing_dir_path)):
    if file.endswith('.txt'):
        shutil.move(f'{processing_dir_path}\\{file}', f'{iad_output_dir}\\IAD-Output')
