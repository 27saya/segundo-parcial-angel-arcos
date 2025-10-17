# Simulacion de perceptron con paradigma de agentes - Angel Arcos

## 1. Introducción

### 1.1 El Perceptrón
El perceptrón es uno de los modelos más fundamentales en el aprendizaje automático y las redes neuronales, ya que, representa un clasificador lineal binario que puede separar datos linealmente separables segun ciertas características.

#### Funcionamiento matemático:
- **Función de activación**: f(x) = sign(w₁x₁ + w₂x₂ + b)
- **Regla de actualización**: wᵢ(t+1) = wᵢ(t) + α·error·xᵢ
- **Error**: error = etiquetaReal - predicción
- **Parámetros**:
  - w₁, w₂: Pesos
  - b: Bias (sesgo)
  - α: Tasa de aprendizaje

## 2. Arquitectura de la implementación

### 2.1 Diseño de Agentes

La implementación consta de tres tipos principales de agentes:

#### **DataPointAgent** - Agente punto de datos
```python
Atributos:
- Posición (x, y)
- Etiqueta real (1 o -1)
- Predicción actual
- Estado de clasificación (correcto/incorrecto)

Comportamientos:
- Consultar al perceptrón para obtener predicción
- Actualizar su color según clasificación
- Reportar su estado al modelo
```

#### **PerceptronAgent** - Agente perceptrón
```python
Atributos:
- Pesos (w1, w2)
- Bias
- Tasa de aprendizaje
- Estado de entrenamiento

Comportamientos:
- Hacer predicciones para puntos dados
- Aprender mediante regla de actualización
- Generar línea de decisión
- Reportar convergencia
```

#### **PerceptronModel** - Agente coordinador
```python
Responsabilidades:
- Coordinar interacciones entre agentes
- Controlar ciclo de entrenamiento
- Generar datos linealmente separables
- Evaluar rendimiento global
```

### 2.2 Interacciones entre agentes

1. **Inicialización**: El modelo genera puntos de datos como agentes independientes
2. **Consulta**: Cada punto consulta al perceptrón para obtener su predicción
3. **Aprendizaje**: El perceptrón actualiza sus pesos basado en todos los puntos
4. **Actualización**: Los puntos actualizan su estado de clasificación
5. **Evaluación**: El modelo evalúa el progreso global

---

## 3. Implementación

### 3.1 Generación de datos linealmente separables
```python
# Línea de separación real: y = 0.5x + 1
true_w1 = 0.5
true_w2 = -1  
true_bias = 1

# Clasificación basada en:
activation = true_w1 * x + true_w2 * y + true_bias
label = 1 if activation >= 0 else -1
```

### 3.2 Algoritmo de entrenamiento
```python
for cada_punto in data_points:
    predicción = perceptron.predict(punto.x, punto.y)
    error = punto.etiqueta_real - predicción
    
    if error != 0:
        w1 += α * error * punto.x
        w2 += α * error * punto.y
        bias += α * error
```

### 3.3 Interfaz grafica interactiva
- **Sliders**: Control de tasa de aprendizaje (0.01-1.0) y iteraciones máximas (10-500)
- **Botones**: Iniciar entrenamiento y restablecer simulación
- **Visualización**: Tiempo real con colores dinámicos y línea de decisión
- **Información**: Iteración actual, precisión, pesos y estado

---

## 4. ANÁLISIS DE RESULTADOS EXPERIMENTALES

### 4.1 Experimento 1: Tasa de aprendizaje baja (≈0.1)
**Observaciones de la Imagen 1:**
- **Iteraciones completadas**: 24/100
- **Precisión final**: 100.0%
- **Pesos finales**: w1=0.301, w2=-0.664
- **Bias final**: 0.551
- **Estado**: Completado (convergencia temprana)
  <img width="1919" height="1029" alt="Screenshot 2025-10-16 212703" src="https://github.com/user-attachments/assets/f2fe5acf-e23b-4918-aa57-188611a1bba5" />

**Análisis:**
- Capacidad de alcance de equilibrio rápida y estable
- Separación lineal perfecta lograda
- Todos los puntos correctamente clasificados (verde)
- Línea de decisión bien posicionada

### 4.2 Experimento 2: Tasa de aprendizaje alta (≈0.8-1.0)
**Observaciones de la Imagen 2:**
- **Iteraciones completadas**: 8/100
- **Precisión final**: 100.0%
- **Pesos finales**: w1=1.228, w2=-2.468
- **Bias final**: 2.373
- **Estado**: Completado
  <img width="1919" height="1008" alt="Screenshot 2025-10-16 212754" src="https://github.com/user-attachments/assets/8e19c75d-19e9-41d3-9437-3147a9ef0f7f" />

**Análisis:**
- Capacidad de alcance de equilibrio muy rápida (solo 8 iteraciones)
- Precisión perfecta alcanzada
- Mayor magnitud en los pesos debido a tasa de aprendizaje más alta
- Separación efectiva de las clases
  

### 4.3 Experimento 3: Tasa de aprendizaje media (≈0.3-0.4)
**Observaciones de la Imagen 3:**
- **Iteraciones completadas**: 14/100
- **Precisión final**: 100.0%
- **Pesos finales**: w1=0.491, w2=-1.282
- **Bias final**: 1.323
- **Estado**: Completado
  <img width="1919" height="1006" alt="Screenshot 2025-10-16 212723" src="https://github.com/user-attachments/assets/def46c86-5b03-4b90-931f-1eda5e655065" />

**Análisis:**
- Capacidad de alcance de equilibrio intermedia (14 iteraciones)
- Precisión perfecta mantenida
- Pesos con valores moderados
- Comportamiento estable a pesar de tasa alta
  >

### 4.4 Comparación de resultados

| Tasa de aprendizaje | Iteraciones | Precisión | Magnitud de pesos | Alcance de equilibrio |
|---------------------|-------------|-----------|-------------------|--------------|
| Baja (~0.1)         | 24          | 100.0%    | Moderada          | Estable      |
| Alta (~0.8-1.0)    | 8           | 100.0%    | Alta              | Muy rápida   |
| Media (~0.3-0.4)     | 14          | 100.0%    | Moderada          | Rápida       |

### 4.5 Observaciones

1. **Efectividad del algoritmo**: Todos los experimentos alcanzaron 100% de precisión
2. **Robustez**: El perceptrón converge independientemente de la tasa de aprendizaje
3. **Velocidad de convergencia**: Las tasas medias mostraron convergencia más rápida
4. **Estabilidad**: No se observó oscilación en ningún caso

---

## 5. Validación del paradigma de agentes

### 5.1 Comportamientos emergentes observados
- **Autoorganización**: Los puntos se auto-clasifican según la línea aprendida
- **Cooperación**: Los agentes trabajan juntos para el objetivo común
- **Adaptabilidad**: El sistema responde dinámicamente a cambios de parámetros

### 5.2 Ventajas del enfoque de agentes
- **Modularidad**: Cada componente tiene responsabilidades bien definidas
- **Escalabilidad**: Fácil agregar nuevos tipos de agentes o comportamientos
- **Visualización**: Representación natural del proceso de aprendizaje
- **Debugging**: Fácil seguimiento del estado de cada componente


## 6. Conclusiones

### 6.1 Lo observado
1. **Implementación exitosa** del perceptrón usando paradigma de agentes
2. **Interfaz gráfica completa** con controles interactivos
3. **Visualización efectiva** del proceso de aprendizaje
4. **Convergencia rapida** en todos los escenarios probados

### 6.2 Sobre el paradigma de agentes
- El enfoque de agentes proporciona una representación natural del aprendizaje distribuido
- La modularidad facilita el mantenimiento y extensión del código
- Las interacciones locales entre agentes producen un comportamiento coherente en general

### 6.3 Rendimiento del perceptrón
- **Efectividad**: 100% de precisión en clasificación
- **Eficiencia**: Convergencia rápida (8-24 iteraciones)
- **Robustez**: Funcionamiento estable con diferentes parámetros
- **Adaptabilidad**: Respuesta adecuada a cambios de configuración
