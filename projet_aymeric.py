import PIL as pil
from PIL import Image
from PIL import ImageTk
import tkinter as tk
from tkinter.filedialog import askopenfilename
import os

C_H, C_W = 250, 250
C_RAY = C_H/25
reading = False
check = False
dir_frame = ''


def nbrCol(matrice):
    return(len(matrice[0]))


def nbrLig(matrice):
    return len(matrice)


def saving(matPix, filename):
    # sauvegarde l'image contenue dans matpix dans le fichier filename
	# utiliser une extension png pour que la fonction fonctionne sans perte d'information
    toSave = pil.Image.new(mode= "1",size= (nbrCol(matPix),nbrLig(matPix)))
    for i in range(nbrLig(matPix)):
        for j in range(nbrCol(matPix)):
            toSave.putpixel((j,i),matPix[i][j])
    toSave.save(filename)


def loading(filename):
    # charge le fichier image filename et renvoie une matrice de 0 et de 1 qui représente 
    # l'image en noir et blanc
    global dimension_qr
    toLoad = pil.Image.open(filename)
    mat = [[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    dimension_qr = toLoad.size[1], toLoad.size[0]
    for i in range(dimension_qr[0]):
        for j in range(dimension_qr[1]):
            mat[i][j] = 0 if toLoad.getpixel((j, i)) == 0 else 1
    return mat


def affiche_mat(matrice):
    label = str()
    for i in matrice:
        if len(label) != 0:
            label += '\n'
        for y in i:
            label += str(y)+' '
    return label


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


def mat_rotate(matrice, rotation):
    '''Fonction qui prend en entrée une matrice puis la rotation désirée
    et qui retourne la matrice retournée.'''
    if rotation == 90:
        for i in range(3):
            matrice = list(reversed(list(zip(*matrice))))
    elif rotation == 180:
        for i in range(2):
            matrice = list(reversed(list(zip(*matrice))))
    elif rotation == -90:
        matrice = list(reversed(list(zip(*matrice))))
    return(matrice)


def dir_image():
    file_dir = askopenfilename(initialdir=os.path.realpath(os.getcwd()))
    return file_dir


def load_canvas():
    canvas.delete("all")
    cpt = [0, 0]
    for line in range(len(mat)):
        for i in range(len(mat[line])):
            if mat[line][i] == 1:
                canvas.create_rectangle(C_RAY*i,C_RAY*line,C_RAY*i+C_RAY,C_RAY*line+C_RAY,fill="white")
    canvas.update()
    print("qr code affiché")
        


def load_image():
    global mat, check
    mat = loading(dir_image())
    print(affiche_mat(mat))
    if dimension_qr[0] == 25 and dimension_qr[1] == 25:
        load_canvas()
        check = True


def check_corner():
    global check, mat
    if check:
        coin_ref = qr_coin()
        coins = [[], [], [], []]
        for i in range(7):
            coins[0].append([])
            coins[1].append([])
            for j in range(7):
                coins[0][i].append(mat[i][j])
            for j in range(18, 25):
                coins[1][i].append(mat[i][j])
        for i in range(18, 25):
            coins[2].append([])
            coins[3].append([])
            for j in range(7):
                coins[2][i-18].append(mat[i][j])
            for j in range(18, 25):
                coins[3][i-18].append(mat[i][j])
        print('\n'+affiche_mat(coins[0])+'UP left corner')
        print('\n'+affiche_mat(coins[1])+'UP right corner')
        print('\n'+affiche_mat(coins[2])+'DOWN left corner')
        print('\n'+affiche_mat(coins[3])+'DOWN right corner')
        print('\n'+affiche_mat(coin_ref)+'Référence\n\n')
        if coins[0] != coin_ref:
            print('UP Left corner should be the DOWN Right')
            mat = mat_rotate(mat, 180)
            print('Correction...')
        elif coins[1] != coin_ref:
            print('UP Right corner should be the DOWN Right')
            mat = mat_rotate(mat, 90)
            print('Correction...')
        elif coins[2] != coin_ref:
            print('DOWN Left corner should be the DOWN Right')
            mat = mat_rotate(mat, -90)
            print('Correction...')
        elif coins[3] != coin_ref:
            print('Le QR code est bien placé')
        load_canvas()
    else:
        canvas.delete("all")


def check_line():
    global mat, check, reading
    if check:
        erreur = False
        if dir_frame == '':
            print('Il faut localiser le QR frame.png')
            qr_frame = loading(dir_image())
        else:
            qr_frame = loading(dir_frame)
        print('QR Frame chargé')
        for i in range(6, 18):
            if mat[6][i] != qr_frame[6][i]:
                erreur = True
            if mat[i][6] != qr_frame[i][6]:
                erreur = True
        if erreur:
            print('Les lignes de coins du QR Code ne sont pas identifiées')
            reading = True
        else:
            print('Les lignes de coins du QR Code sont identifiées')


def parité(bits: list, indices: list):
    out = 0
    for bit in indices:
        out += bits[bit]
    return out % 2


def switch_bin(binary: int):
    if binary == 0:
        binary = 1
    else:
        binary = 0
    return binary


def hamming(bits):
    '''Prend 7 bits en entrée et rend 4 bits de données
    (C'est un code de correction d'erreur de Hamming)'''
    c1, c2, c3 = parité(bits, [0, 1, 3]), parité(bits, [0, 2, 3]), parité(bits, [2, 1, 3])
    if c1 != bits[-3] and c2 != bits[-2] and c3 != bits[-1]:
        bits[3] = switch_bin(bits[3])
    elif c2 != bits[-2] and c3 != bits[-1]:
        bits[2] = switch_bin(bits[2])
    elif c1 != bits[-3] and c3 != bits[-1]:
        bits[1] = switch_bin(bits[1])
    elif c1 != bits[-3] and c2 != bits[-2]:
        bits[0] = switch_bin(bits[0])
    return [bits[0], bits[1], bits[2], bits[3]]


def sorting_qr():
    '''Cette fonction lit une matrice de 25x25 représentant
    un QR code correctement orienté afin de retourner
    les blocs de lecture binaire associés'''
    global mat
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
                liste_binaire[(zigzag*2)-2].append(mat[y][x])
        size -= 2
        liste_binaire.append([])
        for i in range(14):
            x = 11+i
            for j in range(2):
                y = size-j
                liste_binaire[(zigzag*2)-1].append(mat[y][x])
        size -= 2
    for ligne in liste_binaire:
        if ligne[0:len(ligne)//2].count(1) != 14:
            blocs.append(ligne[0:len(ligne)//2])
        if ligne[len(ligne)//2:len(ligne)].count(1) != 14:
            blocs.append(ligne[len(ligne)//2:len(ligne)])
    return blocs


def blocs_to_hamming(blocs):
    output = []
    for bloc in blocs:
        output.append(hamming(bloc[:7]) + hamming(bloc[7:]))
    return output


def bits_to_ascii(binary: list):
    '''Prend du binaire en argument (list) et retourne
    le character ASCII associé'''
    value = str()
    for i in binary:
        value += str(i)
    print(repr(value))
    value = chr(int(value, 2))
    print(repr(value))
    return value


def check_filter():
    '''Identifie le type de filtre appliqué au QR Code
    pour sa lisibilité puis retire de la matrice le filtre.
    \nLe paramètre du filtre dépend de 2 bits de la matrice: 
    (23,8) et (22,8). \n\nSi "00" : entièrement noire (pas de changement).
    \nSi "01" : damier dont la case en haut à gauche est noire.
    \nSi "10" des lignes horizontales alternées noires et blanches,
    la plus haute étant noire.
    \nSi "11" des lignes verticales alternées noires et blanches, 
    la plus à gauche étant noire.'''
    global mat
    filtre = str(mat[23][8]) + str(mat[22][8])
    if filtre == '01':
        pass
    elif filtre == '10':
        pass
    elif filtre == '11':
        pass


def check_qr():
    if check:
        check_corner()
        check_line()
        check_filter()
        blocs = sorting_qr()
        print('\nExtraction des blocs binaires du QR Code :\n')
        for i in blocs:
            print(i)
        print("\nFin de l'extraction\n")
        blocs = blocs_to_hamming(blocs)
        if mat[24][8] == 1:  # ASCII
            output = str()
            for bloc in blocs:
                output += bits_to_ascii(bloc)
            print('Contenu du QR Code : ', output)
        else:
            # Données numériques
            pass
    else:
        canvas.delete("all")


# Initialisation du GUI

root = tk.Tk()
root.title('QR Code')
root.geometry('420x490')

# Ajout de fonctionnalités

button_charger = tk.Button(root, text='Charger', command=load_image, bg='gray')
button_check_qr = tk.Button(root, text='Check & Process', command=check_qr, bg='gray')
canvas = tk.Canvas(root, width=C_W,height=C_H,bg="black")

button_charger.pack(side=tk.BOTTOM, ipadx=150, ipady=6)
button_check_qr.pack(side=tk.BOTTOM, ipadx=70)
canvas.pack(pady=20)

# Maintien de la fenêtre

root.mainloop()
