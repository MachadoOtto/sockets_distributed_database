#!/usr/bin/python

## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo Principal de Cliente (Client.py) ##

# Definicion de Imports #
import os # Utilizado para limpiar la consola
import client
from src.client.clientSocket import ClientSocket
from src.util.utilis import checkIp, checkPort 

# Definicion de Constantes #
METHODS = ['GET', 'SET', 'DEL']
WELCOME_MSG = ("##################################################\n"
    "#           Bienvenido a client.py CLI           #\n"
    "#                                                #\n"
    "# Redes de Computadoras - GRUPO 16               #\n"
    "#                             - Alexis Badalon   #\n"
    "#                             - Jorge Machado    #\n"
    "#                             - Mathias Martinez #\n"
    "##################################################\n")
MENU_OPTS = ("(1) Ejecutar metodo GET\n"
    "(2) Ejecutar metodo SET\n"
    "(3) Ejecutar metodo DEL\n"
    "(4) Ejecucion manual\n"
    "(5) Desplegar ayuda\n\n"
    "(0) Salir\n")
HELP = [("(1) Ayuda para metodo GET\n(2) Ayuda para metodo SET\n"
    "(3) Ayuda para metodo DEL\n(4) Ayuda con ejecucion manual\n\n"
    "(0) Volver al menu anterior\n"), 
    ("  Metodo GET:\nRealiza el metodo GET del Protocolo DATOS para un servidor"
    " dado. \nLa herramienta le solicitara que especifique la direccion IPv4,"
    " puerto y llave.\n"), 
    ("  Metodo SET:\nRealiza el metodo SET del Protocolo DATOS para un servidor"
    " dado. \nLa herramienta le solicitara que especifique la direccion IPv4,"
    " puerto, llave y valor.\n"), 
    ("  Metodo DEL:\nRealiza el metodo DEL del Protocolo DATOS para un servidor"
    " dado. \nLa herramienta le solicitara que especifique la direccion IPv4,"
    " puerto y llave.\n"), 
    ("  Ejecucion Manual:\nPermite la ejecucion manual de operaciones mediante"
    " el Protocolo DATOS.\nEl metodo de invocacion viene dado por:\n"
    "    <ServerIP> <ServerPort> <Op> <Key> [<Value>]\n")]

# Definicion de Funciones #

# Limpia la consola:
def cliClear():
    os.system('cls||clear')
    print(WELCOME_MSG)
    return None

# Imprime el texto de ayuda
def help():
    while True: 
        print(HELP[0])
        try:
            opt = int(input('Seleccione una opcion: '))
            if (opt == 0):
                return None
            cliClear()
            if (opt < 0 or opt > 4):
                print('[ATENCION] El valor ingresado no es valido\n')
            else:
                print(HELP[opt])
                return None
        except ValueError:
            cliClear()
            print('[ATENCION] El valor ingresado no es valido\n')

# Obtiene la direccion a enviar de la entrada de la tabla
def inputAddr():
    cliClear()
    print('Obteniendo direccion a conectar')
    addr = ''
    while True:
        addr = input("Ingrese direccion del servidor: ")
        try:
            addr = checkIp(addr)
            break
        except Exception as e:
            print('[ATENCION] ', str(e), '\n')
    port = 2022
    while True:
        try:
            port = checkPort(input("Ingrese puerto a conectarse: "))
            break
        except ValueError as e:
            print('[ATENCION] ', str(e), '\n')
    return (addr, port)

# Genera los datos necesarios para enviar un mensaje mediante el protocolo DATOS
# Lee la entrada provista por el usuario
# Retorna la tupla (addr, port, message), donde:
# -addr es la direccion IPv4 del servidor
# -port es el puerto del servidor
# -message es el mensaje a ser enviado
def inputMethodAuto(method: str) -> str:
    cliClear()
    print('Generando mensaje con el metodo %s\n' % method)
    key = ''
    while True:
        key = input('Ingrese clave: ')
        if (not key == ''):
            break
        else:
            print('[ATENCION] Por favor, ingrese una clave valida\n')
    value = ''
    if method.upper() == 'SET':
        while True:
            value = input('Ingrese valor: ')
            if (not value == ''):
                break
            else:
                print('[ATENCION] Por favor, ingrese un valor valido\n')
    return (method, key, value)

def manualInput():
    print('Ingrese un comando manual para el Protocolo Datos, siga el siguiente formato:\n',
    "    <ServerIP> <ServerPort> <Op> <Key> [<Value>]\n")
    client.main(input('Comando: ').split())
    return None

def main():
    cliClear()
    while True:
        print(MENU_OPTS)
        try:
            opt = int(input('Seleccione una opcion: '))
            if (opt == 0):
                print('Finalizando...')
                break
            cliClear()
            if (opt < 0 or opt > 5):
                print('[ATENCION] El valor ingresado no es valido\n')
            else:
                if (opt == 4):
                    manualInput()
                elif (opt == 5):
                    help()
                else:
                    (addr, port) = inputAddr()
                    sock = ClientSocket()
                    sock.connect(addr, port)
                    msg = inputMethodAuto(METHODS[opt - 1])
                    client.send_recv_data(sock, addr, port, msg)
                    sock.close()
                input("Presione ENTER para volver al menu principal... ")
                cliClear()
        except KeyboardInterrupt:
            print('Finalizando...')
            sock.close()
            break
        except ConnectionRefusedError:
            cliClear()
            print("[ATENCION] No se puede establecer una conexión ya que el equipo de destino denegó expresamente dicha conexión")
        except ValueError:
            cliClear()
            print('[ATENCION] El valor ingresado no es valido\n')
    return None

# Main Init
if __name__ == "__main__":
    main()