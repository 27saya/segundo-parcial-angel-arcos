# Calculadora basada en agentes

## 1. Visión general del sistema

La calculadora distribuida implementa el paradigma de agentes, donde cada operación aritmética es gestionada por un agente autónomo. Un agente coordinador recibe la expresión del usuario, la vuelve tokens y maneja la resolución delegando las operaciones a los agentes especializados. El resultado final se construye en base a las respuestas de cada agente.

---

## 2. Componentes y Agentes

**Agente entrada/salida** (`agent_io`)
- Función: interfaz con el usuario, parseo de la expresión y coordinación global.
- Algoritmo: De precedencia y manejo de paréntesis.

**Agentes de operación**
- Agente suma (`agent_sum`): calcula `a + b`.
- Agente resta (`agent_subtract`): calcula `a - b`.
- Agente multiplicación (`agent_multiply`): calcula `a * b`.
- Agente división (`agent_divide`): calcula `a / b` (incluye manejo de división por cero).
- Agente potencia (`agent_power`): calcula `a ^ b`.

---

## 3. Flujo de interacción

1. **Entrada del usuario**
   - El usuario ingresa una expresión (ejemplo: `169 + 49 * 100 / 11 + 124 / 7 ^ 3`).

2. **Analisis e individualización**
   - El agente entrada/salida reemplaza `**` por `^`, elimina espacios y aplica regex para generar tokens individuales:  
     `['169','+','49','*','100','/','11','+','124','/','7','^','3']`.

3. **Gestión de precedencia**
   - Se usa el algoritmo de organización por precedencia o *Shunting Yard*: números van a la cola de salida y operadores a la pila según precedencia.

4. **Delegación a agentes**
   - Al desapilar un operador, el coordinador extrae dos operandos y llama a `calculate(a,b)` del agente apropiado.
   - Ejemplo: para `49 * 100`, el Agente Multiplicación devuelve `4900.0`.

5. **Resultado final**
   - Tras procesar todos los operadores, el primer elemento de la cola es el resultado (p.ej. `614.816061489531`).
   - El agente entrada/salida presenta el resultado al usuario.

---

## 4. Mecanismo de comunicación

- **Mensajes en memoria**: cada agente dispone de `send_message` y `receive_message`, aunque aquí las llamadas a métodos simulan una comunicación sincronizada.
- **Coordinación**: el agente entrada/salida invoca directamente `calculate` en cada agente.

---

## 5. Ejemplos de operaciones

| Expresión                                      | Resultado           | Imagen de referencia |
|-----------------------------------------------|---------------------|----------------------|
| `169 + 49 * 100 / 11 + 124 / 7 ^ 3`            | 614.816061489531    | <img width="1085" height="543" alt="Screenshot 2025-10-16 232649" src="https://github.com/user-attachments/assets/31b176ec-84f2-4f07-a2e4-5cd3049c2a32" />                  |
| `(20 + 47) * 3 ^ 3 - 12`                      | 1797.0              | <img width="996" height="531" alt="Screenshot 2025-10-16 232156" src="https://github.com/user-attachments/assets/539b90c3-74a8-48d7-bc6b-b0d1fdb42348" />                  |
| `894512 - 84552 * 6`                          | 387200.0            | <img width="747" height="487" alt="Screenshot 2025-10-16 232021" src="https://github.com/user-attachments/assets/2e15947b-f255-44bd-8e01-fd1a3fcec99c" />                 |

---

## 6. Conclusiones

- **Modularidad**: cada operación está aislada en su propio agente.
- **Extensibilidad**: agregar nuevos operadores (raíz, módulo) es directo.
- **Robustez**: manejo de errores (división por cero).
- **Claridad**: la interacción de agentes refleja el flujo matemático.

