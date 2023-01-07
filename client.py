#!/usr/bin/python

## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo Principal de Cliente (client.py) ##

# Definicion de Imports #
import sys, getopt
from src.client.clientSocket import ClientSocket
from src.exceptions.keyError import KeyError
from src.exceptions.methodError import MethodError
from src.util.utilis import checkIp, checkPort, genMsgDatos, parseCommand

# Definicion de Constantes #
HELP = ["client.py [options] | <ServerIP> <ServerPort> <Op> <Key> [<Value>]\n",
    (" ServerIP:        Dirección IP del servidor al que se desea conectar\n"
    "  ServerPort:      Puerto del servidor al que se desea conectar\n"
    "  Op:              Operación a realizar: GET, SET o DEL\n"
    "  Key:             Clave del valor que se desea leer, escribir o borrar\n"
    "  Value:           Valor a almacenar. Solo al usar metodo SET\n\n"
    "Options:\n  -h:    Imprime el texto de ayuda\n"
    "-p:    Persiste la conexion con el servidor")]

EXIT = ["cerrar", "exit", "quit", "salir"]

# Definicion de Funciones #

# Envia y recibe datos entre el cliente y el servidor utilizando el socket TCP
#   'sock'. Luego, imprime los datos obtenidos.
# Precondicion: 'sock' debe estar inicializado.
def send_recv_data(sock: ClientSocket, ip: str, port: str, msg):
    try:
        msg = genMsgDatos(msg[0], msg[1], msg[2])
        if (parseCommand(msg)[0] == None):
            print("[ATENCION] Formato de mensaje invalido")
            return None
        print('\nSumario:')
        print('*Conexion: %s:%d\n' % (ip, port))
        print('*Mensaje enviado: %s' % msg)
        data = sock.send_msg_datos(msg)
        print('*Respuesta obtenida: %s' % data)
    except (ValueError, KeyError, MethodError) as ke:
        print("[ATENCION] ", str(ke))
        print(HELP[0])
    return

# Metodo de comunicacion con servidor mediante el Protocolo DATOS
# Precondiciones:
# - Host:Port tienen un formato valido, es decir: xxx.xxx.xxx.xxx:yyyy
# - Msg es un mensaje valido para el Protocolo DATOS
def client_datos(ip: str, port: int, persist: bool, msg):
    try:
        sock = ClientSocket() # Crea el socket TCP
        sock.connect(ip, port)
        print(f'Conectando con servidor {ip}:{port}')
        while True:
            try:
                send_recv_data(sock, ip, port, msg)
            except TimeoutError as te:
                print('[TIMEOUT_ERR] ' + str(te))
                break
            except InterruptedError as ie:
                print('[INTERRUPTED_ERR] ' + str(ie))
                break
            except IndexError:
                print("[ATENCION] Comando no reconocido")
            except Exception as e:
                print('[ERR] ' + str(e))
                break
            # Terminar el loop y cerrar el socket si no se persiste mas la conexion
            if not persist:
                break
            user_input = input("\n")
            if (user_input.lower() in EXIT):
                break
            try:
                msg = user_input.split()[0:3]
                if (len(msg) > 1 and len(msg) < 4):
                    if (len(msg) < 3):
                        msg.append('')
            except IndexError:
                print("[ATENCION] Comando no reconocido")
        sock.close()
    except KeyboardInterrupt:
        sock.close()
        raise KeyboardInterrupt()
    return

# Funcion principal, ejecuta la logica de cliente para los argumentos ingresados
#   en la invocacion. Utilizada por clientCLI.py para "MetodoManual"
def main(argv):
    persist_conn = False
    try:
        opts, args = getopt.getopt(argv,"hp")
    except getopt.GetoptError:
        print(HELP[0])
        return None
    if (('-h', '') in opts):
        print(HELP[0], HELP[1])
        return None
    if (('-p', '') in opts):
        persist_conn = True
    if (len(args) > 5):
        print("[ATENCION] Demasiados argumentos")
        print(HELP[0])
        return None
    elif (len(args) < 4):
        print("[ATENCION] Argumentos faltantes")
        print(HELP[0])
        return None
    elif (len(args) == 4): # Seteo value como el string vacio, si no existe
        args.append('')
    try:
        mensaje = (args[2], args[3], args[4])
        client_datos(checkIp(args[0]), checkPort(args[1]), persist_conn, mensaje)
    except Exception as e:
        print("[ATENCION] ", str(e))
        print(HELP[0])
    return None

# Main Init #
if __name__ == "__main__":
    main(sys.argv[1:])