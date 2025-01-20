# Compte Rendu POO2 BENIS Bastien MURY Gurvan

## Introduction

Ce document présente un compte rendu des fonctionnalités développées pour le robot n°13 dans le cadre de la SAÉ 3.02. Nous avons implémenté une application client-serveur en Python permettant de contrôler le robot à distance et de le faire fonctionner en mode autonome.

Le robot possède:
- 3 capteurs optique
- 2 roues
- 2 moteurs
- 1 carte raspberry pi V0
- 1 buzzer
- 1 led RGB


## Fonctionnalités Implémentées

### Serveur

Le serveur est responsable de la gestion des commandes envoyées par le client et du contrôle des différents composants du robot (moteurs, capteurs, LED RGB, buzzer). Les principales fonctionnalités du serveur incluent :

- **Déplacement du robot** : Le serveur peut recevoir des commandes pour avancer, reculer, tourner à gauche et tourner à droite et s'arrêter.
- **Mode autonome** : Le serveur peut activer un mode autonome où le robot utilise ses capteurs pour naviguer de manière autonome avec un déplacement fluide.
- **Contrôle des capteurs** : Le serveur peut envoyer les valeurs des capteurs au client et s'en servire pour le mode autonome.
- **Contrôle de la batterie** : Le serveur peut envoyer le niveau de la batterie au client.
- **Mode police** : Le serveur peut activer un mode où la LED RGB change de couleur et le buzzer joue une mélodie.

### Client

Le client est une interface graphique développée en Python utilisant Tkinter. Il permet à l'utilisateur de se connecter au serveur et de contrôler le robot. Les principales fonctionnalités du client incluent :

- **Connexion au serveur** : L'utilisateur peut entrer l'adresse IP et le port du serveur pour se connecter.
- **Contrôle manuel** : L'utilisateur peut envoyer des commandes pour avancer, reculer, tourner à gauche et tourner à droite.
- **Mode autonome** : L'utilisateur peut activer ou désactiver le mode autonome.
- **Affichage des capteurs** : L'utilisateur peut demander les valeurs des capteurs et les afficher en continu.
- **Affichage de la batterie** : L'utilisateur peut demander le niveau de la batterie et l'afficher en continu.
- **Mode police** : L'utilisateur peut activer ou désactiver le mode police.
- **Logs** : Les actions et messages sont enregistrés dans un fichier de log au format JSON.

## Conformité avec le Cahier des Charges

### Objectifs Réalisés

- **Mode autonome avec la gestion des angles** : Le mode autonome utilise les capteurs pour détecter les obstacles et ajuster la direction du robot sans tourner brusquement.
- **Application client-serveur** : Nous avons développé une application client-serveur en Python utilisant le protocole TCP.
- **Interface graphique** : Le client dispose d'une interface graphique permettant de configurer les paramètres réseau et de contrôler le robot.
- **Sauvegarde des données** : Les logs des actions et messages sont sauvegardés dans un fichier JSON.

### Objectifs Non Réalisés

- **Base de données** : Nous avons implémenter la sauvegarde de donné grace à un json que nous pouvons récupéré sur demmande avec le boutton Logs

## Diagramme de Gantt

Le diagramme de Gantt ci-dessous montre les différentes étapes du projet en fonction de l'avancement sur le Projet.

| Tâche                          | Début       | Fin         | Durée (jours) |
|--------------------------------|-------------|-------------|---------------|
| Initialisation du projet       | 12/11/2024  | 16/11/2024  | 5             |
| Développement du serveur       | 12/11/2024  | 12/01/2025  | 62            |
| Développement du client        | 12/11/2024  | 12/01/2025  | 62            |
| Intégration des capteurs       | 13/12/2024  | 12/01/2025  | 31            |
| Implémentation du mode autonome| 13/12/2024  | 12/01/2025  | 31            |
| Tests et débogage              | 12/11/2024  | 16/01/2025  | 66            |
| Documentation                  | 16/01/2025  | 16/01/2025  | 1             |


## Diagrame des classes
| Fonctionnalité     | Prévue      | Implémenter |
|--------------------|-------------|-------------|
| Mode autonome | oui | oui |
| Mode police | non | oui |
| Déplacement flèche directionnel | oui | oui |
| log de connection | non | oui |
| optimisation des déplacment en mode automatique | non | oui |
| Mode pour aquisition périodique des capteurs et de la batterie par l'IHM | non | oui |
| connection au robot avec une IHM | oui | oui |


## Fonctionnement des programmes

### Client


### Serveur

classe Deplacement:

-> active les moteurs et les arrêtes.

 Est utiliser dans le mode autonome et quand on recois les indication de mouvement (flèche de direction).

classe Capteur:

-> prend les valeurs des capteurs et renvoie les valeur.
 
 Est utiliser pour la demande de capteur de l'IHM quand on n'est pas en mode autonome.

classe Autonome:

-> permet déplacer le robot sans toucher les obstacles et en perdant le moins de vitesse possible.

Il ce lance quand l'IHM lui envoie l'instruction. Il lance la fonctionnalité autonome avec un thread.


classe LedRGB:

-> permet de l'activation de la ledRGB

Il est lancée en même temps que le Buzzer en thread. Il est lancée avec l'IHM. 

classe Buzzer:

-> permet l'activation du buzzer pour lancer une mélodie. Il est lancée en même temps que la ledRGB en thread. 

Il est lancée avec l'IHM.

classe ServiceEcoute:

-> permet d'initier la communication entre le client et le robot pour ensuite communiquer. 

Il est lancée à l'activation du code python.

classe ServiceEchange:

-> permet d'attendre l'envoie des demandes de l'IHM et de traiter ces demandes pour ensuite faire appelle au bonne fonction.

Il est lancée après avoir fait la connection en TCP entre le robot et le client (IHM).

## Conclusion

Nous avons réussi à implémenter la majorité des fonctionnalités décrites dans le cahier des charges. Le robot peut être contrôlé manuellement ou fonctionner en mode autonome, et les données des capteurs et de la batterie peuvent être affichées en temps réel. Les logs des actions sont sauvegardés dans un fichier JSON, permettant de suivre l'historique des interactions avec le robot.


## Annexe

### Client

```python
from tkinter import *
from tkinter import ttk
from Client_tcp_class import Client_TCP
from socket import *
import json
from datetime import datetime
from time import *


class IHM_client_tcp(Tk):

    POLICE: str = "times"
    TAILLE_POLICE: int = 12

    def __init__(self):
        Tk.__init__(self)
        self.style = ttk.Style(self)
        self.style.theme_use('clam')  # Utiliser un thème moderne
        self.configure(background="light grey")

        # déclaration des références d'objets
        self.__fen_connexion: Frame
        self.__label_ip: Label
        self.__entree_ip_serveur: Label
        self.__label_port: Label
        self.__entree_port_serveur: Label
        self.__btn_connexion: Button
        self.__btn_Configuration: Button
        self.__client_tcp: Client_TCP

        self.__fen_echange: Frame
        self.__btn_envoyer: Button
        self.__btn_quitter: Button

        self.__btn_avancer: Button
        self.__btn_reculer: Button
        self.__btn_LFI: Button
        self.__btn_RN: Button
        self.__btn_stop: Button
        self.__btn_police: Button
        self.__label_mode: Label
        self.__label_status: Label
        self.__label_status_Capteur: Label
        self.__label_status_Baterrie: Label
        self.__btn_auto: Button
        self.__btn_capteur: Button
        self.__btn_bat: Button

        self.mode_auto: bool = False
        self.mode_police: bool = False

        self.__fen_info: Frame

        self.capteur_active = False
        self.batterie_active = False

        self.logs = {"server_ip": "", "server_port": "", "client_ip": "", "client_port": "", "messages": []}

        # instanciation
        self.__fen_connexion = ttk.Frame(self, padding=10)
        self.__label_ip = ttk.Label(self.__fen_connexion, text="IP Serveur", font=(self.POLICE, self.TAILLE_POLICE))
        self.__entree_ip_serveur = ttk.Label(self.__fen_connexion, width=20, text="XXX.XXX.XXX.XXX")
        self.__label_port = ttk.Label(self.__fen_connexion, text="Port Serveur", font=(self.POLICE, self.TAILLE_POLICE))
        self.__entree_port_serveur = ttk.Label(self.__fen_connexion, width=15, text="XXXX")
        self.__btn_connexion = ttk.Button(self.__fen_connexion, text="Connexion", command=self.connexion)
        self.__btn_Configuration = ttk.Button(self.__fen_connexion, text="Configuration", command=lambda: Fen_Config(self))
        self.__btn_view_logs = ttk.Button(self.__fen_connexion, text="Voir Logs", command=self.view_logs)

        self.__fen_echange = ttk.Frame(self, padding=10)
        self.__btn_envoyer = ttk.Button(self.__fen_echange, text="Envoyer", state='disabled', command=self.envoyer)
        self.__btn_quitter = ttk.Button(self.__fen_connexion, text="Quitter", state='active', command=self.quitter)

        self.__btn_avancer = ttk.Button(self.__fen_echange, text="Avancer", state='disabled', command=lambda: self.envoyer_commande("avancer"))
        self.__btn_reculer = ttk.Button(self.__fen_echange, text="Reculer", state='disabled', command=lambda: self.envoyer_commande("reculer"))
        self.__btn_LFI = ttk.Button(self.__fen_echange, text="Gauche", state='disabled', command=lambda: self.envoyer_commande("gauche"))
        self.__btn_RN = ttk.Button(self.__fen_echange, text="Droite", state='disabled', command=lambda: self.envoyer_commande("droite"))
        self.__btn_auto = ttk.Button(self.__fen_echange, state='disabled', text="Mode Auto", command=self.auto_mode)
        self.__btn_stop = ttk.Button(self.__fen_echange, text="Arret", state='disabled', command=lambda: self.envoyer_commande("stop"))
        self.__btn_police = ttk.Button(self.__fen_echange, text="Mode police", state='disabled', command= self.police)
        self.__btn_capteur = ttk.Button(self.__fen_echange, text="Demander Capteurs", state='disabled', command=self.demander_capteurs)
        self.__btn_bat = ttk.Button(self.__fen_echange, text="Demander baterrie", state='disabled', command=self.demander_Baterrie)

        self.__fen_info = ttk.Frame(self, padding=10)
        self.__label_status = ttk.Label(self.__fen_info, text="", font=(self.POLICE, self.TAILLE_POLICE))
        self.__label_mode = ttk.Label(self.__fen_info, text="Mode : Manuel", font=(self.POLICE, self.TAILLE_POLICE))
        self.__label_status_Capteur = ttk.Label(self.__fen_info, text="", font=(self.POLICE, self.TAILLE_POLICE))
        self.__label_status_Baterrie = ttk.Label(self.__fen_info, text="", font=(self.POLICE, self.TAILLE_POLICE))

        # ajout des widgets
        self.title("Échange avec le robot 13")
        self.__fen_connexion.pack(pady=10)
        self.__label_ip.grid(row=0, column=0, padx=5, pady=5)
        self.__entree_ip_serveur.grid(row=0, column=1, padx=5, pady=5)
        self.__label_port.grid(row=1, column=0, padx=5, pady=5)
        self.__entree_port_serveur.grid(row=1, column=1, padx=5, pady=5)
        self.__btn_connexion.grid(row=0, column=2, padx=5, pady=5)
        self.__btn_Configuration.grid(row=1, column=2, padx=5, pady=5)
        self.__btn_quitter.grid(row=1, column=3, padx=5, pady=5)
        self.__btn_view_logs.grid(row=1, column=4, padx=5, pady=5)

        self.__fen_echange.pack(pady=10)
        self.__btn_envoyer.grid(row=0, column=1, padx=5, pady=5)
        self.__btn_police.grid(row=0, column=0, padx=5, pady=5)
        self.__btn_avancer.grid(row=2, column=1, padx=5, pady=5)
        self.__btn_LFI.grid(row=3, column=0, padx=5, pady=5)
        self.__btn_RN.grid(row=3, column=2, padx=5, pady=5)
        self.__btn_reculer.grid(row=4, column=1, padx=5, pady=5)
        self.__btn_stop.grid(row=3, column=1, padx=5, pady=5)
        self.__btn_auto.grid(row=5, column=2, padx=5, pady=5)
        self.__btn_capteur.grid(row=5, column=1, padx=5, pady=5)
        self.__btn_bat.grid(row=5, column=0, padx=5, pady=5)

        self.__fen_info.pack(pady=10)
        self.__label_status.grid(row=6, column=0, columnspan=3, padx=5, pady=5)
        self.__label_mode.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.__label_status_Capteur.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        self.__label_status_Baterrie.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        self.mainloop()

        self.protocol("WM_DELETE_WINDOW", self.quitter)

    def action_evt(self, evt: Event) -> None:
        """
        Gérer les événements.

        Paramètres:
        evt (Event): L'événement à gérer.

        Retourne:
        None
        """
        print(evt)

    # modificateur
    def set_addr(self, addr: str) -> None:
        """
        Définir l'adresse IP du serveur.

        Paramètres:
        addr (str): L'adresse IP à définir.

        Retourne:
        None
        """
        self.__entree_ip_serveur.config(text=addr)

    def set_port(self, port: int) -> None:
        """
        Définir le port du serveur.

        Paramètres:
        port (int): Le numéro de port à définir.

        Retourne:
        None
        """
        self.__entree_port_serveur.config(text=str(port))

    def set_mode(self, mode: str) -> None:
        """
        Définir le mode (Manuel ou Automatique).

        Paramètres:
        mode (str): Le mode à définir ("Manuel" ou "Automatique").

        Retourne:
        None
        """
        self.__label_mode.config(text=f"Mode: {mode}")

    def connexion(self) -> None:
        """
        Se connecter au serveur du robot.

        Retourne:
        None
        """
        try:
            print("Connexion au Robot 13 en cours ...")
            ip_serveur: str = self.__entree_ip_serveur.cget("text")
            port_serveur: int = int(self.__entree_port_serveur.cget("text"))
            # instanciation du client TCP
            self.__client_tcp = Client_TCP(ip_serveur, port_serveur)

            # connexion au serveur
            self.__client_tcp.connexion()

            self.logs["server_ip"] = ip_serveur
            self.logs["server_port"] = port_serveur
            self.logs["client_ip"] = self.__client_tcp.get_ip()[0]
            self.logs["client_port"] = self.__client_tcp.get_ip()[1]
            self.save_log(f"Connexion au robot 13 : ok")

            print("Connexion au robot 13 : ok")
        except Exception as ex:
            error_message = f"Erreur de connexion au robot 13 : {ex}"
            print(error_message)
            self.save_log(error_message)
        else:
            # désactiver le bouton de connexion
            self.__btn_connexion.configure(state='disabled')
            self.__btn_Configuration.configure(state='disabled')

            # activer les boutons pour envoyer un message et pour quitter
            self.__btn_envoyer.configure(state='active')
            self.__btn_avancer.configure(state='active')
            self.__btn_reculer.configure(state='active')
            self.__btn_LFI.configure(state='active')
            self.__btn_RN.configure(state='active')
            self.__btn_stop.configure(state='active')
            self.__btn_capteur.configure(state='active')
            self.__btn_bat.configure(state='active')
            self.__btn_auto.configure(state='active')
            self.__btn_police.configure(state='active')

    def envoyer(self) -> None:
        """
        Envoyer un message au serveur.

        Retourne:
        None
        """
        msg = self.__entree_msg_client.get()
        if msg != "":
            self.__entree_msg_client.delete(0, END)
            self.__client_tcp.envoyer(msg=msg)
            chaine = self.__client_tcp.recevoir()
            self.__text_msg_serveur.insert(INSERT, chaine + "\n")

    def envoyer_commande(self, commande: str) -> None:
        """
        Envoyer une commande au robot.

        Paramètres:
        commande (str): La commande à envoyer ("avancer", "reculer", "gauche", "droite", "stop").

        Retourne:
        None
        """
        self.__client_tcp.envoyer(msg=commande)
        chaine = self.__client_tcp.recevoir()
        if commande == "avancer":
            self.__label_status.config(text="Le robot avance")
            self.save_log("Le robot avance")
        elif commande == "reculer":
            self.__label_status.config(text="Le robot recule")
            self.save_log("Le robot recule")
        elif commande == "gauche":
            self.__label_status.config(text="Le robot tourne à gauche")
            self.save_log("Le robot tourne à gauche")
        elif commande == "droite":
            self.__label_status.config(text="Le robot tourne à droite")
            self.save_log("Le robot tourne à droite")
        elif commande == "stop":
            self.__label_status.config(text="Le robot s'arrête")
            self.save_log("Le robot s'arrête")
        self.__text_msg_serveur.insert(INSERT, chaine + "\n")
        self.save_log(chaine)

    def demander_capteurs(self) -> None:
        """
        Basculer les demandes continues de données des capteurs.

        Retourne:
        None
        """
        if not self.capteur_active:
            self.capteur_active = True
            self.__btn_capteur.config(text="Arrêter Capteurs")
            self.update_capteurs()
        else:
            self.capteur_active = False
            self.__btn_capteur.config(text="Demander Capteurs")

    def update_capteurs(self) -> None:
        """
        Demander des données de capteurs au serveur toutes les secondes.

        Retourne:
        None
        """
        if self.capteur_active:
            self.__client_tcp.envoyer("capteur")
            cap = self.__client_tcp.recevoir()
            self.__label_status_Capteur.config(text=f"valeur capteur : {cap}")
            self.save_log(f"Capteur: {cap}")
            self.after(1000, self.update_capteurs)

    def demander_Baterrie(self) -> None:
        """
        Basculer les demandes continues de données de la batterie.

        Retourne:
        None
        """
        if not self.batterie_active:
            self.batterie_active = True
            self.__btn_bat.config(text="Arrêter Batterie")
            self.update_batterie()
        else:
            self.batterie_active = False
            self.__btn_bat.config(text="Demander Batterie")

    def update_batterie(self) -> None:
        """
        Demander des données de la batterie au serveur toutes les secondes.

        Retourne:
        None
        """
        if self.batterie_active:
            self.__client_tcp.envoyer("bat")
            bat = self.__client_tcp.recevoir()
            self.__label_status_Baterrie.config(text=f"valeur baterrie : {bat}")
            self.save_log(f"Batterie: {bat}")
            self.after(1000, self.update_batterie)

    def quitter(self) -> None:
        """
        Se déconnecter du serveur et fermer l'application.

        Retourne:
        None
        """
        try:
            # envoyer le mot cle "fin" au serveur
            self.__client_tcp.envoyer("fin")

            # attendre la reponse du serveur
            reponse = self.__client_tcp.recevoir()
            print("Réponse du serveur :", reponse)

            # appeler la méthode arret() du client TCP
            self.__client_tcp.arret()
        except Exception as ex:
            print("Erreur lors de la déconnexion:", ex)
        finally:
            # fermer l’application
            self.destroy()
            self.__client_tcp.arret()

    def auto_mode(self) -> None:
        """
        Basculer entre le mode manuel et automatique.
        avec activation ou désactivation des boutton qui ne son pas utile en mode automatique 

        Retourne:
        None
        """
        if self.mode_auto:
            self.set_mode("Manuel")
            self.__client_tcp.envoyer("mode manuel")
            self.__btn_auto.config(text="Mode Auto")
            self.__btn_envoyer.configure(state='active')
            self.__btn_avancer.configure(state='active')
            self.__btn_reculer.configure(state='active')
            self.__btn_LFI.configure(state='active')
            self.__btn_RN.configure(state='active')
            self.__btn_police.configure(state='active')
            
        else:
            self.set_mode("Automatique")
            self.__client_tcp.envoyer("mode automatique")
            self.__btn_auto.config(text="Mode Manuel")
            self.__btn_envoyer.configure(state='disabled')
            self.__btn_avancer.configure(state='disabled')
            self.__btn_reculer.configure(state='disabled')
            self.__btn_LFI.configure(state='disabled')
            self.__btn_RN.configure(state='disabled')
            self.__btn_police.configure(state='active')
        self.mode_auto = not self.mode_auto
        
    def police(self) -> None:
        """
        Basculer entre le mode police et normal.

        Retourne:
        None
        """
        if self.mode_police:
            self.__client_tcp.envoyer("police_off")
            self.__btn_police.config(text="Mode Police")
            self.save_log(f"Mode police desactiver")
        else:
            self.__client_tcp.envoyer("police_on")
            self.__btn_police.config(text="Mode Normal")
            self.save_log(f"Mode police activer")
        self.mode_police = not self.mode_police
        

    def save_log(self, message: str) -> None:
        """
        Sauvegarder un message dans le fichier de log au format JSON avec un timestamp.

        Paramètres:
        message (str): Le message à sauvegarder.

        Retourne:
        None
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {message}"
        self.logs["messages"].append(log_entry)
        with open("logs.json", "w") as log_file:
            json.dump(self.logs, log_file, indent=4)

    def view_logs(self) -> None:
        """
        Ouvrir une nouvelle fenêtre pour voir les logs.

        Retourne:
        None
        """
        Fen_Logs(self)


class Fen_Logs(Toplevel):
    """
    Fenêtre pour voir les logs.
    """
    def __init__(self, fenP: IHM_client_tcp) -> None:
        """
        Initialiser la fenêtre de visualisation des logs.
        """
        Toplevel.__init__(self)
        self.__fenP = fenP
        self.title("Logs")
        self.__text_logs = Text(self, wrap=WORD)
        self.__text_logs.pack(expand=True, fill=BOTH)
        self.load_logs()

    def load_logs(self) -> None:
        """
        Charger les logs depuis le fichier JSON et les afficher.

        Retourne:
        None
        """
        try:
            with open("logs.json", "r") as log_file:
                logs = json.load(log_file)
                self.__text_logs.insert(END, f"Server IP: {logs['server_ip']}\n")
                self.__text_logs.insert(END, f"Server Port: {logs['server_port']}\n")
                self.__text_logs.insert(END, f"Client IP: {logs['client_ip']}\n")
                self.__text_logs.insert(END, f"Client Port: {logs['client_port']}\n")
                for message in logs["messages"]:
                    self.__text_logs.insert(END, f"{message}\n")
        except FileNotFoundError:
            self.__text_logs.insert(END, "Aucun log trouvé.")


class Fen_Config(Toplevel):
    """
    Fenêtre de configuration pour définir l'adresse IP et le port du robot.
    """
    def __init__(self, fenP: IHM_client_tcp) -> None:
        """
        Initialiser la fenêtre de configuration.
        """
        Toplevel.__init__(self)
        self.__fenP = fenP  # mémorisation de la fenêtre principale, accès aux méthodes
        # déclaration
        self.__lbl_adr: Label
        self.__entree_adr: Entry
        self.__lbl_port: Label
        self.__entree_port: Entry
        self.__btn_retour: Button

        # instantiation / initialisation
        self.__fenP.withdraw()  # effacer fenêtre principale
        self.title("Configuration du client")
        self.__lbl_adr = ttk.Label(self, text="Adresse du Robot :")
        self.__entree_adr = ttk.Entry(self, width=15)
        self.__entree_adr.insert(0, "10.15.141.1")
        self.__lbl_port = ttk.Label(self, text="Port du Robot : ")
        self.__entree_port = ttk.Entry(self, width=5)
        self.__entree_port.insert(0, "5000")
        self.__btn_retour = ttk.Button(self, text="Retour", command=self.configuration)
        # ajout des widgets
        self.__lbl_adr.grid(row=0, column=0, padx=5, pady=5)
        self.__entree_adr.grid(row=0, column=1, padx=5, pady=5)
        self.__lbl_port.grid(row=1, column=0, padx=5, pady=5)
        self.__entree_port.grid(row=1, column=1, padx=5, pady=5)
        self.__btn_retour.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        # événements
        self.protocol("WM_DELETE_WINDOW", self.configuration)

    def configuration(self) -> None:
        """
        Appliquer la configuration et revenir à la fenêtre principale.

        Retourne:
        None
        """
        self.__fenP.set_addr(self.__entree_adr.get())
        self.__fenP.set_port(int(self.__entree_port.get()))

        self.__fenP.deiconify()  # afficher la fenêtre principale
        self.destroy()  # detruire la fenetre courante


if __name__ == "__main__":
    ihm: IHM_client_tcp = IHM_client_tcp()
```

### Serveur

```python
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
```