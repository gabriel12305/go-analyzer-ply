package main

import "fmt"

func calcularDemanda() int {
	const limite = 10

	var activo = true
	var terminado = false

	var demanda = map[string]int{
		"FIEC":        5,
		"Rectorado":   8,
		"Tecnologias": 3,
	}

	var total = 0

	for parada := range demanda {
		total = total + demanda[parada]
	}

	if activo == true {
		total = total + 1
	} else {
		total = total - 1
	}

	switch total {
	case 0:
		terminado = true
	case 10:
		terminado = false
	default:
		terminado = false
	}

	if terminado == false {
		return total
	}

	fmt.Print("Hola")
	fmt.Println(variableinexistente)

	var edad int = 10
	fmt.Println(edad)

	var a int = 10
	var b int = 20
	var c int = a + b

	var resultado bool = activo + false
	return 0
	#
	@
}
