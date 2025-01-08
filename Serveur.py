from socket import *
import sys
import mrpiZ
import time
import threading

A_GAUCHE: int = 1
A_DROITE: int = -1

AVANT: int = 0
ARRIERE: int = 1

VITESSE_MAX_gauche: float = 94
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
        
    def motor_left_avant(self, vitesse: int):
        self.sens_gauche = AVANT
        self.vitesse_gauche = vitesse
        mrpiZ.motorLeft(self.sens_gauche, self.vitesse_gauche)
        
    def motor_left_arriere(self, vitesse: int):
        self.sens_gauche = ARRIERE
        self.vitesse_gauche = vitesse
        mrpiZ.motorLeft(self.sens_gauche, self.vitesse_gauche)    
        
    def motor_right_avant(self, vitesse: int):
        self.sens_droit = AVANT
        self.vitesse_droite = vitesse
        mrpiZ.motorRight(self.sens_droit, self.vitesse_droite)
        
    def motor_right_arriere(self, vitesse: int):
        self.sens_droit = ARRIERE
        self.vitesse_droite = vitesse
        mrpiZ.motorRight(self.sens_droit, self.vitesse_droite)

    def arret(self):
        mrpiZ.motorLeft(0, 0)
        mrpiZ.motorRight(0, 0)

class capteur:
    def __init__(self):
        pass

    def get_all(self) -> list[int]:
        try:
            p2 = int(mrpiZ.proxSensor(2))
            p3 = int(mrpiZ.proxSensor(3))
            p4 = int(mrpiZ.proxSensor(4))
            print(p2, p3, p4)
            return [p2, p3, p4]
        except ValueError as e:
            print(f"Erreur de conversion des données du capteur: {e}")
            return [-1, -1, -1]  # Valeurs par défaut en cas d'erreur

class autonome:
    def __init__(self):
        self.__arret : bool = False
        self.__thread = None
        self.__deplacement = deplacement()
        self.__capteur = capteur()
        self.__list_capteurs = list()

    def course(self):
        while self.__arret:
            self.__list_capteurs = self.__capteur.get_all()
            p2: int = self.__list_capteurs[0]
            p3: int = self.__list_capteurs[1]
            p4: int = self.__list_capteurs[2]
            
            if p4 < 40 and p3 < 50 and p2 < 40:
                self.__deplacement.motor_left_arriere(20)
                self.__deplacement.motor_right_avant(100)
            elif p3 < 50:  # Obstacle droit devant
                self.__deplacement.motor_left_arriere(20)
                self.__deplacement.motor_right_avant(100)
            elif p2 < 50:  # Obstacle à gauche
                self.__deplacement.motor_left_avant(100)
                self.__deplacement.motor_right_avant(20)
            elif p4 < 50:  # Obstacle à droite
                self.__deplacement.motor_right_avant(100)
                self.__deplacement.motor_left_avant(20)
            else:
                self.__deplacement.avancer()
            time.sleep(0.5)
            #print(self.get_autonome())
            #print(self.get_all_autonome())
            

    def start_course(self):
        self.__thread = threading.Thread(target=self.course)
        self.__thread.start()

    def arret_autonome(self):
        self.__arret = True
        if self.__thread is not None:
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
        self.__arret : bool = False

    def changer_couleur(self):
        while  not self.__arret:
            
            mrpiZ.ledRGB(0, 0, 255)
            time.sleep(0.1)
            mrpiZ.ledRGB(0,255,255)
            time.sleep(0.1)

    def start(self):
        self.__thread = threading.Thread(target=self.changer_couleur)
        self.__thread.start()

    def stop(self):
        self.__arret = True
        if self.__thread is not None:
            self.__thread = None
        

class Buzzer:
    def __init__(self):
        self.__thread = None
        self.__arret : bool = False
        
    def sonnerie(self):
        while not self.__arret:
            mrpiZ.buzzer(1000)
            time.sleep(0.1)
            mrpiZ.buzzer(10000)
            time.sleep(0.1)
            
    def start(self):
        self.__thread = threading.Thread(target=self.sonnerie)
        self.__thread.start()
        
    def stop(self):
        self.__arret = True
        if self.__thread is not None:
            self.__thread = None
        mrpiZ.buzzerStop()

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
        self.__buzzer = Buzzer()

    def envoyer(self, msg: str) -> None:
        self.__socket_echange.send(msg.encode('utf-8'))

    def recevoir(self) -> str:
        tab_octets = self.__socket_echange.recv(1024)
        return tab_octets.decode(encoding='utf-8')

    def echange(self) -> None:
        fin: bool = False
        while not fin:
            tab_octets = self.__socket_echange.recv(1024) # bloquant
            commande = tab_octets.decode(encoding="utf-8")
            print(commande)
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
                if (self.__course_autonome.get_autonome() == None):
                    tab_octets = self.__capteur.get_all()
                elif (self.__course_autonome.get_autonome() != None):
                    tab_octets = self.__course_autonome.get_all_autonome()
                #print(self.__course_autonome.get_autonome())
                #print(f"{self.__course_autonome.get_all_autonome()} pour le mode autonome")
                #print(f"{self.__capteur.get_all()} pour le mode manuel")
                tab_octets = str(tab_octets).encode("utf-8")
                self.__socket_echange.send(tab_octets)
            elif commande == "bat":
                tab_octets = self.__option.get_batterie()
                tab_octets = str(tab_octets).encode("utf-8")
                self.__socket_echange.send(tab_octets)
            elif commande == "police_on":
                self.__led_rgb.start()
                self.__buzzer.start()
                tab_octets = commande.encode("utf-8")
                self.__socket_echange.send(tab_octets)
            elif commande == "police_off":
                self.__led_rgb.stop()
                self.__buzzer.stop()
                tab_octets = commande.encode("utf-8")
                self.__socket_echange.send(tab_octets)

            # envoie données capteurs au client
            '''msg_serveur: str = f"distance capteur 2 : {mrpiZ.proxSensor(2)}\n distance capteur 3 : {mrpiZ.proxSensor(3)}\n distance capteur 4 : {mrpiZ.proxSensor(4)}\n"
            tab_octets = msg_serveur.encode(encoding="utf-8")
            self.__socket_echange.send(tab_octets)
            msg_serveur: str = f"batterie : {mrpiZ.battery()}\n"'''

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