from random import randint
from math import *
from math import log2, floor

# Cette fonction permet de générer un nombre aléatoire entier dans l'intervalle donné
def generation_nombre_aleatoires(a, b):
    return randint(a, b)

# Cette fonction permet de donner la liste des puissances de 2 d'un nombre
def puissance_de_deux(p):

    # On initialise une variable locale et un tableau vide
    expo=1
    tab_expo=[]

    while (expo != 0):

        # On prend la partie entière inférieure du log en base 2 de la puissance
        expo = floor(log2(p))

        # On ajoute ce nombre à notre liste
        tab_expo.append(expo)

        # On enlève à la puissance le nombre obtenu, permettant ainsi de la réduire
        p=p-(2**expo)

        # Si la puissance est nulle, on retourne notre tableau de puissances, car il n'y a plus rien à calculer
        if (p == 0):
            return tab_expo
    return tab_expo

def exp_rapide(a, p, n):

    # On commence par prendre la liste des puissances de 2 de la puissance du nombre
    tab_puissance_deux = puissance_de_deux(p)

    # On prend toutes les puissances de 2 et on calcule leur valeur
    for i in range(len(tab_puissance_deux)):
        tab_puissance_deux[i] = 2**tab_puissance_deux[i]

    # On initialise une variable locale et un tableau vide, auquel on ajoute le nombre initial et la puissance 1
    puissance = 1
    new_tab = []
    new_tab.append([puissance, (a**puissance) % n])
    k = 0

    # Tant que la puissance du nombre est inférieur à la partie entière inférieure de la puissance demandée du nombre, on boucle
    while (puissance <= floor(p/2)):

        # On crée un nouveau tableau
        new_tab_2 = []

        # On double la puissance
        puissance *= 2

        # On ajoute au tableau la puissance
        new_tab_2.append(puissance)

        # On ajoute à new_tab_2 le dernier élément du tableau, mis au carré et modulo n
        new_tab_2.append((new_tab[k][1]**2) % n)

        # On ajoute au tableau new_tab_2
        new_tab.append(new_tab_2)

        # On change l'indice du dernier élément du tableau
        k += 1

    # On initie le résultat à 1    
    result = 1

    # On parcours le tableau des puissances de 2 obtenus
    for i in range(len(tab_puissance_deux)):

        # On parcours le tableau créé précédement
        for j in range(len(new_tab)):

            # Si les valeurs des puissances de 2 correspondent, on multiplie le résultat par la valeur du tableau créé correspondant à l'élément à la puissance de 2
            # modulo n
            if (tab_puissance_deux[i] == new_tab[j][0]):
                result = (result * new_tab[j][1]) % n

    # On retourne le résultat
    return result

#value = exp_rapide(2**512 + 7, 123456789, 2**1024)
#print(value)


# Cette fonction permet de vérifier qu'un nombre est premier
def verif_nb_prem(n):

    # On vérifie 20 fois
    for i in range(20):

        # On génère un nombre alpha compris entre 2 et n - 1 pour un nombre initial n
        value = generation_nombre_aleatoires(2, n - 1)

        # On met ce nombre à la puissance n - 1 modulo n
        value_2 = exp_rapide(value, n-1, n)

        # Si le résultat diffère de 1, cela signifie que le nombre n'est pas premier, donc on quitte la fonction en retournant False
        if (value_2 != 1):
            return False

    # Si tout c'est bien passé, cela signifie que le nombre est premier, et on retourne True. (On remarque que cependant, on n'est pas certain que le nombre soit premier...)
    return True

#if (verif_nb_prem(18)):
#    print(18)
#else :
#    print("pas premier")

# Cette fonction permet de générer un nombre premier dans l'intervalle [a; b]
def gen_nb_prem(a, b):

    # On boucle à l'infini
    while True :

        # On génère un nombre compris dans l'intervalle demandé
        p = generation_nombre_aleatoires(a, b)

        # Si le nombre est accepté par la fonction verif_nb_prem(), on le renvoie, sinon, on boucle.
        if (verif_nb_prem(p) == True):
            return p

#print (gen_nb_prem(2, 100))

# Cette fonction permet de trouver le pgcd de 2 nombres, et l'inverse modulaire de b si pgcd(a, b) = 1
def Euclide(a, b):

    # Si a est plus petit que b, on signale une erreur et on quitte
    if (a < b):
        print("Attention, a < b")
        return None

    # Sinon, on suit étape par étape l'algorithme donné dans l'énoncé. La seule différence est qu'on doit introduire des nouvelles variables pour faire des switch
    # de variables.
    r_0 = a
    r_1 = b
    s_0 = 1
    s_1 = 0
    t_0 = 0
    t_1 = 1
    q_1 = r_0 // r_1
    while (r_1 != 0):
        c = r_1
        r_1 = r_0 - q_1 * r_1
        r_0 = c
        d = s_1
        s_1 = s_0 - q_1 * s_1
        s_0 = d
        e = t_1
        t_1 = t_0 - q_1 * t_1
        t_0 = e
        # Ici je m'assure qu'on n'ait pas de divisions par 0 au cas où r_1 devient 0, car lorsque r_1 devient 0, on finit la boucle while...
        if (r_1 != 0):
            q_1 = r_0 // r_1

    # On retourne les avant-dernières valeurs obtenues dans un tableau
    tab = []
    tab.append(r_0)
    tab.append(s_0 if s_0 >= 0 else s_0 + b)
    tab.append(t_0 if t_0 >= 0 else t_0 + a)
    return tab

#print(Euclide(120, 7))

# Cette fonction permet de générer des clés de 512 bits environ
def gen_cle():

    # On commence par générer 2 nombres premiers d'environ 512 bits
    p = gen_nb_prem(2**511, 2**512)
    q = gen_nb_prem(2**511, 2**512)

    # On calcule ensuite n qui aura environ une taille de 1024 bits
    n = p * q

    # On calcule la fonction phi d'Euler pour n
    phi_n = (p - 1) * (q - 1)

    # On initialise un tableau vide qui permettra de stocker le résultat de l'algorithme d'Euclide, ainsi que les valeurs de e et d à 1
    tab = []
    e = 1
    d = 1

    # Tant qu'on n'a pas trouvé de nombre e premier avec phi_n, on boucle
    while (e == 1):

        # On commence par générer un nombre aléatoire de environ 512 bits
        e = generation_nombre_aleatoires(2**511, 2**512)

        # On regarde si ce nombre est premier avec n, c'est à dire si pgcd(phi_n, e) = 1. Pour cela, on exécute l'algorithme d'Euclide.
        tab = Euclide(phi_n, e)

        # Le résultat du pgcd(phi_n, e) est stocké à la première place dans le tableau, et l'inverse modulaire de e à la dernière place, si le pgcd est 1.
        # Si le pgcd est égal à 1, on donne à d la valeur de l'inverse modulaire de e. Sinon, on remet e à 1 et on recommence.
        if (tab[0] == 1):
            d = tab[2]
            break
        else :
            e = 1

    # On exporte notre tableau contenant p, q, n, e et d, donnant ainsi une paire de clés publique/privé
    key = []
    key.append(p)
    key.append(q)
    key.append(n)
    key.append(e)
    key.append(d)
    return key

# Cette fonction permet d'encryptrer un message avec une clé donné. On va prendre le message, on le met à la puissance e modulo n, et on renvoie le résultat
def encryption(message, key):
    return exp_rapide(message, key[3], key[2])

# Cette fonction permet de décrypter un message avec une clé donné. On va prendre le cipher, et on le met à la puissance d modulo n, et on renvoie le résultat
def decryption(cipher, key):
    return exp_rapide(cipher, key[4], key[2])

# On teste notre fonction. On génère une paire de clé (ce qui peut prendre 20 secondes sur mon ordinateur... Au fait, cela dépend du nombre qu'il génère pour e, car 
# si il ne génère pas le bon e premier avec phi_n, il devra exécuter plusieurs fois), puis on crée un message qu'on encode
# et qu'on décode après. On regarde si le message encodé puis décodé est le même message que le message initial.

key = gen_cle()

message = 15
print(message)

cipher = encryption(message, key)
print(cipher)

message_2 = decryption(cipher, key)
print(message_2)


