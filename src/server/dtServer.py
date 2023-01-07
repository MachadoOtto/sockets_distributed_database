## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo de DtServer (dtServer.py) ##

# Definicion de Imports #
import zlib
from src.server.peerHandler import PeerHandler
from src.server.database import Database
from src.util.utilis import parseCommand, formatResponse

# Definicion de Clase DtServer #
class DtServer:
    def __init__(self, ip: str, datos_port: int, announce_port: int, descubrimiento_port: int):
        self.ip = ip # Direccion SERVER
        self.datos_port = datos_port # TCP DATOS
        self.announce_port = announce_port # UDP ANNOUNCE
        self.descubrimiento_port = descubrimiento_port # UDP DESCUBRIMIENTO
        
        self.firma = zlib.crc32(f'{ip}:{datos_port}'.encode())
        self.database = Database()
        self.peers = PeerHandler()
        return

    # Determina el servidor reponsable de la key
    # Retorna ip y puerto de datos del responsable
    def determine_designated_server(self, key_crc: int):
        min_distance = abs(self.firma - key_crc)
        (min_ip, min_port) = (self.ip, self.datos_port)
        for peer in self.peers.get_peers():
            peer_distance = abs(peer.crc - key_crc)
            if peer_distance < min_distance:
                min_distance = peer_distance
                (min_ip, min_port) = peer.ip, peer.datos_port
        return min_ip, min_port
    
    # Procesa la request obteniendo una respuesta acorde al protocolo DATOS
    # En caso de ser necesario, envia la peticion a otro servidor responsable
    # En caso de error con el metodo se lanza la excepcion MethodError
    def processRequest(self, request: str) -> str:
        database_access = {
            "GET": {"database_access": lambda key, value: self.database.get(key),   "success_msg": lambda key: f"[DATABASE] Elemento {key} obtenido"},
            "SET": {"database_access": self.database.set,                           "success_msg": lambda key: f"[DATABASE] Valor nuevo almacenado en elemento {key}"},
            "DEL": {"database_access": lambda key, value: self.database.delete(key),"success_msg": lambda key: f"[DATABASE] Elemento {key} eliminado"},
        }
        response = formatResponse(None, None)
        (method, key, value) = parseCommand(request)
        if method == None:
            print("Comando no soportado: %s" % request)
            return response
        (ip, port) = self.determine_designated_server(int(hex(zlib.crc32(key.encode())), 16))
        if (ip == self.ip and port == self.datos_port):
            try:
                response = database_access[method]["database_access"](key, value)
                response = formatResponse(method, response)
                print(database_access[method]["success_msg"](key))
            except KeyError:
                print(f"[DATABASE] Elemento {key} no encontrado")
                response = formatResponse(None, None)
        else:
            try:
                peer = self.peers.get_peer(ip, port)
                response = peer.get_data(request)
            except Exception:
                print(f'[PEERS] No se ha podido comunicar con el peer {ip}:{port}')
        return response