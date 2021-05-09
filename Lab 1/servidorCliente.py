import socket as skt

#-----------------CONEXION TCP CON INTERMEDIARIO---------------------------------------#
serverAddr = 'localhost'
puertoServidor = 52457 #mismo puerto que el del cliente
socketCliente = skt.socket(skt.AF_INET, skt.SOCK_STREAM) #Sockstream = TCP
socketCliente.connect((serverAddr,puertoServidor)) #Cliente realiza el Handshake

#-----------------CONEXION TCP CON INTERMEDIARIO---------------------------------------#

def jugarCachipun():
    while(1):
        jugada_cliente = input("Ingresa tu jugada\n1) Papel\n2) Piedra\n3) Tijera\n")
        socketCliente.send(jugada_cliente.encode()) #envia jugada a intermediario
        resultado = socketCliente.recv(2048).decode()
        print(resultado)
        if "3" in resultado:
            break



while(1):
    mensajeInicio = input('Ingrese una opcion:\n0) Salir\n1) Jugar\n')
    socketCliente.send(mensajeInicio.encode())
    response = socketCliente.recv(2048).decode()
    if response == '0': #Servidor cachipun no quiere jugar
        print("Cliente apagado")
        break
    elif response == '1':
        print("Servidor Cachipun quiere jugar, empezamos el juego.\n")
        jugarCachipun()
        ganador = socketCliente.recv(2048).decode()
        print(ganador)
    

socketCliente.close()