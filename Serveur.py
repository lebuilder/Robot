from socket import *
import sys
import mrpiZ
import time
import threading

A_GAUCHE: int = 1
A_DROITE: int = -1

AVANT: int = 0
ARRIERE: int = 1

VITESSE_MAX_gauche: float = 99.25
VITESSE_MAX_droite: int = 100
VITESSE_MIN: int = 25

class deplacement:
    def __init__(self):
        self.vitesse_gauche: int = VITESSE_MAX_gauche
        self.vitesse_droite: int = VITESSE_MAX_droite
        self.sens_gauche: int = AVANT
        self.sens_droit: int = AVANT

    def avancer(self):
        self.sens_gauche = AVANT
        self.sens_droit = AVANT
        mrpiZ.motorLeft(self.sens_gauche, self.vitesse_gauche)
        mrpiZ.motorRight(self.sens_droit, self.vitesse_droite)

    def reculer(self):
        self.sens_gauche = ARRIERE
        self.sens_droit = ARRIERE
        mrpiZ.motorLeft(self.sens_gauche, self.vitesse_gauche)
        mrpiZ.motorRight(self.sens_droit, self.vitesse_droite)

    def tourner_gauche(self):
        self.sens_gauche = ARRIERE
        self.sens_droit = AVANT
        mrpiZ.motorLeft(self.sens_gauche, self.vitesse_gauche)
        mrpiZ.motorRight(self.sens_droit, self.vitesse_droite)

    def tourner_droite(self):
        self.sens_gauche = AVANT
        self.sens_droit = ARRIERE
        mrpiZ.motorLeft(self.sens_gauche, self.vitesse_gauche)
        mrpiZ.motorRight(self.sens_droit, self.vitesse_droite)

    def arret(self):
        mrpiZ.motorLeft(0, 0)
        mrpiZ.motorRight(0, 0)

class capteur:
    def __init__(self):
        self.__p2: int = mrpiZ.proxSensor(2)
        self.__p3: int = mrpiZ.proxSensor(3)
        self.__p4: int = mrpiZ.proxSensor(4)

    def get_p2(self) -> int:
        return mrpiZ.proxSensor(2)

    def get_p3(self) -> int:
        return mrpiZ.proxSensor(3)

    def get_p4(self) -> int:
        return mrpiZ.proxSensor(4)

    def get_all(self) -> list[float]:
        return [mrpiZ.proxSensor(2), mrpiZ.proxSensor(3), mrpiZ.proxSensor(4)]

class autonome:
    def __init__(self):
        self.__arret = threading.Event()
        self.__thread = None
        self.__deplacement = deplacement()
        self.__capteur = capteur()
        self.__list_capteurs = list()

    def course(self):
        while not self.__arret.is_set():
            self.__list_capteurs = self.__capteur.get_all()
            p2: int = self.__list_capteurs[0]
            p3: int = self.__list_capteurs[1]
            p4: int = self.__list_capteurs[2]
            
            if p4 < 40 and p3 < 40 and p2 < 40:
                self.__deplacement.reculer()
                time.sleep(1)
                self.__deplacement.tourner_droite()
            elif p3 < 50:  # Obstacle droit devant
                self.__deplacement.tourner_gauche()
            elif p2 < 50:  # Obstacle à gauche
                self.__deplacement.tourner_droite()
            elif p4 < 50:  # Obstacle à droite
                self.__deplacement.tourner_gauche()
            else:
                self.__deplacement.avancer()
            time.sleep(0.25)
            

    def start_course(self):
        self.__thread = threading.Thread(target=self.course)
        self.__thread.start()

    def arret_autonome(self):
        self.__arret.set()
        if self.__thread is not None:
            self.__thread.join()
            self.__thread = None
        self.__deplacement.arret()
        
    def get_autonome(self)-> bool:
        return self.__thread
    
    def get_all_autonome(self) -> list[int]:
        return self.__list_capteurs

class Option:
    def __init__(self) -> None:
        self.__batterie: float = mrpiZ.battery()
        
    def get_batterie(self) -> float:
        return self.__batterie

class LedRGB:
    def __init__(self):
        self.__thread = None
        self.__arret = threading.Event()

    def changer_couleur(self):
        while not self.__arret.is_set():
            mrpiZ.ledRGB(0, 0, 255)  # Bleu
            time.sleep(1)
            mrpiZ.ledRGB(255, 255, 255)  # Blanc
            time.sleep(1)
            mrpiZ.ledRGB(255, 0, 0)  # Rouge
            time.sleep(1)

    def start(self):
        self.__arret.clear()
        self.__thread = threading.Thread(target=self.changer_couleur)
        self.__thread.start()

    def stop(self):
        self.__arret.set()
        if self.__thread is not None:
            self.__thread.join()

class ServiceEcoute:
    def __init__(self, port_serveur: int) -> None:
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
    def __init__(self, socket_echange: socket) -> None:
        self.__socket_echange = socket_echange
        self.__robot : deplacement = deplacement()
        self.__option : Option = Option()
        self.__course_autonome : autonome = autonome()
        self.__capteur : capteur = capteur()
        self.__led_rgb = LedRGB()

    def envoyer(self, msg: str) -> None:
        self.__socket_echange.send(msg.encode('utf-8'))

    def recevoir(self) -> str:
        tab_octets = self.__socket_echange.recv(1024)
        return tab_octets.decode(encoding='utf-8')

    def echange(self) -> None:
        fin: bool = False
        self.__led_rgb.start()  # Démarrer le thread pour la LED RGB
        while not fin:
            tab_octets = self.__socket_echange.recv(1024) # bloquant
            commande = tab_octets.decode(encoding="utf-8")

            if commande == "avancer":
                self.__robot.avancer()
                tab_octets = commande.encode("utf-8")
                self.__socket_echange.send(tab_octets)
            elif commande == "reculer":
                self.__robot.reculer()
                tab_octets = commande.encode("utf-8")
                self.__socket_echange.send(tab_octets)
            elif commande == "gauche":
                self.__robot.tourner_gauche()
                tab_octets = commande.encode("utf-8")
                self.__socket_echange.send(tab_octets)
            elif commande == "droite":
                self.__robot.tourner_droite()
                tab_octets = commande.encode("utf-8")
                self.__socket_echange.send(tab_octets)
            elif commande == "mode automatique":
                self.__course_autonome.start_course()
                tab_octets = commande.encode("utf-8")
                self.__socket_echange.send(tab_octets)
            elif commande == "fin":
                self.__robot.arret()
                tab_octets = commande.encode("utf-8")
                self.__socket_echange.send(tab_octets)
                fin = True
                self.__course_autonome.arret_autonome()
            elif commande == "mode manuel":
                self.__course_autonome.arret_autonome()
                tab_octets = commande.encode("utf-8")
                self.__socket_echange.send(tab_octets)
            elif commande == "stop":
                self.__robot.arret()
                self.__course_autonome.arret_autonome()
                tab_octets = commande.encode("utf-8")
                self.__socket_echange.send(tab_octets)
            elif commande == "capteur":
                if self.__course_autonome.get_autonome() == None:
                    tab_octets = self.__capteur.get_all()
                else:
                    tab_octets = self.__course_autonome.get_all_autonome()
                tab_octets = str(tab_octets).encode("utf-8")
                self.__socket_echange.send(tab_octets)
            elif commande == "bat":
                tab_octets = self.__option.get_batterie()
                tab_octets = str(tab_octets).encode("utf-8")
                self.__socket_echange.send(tab_octets)

            # envoie données capteurs au client
            '''msg_serveur: str = f"distance capteur 2 : {mrpiZ.proxSensor(2)}\n distance capteur 3 : {mrpiZ.proxSensor(3)}\n distance capteur 4 : {mrpiZ.proxSensor(4)}\n"
            tab_octets = msg_serveur.encode(encoding="utf-8")
            self.__socket_echange.send(tab_octets)
            msg_serveur: str = f"batterie : {mrpiZ.battery()}\n"'''

        self.__led_rgb.stop()  # Arrêter le thread pour la LED RGB

    def arret(self) -> None:
        self.__socket_echange.close()

if __name__ == "__main__":
    # declaration des variables
    Robot = deplacement()
    #Capteur = capteur()
    #Course_autonome = autonome()
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
        service_echange = ServiceEchange(socket_client)
        service_echange.echange()
    except Exception as ex:
        print("erreur : ", ex)