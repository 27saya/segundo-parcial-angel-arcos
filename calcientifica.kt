import java.util.Locale.getDefault
import kotlin.math.*

    open class Calculadora {

        open fun sumar(a: Int, b: Int): Int {
            return a + b
        }

        open fun sumar(a: Double, b: Double): Double {
            return a + b
        }

        open fun restar(a: Int, b: Int): Int {
            return a - b
        }

        open fun restar(a: Double, b: Double): Double {
            return a - b
        }

        open fun multiplicar(a: Int, b: Int): Int {
            return a * b
        }

        open fun multiplicar(a: Double, b: Double): Double {
            return a * b
        }

        open fun dividir(a: Int, b: Int): Double {
            if (b == 0) {
                throw ArithmeticException("Error: División por cero no permitida")
            }
            return a.toDouble() / b.toDouble()
        }

        open fun dividir(a: Double, b: Double): Double {
            if (b == 0.0) {
                throw ArithmeticException("Error: División por cero no permitida")
            }
            return a / b
        }

        protected fun validarNumero(valor: String): Double {
            return try {
                valor.toDouble()
            } catch (e: NumberFormatException) {
                throw IllegalArgumentException("Error: '$valor' no es un número válido")
            }
        }
    }

    class CalculadoraCientifica : Calculadora() {
        // Encapsulamiento (memoria)
        private var memoria: Double = 0.0

        fun seno(grados: Double): Double {
            val radianes = gradosARadianes(grados)
            return sin(radianes)
        }

        fun coseno(grados: Double): Double {
            val radianes = gradosARadianes(grados)
            return cos(radianes)
        }

        fun tangente(grados: Double): Double {
            val radianes = gradosARadianes(grados)
            if (cos(radianes) == 0.0) {
                throw ArithmeticException("Error: Tangente indefinida (cos = 0)")
            }
            return tan(radianes)
        }

        fun gradosARadianes(grados: Double): Double {
            return grados * PI / 180.0
        }

        fun radianesAGrados(radianes: Double): Double {
            return radianes * 180.0 / PI
        }

        fun potencia(base: Double, exponente: Double): Double {
            return base.pow(exponente)
        }

        fun raizCuadrada(numero: Double): Double {
            if (numero < 0) {
                throw ArithmeticException(" Error: No se puede calcular raíz cuadrada de número negativo")
            }
            return sqrt(numero)
        }

        fun raizN(numero: Double, n: Double): Double {
            if (numero < 0 && n % 2 == 0.0) {
                throw ArithmeticException("Error: Raíz par de número negativo no es real")
            }
            return numero.pow(1.0 / n)
        }

        fun log10(numero: Double): Double {
            if (numero <= 0) {
                throw ArithmeticException("Error: Logaritmo de número no positivo")
            }
            return log10(numero)
        }

        fun ln(numero: Double): Double {
            if (numero <= 0) {
                throw ArithmeticException("Error: Logaritmo natural de número no positivo")
            }
            return ln(numero)
        }

        fun logaritmo(numero: Double, base: Double): Double {
            if (numero <= 0 || base <= 0 || base == 1.0) {
                throw ArithmeticException("Error: Parámetros inválidos para logaritmo")
            }
            return ln(numero) / ln(base)
        }

        fun exponencial(x: Double): Double {
            return exp(x)
        }

        fun potenciaDe10(x: Double): Double {
            return 10.0.pow(x)
        }

        fun memorySumar(valor: Double) {
            memoria += valor
            println("Memoria actualizada: M = $memoria")
        }

        fun memoryRestar(valor: Double) {
            memoria -= valor
            println("Memoria actualizada: M = $memoria")
        }

        fun memoryRecuperar(): Double {
            println("Memoria recuperada: M = $memoria")
            return memoria
        }

        fun memoryLimpiar() {
            memoria = 0.0
            println("Memoria limpiada: M = 0.0")
        }


        fun evaluarExpresion(expresion: String): Double {
            println("\n🔍 Evaluando: $expresion")

            try {
                var expr = expresion.replace(" ", "").lowercase(getDefault())

                expr = procesarFunciones(expr)

                val resultado = evaluarAritmetica(expr)

                println("Resultado: $resultado")
                return resultado

            } catch (e: Exception) {
                throw IllegalArgumentException("Error al evaluar expresión: ${e.message}")
            }
        }

        private fun procesarFunciones(expresion: String): String {
            var expr = expresion

            expr = procesarFuncion(expr, "sin") { seno(it) }
            expr = procesarFuncion(expr, "cos") { coseno(it) }
            expr = procesarFuncion(expr, "tan") { tangente(it) }

            expr = procesarFuncion(expr, "log") { log10(it) }
            expr = procesarFuncion(expr, "ln") { ln(it) }

            expr = procesarFuncion(expr, "sqrt") { raizCuadrada(it) }

            return expr
        }

        private fun procesarFuncion(expresion: String, funcion: String, calculo: (Double) -> Double): String {
            var expr = expresion
            val regex = Regex("$funcion\\(([^)]+)\\)")

            while (regex.containsMatchIn(expr)) {
                val match = regex.find(expr)!!
                val argumento = match.groupValues[1].toDouble()
                val resultado = calculo(argumento)
                expr = expr.replace(match.value, resultado.toString())
            }

            return expr
        }

        private fun evaluarAritmetica(expresion: String): Double {
            // Implementación simplificada usando evaluación directa
            // Para producción, se recomienda un parser más robusto
            return try {
                // Usar el motor de scripts de Kotlin (simplificado)
                evaluarConPrecedencia(expresion)
            } catch (e: Exception) {
                throw IllegalArgumentException("Error en evaluación aritmética: ${e.message}")
            }
        }

        private fun evaluarConPrecedencia(expresion: String): Double {
            // Implementación básica - para expresiones más complejas usar un parser real
            val tokens = tokenizar(expresion)
            return evaluarTokens(tokens)
        }


        private fun tokenizar(expresion: String): List<String> {
            val tokens = mutableListOf<String>()
            var numero = ""

            for (char in expresion) {
                when {
                    char.isDigit() || char == '.' -> numero += char
                    char in listOf('+', '-', '*', '/', '^', '(', ')') -> {
                        if (numero.isNotEmpty()) {
                            tokens.add(numero)
                            numero = ""
                        }
                        tokens.add(char.toString())
                    }
                }
            }

            if (numero.isNotEmpty()) {
                tokens.add(numero)
            }

            return tokens
        }

        private fun evaluarTokens(tokens: List<String>): Double {
            var resultado = 0.0
            var operador = "+"

            for (token in tokens) {
                when {
                    token.toDoubleOrNull() != null -> {
                        val numero = token.toDouble()
                        resultado = when (operador) {
                            "+" -> resultado + numero
                            "-" -> resultado - numero
                            "*" -> resultado * numero
                            "/" -> resultado / numero
                            else -> numero
                        }
                    }
                    token in listOf("+", "-", "*", "/") -> operador = token
                }
            }

            return resultado
        }
    }

    class CalculadoraUI {
        private val calc = CalculadoraCientifica()

        fun iniciar() {
            println("Calculadora cientifica basada en POO")
            mostrarMenu()

            while (true) {
                print("\nSelecciona una opción: ")
                val opcion = readLine()?.trim() ?: ""

                when (opcion) {
                    "1" -> operacionesBasicas()
                    "2" -> operacionesTrigonometricas()
                    "3" -> operacionesPotencias()
                    "4" -> operacionesLogaritmos()
                    "5" -> operacionesMemoria()
                    "6" -> evaluarExpresionCompleta()
                    "7" -> mostrarMenu()
                    "8" -> {
                        println("\nAdeu, hasta nunca")
                        break
                    }
                    else -> println("Opción inválida. Intenta de nuevo.")
                }
            }
        }

        private fun mostrarMenu() {
            println("\n┌─────────────────────────────────────────────────────────┐")
            println("│  Menu principal                                         │")
            println("├─────────────────────────────────────────────────────────┤")
            println("│  1. Operaciones básicas (+, -, ×, ÷)                   │")
            println("│  2. Funciones trigonométricas (sin, cos, tan)          │")
            println("│  3. Potencias y raíces (x^y, √x)                       │")
            println("│  4. Logaritmos (log, ln)                               │")
            println("│  5. Memoria (M+, M-, MR, MC)                           │")
            println("│  6. Evaluar expresión completa                         │")
            println("│  7. Mostrar menú                                       │")
            println("│  8. Salir                                              │")
            println("└─────────────────────────────────────────────────────────┘")
        }

        private fun operacionesBasicas() {
            println("\nOperaciones basicas")
            println("1. Suma  2. Resta  3. Multiplicación  4. División")
            print("Opción: ")
            val op = readLine()?.trim() ?: ""

            try {
                print("Primer número: ")
                val a = readLine()?.toDouble() ?: 0.0
                print("Segundo número: ")
                val b = readLine()?.toDouble() ?: 0.0

                val resultado = when (op) {
                    "1" -> calc.sumar(a, b)
                    "2" -> calc.restar(a, b)
                    "3" -> calc.multiplicar(a, b)
                    "4" -> calc.dividir(a, b)
                    else -> {
                        println("Opción inválida")
                        return
                    }
                }

                println("Resultado: $resultado")
            } catch (e: Exception) {
                println("Error: ${e.message}")
            }
        }

        private fun operacionesTrigonometricas() {
            println("\nFunciones trigonometricas")
            println("1. Seno  2. Coseno  3. Tangente")
            print("Opción: ")
            val op = readLine()?.trim() ?: ""

            try {
                print("Ángulo en grados: ")
                val angulo = readLine()?.toDouble() ?: 0.0

                val resultado = when (op) {
                    "1" -> calc.seno(angulo)
                    "2" -> calc.coseno(angulo)
                    "3" -> calc.tangente(angulo)
                    else -> {
                        println("Opción inválida")
                        return
                    }
                }

                println("Resultado: $resultado")
            } catch (e: Exception) {
                println("Error: ${e.message}")
            }
        }

        private fun operacionesPotencias() {
            println("\nPotencias y raices")
            println("1. Potencia (x^y)  2. Raíz Cuadrada  3. Raíz n-ésima")
            print("Opción: ")
            val op = readLine()?.trim() ?: ""

            try {
                when (op) {
                    "1" -> {
                        print("Base: ")
                        val base = readLine()?.toDouble() ?: 0.0
                        print("Exponente: ")
                        val exp = readLine()?.toDouble() ?: 0.0
                        println("Resultado: ${calc.potencia(base, exp)}")
                    }
                    "2" -> {
                        print("Número: ")
                        val num = readLine()?.toDouble() ?: 0.0
                        println("Resultado: ${calc.raizCuadrada(num)}")
                    }
                    "3" -> {
                        print("Número: ")
                        val num = readLine()?.toDouble() ?: 0.0
                        print("Índice de la raíz: ")
                        val n = readLine()?.toDouble() ?: 0.0
                        println("Resultado: ${calc.raizN(num, n)}")
                    }
                    else -> println("Opción inválida")
                }
            } catch (e: Exception) {
                println("Error: ${e.message}")
            }
        }

        private fun operacionesLogaritmos() {
            println("\nLogaritmos")
            println("1. log₁₀  2. ln (log natural)  3. Logaritmo base personalizada")
            print("Opción: ")
            val op = readLine()?.trim() ?: ""

            try {
                print("Número: ")
                val num = readLine()?.toDouble() ?: 0.0

                val resultado = when (op) {
                    "1" -> calc.log10(num)
                    "2" -> calc.ln(num)
                    "3" -> {
                        print("Base: ")
                        val base = readLine()?.toDouble() ?: 0.0
                        calc.logaritmo(num, base)
                    }
                    else -> {
                        println("Opción inválida")
                        return
                    }
                }

                println("Resultado: $resultado")
            } catch (e: Exception) {
                println("Error: ${e.message}")
            }
        }

        private fun operacionesMemoria() {
            println("\nFunciones de memoria")
            println("1. M+ (Sumar a memoria)  2. M- (Restar de memoria)")
            println("3. MR (Recuperar)        4. MC (Limpiar)")
            print("Opción: ")
            val op = readLine()?.trim() ?: ""

            try {
                when (op) {
                    "1" -> {
                        print("Valor a sumar: ")
                        val valor = readLine()?.toDouble() ?: 0.0
                        calc.memorySumar(valor)
                    }
                    "2" -> {
                        print("Valor a restar: ")
                        val valor = readLine()?.toDouble() ?: 0.0
                        calc.memoryRestar(valor)
                    }
                    "3" -> {
                        val valor = calc.memoryRecuperar()
                        println("✅ Valor en memoria: $valor")
                    }
                    "4" -> calc.memoryLimpiar()
                    else -> println("Opción inválida")
                }
            } catch (e: Exception) {
                println("Error: ${e.message}")
            }
        }

        private fun evaluarExpresionCompleta() {
            println("\nEvaluar expresiones completas")
            println("Ejemplos: 2 + 3 * 4, sin(45) + cos(30), log(100) - 5")
            print("Expresión: ")
            val expresion = readLine()?.trim() ?: ""

            try {
                val resultado = calc.evaluarExpresion(expresion)
                println("Resultado final: $resultado")
            } catch (e: Exception) {
                println("Error: ${e.message}")
            }
        }
    }

    fun main() {
        val ui = CalculadoraUI()
        ui.iniciar()
    }
