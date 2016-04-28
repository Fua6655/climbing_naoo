#!/usr/bin/python
import argparse
from naoqi import ALProxy

def main(ip, port):
    motionProxy  = ALProxy("ALMotion", ip, port)

     # Go to rest position
    motionProxy.rest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="169.254.89.225", help="Robot ip address") #Edith
    #parser.add_argument("--ip", type=str, default="169.254.28.144", help="Robot ip address") #Her Flick
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)
