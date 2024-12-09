
from tkinter import *

class Fen_Principale(Tk):
    def __init__(self)-> None:
        Tk.__init__(self)
        # déclaration
        self.__addr:str
        self.__port:int
        self.__lbl_adr_port:Label
        self.__btn_config:Button
        self.__btn_init:Button
        self.__btn_quitter:Button
        # instanciation / initialisation
        self.title("fenetre principale")
        self.__lbl_adr_port = Label(self)
        self.__btn_config = Button(self, text="configuration", command= lambda : Fen_Config(self))               
        self.__btn_init = Button(self,text="initialisation",command=self.init)
        self.__btn_quitter = Button(self,text="Quitter",bg="red",command=self.destroy )
        self.init() # premier appel pour intialisation de l'adresse

        # ajout des widgets
        self.__lbl_adr_port.pack()
        self.__btn_config.pack()
        self.__btn_init.pack()
        self.__btn_quitter.pack()

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
        self.__fenP.set_lbl_adr_port()


        self.__fenP.deiconify() # afficher la fenetre principale
        self.destroy() # detruire la fenetre courante


if __name__ == "__main__":
    fen_principale:Fen_Principale = Fen_Principale()
    fen_principale.mainloop()
