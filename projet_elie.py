# noir = 0
# blanc  = 1
from json import decoder
from tracemalloc import stop
import PIL as pil
from PIL import Image
from PIL import ImageTk 
import tkinter as tk
import tkinter.filedialog as tkf


def nbrCol(matrice):
    return(len(matrice[0]))


def nbrLig(matrice):
    return len(matrice)


def saving(matPix, filename):#sauvegarde l'image contenue dans matpix dans le fichier filename
							 #utiliser une extension png pour que la fonction fonctionne sans perte d'information
    toSave=pil.Image.new(mode = "1", size = (nbrCol(matPix),nbrLig(matPix)))
    for i in range(nbrLig(matPix)):
        for j in range(nbrCol(matPix)):
            toSave.putpixel((j,i),matPix[i][j])
    toSave.save(filename)


def loading(filename):#charge le fichier image filename et renvoie une matrice de 0 et de 1 qui représente 
					  #l'image en noir et blanc
    toLoad=pil.Image.open(filename)
    mat=[[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            mat[i][j]= 0 if toLoad.getpixel((j,i)) == 0 else 1
    return mat


def squellette():
    matrice =loading("coin.png")
    return matrice


def check_coin(matrice):
    matrice = loading(matrice)
    test = squellette()
    chek = 0

    for i in range (8):
        if matrice[i][:8] == test[i] and matrice[-i+(-1)][:8] == test[i] and matrice[i][17:] == test[i] [: :-1] :
            chek  = True
            pass
        else: 
            print("ce n'est pa un bon carré" )
            matrice = rotate(matrice)
    if chek == True :        
        print("les qr code est dans la bonne position")


def check_alternance(matrice):
    alternance = [1,0,1,0,1,0,1,0,1,0,1]
    matrice = loading(matrice)
    verif = True
    for i in range (11):
        if matrice[6][7+i] == alternance[i] and matrice[7+i][6] == alternance[i]  :
            verif = True
            print("ca marche")
        else : 
            print("nope")
            matrice = rotate(matrice)

 
        


def rotate(matrice):
    mat=[]
    for i in range(nbrCol(matrice)):
        ligne = []
        for j in range(nbrLig(matrice)):
            ligne.append(matrice[j][i])
        ligne.reverse()
        mat.append(ligne)
    matrice = list(mat)
    return matrice


def verification(l):
    p1,p2,p3,d1,d2,d3,d4 = l
    c = [True,True,True]
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
            if c[0] == False and c[1] == False:
                d1 = 1 - d1
                correction = "d1"
            elif c[0] == False and c[2] == False:
                d2 = 1 - d2
                correction = "d2"
            elif c[1] == False and c[2] == False:
                d3 = 1 - d3
                correction = "d3"
        elif c.count(False) == 1 :
            if c[0] == False:
                p1 = 1 - p1
                correction = "p1"
            if c[1] == False:
                p2 = 1 - p2
                correction = "p2"
            if c[2] == False:
                p3 = 1 - p3
                correction = "p3"
    else: 
        correction = "aucune correction"
    l = p1,p2,p3,d1,d2,d3,d4
    d = d1,d2,d3,d4

    return(l)
# a = decode([0, 1, 1, 0, 1, 1, 0])
# print(a)


def read_bolc(m):
    a  = []
    # for i in range (nbrCol(m)):
    b = []
    sens = True
    for i in range (1,nbrCol(m)+1,2):
        if sens == True  and i < len(m)-7 :
            case = 0
            for j in range (2):
                b = []
                while len(b) < 14 :
                    case += 1
                    b.append(m[-i][-case])
                    b.append(m[-i-1][-case])
                a.append(b)
        elif sens == False and i <= len(m)-7:
            case = 15
            for j in range (2):
                b = []
                while len(b) < 14 :
                    case -= 1
                    b.append(m[-i][-case])
                    b.append(m[-i-1][-case])
                a.append(b)
        sens = not sens
    return a


# def decoupage(m):
#     a =[]
#     for i in m:
#         if i.count(1) != len(i):
#             a.append(i[-1:-8:-1])
#             a.append(i[-8::-1])
        
#     return a




# def decodage(m) :
#     message = ""
#     for i in range (0,len(m)-1,2):
#         code_bi = ""
#         for j in range (3,7):
#             code_bi += str(m[i][j])
#         for j in range (3,7):
#             code_bi += str(m[i+1][j])
#         code_num = int(code_bi,2)
#         print(code_bi)
#         print(code_num)
#         message += chr(code_num)
#     # print(message)
#     return message


def decoupage(m):
    a =[]
    for i in m:
        if i.count(1) != len(i):
            a.append(i[:7])
            a.append(i[7:])
    return a
def decodage(m) :
    message = ""
    for i in range (0,len(m)-1,2):
        code_bi = ""
        for j in range (4):
            code_bi += str(m[i][j])
        for j in range (4):
            code_bi += str(m[i+1][j])
        code_num = int(code_bi,2)
        print(code_bi)
        print(code_num)
        message += chr(code_num)
    # print(message)
    return message


def decodage_hex(m) :
    message = ""
    for i in range (0,len(m)-1,2):
        multiplicateur = 8
        code_hexa = ""
        code_bi_1 = 0
        code_bi_2 = 0
        for j in range (3,7):
            code_bi_1 += (m[i][j])*multiplicateur
            multiplicateur //= 2
        multiplicateur = 8
        for j in range (3,7):
            code_bi_2 += (m[i+1][j])*multiplicateur
            multiplicateur //= 2
        print(code_bi_1,code_bi_2)
        code_hexa = hex(code_bi_1)[2:].zfill(0) + hex(code_bi_2) [2:].zfill(0) 
        code_hexa = int(code_hexa,16)
        message += chr(code_hexa)

    return message
        

def importation():
    global fichiers
    fichiers = tkf.askopenfilename(initialdir="/Users/elie/Desktop/QR-Code/DM IN202/Exemples")
    

def  essai():
    
    m = loading(fichiers)

    b = read_bolc(m)

    c =decoupage(b)
    print(c)
    # for i in range (len(c)):
    #     c[i] = verification(c[i])
    # print(verification(c[1]))
    
    d = decodage(c)
    # print('hello' ,d)
    print(d)
    text.insert(0,d)


fichiers = ""



racine = tk.Tk()
racine.title( "QR-CODE")
importer = tk.Button(racine,text="importer le ficher", command= importation)
importer.grid(column= 0, row= 1)
deco = tk.Button(racine,text="decoder le ficher", command= essai)
deco.grid(column= 0 , row= 2)
text = tk.Entry(racine)
text.grid(column = 0, row= 0)









racine.mainloop()


