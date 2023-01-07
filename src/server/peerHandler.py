## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo de Peer y PeerHandler (peerHandler.py) ##

# Definicion de Imports #
from threading import Lock
from datetime import datetime
from src.client.clientSocket import ClientSocket

# Definicion clase Peer #
class Peer:
    def __init__(self, ip: str, datos_port: int, socket: ClientSocket, crc: int):
        self.lock = Lock()
        self.ip: str = ip
        self.datos_port: int = datos_port
        self.socket: ClientSocket = socket
        self.crc: int = crc
        self.last_announce_time: datetime = datetime.now()
        return

    def get_data(self, message) -> str:
        with self.lock:
            self.socket.send(message)
            data = self.socket.receive()
        return data

    def update_time(self):
        with self.lock:
            self.last_announce_time = datetime.now()
        return

    def acquire(self):
        self.lock.acquire()

    def release(self):
        self.lock.release()

# Definicion clase PeerHandler #
class PeerHandler:
    def __init__(self, peers: dict = {}):
        self.lock = Lock()
        self.peers: dict = peers

    def get_peers(self):
        with self.lock:
            peers = list(self.peers.values())
        return peers

    def get_peers_keys(self):
        with self.lock:
            keys = list(self.peers.keys())
        return keys

    def get_peer(self, addr, port):
        with self.lock:
            value = self.peers[self.__format_key(addr, port)]
        return value
        
    def set_peer(self, addr, port, peer: Peer, lock = True):
        if lock:
            self.lock.acquire()
        self.peers[self.__format_key(addr, port)] = peer
        if lock:
            self.lock.release()
        return

    def delete_peer(self, addr, port):
        with self.lock:
            del self.peers[self.__format_key(addr, port)]
        return

    def acquire(self):
        self.lock.acquire()

    def release(self):
        self.lock.release()

    def exists(self, ip, port, lock = True):
        if lock:
            self.lock.acquire()
        exists_peer = self.__format_key(ip, port) in self.peers.keys()
        if lock:
            self.lock.release()
        return exists_peer

    # Funciones auxiliares #

    # Cierra los sockets de los peers
    def shutdown_peer_sockets(self):
        with self.lock:
            for peer in self.peers.values():
                peer.socket.close()
        return

    def addr_is_peer(self, ip, port, lock = True) -> bool:
        res = False
        if lock:
            self.lock.acquire()
            for peer in self.peers.values():
                if (peer.socket.sock.gethostname() == (ip, port)):
                    res = True
                    break
        if lock:
            self.lock.release()
        return res
    
    def __format_key(self, addr, port) -> str:
        return f'{addr}:{port}'