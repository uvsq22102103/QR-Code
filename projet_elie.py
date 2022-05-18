# noir = 0
# blanc  = 1

##########################
# importation des librairies

import PIL as pil
from PIL import Image  
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


def read_bolc():
    global num_filtre
    liste_binaire = []
    blocs = []
    size = 24
    for zigzag in range(4):
        zigzag += 1
        liste_binaire.append([])
        for i in range(14):
            x = 24-i
            for j in range(2):
                y = size-j
                liste_binaire[(zigzag*2)-2].append(num_filtre[y][x])
        size -= 2
        liste_binaire.append([])
        for i in range(14):
            x = 11+i
            for j in range(2):
                y = size-j
                liste_binaire[(zigzag*2)-1].append(num_filtre[y][x])
        size -= 2
    for ligne in liste_binaire:
        if ligne[0:len(ligne)//2].count(1) != 14:
            blocs.append(ligne[0:len(ligne)//2])
        if ligne[len(ligne)//2:len(ligne)].count(1) != 14:
            blocs.append(ligne[len(ligne)//2:len(ligne)])
    return blocs


def decoupage(bloc):
    """ decoupe le bloc de 14 en deux bloc de 7 bits"""
    partie = []
    num_bloc = 0
    for i in bloc:
        if i.count(1) != len(i):
            partie.append(i[:7])
            partie.append(i[7:])
        num_bloc += 2
    
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
    bloc = read_bolc()
    donne = decoupage(bloc)
    print(donne)
    for i in range(len(donne)-8):
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
    return m


def chr_to_ascii_in_bin():
    lettre = list(text.get())

    for i in range(len(lettre)):
        lettre[i] = bin(ord(lettre[i]))[2:]
        while len(lettre[i]) < 8:
            lettre[i] = "0"+lettre[i]
    return(lettre)


def decoupage_to_w(bin_entier):
    bin_decoupe = []
    for i in range(len(bin_entier)):
        bin_decoupe.append(bin_entier[i][:4])
        bin_decoupe.append(bin_entier[i][4:])
    return bin_decoupe


def hamming_inverse(donnee):
    donnee = list(donnee)
    for i in range(len(donnee)):
        donnee[i] = int(donnee[i])
    d1, d2, d3, d4 = donnee
    p1 = ((d1 + d2 + d4) % 2)
    p2 = ((d1 + d3 + d4) % 2)
    p3 = ((d2 + d3 + d4) % 2)
    return ([d1, d2, d3, d4, p1, p2, p3])


def form_bloc(bloc):
    bloc_de_14 = []
    for i in range(0,len(bloc),2):
        bloc_de_14.append((bloc[i]+bloc[i+1]))
    if len(bloc_de_14) % 2 != 0:
        bloc_de_14.append([1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    return bloc_de_14


def remplissage_qr(qr_code,bloc_to_qr):
    bloc = 0
    sens = True
    qr_code[22][8] = 0
    qr_code[23][8] = 0
    print(bloc_to_qr)
    for i in range(0,len(bloc_to_qr),2):
        if sens:
            i = 24 - i
            chiffre = 0
            for j in range(7):
                j = 24-j
                qr_code[i][j] = bloc_to_qr[bloc][chiffre]
                chiffre += 1
                qr_code[i-1][j] = bloc_to_qr[bloc][chiffre]
                chiffre += 1
            bloc += 1
            chiffre = 0
            for j in range(7,14):
                j = 24-j
                qr_code[i][j] = bloc_to_qr[bloc][chiffre]
                chiffre += 1
                qr_code[i-1][j] = bloc_to_qr[bloc][chiffre]
                chiffre += 1
            bloc += 1
        else:
            i = 24 - i
            chiffre = 0
            for j in range(7):
                j = 11+j
                qr_code[i][j] = bloc_to_qr[bloc][chiffre]
                chiffre += 1
                qr_code[i-1][j] = bloc_to_qr[bloc][chiffre]
                chiffre += 1
            bloc += 1
            chiffre = 0
            for j in range(7):
                j = 18+j
                qr_code[i][j] = bloc_to_qr[bloc][chiffre]
                chiffre += 1
                qr_code[i-1][j] = bloc_to_qr[bloc][chiffre]
                chiffre += 1
            bloc += 1
        sens = not sens

    for i in range(25):
        print(qr_code[i])
    saving(qr_code,"DM IN202/Exemples/qr_message.png")


def ecriture_qr():
    qr_e = loading("DM IN202/Exemples/frame.png")
    text_bin = chr_to_ascii_in_bin()
    bloc_4 = decoupage_to_w(text_bin)
    bloc_7 = []
    for i in range(len(bloc_4)):
        bloc_7.append(hamming_inverse(bloc_4[i]))
    print(bloc_7)
    bloc_14 = form_bloc(bloc_7)
    remplissage_qr(qr_e,bloc_14)
    return


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
sauv = tk.Button(racine, text="créer un qr", command=ecriture_qr)
sauv.grid(column=0, row=3)
text = tk.Entry(racine)
text.grid(column=0, row=0)

racine.mainloop()
