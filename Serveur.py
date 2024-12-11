from socket import *
import sys
from mrpiZ_lib import *
import time

A_GAUCHE: int = 1
A_DROITE: int = -1

AVANT: int = 0
ARRIERE: int = 1

VITESSE_MAX: int = 100
VITESSE_MIN: int = 25

class deplacement:
    def _init_(self):
        self.vitesse_gauche: int = VITESSE_MAX
        self.vitesse_droite: int = VITESSE_MAX
        self.sens_gauche: int = AVANT
        self.sens_droit: int = AVANT

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

    def arret(self):
        motorLeft(0, 0)
        motorRight(0, 0)
        return True

class capteur:
    def _init_(self):
        self.__p2: int = proxSensor(2)
        self.__p3: int = proxSensor(3)
        self.__p4: int = proxSensor(4)

    def get_p2(self) -> int:
        return self.__p2

    def get_p3(self) -> int:
        return self.__p3

    def get_p4(self) -> int:
        return self.__p4

class autonome(deplacement, capteur):
    def _init_(self):
        deplacement._init_(self)
        capteur._init_(self)

    def course(self):
        while True:
            p2 = self.get_p2()
            p3 = self.get_p3()
            p4 = self.get_p4()

            if p3 < 100:  # Obstacle droit devant
                self.tourner_gauche()
            elif p2 < 100:  # Obstacle à gauche
                self.tourner_droite()
            elif p4 < 100:  # Obstacle à droite
                self.tourner_gauche()
            else:
                self.avancer()
            time.sleep(0.01)

    def arret_autonome(self):
        self.arret()
        self.__sortie = True
        return self.__sortie

class ServiceEcoute:
    def _init_(self, port_serveur: int) -> None:
        self.__socket_ecoute: socket = socket(AF_INET, SOCK_STREAM)
        self.__socket_ecoute.bind(('', port_serveur))
        self.__socket_ecoute.listen(1)
        print(f"écoute sur le port :  {port_serveur}")

    def attente(self) -> socket:
        print("Attente d'une connexion ... ")
        client_socket, client_address = self.__socket_ecoute.accept()
        print(f"connexion avec le client : {client_address}")
        return client_socket

class ServiceEchange:
    def _init_(self, socket_echange: socket, robot: deplacement, course_autonome: autonome) -> None:
        self.__socket_echange = socket_echange
        self.robot = robot
        self.course_autonome = course_autonome

    def envoyer(self, msg: str) -> None:
        self.__socket_echange.send(msg.encode('utf-8'))

    def recevoir(self) -> str:
        tab_octets = self.__socket_echange.recv(1024)
        return tab_octets.decode(encoding='utf-8')

    def echange(self) -> None:
        fin: bool = False
        while not fin:
            tab_octets = self.__socket_echange.recv(1024)
            commande = tab_octets.decode(encoding="utf-8")

            if commande == "z":
                self.robot.avancer()
            elif commande == "s":
                self.robot.reculer()
            elif commande == "q":
                self.robot.tourner_gauche()
            elif commande == "d":
                self.robot.tourner_droite()
            elif commande == "course_autonome":
                self.course_autonome.course()
            elif commande == "arret_course_autonome":
                self.course_autonome.arret_autonome()
            elif commande == "fin":
                self.robot.arret()
                fin = True
            elif commande == "c":
                capteur.get_p2(self)

            # envoie données capteurs au client
            msg_serveur: str = f"distance capteur 2 : {proxSensor(2)}\n distance capteur 3 : {proxSensor(3)}\n distance capteur 4 : {proxSensor(4)}\n"
            tab_octets = msg_serveur.encode(encoding="utf-8")
            self.__socket_echange.send(tab_octets)

    def arret(self) -> None:
        self.__socket_echange.close()

if _name_ == "_main_":
    # declaration des variables
    Robot = deplacement()
    Capteur = capteur()
    Course_autonome = autonome()
    port_ecoute: int = None
    service_ecoute: ServiceEcoute = None
    socket_client: socket = None
    service_echange: ServiceEchange = None
    # lecture des parametres (le numero de port)
    if len(sys.argv) == 2:
        port_ecoute = int(sys.argv[1])
    else:
        port_ecoute = 5000
    try:
        service_ecoute = ServiceEcoute(port_ecoute)
        socket_client = service_ecoute.attente()
        service_echange = ServiceEchange(socket_client, Robot, Course_autonome)
        service_echange.echange()
    except Exception as ex:
        print("erreur : ", ex)