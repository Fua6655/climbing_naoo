import almath


def set_camera_angle(motionProxy, Yaw_angle, Pitch_angle):
    # Set camera angle for taking the picture
    # Angle in Degrees
    motionProxy.setStiffnesses("Head", 1.0)

    Yaw_current = motionProxy.getAngles("HeadYaw", True)
    Pitch_current = motionProxy.getAngles("HeadPitch", True)

    names  = ["HeadYaw", "HeadPitch"]
    angles  = [Yaw_current[0]+Yaw_angle*almath.TO_RAD, Pitch_current[0]+Pitch_angle*almath.TO_RAD]
    fractionMaxSpeed  = 0.2
    motionProxy.setAngles(names, angles, fractionMaxSpeed)


############################################# Optimal spot
def finding_optimal_spot(tocke_3D):
    lijeva_tocka = tocke_3D[0][0][0]
    print lijeva_tocka

    desna_tocka = tocke_3D[0][0][1]
    print desna_tocka
    X = (lijeva_tocka[0] + desna_tocka[0])/2 - 0.70
    Y = (lijeva_tocka[1] - desna_tocka[1])/2 + desna_tocka[1]
    Theta = 0

    return X, Y, Theta



