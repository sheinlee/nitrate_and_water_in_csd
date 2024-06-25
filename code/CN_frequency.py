import os
from ccdc.io import MoleculeReader
import numpy as np
import pandas as pd
from time import process_time


def find_cn_frequency(ELEMENT,filepath,A,writerA):
    mol_reader = MoleculeReader(filepath, format='identifiers')

def main():
    start = process_time()
    LIST_OF_ELEMENT = [
        'La', 'Ce','Pr','Nd','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu'
                        ]
    folder_path_list = ['water','nitrate','org_water','org_nitrate','org_nitrate_no_water','org_water_and_nitrate','org_water_no_nitrate']
    for folder_path in folder_path_list:
        # 如果文件夹不存在，创建它
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # writerA = pd.ExcelWriter('org_n_and_w_in_fs.xlsx')
    writerA = pd.ExcelWriter('analysis_CN_frequency.xlsx')
    A = np.zeros(shape=(4000, 10), dtype=object)
    B = np.zeros(shape=(10, 5), dtype=object)  # Updated shape to hold average and std

    
    for ELEMENT in LIST_OF_ELEMENT:
        filepath = './subset2_2023/subset2_' + ELEMENT + '.txt'
    #     file_path_list = ['water/water_'+ELEMENT+'.txt','org_water/org_water_'+ELEMENT+'.txt','org_water_no_nitrate/org_water_no_nitrate_'+ELEMENT+'.txt',
    #                 'org_water_and_nitrate/org_water_and_nitrate_'+ELEMENT+'.txt','nitrate/nitrate_'+ELEMENT+'.txt','org_nitrate/org_nitrate_'+ELEMENT+'.txt',
    #                 'org_nitrate_no_water/org_nitrate_no_water_'+ELEMENT+'.txt']
    #     for file_path in file_path_list:
    #         # 如果同名文件存在，删除它
    #         if os.path.exists(file_path):
    #             os.remove(file_path)

        find_cn_frequency(ELEMENT,filepath,A,writerA)

    writerA.save()
    # writerB.save()
    #processing time
    end = process_time()
    print('Running time: %s Seconds' % (end - start))


if __name__ == "__main__":
    main()