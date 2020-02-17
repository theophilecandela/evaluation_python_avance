import numpy as np
from colorama import Fore, Style

    # def red_text(text):
    #     return f"{Fore.RED}{text}{Style.RESET_ALL}"
    # 
    # # que l'on peut utiliser comme ceci
    # message = "def"
    # print(f"abc{red_text(message)}ghi")
    
    
    # indice bundle:
    # import sys"
    # sys.argv['budle.py', 'DATASET']
    # 
    # ou alors:
    # voir argparse
    
    
class Ruler:
    #pour modifier coût de substitution, deux méthodes: 
        #soit on veut tout modifier: alors on fournit en entrée la matrice de s coût (un dictionnaire de dictionnaire). 
        #soit on veut modifier la valeur de substitution pour un/plusieurs couple(s) donné(s). On peut alors fournir une liste de tuples (lettre_1, lettre_2, coût). La matrice de substitution est à priori symétrique. Les autres couples restent à un coût de subtitution 1. 
        
        #--> OU ALORS l'utilisateur doit dans les deux cas fournir un dictionnaire de dictionnaires? 
        #dict[lettre_1][lettre_2] = coût
    '''On ne construit la matrice que dans le cas où elle est fournie par l'utilisateur'''
    
    @staticmethod
    def build_matrix(liste):
        dico = {}
        for couple in liste:
            lettre_1, lettre_2, cout = couple
            lettre_1, lettre_2 = min(lettre_1, lettre_2), max(lettre_1, lettre_2)
            if lettre_1 in dico.keys():
                dico[lettre_1][lettre_2] = cout
            else:
                dico[lettre_1] = {lettre_2: cout}
        return dico
        
    @staticmethod
    def red_text(text):
        return f'{Fore.RED}{text}{Style.RESET_ALL}'
        
    
    
    def __init__(self, mot_1, mot_2, cout_substitution = []):
        #cout_substitution: dictionnaire {lettre_1: {lettre_2: cout1_2, ...},...}
        #ou [(lettre_1, lettre_2, cout), ...]
        self.top= mot_1
        self.bottom= mot_2
        self.distance = np.inf
        self.matrice = False
        self.couts = {}
        
        if type(cout_substitution) == dict:
            self.matrice = True
            self.couts = cout_substitution
            
        elif type(cout_substitution) == list:
            if len(cout_substitution) == 0:
                self.matrice = False
                self.couts = []
            elif type(cout_substitution[0]) != tuple:
                raise TypeError('le format des valeurs de substitution ne correspond pas à ce qui est attendu')
            else:
                self.matrice = True
                self.couts = Ruler.build_matrix(cout_substitution)
        else:
            raise TypeError('le format des valeurs de substitution ne correspond pas à ce qui est attendu')
       
            
            
    def report(self):
        #On colore les lettres et on renvoie les chaines prêtes à être affichées
        #fonctionne correctement
        top = ''
        bot = ''
        for lettre_1, lettre_2 in zip(self.top, self.bottom):
            if lettre_1 != lettre_2:
                if lettre_1 == '=':
                    lettre_1 = f'{Ruler.red_text(lettre_1)}'
                elif lettre_2 == '=':
                    lettre_2 = f'{Ruler.red_text(lettre_2)}'
                else:
                    lettre_1 = f'{Ruler.red_text(lettre_1)}'
                    lettre_2 = f'{Ruler.red_text(lettre_2)}'
                    
            top = top + lettre_1
            bot = bot + lettre_2
            
        return top, bot
    
    @staticmethod
    def cout(matrice, couts, lettre_1, lettre_2):
        d = 0 
        if lettre_1 != lettre_2:
            l1, l2 = min(lettre_1, lettre_2), max(lettre_1, lettre_2)
            if matrice:
                if l1 in couts.keys():
                    if l2 in couts[l1].keys():
                        d = couts[l1][l2]
            else:
                    d = 1
        return d
        
        
        
        
    def compute(self):
        n = len(self.top)
        m = len(self.bottom)
        p = min(n,m)
        distances = np.zeros((n,m))
        
        for k in range(p):
            j = m-1-k
            for i in range(n-1-k,-1,-1):
                
                c_ij = Ruler.cout(self.matrice, self.couts, self.top[i],self.bottom[j])
                
                #pb indice
                if (j < (m-2) and i < (n-2) and j > 0 and i>0) or (i,j) == (0,0):
                    plus_court = distances[i+1][j+1] #pb indice m = n = 1
                    for v in range(i+1, n):
                        cout_saut = 0
                        for p in range(i+1, v):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.top[p], '=')
                        plus_court = min(plus_court, (distances[v][j+1] + cout_saut))
                        
                    for l in range(j+1, m):
                        cout_saut = 0
                        for p in range(j+1, l):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.bottom[p], '=')
                        plus_court = min(plus_court, (distances[i+1][l] + cout_saut))
                    
                    distances[i][j] = c_ij + plus_court
                
                elif j == (m-1) and i == (n-1):
                    distances[i][j] = c_ij
                    
                    #Que faire de ça??? Peut être le stocver dans une variable annexe
                    #Ruler.cout(self.matrice, self.couts, self.bottom[j], '=') + Ruler.cout(self.matrice, self.couts, self.top[i], '='))
                elif j == (m-2) and i == (n-2):
                    distances[i][j] = c_ij + min(distances[i+1, j+1], Ruler.cout(self.matrice, self.couts, self.bottom[j], '=') + Ruler.cout(self.matrice, self.couts, self.top[i], '=')) 
                    
                elif j == (m-1) and i == (n-2):
                    distances[i][j] = c_ij + Ruler.cout(self.matrice, self.couts, self.top[i+1],'=')
                    
                elif j ==(m-2) and i ==(n-1):
                    distances[i][j] = c_ij + Ruler.cout(self.matrice, self.couts, self.bottom[j+1],'=')
                    
                elif j == 0 and i == (n-1):
                    cout_fin = 0
                    for l in range(j+1, m): #On complete top par des '='
                        cout_fin += Ruler.cout(self.matrice, self.couts, self.bottom[l], '=')
                    cout_debut = 0
                    for p in range(0, i): #On complete top par des '='
                        cout_debut += Ruler.cout(self.matrice, self.couts, self.top[p], '=')
                    distances[i][j] = c_ij + cout_fin + cout_debut
                    
                    
                elif j == (m-1) and i == 0:
                    cout_fin = 0
                    for l in range(i+1, m): #On complete top par des '='
                        cout_fin += Ruler.cout(self.matrice, self.couts, self.top[l], '=')
                    cout_debut = 0
                    for p in range(0, j): 
                        cout_debut += Ruler.cout(self.matrice, self.couts, self.bottom[p], '=')
                    distances[i][j] = c_ij + cout_fin + cout_debut
                    
                elif j == 0 and i == (n-2):
                    plus_court = distances[i+1][j+1]
                    for l in range(j+1, m):
                        cout_saut = 0
                        for p in range(j+1, l):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.bottom[p], '=')
                        plus_court = min(plus_court, (distances[i+1][l] + cout_saut))
                    cout_debut = 0
                    for p in range(0, i): 
                        cout_debut += Ruler.cout(self.matrice, self.couts, self.top[p], '=')
                    distances[i][j] = c_ij + plus_court + cout_debut
                    
                elif j == (m-2) and i ==0:
                    plus_court = distances[i+1][j+1]
                    for v in range(i+1, n):
                        cout_saut = 0
                        for p in range(i+1, v):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.top[p], '=')
                        plus_court = min(plus_court, (distances[v][j+1] + cout_saut))
                    cout_debut = 0
                    for p in range(0, j): 
                        cout_debut += Ruler.cout(self.matrice, self.couts, self.bottom[p], '=')
                    distances[i][j] = c_ij + plus_court + cout_debut
                    
                elif j == 0:
                    plus_court = distances[i+1][j+1]
                    for v in range(i+1, n):
                        cout_saut = 0
                        for p in range(i+1, v):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.top[p], '=')
                        plus_court = min(plus_court, (distances[v][j+1] + cout_saut))
                        
                    for l in range(j+1, m):
                        cout_saut = 0
                        for p in range(j+1, l):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.bottom[p], '=')
                        plus_court = min(plus_court, (distances[i+1][l] + cout_saut))
                    
                    cout_debut = 0
                    for p in range(0, i): 
                        cout_debut += Ruler.cout(self.matrice, self.couts, self.top[p], '=')
                    distances[i][j] = c_ij + plus_court + cout_debut
                        
                elif i == 0:
                    plus_court = distances[i+1][j+1]
                    for v in range(i+1, n):
                        cout_saut = 0
                        for p in range(i+1, v):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.top[p], '=')
                        plus_court = min(plus_court, (distances[v][j+1] + cout_saut))
                        
                    for l in range(j+1, m):
                        cout_saut = 0
                        for p in range(j+1, l):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.bottom[p], '=')
                        plus_court = min(plus_court, (distances[i+1][l] + cout_saut))
                    cout_debut = 0
                    for p in range(0, j): 
                        cout_debut += Ruler.cout(self.matrice, self.couts, self.bottom[p], '=')
                    distances[i][j] = c_ij + plus_court + cout_debut   
                        
                elif i == (n-1): #and j < (m-2)
                    cout_fin = 0
                    for l in range(j+1, m): #On complete top par des '='
                        cout_fin += Ruler.cout(self.matrice, self.couts, self.bottom[l], '=')
                    distances[i][j] = c_ij + cout_fin
                    
                elif j == m-1: #and i< (n-2)
                    cout_fin = 0
                    for l in range(i+1, n):
                        cout_fin += Ruler.cout(self.matrice, self.couts, self.top[l], '=')
                    distances[i][j] = c_ij + cout_fin
                    
                elif j == (m-2) : #and i< (n-2)
                    plus_court = distances[i+1][j+1]
                    for v in range(i+1, n):
                        cout_saut = 0
                        for p in range(i+1, v):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.top[p], '=')
                        plus_court = min(plus_court, (distances[v][j+1] + cout_saut))
                        
                    distances[i][j] = c_ij + plus_court
                    
                    
                    
                    
                elif i ==(n-2): #and j < (m-2)
                    plus_court = distances[i+1][j+1]
                    for l in range(j+1, m):
                        cout_saut = 0
                        for p in range(j+1, l):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.bottom[p], '=')
                        plus_court = min(plus_court, (distances[i+1][l] + cout_saut))
                    
                    distances[i][j] = c_ij + plus_court
                    
              
                    
            i = n-1-k
            for j in range(m-2-k,-1,-1):# m-1-k déjà calculé
                
                
                c_ij = Ruler.cout(self.matrice, self.couts, self.top[i],self.bottom[j])
                
                if (j < (m-2) and i < (n-2) and j > 0 and i>0) or (i,j) == (0,0):
                    plus_court = distances[i+1][j+1]
                    for k in range(i+1, n):
                        cout_saut = 0
                        for p in range(i+1, k):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.top[p], '=')
                        plus_court = min(plus_court, (distances[k][j+1] + cout_saut))
                        
                    for l in range(j+1, m):
                        cout_saut = 0
                        for p in range(j+1, l):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.bottom[p], '=')
                        plus_court = min(plus_court, (distances[i+1][l] + cout_saut))
                    
                    distances[i][j] = c_ij + plus_court
                
                elif j == (m-2) and i == (n-2):
                    distances[i][j] = c_ij + min(distances[i+1, j+1], Ruler.cout(self.matrice, self.couts, self.bottom[j], '=') + Ruler.cout(self.matrice, self.couts, self.top[i], '=')) 
                    
                elif j ==(m-2) and i ==(n-1):
                    distances[i][j] = c_ij + Ruler.cout(self.matrice, self.couts, self.bottom[j+1],'=')
                    
                elif j == 0 and i == (n-1):
                    cout_fin = 0
                    for l in range(j+1, m): #On complete top par des '='
                        cout_fin += Ruler.cout(self.matrice, self.couts, self.bottom[l], '=')
                    cout_debut = 0
                    for p in range(0, i): #On complete top par des '='
                        cout_debut += Ruler.cout(self.matrice, self.couts, self.top[p], '=')
                    distances[i][j] = c_ij + cout_fin + cout_debut
                    
                elif j == 0 and i == (n-2):
                    plus_court = distances[i+1][j+1]
                    for l in range(j+1, m):
                        cout_saut = 0
                        for p in range(j+1, l):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.bottom[p], '=')
                        plus_court = min(plus_court, (distances[i+1][l] + cout_saut))
                    cout_debut = 0
                    for p in range(0, i): 
                        cout_debut += Ruler.cout(self.matrice, self.couts, self.top[p], '=')
                    distances[i][j] = c_ij + plus_court + cout_debut
                    
                elif j == (m-2) and i ==0:
                    plus_court = distances[i+1][j+1]
                    for k in range(i+1, n):
                        cout_saut = 0
                        for p in range(i+1, k):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.top[p], '=')
                        plus_court = min(plus_court, (distances[k][j+1] + cout_saut))
                    cout_debut = 0
                    for p in range(0, j): 
                        cout_debut += Ruler.cout(self.matrice, self.couts, self.bottom[p], '=')
                    distances[i][j] = c_ij + plus_court + cout_debut
                    
                elif j == 0:
                    plus_court = distances[i+1][j+1]
                    for k in range(i+1, n):
                        cout_saut = 0
                        for p in range(i+1, k):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.top[p], '=')
                        plus_court = min(plus_court, (distances[k][j+1] + cout_saut))
                        
                    for l in range(j+1, m):
                        cout_saut = 0
                        for p in range(j+1, l):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.bottom[p], '=')
                        plus_court = min(plus_court, (distances[i+1][l] + cout_saut))
                    
                    cout_debut = 0
                    for p in range(0, i): 
                        cout_debut += Ruler.cout(self.matrice, self.couts, self.top[p], '=')
                    distances[i][j] = c_ij + plus_court + cout_debut
                        
                elif i == 0:
                    plus_court = distances[i+1][j+1]
                    for k in range(i+1, n):
                        cout_saut = 0
                        for p in range(i+1, k):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.top[p], '=')
                        plus_court = min(plus_court, (distances[k][j+1] + cout_saut))
                    
                elif i == (n-1): #and j < (m-2)
                    cout_fin = 0
                    for l in range(j, m): #On complete top par des '='
                        cout_fin += Ruler.cout(self.matrice, self.couts, self.bottom[l], '=')
                    distances[i][j] = c_ij + cout_fin
                    
                elif j == (m-2) : #and i< (n-2)
                    plus_court = distances[i+1][j+1]
                    for k in range(i+1, n):
                        cout_saut = 0
                        for p in range(i+1, k):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.top[p], '=')
                        plus_court = min(plus_court, (distances[k][j+1] + cout_saut))
                    distances[i][j] = c_ij + plus_court
                    
                    
                elif i ==(n-2): #and j < (m-2)
                    for l in range(j+1, m):
                        cout_saut = 0
                        for p in range(j+1, l):
                            cout_saut += Ruler.cout(self.matrice, self.couts, self.bottom[p], '=')
                        plus_court = min(plus_court, (distances[i+1][l] + cout_saut))
                    
                    distances[i][j] = c_ij + plus_court
                
                
                
                
        #On reconstruit les mots et on récupère la distance minimale
        self.distance = min(min(distances[0,:]), min(distances[:,0]))
        
        (i,j) = (0,0)
        top = ''
        bot = ''
        #print(distances)
        
        while ((i<n) or (j<m)):
                if j <= (m-1) and i <= (n-1):
                    d = min(min(distances[i,j:]), min(distances[i:,j]))
                    
                    test = False
                    for k in range(i, n):
                        if distances[k][j] == d: #self.distance?
                            depart = (k,j)
                            test = True
                            break
                    if not test:
                        for l in range(j,m):
                            if distances[i][l] == d: #self.distance?
                                depart = (i,l)
                                test = True
                                break
                    i_new,j_new = depart[0], depart[1]
                    top = top + '='*(j_new-j) + self.top[i:(i_new + 1)] 
                    bot = bot + '='*(i_new - i) + self.bottom[j:(j_new + 1)]
                    i, j = i_new + 1, j_new + 1
                    
                
                elif j == m:
                    top = top + self.top[i::]
                    bot = bot + '='*len(self.top[i::])
                    i = n
                elif i == n:
                    bot = bot + self.bottom[j::]
                    top = top + '='* len(self.bottom[j::])
                    j = m
            
        self.top = top
        self.bottom = bot
            
        
    def report(self):
        mot1, mot2 = self.top, self.bottom
        top = ''
        bot = ''
        for lettre_1, lettre_2 in zip(mot1, mot2):
            if lettre_1 != lettre_2:
                if lettre_1 == '=':
                    lettre_1 = f'{Ruler.red_text(lettre_1)}'
                elif lettre_2 == '=':
                    lettre_2 = f'{Ruler.red_text(lettre_2)}'
                else:
                    lettre_1 = f'{Ruler.red_text(lettre_1)}'
                    lettre_2 = f'{Ruler.red_text(lettre_2)}'
                    
            top = top + lettre_1
            bot = bot + lettre_2
            
        return top, bot
    
        
        
        
        
        
        
        
        