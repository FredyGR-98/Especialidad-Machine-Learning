"""
Este script entrena un modelo de Machine Learning utilizando el dataset
de cáncer de mama (Breast Cancer) incluido en `scikit-learn`.

¿Por qué es importante?
-----------------------
Este modelo es la base de todo el sistema MLOps: permite predecir si un caso
es maligno o benigno a partir de características clínicas. Sin este modelo
entrenado, la API y el despliegue posterior en Docker no tendrían ninguna
funcionalidad práctica.

Justificación de la elección del modelo
---------------------------------------
Se utilizó un **RandomForestClassifier** porque:
- En experiencias previas ha mostrado mejor rendimiento frente a otros
  clasificadores clásicos en datasets con múltiples variables.
- No requiere estandarización de los datos, ya que los árboles de decisión
  internos pueden manejar distintas escalas de forma robusta.
- Ofrece un equilibrio entre precisión y robustez, reduciendo el riesgo
  de sobreajuste gracias al ensamble de múltiples árboles.
- Permite una fácil serialización con `joblib` para integrarlo en la API.

Pasos principales del script:
1. Cargar el dataset de breast cancer desde scikit-learn.
2. Dividir los datos en entrenamiento y prueba.
3. Entrenar un modelo (RandomForestClassifier en este caso).
4. Evaluar el modelo con un conjunto de prueba y mostrar la precisión.
5. Guardar el modelo entrenado en un archivo (`model.joblib`) para su uso futuro.
"""
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# 1. Cargar dataset
data = load_breast_cancer()
X, y = data.data, data.target

# 2. Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Crear y entrenar modelo
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 4. Evaluar modelo
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# 5. Guardar modelo entrenado
joblib.dump(model, "model.joblib")
print("✅ Modelo guardado en 'model.joblib'")
print("✅ Entrenamiento completado")