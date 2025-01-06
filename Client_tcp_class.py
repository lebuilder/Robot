import socket
import sys

class Client_TCP:
    def __init__(self, ip_serveur: str, port_serveur: int) -> None:
        self.__ip_serveur = ip_serveur
        self.__port_serveur = port_serveur
        self.__socket_echange = None

    def connexion(self) -> None:
        try:
            self.__socket_echange = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket_echange.connect((self.__ip_serveur, self.__port_serveur))
            
            print(f"Connecter au serveur : {self.__ip_serveur} sur le port : {self.__port_serveur}")
            
        except Exception as ex:
            print("Erreur de connexion:", ex)
            self.arret()
    
    def get_ip(self) -> str:
        return self.__socket_echange.getsockname()
    

    def envoyer(self, msg: str) -> None:
        self.__socket_echange.sendall(msg.encode())

    def recevoir(self) -> str:
        return self.__socket_echange.recv(1024).decode()

    def echange(self) -> None:
        msg_client = input("Message pour le serv : ")
        self.envoyer(msg_client)
        print(f"C=>S : {msg_client}")
        msg_serveur = self.recevoir()
        print(f"S=>C : {msg_serveur}")
        self.arret()

    def arret(self) -> None:
        if self.__socket_echange:
            self.__socket_echange.close()

if __name__ == "__main__":
    ip_serveur: str = None
    port_serveur: int = None
    client: Client_TCP = None

    if len(sys.argv) == 3:
        ip_serveur = sys.argv[1]
        port_serveur = int(sys.argv[2])
    else:
        ip_serveur = "127.0.0.1"
        port_serveur = 5000

    client = Client_TCP(ip_serveur, port_serveur)
    client.connexion()
    client.echange()
    client.arret()