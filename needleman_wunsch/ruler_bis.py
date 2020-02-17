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
                    if l2 in self.couts[l1].keys():
                        d = self.couts[l1][l2]
            else:
                    d = 1
        return d
        
        
        
        
    def compute(self):
        n = len(self.top)
        m = len(self.bottom)
        p = min(n,m)
        distances = np.zeros((n,m))
        
        for k in range(p):
            
            for i in range(n-1-k,-1,-1):
                j = m-1-k
                #ATTENTION aux bords
                if j < (m-1) and i < (n-1):
                    c = Ruler.cout(self.matrice, self.couts, self.top[i],self.bottom[j])
                    distances[i][j] = min(distances[i+1][j+1] + c, distances[i][j+1] + Ruler.cout(self.matrice, self.couts, self.bottom[j], '='), distances[i+1][j] + Ruler.cout(self.matrice, self.couts, self.top[i], '='))
                
                elif j == (m-1) and i == (n-1):
                    c = Ruler.cout(self.matrice, self.couts, self.top[i],self.bottom[j])
                    distances[i][j] = min(c, Ruler.cout(self.matrice, self.couts, self.bottom[j], '=') + Ruler.cout(self.matrice, self.couts, self.top[i], '='))
                    
                elif j == m-1:
                    c = Ruler.cout(self.matrice, self.couts, self.top[i],self.bottom[j])
                    #calcul du cout de la fin du mot
                    a = 0
                    for l in range(i, n):
                        a += Ruler.cout(self.matrice, self.couts, self.top[i], '=')
                    distances[i][j] = min( c + a - Ruler.cout(self.matrice, self.couts, self.top[i], '='), a + Ruler.cout(self.matrice, self.couts, self.bottom[j], '='), distances[i+1][j] + Ruler.cout(self.matrice, self.couts, self.top[i], '='))
                    
                else:
                    c = Ruler.cout(self.matrice, self.couts, self.top[i],self.bottom[j])
                    a = 0
                    for l in range(j, m):
                        a += Ruler.cout(self.matrice, self.couts, self.bottom[j], '=')
                    distances[i][j] = min( c + a - Ruler.cout(self.matrice, self.couts, self.bottom[j], '='), a + Ruler.cout(self.matrice, self.couts, self.top[i], '='), distances[i][j+1] + Ruler.cout(self.matrice, self.couts, self.bottom[j], '='))
                
                
            for j in range(m-2-k,-1,-1):# m-1-k déjà calculé
                i = n-1-k
                if j < (m-1) and i < (n-1):
                    c = Ruler.cout(self.matrice, self.couts, self.top[i],self.bottom[j])
                    distances[i][j] = min(distances[i+1][j+1] + c, distances[i][j+1] + Ruler.cout(self.matrice, self.couts, self.bottom[j], '='), distances[i+1][j] + Ruler.cout(self.matrice, self.couts, self.top[i], '='))
                
                else:
                    c = Ruler.cout(self.matrice, self.couts, self.top[i],self.bottom[j])
                    a = 0
                    for l in range(j, m):
                        a += Ruler.cout(self.matrice, self.couts, self.bottom[j], '=')
                    distances[i][j] = min( c + a - Ruler.cout(self.matrice, self.couts, self.bottom[j], '='), a + Ruler.cout(self.matrice, self.couts, self.top[i], '='), distances[i][j+1] + Ruler.cout(self.matrice, self.couts, self.bottom[j], '='))
                

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
                        if distances[k][j] == d:
                            depart = (k,j)
                            test = True
                            break
                    if not test:
                        for l in range(j,m):
                            if distances[i][l] == d:
                                depart = (i,l)
                                test = True
                                break
                    i_new,j_new = depart[0], depart[1]
                    top = top + '='*(j_new-j) + self.top[i:(i_new + 1)] 
                    bot = bot + '='*(i_new - i) + self.bottom[j:(j_new + 1)]
                    i, j = i_new + 1, j_new + 1
                    #print(i_new, j_new)
                
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
    
        
        






































        

        
        
    # def compute(self):
    #     if self.top == '':
    #         self.top = '=' * len(self.bottom)
    #         #mise à jour de la distance
    #         self.distance = 0
    #         if self.matrice:
    #             for lettre in self.bottom:
    #                 if lettre in self.couts.keys():
    #                     if '=' in self.couts[lettre].keys():
    #                         self.distance += self.couts[lettre]['=']
    #                     else:
    #                         self.distance += 1
    #                 else:
    #                     self.distance += 1
    #         else:
    #             self.distance += len(self.bottom)
    #             
    #         
    #     elif self.bottom == '':
    #         self.bottom = '='*len(self.top)
    #         #mise à jour de la distance
    #         self.distance = 0
    #         if self.matrice:
    #             for lettre in self.top:
    #                 if lettre in self.couts.keys():
    #                     if '=' in self.couts[lettre].keys():
    #                         self.distance += self.couts[lettre]['=']
    #                     else:
    #                         self.distance += 1
    #                 else:
    #                     self.distance += 1
    #         else:
    #             self.distance += len(self.top)
    #             
    #     else:
    #         #On distingue les trois cas de la récursion
    #         recursion = [ (self.top[0], self.bottom[0], Ruler(self.top[1:], self.bottom[1:], self.couts)) , (self.top[0], '=', Ruler(self.top[1:], self.bottom, self.couts)) , ('=', self.bottom[0], Ruler(self.top, self.bottom[1:], self.couts)) ]
    #         
    #         for cas in recursion:
    #             lettre_1, lettre_2, ruler = cas
    #             l1, l2 = min(lettre_1, lettre_2), max(lettre_1, lettre_2)
    #             ruler.compute()
    #             d = 0 
    #             if lettre_1 != lettre_2:
    #                 if self.matrice:
    #                     if l1 in self.couts.keys():
    #                         if l2 in self.couts[l1].keys():
    #                             d = self.couts[l1][l2]
    #                 else:
    #                      d = 1
    #             d += ruler.distance
    #             if d < self.distance:
    #                 self.distance = d
    #                 top, bottom = ruler.report() 
    #                 self.top, self.bottom = lettre_1 + top, lettre_2 + bottom
    
    
        
        
        
        
        