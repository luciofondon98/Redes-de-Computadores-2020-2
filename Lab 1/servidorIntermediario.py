
import socket as skt
serverPort = 52456 #49152-65535

serverSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM) #primer prámetro indica que se trabaja con pv4
                                                        #segundo indica que se trabaja en TCP
#Sockstream = TCP, AFINET = IPV4
serverSocket.bind(('',serverPort))

serverSocket.listen(1) #queda escuchando esperando mensajes

print('Servidor TCP escuchado en: ', serverPort)

clientSocket, clientAddr = serverSocket.accept()
msg = clientSocket.recv(2048).decode() #decodifica mensaje, ya que viene en bytes

respuesta = 'El largo de ' + msg + ' es de ' + str(len(msg)) + ' letras\n'
clientSocket.send(respuesta.encode()) #envía respuesta al cliente codificada
clientSocket.close()