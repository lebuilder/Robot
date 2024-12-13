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
        self.__entree_msg_client: Entry
        self.__btn_envoyer: Button
        self.__text_msg_serveur: Text
        self.__btn_quitter: Button

        self.__btn_avancer: Button
        self.__btn_reculer: Button
        self.__btn_LFI: Button
        self.__btn_RN: Button

        # instanciation
        self.__fen_connexion = ttk.Frame(self, padding=10)
        self.__label_ip = ttk.Label(self.__fen_connexion, text="IP Serveur", font=(self.POLICE, self.TAILLE_POLICE))
        self.__entree_ip_serveur = ttk.Label(self.__fen_connexion, width=15, text="XXX.XXX.XXX.XXX")
        self.__label_port = ttk.Label(self.__fen_connexion, text="Port Serveur")
        self.__entree_port_serveur = ttk.Label(self.__fen_connexion, width=15, text="XXXX")
        self.__btn_connexion = ttk.Button(self.__fen_connexion, text="Connexion", command=self.connexion)
        self.__btn_Configuration = ttk.Button(self.__fen_connexion, text="Configuration", command=lambda: Fen_Config(self))

        self.__fen_echange = ttk.Frame(self, padding=10)
        self.__entree_msg_client = ttk.Entry(self.__fen_echange, width=15)
        self.__btn_envoyer = ttk.Button(self.__fen_echange, text="Envoyer", state='disabled', command=self.envoyer)
        self.__text_msg_serveur = ttk.Entry(self.__fen_echange, width=15)
        self.__btn_quitter = ttk.Button(self.__fen_echange, text="Quitter", state='disabled', command=self.quitter)

        self.__btn_avancer = ttk.Button(self.__fen_echange, text="Avancer", state='disabled', command=lambda: self.envoyer_commande("avancer"))
        self.__btn_reculer = ttk.Button(self.__fen_echange, text="Reculer", state='disabled', command=lambda: self.envoyer_commande("reculer"))
        self.__btn_LFI = ttk.Button(self.__fen_echange, text="Gauche", state='disabled', command=lambda: self.envoyer_commande("gauche"))
        self.__btn_RN = ttk.Button(self.__fen_echange, text="Droite", state='disabled', command=lambda: self.envoyer_commande("droite"))

        # ajout des widgets
        self.title("Échange avec le robot 13")
        self.__fen_connexion.pack()
        self.__label_ip.grid(row=0, column=0)
        self.__entree_ip_serveur.grid(row=0, column=1)
        self.__label_port.grid(row=1, column=0)
        self.__entree_port_serveur.grid(row=1, column=1)
        self.__btn_connexion.grid(row=0, column=2)
        self.__btn_Configuration.grid(row=1, column=2)

        self.__fen_echange.pack()
        self.__entree_msg_client.grid(row=0, column=0)
        self.__btn_envoyer.grid(row=0, column=1)
        self.__text_msg_serveur.grid(row=1, column=0)
        self.__btn_quitter.grid(row=1, column=1)
        self.__btn_avancer.grid(row=2, column=1)
        self.__btn_LFI.grid(row=3, column=0)
        self.__btn_RN.grid(row=3, column=2)
        self.__btn_reculer.grid(row=4, column=1)
        self.mainloop()

        self.protocol("WM_DELETE_WINDOW", self.quitter)

    # modificateur
    def set_addr(self, addr: str) -> None:
        self.__entree_ip_serveur.config(text=addr)

    def set_port(self, port: int) -> None:
        self.__entree_port_serveur.config(text=str(port))

    def connexion(self) -> None:
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
            self.__btn_quitter.configure(state='active')
            self.__btn_avancer.configure(state='active')
            self.__btn_reculer.configure(state='active')
            self.__btn_LFI.configure(state='active')
            self.__btn_RN.configure(state='active')

    def envoyer(self) -> None:
        msg = self.__entree_msg_client.get()
        if msg != "":
            self.__entree_msg_client.delete(0, END)
            self.__client_tcp.envoyer(msg=msg)
            chaine = self.__client_tcp.recevoir()
            self.__text_msg_serveur.insert(INSERT, chaine + "\n")

    def envoyer_commande(self, commande: str) -> None:
        self.__client_tcp.envoyer(msg=commande)
        chaine = self.__client_tcp.recevoir()
        self.__text_msg_serveur.insert(INSERT, chaine + "\n")

    def quitter(self) -> None:
        try:
            # envoyer le mot cle "fin" au serveur
            self.__client_tcp.envoyer("fin")

            # attendre la reponse du serveur
            reponse = self.__client_tcp.recevoir()
            print("Réponse du serveur:", reponse)

            # appeler la méthode arret() du client TCP
            self.__client_tcp.arret()
        except Exception as ex:
            print("Erreur lors de la déconnexion:", ex)
        finally:
            # fermer l’application
            self.destroy()
            self.__client_tcp.arret()


class Fen_Config(Toplevel):
    def __init__(self, fenP: IHM_client_tcp) -> None:
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
        self.__lbl_adr.grid(row=0, column=0)
        self.__entree_adr.grid(row=0, column=1)
        self.__lbl_port.grid(row=1, column=0)
        self.__entree_port.grid(row=1, column=1)
        self.__btn_retour.grid(row=2, column=0)
        # evenements
        self.protocol("WM_DELETE_WINDOW", self.configuration)

    def configuration(self) -> None:
        self.__fenP.set_addr(self.__entree_adr.get())
        self.__fenP.set_port(int(self.__entree_port.get()))

        self.__fenP.deiconify()  # afficher la fenetre principale
        self.destroy()  # detruire la fenetre courante

if __name__ == "__main__":
    ihm: IHM_client_tcp = IHM_client_tcp()