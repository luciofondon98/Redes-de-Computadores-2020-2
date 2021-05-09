import socket as skt


#-----------------CONEXION TCP CON CLIENTE---------------------------------------#
serverPort = 52457 #49152-65535
serverSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM) #primer prámetro indica que se trabaja con pv4
                                                        #segundo indica que se trabaja en TCP
#Sockstream = TCP, AFINET = IPV4
serverSocket.bind(('',serverPort))
serverSocket.listen(1) #queda escuchando esperando mensajes
print('Servidor TCP escuchado en: ', serverPort)
clientSocket, clientAddr = serverSocket.accept()
#-----------------CONEXION TCP CON CLIENTE---------------------------------------#


#-----------------CONEXION UDP CON CACHIPUN---------------------------------------#
serverAddr = 'localhost'
serverPort = 50003 
cachipunSocket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
#-----------------CONEXION UDP CON CACHIPUN---------------------------------------#

def terminarPrograma():
    cachipunSocket.sendto('STOP'.encode(), (serverAddr, serverPort))
    msg, addr = cachipunSocket.recvfrom(2048)
    print(msg.decode())
    clientSocket.send('0'.encode())

def solicitarJugar():
    print("Solicitando a servidor cachipun jugar una partida")
    cachipunSocket.sendto('Oye wn, quieren jugar, queri?'.encode(), (serverAddr, serverPort))
    respuestaCachipun, addr = cachipunSocket.recvfrom(2048)
    return respuestaCachipun.decode()

def solicitarJugadaACachipun():
    cachipunSocket.sendto('Tira tu jugada'.encode(), (serverAddr, serverPort))
    jugada_cachipun, addr = cachipunSocket.recvfrom(2048)
    return jugada_cachipun

def jugarCachipun():
    puntaje_cliente = 0
    puntaje_cachipun = 0
    ganador = ""
    while puntaje_cliente != 3 or puntaje_cachipun != 3:

        jugada_cliente = clientSocket.recv(2048).decode() #decodifica mensaje, ya que viene en bytes
        jugada_cachipun = solicitarJugadaACachipun()
        mensaje = ""
        if jugada_cliente == jugada_cachipun: #empate
            mensaje = "Empate"
        elif jugada_cliente%3 == (jugada_cachipun+1)%3: #cliente pierde      
            puntaje_cachipun+=1
            mensaje = "Servidor cachipun ganó, la cuenta va: Cliente -> " + str(puntaje_cliente) + "Servidor Cachipun" + str(puntaje_cachipun)
        elif (jugada_cliente+1)%3 == jugada_cachipun: #cliente gana
            puntaje_cliente+=1
            mensaje = "Ganaste, la cuenta va: Cliente -> " + str(puntaje_cliente) + "Servidor Cachipun" + str(puntaje_cachipun)

        clientSocket.send(mensaje.encode())

    if puntaje_cachipun == 3:
        return "Gano cachipun"
    else:
        return "Gano cliente"


while(1): #comienza programa
    msg = clientSocket.recv(2048).decode() #decodifica mensaje, ya que viene en bytes
    print(msg)
    if msg == '0':
        terminarPrograma()
        break
    elif msg == '1':
        if solicitarJugar() == 'No':
            terminarPrograma()
            break
        elif solicitarJugar() == 'Si':
            clientSocket.send('1'.encode())
            ganador = jugarCachipun()
            clientSocket.send(ganador.encode())
            
    
    # respuesta = input('Ingresa tu respuesta: ')
    # clientSocket.send(respuesta.encode()) #envía respuesta al cliente codificada
clientSocket.close()