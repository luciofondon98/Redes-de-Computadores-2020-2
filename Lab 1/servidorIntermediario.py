import socket as skt

def terminarPrograma():
    cachipunSocket.sendto('STOP'.encode(), (serverAddr, serverPort))
    msg, addr = cachipunSocket.recvfrom(2048)
    print(msg.decode())
    clientSocket.send('0'.encode())

def solicitarJugar():
    ...

#-----------------CONEXION TCP CON CLIENTE---------------------------------------#

serverPort = 52457 #49152-65535

serverSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM) #primer prámetro indica que se trabaja con pv4
                                                        #segundo indica que se trabaja en TCP
#Sockstream = TCP, AFINET = IPV4
serverSocket.bind(('',serverPort))

serverSocket.listen(1) #queda escuchando esperando mensajes

print('Servidor TCP escuchado en: ', serverPort)

clientSocket, clientAddr = serverSocket.accept()

serverAddr = 'localhost'
serverPort = 50003 
cachipunSocket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)

while(1):
    msg = clientSocket.recv(2048).decode() #decodifica mensaje, ya que viene en bytes
    print(msg)
    if msg == '0':
        terminarPrograma()
        break
    elif msg == '1':
        solicitarJugar()
    
    # respuesta = input('Ingresa tu respuesta: ')
    # clientSocket.send(respuesta.encode()) #envía respuesta al cliente codificada
clientSocket.close()