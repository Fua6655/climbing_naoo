import numpy as np
import cv2
import math
from PIL import Image
from naoqi import ALProxy
import sys


def main(ip, port, theta_horizont, theta_kose, faktor_odbacivanja_linija, faktor_osjetljivosti_stepenica):

    '''Funkcija'''
    # Nao taking picture
    picture = 'pictures/stairs_nao.png'
    camProxy = ALProxy("ALVideoDevice", ip, port)
    resolution = 2    # 1280x960 Max = 3
    colorSpace = 11   # RGB

    camProxy.setParam(18, 1)    # 18 option for using camera, 1 for bottom camera
    videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 30)

    naoImage = camProxy.getImageRemote(videoClient)

    # Dimensions
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]
    # using PIL library
    im = Image.fromstring("RGB", (imageWidth, imageHeight), array)

    # Save the image
    im.save(picture, "PNG")
    # im.show()
    camProxy.unsubscribe(videoClient)



    '''Funkcija'''
    # reading pictures in dictionary
    im = cv2.imread(picture)
    im_horizont = cv2.imread(picture)
    im_kose = cv2.imread(picture)
    rows, colons, chanels = im.shape
    diagonal = math.sqrt(math.pow(rows, 2) + math.pow(colons, 2))



    '''Funkcija'''
    # image filtering
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur_gauss = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur_gauss, 50, 150, apertureSize=3)
    cv2.imwrite('pictures/stairs_canny.png', canny)



    '''Funkcija'''
    # pull out lines from pictures
    #faktor_osjetljivosti_stepenica = 80  # sto je majni faktor, to su osjetljivije
    lines = cv2.HoughLines(canny, 1, np.pi/180, faktor_osjetljivosti_stepenica)



    '''Funkcija'''
    # writing down horizontal lines in to dictionary lines_horizont
    broj_clanova = 0
    lines_horizont_pomocna = np.zeros((1, np.shape(lines[0])[0], 2))

    for i in range(0, len(lines[0])):
        if (lines[0][i][1]*180/np.pi > theta_horizont[0]) and (lines[0][i][1]*180/np.pi < theta_horizont[1]):
            lines_horizont_pomocna[0][broj_clanova][0] = lines[0][i][0]
            lines_horizont_pomocna[0][broj_clanova][1] = lines[0][i][1]
            broj_clanova += 1

    # izbacivanje 0 iz matrice horizontalnih linija
    lines_horizont = np.zeros((1, broj_clanova, 2))

    for i in range(0, len(lines_horizont[0])):
        lines_horizont[0][i][0] = lines_horizont_pomocna[0][i][0]
        lines_horizont[0][i][1] = lines_horizont_pomocna[0][i][1]

    # Bubble sort algoritam za sortiranje lines_horizont
    for i in range(0, len(lines_horizont[0])):
        for j in range(len(lines_horizont[0])-1-i):
            if lines_horizont[0][j][0] < lines_horizont[0][j+1][0]:
                lines_horizont[0][j][0], lines_horizont[0][j+1][0] = lines_horizont[0][j+1][0], lines_horizont[0][j][0]
                lines_horizont[0][j][1], lines_horizont[0][j+1][1] = lines_horizont[0][j+1][1], lines_horizont[0][j][1]

    broj_clanova_horizont = broj_clanova



    '''Funkcija'''
    # writing down inclined lines in dictionary lines_kosina
    broj_clanova = 0
    lines_kose_pomocna = np.zeros((1, np.shape(lines[0])[0], 2))

    for i in range(0, len(lines[0])):
        # prvo trazimo lijevu kosu liniju
        if (lines[0][i][1]*180/np.pi > theta_kose[0]) and (lines[0][i][1]*180/np.pi < theta_kose[1]):
            lines_kose_pomocna[0][broj_clanova][0] = lines[0][i][0]
            lines_kose_pomocna[0][broj_clanova][1] = lines[0][i][1]
            broj_clanova += 1
        # zatim trazimo desnu kosu liniju
        elif (lines[0][i][1]*180/np.pi > theta_kose[2]) and (lines[0][i][1]*180/np.pi < theta_kose[3]):
            lines_kose_pomocna[0][broj_clanova][0] = lines[0][i][0]
            lines_kose_pomocna[0][broj_clanova][1] = lines[0][i][1]
            broj_clanova += 1

    # izbacivanje 0 iz matrice kosih linija
    lines_kose = np.zeros((1, broj_clanova, 2))

    for i in range(0, len(lines_kose[0])):
        lines_kose[0][i][0] = lines_kose_pomocna[0][i][0]
        lines_kose[0][i][1] = lines_kose_pomocna[0][i][1]

    broj_clanova_kose = broj_clanova



    '''Funkcija'''
    #  Determine the intersections of inclined and horizontal lines
    # definicija pocetnih i konacnih koordinata lijeve i desne kose linije
    for rho, theta in lines_kose[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        # ako je tocka sa lijeve strane
        if (theta*180/np.pi > theta_kose[0]) and (theta*180/np.pi < theta_kose[1]):
            x1L = round((x0 + diagonal*(-b)), 1)
            y1L = round((y0 + diagonal*(a)), 1)
            x2L = round((x0 - diagonal*(-b)), 1)
            y2L = round((y0 - diagonal*(a)), 1)
        # ako je tocka s desne strane
        elif (theta*180/np.pi > theta_kose[2]) and (theta*180/np.pi < theta_kose[3]):

            x1R = round((x0 + diagonal*(-b)), 1)
            y1R = round((y0 + diagonal*(a)), 1)
            x2R = round((x0 - diagonal*(-b)), 1)
            y2R = round((y0 - diagonal*(a)), 1)
    # rijecnik za punit parove centralnih tocki. kljucna rijec je broj linije
    pixeli = {}
    i = 0

    # pronalazak presjecista horizontalnih linija sa kosim
    for j in range(0, broj_clanova_horizont):
        pixeli[j] = []
        x, y = presjeciste(([[x1L, y1L], [x2L, y2L]]), ([[0, round(lines_horizont[0][i][0], 1)], [rows, round(lines_horizont[0][i][0], 1)]]))
        pixeli[j].append((x, y))
        x, y = presjeciste(([[x1R, y1R], [x2R, y2R]]), ([[0, round(lines_horizont[0][i][0], 1)], [rows, round(lines_horizont[0][i][0], 1)]]))
        pixeli[j].append((x, y))
        i += 1



    '''Funkcija'''
    # Rejection of unnecessary pixels, to get the three lines for one stair
    centralna_tocka = {}

    # pronalazak tocke na sredini linije stepenice
    for j in range(0, broj_clanova_horizont):
        centralna_tocka[j] = []
        x = (pixeli[j][1][0]-pixeli[j][0][0])/2 + pixeli[j][0][0]  # x2-x1/2 + X1
        y = (pixeli[j][0][1] + pixeli[j][1][1])/2  # y1+y2/2
        centralna_tocka[j].append((x, y))

    pomocna_lista = {}  # diction za odredivanje koliko linija je nasao umjesto jedne linije
    a = 3  # proizvoljan broj koji puni pomocnu listu u rijecniku


    for j in range(0, (len(centralna_tocka) - 1)):
        if (centralna_tocka[j][0][1] - faktor_odbacivanja_linija) < centralna_tocka[j+1][0][1]: # ako je sljedeci manji od pixel_razmak onda ga izbaci
            pomocna_lista[j] = []
            pomocna_lista[j].append(a)

    z = 0

    pixeli_novi = {}  # ovdje se nalaze pixeli zadnje linije od mnostva linija

    for j in range(0, broj_clanova_horizont):  # ovdje stavit broj_cl_hor -1 da se zadnja linija izbrise
        if j in pomocna_lista:
            pass
        else:
            pixeli_novi[z] = pixeli[j]
            z += 1

    broj_clanova_horizont = len(pixeli_novi)

    pixeli = pixeli_novi


    '''Poziv Funkcije'''
    # showing horizontal lines on picture
    im_horizont = prikaz_linija_na_slici(im_horizont, lines_horizont, rows, colons, diagonal, theta_horizont, theta_kose)
    cv2.imwrite('pictures/stairs_lines_horizont.png', im_horizont)


    '''Poziv Funkcije'''
    # showing inclined lines on picture
    im_kose = prikaz_linija_na_slici(im_kose, lines_kose, rows, colons, diagonal, theta_horizont, theta_kose)
    cv2.imwrite('pictures/stairs_lines_inclined.png', im_kose)


    '''Funkcija'''
    # showing lines on picture
    im_stepenice = prikaz_stepenica_na_slici(im, broj_clanova_horizont, pixeli)
    cv2.imwrite('pictures/stairs_with_lines.png', im_stepenice)



    '''Funkcija'''
    # pixeli_kamera is dictionary with key for koordinates of pixel in center of camera
    pixeli_kamera = {}
    fokus = 573.19

    for j in range(0, broj_clanova_horizont):
        pixeli_kamera[j] = []
        # proracun za lijevu tocku
        x = pixeli[j][0][0] - colons/2
        y = rows/2 - pixeli[j][0][1]     # ovo je dobro
        z = fokus
        pixeli_kamera[j].append((x, y, z))

        #racun za desnu tocku
        x = pixeli[j][1][0] - colons/2
        y = rows/2 - pixeli[j][1][1]   # ovo je dobro
        z = fokus
        pixeli_kamera[j].append((x, y, z))



    '''Funkcija'''
    # vektor_pixela_robot is dictionary with key for vektors of pixels in frame robot
    pixeli_robot = {}

    motion = ALProxy("ALMotion", ip, port)
    T1 = motion.getTransform("CameraBottom", 2, True)
    T1 = np.asarray(T1)
    T1 = np.reshape(T1, (4, 4))


    ''' matrica transformacija tocaka iz openCV u Nao-svijet'''
    T2 = np.zeros((4, 4), dtype=np.float64)
    T2[0, 2] = 1    # Z'=X
    T2[1, 0] = -1    # X'=-Y
    T2[2, 1] = 1    # Y'=-Z
    T2[3, 3] = 1    # homogena koordinata

    T = np.dot(T1, T2)
    ''' tocka centra kamere je tocka izrazena u koordinatnom sustavu robota'''
    kamera_robot = np.transpose([T[0][3], T[1][3], T[2][3]])

    for j in range(0, broj_clanova_horizont):
        pixeli_robot[j] = []
        # pravljenje vektora pixela od pixela kamere da se moze mnozit
        vektor_pixela_kamere = np.ones((4, 1), dtype=np.float64)

        #racun za lijevu tocku na liniji prva tocka u dictionary
        vektor_pixela_kamere[0] = pixeli_kamera[j][0][0]
        vektor_pixela_kamere[1] = pixeli_kamera[j][0][1]
        vektor_pixela_kamere[2] = pixeli_kamera[j][0][2]
        vektor_pixela_kamere[3] = 1  # zbog homogenosti
        a = np.dot(T, vektor_pixela_kamere)
        pixeli_robot[j].append((a[0], a[1], a[2]))

        #racun za desnu tocku na liniji druga tocka u dictionary
        vektor_pixela_kamere[0] = pixeli_kamera[j][1][0]
        vektor_pixela_kamere[1] = pixeli_kamera[j][1][1]
        vektor_pixela_kamere[2] = pixeli_kamera[j][1][2]
        vektor_pixela_kamere[3] = 1  # zbog homogenosti
        a = np.dot(T, vektor_pixela_kamere)
        pixeli_robot[j].append((a[0], a[1], a[2]))

    vektor_pixela_robot = {}  # to je vektor koji sluzi za odredivanje t-a on je normiran

    for j in range(0, broj_clanova_horizont):
        vektor_pixela_robot[j] = []

        # vektor za prvu tocku
        x = pixeli_robot[j][0][0] - kamera_robot[0]
        y = pixeli_robot[j][0][1] - kamera_robot[1]
        z = pixeli_robot[j][0][2] - kamera_robot[2]
        norm = np.sqrt(x*x + y*y + z*z)
        vektor_pixela_robot[j].append((x/norm, y/norm, z/norm))

        # vektor za drugu tocku
        x = pixeli_robot[j][1][0] - kamera_robot[0]
        y = pixeli_robot[j][1][1] - kamera_robot[1]
        z = pixeli_robot[j][1][2] - kamera_robot[2]
        norm = np.sqrt(x*x + y*y + z*z)
        vektor_pixela_robot[j].append((x/norm, y/norm, z/norm))

        # vektor_pixela_robot je normiran




    '''Funkcija'''
    # determination of 3D spots along with plane
    tocke_3D = {}  # sluzi za spremanje tocaka u 3D sustavu
    ravnine_3D = {}  #  sluzi za spremanje ravnina u 3D sustavu, za svaku liniju sprema prijasnju ravninu

    for j in range(0, broj_clanova_horizont):
        tocke_3D, ravnine_3D = odredivanje_tocaka_i_ravnina(vektor_pixela_robot, kamera_robot, tocke_3D, ravnine_3D, j)



    '''Funkcija'''
    # determinating distance fron stairs, height and depth of stairs
    stepenice = {}  # lista stepenice na nultom mjestu se nalazi udaljenost od stepenice, a na ostalim mjestima redni broj stepenice i prvo visina pa onda duljina
    stepenice[0] = []

    udaljenost_od_stepenica = (tocke_3D[0][0][0] + tocke_3D[0][1][0])/2 #po x osi
    k = (tocke_3D[0][1][1] - tocke_3D[0][0][1])/(tocke_3D[0][1][0] - tocke_3D[0][0][0])
    fi = np.arctan(udaljenost_od_stepenica/(np.absolute(k*tocke_3D[0][0][0]) + tocke_3D[0][0][1]))
    stepenice[0].append(udaljenost_od_stepenica)
    stepenice[0].append(fi)

    broj_stepenica = 1
    brojac_stepenica = 'nemoj_prelazit_na_novu_stepenicu'

    for j in range(1, broj_clanova_horizont): # j je broj linije a ne stepenice
        stepenice[j] = []

        if j % 2 == 1:  # ako je pri djeljenju ima ostatak, neparan je onda se racunaju visine
            visina_stepenice = ((tocke_3D[j][0][2]-tocke_3D[j-1][0][2]) + (tocke_3D[j][1][2]-tocke_3D[j-1][1][2]))/2  # po z osi
            stepenice[broj_stepenica].append(visina_stepenice)
            brojac_stepenica = 'nemoj_prelazit_na_novu_stepenicu'

        elif j % 2 == 0:       # ako je paran broj linije, onda racunanje dubine
            dubina_stepenice = ((tocke_3D[j][0][0]-tocke_3D[j-1][0][0]) + (tocke_3D[j][1][0]-tocke_3D[j-1][1][0]))/2  # po x osi
            stepenice[broj_stepenica].append(dubina_stepenice)
            brojac_stepenica = 'predji_na_novu_stepenicu'

        if brojac_stepenica == 'predji_na_novu_stepenicu':  # onda znamo da je izracunao dubinu gazista i treba povecat brojac stepenica
            broj_stepenica += 1




    '''Funkcija'''
    # printing stairs height, depth and filling dictionary parametri_stepenica for json format
    print '_____PARAMETRI STEPENICA_____'
    parametri_stepenica = {}

    for z in range(0, broj_stepenica): #jer je uracunao zadnju letvicu pa trebamo stavit ++++++1
        if z == 0: #udaljenost
            print 'udaljenost od stepenica', stepenice[0][0][0], 'kut stepenica', stepenice[0][1][0]
            print '--------------'
            parametri_stepenica[z] = []
            parametri_stepenica[z].append((stepenice[0][0][0], stepenice[0][1][0]))
        else:
            print z, '. stepenica'
            print 'Visina ', stepenice[z][0][0], ' dubina ', stepenice[z][1][0]
            print '----'
            parametri_stepenica[z] = []
            parametri_stepenica[z].append((stepenice[z][0][0], stepenice[z][1][0]))



    '''Funkcija'''
    #tocke_3D needs to be in more beautiful format
    tocke_3D_json = {}

    for j in range(0, broj_clanova_horizont):
        tocke_3D_json[j] = []
        lijeva_tocka = tocke_3D[j][0][0][0], tocke_3D[j][0][1][0], tocke_3D[j][0][2][0]
        desna_tocka = tocke_3D[j][1][0][0], tocke_3D[j][1][1][0], tocke_3D[j][0][2][0]
        tocke_3D_json[j].append((lijeva_tocka, desna_tocka))


    """Poziv Funkcije"""
    # prije nego sto vrati parametre u glavni program, treba prikazati sliku.
    prikaz_slike()

    return parametri_stepenica, tocke_3D_json, broj_stepenica


#######################################################################################################################
def presjeciste(line1, line2):  # line1 = [[x1, y1],[x2, y2]] & line2 = [[x1, y1],[x2, y2]]
    # funkcija z racunanje presjecista dva pravca. tocke trebaju biti zaokruzene na jednu decimalu
    s1 = np.array(line1[0])
    e1 = np.array(line1[1])

    s2 = np.array(line2[0])
    e2 = np.array(line2[1])

    a1 = (s1[1] - e1[1]) / (s1[0] - e1[0])
    b1 = s1[1] - (a1 * s1[0])

    a2 = (s2[1] - e2[1]) / (s2[0] - e2[0])
    b2 = s2[1] - (a2 * s2[0])

    if abs(a1 - a2) < sys.float_info.epsilon:
        return False

    x = (b2 - b1) / (a1 - a2)
    y = a1 * x + b1
    return x, y


#####################################################################################################################
def prikaz_linija_na_slici(im, lines_plot, rows, colons, diagonal, theta_horizont, theta_kose):
    # showing lines on picture

    for rho, theta in lines_plot[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + diagonal*(-b))
        y1 = int(y0 + diagonal*(a))
        x2 = int(x0 - diagonal*(-b))
        y2 = int(y0 - diagonal*(a))
        if (theta*180/np.pi > theta_horizont[0]) and (theta*180/np.pi < theta_horizont[1]):
            cv2.line(im, (0, int(rho)), (rows, int(rho)), (0, 0, 255), 1)

        else:
            cv2.line(im, (x1, y1), (x2, y2), (255, 0, 0), 1)
    return im


######################################################################################################################
def prikaz_stepenica_na_slici(im, broj_clanova_horizont, pixeli):
    # showing lines on picture
    for linija in range(0, broj_clanova_horizont):
        cv2.line(im, (int(pixeli[linija][0][0]), int(pixeli[linija][0][1])), (int(pixeli[linija][1][0]), int(pixeli[linija][1][1])), (0, 255, 0), 1)

    return im


#######################################################################################################################
def odredivanje_tocaka_i_ravnina(vektor_pixela_robot, kamera_robot, tocke_3D, ravnine_3D, j):

    #prvo treba osigurati mjesto za upis u dictionari tocke i ravnine
    tocke_3D[j] = []
    ravnine_3D[j] = []

    if j == 0:  # ako su prve dvije tocke u pitanju
        A = 0
        B = 0
        C = 1
        D = 0
        ravnine_3D[j].append((A, B, C, D))

    elif j > 0:  # ako su ostale tocke u pitanju

        # funkcija za pronalazak normale koja je okomita na vektor i ravninu odredivanje parametara A,B,C,D
        vektor_3D_x = tocke_3D[j-1][0][0] - tocke_3D[j-1][1][0] # x3DL - x3DR
        vektor_3D_y = tocke_3D[j-1][0][1] - tocke_3D[j-1][1][1] # y3DL - y3DR
        vektor_3D_z = tocke_3D[j-1][0][2] - tocke_3D[j-1][1][2] # z3DL - z3DR

        norm = np.sqrt(vektor_3D_x*vektor_3D_x + vektor_3D_y*vektor_3D_y + vektor_3D_z*vektor_3D_z)  # normiranje za pravac izmedu 3D tocaka
        vektor_linije_3D = [vektor_3D_x[0]/norm, vektor_3D_y[0]/norm, vektor_3D_z[0]/norm]
        vektor_linije_3D = [vektor_linije_3D[0][0], vektor_linije_3D[1][0], vektor_linije_3D[2][0]]  # ovo je zato da bude lipo slozeno u liste

        vektor_3D_normala_x = ravnine_3D[j-1][0][0]
        vektor_3D_normala_y = ravnine_3D[j-1][0][1]
        vektor_3D_normala_z = ravnine_3D[j-1][0][2]

        norm = np.sqrt(vektor_3D_normala_x*vektor_3D_normala_x + vektor_3D_normala_y*vektor_3D_normala_y + vektor_3D_normala_z*vektor_3D_normala_z) #normiranje za pravac izmedu 3D tocaka
        normala_ravnine_3D = [vektor_3D_normala_x/norm, vektor_3D_normala_y/norm, vektor_3D_normala_z/norm]

        # sad ide produkt normale ravnine i vektora pravca ovdje treba pazit sto se kako mnozi, ako se mnozi za neparan j onda se
        if j > 0 and j % 2 == 1:
            normala_nove_ravnine_3D = np.cross(normala_ravnine_3D, vektor_linije_3D)
        else:
            normala_nove_ravnine_3D = np.cross(vektor_linije_3D, normala_ravnine_3D)


        norm = np.sqrt(math.pow(normala_nove_ravnine_3D[0], 2) + math.pow(normala_nove_ravnine_3D[1], 2) + math.pow(normala_nove_ravnine_3D[2], 2))

        A = normala_nove_ravnine_3D[0]/norm
        B = normala_nove_ravnine_3D[1]/norm
        C = normala_nove_ravnine_3D[2]/norm

        # komponenta D se odreduje uvrstavanjem tocke u jednadzbu ravnine uvrstavamo lijevu tocku
        DL = - (A*tocke_3D[j-1][0][0] + B*tocke_3D[j-1][0][1] + C*tocke_3D[j-1][0][2])
        DR = - (A*tocke_3D[j-1][1][0] + B*tocke_3D[j-1][1][1] + C*tocke_3D[j-1][1][2])
        #print DL-DR

        # punjenje dictionarija sa novom ravninom
        ravnine_3D[j].append((A, B, C, DL))

    A = ravnine_3D[j][0][0]
    B = ravnine_3D[j][0][1]
    C = ravnine_3D[j][0][2]
    D = ravnine_3D[j][0][3]

    # kad imamo koeficjente ravnine potrebno je pronaci presjeciste vektora_pixela_robot s ravninom A,B,C,D

    # tocka kamere
    xC = kamera_robot[0]
    yC = kamera_robot[1]
    zC = kamera_robot[2]

    ''' za lijevu tocku racun '''
    # ljevi vektor j
    vektor_xL = vektor_pixela_robot[j][0][0]
    vektor_yL = vektor_pixela_robot[j][0][1]
    vektor_zL = vektor_pixela_robot[j][0][2]

    # za lijevu tocku
    tL = -(A*xC + B*yC + C*zC + D)/(A*(vektor_xL) + B*(vektor_yL) + C*(vektor_zL))

    XL = xC + vektor_xL*tL
    YL = yC + vektor_yL*tL
    ZL = zC + vektor_zL*tL

    tocke_3D[j].append((XL, YL, ZL))

    ''' za desnu tocku racun '''
    # desni vektor j
    vektor_xR = vektor_pixela_robot[j][1][0]
    vektor_yR = vektor_pixela_robot[j][1][1]
    vektor_zR = vektor_pixela_robot[j][1][2]

    # za desnu tocku
    tR = -(A*xC + B*yC + C*zC + D)/(A*(vektor_xR) + B*(vektor_yR) + C*(vektor_zR))

    XR = xC + vektor_xR*tR
    YR = yC + vektor_yR*tR
    ZR = zC + vektor_zR*tR

    tocke_3D[j].append((XR, YR, ZR))

    return tocke_3D, ravnine_3D


#################################################################################################################
def prikaz_slike():
	print "Enter za nastavak, ESC za kraj"
    img = cv2.imread('pictures/stairs_with_lines.png', 1)
    cv2.imshow('image processed stairs', img)

    k = cv2.waitKey(0)
    if k == 27:  # wait for ESC key and exit all program
        cv2.destroyAllWindows()
        sys.exit(0)

    elif k == 13:  # wait for enter key
        cv2.destroyAllWindows()
