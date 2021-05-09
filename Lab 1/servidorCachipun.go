package main

import (
	"fmt"
	"math/rand"
	"net"
	"strconv"
	"strings"
	"time"
)

func mensaje_bienvenida() {
	fmt.Println("Iniciando Servidor")
}

func main() {
	rand.Seed(time.Now().UTC().UnixNano())
	go mensaje_bienvenida()
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
		//fmt.Print(addr, err) esto printea el IP address y si hay error
		fmt.Print("\n")
		fmt.Print("-> " + string(buffer[0:n]) + "\n")

		if strings.TrimSpace(string(buffer[0:n])) == "STOP" {
			fmt.Println("Exiting UDP server!")
			_, err = connection.WriteToUDP([]byte("muere cachipun"), addr)
			return
		}
		RandomIntegerwithinRange := rand.Intn(10) //problema con el random, tal vez falta semilla
		fmt.Println(strconv.Itoa(RandomIntegerwithinRange))
		if strings.TrimSpace(string(buffer[0:n])) == "Tira tu jugada" {
			RandomIntegerwithinRange = rand.Intn(3) + 1
			fmt.Print("Esta es la jugada papucho\n")
			fmt.Println(strconv.Itoa(RandomIntegerwithinRange))
		}

		mensaje := []byte(strconv.Itoa(RandomIntegerwithinRange))
		_, err = connection.WriteToUDP(mensaje, addr)
		if err != nil {
			fmt.Println(err)
			return
		}
	}
}
