from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

def entrenar_modelo_clasificacion(df, features, target):
    """Entrena un modelo RandomForestClassifier y retorna métricas."""
    X = df[features]
    y = df[target]
    # Eliminar filas con NaN en features o target
    datos = pd.concat([X, y], axis=1).dropna()
    X = datos[features]
    y = datos[target]
    if X.empty or y.empty:
        raise ValueError("Las columnas de características o objetivo están vacías.")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    reporte = classification_report(y_test, y_pred)
    return acc, reporte
