import numpy as np
import almath
import time


def main(motionProxy, postureProxy, parametri_stepenica):

    motionProxy.setFallManagerEnabled(False)

    # Parametri
    visina_stepenice = parametri_stepenica[1][0][0]
    dubina_stepenice = parametri_stepenica[1][0][1]
    #visina_stepenice = 0.055827938778101105
    odmak_od_stepenice_visinski = 0.01

    #############################################################################################################
    #prebacivanje ravnoteze na  nogu
    motionProxy.wbEnable(True)
    motionProxy.wbGoToBalance("RLeg", 2)
    motionProxy.wbEnable(False)
    print "Prebacio sam ravnotezu na desnu nogu"
    time.sleep(1)
    #############################################################################################################

    # podizanje lijeve noge
    visina = visina_stepenice + odmak_od_stepenice_visinski*2
    brzina = 0.1
    leg_z(motionProxy, brzina, visina, "LLeg", "World")
    print "Lijeva noga Z"
    time.sleep(4)

    # ispruzi lijevu nogu
    zakorak_na_stepenicu = 0.1
    brzina = 0.1
    leg_x(motionProxy, brzina, zakorak_na_stepenicu, "LLeg", "World")
    print "Lijeva noga X"
    time.sleep(5)

    # torso XXXX
    ispruzi_torso = 0.03
    brzina = 0.1
    torso_x(motionProxy, brzina, ispruzi_torso)
    print "Torso XXX"
    time.sleep(1)

    # ispruzi lijevu nogu
    zakorak_na_stepenicu = 0.05
    brzina = 0.1
    leg_x(motionProxy, brzina, zakorak_na_stepenicu, "LLeg", "World")
    print "Lijeva noga X"
    time.sleep(2)

    # torso XXXX
    ispruzi_torso = 0.03
    brzina = 0.1
    torso_x(motionProxy, brzina, ispruzi_torso)
    print "Torso X"
    time.sleep(1)

    #iskreni lijevu nogu
    brzina = 0.05
    kut = 35  # treba zakrenit nogu u worldu za pozitivan smijer
    leg_rotate_z(motionProxy, brzina, kut, "LLeg", "World")
    print "Rotiram lijevu nogu"
    time.sleep(7)

    #spusti lijevu nogu
    zakret_na_stepenici = -odmak_od_stepenice_visinski*1.25
    brzina = 0.1
    leg_z(motionProxy, brzina, zakret_na_stepenici, "LLeg", "Torso")
    print "Lijeva noga -Z"
    time.sleep(1)

    #####################################################################################################
    # prebacivanje ravnoteze u lijevu nogu
    motionProxy.wbEnable(True)
    motionProxy.wbGoToBalance("LLeg", 15.0) #blocking call
    motionProxy.wbEnable(False)
    print "Prebacio ravnotezu na lijevu nogu"
    time.sleep(1)
    #####################################################################################################

    #spusti lijevu nogu digni desnu nogu
    zakret_na_stepenici = -0.02
    brzina = 0.08
    leg_z(motionProxy, brzina, zakret_na_stepenici, "LLeg", "Torso")
    print "Lijeva noga -Z"
    time.sleep(3)

    # torso YYYY
    ispruzi_torso = 0.04
    brzina = 0.06
    torso_y(motionProxy, brzina, ispruzi_torso)
    print "Torso Y"
    time.sleep(4)

    # digni desnu nogu
    zakorak_na_stepenicu = visina_stepenice
    brzina = 0.1
    leg_up(motionProxy, brzina, zakorak_na_stepenicu, "RLeg", "World")
    print "Desna noga Z_up"
    time.sleep(2)

    #spusti lijevu nogu digni desnu nogu
    zakret_na_stepenici = -0.03
    brzina = 0.1
    leg_z(motionProxy, brzina, zakret_na_stepenici, "LLeg", "Torso")
    print "Lijeva noga -Z"
    time.sleep(2)

    # ispruzi desnu nogu
    zakorak_na_stepenicu = 0.17
    brzina = 0.1
    leg_x(motionProxy, brzina, zakorak_na_stepenicu, "RLeg", "World")
    print "Desna noga X"
    time.sleep(4)

    postureProxy.goToPosture("StandInit", 0.1)

    motionProxy.setFallManagerEnabled(True)


def leg_x(motion, speed, zakorak_na_stepenicu, leg, system):
    # provjera koji koordinatni je u pitanju
    if system == "Torso":
        frame = 0
    elif system == "World":
        frame = 1
    elif system == "Robot":
        frame = 2

    # matrica transformacija iz koordinatnog sustava world u lijevu nogu
    T1 = motion.getTransform(leg, frame, True)
    T1 = np.asarray(T1)
    T1 = np.reshape(T1, (4, 4))

    # transformacija koordinatnih sustava racunamo promjenu iz pocetne tocke noge do konacne tocke noge vektor i bacamo u funkciju
    vektor_translacije = [T1[0][3], T1[1][3], T1[2][3]]

    # zapis koordinatne osi lijeve noge u koordinatama robot world
    vektor_x = [T1[0][0], T1[1][0], T1[2][0]]

    # sad trazim faktor skaliranja vektora_x koji se zove "a" u 2D
    a = zakorak_na_stepenicu/np.sqrt(np.power(vektor_x[0], 2) + np.power(vektor_x[1], 2))
    vektor_x_normiran = [vektor_x[0]*a, vektor_x[1]*a, 0.0]

    vektor_pozicije = [vektor_x_normiran[0] + vektor_translacije[0], vektor_x_normiran[1] + vektor_translacije[1], vektor_x_normiran[2] + vektor_translacije[2]]

    target = [vektor_pozicije[0], vektor_pozicije[1], vektor_pozicije[2], 0.0, 0.0, 0.0]

    # ispruzi lijevu nogu
    motion.setPositions(leg, frame, target, speed, 7)


def leg_y(motion, speed, zakorak_na_stepenicu, leg, system):
    # provjera koji koordinatni je u pitanju
    if system == "Torso":
        frame = 0
    elif system == "World":
        frame = 1
    elif system == "Robot":
        frame = 2

    # matrica transformacija iz koordinatnog sustava world u lijevu nogu
    T1 = motion.getTransform(leg, frame, True)
    T1 = np.asarray(T1)
    T1 = np.reshape(T1, (4, 4))

    # transformacija koordinatnih sustava racunamo promjenu iz pocetne tocke noge do konacne tocke noge vektor i bacamo u funkciju
    vektor_translacije = [T1[0][3], T1[1][3], T1[2][3]]

    # zapis koordinatne osi lijeve noge u koordinatama robot world
    vektor_y = [T1[0][1], T1[1][1], T1[2][1]]

    # sad trazim faktor skaliranja vektora_x koji se zove "a" u 2D
    a = zakorak_na_stepenicu/np.sqrt(np.power(vektor_y[0], 2) + np.power(vektor_y[1], 2))
    vektor_y_normiran = [vektor_y[0]*a, vektor_y[1]*a, 0.0]

    vektor_pozicije = [vektor_y_normiran[0] + vektor_translacije[0], vektor_y_normiran[1] + vektor_translacije[1], vektor_y_normiran[2] + vektor_translacije[2]]

    target = [vektor_pozicije[0], vektor_pozicije[1], vektor_pozicije[2], 0.0, 0.0, 0.0]

    # skreni lijevu nogu
    motion.setPositions(leg, frame, target, speed, 7)


def leg_z(motion, speed, visina, leg, system):
    # provjera koji koordinatni je u pitanju
    if system == "Torso":
        frame = 0
    elif system == "World":
        frame = 1
    elif system == "Robot":
        frame = 2

    # matrica transformacija iz koordinatnog sustava world u lijevu nogu
    T1 = motion.getTransform(leg, frame, True)
    T1 = np.asarray(T1)
    T1 = np.reshape(T1, (4, 4))

    # trazimo vektor translacije koordinatnih sustava
    vektor_translacije = [T1[0][3], T1[1][3], T1[2][3]]

    vektor_z = [T1[0][2], T1[1][2], T1[2][2]]

    # sad trazim faktor skaliranja vektora_z koji se zove a
    a = visina/np.sqrt(np.power(vektor_z[0], 2) + np.power(vektor_z[1], 2) + np.power(vektor_z[2], 2))
    vektor_z_normiran = [vektor_z[0]*a, vektor_z[1]*a, vektor_z[2]*a]

    vektor_pozicije = [vektor_z_normiran[0] + vektor_translacije[0], vektor_z_normiran[1] + vektor_translacije[1], vektor_z_normiran[2] + vektor_translacije[2]]

    target = [vektor_pozicije[0], vektor_pozicije[1], vektor_pozicije[2], 0.0, 0.0, 0.0]

    # podizanje ili spustanje lijeve noge
    motion.setPositions(leg, frame, target, speed, 7)


def leg_rotate_z(motion, speed, angle, leg, system):
    # provjera koji koordinatni je u pitanju
    if system == "Torso":
        frame = 0
    elif system == "World":
        frame = 1
    elif system == "Robot":
        frame = 2

    position = motion.getPosition(leg, frame, True)

    position[5] = position[5]+angle*almath.TO_RAD

    motion.setPositions(leg, frame, position, speed, 63)  # 63 za oba 56 za rotaciju


def leg_up(motion, speed, distance, leg, system):
    # provjera koji koordinatni je u pitanju
    if system == "Torso":
        frame = 0
    elif system == "World":
        frame = 1
    elif system == "Robot":
        frame = 2

    position = motion.getPosition(leg, frame, True)

    position[2] = position[2] + distance

    motion.setPositions(leg, frame, position, speed, 7)  # 63 za oba 56 za rotaciju


def torso_x(motion, speed, ispruzi_torzo):
    # matrica transformacija iz koordinatnog sustava world u Torso
    T1T = motion.getTransform("Torso", 1, True)
    T1T = np.asarray(T1T)
    T1T = np.reshape(T1T, (4, 4))

    # transformacija koordinatnih sustava vektor translacije koordinatnih
    vektor_translacije = [T1T[0][3], T1T[1][3], T1T[2][3]]

    # zapis x koordinatne torza u koordinatama robot world
    vektor_x = [T1T[0][0], T1T[1][0], T1T[2][0]]

    # sad trazim faktor skaliranja vektora_x koji se zove a 3D
    a = ispruzi_torzo/np.sqrt(np.power(vektor_x[0], 2) + np.power(vektor_x[1], 2) + np.power(vektor_x[2], 2))
    vektor_x_normiran = [vektor_x[0]*a, vektor_x[1]*a, vektor_x[2]*a]

    # ovo je vektor promjene, di se se nalaziti torzo u koordinatama world
    vektor_pozicije = [vektor_x_normiran[0] + vektor_translacije[0], vektor_x_normiran[1] + vektor_translacije[1], vektor_x_normiran[2] + vektor_translacije[2]]

    target = [vektor_pozicije[0], vektor_pozicije[1], vektor_pozicije[2], 0.0, 0.0, 0.0]

    positionChange = [vektor_x_normiran[0], vektor_x_normiran[1], vektor_x_normiran[2], 0.0, 0.0, 0.0]

    # ispravljanje torsa koristi se jedna od tri funkcije
    #motion.setPositions("Torso", 1, target, 0.5, 7)  # konacna pozicija
    #motion.positionInterpolations("Torso", 1, target, 7, 8)  #konacna pozicija ovo nevalja
    motion.changePosition("Torso", 1, positionChange, speed, 7)  #promjena pozicije


def torso_y(motion, speed, skreni_torzo):
    # matrica transformacija iz koordinatnog sustava world u Torso
    T1T = motion.getTransform("Torso", 1, True)
    T1T = np.asarray(T1T)
    T1T = np.reshape(T1T, (4, 4))

    # transformacija koordinatnih sustava vektor translacije koordinatnih
    vektor_translacije = [T1T[0][3], T1T[1][3], T1T[2][3]]

    # zapis y koordinatne torza u koordinatama robot world
    vektor_y = [T1T[0][1], T1T[1][1], T1T[2][1]]

    # sad trazim faktor skaliranja vektora_x koji se zove a 3D
    a = skreni_torzo/np.sqrt(np.power(vektor_y[0], 2) + np.power(vektor_y[1], 2) + np.power(vektor_y[2], 2))
    vektor_y_normiran = [vektor_y[0]*a, vektor_y[1]*a, vektor_y[2]*a]

    # ovo je vektor promjene, di se se nalaziti torzo u koordinatama world
    vektor_pozicije = [vektor_y_normiran[0] + vektor_translacije[0], vektor_y_normiran[1] + vektor_translacije[1], vektor_y_normiran[2] + vektor_translacije[2]]

    target = [vektor_pozicije[0], vektor_pozicije[1], vektor_pozicije[2], 0.0, 0.0, 0.0]

    positionChange = [vektor_y_normiran[0], vektor_y_normiran[1], vektor_y_normiran[2], 0.0, 0.0, 0.0]

    # ispravljanje torsa koristi se jedna od tri funkcije
    #motion.setPositions("Torso", 1, target, 0.5, 7)  # konacna pozicija
    #motion.positionInterpolations("Torso", 1, target, 7, 8)  #konacna pozicija ovo nevalja
    motion.changePosition("Torso", 1, positionChange, speed, 7)  #promjena pozicije non-blocking


def torso_z(motion, speed, ispruzi_torzo):
    # matrica transformacija iz koordinatnog sustava world u Torso
    T1T = motion.getTransform("Torso", 1, True)
    T1T = np.asarray(T1T)
    T1T = np.reshape(T1T, (4, 4))

    # transformacija koordinatnih sustava vektor translacije koordinatnih
    vektor_translacije = [T1T[0][3], T1T[1][3], T1T[2][3]]

    # zapis z koordinatne torza u koordinatama robot world
    vektor_z = [T1T[0][2], T1T[1][2], T1T[2][2]]

    # sad trazim faktor skaliranja vektora_x koji se zove a 3D
    a = ispruzi_torzo/np.sqrt(np.power(vektor_z[0], 2) + np.power(vektor_z[1], 2) + np.power(vektor_z[2], 2))
    vektor_z_normiran = [vektor_z[0]*a, vektor_z[1]*a, vektor_z[2]*a]

    # ovo je vektor promjene, di se se nalaziti torzo u koordinatama world
    vektor_pozicije = [vektor_z_normiran[0] + vektor_translacije[0], vektor_z_normiran[1] + vektor_translacije[1], vektor_z_normiran[2] + vektor_translacije[2]]

    target = [vektor_pozicije[0], vektor_pozicije[1], vektor_pozicije[2], 0.0, 0.0, 0.0]

    positionChange = [vektor_z_normiran[0], vektor_z_normiran[1], vektor_z_normiran[2], 0.0, 0.0, 0.0]

    # ispravljanje torsa koristi se jedna od tri funkcije
    #motion.setPositions("Torso", 1, target, 0.5, 7)  # konacna pozicija
    #motion.positionInterpolations("Torso", 1, target, 7, 8)  #konacna pozicija ovo nevalja
    motion.changePosition("Torso", 1, positionChange, speed, 7)  #promjena pozicije
