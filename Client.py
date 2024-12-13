from tkinter import *
from Client_tcp_class import Client_TCP
from socket import *


class IHM_client_tcp(Tk):

    POLICE: str = "times"
    TAILLE_POLICE: int = 12

    def __init__(self):
        Tk.__init__(self)
        # déclaration des références d'objets

        self.__fen_connexion: Frame
        self.__label_ip: Label
        self.__entree_ip_serveur: Entry
        self.__label_port: Label
        self.__entree_port_serveur: Entry
        self.__btn_connexion: Button
        self.__btn_Configuration: Button
        self.__client_tcp:Client_TCP

        self.__fen_echange: Frame
        self.__entree_msg_client: Entry
        self.__btn_envoyer: Button
        self.__text_msg_serveur: Text
        self.__btn_quitter: Button
        
        
        self.__btn_avancer: Button
        self.__btn_reculer: Button
        self.__btn_LFI: Button
        self.__btn_RN: Button

        #instanciation
        
        self.__fen_connexion = Frame(self, borderwidth=10, relief="groove")
        self.__label_ip = Label(self.__fen_connexion, text = "ip serveur", font=(self.POLICE,self.TAILLE_POLICE))
        self.__entree_ip_serveur = Entry(self.__fen_connexion, width=15)
        self.__label_port = Label(self.__fen_connexion, text="port serveur")
        self.__entree_port_serveur = Entry(self.__fen_connexion, width=15)
        self.__btn_connexion = Button(self.__fen_connexion, text = "connexion", font= (self.POLICE,self.TAILLE_POLICE), command=  self.connexion)
        self.__btn_Configuration = Button(self.__fen_connexion, text = "Configuration", font= (self.POLICE,self.TAILLE_POLICE), command= lambda : Fen_Config(self))

        self.__fen_echange = Frame(self, relief="groove")
        self.__entree_msg_client = Entry(self.__fen_echange, width=15) 
        self.__btn_envoyer = Button(self.__fen_echange, text = "envoyer",state='disabled', font= (self.POLICE,self.TAILLE_POLICE),bg='blue', command= self.envoyer)
        self.__text_msg_serveur = Entry(self.__fen_echange, width=15 )
        self.__btn_quitter = Button(self.__fen_echange, text = "quitter",state='disabled', font= (self.POLICE,self.TAILLE_POLICE), bg="red", command= self.quitter)

        self.__btn_avancer = Button(self.__fen_echange, text = "avancer",state='disabled', font= (self.POLICE,self.TAILLE_POLICE), bg="yellow" )
        self.__btn_reculer = Button(self.__fen_echange, text = "reculer",state='disabled', font= (self.POLICE,self.TAILLE_POLICE), bg="yellow" )
        self.__btn_LFI = Button(self.__fen_echange, text = "gauche",state='disabled', font= (self.POLICE,self.TAILLE_POLICE), bg="yellow" )
        self.__btn_RN = Button(self.__fen_echange, text = "droite",state='disabled', font= (self.POLICE,self.TAILLE_POLICE), bg="yellow" )
        
        #ajout des widget
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
        
    #modificateur
    def set_addr(self, addr: str) -> None:
        self.__entree_ip_serveur.delete(0, END)
        self.__entree_ip_serveur.insert(0, addr)

    def set_port(self, port: int) -> None:
        self.__entree_port_serveur.delete(0, END)
        self.__entree_port_serveur.insert(0, port)
        
    def connexion(self)-> None:
        try:
            print("connexion en cours")
            ip_serveur:str= self.__entree_ip_serveur.get()
            port_serveur:int= int(self.__entree_port_serveur.get())
            # instanciation du client TCP
            self.__client_tcp= Client_TCP(ip_serveur, port_serveur)
            
            # connexion au serveur
            self.__client_tcp.connexion()
            
            print("connexion ok")
        except Exception as ex:
            print("erreur de connexion : ", ex)
        else:
            # désactiver le bouton de connexion
            self.__btn_connexion.configure(state='disabled')
            
            # activer les boutons pour envoyer un message et pour quitter
            self.__btn_envoyer.configure(state='active')
            self.__btn_quitter.configure(state='active')
            self.__btn_avancer.configure(state='active')
            self.__btn_reculer.configure(state='active')
            self.__btn_LFI.configure(state='active')
            self.__btn_RN.configure(state='active')
        
    def envoyer(self)-> None:
        msg = self.__entree_msg_client.get()
        if msg != "":
            self.__entree_msg_client.delete(0, END)
            self.__client_tcp.envoyer(msg= msg)
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
    def __init__(self, fenP:IHM_client_tcp)-> None:
        Toplevel.__init__(self)
        self.__fenP = fenP# memorisation de la fenètre principale, accès aux méthodes
        # declaration
        self.__lbl_adr:Label
        self.__entree_adr:Entry
        self.__lbl_port:Label
        self.__entree_port:Entry
        self.__btn_retour:Button

        # instantiation / initialisation
        self.__fenP.withdraw() # effacer fenetre principale
        self.title("config")
        self.__lbl_adr = Label(self, text="adr serveur")
        self.__entree_adr = Entry(self,width=15)
        self.__entree_adr.insert(0,"127.0.0.1")
        self.__lbl_port = Label(self,text="port serveur")
        self.__entree_port = Entry(self,width= 5)
        self.__entree_port.insert(0,"5000")
        self.__btn_retour = Button(self,text="Retour", command= self.configuration)
        # ajout des widgets
        self.__lbl_adr.grid(row= 0,column= 0)
        self.__entree_adr.grid(row=0,column= 1)
        self.__lbl_port.grid(row=1,column= 0)
        self.__entree_port.grid(row=1,column= 1)
        self.__btn_retour.grid(row=2,column=0)
        # evenements
        self.protocol("WM_DELETE_WINDOW", self.configuration)

    def configuration(self)-> None:
        self.__fenP.set_addr(self.__entree_adr.get())
        self.__fenP.set_port(int(self.__entree_port.get()))
        

        self.__fenP.deiconify() # afficher la fenetre principale
        self.destroy() # detruire la fenetre courante

if __name__ == "__main__":
    ihm: IHM_client_tcp = IHM_client_tcp()