

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Supongamos que tienes la matriz de confusión ya calculada
# matriz_confusion = ...
matriz_confusion=[[ 3177,    87],[   86, 16650]]
# Define las etiquetas de las clases
etiquetas_clases = ['Estado operativo', 'Falla']  # Reemplaza con tus etiquetas reales

# Crea el heatmap de la matriz de confusión
plt.figure(figsize=(8, 6))
sns.set(font_scale=1.2)  # Escala de la fuente para facilitar la lectura
sns.heatmap(matriz_confusion, annot=True, fmt='d', cmap='YlGnBu', cbar=False,
            xticklabels=etiquetas_clases, yticklabels=etiquetas_clases)
plt.xlabel('Caso')
plt.ylabel('Predicción')
plt.title('Matriz de Confusión')
plt.show()