#########################################
######### PROJET QR CODE IN-202 #########
#########################################
#
#
# GITHUB : https://github.com/uvsq22102103/QR-Code
#
#
# Note avant usage : ce programme nécéssite une copie du fichier
#                    DM IN202 dans le même Directory pour fonctionner,
#                    le Directory doit se nommer QR-Code
#
######################################################################

# importation des librairies

import PIL as pil
from PIL import Image  # noqa
import tkinter as tk
import tkinter.filedialog as tkf
import tkinter.messagebox as tkm


###########################
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
    qr = [[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            qr[i][j] = 0 if toLoad.getpixel((j, i)) == 0 else 1
    return qr


def qr_coin():
    '''Cette fonction ne prend rien en argument et retourne un coin de QR code
    sous forme de matrice ! '''
    coin = []
    for i in range(7):
        coin.append([])
        for j in range(7):
            coin[i].append(0)
    for i in range(5):
        i += 1
        for j in range(5):
            j += 1
            coin[i][j] = 1
    for i in range(3):
        i += 2
        for j in range(3):
            j += 2
            coin[i][j] = 0
    return coin


def check_coin(qr):
    """Vérifie si 'qr' est orientée dans le sens de lecture que
    veut la convention et le corrige sinon."""
    coin_ref = qr_coin()
    coins = [[], [], [], []]
    for i in range(7):
        coins[0].append([])
        coins[1].append([])
        for j in range(7):
            coins[0][i].append(qr[i][j])
        for j in range(18, 25):
            coins[1][i].append(qr[i][j])
    for i in range(18, 25):
        coins[2].append([])
        coins[3].append([])
        for j in range(7):
            coins[2][i-18].append(qr[i][j])
        for j in range(18, 25):
            coins[3][i-18].append(qr[i][j])
    if coins[0] != coin_ref:
        print('UP Left corner should be the DOWN Right')
        qr = rotate(qr)
        qr = rotate(qr)
        print('Correction...')
    elif coins[1] != coin_ref:
        print('UP Right corner should be the DOWN Right')
        qr = rotate(qr)
        print('Correction...')
    elif coins[2] != coin_ref:
        print('DOWN Left corner should be the DOWN Right')
        qr = rotate(qr)
        qr = rotate(qr)
        qr = rotate(qr)
        print('Correction...')
    elif coins[3] != coin_ref:
        print('Le QR code est bien placé')
    return qr


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
            print("Alternance introuvable, rotation")
            matrice = rotate(matrice)
    if verif:
        print("Alternance OK")
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
    if p1 != ((d1 + d2 + d4) % 2):
        c[0] = False
    if p2 != ((d1 + d3 + d4) % 2):
        c[1] = False
    if p3 != ((d2 + d3 + d4) % 2):
        c[2] = False
    if False in c:
        if c.count(False) == 3:
            d4 = 1 - d4
        elif c.count(False) == 2:
            if c[0] is False and c[1] is False:
                d1 = 1 - d1
            elif c[0] is False and c[2] is False:
                d2 = 1 - d2
            elif c[1] is False and c[2] is False:
                d3 = 1 - d3
        elif c.count(False) == 1:
            if c[0] is False:
                p1 = 1 - p1
            if c[1] is False:
                p2 = 1 - p2
            if c[2] is False:
                p3 = 1 - p3
    liste = d1, d2, d3, d4, p1, p2, p3
    return(liste)


def read_bloc():
    global num_filtre
    liste_binaire = []
    blocs = []
    size = 24
    for zigzag in range(5):
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
    print("Fichier importé")


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
    return bloc_de_14


def remplissage_qr(qr_code,bloc_to_qr):
    bloc = 0
    sens = True
    longueurs = bin(len(bloc_to_qr))[2:]
    print(longueurs)
    while len(longueurs) != 5:
        longueurs = "0" + longueurs
    qr_code[22][8] = 0
    qr_code[23][8] = 0
    qr_code[13][0] = int(longueurs[0])
    qr_code[14][0] = int(longueurs[1])
    qr_code[15][0] = int(longueurs[2])
    qr_code[16][0] = int(longueurs[3])
    qr_code[17][0] = int(longueurs[4])
    if len(bloc_to_qr) % 2 != 0:
        bloc_to_qr.append([1,1,1,1,1,1,1,1,1,1,1,1,1,1])


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
    remplissage_qr(qr_e, bloc_14)
    return


def decodage():
    "permet de decoder un QR code"
    global num_filtre
    text.delete(0, tk.END)
    qr = loading(fichiers)
    qr = check_coin(qr)
    qr = check_alternance(qr)
    nbr_blocs = int(str(qr[13][0])+str(qr[14][0])+str(qr[15][0])+str(qr[16][0])+str(qr[17][0]), 2)
    num_filtre = filtre(qr)
    bloc = read_bloc()
    donne = decoupage(bloc)
    donne = donne[0:nbr_blocs*2]
    for i in range(len(donne)-8):
        donne[i] = hamming(donne[i])
    if qr[24][8] == 1:
        resultat = trad_ascii(donne)
    else:
        resultat = trad_hex(donne)
    print("Décodage achevé")
    text.insert(0, resultat)
    tkm.showinfo("Résultat", message="Le QR Code contient: "+resultat)


##########################
# fenetre graphique

num_filtre = ""
fichiers = ""

racine = tk.Tk()
racine.title("QR-CODE // by KANGA Elie & GOUDOUT Aymeric //")
importer = tk.Button(racine, text="Import fichier", command=importation)
importer.grid(column=0, row=1)
deco = tk.Button(racine, text="Décodage fichier", command=decodage)
deco.grid(column=0, row=2)
sauv = tk.Button(racine, text="créer un qr", command=ecriture_qr)
sauv.grid(column=0, row=3)
text = tk.Entry(racine, width=50)
text.grid(column=0, row=0)

racine.mainloop()
