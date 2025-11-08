import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
from backend import machine_learning as ml_backend


def render():
    st.title("Machine Learning — Módulo")
    st.write("Sube un CSV, preprocesa los datos y entrena algoritmos de clasificación.")

    uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=["csv"] )

    if uploaded_file is None:
        st.info("Sube un archivo CSV para comenzar.")
        return

    try:
        df = ml_backend.load_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error al leer CSV: {e}")
        return

    # Sección de preprocesamiento de datos
    st.subheader("🔧 Preprocesamiento de Datos")
    
    # Mostrar información del dataset
    st.write("📊 Información del dataset:")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Filas", df.shape[0])
    with col2:
        st.metric("Columnas", df.shape[1])

    # Expandir para ver detalles del dataset
    with st.expander("📋 Ver detalles del dataset"):
        # Información de tipos de datos
        st.write("Tipos de datos por columna:")
        dtypes_df = pd.DataFrame({
            'Tipo': df.dtypes,
            'Valores Nulos': df.isnull().sum(),
            'Valores Únicos': [df[col].nunique() for col in df.columns]
        })
        st.dataframe(dtypes_df)

    # Opciones de preprocesamiento
    st.write("🛠️ Opciones de preprocesamiento:")
    
    # Manejo de valores nulos
    null_handling = st.radio(
        "Manejo de valores nulos:",
        ["Mantener valores nulos", "Eliminar filas con valores nulos", "Rellenar valores nulos"],
        help="Elige cómo manejar las filas que contienen valores nulos"
    )

    if null_handling == "Rellenar valores nulos":
        fill_method = st.selectbox(
            "Método de relleno:",
            ["Media", "Mediana", "Moda", "Valor constante"],
            help="Elige el método para rellenar los valores nulos"
        )
        if fill_method == "Valor constante":
            fill_value = st.number_input("Valor de relleno:", value=0)
            df = df.fillna(fill_value)
        elif fill_method == "Media":
            df = df.fillna(df.mean(numeric_only=True))
        elif fill_method == "Mediana":
            df = df.fillna(df.median(numeric_only=True))
        elif fill_method == "Moda":
            df = df.fillna(df.mode().iloc[0])
    elif null_handling == "Eliminar filas con valores nulos":
        df = df.dropna()
        st.info(f"Filas restantes después de eliminar valores nulos: {len(df)}")

    # Normalización de datos numéricos
    if st.checkbox("Normalizar columnas numéricas", help="Escala los valores numéricos entre 0 y 1"):
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            for col in numeric_cols:
                if df[col].max() != df[col].min():
                    df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
            st.success("✅ Columnas numéricas normalizadas")
        else:
            st.warning("⚠️ No se encontraron columnas numéricas para normalizar")

    # Mostrar primeras filas del dataset procesado
    st.write("Vista previa del dataset procesado:")
    st.dataframe(df.head())

    # Obtener lista de columnas y detectar numéricas
    columnas = df.columns.tolist()
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    # Selección de variables
    st.subheader("📊 Selección de variables")
    
    # Control para mantener índice seleccionado del target
    target_index_key = "ml_target_index"
    if target_index_key not in st.session_state:
        st.session_state[target_index_key] = 0

    # Botones de ayuda para selección
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🎯 Seleccionar target numérico", key="select_numeric_target"):
            if len(numeric_cols) > 0:
                try:
                    st.session_state[target_index_key] = columnas.index(numeric_cols[0])
                except ValueError:
                    st.session_state[target_index_key] = 0
            else:
                st.warning("No hay columnas numéricas en el CSV.")
    with col2:
        if st.button("📊 Seleccionar features numéricas", key="select_numeric_feats"):
            if len(numeric_cols) > 0:
                for c in numeric_cols:
                    st.session_state[f"feat_{c}"] = True
            else:
                st.warning("No hay columnas numéricas para seleccionar como features.")

        # Target como radio (selección única) — usa el índice guardado en session_state
        # Aseguramos que el índice sea válido
        idx = st.session_state.get(target_index_key, 0)
        if idx < 0 or idx >= len(columnas):
            idx = 0
            st.session_state[target_index_key] = 0
        target_col = st.radio("Selecciona la columna objetivo (target):", columnas, index=idx)
        # guardar el índice actual para futuras reruns
        st.session_state[target_index_key] = columnas.index(target_col)

        # Features como checkboxes (botones) con opción de seleccionar todas
        st.write("Selecciona columnas de entrada (features):")
        default_features = [c for c in columnas if c != target_col][:5]

        feature_cols = []
        for c in columnas:
            if c == target_col:
                # asegurar que la columna target no esté marcada como feature
                st.session_state.setdefault(f"feat_{c}", False)
                continue
            key = f"feat_{c}"
            # Inicializar valor en session_state si no existe
            if key not in st.session_state:
                st.session_state[key] = (c in default_features)
            # st.checkbox sincroniza su valor con session_state cuando se usa 'key'
            checked = st.checkbox(c, value=st.session_state[key], key=key)
            if checked:
                feature_cols.append(c)

    modelos_humanos = {
        "🌲 Random Forest": "RandomForest",
        "📈 Regresión Logística": "LogisticRegression",
        "🎯 SVM": "SVM",
        "🌳 Árbol de Decisión": "DecisionTree",
        "📊 Naive Bayes": "NaiveBayes",
        "🚀 Gradient Boosting": "GradientBoosting",
        "👥 K-Nearest Neighbors": "KNN",
        "⚡ XGBoost": "XGBoost",
    }

    # Selector de tipo de codificación para columnas categóricas
    st.subheader("Preprocesamiento")
    encoding_option = st.selectbox(
        "Tipo de codificación para columnas categóricas:",
        ["One-hot (pd.get_dummies)", "Label encoding (cat.codes)", "Ninguno"],
        index=0,
    )
    encoding_map = {
        "One-hot (pd.get_dummies)": "onehot",
        "Label encoding (cat.codes)": "label",
        "Ninguno": "none",
    }
    encoding_param = encoding_map.get(encoding_option, "onehot")

    st.subheader("Algoritmos")
    modelo_seleccionado = st.selectbox(
        "Elige el algoritmo a entrenar:",
        list(modelos_humanos.keys()),
        format_func=lambda x: f"{x} 🤖"
    )

    if st.button("Entrenar modelo"):
        if not feature_cols or not target_col:
            st.warning("Selecciona la columna objetivo y al menos una característica.")
        else:
            modelo_id = modelos_humanos[modelo_seleccionado]
            with st.spinner(f"Entrenando {modelo_seleccionado}..."):
                resultados = ml_backend.entrenar_modelo(df, feature_cols, target_col, modelo=modelo_id, encoding=encoding_param)

            st.success("✨ Entrenamiento finalizado")
            
            # Mostrar métricas principales
            st.markdown(f"### 🤖 Resultado: {modelo_seleccionado}")
            if "error" in resultados:
                st.error(resultados["error"])
                return

            # Dividir la pantalla en 2 columnas para métricas clave
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🎯 Accuracy", f"{resultados['accuracy']:.4f}")
            
            # Reporte detallado en un expander
            with st.expander("📋 Ver reporte detallado"):
                st.text(resultados["report"])
            
            # Matriz de confusión usando plotly con mejor estilo
            
            st.subheader("📊 Matriz de Confusión")
            conf_matrix = resultados["confusion_matrix"]
            fig = ff.create_annotated_heatmap(
                z=conf_matrix,
                x=['Pred ' + str(i) for i in range(conf_matrix.shape[1])],
                y=['Real ' + str(i) for i in range(conf_matrix.shape[0])],
                colorscale='Viridis',
                showscale=True
            )
            # Mejorar el layout de la matriz
            fig.update_layout(
                title='Matriz de Confusión',
                xaxis_title='Predicción',
                yaxis_title='Valor Real',
                width=600,
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Curva ROC si está disponible
            if "roc" in resultados:
                st.subheader("📈 Curva ROC")
                roc_data = resultados["roc"]
                fig = px.line(
                    x=roc_data["fpr"], y=roc_data["tpr"],
                    title=f'Curva ROC (AUC = {roc_data["auc"]:.4f})',
                    labels={
                        "x": "Tasa de Falsos Positivos",
                        "y": "Tasa de Verdaderos Positivos"
                    }
                )
                # Mejorar el estilo de la curva ROC
                fig.update_layout(
                    xaxis_range=[0,1],
                    yaxis_range=[0,1],
                    width=600,
                    height=500,
                    showlegend=False
                )
                # Agregar línea diagonal de referencia con mejor estilo
                fig.add_shape(
                    type='line',
                    line=dict(dash='dash', color='gray', width=1),
                    x0=0, x1=1, y0=0, y1=1
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Tabla de comparación valores reales vs predichos con mejor formato
            st.subheader("🔍 Muestra de Predicciones")
            df_pred = pd.DataFrame({
                'Valor Real': resultados['y_test'],
                'Predicción': resultados['y_pred']
            })
            
            # Agregar columna de acierto/error
            df_pred['Resultado'] = np.where(
                df_pred['Valor Real'] == df_pred['Predicción'],
                '✅ Correcto',
                '❌ Incorrecto'
            )
            
            # Mostrar DataFrame con estilo
            def highlight_predictions(val):
                if val == '✅ Correcto':
                    return 'background-color: #e6ffe6'
                elif val == '❌ Incorrecto':
                    return 'background-color: #ffe6e6'
                return ''
            
            st.dataframe(
                df_pred.style.applymap(highlight_predictions, subset=['Resultado']),
                use_container_width=True
            )

    st.markdown("---")
    st.info("💡 Consejo: asegúrate de que las columnas seleccionadas tengan el tipo adecuado (numérico/categórico según el modelo).")
