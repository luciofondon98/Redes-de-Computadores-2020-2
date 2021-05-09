import socket as skt

serverAddr = 'localhost'
puertoServidor = 52457 #mismo puerto que el del cliente
socketCliente = skt.socket(skt.AF_INET, skt.SOCK_STREAM) #Sockstream = TCP


socketCliente.connect((serverAddr,puertoServidor)) #Cliente realiza el Handshake
mensajeInicio = '¿Quieres jugar cachipun?\n'

while(1):
    socketCliente.send(mensajeInicio.encode())
    response = socketCliente.recv(2048).decode()
    if response == 'chupala':
        socketCliente.send('para'.encode())
        break
    print(response)

socketCliente.close()