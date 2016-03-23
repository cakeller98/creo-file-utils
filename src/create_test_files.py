import os
import random
import shutil

filesList = ['test_d.drw', 'test_a.asm', 'test_p.prt', 'test_l.lay']
folderList = [r'model', r'model\level_1', r'model\level_1\level_2']

if os.path.exists(folderList[0]):
    shutil.rmtree(folderList[0])

for folder in folderList:
    os.makedirs(folder, exist_ok=True)

    for file in filesList:
        x = random.randint(1, 10)

        for ext in range(1, x):
            with open(r'{0}\{1}.{2}'.format(folder, file, ext), 'w') as f:
                f.write('{0}\n'.format(ext))
