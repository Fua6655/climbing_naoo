from naoqi import ALProxy
import argparse
import time
import searching
import walking
import image_processing
import climbing


def main(ip, port):
    motionProxy = ALProxy("ALMotion", ip, port)
    postureProxy = ALProxy("ALRobotPosture", ip, port)

    postureProxy.goToPosture("StandInit", 0.5)

    Yaw_angle = 0
    Pitch_angle = -15
    searching.set_camera_angle(motionProxy, Yaw_angle, Pitch_angle)
    time.sleep(5)

    theta_horizont = [89.5, 90.5]
    theta_kose = [10, 25, 160, 165]
    faktor_odbacivanja_linija = 8
    faktor_osjetljivosti_stepenica = 70  # sto je majni faktor, to su osjetljivije
    parametri_stepenica, tocke_3D, broj_stepenica = image_processing.main(ip, port, theta_horizont, theta_kose, faktor_odbacivanja_linija, faktor_osjetljivosti_stepenica)

    walking.main(motionProxy, parametri_stepenica[0][0][0]-0.3, 0, 0)


    # penjanje na stepenice koliko ih ima
    for i in range(0, broj_stepenica, 1):
        climbing.main(motionProxy, postureProxy, parametri_stepenica)
        walking.main(motionProxy, 0.05, 0.01, 0)



    time.sleep(3)
    motionProxy.rest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="169.254.89.225", help="Robot ip address") #Edith
    #parser.add_argument("--ip", type=str, default="169.254.28.144", help="Robot ip address") #Her Flick
    #parser.add_argument("--ip", type=str, default="127.0.0.1", help="Robot ip address") #V-rep
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)
