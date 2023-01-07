## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo de ClientSocket (clientSocket.py) ##

# Definicion de Imports #
import socket
from datetime import datetime
from src.exceptions.clientError import ClientError

# Definicion de Constantes #
SIZE = 1024 # Tamanio del buffer del mensaje
FORMAT = 'utf-8' # Formato del mensaje
WAITING_TIME = 60 # Tiempo de espera por un mensaje (en segundos)

# Definicion clase ClientSocket #
class ClientSocket:
    # Inicializar el socket del cliente
    def __init__(self, sock=None):
        if sock == None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    #######################
    # Funciones de Server #
    #######################
    
    def accept(self):
        return self.sock.accept()
        
    def listen(self):
        self.sock.listen()
        return

    ########################
    # Funciones de Cliente #
    ########################

    # Conecta con un socket remoto en host:port
    # Nota: Lanza las excepciones TimeoutError y InterruptedError
    def connect(self, host, port):
        self.sock.connect((host, int(port)))

    #######################
    # Funciones generales #
    #######################
    
    def bind(self, addr, port):
        self.sock.bind((addr, port))
        return

    # Precondicion: se debe estar conectado con el socket remoto
    def send(self, msg):
        data = msg.encode(FORMAT)
        if (len(data) == 0):
            raise ClientError("El mensaje a enviar es vacio")
        sent = self.sock.sendall(data)
        if (sent != None):
            raise ClientError("Ha ocurrido un error al enviar el mensaje")
            
    # Precondicion: se debe estar conectado con el socket remoto
    def receive(self) -> str:
        data = ''
        init_time = datetime.now()
        while not data.endswith("\n"):
            current_time = datetime.now()
            if  (current_time - init_time).total_seconds() > WAITING_TIME:
                raise TimeoutError("Tiempo de conexion excedido")
            msg = self.sock.recv(SIZE)
            data += msg.decode(FORMAT)
        return data

    # Finalizar conexion con el socket remoto
    def close(self):
        self.sock.close()

    # Envia el mensaje 'msg' al socket remoto en addr:port siguiendo el 
    #   Protocolo DATOS
    # Mantiene persistente la conexion y retorna la respuesta por parte del servidor.
    def send_msg_datos(self, msg: str) -> str:
        self.send(msg) # Enviar mensaje (DATOS)
        data = self.receive() # Recibir respuesta
        return data

