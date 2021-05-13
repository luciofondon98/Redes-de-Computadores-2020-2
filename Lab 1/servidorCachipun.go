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
	PUERTO := ":51234" //socket 50000 al 50020
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
		fmt.Print("\n")
		fmt.Print("-> " + string(buffer[0:n]) + "\n")

		if strings.TrimSpace(string(buffer[0:n])) == "STOP" {
			fmt.Println("Exiting UDP server!")
			_, err = connection.WriteToUDP([]byte("muere cachipun"), addr)
			return
		}
		RandomIntegerwithinRange := rand.Intn(10)

		if RandomIntegerwithinRange != 0 { // si cachipun quiere jugar una partida
			fmt.Println("Ya! Juguemos un cachipun.")
			PUERTO_ALEATORIO := 52000 + rand.Intn(110)
			fmt.Println("Puerto nuevo para el juego es: " + strconv.Itoa(PUERTO_ALEATORIO))
			mensaje_con_puerto_nuevo := []byte(strconv.Itoa(PUERTO_ALEATORIO))
			_, err = connection.WriteToUDP(mensaje_con_puerto_nuevo, addr)

			//Conexión puerto jugada

			PUERTO_NUEVO := ":" + strconv.Itoa(PUERTO_ALEATORIO) //socket 50000 al 50020
			BUFFER := 1024
			s, err := net.ResolveUDPAddr("udp4", PUERTO_NUEVO)
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
				fmt.Print("\n")
				fmt.Print("-> " + string(buffer[0:n]) + "\n")

				if strings.TrimSpace(string(buffer[0:n])) == "Terminar partida" {
					fmt.Println("Cerrando puerto de juego")
					_, err = connection.WriteToUDP([]byte("Terminó la partida, cerrando puerto de juego."), addr)
					break
				}

				RandomIntegerwithinRange = rand.Intn(3) + 1
				fmt.Print("La opción del servidor cachipun es: " + strconv.Itoa(RandomIntegerwithinRange) + "\n")

				mensaje := []byte(strconv.Itoa(RandomIntegerwithinRange))
				_, err = connection.WriteToUDP(mensaje, addr)
				if err != nil {
					fmt.Println(err)
					return
				}
			}

		} else {

			mensaje := []byte(strconv.Itoa(RandomIntegerwithinRange))
			_, err = connection.WriteToUDP(mensaje, addr)
			if err != nil {
				fmt.Println(err)
				return
			}
		}
	}
}
