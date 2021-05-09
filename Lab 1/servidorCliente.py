import socket as skt

serverAddr = 'localhost'
puertoServidor = 52457 #mismo puerto que el del cliente
socketCliente = skt.socket(skt.AF_INET, skt.SOCK_STREAM) #Sockstream = TCP


socketCliente.connect((serverAddr,puertoServidor)) #Cliente realiza el Handshake
mensajeInicio = input('Ingrese una opcion:\n 0) Salir\n1) Jugar')

while(1):
    socketCliente.send(mensajeInicio.encode())
    response = socketCliente.recv(2048).decode()
    if response == '0':
        print("Cliente apagado")
        break
    print(response)

socketCliente.close()