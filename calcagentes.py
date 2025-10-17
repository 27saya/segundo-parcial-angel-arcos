import re
from typing import List, Tuple, Union
import time

class Agent:
    def __init__(self, agent_id: str, name: str):
        self.id = agent_id
        self.name = name
        self.messages = []
        
    def receive_message(self, message: dict):
        self.messages.append(message)
        
    def send_message(self, recipient, message_type: str, data: dict):
        message = {
            'from': self.id,
            'type': message_type,
            'data': data
        }
        recipient.receive_message(message)
        
    def process_messages(self):
        pass

class SumAgent(Agent):
    def __init__(self):
        super().__init__("agent_sum", "Agente suma")
        
    def calculate(self, a: float, b: float) -> float:
        result = a + b
        print(f"  [{self.name}] Calculando: {a} + {b} = {result}")
        return result


class SubtractAgent(Agent):
    def __init__(self):
        super().__init__("agent_subtract", "Agente resta")
        
    def calculate(self, a: float, b: float) -> float:
        result = a - b
        print(f"  [{self.name}] Calculando: {a} - {b} = {result}")
        return result


class MultiplyAgent(Agent):
    def __init__(self):
        super().__init__("agent_multiply", "Agente multiplicación")
        
    def calculate(self, a: float, b: float) -> float:
        result = a * b
        print(f"  [{self.name}] Calculando: {a} × {b} = {result}")
        return result


class DivideAgent(Agent):
    def __init__(self):
        super().__init__("agent_divide", "Agente división")
        
    def calculate(self, a: float, b: float) -> float:
        if b == 0:
            print(f"  [{self.name}] ERROR: División por cero")
            raise ValueError("División por cero no permitida")
        result = a / b
        print(f"  [{self.name}] Calculando: {a} ÷ {b} = {result}")
        return result


class PowerAgent(Agent):
    def __init__(self):
        super().__init__("agent_power", "Agente potencia")
        
    def calculate(self, a: float, b: float) -> float:
        result = a ** b
        print(f"  [{self.name}] Calculando: {a} ^ {b} = {result}")
        return result

class IOAgent(Agent):
    """
    Agente de entrada/salida que coordina todas las operaciones.
    
    Este agente es el cerebro del sistema. Recibe expresiones del usuario,
    las vuelve tokens, coordina a los agentes de operación respetando
    la precedencia de operadores, y devuelve el resultado final.
    
    Implementa el algoritmo de precedencia para manejar correctamente
    los operadores y paréntesis.
    """
    
    def __init__(self):
        super().__init__("agent_io", "Agente entrada/salida")
        
        # Iniciar agentes de operaciones
        self.sum_agent = SumAgent()
        self.subtract_agent = SubtractAgent()
        self.multiply_agent = MultiplyAgent()
        self.divide_agent = DivideAgent()
        self.power_agent = PowerAgent()
        
        # Mapeo de operadores a agentes
        self.operator_agents = {
            '+': self.sum_agent,
            '-': self.subtract_agent,
            '*': self.multiply_agent,
            '/': self.divide_agent,
            '^': self.power_agent,
            '**': self.power_agent
        }
        
    def parse_expression(self, expression: str) -> List[str]:
        """
        Convierte una expresión como "2 + 3 * 4" en individuales
        ['2', '+', '3', '*', '4'], manejando números enteros, decimales,
        operadores y paréntesis.
        """
        # Reemplazar ** por ^
        expression = expression.replace('**', '^')

        # Patrón (forma regex (sacado por ia xd)) para números (enteros y decimales) y operadores
        pattern = r'(\d+\.?\d*|[+\-*/()^])'
        tokens = re.findall(pattern, expression.replace(' ', ''))
        
        return tokens
    
    def apply_operator(self, operator: str, a: float, b: float) -> float:
        agent = self.operator_agents.get(operator)
        if agent:
            return agent.calculate(a, b)
        else:
            raise ValueError(f"Operador desconocido: {operator}")
    
    def get_precedence(self, operator: str) -> int:
        """
        Devuelve la precedencia de un operador.
        
        Precedencia estándar matemática:
        - Nivel 1: Suma y Resta
        - Nivel 2: Multiplicación y División
        - Nivel 3: Potencia
        """
        precedences = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '^': 3,
            '**': 3
        }
        return precedences.get(operator, 0)
    
    def evaluate_expression(self, expression: str) -> float:
        print(f"\n[{self.name}] Procesando expresión: {expression}")
        
        tokens = self.parse_expression(expression)
        print(f"[{self.name}] Tokens identificados: {tokens}")
        
        # Algoritmo de evaluación con precedencia
        output_queue = []
        operator_stack = [] 
        for token in tokens:
            if self.is_number(token):
                output_queue.append(float(token))
                
            elif token in self.operator_agents:
                while (operator_stack and 
                       operator_stack[-1] != '(' and
                       operator_stack[-1] in self.operator_agents and
                       self.get_precedence(operator_stack[-1]) >= self.get_precedence(token)):
                    self.process_operator(output_queue, operator_stack)
                
                operator_stack.append(token)
                
            elif token == '(':
                operator_stack.append(token)
                
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    self.process_operator(output_queue, operator_stack)
                if operator_stack:
                    operator_stack.pop()  # Eliminar '('
        
        while operator_stack:
            self.process_operator(output_queue, operator_stack)
        
        # El resultado final esta en la cola de salida
        result = output_queue[0] if output_queue else 0
        print(f"[{self.name}] Resultado final: {result}")
        
        return result
    
    def process_operator(self, output_queue: List[float], operator_stack: List[str]):
        """
        Procesa un operador de la pila.
        
        Toma dos operandos de la cola, aplica el operador usando
        el agente correspondiente, y coloca el resultado de vuelta
        en la cola.
        """
        operator = operator_stack.pop()
        if len(output_queue) >= 2:
            b = output_queue.pop()
            a = output_queue.pop()
            result = self.apply_operator(operator, a, b)
            output_queue.append(result)
    
    def is_number(self, token: str) -> bool:
        try:
            float(token)
            return True
        except ValueError:
            return False
    
    def receive_user_input(self, expression: str) -> float:
        try:
            result = self.evaluate_expression(expression)
            return result
        except Exception as e:
            print(f"[{self.name}] Error: {str(e)}")
            raise

class AgentCalculator:
    def __init__(self):
        self.io_agent = IOAgent()
        self.history = []
        
    def calculate(self, expression: str) -> float:
        print("\n" + "="*60)
        result = self.io_agent.receive_user_input(expression)
        self.history.append({
            'expression': expression,
            'result': result
        })
        print("="*60)
        return result
    
    def show_history(self):
        print("\n Historial de Cálculos:")
        print("-" * 40)
        for i, item in enumerate(self.history, 1):
            print(f"{i}. {item['expression']} = {item['result']}")
        print("-" * 40)
    
    def interactive_mode(self):
        print("\n" + "="*60)
        print("Calculadora basada en agentes")
        print("="*60)
        print("\nOpciones disponibles:")
        print("  - Ingresa una expresión matemática para calcular")
        print("  - Escribe historial para verlo")
        print("  - Escribe salir para terminar")
        print("\nOperadores soportados: +, -, *, /, ^ (potencia), ()")
        print("Ejemplos: '2 + 3 * 4', '(5 + 3) * 2', '10 / 2 + 3 ^ 2'")
        print("="*60)
        
        while True:
            try:
                user_input = input("\n Ingresa expresión: ").strip()
                
                if user_input.lower() in ['salir', 'exit', 'quit']:
                    print("\nAdeu, no vuelvas! >:(")
                    break
                    
                elif user_input.lower() in ['historial', 'history', 'h']:
                    self.show_history()
                    
                elif user_input:
                    result = self.calculate(user_input)
                    print(f"\nResultado: {result}")
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
                print("Por favor, verifica tu expresión e intenta de nuevo.")


def run_calculator():
    """Función principal para ejecutar la calculadora"""
    calc = AgentCalculator()
    
if __name__ == "__main__":
    calc = AgentCalculator()
    calc.interactive_mode()

