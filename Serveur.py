#!/usr/bin/python
from mrpiZ_lib import *
import time, os
from typing import Tuple

A_GAUCHE : int = 1
A_DROITE : int = -1

AVANT : int = 0
ARRIERE : int = 1

VITESSE_MAX:int = 100
VITESSE_MIN:int = 25

if __name__ == "__main__":
    vitesse_gauche:int
    vitesse_droite:int
    sens_gauche:int
    sens_droit:int
    fin:bool = False
    try:
        vitesse_gauche = VITESSE_MAX
        vitesse_droite = VITESSE_MAX
        sens_gauche = AVANT
        sens_droit = AVANT

        motorLeft(sens_gauche, vitesse_gauche)
        motorRight(sens_droit, vitesse_droite)
        time.sleep(2)

        sens_gauche = ARRIERE
        sens_droit = ARRIERE
        motorLeft(sens_gauche, vitesse_gauche)
        motorRight(sens_droit, vitesse_droite)
        time.sleep(2)

        sens_gauche = AVANT
        sens_droit = ARRIERE
        motorLeft(sens_gauche, vitesse_gauche)
        motorRight(sens_droit, vitesse_droite)
        time.sleep(2)

        sens_gauche = ARRIERE
        sens_droit = AVANT
        motorLeft(sens_gauche, vitesse_gauche)
        motorRight(sens_droit, vitesse_droite)
        
        time.sleep(2)

        stop()
    except KeyboardInterrupt as ex:
        stop()
