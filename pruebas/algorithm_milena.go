// =====================================================
// CASO DE PRUEBA GENERAL
// MILENA PAZMIÑO
// Analizador Léxico - Sintáctico - Semántico
// =====================================================


// =====================================================
// CÓDIGO CORRECTO
// =====================================================

var edad int
var promedio float64
var nombre string
var activo bool

edad = 21
promedio = 9.75
nombre = "Milena Pazmiño"
activo = true

/*
    Comentario multilínea
    para probar el reconocimiento
    de comentarios
*/

var mensaje string

if edad > 18 {
    mensaje = "Mayor de edad"
} else {
    mensaje = "Menor de edad"
}

nombreUsuario := "Milena"
edadUsuario := 21
promedioUsuario := 9.8
activoUsuario := true

fmt.Println(nombreUsuario)
fmt.Println(edadUsuario)
fmt.Println(activoUsuario)

nombresVacio := []string{}

for edadUsuario > 18 {
    adulto := true
}

suma := 5 + 3
resta := 10 - 2
multiplicacion := 4 * 6
division := 20 / 5
operacionCompleta := (5 + 3) * 2

func obtenerEdad() int {
    return 21
}

func obtenerPromedio() float64 {
    return 9.75
}

func obtenerNombre() string {
    return "Milena"
}

func estaActivo() bool {
    return true
}



// =====================================================
// CASOS DE PRUEBA LÉXICOS
// =====================================================

// ---------- Error Léxico 1 ----------
// Cadena no cerrada

nombre = "Milena Pazmiño

// ---------- Error Léxico 2 ----------
// Carácter ilegal

edad = 20 @ 5

// ---------- Error Léxico 3 ----------
// Símbolo no permitido

# Esto no es un comentario en Go

// ---------- Error Léxico 4 ----------
// Carácter especial ilegal

nombre = "Milena" €


// =====================================================
// CASOS DE PRUEBA SINTÁCTICOS
// =====================================================

// ---------- Error Sintáctico 1 ----------
// Falta el operador =

var numero int
numero 10

// ---------- Error Sintáctico 2 ----------
// Falta cerrar paréntesis

fmt.Println(numero

// ---------- Error Sintáctico 3 ----------
// Falta llave de apertura

if numero > 5
    numero = 20
}

// ---------- Error Sintáctico 4 ----------
// Return incompleto

func obtenerNumero() int {
    return
}

// ---------- Error Sintáctico 5 ----------
// Slice sin cerrar

lista := []string{

// ---------- Error Sintáctico 6 ----------
// For incompleto

for numero > 0


// =====================================================
// CASOS DE PRUEBA SEMÁNTICOS
// =====================================================

// ---------- Error Semántico 1 ----------
// Asignación incorrecta (int <- string)

var edadError int
edadError = "veintiuno"

// ---------- Error Semántico 2 ----------
// Asignación incorrecta (float64 <- bool)

var promedioError float64
promedioError = true

// ---------- Error Semántico 3 ----------
// Asignación incorrecta (string <- int)

var nombreError string
nombreError = 100

// ---------- Error Semántico 4 ----------
// Asignación incorrecta (bool <- string)

var activoError bool
activoError = "true"

// ---------- Error Semántico 5 ----------
// Retorno incorrecto (int <- bool)

func edadIncorrecta() int {
    return true
}

// ---------- Error Semántico 6 ----------
// Retorno incorrecto (float64 <- string)

func promedioIncorrecto() float64 {
    return "9.75"
}

// ---------- Error Semántico 7 ----------
// Retorno incorrecto (bool <- string)

func activoIncorrecto() bool {
    return "false"
}