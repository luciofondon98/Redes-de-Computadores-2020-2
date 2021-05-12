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
serverPort = 51234 
cachipunSocket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
#-----------------CONEXION UDP CON CACHIPUN---------------------------------------#

def queJugadaEs(jugada):
    if jugada == 1:
        return "Papel"
    elif jugada == 2:
        return "Piedra"
    elif jugada == 3:
        return "Tijera"

def terminarPrograma():
    cachipunSocket.sendto('STOP'.encode(), (serverAddr, serverPort))
    msg, addr = cachipunSocket.recvfrom(2048)
    print(msg.decode())
    clientSocket.send('0'.encode())

def solicitarJugar():
    print("Solicitando a servidor cachipun jugar una partida")
    cachipunSocket.sendto('Oye wn, quieren jugar, queri?'.encode(), (serverAddr, serverPort))
    respuestaCachipun, addr = cachipunSocket.recvfrom(2048)
    if (respuestaCachipun.decode() == "0"): #cachipun no quiere jugar
        return "No"
    else: #desde [1-9] 90% de jugar
        puerto_nuevo = int(respuestaCachipun.decode())
        return puerto_nuevo #retorna puerto nuevo donde se jugará cachipun

def solicitarJugadaACachipun(puerto):
    cachipunSocket.sendto('Tira tu jugada'.encode(), (serverAddr, puerto))
    jugada_cachipun, addr = cachipunSocket.recvfrom(2048)
    return jugada_cachipun

def jugarCachipun(puerto):

    #-----------------CONEXION UDP CON CACHIPUN---------------------------------------#
    serverAddr = 'localhost'
    serverPort = puerto 
    # cachipunSocket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
    #-----------------CONEXION UDP CON CACHIPUN---------------------------------------#

    puntaje_cliente = 0
    puntaje_cachipun = 0
    ganador = ""
    while (1):
        jugada_cliente = int(clientSocket.recv(2048).decode()) #decodifica mensaje, ya que viene en bytes
        jugada_cachipun = int(solicitarJugadaACachipun(puerto))
        mensaje = ""
        jugadas = "Jugaste " + queJugadaEs(jugada_cliente) + ". Cachipun jugó " + queJugadaEs(jugada_cachipun) + "\n"
        if jugada_cliente == jugada_cachipun: #empate
            mensaje = "Empate, ambos jugaron " + queJugadaEs(jugada_cliente)
        elif jugada_cliente%3 == (jugada_cachipun+1)%3: #cliente pierde      
            puntaje_cachipun+=1
            if (puntaje_cachipun == 3):
                mensaje = jugadas + "Perdiste, ganó cachipun: Cliente -> " + str(puntaje_cliente) + " Servidor Cachipun " + str(puntaje_cachipun)
                clientSocket.send(mensaje.encode())
                break
            mensaje = jugadas + "Servidor cachipun ganó, la cuenta va: Cliente -> " + str(puntaje_cliente) + " Servidor Cachipun " + str(puntaje_cachipun)
        elif (jugada_cliente+1)%3 == jugada_cachipun%3: #cliente gana
            puntaje_cliente+=1
            if (puntaje_cliente == 3):
                mensaje = jugadas + "Ganaste la ronda Cliente -> " + str(puntaje_cliente) + " Servidor Cachipun " + str(puntaje_cachipun) 
                clientSocket.send(mensaje.encode())
                break
            mensaje = jugadas + "Ganaste, la cuenta va: Cliente -> " + str(puntaje_cliente) + " Servidor Cachipun " + str(puntaje_cachipun)

        clientSocket.send(mensaje.encode())


    cachipunSocket.sendto('Terminar partida'.encode(), (serverAddr, puerto))
    msg, addr = cachipunSocket.recvfrom(2048)
    print(msg.decode())

    if puntaje_cachipun == 3:
        return "Gano cachipun"
    else:
        return "Gano cliente"


while(1): #comienza programa escuchando al cliente
    msg = clientSocket.recv(2048).decode() #decodifica mensaje, ya que viene en bytes
    print(msg)
    if msg == '0': #cliente quiere salir
        terminarPrograma()
        break
    elif msg == '1':  #cliente quiere jugar
        solicitud = solicitarJugar() 
        if solicitud == 'No':
            clientSocket.send("El servidor cachipun no quiere jugar.".encode())
        else: #solicitud contiene puerto nuevo a utilizar para jugar
            clientSocket.send('1'.encode())
            ganador = jugarCachipun(solicitud)
            clientSocket.send(ganador.encode())
clientSocket.close()