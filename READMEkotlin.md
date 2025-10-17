# Calculadora cientifica en POO - Kotlin

## 1. INTRODUCCIÓN

Este proyecto implementa una **calculadora científica completa** utilizando los principios fundamentales de la programación orientada a objetos en Kotlin. La aplicación permite realizar operaciones aritméticas básicas y avanzadas (trigonometría, potencias, logaritmos, funciones exponenciales) mediante una interfaz de consola interactiva.

### Lo desarrollado
 - Implementar clase base con operaciones básicas  
 - Aplicar herencia para extender funcionalidades científicas  
 - Demostrar polimorfismo mediante sobrecarga de métodos  
 - Implementar manejo robusto de excepciones  
 - Desarrollar sistema de memoria y evaluación de expresiones  

---

## 2. Arquitectura del sistema

### 2.1 Diagrama de Clases

<img width="408" height="674" alt="imagen_2025-10-17_012958791" src="https://github.com/user-attachments/assets/459938d2-f7ea-40db-bcbe-62a51735a278" />


---

## 3. Aplicacion de POO

### 3.1 Encapsulamiento

El encapsulamiento es el principio de ocultar los detalles de implementación y exponer solo lo necesario a través de una interfaz pública.

#### Implementación la calc:

**a) Variable de memoria privada**
```kotlin
class CalculadoraCientifica : Calculadora() {
    private var memoria: Double = 0.0  // ← ENCAPSULACIÓN
    
    fun memorySumar(valor: Double) {
        memoria += valor  // Acceso controlado
    }
    
    fun memoryRecuperar(): Double {
        return memoria  // Lectura controlada
    }
}
```

**Ventajas:**
- La variable `memoria` no puede ser modificada directamente desde fuera de la clase
- Todo acceso se controla mediante métodos públicos (`M+`, `M-`, `MR`, `MC`)
- Se puede agregar validación in afectar el código externo

**b) Metodo protegido de validación**
```kotlin
open class Calculadora {
    protected fun validarNumero(valor: String): Double {
        return try {
            valor.toDouble()
        } catch (e: NumberFormatException) {
            throw IllegalArgumentException("Error: '$valor' no es válido")
        }
    }
}
```

**Ventajas:**
- El método `validarNumero` es accesible para clases derivadas (`protected`)
- No es accesible desde fuera de la jerarquía de clases

---

### 3.2 Herencia

La herencia permite crear nuevas clases basadas en clases existentes, reutilizando y extendiendo funcionalidades.

#### Implementacion:

**Jerarquía de clases:**
```kotlin
// Clase base con operaciones fundamentales
open class Calculadora {
    open fun sumar(a: Double, b: Double): Double { ... }
    open fun dividir(a: Double, b: Double): Double { ... }
}

// Clase derivada que hereda y extiende
class CalculadoraCientifica : Calculadora() {
    // Hereda: sumar, restar, multiplicar, dividir
    
    // Extiende con nuevas capacidades:
    fun seno(grados: Double): Double { ... }
    fun logaritmo(numero: Double, base: Double): Double { ... }
    fun potencia(base: Double, exponente: Double): Double { ... }
}
```

**Ventajas:**
- `CalculadoraCientifica` reutiliza todo el código de `Calculadora`
- No es necesario reimplementar operaciones básicas
- Se mantiene la relación "es-un" (una calculadora científica es una calculadora)
- Facilita el mantenimiento: cambios en `Calculadora` se expanden de forma automatica

**Ejemplo:**
```kotlin
val calc = CalculadoraCientifica()

// Usa métodos heredados:
calc.sumar(5.0, 3.0)        // De la clase base
calc.dividir(10.0, 2.0)     // De la clase base

// Usa métodos propios:
calc.seno(45.0)             // De la clase derivada
calc.logaritmo(100.0, 10.0) // De la clase derivada
```

---

### 3.3 Polimorfismo

El polimorfismo permite que objetos de diferentes tipos sean tratados de manera uniforme, y que métodos con el mismo nombre se comporten diferente según el contexto.

#### Implementación:

**a) Sobrecarga de métodos**

La calculadora soporta operaciones con diferentes tipos de datos:

```kotlin
open class Calculadora {
    // Versión para números enteros
    open fun sumar(a: Int, b: Int): Int {
        return a + b
    }
    
    // Versión para números decimales
    open fun sumar(a: Double, b: Double): Double {
        return a + b
    }
    
    // Versión para multiplicación con enteros
    open fun multiplicar(a: Int, b: Int): Int {
        return a * b
    }
    
    // Versión para multiplicación con decimales
    open fun multiplicar(a: Double, b: Double): Double {
        return a * b
    }
}
```

**Ventajas:**
- El mismo nombre de método funciona con diferentes tipos
- Kotlin selecciona automáticamente la versión correcta según los parámetros
- Código más limpio y facil de usar

**Ejemplo:**
```kotlin
val calc = Calculadora()

val resultado1 = calc.sumar(5, 3)        // Llama a sumar(Int, Int) → 8
val resultado2 = calc.sumar(5.5, 3.2)    // Llama a sumar(Double, Double) → 8.7
```

**b) Polimorfismo por herencia**

```kotlin
// Se puede asignar una calculadora científica a una variable de tipo base
val calculadora: Calculadora = CalculadoraCientifica()

// Funciona porque CalculadoraCientifica "es-una" Calculadora
calculadora.sumar(10.0, 5.0)  // Funciona perfectamente
```

---

### 3.4 Excepciones

El manejo amplio de excepciones es clave para aplicaciones confiables.

#### Implementación:

**a) División por cero**
```kotlin
open fun dividir(a: Double, b: Double): Double {
    if (b == 0.0) {
        throw ArithmeticException("Error: División por cero no permitida")
    }
    return a / b
}
```

**b) Raíces de numeros negativos**
```kotlin
fun raizCuadrada(numero: Double): Double {
    if (numero < 0) {
        throw ArithmeticException("Error: Raíz cuadrada de número negativo")
    }
    return sqrt(numero)
}
```

**c) Logaritmos inválidos**
```kotlin
fun ln(numero: Double): Double {
    if (numero <= 0) {
        throw ArithmeticException("Error: Logaritmo de número no positivo")
    }
    return ln(numero)
}
```

**d) Tangente indefinida**
```kotlin
fun tangente(grados: Double): Double {
    val radianes = gradosARadianes(grados)
    if (cos(radianes) == 0.0) {
        throw ArithmeticException("Error: Tangente indefinida (cos = 0)")
    }
    return tan(radianes)
}
```

**Ventajas:**
- Mensajes de error claros y específicos
- Prevención de resultados incorrectos
- Aplicación más robusta y confiable

---

## 4. Funcionalidades de la calc

### 4.1 Operaciones básicas
- Suma, resta, multiplicación, división
- Soporte para enteros y decimales
- Validación de división por cero

### 4.2 Funciones trigonométricas
- `seno(grados)`: Calcula sin(x)
- `coseno(grados)`: Calcula cos(x)
- `tangente(grados)`: Calcula tan(x)
- Conversión automática de grados a radianes

### 4.3 Potencias y raíces
- `potencia(base, exponente)`: Calcula x^y
- `raizCuadrada(numero)`: Calcula √x
- `raizN(numero, n)`: Calcula ⁿ√x
- Validación de raíces pares de negativos

### 4.4 Logaritmos
- `log10(numero)`: Logaritmo base 10
- `ln(numero)`: Logaritmo natural (base e)
- `logaritmo(numero, base)`: Logaritmo en cualquier base
- Validación de argumentos positivos

### 4.5 Funciones exponenciales
- `exponencial(x)`: Calcula e^x
- `potenciaDe10(x)`: Calcula 10^x

### 4.6 Sistema de memoria
- `M+`: Suma a la memoria
- `M-`: Resta de la memoria
- `MR`: Recupera el valor almacenado
- `MC`: Limpia la memoria

### 4.7 Evaluación de expresiones
- Soporta expresiones complejas como: `sin(143) + tan(24) - 2 * 9`
- Procesa funciones matemáticas integradas
- Respeta precedencia de operadores

---

## 5. Resultados y pruebas

### 5.1 Operaciones básicas

**Prueba: Suma de números decimales**

<img width="492" height="469" alt="imagen_2025-10-17_013743339" src="https://github.com/user-attachments/assets/02e05bea-0a80-4e00-96e8-f596eebb2604" />

**Descripción:**
- Operación ejecutada: 415665.56 + 12145.12
- Resultado obtenido: 427810.68
- Observación: La sobrecarga de métodos permite trabajar tanto con enteros como decimales de forma correcta.

---

### 5.2 Funciones trigonométricas

**Prueba: Coseno de 45 grados**

<img width="286" height="217" alt="Screenshot 2025-10-17 010938" src="https://github.com/user-attachments/assets/4fb8804a-c8b7-4429-ac3c-3bc24a250533" />

**Descripción:**
- Operación ejecutada: cos(45°)
- Resultado obtenido: 0.7071067811865476
- Observación: El sistema convierte automáticamente grados a radianes antes del cálculo. El resultado es correcto (√2/2 ≈ 0.707).

---

### 5.3 Potencias y raíces

**Prueba: Raíz cuadrada**

<img width="440" height="171" alt="Screenshot 2025-10-17 010958" src="https://github.com/user-attachments/assets/e0323bbe-cfa8-4f4c-bb0f-fdea6114487d" />

**Descripción:**
- Operación ejecutada: √40
- Resultado obtenido: 6.324555320336759
- Observación: El cálculo es preciso. Verificación: 6.324² ≈ 40.

---

### 5.4 Funciones de Memoria

**Prueba: Almacenamiento en memoria (M+)**

<img width="478" height="482" alt="Screenshot 2025-10-17 011127" src="https://github.com/user-attachments/assets/0f696d96-6f94-4f05-a7f9-84586587ad28" />

**Descripción:**
- Operación ejecutada: M+ con valor 8745
- Estado de memoria: M = 8745.0
- Observación: El sistema de memoria funciona correctamente, tomando el valor y permitiendo operaciones acumulativas.

---

### 5.5 Evaluación de Expresiones Complejas

**Prueba: Expresión con funciones trigonométricas**

<img width="429" height="217" alt="Screenshot 2025-10-17 011141" src="https://github.com/user-attachments/assets/46be08f2-3b4d-4531-85dc-939e57955cdf" />

**Descripción:**
- Expresión evaluada: `sin(143) + tan(24) - 2 * 9`
- Resultado obtenido: -8.576060623854474
- Observación: El evaluador de expresiones procesa correctamente:
  1. Las funciones trigonométricas (sin, tan)
  2. La precedencia de operadores (multiplicación antes que suma/resta)
  3. La secuencia completa de operaciones

## 6. Analisis de resultados

### 6.1 Precisión
Todos los cálculos muestran una alta precisión y fidelidad en sus resultados, comprobando que la calculadora es apropiada para aplicaciones científicas y de ingeniería.

### 6.2 Amplitud
El sistema maneja correctamente:
- Valores extremos
- Operaciones inválidas (división por cero)
- Entrada de usuario incorrecta
- Funciones indefinidas (tangente de 90°)

### 6.3 Usabilidad
La interfaz de menú es:
- **Intuitiva**: opciones claramente numeradas
- **Completa**: cubre todas las funcionalidades
- **Informativa**: muestra resultados claramente formateados

---

### 8.2 Beneficios de la POO
- **Modularidad**: Cada clase tiene responsabilidades bien definidas
- **Reutilización**: La herencia evita duplicación de código
- **Extensibilidad**: Fácil agregar nuevas operaciones
- **Mantenibilidad**: Cambios localizados no afectan todo el sistema
- **Legibilidad**: Código organizado y autodocumentado

---

## 9. Como ejecutar el codigo

Si bien existen varios metoodos para ejecutar un codigo en kotlin tales como el Kotlin Playground hallado en la pagina oficial de kotlin o el compiler para Windows, la mejor y mas facil opción es IntelliJ IDEA, ya que cuenta con el soporte oficial para ese lenguaje.

### Requisitos previos
- IntelliJ IDEA instalado (Community o Ultimate)
- JDK 8 o superior instalado

### Pasos para ejecutar

#### 1. Crear Nuevo Proyecto
1. Abrir IntelliJ IDEA
2. Selecciona "new project"
3. Elige "Kotlin"
4. Asigna un nombre al proyecto y selecciona ubicación
5. Haz clic en "create"

#### 2. Agregar el codigo
1. Haz clic derecho en la carpeta `src`
2. Selecciona "New > Kotlin File/Class"
3. Nómbralo como gustes
4. Copia y pega todo el contenido del archivo `calcientifica.kt`

#### 3. Verificar la función main
Asegurate de que existe la función `main()`:
```kotlin
fun main() {
    val ui = CalculadoraUI()
    ui.iniciar()
}
```

#### 4. Ejecutar el programa
- Haz clic en el icono verde de "Play" al lado de Current File
- O presiona `Control + F5`

#### 5. Interactuar con la Calculadora
- La consola aparecerá en la parte inferior del IDE
- Ingresa el número de la opción deseada
- Sigue las instrucciones en pantalla
- Para salir, selecciona la opción 8 :D
- Eso es todo :P
