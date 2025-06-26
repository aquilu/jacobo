# Proyecto de Predicción de Libros Solicitados

Sistema de predicción basado en Machine Learning para determinar la probabilidad de que un libro sea solicitado en la biblioteca.

## Autor
**Jacobo Mican**  
Estudiante en Práctica - Universidad Nacional  
Banco de la República  
Email: jacobo_1501@hotmail.com

## Contacto Institucional
**halbarba@banrep.gov.co**  
Banco de la República

## Descripción
Aplicación web desarrollada con Streamlit que utiliza un modelo de Regresión Logística para predecir la probabilidad de que un libro sea solicitado basándose en características como:
- Categoría
- Autor
- Editorial (Publisher)

## Instalación
```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso
```bash
streamlit run Interfaz_Final.py
```

## Requisitos
- Python 3.8+
- Ver requirements.txt para dependencias completas