import os
from ccdc.io import CrystalReader
import numpy as np
import pandas as pd
from collections import Counter
from time import process_time

start = process_time()

cry_reader = CrystalReader('CSD')

# 目标晶胞参数
target_lengths = [8.2115, 10.1867, 11.6511]
target_angles = [114.078, 98.370, 99.812]

# 允许误差范围
tolerance_length_less_accurate = 0.1
tolerance_length_more_accurate = 0.0001
tolerance_angle_less_accurate = 0.1
tolerance_angle_more_accurate = 0.001

for cry in cry_reader:
    print(cry.identifier)
    lengths = sorted(cry.cell_lengths)
    angles = sorted(cry.cell_angles)
    
    #less accurate search
    if all(abs(lengths[i] - target_lengths[i]) <= tolerance_length_less_accurate for i in range(3)) and \
       all(abs(angles[i] - target_angles[i]) <= tolerance_angle_less_accurate for i in range(3)):
        with open('less_accurate_cell_list.txt', 'a') as f:
            f.write(f'{cry.identifier}\n')
        
    #more accurate search
    if all(abs(lengths[i] - target_lengths[i]) <= tolerance_length_more_accurate for i in range(3)) and \
       all(abs(angles[i] - target_angles[i]) <= tolerance_angle_more_accurate for i in range(3)):
        with open('more_accurate_cell_list.txt', 'a') as f:
            f.write(f'{cry.identifier}\n')

# processing time
end = process_time()
print('Running time: %s Seconds' % (end - start))
