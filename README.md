# Sistema de Auditoría de Pasivos Corrientes

Sistema profesional para auditoría y análisis de pasivos corrientes con generación de informes según normas RT 7, RT 37 y NIAs.

## Instalación

```bash
pip install -r requirements.txt
streamlit run pasivos_corrientes_app.py
```

## Despliegue en Render

Build Command: `pip install -r requirements.txt`
Start Command: `streamlit run pasivos_corrientes_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`

## Características

- 7 Módulos de análisis
- 3 Tipos de informes (PDF, Excel, Auditoría con Normas)
- Detección de anomalías con ML
- Visualizaciones interactivas
