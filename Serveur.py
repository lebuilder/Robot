from socket import *
import sys
import mrpiZ
import time
import threading

# Constantes pour les directions
A_GAUCHE: int = 1
A_DROITE: int = -1

AVANT: int = 0
ARRIERE: int = 1

# Constantes pour les vitesses
VITESSE_MAX_gauche: float = 94
VITESSE_MAX_droite: int = 100
VITESSE_MIN: int = 25

# Classe pour gérer les déplacements du robot
class deplacement:
    def __init__(self):
        self.vitesse_gauche: int = VITESSE_MAX_gauche
        self.vitesse_droite: int = VITESSE_MAX_droite
        self.sens_gauche: int = AVANT
        self.sens_droit: int = AVANT

    # Méthode pour avancer
    def avancer(self):
        self.sens_gauche = AVANT
        self.sens_droit = AVANT
        mrpiZ.motorLeft(self.sens_gauche, self.vitesse_gauche)
        mrpiZ.motorRight(self.sens_droit, self.vitesse_droite)

    # Méthode pour reculer
    def reculer(self):
        self.sens_gauche = ARRIERE
        self.sens_droit = ARRIERE
        mrpiZ.motorLeft(self.sens_gauche, self.vitesse_gauche)
        mrpiZ.motorRight(self.sens_droit, self.vitesse_droite)

    # Méthode pour tourner à gauche
    def tourner_gauche(self):
        self.sens_gauche = ARRIERE
        self.sens_droit = AVANT
        mrpiZ.motorLeft(self.sens_gauche, self.vitesse_gauche)
        mrpiZ.motorRight(self.sens_droit, self.vitesse_droite)

    # Méthode pour tourner à droite
    def tourner_droite(self):
        self.sens_gauche = AVANT
        self.sens_droit = ARRIERE
        mrpiZ.motorLeft(self.sens_gauche, self.vitesse_gauche)
        mrpiZ.motorRight(self.sens_droit, self.vitesse_droite)
        
    # Méthode pour contrôler le moteur gauche en avant
    def motor_left_avant(self, vitesse: int):
        self.sens_gauche = AVANT
        vitesse_gauche = vitesse
        mrpiZ.motorLeft(self.sens_gauche, vitesse_gauche)
        
    # Méthode pour contrôler le moteur gauche en arrière
    def motor_left_arriere(self, vitesse: int):
        self.sens_gauche = ARRIERE
        vitesse_gauche = vitesse
        mrpiZ.motorLeft(self.sens_gauche, vitesse_gauche)    
        
    # Méthode pour contrôler le moteur droit en avant
    def motor_right_avant(self, vitesse: int):
        self.sens_droit = AVANT
        vitesse_droite = vitesse
        mrpiZ.motorRight(self.sens_droit, vitesse_droite)
        
    # Méthode pour contrôler le moteur droit en arrière
    def motor_right_arriere(self, vitesse: int):
        self.sens_droit = ARRIERE
        vitesse_droite = vitesse
        mrpiZ.motorRight(self.sens_droit, vitesse_droite)

    # Méthode pour arrêter le robot
    def arret(self):
        mrpiZ.motorLeft(0, 0)
        mrpiZ.motorRight(0, 0)

# Classe pour gérer les capteurs du robot
class capteur:
    def __init__(self):
        pass

    # Méthode pour obtenir les valeurs de tous les capteurs
    def get_all(self) -> list[int]:
        try:
            p2 = int(mrpiZ.proxSensor(2))
            p3 = int(mrpiZ.proxSensor(3))
            p4 = int(mrpiZ.proxSensor(4))
            #print(p2, p3, p4)
            return [p2, p3, p4]
        except ValueError as e:
            print(f"Erreur de conversion des données du capteur: {e}")
            return [-1, -1, -1]  # Valeurs par défaut en cas d'erreur

# Classe pour gérer le mode autonome du robot
class autonome:
    def __init__(self):
        self.__arret: bool = True
        self.__thread = None
        self.__deplacement = deplacement()
        self.__capteur = capteur()
        self.__list_capteurs = list()

    # Méthode pour la course autonome
    def course(self):
        while self.__arret:
            self.__list_capteurs = self.__capteur.get_all()
            p2: int = self.__list_capteurs[0]
            p3: int = self.__list_capteurs[1]
            p4: int = self.__list_capteurs[2]
            
            if p4 < 100 and p3 < 110 and p2 < 100:
                self.__deplacement.motor_left_arriere(20)
                self.__deplacement.motor_right_avant(100)
            elif p3 < 110:  # Obstacle droit devant
                self.__deplacement.motor_left_arriere(20)
                self.__deplacement.motor_right_avant(100)
            elif p2 < 110:  # Obstacle à gauche
                self.__deplacement.motor_left_avant(100)
                self.__deplacement.motor_right_avant(20)
            elif p4 < 110:  # Obstacle à droite
                self.__deplacement.motor_right_avant(100)
                self.__deplacement.motor_left_avant(20)
            else:
                self.__deplacement.avancer()
            time.sleep(0.25)

    # Méthode pour démarrer la course autonome
    def start_course(self):
        self.__arret = True
        self.__thread = threading.Thread(target=self.course)
        self.__thread.start()

    # Méthode pour arrêter la course autonome
    def arret_autonome(self):
        self.__arret = False
        self.__thread = None
        self.__deplacement.arret()
        
    # Méthode pour vérifier si le mode autonome est actif
    def get_autonome(self) -> bool:
        return self.__thread
    
    # Méthode pour obtenir les valeurs des capteurs en mode autonome
    def get_all_autonome(self) -> list[int]:
        return self.__list_capteurs

# Classe pour gérer les options du robot
class Option:
    def __init__(self) -> None:
        self.__batterie: float = mrpiZ.battery()
        
    # Méthode pour obtenir le niveau de la batterie
    def get_batterie(self) -> float:
        return self.__batterie

# Classe pour gérer la LED RGB du robot
class LedRGB:
    def __init__(self):
        self.__thread = None
        self.__arret: bool = False

    # Méthode pour changer la couleur de la LED
    def changer_couleur(self):
        while not self.__arret:
            mrpiZ.ledRGB(0, 0, 255)
            time.sleep(0.1)
            mrpiZ.ledRGB(0, 255, 255)
            time.sleep(0.1)

    # Méthode pour démarrer le changement de couleur
    def start(self):
        self.__thread = threading.Thread(target=self.changer_couleur)
        self.__thread.start()

    # Méthode pour arrêter le changement de couleur
    def stop(self):
        self.__arret = True
        if self.__thread is not None:
            self.__thread = None

# Classe pour gérer le buzzer du robot
class Buzzer:
    def __init__(self):
        self.__thread = None
        self.__arret: bool = False
        
    # Méthode pour faire sonner le buzzer
    def sonnerie(self):
        # Durées ajustées à 120 BPM
        bpm = 120
        beat_duration = 60 / bpm  # 0.5 seconde par battement
        croche = beat_duration * 0.5  # 0.25 seconde
        noire = beat_duration         # 0.5 seconde
        blanche = beat_duration * 2   # 1 seconde complète

        # Fréquences des notes utilisées (octave 4 et 5)
        Sol = 392  # Sol
        La = 440  # La
        Si = 493  # Si
        Do = 523  # Do
        Ré = 587  # Ré
        Mi = 659  # Mi
        Fa = 698  # Fa

        # Début du Menuet de Mozart (simplifié)
        mrpiZ.buzzer(Sol)  # Sol
        time.sleep(noire)

        mrpiZ.buzzer(La)  # La
        time.sleep(noire)

        mrpiZ.buzzer(Si)  # Si
        time.sleep(noire)

        mrpiZ.buzzer(Do)  # Do
        time.sleep(noire)

        mrpiZ.buzzer(Ré)  # Ré
        time.sleep(noire)

        mrpiZ.buzzer(Mi)  # Mi
        time.sleep(noire)

        mrpiZ.buzzer(Fa)  # Fa
        time.sleep(noire)

        mrpiZ.buzzer(Sol)  # Sol
        time.sleep(blanche)

        # Deuxième phrase musicale
        mrpiZ.buzzer(Sol)  # Sol
        time.sleep(noire)

        mrpiZ.buzzer(Fa)  # Fa
        time.sleep(noire)

        mrpiZ.buzzer(Mi)  # Mi
        time.sleep(noire)

        mrpiZ.buzzer(Ré)  # Ré
        time.sleep(noire)

        mrpiZ.buzzer(Do)  # Do
        time.sleep(noire)

        mrpiZ.buzzer(Si)  # Si
        time.sleep(noire)

        mrpiZ.buzzer(La)  # La
        time.sleep(noire)

        mrpiZ.buzzer(Sol)  # Sol
        time.sleep(blanche)

        # Pause avant de rejouer
        time.sleep(1)
            
    # Méthode pour démarrer la sonnerie
    def start(self):
        self.__thread = threading.Thread(target=self.sonnerie)
        self.__thread.start()
        
    # Méthode pour arrêter la sonnerie
    def stop(self):
        self.__arret = True
        if self.__thread is not None:
            self.__thread = None
        mrpiZ.buzzerStop()

# Classe pour gérer l'écoute des connexions entrantes
class ServiceEcoute:
    def __init__(self, port_serveur: int) -> None:
        self.__socket_ecoute: socket = socket(AF_INET, SOCK_STREAM)
        self.__socket_ecoute.bind(('', port_serveur))
        self.__socket_ecoute.listen(1)
        print(f"écoute sur le port :  {port_serveur}")

    # Méthode pour attendre une connexion
    def attente(self) -> socket:
        print("Attente d'une connexion ... ")
        client_socket, client_address = self.__socket_ecoute.accept()
        print(f"connexion avec le client : {client_address}")
        return client_socket

# Classe pour gérer les échanges avec le client
class ServiceEchange:
    def __init__(self, socket_echange: socket) -> None:
        self.__socket_echange = socket_echange
        self.__robot: deplacement = deplacement()
        self.__option: Option = Option()
        self.__course_autonome: autonome = autonome()
        self.__capteur: capteur = capteur()
        self.__led_rgb = LedRGB()
        self.__buzzer = Buzzer()

    # Méthode pour envoyer un message au client
    def envoyer(self, msg: str) -> None:
        self.__socket_echange.send(msg.encode('utf-8'))

    # Méthode pour recevoir un message du client
    def recevoir(self) -> str:
        tab_octets = self.__socket_echange.recv(1024)
        return tab_octets.decode(encoding='utf-8')

    # Méthode pour gérer les échanges avec le client
    def echange(self) -> None:
        fin: bool = False
        while not fin:
            tab_octets = self.__socket_echange.recv(1024)  # bloquant
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
                time.sleep(0.10)
                self.__robot.arret()
                tab_octets = commande.encode("utf-8")
                self.__socket_echange.send(tab_octets)
                
            elif commande == "stop":
                self.__course_autonome.arret_autonome()
                self.__robot.arret()
                tab_octets = commande.encode("utf-8")
                self.__socket_echange.send(tab_octets)
                
            elif commande == "capteur":
                if self.__course_autonome.get_autonome() == None:
                    tab_octets = self.__capteur.get_all()
                elif self.__course_autonome.get_autonome() != None:
                    tab_octets = self.__course_autonome.get_all_autonome()
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

    # Méthode pour arrêter les échanges
    def arret(self) -> None:
        self.__socket_echange.close()

if __name__ == "__main__":
    # Déclaration des variables
    Robot = deplacement()
    port_ecoute: int = None
    service_ecoute: ServiceEcoute = None
    socket_client: socket = None
    service_echange: ServiceEchange = None
    # Lecture des paramètres (le numéro de port)
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