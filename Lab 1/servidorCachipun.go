package main

import (
	"fmt"
	"math/rand"
	"net"
	"strconv"
	"strings"
)

func mensaje_bienvenida() {
	fmt.Println("Iniciando Servidor")
}

func main() {
	go mensaje_bienvenida()
	fmt.Print(rand.Intn(100), ",")

	PUERTO := ":50003" //socket 50000 al 50020
	BUFFER := 1024
	s, err := net.ResolveUDPAddr("udp4", PUERTO)
	if err != nil {
		fmt.Println(err)
		return
	}
	connection, err := net.ListenUDP("udp4", s)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer connection.Close()
	buffer := make([]byte, BUFFER)

	for {
		n, addr, err := connection.ReadFromUDP(buffer)
		fmt.Print(addr, err)
		fmt.Print("\n")
		fmt.Print("-> " + string(buffer[0:n]) + "\n")

		if strings.TrimSpace(string(buffer[0:n])) == "STOP" {
			fmt.Println("Exiting UDP server!")
			return
		}
		RandomIntegerwithinRange := rand.Intn(9)

		mensaje := []byte(strconv.Itoa(RandomIntegerwithinRange))
		fmt.Println("mensaje es " + string(mensaje))
		_, err = connection.WriteToUDP(mensaje, addr)
		if err != nil {
			fmt.Println(err)
			return
		}
	}
}
