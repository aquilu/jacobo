#!/usr/bin/env python
# coding: utf-8

# In[7]:


import streamlit as st
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
import difflib

@st.cache_resource
def load_models():
    modelos = {
        'Modelo Regresión Logística': joblib.load('modelo_BLAA.pkl')
    }
    return modelos

columnas_modelo = ['Categoria', 'Author', 'Publisher']

def corregir_nombres_columnas(df, columnas_objetivo):
    """Corrige nombres de columnas usando coincidencias aproximadas"""
    df_renombrado = df.copy()
    columnas_actuales = df.columns.tolist()
    mapeo = {}
    for col_obj in columnas_objetivo:
        match = difflib.get_close_matches(col_obj, columnas_actuales, n=1, cutoff=0.8)
        if match:
            mapeo[match[0]] = col_obj
    if mapeo:
        df_renombrado = df_renombrado.rename(columns=mapeo)
    return df_renombrado, list(mapeo.keys())

def preprocess_dataframe(df):
    """Preprocesa el DataFrame para el modelo"""
    df_processed = df.copy()
    # Implementar preprocesamiento real aquí (ejemplo: codificación de variables categóricas)
    return df_processed

def main():
    st.set_page_config(page_title="Modelo BLAA", layout="wide")
    st.title("Predicción de libros que sean solicitados")

    # Inicializar session_state para almacenar df_input
    if 'df_input' not in st.session_state:
        st.session_state.df_input = None

    st.info(f"Antes de subir el archivo, asegúrate de que las columnas estén nombradas como: {', '.join(columnas_modelo)}")

    # Cargar modelos
    modelos = load_models()
    
    # Selector de modelo
    st.header("Selección de Modelo")
    modelo_seleccionado = st.selectbox(
        "Selecciona el modelo",
        options=list(modelos.keys()),
        help="El modelo de Regresión Logística genera valores probabilísticos entre 0 y 1"
    )
    
    st.info(f"📊 Modelo seleccionado: **{modelo_seleccionado}**")
    modelo = modelos[modelo_seleccionado]
    
    # Opciones de entrada
    st.header("📊 Datos de Entrada")
    option = st.radio("Selecciona entrada:", ["Subir archivo", "Entrada manual"])
    
    if option == "Subir archivo":
       
      uploaded_file = st.file_uploader("Sube tu archivo CSV o Excel", type=['csv', 'xlsx'], key="file_uploader")

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                st.session_state.df_input = pd.read_csv(uploaded_file)
            else:
                st.session_state.df_input = pd.read_excel(uploaded_file)

            # ✅ Mapeo manual de columnas (normalización básica)
            mapeo_columnas = {
                'editorial': 'Publisher',
                'autor': 'Author',
                'AUTOR': 'Author',
                'autor(a)': 'Author',
                'autor/a': 'Author',
                'categoria': 'Categoria',
                'Area Tematica': 'Categoria',
                'ÁREA TEMÁTICA':'Categoria',
                'publicador': 'Publisher',
                'publisher': 'Publisher',
                'EDITORIAL':'Publisher'
            }

            # Limpiar espacios y aplicar renombramiento
            st.session_state.df_input.columns = [col.strip() for col in st.session_state.df_input.columns]
            st.session_state.df_input = st.session_state.df_input.rename(
                columns=lambda x: mapeo_columnas.get(x.lower(), x)
            )

            #  Corrección de nombres parecidos (difflib)
            df_input, corregidas = corregir_nombres_columnas(st.session_state.df_input, columnas_modelo)

            if corregidas:
                st.success(f"Se renombraron automáticamente estas columnas: {', '.join(corregidas)}")

            #  Verificar que al menos haya columnas válidas
            columnas_presentes = [col for col in columnas_modelo if col in df_input.columns]
            if not columnas_presentes:
                st.error("⚠️ El archivo no contiene ninguna de las columnas requeridas para el modelo.")
                st.session_state.df_input = None
            else:
                st.session_state.df_input = df_input  # Actualizar con correcciones

        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")

    elif option == "Entrada manual":
        num_filas = st.number_input("¿Cuántas filas deseas ingresar?", min_value=1, max_value=50, value=1, step=1, key="num_filas")
        data_manual = {'Categoria': [], 'Author': [], 'Publisher': []}
        
        # Usar un formulario para mantener la consistencia de los datos
        with st.form(key="manual_input_form"):
            for i in range(int(num_filas)):
                st.markdown(f"### Fila {i+1}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    categoria = st.text_input(f"Categoría {i+1}", key=f"cat_{i}")
                with col2:
                    author = st.text_input(f"Autor {i+1}", key=f"auth_{i}")
                with col3:
                    publisher = st.text_input(f"Editorial {i+1}", key=f"pub_{i}")
                data_manual['Categoria'].append(categoria)
                data_manual['Author'].append(author)
                data_manual['Publisher'].append(publisher)
            
            submit_button = st.form_submit_button("Crear DataFrame")
            
            if submit_button:
                # Validar que todas las entradas estén completas
                if all(len(data_manual[col]) == int(num_filas) and all(val.strip() for val in data_manual[col]) 
                       for col in data_manual):
                    st.session_state.df_input = pd.DataFrame(data_manual)
                    st.success("DataFrame creado correctamente")
                else:
                    st.warning("⚠️ Asegúrate de llenar todas las filas completamente.")

    # Procesamiento y predicción
    if st.session_state.df_input is not None:
        st.header("Datos a Evaluar")
        try:
            df_processed = preprocess_dataframe(st.session_state.df_input)
            st.dataframe(df_processed)
            
            if st.button("Realizar Predicción", type="primary", key="predict_button"):
                with st.spinner('Procesando...'):
                    probabilidades = modelo.predict_proba(df_processed)[:, 1]
                    probabilidades_formateadas = [round(prob, 5) for prob in probabilidades]
                    
                    result_df = df_processed.copy()
                    result_df['Probabilidad'] = probabilidades_formateadas
                    
                    st.header(f"🎯 Resultados - {modelo_seleccionado}")
                    st.dataframe(result_df)
                    
                    st.subheader("📈 Distribución de Probabilidades")
                    fig, ax = plt.subplots(figsize=(9, 6))
                    ax.hist(probabilidades, bins=20, alpha=0.8, color='teal', edgecolor='black')
                    ax.set_xlabel('Probabilidad')
                    ax.set_ylabel('Frecuencia')
                    ax.set_title(f'Distribución de Probabilidades - {modelo_seleccionado}')
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
                    
                    st.subheader("📊 Estadísticas del Modelo")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Probabilidad Promedio", f"{probabilidades.mean():.5f}")
                    with col2:
                        st.metric("Probabilidad Máxima", f"{probabilidades.max():.5f}")
                    with col3:
                        st.metric("Probabilidad Mínima", f"{probabilidades.min():.5f}")
                    
                    csv = result_df.to_csv(index=False)
                    st.download_button(
                        "📥 Descargar Resultados CSV",
                        csv,
                        f"predicciones_{modelo_seleccionado.lower().replace(' ', '_')}.csv",
                        key="download_button"
                    )
        except Exception as e:
            st.error(f"Error al procesar los datos: {str(e)}")
    else:
        st.info("Por favor, crea o sube un DataFrame válido para realizar la predicción.")

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




