## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo de Database (database.py) ##

# Definicion de Imports #
from threading import Lock

# Definicion clase Database #
class Database:
    def __init__(self):
        self.database: dict(str) = {}
        self.lock = Lock()
        return

    # Si la key no existe, se lanza KeyError
    def get(self, key: str) -> str:
        with self.lock:
            value = self.database[key]
        return value

    def set(self, key: str, value: str):
        with self.lock:
            self.database[key] = value
        return

    # Si la key no existe, se lanza KeyError
    def delete(self, key: str):
        with self.lock:
            del self.database[key]
        return
    
    def get_keys(self):
        with self.lock:
            keys = self.database.keys()
        return keys

    # Retorna un set con todos los datos de la base de datos
    def get_all(self):
        with self.lock:
            values = self.database.copy()
        return values