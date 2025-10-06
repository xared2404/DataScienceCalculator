import streamlit as st
import pandas as pd
from backend.machine_learning import entrenar_modelo_clasificacion


def render():
    st.title("Módulo de Machine Learning")
    st.write("Sube un archivo CSV para aplicar un modelo de clasificación básico.")

    uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Vista previa de los datos:")
        st.dataframe(df.head())

        columnas = df.columns.tolist()
        target_col = st.selectbox("Selecciona la columna objetivo (variable a predecir):", columnas)
        feature_cols = st.multiselect("Selecciona las columnas de entrada (features):", [col for col in columnas if col != target_col], default=[col for col in columnas if col != target_col])

        # Selector de algoritmo de machine learning
        algoritmo = st.selectbox(
            "Selecciona el algoritmo de Machine Learning:",
            ["RandomForest", "LogisticRegression", "SVM", "DecisionTree", "NaiveBayes", "SVD", "KMeans"]
        )

        if st.button("Entrenar modelo de clasificación"):  # Botón para ejecutar ML
            if not feature_cols or not target_col:
                st.warning("Debes seleccionar al menos una columna de entrada y una columna objetivo.")
            else:
                if algoritmo == "SVD":
                    st.info("SVD es un método de reducción de dimensionalidad, no de clasificación directa. Implementa aquí la lógica si deseas usar SVD.")
                elif algoritmo == "KMeans":
                    from sklearn.cluster import KMeans
                    X = df[feature_cols].dropna()
                    st.write("Entrenando modelo KMeans (clustering)...")
                    n_clusters = st.number_input("Número de clusters (K):", min_value=2, max_value=10, value=3)
                    kmeans = KMeans(n_clusters=int(n_clusters), random_state=42)
                    labels = kmeans.fit_predict(X)
                    st.success("Modelo KMeans entrenado.")
                    st.write("Etiquetas de cluster para las primeras filas:")
                    st.write(labels[:10])
                else:
                    st.write(f"Entrenando modelo {algoritmo}...")
                    acc, reporte = entrenar_modelo_clasificacion(df, feature_cols, target_col, modelo=algoritmo)
                    st.success(f"Precisión del modelo: {acc:.2f}")
                    st.text("Reporte de clasificación:")
                    st.text(reporte)
