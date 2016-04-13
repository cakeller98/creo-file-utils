import os
import random
import shutil

filesList = ['test_d_a.drw', 'test_d_b.drw', 'test_a_a.asm', 'test_a_b.asm', 'test_p_a.prt', 'test_p_b.prt',
             'test_l_a.lay', 'test_l_b.lay']
folderList = [r'model', r'model\level_1', r'model\level_1\level_2']

if os.path.exists(folderList[0]):
    shutil.rmtree(folderList[0])

for folder in folderList:
    os.makedirs(folder, exist_ok=True)

    for file in filesList:
        x = random.randint(1, 10)

        for ext in range(1, x):
            with open(r'{0}\{1}.{2}'.format(folder, file, ext), 'w') as f:
                f.write(r'{0}\{1}.{2}'.format(folder, file, ext))
