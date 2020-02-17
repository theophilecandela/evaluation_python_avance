# evaluation_python_avance

Pour Needleman-wunsher
Utiliser Ruler ou Ruler bis (Ruler marche mieux)
le premier construit la table des distances distance[i][j] pour les mots top[i::], bottom[j::] où l'on impose top[i] et bottom[j] en vis à vis. Sauf en position 0 où l'on compte eventuellement le décalage (on souhaite que la première colonne et la première ligne indiquent les "vraies" distances.
le second construit la table des plus courtes distances distance[i][j] pour les mots top[i::], bottom[j::]. 
