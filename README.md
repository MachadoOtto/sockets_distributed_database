# Obligatorio 2
## Redes de Computadoras 2022 - Facultad de Ingeniería - UdelaR
GRUPO 16:
 *      Alexis Baladón
 *      Jorge Machado
 *      Mathias Martinez

### Atención:
Aplicaciones ejecutadas utilizando Python versión 3.6.9.

## server.py (Aplicación Servidor):
Método de ejecución:
 *      python3 server.py [options] | <ServerIP> <ServerDatosPort [<ServerAnnouncePort>] [<ServerDiscoverPort>]

donde:
* ServerIP: Dirección IP del servidor.
* ServerDatosPort: Puerto del servidor de DATOS.
* ServerAnnouncePort: Puerto del servidor de ANNOUNCE.
* ServerDiscoverPort: Puerto del servidor de DESCUBRIMIENTO.
* Options:
	* -h: Imprime el texto de ayuda.

Una vez en ejecución se pueden usar los siguientes comandos para obtener diversos valores:
* active threads: Muestra la cantidad de Threads activos.
* clear: Limpia la consola.
* exit: Termina el proceso de server.
* get clients: Retorna la cantidad de clientes actualmente conectados.
* get database: Retorna las keys de la base de datos.
* get peers: Retorna los peers descubiertos.
* get server info: Retorna la informacion del server.
* help: Obtiene ayuda.

## client.py (Aplicación Cliente):
Método de ejecución:
 *      python3 client.py [options] | <ServerIP> <ServerPort> <Op> <Key> [<Value>]

donde:
* ServerIP: Dirección IP del servidor al que se desea conectar.
* ServerPort: Puerto del servidor al que se desea conectar.
* Op: Operación a realizar: GET, SET o DEL.
* Key: Clave del valor que se desea leer, escribir o borrar.
* Value: Valor a almacenar. Solo al usar método SET.
* Options:
	* -h: Imprime el texto de ayuda.
	* -p: Habilita la conexión persistente con el servidor.

## clientCLI.py (Aplicación Cliente con una Interfaz en Línea de Comandos)
Método de ejecución:
 *      python3 clientCLI.py
Opciones:
	(1) Ejecutar método GET
	(2) Ejecutar método SET
	(3) Ejecutar método DEL
	(4) Ejecución manual
	(5) Desplegar ayuda
	(0) Salir
