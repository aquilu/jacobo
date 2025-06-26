# 📚 Sistema de Predicción de Libros Solicitados - BLAA

Sistema de predicción basado en Machine Learning para determinar la probabilidad de que un libro sea solicitado en la Biblioteca Luis Ángel Arango.

## 👨‍💼 Autor
**Jacobo Mican**  
Estudiante en Práctica - Universidad Nacional  
Banco de la República  
Email: jacobo_1501@hotmail.com

## 🏛️ Contacto Institucional
**halbarba@banrep.gov.co**  
Banco de la República

## 📋 Descripción
Aplicación web desarrollada con Streamlit que utiliza un modelo de Regresión Logística para predecir la probabilidad de que un libro sea solicitado basándose en características como:
- 📖 Categoría
- ✍️ Autor  
- 🏢 Editorial (Publisher)

## 🚀 Instalación y Configuración

### 1. Preparar el entorno
```bash
# Navegar al directorio del proyecto
cd /home/halbarba/proyectos/jacobo

# Activar entorno virtual
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
# Instalar todas las dependencias necesarias
pip install streamlit plotly pillow scikit-learn pandas joblib openpyxl
```

## 🎯 Ejecución de la Aplicación

### Pasos para ejecutar:

1. **Activar el entorno virtual**
   ```bash
   source venv/bin/activate
   ```

2. **Verificar directorio actual**
   ```bash
   pwd
   # Debe mostrar: /home/halbarba/proyectos/jacobo
   ```

3. **Ejecutar la aplicación**
   ```bash
   streamlit run Interfaz_Final.py
   ```

4. **Acceder a la aplicación**
   - Abrir navegador web
   - Ir a: **http://localhost:8501**

### 🔄 Comandos completos en secuencia:
```bash
cd /home/halbarba/proyectos/jacobo
source venv/bin/activate
streamlit run Interfaz_Final.py
```

### 🛑 Para detener la aplicación:
- Presionar `Ctrl + C` en la terminal

## ✨ Características de la Interfaz

- 🎨 **Diseño moderno** con imagen institucional del Banco de la República
- 📊 **Gráficos interactivos** con Plotly
- 📁 **Carga de archivos** CSV/Excel o entrada manual
- 🎯 **Análisis detallado** de resultados con métricas de demanda
- 📱 **Diseño responsivo** y sidebar de configuración
- 💾 **Descarga de resultados** en formato CSV

## 📦 Archivos Principales

- `Interfaz_Final.py` - Aplicación principal de Streamlit
- `modelo_BLAA.pkl` - Modelo entrenado de Machine Learning
- `img/banrep.jpeg` - Imagen institucional
- `venv/` - Entorno virtual con dependencias

## 🔧 Requisitos del Sistema

- **Python**: 3.8+
- **Dependencias principales**:
  - streamlit
  - pandas
  - scikit-learn
  - plotly
  - pillow
  - joblib
  - openpyxl

## 📝 Formato de Datos

### Columnas requeridas:
- `Categoria` - Categoría temática del libro
- `Author` - Autor del libro
- `Publisher` - Editorial del libro

### Formatos soportados:
- CSV (separado por comas)
- Excel (.xlsx)

## 🎯 Resultados

La aplicación proporciona:
- **Probabilidades individuales** para cada libro
- **Distribución de probabilidades** mediante histograma interactivo
- **Estadísticas del modelo** (promedio, máximo, mínimo)
- **Análisis por categorías** de demanda (alta, media, baja)
- **Archivo descargable** con todas las predicciones