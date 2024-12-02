#!/usr/bin/python
from mrpiZ_lib import *
import time

# seuil de la detection obstacle
seuil = 50

while 1:
    p2 = proxSensor(2)
    p4 = proxSensor(4)
    print "%d %d " %(p2,p4)

    if ((p2 < seuil) or (p4 < seuil)):
        stop() # arreter le robot
    else:
        forward(30) # avancer le robot

    time.sleep(0.2)