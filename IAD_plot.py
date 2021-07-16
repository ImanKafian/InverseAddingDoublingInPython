'''
About: Python script to plot the IAD output in batch.
Author: Iman Kafian-Attari
Date: 16.07.2021
Licence: MIT
version: 0.1
=========================================================
How to use:
1. Select yur desired output folder.
2. Select the folder containing all IAD outputs as your input folder.
3. The program will plot the OPs per sample as a 1x2 figure.
=========================================================
'''

print(__doc__)

import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog
import shutil
import os

root = tk.Tk()
root.withdraw()

output_dir = filedialog.askdirectory(parent=root, initialdir='D:\\UEF\\Data\\',
                                     title='Select the output directory')
if not os.path.exists(f'{output_dir}\\IAD_plots'):
    os.mkdir(f'{output_dir}\\IAD_plots')
if not os.path.exists(f'{output_dir}\\IAD_plots_processing'):
    os.mkdir(f'{output_dir}\\IAD_plots_processing')
input_dir = filedialog.askdirectory(parent=root, initialdir='D:\\UEF\\Data\\',
                                                    title='Select the input directory')
file_list = list(os.listdir(input_dir))

collected_data = np.zeros((len(file_list), 381, 3))

for file in range(len(file_list)):
    shutil.copy2(f'{input_dir}\\{file_list[file]}', f'{output_dir}\\IAD_plots_processing')

for file in range(len(file_list)):

    dummy_list = []
    with open(f'{input_dir}\\{file_list[file]}') as f:
        for line in f:
            inner_list = [elt.strip() for elt in line.split('\t')]
            dummy_list.append(inner_list)

    new_list = dummy_list[44:]
    for i in range(len(new_list)):
        temp_ua = float(new_list[i][5])
        temp_us = float(new_list[i][6])

        if temp_ua < 0.000000001:
            temp_ua = 0
        if temp_us < 0.000000001:
            temp_us = 0

        collected_data[file][i][0] = float(new_list[i][0])
        collected_data[file][i][1] = float(new_list[i][5])
        collected_data[file][i][2] = float(new_list[i][6])

final_name = f'{file_list[0][:6]}-OPs'
np.save(f'{output_dir}\\IAD_plots\\{final_name}', collected_data)

temp_plot = collected_data

# Defining the Global properties for plots here
font_style = {'family': 'serif', 'weight': 'bold', 'size': 48} #
ua_colors = ['#343F56', '#810000', '#387C6D'] # Color codes used for Ua plots
us_colors = ['#125D98', '#F5A962', '#480032'] # Color codes used for Us codes
plt.rcParams['axes.facecolor'] = '#F6F5F5' # The color code for the plot background
line_styles = ['-', '--', '-.'] # Line styles used for plots
linewidth = 20 # Thickness of curves drwan on each plot

wn_range = collected_data.shape[1]

for file in range(len(file_list)):
        wn = []
        for i in range(wn_range):
            wn.append(temp_plot[file][i][0])
        ua = []
        for i in range(wn_range):
            ua.append(temp_plot[file][i][1])
        us = []
        for i in range(wn_range):
            us.append(temp_plot[file][i][2])

        plt.figure(file+1, figsize=(20, 40), dpi=300)
        plt.subplot(1, 2, 1)
        plt.plot(wn, ua, color=ua_colors[0], linestyle=line_styles[0], linewidth=linewidth, label='ua')
        plt.subplot(1, 2, 2)
        plt.plot(wn, us, color=us_colors[0], linestyle=line_styles[1], linewidth=linewidth, label='us\'')

        plt.xlabel('Wavelength distance (nm)', fontdict=font_style)
        plt.ylabel('Optical properties (mm-1)', fontdict=font_style)
        plt.xticks(fontfamily='serif', fontsize=48, fontweight='bold')
        plt.yticks(fontfamily='serif', fontsize=48, fontweight='bold')
        plt.grid(True)
        plt.title(f'{file_list[file][:-4]}-OPs')
        plt.tight_layout()

        plt.savefig(f'{file_list[file][:-4]}.png', dpi=300, transparent=False)

        plt.show(block=False)
        plt.pause(10)
