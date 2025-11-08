"""Funciones de backend para Machine Learning.

Contiene utilidades para cargar CSV, mostrar las primeras columnas y entrenar
varios algoritmos de clasificación retornando métricas.
"""
from typing import List, Dict, Tuple
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
import numpy as np


SUPPORTED_MODELS = {
    "RandomForest": RandomForestClassifier,
    "LogisticRegression": LogisticRegression,
    "SVM": SVC,
    "DecisionTree": DecisionTreeClassifier,
    "NaiveBayes": GaussianNB,
    "GradientBoosting": GradientBoostingClassifier,
    "KNN": KNeighborsClassifier,
    "XGBoost": XGBClassifier,
}


def load_csv(file_like) -> pd.DataFrame:
    """Carga un archivo CSV desde un file-like (por ejemplo Streamlit uploader).

    Devuelve un DataFrame.
    """
    return pd.read_csv(file_like)


def primeras_columnas(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Devuelve un DataFrame con las primeras n columnas (y hasta 5 filas para vista rápida)."""
    cols = df.columns[:n]
    return df.loc[:, cols]


def entrenar_modelo(df: pd.DataFrame, features: List[str], target: str, modelo: str = "RandomForest", encoding: str = "onehot") -> Dict:
    """Entrena un único modelo y devuelve diccionario con métricas y datos para visualización.

    - Elimina filas con NaN en las columnas seleccionadas antes del split.
    - modelo es una de las claves de SUPPORTED_MODELS.
    
    Returns:
        Dict con accuracy, reporte, matriz de confusión, curva ROC (si aplica),
        y muestras de predicciones vs valores reales.
    """
    if modelo not in SUPPORTED_MODELS:
        raise ValueError(f"Modelo no soportado: {modelo}")

    X = df[features]
    y = df[target]
    datos = pd.concat([X, y], axis=1).dropna()
    X = datos[features]
    y = datos[target]

    # Preprocesamiento: convertir columnas categóricas (strings) en numéricas
    # según la opción 'encoding'. Opciones aceptadas:
    # - "onehot": aplica pd.get_dummies(drop_first=True)
    # - "label": convierte columnas object a category.cat.codes
    # - "none": no realiza codificación (se intentará entrenar tal cual)
    enc = (encoding or "onehot").lower()
    if enc == "onehot":
        try:
            X = pd.get_dummies(X, drop_first=True)
        except Exception:
            # Fallback a label encoding por si get_dummies falla
            X = X.copy()
            for col in X.columns:
                if X[col].dtype == object:
                    X[col] = X[col].astype('category').cat.codes
    elif enc == "label":
        X = X.copy()
        for col in X.columns:
            if X[col].dtype == object:
                X[col] = X[col].astype('category').cat.codes
    elif enc == "none":
        # No codificamos; esto puede provocar errores si hay columnas object.
        pass
    else:
        raise ValueError(f"Opción de encoding desconocida: {encoding}")

    if X.empty or y.empty:
        raise ValueError("Las columnas de características o la columna objetivo están vacías después de limpiar NaNs.")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Instanciar el modelo con parámetros por defecto adecuados
    ModelClass = SUPPORTED_MODELS[modelo]
    if modelo == "LogisticRegression":
        clf = ModelClass(max_iter=1000)
    else:
        clf = ModelClass()

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    reporte = classification_report(y_test, y_pred, zero_division=0)
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    # Datos para visualización
    resultados = {
        "accuracy": acc,
        "report": reporte,
        "confusion_matrix": conf_matrix,
        "y_test": y_test.values[:20],  # primeros 20 valores reales
        "y_pred": y_pred[:20],         # primeras 20 predicciones
    }
    
    # Curva ROC si el modelo soporta predict_proba y es clasificación binaria
    if hasattr(clf, "predict_proba") and len(np.unique(y)) == 2:
        try:
            y_prob = clf.predict_proba(X_test)[:, 1]
            fpr, tpr, _ = roc_curve(y_test, y_prob)
            roc_auc = auc(fpr, tpr)
            resultados.update({
                "roc": {
                    "fpr": fpr,
                    "tpr": tpr,
                    "auc": roc_auc
                }
            })
        except Exception:
            pass  # si falla predict_proba, simplemente no incluimos ROC
    
    return resultados


def entrenar_varios(df: pd.DataFrame, features: List[str], target: str, modelos: List[str], encoding: str = "onehot") -> Dict[str, Dict]:
    """Entrena varios modelos y devuelve un diccionario con métricas por modelo.

    Resultado ejemplo:
    {
      'RandomForest': {'accuracy': 0.95, 'report': '...'},
      ...
    }
    """
    resultados = {}
    for m in modelos:
        try:
            acc, rep = entrenar_modelo(df, features, target, modelo=m, encoding=encoding)
            resultados[m] = {"accuracy": acc, "report": rep}
        except Exception as e:
            resultados[m] = {"error": str(e)}
    return resultados
