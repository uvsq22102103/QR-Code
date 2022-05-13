# noir = 0
# blanc  = 1

##########################
# importation des librairies

import PIL as pil
from PIL import Image  # noqa
import tkinter as tk
import tkinter.filedialog as tkf
import tkinter.messagebox as tkm


##########################
# definitions des fonctions

def nbrCol(matrice):
    return(len(matrice[0]))


def nbrLig(matrice):
    return len(matrice)


def saving(matPix, filename):  # sauvegarde l'image contenue dans matpix dans\
    #  le fichier filename
    # utiliser une extension png pour que la fonction fonctionne sans perte\
    # d'information
    toSave = pil.Image.new(mode="1", size=(nbrCol(matPix), nbrLig(matPix)))
    for i in range(nbrLig(matPix)):
        for j in range(nbrCol(matPix)):
            toSave.putpixel((j, i), matPix[i][j])
    toSave.save(filename)


def loading(filename):  # charge le fichier image filename et renvoie une\
    #  matrice de 0 et de 1 qui représente
    # l'image en noir et blanc
    toLoad = pil.Image.open(filename)
    mat = [[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            mat[i][j] = 0 if toLoad.getpixel((j, i)) == 0 else 1
    return mat


def squellette():
    """renvoie une matrice correspondante au coin du qr code"""
    matrice = loading("DM IN202/Exemples/coin.png")
    return matrice


def check_coin(matrice):
    """controle si le qr code est dans la bonne position si il ne l'ai pas le
     retourne de 90°"""
    test = squellette()
    chek = 0

    for i in range(8):
        if matrice[i][:8] == test[i] and matrice[-i+(-1)][:8] == test[i] and\
             matrice[i][17:] == test[i][::-1]:
            chek = True
            pass
        else:
            print("le qr code est mal positioné")
            matrice = rotate(matrice)
    if chek:
        print("le qr code est dans la bonne position")
        return matrice


def check_alternance(matrice):
    """controle l'alternance, pixel noir et pixel blanc qui rejoignent
     les symboles des coins de l’image"""
    alternance = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    verif = True
    for i in range(11):
        if matrice[6][7+i] == alternance[i] and matrice[7+i][6]\
             == alternance[i]:
            verif = True
        else:
            print("l'alternance n'est pas respecter")
            matrice = rotate(matrice)
    if verif:
        print("l'alternance est juste")
    return matrice


def rotate(matrice):
    """retourne l'image de 90° vers la droite"""
    mat = []
    for i in range(nbrCol(matrice)):
        ligne = []
        for j in range(nbrLig(matrice)):
            ligne.append(matrice[j][i])
        ligne.reverse()
        mat.append(ligne)
    matrice = list(mat)
    return matrice


def hamming(liste):
    """verifie si les donnée ou les bits de parités ne contiennent
    pas d'erreur"""
    d1, d2, d3, d4, p1, p2, p3 = liste
    c = [True, True, True]
    correction = ""
    if p1 != ((d1 + d2 + d4) % 2):
        c[0] = False
    if p2 != ((d1 + d3 + d4) % 2):
        c[1] = False
    if p3 != ((d2 + d3 + d4) % 2):
        c[2] = False
    if False in c:
        if c.count(False) == 3:
            d4 = 1 - d4
            correction = "d4"
        elif c.count(False) == 2:
            if c[0] is False and c[1] is False:
                d1 = 1 - d1
                correction = "d1"
            elif c[0] is False and c[2] is False:
                d2 = 1 - d2
                correction = "d2"
            elif c[1] is False and c[2] is False:
                d3 = 1 - d3
                correction = "d3"
        elif c.count(False) == 1:
            if c[0] is False:
                p1 = 1 - p1
                correction = "p1"
            if c[1] is False:
                p2 = 1 - p2
                correction = "p2"
            if c[2] is False:
                p3 = 1 - p3
                correction = "p3"
    else:
        correction = "aucun bits"
    print("il y a une erreur a", correction)
    liste = d1, d2, d3, d4, p1, p2, p3

    return(liste)


def read_bolc(m):
    """ lit le QR code par bloc de 14 bits"""
    global num_filtre
    all_blocks = []

    sens = True
    for i in range(1, nbrCol(m)+1, 2):
        if sens and i < len(m)-7:
            case = 0
            for j in range(2):
                block = []
                while len(block) < 14:
                    case += 1
                    block.append(m[-i][-case])
                    block.append(m[-i-1][-case])
                all_blocks.append(block)
        elif sens is False and i <= len(m)-7:
            case = 15
            for j in range(2):
                block = []
                while len(block) < 14:
                    case -= 1
                    block.append(m[-i][-case])
                    block.append(m[-i-1][-case])
                all_blocks.append(block)
        sens = not sens
    return all_blocks


def decoupage(bloc):
    """ decoupe le bloc de 14 en deux bloc de 7 bits"""
    partie = []
    num_bloc = 0
    for i in bloc:
        if i.count(1) != len(i):
            partie.append(i[:7])
            partie.append(i[7:])
        num_bloc += 1
    return partie


def trad_ascii(m):
    """ renvoie la lettre corespondant au  8 bits de donnés """
    message = ""
    for i in range(0, len(m)-1, 2):
        code_bi = ""
        for j in range(4):
            code_bi += str(m[i][j])
        for j in range(4):
            code_bi += str(m[i+1][j])
        code_num = int(code_bi, 2)
        message += chr(code_num)
    return message


def trad_hex(m):
    """ renvoie l'hexadecimal correspondant au 4 bits de donnée"""
    message = ""
    for i in range(0, len(m)):
        multiplicateur = 8
        code_hexa = ""
        code_bi = 0
        for j in range(4):
            code_bi += (m[i][j])*multiplicateur
            multiplicateur //= 2
        code_hexa = hex((code_bi))[2:].zfill(0)
        message += (code_hexa)

    return message


def importation():
    """ importe le fichier selectionner par l'utilisateur"""
    global fichiers
    fichiers = tkf.askopenfilename(initialdir="QR-Code/DM IN202/Exemples")
    print("le fichier est bien importé")


def decodage():
    "permet de decoder un QR code"
    global num_filtre
    # qr = la matrice du qr code
    # bloc = le bloc de 14 bits decoupé
    # donne = les 7 bits de donné et  de parités
    # resultat =  le message contenu par le qr code
    text.delete(0, tk.END)
    qr = loading(fichiers)
    qr = check_coin(qr)
    qr = check_alternance(qr)
    num_filtre = filtre(qr)
    bloc = read_bolc(qr)
    donne = decoupage(bloc)
    print(donne)
    for i in range(len(donne)):
        donne[i] = hamming(donne[i])
    if qr[24][8] == 1:
        resultat = trad_ascii(donne)
    else:
        resultat = trad_hex(donne)
    print("le decodage est terminé")
    text.insert(0, resultat)
    tkm.showinfo("résultat", message="le message est: "+resultat)


def filtre(m):
    """permet de savoir quel filtre est appliqué et de changer les bit\
         de données en fonction de celui-ci"""
    a = str(m[22][8]) + str(m[23][8])
    noir = True
    if a == "01":  # damier
        for i in range(len(m)):
            for j in range(len(m[i])):
                if noir:
                    pass
                else:
                    m[i][j] = m[i][j] ^ int(a[1])
                noir = not noir
    elif a == "10":  # ligne horizontal
        for i in range(len(m)):
            for j in range(len(m[i])):
                if i % 2 == 1:
                    m[i][j] = m[i][j] ^ int(a[1])
                elif i % 2 == 0:
                    m[i][j] = m[i][j] ^ int(a[0])
    elif a == "11":  # ligne verticale
        for i in range(len(m)):
            for j in range(len(m[i])):
                if j % 2 == 1:
                    m[i][j] = m[i][j] ^ int(a[0])
                elif j % 2 == 0:
                    m[i][j] = m[i][j] ^ int(a[1])


##########################
# fenetre graphique

num_filtre = ""
fichiers = ""

racine = tk.Tk()
racine.title("QR-CODE")
importer = tk.Button(racine, text="importer le ficher", command=importation)
importer.grid(column=0, row=1)
deco = tk.Button(racine, text="decoder le ficher", command=decodage)
deco.grid(column=0, row=2)
text = tk.Entry(racine)
text.grid(column=0, row=0)

racine.mainloop()
