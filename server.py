#!/usr/bin/python

## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo Principal de Server (server.py) ##

# Definicion de Imports #
import getopt, sys, threading, os
from src.client.clientSocket import ClientSocket
from src.exceptions.argumentError import ArgumentError
from src.exceptions.clientError import ClientError
from src.server.dtServer import DtServer
from src.server.descubrimiento import DISCOVER, ANNOUNCE
from src.server.udpSocket import UDPSocket
from src.util.utilis import checkIp, checkPort

# Definicion de Constantes #
DEFAULT_DATOS_PORT = 2022
DEFAULT_ANNOUNCE_PORT = 2023
DEFAULT_DISCOVER_PORT = 2024

HELP = [("server.py [options] | <ServerIP> <ServerDatosPort> "
    "[<ServerAnnouncePort>] [<ServerDiscoverPort>]\n"),
    (" ServerIP:           Dirección IP del servidor\n"
    "  ServerDatosPort:    Puerto del servidor de DATOS\n"
    "  ServerAnnouncePort: Puerto del servidor de ANNOUNCE\n"
    "  ServerDiscoverPort: Puerto del servidor de DESCUBRIMIENTO\n"
    "Options:\n  -h:    Imprime el texto de ayuda")]

HELP_COMMANDS = [("[HELP]\n"
    "  active threads:  Muestra la cantidad de Threads activos\n"
    "  clear:           Limpia la consola\n"
    "  exit:            Termina el proceso de server\n"
    "  get clients:     Retorna la cantidad de clientes actualmente conectados\n"
    "  get database:    Retorna las keys de la base de datos\n"
    "  get peers:       Retorna los peers descubiertos\n"
    "  get server info: Retorna la informacion del server\n"
    "  help:            Obtiene ayuda")]

# Agregar comandos en orden alfabetico ascendente
COMMANDS = ["active threads", "clear", "get clients","get database", "get peers", 
    "get server info", "help"]

# Definicion de Funciones #

def handle_args(argv):
    opts, args = getopt.getopt(argv,"h")
    if (('-h', '') in opts):
        print(HELP[0], HELP[1])
        return None, None, None, None
    if (len(args) > 4):
        raise ArgumentError("[ATENCION] Demasiados argumentos")
    if (len(args) < 2):
        raise ArgumentError("[ATENCION] Argumentos faltantes")
    addr = checkIp(args[0])
    datos_port = checkPort(args[1]) if args[1] != 'default' else DEFAULT_DATOS_PORT
    announce_port = checkPort(args[2]) if ((len(args) > 2) and 
        (checkPort(args[2]) != datos_port)) else DEFAULT_ANNOUNCE_PORT
    discover_port = checkPort(args[3]) if ((len(args) > 3) and 
        ((checkPort(args[3]) != datos_port) and 
        (checkPort(args[3]) != announce_port))) else DEFAULT_DISCOVER_PORT
    return addr, datos_port, announce_port, discover_port

def handle_commands(server: DtServer, command: int):
    COMMANDS_FUNC = [
        lambda: print("[SERVER] Cantidad de threads activos: ", threading.active_count()),
        lambda: os.system('cls||clear'),
        lambda: print('[CLIENTS] Cantidad de clientes con conexiones activas: ', threading.active_count() - 5),
        lambda: print("[DATABASE] ", server.database.get_keys()),
        lambda: print("[PEERS] ", server.peers.get_peers_keys()),
        lambda: print(f"""[SERVER]*Direccion IP: {server.ip}
        *Puerto DATOS: {server.datos_port}
        *Puerto ANNOUNCE: {server.announce_port}
        *Puerto DESCUBRIMIENTO: {server.descubrimiento_port}
        *Firma CRC32: {hex(server.firma)}"""),
        lambda: print(HELP_COMMANDS[0])]
    if (command >= 0 and command < 7):
        COMMANDS_FUNC[command]()
    else:
        raise ValueError("Comando invalido")
    return

def handle_discover(server: DtServer, conn):
    while True:
        try:
            DISCOVER(server, conn)
        except Exception as e:
            print(f"[SERV_ERR] {str(e)}")
    conn.close()
    return

def handle_announce(server: DtServer, conn):
    while(True):
        try:
            ANNOUNCE(server, conn)
        except Exception as e:
            print(f"[SERV_ERR] {str(e)}")
    conn.close()
    return

def check_token(server_crc: str, msg: str) -> bool:
    return msg == f"SRV_CONN {server_crc}\n"

def handle_client(server: DtServer, conn: ClientSocket):
    while True:
        response = "NO\n"
        try:
            msg = conn.receive()
            response = server.processRequest(msg)
            conn.send(response)
        except ClientError as e:
            print("[CLIENTS] ", str(e))
        except Exception:
            # Se ha roto la conexion con un cliente y termina el thread
            conn.close()
            break
    return

def handle_datos(server: DtServer, conn: ClientSocket):
    conn.bind(server.ip, server.datos_port)
    conn.listen()
    while True:
        conn_c, addr_c = conn.accept()
        (ip, port) = conn_c.getpeername()
        print(f"[NUEVA_CONEXION] {ip}:{port} conectado.")
        thread_client = threading.Thread(target=handle_client, args=(server, ClientSocket(conn_c)), daemon=True)
        thread_client.start()
    return

# Funcion principal #

def main(args):
    try:
        ip, datos_port, announce_port, discover_port = handle_args(args)
        if (ip == None):
            return None
    except Exception as e:
        print(f"[ATENCION] {str(e)}")
        print(HELP[0])
        return None

    try:
        # Inicializacion del server #
        server = DtServer(ip, datos_port, announce_port, discover_port) 
        announce_udp_socket = UDPSocket(server.announce_port) # Crear announce socket
        discover_udp_socket = UDPSocket(server.descubrimiento_port) # Crear discover socket
        datos_tcp_socket = ClientSocket() # Crear client socket
        thread_announce = threading.Thread(target=handle_announce, args=(server, announce_udp_socket), daemon=True)
        thread_discover = threading.Thread(target=handle_discover, args=(server, discover_udp_socket), daemon=True)
        thread_datos = threading.Thread(target=handle_datos, args=(server, datos_tcp_socket), daemon=True)
        thread_announce.start()
        thread_discover.start()
        thread_datos.start()
        print(f"[SERVER] Servidor atendiendo DATOS en {ip}:{datos_port}")
        print(f"[SERVER] Servidor atendiendo ANNOUNCE en {ip}:{announce_port}")
        print(f"[SERVER] Servidor atendiendo DISCOVER en {ip}:{discover_port}")
        while True:
            command = input()
            try:
                handle_commands(server, COMMANDS.index(command))
            except ValueError:
                if (command == "exit"):
                    raise KeyboardInterrupt("Exit")
                print("[CMND] El comando no es correcto, ingrese 'help' para obtener ayuda")
    except KeyboardInterrupt:
        # Si hay Cntr + C matar todos los threads
        print("[SERVER] Deteniendo servidor")
        # Cerrar todos los sockets
        announce_udp_socket.sock.close()
        discover_udp_socket.sock.close()
        datos_tcp_socket.sock.close()
        server.peers.shutdown_peer_sockets()
    return

# Main Init #
if __name__ == "__main__":
    main(sys.argv[1:])