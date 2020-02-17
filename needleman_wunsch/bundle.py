# from colorama import Fore, Style
# import numpy as np
import ruler as r

import sys
fichier = sys.argv[1]

with open(fichier, 'r') as f:
    lignes = f.readlines()
    lignes = [l.rstrip() for l in lignes if len(l.rstrip()) != 0]
    k = 0
    for i in range(0, len(lignes)-1, 2):
        k+=1
        l1, l2 = lignes[i], lignes[i+1]
        a = r.Ruler(l1, l2)
        a.compute()
        top, bottom = a.report()
        print(f'====== example # {k} - distance = {int(a.distance)} \n{top} \n{bottom}')
        
#Pour le lancer depuis le terminal, taper:
#C:\ProgramData\Anaconda3\python.exe C:\Users\theop\OneDrive\Documents\Theophile\Etudes\Mines\INFO\evaluation_python_avance\needleman_wunsch\bundle.py C:\Users\theop\OneDrive\Documents\Theophile\Etudes\Mines\INFO\evaluation_python_avance\needleman_wunsch\DATASET.txt

