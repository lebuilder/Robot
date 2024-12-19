from socket import *
import sys

class ServiceEcoute :
    def __init__(self, port_serveur: int) -> None:
        self.__socket_ecoute:socket = socket(AF_INET, SOCK_STREAM)
        self.__socket_ecoute.bind(('', port_serveur))
        self.__socket_ecoute.listen(1)
        print(f"écoute sur le port :  {port_serveur}")
        
    def attente(self) -> socket:
        print("Attente d'une connexion ... ")
        client_socket, client_address = self.__socket_ecoute.accept()
        print(f"connexion avec le client : {client_address}")
        return client_socket
    
class ServiceEchange :
    def __init__(self, socket_echange:socket) -> None:
        self.__socket_echange = socket_echange
    
    def envoyer(self, msg:str) -> None:
        self.__socket_echange.send(msg.encode('utf-8'))
        
        
    def recevoir(self) -> str:
        tab_octets = self.__socket_echange.recv(1024)
        return tab_octets.decode(encoding='utf-8')

    
    def echange(self)->None:
        fin:bool =False
        while(not fin):

            tab_octets = self.__socket_echange.recv(1024)

            msg_client = tab_octets.decode(encoding="utf-8")
            print("message du client :", msg_client)

            msg_serveur:str = f"**{msg_client}**"

            if msg_client == "fin":
                fin=True

            tab_octets = msg_serveur.encode(encoding="utf-8")
            self.__socket_echange.send(tab_octets)
    
    
    def arret(self) -> None:
        self.__socket_echange.close()
    
if __name__=="__main__":
    # declaration des variables
    port_ecoute: int=None
    service_ecoute: ServiceEcoute=None
    socket_client: socket=None
    service_echange: ServiceEchange=None
    # lecture des parametres (le numero de port)
    if len(sys.argv)==2:
        port_ecoute=int(sys.argv[1])
    else:
        port_ecoute=5000
    try:
        service_ecoute=ServiceEcoute(port_ecoute)
        socket_client=service_ecoute.attente()
        service_echange=ServiceEchange(socket_client)
        service_echange.echange()
    except Exception as ex:
        print("erreur : ", ex)
