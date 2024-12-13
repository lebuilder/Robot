
#!/usr/bin/python
from mrpiZ import *
import time, os
from typing import Tuple
import keyboard

A_GAUCHE : int = 1
A_DROITE : int = -1

AVANT : int = 0
ARRIERE : int = 1

VITESSE_MAX:int = 100
VITESSE_MIN:int = 25

class deplacement:
    def __init__(self):
        self.vitesse_gauche:int = VITESSE_MAX
        self.vitesse_droite:int = VITESSE_MAX
        self.sens_gauche:int = AVANT
        self.sens_droit:int = AVANT
        
    def avancer(self):
        self.sens_gauche = AVANT
        self.sens_droit = AVANT
        motorLeft(self.sens_gauche, self.vitesse_gauche)
        motorRight(self.sens_droit, self.vitesse_droite)

    def reculer(self):
        self.sens_gauche = ARRIERE
        self.sens_droit = ARRIERE
        motorLeft(self.sens_gauche, self.vitesse_gauche)
        motorRight(self.sens_droit, self.vitesse_droite)

    def tourner_gauche(self):
        self.sens_gauche = ARRIERE
        self.sens_droit = AVANT
        motorLeft(self.sens_gauche, self.vitesse_gauche)
        motorRight(self.sens_droit, self.vitesse_droite)

    def tourner_droite(self):
        self.sens_gauche = AVANT
        self.sens_droit = ARRIERE
        motorLeft(self.sens_gauche, self.vitesse_gauche)
        motorRight(self.sens_droit, self.vitesse_droite)
        

if __name__ == "__main__":
    Robot = deplacement()
    
    while True:
        if keyboard.is_pressed('z'):
            deplacement.avancer()
        elif keyboard.is_pressed('s'):
            deplacement.reculer()
        elif keyboard.is_pressed('q'):
            deplacement.tourner_gauche()
        elif keyboard.is_pressed('d'):
            deplacement.tourner_droite()
        time.sleep(0.1)
