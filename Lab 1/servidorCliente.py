import socket as skt


serverAddr = 'localhost'
puertoServidor = 52456 #mismo puerto que el del cliente
socketCliente = skt.socket(skt.AF_INET, skt.SOCK_STREAM)

socketCliente.connect((serverAddr,puertoServidor)) #Cliente realiza el Handshake
toSend = input("Ingresar texto a enviar: ")
socketCliente.send(toSend.encode())
response = socketCliente.recv(2048).decode()
print(response)
socketCliente.close()