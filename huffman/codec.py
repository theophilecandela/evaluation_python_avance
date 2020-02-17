class Tree:
    def __init__(self, value, fils1=None, fils2 = None, feuille = False, lettre = None):
        self.value = value
        self.feuille = feuille
        self.fils1 = fils1
        self.fils2 = fils2
        self.lettre = lettre
        
    def _ajoutfils_(self, fils):
        pass
        
class TreeBuilder:
    @staticmethod
    def occurences(text):
        d = {}
        for lettre in text:
            if lettre in d.keys():
                d[lettre] += 1
            else:
                d[lettre] = 1
        return d
        
    @staticmethod
    def insertion_arbre(item, liste_tree):
        #item = un arbre
        #modification en place de liste_tree
        # if liste_tree == []:
        #     liste_tree = [item]
        # else:
        indice = 0
        pas_dernier = False
        
        for i, arbre in enumerate(liste_tree):
            if item.value < arbre.value:
                indice = i
                pas_dernier = True
                break
        if pas_dernier:
            liste_tree = liste_tree[0:indice] + [item] + liste_tree[indice::]
        else:
            liste_tree.append(item)
        
        return liste_tree
    
    def __init__(self, texte):
        self.text = texte
        self.occ = TreeBuilder.occurences(texte)

    def tree(self):
        d = sorted(self.occ.items(), key = lambda x: x[1])
        liste_arbre = [Tree(x[1], feuille = True, lettre = x[0]) for x in d]
        while len(liste_arbre) > 1:
            fils2, fils1, liste_arbre = liste_arbre[0], liste_arbre[1], liste_arbre[2::] #le fils gauche a la plus grande valeur
            new_tree = Tree(fils1.value + fils2.value, fils1, fils2)
            liste_arbre = TreeBuilder.insertion_arbre(new_tree, liste_arbre)
        
        if len(liste_arbre) > 0:
            return liste_arbre[0]
    
    
class Codec:
    def __init__(self, tree):
        self.tree = tree
        
    def encode(self, text):
        alphabet = {}
        liste_arbre = [(self.tree, 'r')]
        while len(liste_arbre) != 0:
            arbre, code = liste_arbre.pop()
            if arbre.feuille:
                alphabet[arbre.lettre] = code[1::]
            else:
                liste_arbre.append((arbre.fils1, code + '0'))
                liste_arbre.append((arbre.fils2, code + '1'))
                
        code = ''
        for lettre in text:
            code += alphabet[lettre]
        return code
            

    def decode(self, code):
        arbre_racine = self.tree
        arbre = arbre_racine
        texte = ''
        while len(code) > 0 or arbre.feuille:
            if arbre.feuille:
                texte += arbre.lettre
                arbre = arbre_racine
            else:
                if code[0] == '0':
                    arbre = arbre.fils1
                    code = code[1::]
                elif code[0] == '1':
                    arbre = arbre.fils2
                    code = code[1::]
        
        return texte
    
    
    
    
    
