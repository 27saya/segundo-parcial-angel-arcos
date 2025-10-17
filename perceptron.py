import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation
import time
import csv

# CLASE 1: AGENTE PUNTO DE DATOS
class DataPointAgent:
    """
    Agente que representa un punto de datos para entrenar el perceptrón.
    
    Cada agente mantiene su posición (x, y), su etiqueta verdadera,
    y puede verificar si está siendo clasificado correctamente.
    """
    
    def __init__(self, agent_id, x, y, label):
        self.id = agent_id
        self.x = x
        self.y = y
        self.label = label  # 1 o -1
        self.predicted_label = 0
        self.correctly_classified = False
        
    def actualizarClasificacion(self, perceptron):
        """Actualiza si el punto está correctamente clasificado"""
        self.predicted_label = perceptron.predict(self.x, self.y)
        self.correctly_classified = (self.predicted_label == self.label)
        
    def getColor(self):
        """Devuelve el color del punto según su clasificación"""
        if self.correctly_classified:
            return 'green' if self.label == 1 else 'lightgreen'
        else:
            return 'red' if self.label == 1 else 'darkred'
        

# CLASE 2: AGENTE PERCEPTRÓN
class PerceptronAgent:
    """
    Agente que representa el perceptrón con capacidad de aprendizaje.
    
    Implementa el algoritmo clásico del perceptrón:
    - Función de activación: signo(w·x + b)
    - Regla de actualización: w_new = w_old + α·error·x
    """
    
    def __init__(self, learning_rate=0.1):
        # Inicializar pesos y bias aleatoriamente
        self.w1 = random.uniform(-1, 1)
        self.w2 = random.uniform(-1, 1)
        self.bias = random.uniform(-1, 1)
        self.learning_rate = learning_rate
        self.training_complete = False
        self.iteration = 0
        
    def predict(self, x, y):
        """Hace una predicción para un punto (x, y)"""
        activation = self.w1 * x + self.w2 * y + self.bias
        return 1 if activation >= 0 else -1
    
    def train_step(self, data_points):
        """Entrena el perceptrón con todos los puntos de datos en una iteración"""
        updated = False
        
        for point in data_points:
            prediction = self.predict(point.x, point.y)
            error = point.label - prediction
            
            if error != 0:  # Solo actualizar si hay error
                self.w1 += self.learning_rate * error * point.x
                self.w2 += self.learning_rate * error * point.y
                self.bias += self.learning_rate * error
                updated = True
        
        self.iteration += 1
        return updated
    
    def lineaDecision(self, x_range=(-10, 10)):
        """Calcula los puntos de la línea de decisión para visualización"""
        if abs(self.w2) > 1e-10:
            # Línea: w1*x + w2*y + bias = 0
            # y = (-w1*x - bias) / w2
            x_vals = np.linspace(x_range[0], x_range[1], 100)
            y_vals = (-self.w1 * x_vals - self.bias) / self.w2
            return x_vals, y_vals
        else:
            # Línea vertical
            x_val = -self.bias / self.w1 if abs(self.w1) > 1e-10 else 0
            return [x_val, x_val], [x_range[0], x_range[1]]
    
    def reset(self, learning_rate):
        """Reinicia el perceptrón"""
        self.w1 = random.uniform(-1, 1)
        self.w2 = random.uniform(-1, 1)
        self.bias = random.uniform(-1, 1)
        self.learning_rate = learning_rate
        self.training_complete = False
        self.iteration = 0

# CLASE 3: MODELO PRINCIPAL
class PerceptronModel:
    """
    Modelo que contiene el perceptrón y los puntos de datos.
    
    Coordina la interacción entre todos los agentes y maneja
    el ciclo de entrenamiento y evaluación.
    """
    
    def __init__(self, learning_rate=0.1, max_iterations=100, num_points=30):
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.num_points = num_points
        self.current_iteration = 0
        self.training_complete = False
        
        # Crear el perceptrón
        self.perceptron = PerceptronAgent(learning_rate)
        
        # Generar puntos de datos
        self.data_points = []
        self.generarPuntos()
        
    def generarPuntos(self):
        """Genera puntos de datos linealmente separables"""
        self.data_points = []
        
        # Definir una línea de separación real (y = 0.5*x + 1)
        true_w1 = 0.5
        true_w2 = -1
        true_bias = 1
        
        for i in range(self.num_points):
            # Generar punto aleatorio
            x = random.uniform(-8, 8)
            y = random.uniform(-8, 8)
            
            # Determinar etiqueta basada en la línea de separación real
            activation = true_w1 * x + true_w2 * y + true_bias
            label = 1 if activation >= 0 else -1
            
            # Crear agente punto de datos
            point = DataPointAgent(i, x, y, label)
            self.data_points.append(point)
    
    def step(self):
        """Ejecuta un paso de la simulación"""
        if not self.training_complete and self.current_iteration < self.max_iterations:
            # Entrenar perceptrón
            updated = self.perceptron.train_step(self.data_points)
            
            # Actualizar clasificación de puntos
            for point in self.data_points:
                point.actualizarClasificacion(self.perceptron)
            
            self.current_iteration += 1
            
            # Verificar si el entrenamiento está completo
            if not updated or self.current_iteration >= self.max_iterations:
                self.training_complete = True
        
        return not self.training_complete

    def reiniciarSimulacion(self, learning_rate, max_iterations):
        """Reinicia la simulación"""
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.current_iteration = 0
        self.training_complete = False
        
        # Reinicializar perceptrón
        self.perceptron.reset(learning_rate)
        
        # Regenerar puntos de datos
        self.generarPuntos()

    def evaluarRendimiento(self):
        """Evalúa el rendimiento del perceptrón"""
        # Actualizar clasificaciones
        for point in self.data_points:
            point.actualizarClasificacion(self.perceptron)
        
        correct = sum(1 for point in self.data_points if point.correctly_classified)
        total = len(self.data_points)
        
        return (correct / total) * 100 if total > 0 else 0


# CLASE 4: VISUALIZACIÓN INTERACTIVA
class PerceptronVisualization:
    """
    Clase para manejar la visualización interactiva del perceptrón.
    
    Implementa la interfaz gráfica con sliders, botones y
    animación en tiempo real del proceso de aprendizaje.
    """
    
    def __init__(self):
        self.model = PerceptronModel()
        self.setInterfaz()
        self.is_training = False
        self.animation_obj = None
        
    def setInterfaz(self):
        """Configura la interfaz gráfica con sliders y botones"""
        import matplotlib.pyplot as plt
        plt.close('all')
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        plt.subplots_adjust(bottom=0.25, left=0.1)
        
        # Configurar el eje principal
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_xlabel('X1')
        self.ax.set_ylabel('X2')
        self.ax.set_title('Simulación del Perceptrón - Clasificación en Tiempo Real')
        self.ax.grid(True, alpha=0.3)
        
        # Crear sliders
        ax_learning_rate = plt.axes([0.2, 0.1, 0.3, 0.03])
        self.slider_lr = Slider(ax_learning_rate, 'Tasa de Aprendizaje', 
                               0.01, 1.0, valinit=0.1, valfmt='%.3f')
        
        ax_iterations = plt.axes([0.2, 0.05, 0.3, 0.03])
        self.slider_iter = Slider(ax_iterations, 'Max Iteraciones', 
                                 10, 500, valinit=100, valfmt='%d')
        
        # Crear botones
        ax_start = plt.axes([0.5, 0.1, 0.1, 0.04])
        self.button_start = Button(ax_start, 'Iniciar')
        self.button_start.on_clicked(self.empezarEntreno)
        
        ax_reset = plt.axes([0.7, 0.1, 0.1, 0.04])
        self.button_reset = Button(ax_reset, 'Restablecer')
        self.button_reset.on_clicked(self.reiniciarSimulacion)
        
    def actualizarPlot(self):
        """Actualiza la visualización con el estado actual"""
        self.ax.clear()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_xlabel('X1')
        self.ax.set_ylabel('X2')
        self.ax.set_title('Simulación del Perceptrón - Clasificación en Tiempo Real')
        self.ax.grid(True, alpha=0.3)
        
        # Dibujar puntos de datos
        for point in self.model.data_points:
            color = point.getColor()
            marker = 'o' if point.label == 1 else 's'
            self.ax.scatter(point.x, point.y, c=color, s=100, marker=marker, 
                          edgecolors='black', linewidth=1)
        
        # Dibujar línea de decisión
        try:
            x_vals, y_vals = self.model.perceptron.lineaDecision()
            # Filtrar valores que estén en el rango visible
            valid_indices = (np.array(y_vals) >= -10) & (np.array(y_vals) <= 10)
            if np.any(valid_indices):
                x_vals_filtered = np.array(x_vals)[valid_indices]
                y_vals_filtered = np.array(y_vals)[valid_indices]
                self.ax.plot(x_vals_filtered, y_vals_filtered, 'b-', linewidth=2, 
                           label='Línea de Decisión')
        except:
            pass
        
        # Actualizar información
        accuracy = self.model.evaluarRendimiento()
        info = f"""Iteración: {self.model.current_iteration}/{self.model.max_iterations}
Precisión: {accuracy:.1f}%
Pesos: w1={self.model.perceptron.w1:.3f}, w2={self.model.perceptron.w2:.3f}
Bias: {self.model.perceptron.bias:.3f}
Estado: {'Completado' if self.model.training_complete else 'Entrenando...'}"""
        
        self.ax.text(0.02, 0.98, info, transform=self.ax.transAxes, 
                    verticalalignment='top', fontsize=10,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Leyenda
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='green', 
                   markersize=10, label='Clase +1 (Correcto)'),
            Line2D([0], [0], marker='s', color='w', markerfacecolor='lightgreen', 
                   markersize=10, label='Clase -1 (Correcto)'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
                   markersize=10, label='Clase +1 (Incorrecto)'),
            Line2D([0], [0], marker='s', color='w', markerfacecolor='darkred', 
                   markersize=10, label='Clase -1 (Incorrecto)')
        ]
        self.ax.legend(handles=legend_elements, loc='upper right')
        
        plt.draw()
        
    def animacionEntreno(self, frame):
        """Función de animación para el entrenamiento en tiempo real"""
        if self.is_training and not self.model.training_complete:
            continue_training = self.model.step()
            if not continue_training:
                self.is_training = False
            self.actualizarPlot()
            return []
        else:
            self.is_training = False
            return []
    
    def empezarEntreno(self, event):
        """Inicia el entrenamiento del perceptrón"""
        if not self.is_training:
            # Actualizar parámetros del modelo
            learning_rate = self.slider_lr.val
            max_iterations = int(self.slider_iter.val)
            
            # Reiniciar modelo con nuevos parámetros
            self.model.reiniciarSimulacion(learning_rate, max_iterations)
            
            # Iniciar animación
            self.is_training = True
            if self.animation_obj:
                self.animation_obj.event_source.stop()
            
            self.animation_obj = animation.FuncAnimation(
                self.fig, self.animacionEntreno, interval=200, blit=False, repeat=True)
            
            plt.draw()

    def reiniciarSimulacion(self, event):
        """Reinicia la simulación"""
        # Detener animación si está corriendo
        if self.animation_obj:
            self.animation_obj.event_source.stop()
        
        self.is_training = False
        
        # Reiniciar modelo
        learning_rate = self.slider_lr.val
        max_iterations = int(self.slider_iter.val)
        self.model.reiniciarSimulacion(learning_rate, max_iterations)
        
        # Actualizar visualización
        self.actualizarPlot()
    
    def show(self):
        """Muestra la visualización"""
        plt.show()

def generate_test_data(num_test_points=20):
    """Genera datos de prueba para evaluar el perceptrón entrenado"""
    test_points = []
    
    # Usar la misma línea de separación que para los datos de entrenamiento
    true_w1 = 0.5
    true_w2 = -1
    true_bias = 1
    
    for i in range(num_test_points):
        # Generar punto aleatorio
        x = random.uniform(-8, 8)
        y = random.uniform(-8, 8)
        
        # Determinar etiqueta basada en la línea de separación real
        activation = true_w1 * x + true_w2 * y + true_bias
        label = 1 if activation >= 0 else -1
        
        test_points.append((x, y, label))
    
    return test_points

def evaluarPerceptron(perceptron, test_data):
    """Evalúa el perceptrón en datos de prueba"""
    correct = 0
    total = len(test_data)
    
    results = []
    for x, y, true_label in test_data:
        predicted_label = perceptron.predict(x, y)
        is_correct = (predicted_label == true_label)
        if is_correct:
            correct += 1
        results.append((x, y, true_label, predicted_label, is_correct))
    
    accuracy = (correct / total) * 100 if total > 0 else 0
    return accuracy, results

def runearPerceptron():
    """Función principal que ejecuta la demostración del perceptrón con la interfaz interactiva"""
    print("Simulación del Perceptrón usando el paradigma de agentes")
    print("="*60)
    print("Instrucciones:")
    print("1. Ajusta la tasa de aprendizaje (0.01 - 1.0)")
    print("2. Ajusta el número máximo de iteraciones (10 - 500)")
    print("3. Haz clic en 'Iniciar' para comenzar el entrenamiento")
    print("4. Haz clic en 'Restablecer' para generar nuevos datos")
    print()
   
    viz = PerceptronVisualization()
    viz.show()
    
    return viz

if __name__ == "__main__":
    viz = runearPerceptron()
