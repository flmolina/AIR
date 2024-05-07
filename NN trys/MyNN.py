import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix

# Definimos una función para generar datos de entrenamiento con umbrales específicos para cada entrada
def generar_datos(cantidad):
    # Definimos los umbrales para cada entrada
    umbrales = [5.9, 7, 4]
    # Generamos valores aleatorios para las tres entradas
    entradas = np.random.rand(cantidad, 3)*10
    # Calculamos la salida deseada
    salidas = np.array([1 if np.any(entrada > umbrales) else 0 for entrada in entradas])
    return entradas, salidas

# Generamos datos de entrenamiento
x, y = generar_datos(1000)

# Dividimos los datos en conjuntos de entrenamiento y prueba
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Creamos el clasificador de red neuronal
clf = MLPClassifier(hidden_layer_sizes=(5,), activation='relu', solver='lbfgs', max_iter=1000, random_state=42)

# Entrenamos el clasificador
clf.fit(x_train, y_train)

# Evaluamos el clasificador
accuracy = clf.score(x_test, y_test)
print("Accuracy del clasificador:", accuracy)

# Calculamos y mostramos la matriz de confusión
predicciones = clf.predict(x_test)
matriz_confusion = confusion_matrix(y_test, predicciones)
print("Matriz de Confusión:")
print(matriz_confusion)

# Guardamos el modelo entrenado en un archivo
from joblib import dump
dump(clf, 'NN.joblib')
