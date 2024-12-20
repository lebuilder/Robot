from tkinter import *
from tkinter import ttk
from Client_tcp_class import Client_TCP
from socket import *


class IHM_client_tcp(Tk):
    

    POLICE: str = "times"
    TAILLE_POLICE: int = 12

    def __init__(self):
        
        Tk.__init__(self)
        self.style = ttk.Style(self)
        self.style.theme_use('clam')  # Use a modern theme
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
        self.__label_mode: Label
        self.__label_status: Label
        self.__label_status_Capteur: Label
        self.__label_status_Baterrie: Label
        self.__btn_auto: Button
        self.__btn_capteur: Button
        self.__btn_bat: Button

        self.mode_auto: bool = False
        
        self.__fen_info: Frame

        self.capteur_active = False
        self.batterie_active = False

        # instanciation
        self.__fen_connexion = ttk.Frame(self, padding=10)
        self.__label_ip = ttk.Label(self.__fen_connexion, text="IP Serveur", font=(self.POLICE, self.TAILLE_POLICE))
        self.__entree_ip_serveur = ttk.Label(self.__fen_connexion, width=20, text="XXX.XXX.XXX.XXX")
        self.__label_port = ttk.Label(self.__fen_connexion, text="Port Serveur", font=(self.POLICE, self.TAILLE_POLICE))
        self.__entree_port_serveur = ttk.Label(self.__fen_connexion, width=15, text="XXXX")
        self.__btn_connexion = ttk.Button(self.__fen_connexion, text="Connexion", command=self.connexion)
        self.__btn_Configuration = ttk.Button(self.__fen_connexion, text="Configuration", command=lambda: Fen_Config(self))

        self.__fen_echange = ttk.Frame(self, padding=10)
        self.__btn_envoyer = ttk.Button(self.__fen_echange, text="Envoyer", state='disabled', command=self.envoyer)
        self.__btn_quitter = ttk.Button(self.__fen_connexion, text="Quitter", state='active', command=self.quitter)

        self.__btn_avancer = ttk.Button(self.__fen_echange, text="Avancer", state='disabled', command=lambda: self.envoyer_commande("avancer"))
        self.__btn_reculer = ttk.Button(self.__fen_echange, text="Reculer", state='disabled', command=lambda: self.envoyer_commande("reculer"))
        self.__btn_LFI = ttk.Button(self.__fen_echange, text="Gauche", state='disabled', command=lambda: self.envoyer_commande("gauche"))
        self.__btn_RN = ttk.Button(self.__fen_echange, text="Droite", state='disabled', command=lambda: self.envoyer_commande("droite"))
        self.__btn_auto = ttk.Button(self.__fen_echange, state='disabled',text="Mode Auto", command=self.auto_mode)
        self.__btn_stop = ttk.Button(self.__fen_echange, text="Arret", state='disabled', command=lambda: self.envoyer_commande("stop"))
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
        
        self.__fen_echange.pack(pady=10)
        self.__btn_envoyer.grid(row=0, column=1, padx=5, pady=5)
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
        self.__label_status_Baterrie.grid(row=2,column=0, columnspan=3, padx=5, pady=5)
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

            print("Connexion au robot 13 : ok")
        except Exception as ex:
            print("Erreur de connexion au robot 13  : ", ex)
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
        elif commande == "reculer":
            self.__label_status.config(text="Le robot recule")
        elif commande == "gauche":
            self.__label_status.config(text="Le robot tourne à gauche")
        elif commande == "droite":
            self.__label_status.config(text="Le robot tourne à droite")
        self.__text_msg_serveur.insert(INSERT, chaine + "\n")

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
        
        Retourne:
        None
        """
        if self.mode_auto:
            self.set_mode("Manuel")
            self.__client_tcp.envoyer("mode manuel")
            self.__btn_auto.config(text="Mode Auto")
        else:
            self.set_mode("Automatique")
            self.__client_tcp.envoyer("mode automatique")
            self.__btn_auto.config(text="Mode Manuel")
        self.mode_auto = not self.mode_auto

class Fen_Config(Toplevel):
    """
    Configuration window for setting the robot's IP address and port.
    """
    def __init__(self, fenP: IHM_client_tcp) -> None:
        """
        Initialize the configuration window.
        """
        Toplevel.__init__(self)
        self.__fenP = fenP  # memorisation de la fenètre principale, accès aux méthodes
        # declaration
        self.__lbl_adr: Label
        self.__entree_adr: Entry
        self.__lbl_port: Label
        self.__entree_port: Entry
        self.__btn_retour: Button

        # instantiation / initialisation
        self.__fenP.withdraw()  # effacer fenetre principale
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
        # evenements
        self.protocol("WM_DELETE_WINDOW", self.configuration)

    def configuration(self) -> None:
        """
        Appliquer la configuration et revenir à la fenêtre principale.
        
        Retourne:
        None
        """
        self.__fenP.set_addr(self.__entree_adr.get())
        self.__fenP.set_port(int(self.__entree_port.get()))

        self.__fenP.deiconify()  # afficher la fenetre principale
        self.destroy()  # detruire la fenetre courante


if __name__ == "__main__":
    ihm: IHM_client_tcp = IHM_client_tcp()
