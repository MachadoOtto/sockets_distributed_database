## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo de Utilidades (utilis.py) ##

# Definicion de Imports #
import ipaddress # Utilizado para checkear direcciones IPv4
import re # Regex
from src.exceptions.keyError import KeyError
from src.exceptions.methodError import MethodError

# Definicion de Constantes #
METHODS = ['GET', 'SET', 'DEL']
CHARS_TO_FILTER = [" ", "\n", "\r", "\t"]

# Definicion de Funciones #

# Checkea si 'addr' es una direccion IPv4 valida
def checkIp(addr: str) -> str:
    res = False
    try:
        ip = ipaddress.ip_address(addr)
        if (ip.version == 4):
            res = True
    except ValueError:
        pass
    if (not res):
        raise ValueError("Formato de direccion IP no valido")
    return addr

# Checkea si 'port' es un puerto valido
def checkPort(port: str) -> int:
    res = False
    try:
        port = int(port)
        if (port >= 0 and port <= 65535):
                res = True
    except ValueError:
        pass
    if (not res):
        raise ValueError("Formato de puerto no valido")
    return int(port)

# Checkea si 'input' NO contiene espacios o caracteres especiales como:
#   "\n", "\r", "\t"
def checkStr(value: str) -> bool:
    for spChar in CHARS_TO_FILTER:
            if spChar in value:
                return False
    return True

# Genera el mensaje a enviar siguiendo el prtocolo DATOS
# En caso de que el mensaje no cumpla con el protocolo, se genera una
#   excepcion acorde, tales como:
# - MethodError: Ocurre cuando el metodo indicado no es soportado por DATOS
# - KeyError: Ocurre cuando la key contiene caracteres especiales como espacios,
#   "\n", "\r" o "\t"; o es vacio
# - ValueError: Ocurre cuando el valor contiene caracteres especiales como 
#   espacios, "\n", "\r" o "\t"; o es vacio
def genMsgDatos(method: str, key: str, value: str) -> str:
    message = method.upper()
    if message in METHODS:
        if (checkStr(key) and not key == ''):
            message += ' ' + key
            if (method == 'SET'):
                if (checkStr(value) and not value == ''):
                    message += ' ' + value
                else:
                    raise ValueError("El valor \"%s\" ingresado no es valido" % value)
            return message + '\n'
        else:
            raise KeyError("La key \"%s\" ingresada no es valida" % key)
    else:
        raise MethodError("Metodo \"%s\" no soportado" % method)

#Devuelve el metodo o None en caso de tener un formato erróneo
def parseCommand(command: str) -> tuple:
    regex_methods = {
        "GET": r'^GET (\d|\w+)\n$',
        "SET": r'^SET (\d|\w+) (\d|\w+)\n$',
        "DEL": r'^DEL (\d|\w+)\n$'
    }
    for method in regex_methods:
        regex = re.compile(regex_methods[method])
        method_match = regex.match(command)
        if method_match is not None:
            key = method_match.group(1)
            value = method_match.group(2) if method == "SET" else None
            return method, key, value
    return None, None, None

def formatResponse(method: str, response: str) -> str:
    if method == None:
        return "NO\n"
    if method == "GET":
        return f'OK {response}\n'
    return 'OK\n'

# Retorna true si la distancia entre input_value y value1 es menor o igual que
# la distancia entre input_value y value2
def is_minimum(input_value: int, value1: int, value2: int) -> bool:
    diff1 = input_value - value1
    diff2 = input_value - value2
    return (abs(diff1) <= abs(diff2))