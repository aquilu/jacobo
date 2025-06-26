#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import joblib
import difflib
from PIL import Image
import plotly.express as px

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
    return df_processed

def main():
    st.set_page_config(
        page_title="Sistema de Predicción BLAA", 
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header con imagen y título mejorado
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            image = Image.open('img/banrep.jpeg')
            st.image(image, width=250, use_container_width=False)
        except:
            st.warning("⚠️ Imagen no encontrada: img/banrep.jpeg")
    
    # Espaciado adicional después de la imagen
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.title("📚 Sistema de Predicción de Libros Solicitados")
    st.markdown("---")
    
    # CSS personalizado mejorado
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
    }
    .prediction-section {
        background-color: #e8f5e8;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #28a745;
    }
    /* Estilo para mejorar la imagen del header */
    [data-testid="stImage"] > img {
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        border: 3px solid #ffffff;
        transition: transform 0.3s ease;
    }
    [data-testid="stImage"] > img:hover {
        transform: scale(1.02);
    }
    /* Mejoras adicionales para el título */
    .main > div:first-child h1 {
        text-align: center;
        color: #1f77b4;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Inicializar session_state para almacenar df_input
    if 'df_input' not in st.session_state:
        st.session_state.df_input = None

    # Información importante en un contenedor destacado
    with st.container():
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.info(f"📋 **Columnas requeridas:** {', '.join(columnas_modelo)}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Cargar modelos
    modelos = load_models()
    
    # Sidebar para configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        st.markdown("---")
        
        # Selector de modelo
        st.subheader("🤖 Modelo de Predicción")
        modelo_seleccionado = st.selectbox(
            "Selecciona el modelo",
            options=list(modelos.keys()),
            help="El modelo de Regresión Logística genera valores probabilísticos entre 0 y 1"
        )
        
        st.success(f"✅ **{modelo_seleccionado}**")
        modelo = modelos[modelo_seleccionado]
        
        st.markdown("---")
        st.subheader("📊 Información del Modelo")
        st.write("• **Tipo:** Regresión Logística")
        st.write("• **Salida:** Probabilidades (0-1)")
        st.write("• **Variables:** Categoría, Autor, Editorial")
    
    # Opciones de entrada con mejor diseño
    st.header("📊 Datos de Entrada")
    st.markdown("---")
    
    # Tabs para mejor organización
    tab1, tab2 = st.tabs(["📁 Subir Archivo", "✏️ Entrada Manual"])
    
    uploaded_file = None
    
    with tab1:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "📁 Arrastra y suelta tu archivo CSV o Excel aquí", 
            type=['csv', 'xlsx'], 
            key="file_uploader",
            help="Formatos soportados: CSV, Excel (.xlsx)"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                st.session_state.df_input = pd.read_csv(uploaded_file)
            else:
                st.session_state.df_input = pd.read_excel(uploaded_file)

            # Mapeo manual de columnas (normalización básica)
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

            # Corrección de nombres parecidos (difflib)
            df_input, corregidas = corregir_nombres_columnas(st.session_state.df_input, columnas_modelo)

            if corregidas:
                st.success(f"Se renombraron automáticamente estas columnas: {', '.join(corregidas)}")

            # Verificar que al menos haya columnas válidas
            columnas_presentes = [col for col in columnas_modelo if col in df_input.columns]
            if not columnas_presentes:
                st.error("⚠️ El archivo no contiene ninguna de las columnas requeridas para el modelo.")
                st.session_state.df_input = None
            else:
                st.session_state.df_input = df_input  # Actualizar con correcciones

        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")

    with tab2:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        num_filas = st.number_input(
            "¿Cuántas filas deseas ingresar?", 
            min_value=1, max_value=50, value=1, step=1, 
            key="num_filas",
            help="Máximo 50 filas por sesión"
        )
        data_manual = {'Categoria': [], 'Author': [], 'Publisher': []}
        
        # Usar un formulario para mantener la consistencia de los datos
        with st.form(key="manual_input_form"):
            for i in range(int(num_filas)):
                with st.expander(f"📖 Libro {i+1}", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        categoria = st.text_input(f"Categoría", key=f"cat_{i}", placeholder="Ej: Ficción")
                    with col2:
                        author = st.text_input(f"Autor", key=f"auth_{i}", placeholder="Ej: Gabriel García Márquez")
                    with col3:
                        publisher = st.text_input(f"Editorial", key=f"pub_{i}", placeholder="Ej: Planeta")
                    data_manual['Categoria'].append(categoria)
                    data_manual['Author'].append(author)
                    data_manual['Publisher'].append(publisher)
            
            submit_button = st.form_submit_button("🔄 Crear DataFrame", type="primary")
            
            if submit_button:
                # Validar que todas las entradas estén completas
                if all(len(data_manual[col]) == int(num_filas) and all(val.strip() for val in data_manual[col]) 
                       for col in data_manual):
                    st.session_state.df_input = pd.DataFrame(data_manual)
                    st.success("✅ DataFrame creado correctamente")
                else:
                    st.warning("⚠️ Asegúrate de llenar todas las filas completamente.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Procesamiento y predicción con mejor diseño
    if st.session_state.df_input is not None:
        st.markdown("---")
        st.header("📋 Datos a Evaluar")
        
        try:
            df_processed = preprocess_dataframe(st.session_state.df_input)
            
            # Mostrar datos en un contenedor estilizado
            with st.container():
                st.subheader(f"📊 Vista previa ({len(df_processed)} registros)")
                st.dataframe(df_processed, use_container_width=True)
            
            # Botón de predicción centrado y destacado
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                predict_button = st.button(
                    "🚀 Realizar Predicción", 
                    type="primary", 
                    key="predict_button",
                    use_container_width=True
                )
            
            if predict_button:
                with st.spinner('🔄 Procesando predicciones...'):
                    probabilidades = modelo.predict_proba(df_processed)[:, 1]
                    probabilidades_formateadas = [round(prob, 5) for prob in probabilidades]
                    
                    result_df = df_processed.copy()
                    result_df['Probabilidad'] = probabilidades_formateadas
                    
                    # Resultados en contenedor estilizado
                    st.markdown("---")
                    st.markdown('<div class="prediction-section">', unsafe_allow_html=True)
                    st.header(f"🎯 Resultados - {modelo_seleccionado}")
                    
                    # Tabla de resultados con colores
                    st.subheader("📋 Predicciones Detalladas")
                    st.dataframe(
                        result_df.style.background_gradient(subset=['Probabilidad'], cmap='RdYlGn'),
                        use_container_width=True
                    )
                    
                    # Gráfico interactivo con Plotly
                    st.subheader("📈 Distribución de Probabilidades")
                    fig = px.histogram(
                        x=probabilidades, 
                        nbins=20,
                        title=f'Distribución de Probabilidades - {modelo_seleccionado}',
                        labels={'x': 'Probabilidad', 'y': 'Frecuencia'},
                        color_discrete_sequence=['#1f77b4']
                    )
                    fig.update_layout(
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Métricas mejoradas
                    st.subheader("📊 Estadísticas del Modelo")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric(
                            "Probabilidad Promedio", 
                            f"{probabilidades.mean():.5f}",
                            help="Valor promedio de todas las predicciones"
                        )
                    with col2:
                        st.metric(
                            "Probabilidad Máxima", 
                            f"{probabilidades.max():.5f}",
                            help="Mayor probabilidad predicha"
                        )
                    with col3:
                        st.metric(
                            "Probabilidad Mínima", 
                            f"{probabilidades.min():.5f}",
                            help="Menor probabilidad predicha"
                        )
                    with col4:
                        st.metric(
                            "Total Registros", 
                            f"{len(result_df)}",
                            help="Número total de predicciones realizadas"
                        )
                    
                    # Análisis adicional
                    alta_probabilidad = (probabilidades > 0.7).sum()
                    media_probabilidad = ((probabilidades >= 0.3) & (probabilidades <= 0.7)).sum()
                    baja_probabilidad = (probabilidades < 0.3).sum()
                    
                    st.subheader("🎯 Análisis de Resultados")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Alta Demanda (>70%)", alta_probabilidad, help="Libros con alta probabilidad de ser solicitados")
                    with col2:
                        st.metric("Demanda Media (30-70%)", media_probabilidad, help="Libros con probabilidad moderada")
                    with col3:
                        st.metric("Baja Demanda (<30%)", baja_probabilidad, help="Libros con baja probabilidad")
                    
                    # Botón de descarga mejorado
                    csv = result_df.to_csv(index=False)
                    st.download_button(
                        "📥 Descargar Resultados CSV",
                        csv,
                        f"predicciones_{modelo_seleccionado.lower().replace(' ', '_')}.csv",
                        key="download_button",
                        help="Descargar todas las predicciones en formato CSV"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Error al procesar los datos: {str(e)}")
    else:
        # Mensaje de bienvenida cuando no hay datos
        st.markdown("---")
        with st.container():
            st.info("👆 Por favor, carga tus datos usando una de las opciones de arriba para comenzar con las predicciones.")
            
            # Información adicional
            with st.expander("ℹ️ Información sobre el sistema"):
                st.markdown("""
                **¿Qué hace este sistema?**
                - Predice la probabilidad de que un libro sea solicitado
                - Utiliza algoritmos de Machine Learning entrenados con datos históricos
                - Analiza categoría, autor y editorial para hacer predicciones
                
                **¿Cómo usar el sistema?**
                1. Sube un archivo CSV/Excel o ingresa datos manualmente
                2. Verifica que los datos tengan las columnas correctas
                3. Haz clic en "Realizar Predicción"
                4. Revisa los resultados y descarga el archivo con las predicciones
                
                **Formatos de archivo soportados:**
                - CSV (separado por comas)
                - Excel (.xlsx)
                """)

if __name__ == "__main__":
    main()