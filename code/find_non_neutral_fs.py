#find net charge of first shell(component with Ln) 

import os
from ccdc.io import MoleculeReader
import numpy as np
import pandas as pd
from time import process_time


def find_non_neutral_fs(ELEMENT,key,B,writerB):
    count = -1
    filepath = f'./{key}/{key}_' + ELEMENT + '.txt'
    mol_reader = MoleculeReader(filepath, format='identifiers')
    count_neutral_fs = 0
    count_non_neutral_fs = 0  
    NC_values = []  #NET CHARGE
    NC_values_in_non_neutral= []
    for mol in mol_reader:
        count += 1
        B[count, 0] = mol.identifier

        try:
            mol.assign_bond_types()
            mol.add_hydrogens()
        except RuntimeError as e:
            print(f"Error adding hydrogens to molecule {mol.identifier}: {e}")
            continue

        find_ELEMENT = False
        # mol_is_organic = False
        for com in mol.components:
            for atom in com.atoms:
                if atom.atomic_symbol == ELEMENT:
                    find_ELEMENT = True
                    NC = com.formal_charge
                    B[count,1] = com.formal_charge
                    NC_values.append(NC)
                    if com.formal_charge == 0: 
                        count_neutral_fs +=1
                        with open(f'neutral_fs_{key}/neutral_fs_{key}_'+ELEMENT+'.txt','a') as f:
                            f.write(mol.identifier + '\n')
                    if com.formal_charge !=0: 
                        count_non_neutral_fs +=1
                        NC_values_in_non_neutral.append(NC)
                        with open(f'non_neutral_fs_{key}/non_neutral_fs_{key}_'+ELEMENT+'.txt','a') as f:
                            f.write(mol.identifier + '\n')
                if find_ELEMENT:break
            if find_ELEMENT: break

    B[0,3]=count_neutral_fs
    B[0,4]=count_non_neutral_fs
    B[0,6] = np.mean(NC_values)
    B[0,7] = np.std(NC_values)
    B[0,8] = np.mean(NC_values_in_non_neutral)
    B[0,9] = np.std(NC_values_in_non_neutral)    


    pd.DataFrame(B).to_excel(writerB, sheet_name=ELEMENT, float_format='%.5f') 



def main():
    start = process_time()
    LIST_OF_ELEMENT = [
        'La', 
        'Ce','Pr','Nd','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu'
                        ]
    key1 = 'nitrate'
    key2 = 'water'
    
    folder_path_list = ['non_neutral_fs_nitrate','non_neutral_fs_water','neutral_fs_nitrate','neutral_fs_water']
    for folder_path in folder_path_list:
        # 如果文件夹不存在，创建它
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # writerA = pd.ExcelWriter('non_neutral_fs_nitrate.xlsx')
    writerB = pd.ExcelWriter('analysis_non_neutral_fs_nitrate.xlsx')
    # writerC = pd.ExcelWriter('non_neutral_fs_water.xlsx')
    writerD = pd.ExcelWriter('analysis_non_neutral_fs_water.xlsx')
    # A = np.zeros(shape=(1300, 10), dtype=object)
    B = np.zeros(shape=(1300, 10), dtype=object)  # count (non) neutral fs in nitrate
    # C = np.zeros(shape=(1300, 10), dtype=object)
    D = np.zeros(shape=(1300, 10), dtype=object)  # count (non) neutral fs in nitrate

    
    for ELEMENT in LIST_OF_ELEMENT:
        key1 = 'nitrate'
        key2 = 'water'
        # filepath1 = './nitrate/nitrate_' + ELEMENT + '.txt'
        # filepath2 = './water/water_' + ELEMENT + '.txt'
        file_path_list = ['non_neutral_fs_nitrate/non_neutral_fs_nitrate_'+ELEMENT+'.txt',
        'non_neutral_fs_water/non_neutral_fs_water_'+ELEMENT+'.txt',
        'neutral_fs_nitrate/neutral_fs_nitrate_'+ELEMENT+'.txt',
        'neutral_fs_water/neutral_fs_water_'+ELEMENT+'.txt']
        for file_path in file_path_list:
            # 如果同名文件存在，删除它
            if os.path.exists(file_path):
                os.remove(file_path)

        # find_non_neutral_fs(ELEMENT,filepath1,A,B,writerA,writerB)
        # find_non_neutral_fs(ELEMENT,filepath1,C,D,writerA,writerB)
        find_non_neutral_fs(ELEMENT,key1,B,writerB)
        find_non_neutral_fs(ELEMENT,key2,D,writerD)

    # writerA.save()
    writerB.save()
    
    # writerC.save()
    writerD.save()
    #processing time
    end = process_time()
    print('Running time: %s Seconds' % (end - start))


if __name__ == "__main__":
    main()