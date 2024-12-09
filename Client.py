from tkinter import *
from Client_tcp_class import Client_TCP

class Fen_Principale(Tk):
    
    def __init__(self)-> None:
        Tk.__init__(self)
        # déclaration
        self.__addr:str
        self.__port:int
        self.__lbl_adr_port:Label
        self.__fen:Frame
        self.__btn_config:Button
        self.__btn_connexion:Button
        self.__btn_init:Button
        self.__btn_quitter:Button
        
        # instanciation / initialisation
        self.title("fenetre principale") # titre de la fenetre
        self.__fen = Frame(self, relief="groove") # cadre de la fenetre
        self.__lbl_adr_port = Label(self.__fen) # label pour l'adresse et le port du serveur
        self.__btn_config = Button(self.__fen, text="Configuration", command= lambda : Fen_Config(self)) # bouton de pour lancer la fen de configuration
        self.__btn_connexion = Button(self.__fen, text="Connexion", command= lambda : Fen_echange(self)) # bouton pour lancer la fen d'échange               
        self.__btn_init = Button(self.__fen,text="Réinitialisation",command=self.init) # bouton de réinitialisation
        self.__btn_quitter = Button(self.__fen,text="Quitter",bg="red",command=self.destroy ) # bouton pour tout quitter
        self.init() # premier appel pour intialisation de l'adresse

        # ajout des widgets
        self.__fen.pack() # affichage du cadre
        self.__lbl_adr_port.grid(row=0,column=0) # affichage de l'adresse et du port du serveur
        self.__btn_config.grid(row=1,column=0) # affichage du bouton de configuration
        self.__btn_connexion.grid(row=1,column=2) # affichage du bouton de connexion
        self.__btn_init.grid(row=2,column=0) # affichage du bouton d'initialisation
        self.__btn_quitter.grid(row=2,column=2) # affichage du bouton de quitter

    #modificateur
    def set_addr(self,addr:str)->None:
        self.__addr = addr
    def set_port(self,port:int)->None:
        self.__port = port
    def set_lbl_adr_port(self)->None:
        self.__lbl_adr_port["text"]=f"serveur {self.__addr}:{str(self.__port)}"
    def init(self)->None:
        self.__lbl_adr_port["text"]="serveur xxx.xxx.xxx.xxx : XXXX"

class Fen_Config(Toplevel):
    def __init__(self, fenP:Fen_Principale)-> None:
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
        self.__lbl_adr = Label(self, text="addresse du serveur")
        self.__entree_adr = Entry(self,width=15)
        self.__entree_adr.insert(0,"127.0.0.1")
        self.__lbl_port = Label(self,text="port du serveur")
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
        self.__fenP.set_lbl_adr_port()
        
        self.__fenP.deiconify() # afficher la fenetre principale
        self.destroy() # detruire la fenetre courante
        
class Fen_echange(Toplevel):
    
    
    def __init__(self, fenP:Fen_Principale)-> None:
        Toplevel.__init__(self)
        self.__fenP = fenP
        # déclaration des variables 
        self.__POLICE: str = "times"
        self.__TAILLE_POLICE: int = 12
        # déclaration des références d'objets
        self.__client_tcp:Client_TCP

        self.__fen_echange: Frame
        self.__entree_msg_client: Entry
        self.__btn_envoyer: Button
        self.__text_msg_serveur: Text
        self.__btn_quitter: Button

        #instanciation
        self.title("fenetre echange")
        

        self.__fen_echange = Frame(self, relief="groove")
        self.__entree_msg_client = Entry(self.__fen_echange, width=15) 
        self.__btn_envoyer = Button(self.__fen_echange, text = "envoyer",state='normal', font= (self.__POLICE,self.__TAILLE_POLICE),bg='blue', command= self.envoyer)
        self.__text_msg_serveur = Entry(self.__fen_echange, width=15 )
        self.__btn_quitter = Button(self.__fen_echange, text = "quitter",state='normal', font= (self.__POLICE,self.__TAILLE_POLICE), bg="red", command= self.quitter)

        #ajout des widget
        

        self.__fen_echange.pack()
        self.__entree_msg_client.grid(row=0, column=0)
        self.__btn_envoyer.grid(row=0, column=1)
        self.__text_msg_serveur.grid(row=1, column=0)
        self.__btn_quitter.grid(row=1, column=1)

        self.mainloop()
        
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
            


if __name__ == "__main__":
    fen_principale:Fen_Principale = Fen_Principale()
    fen_principale.mainloop()
