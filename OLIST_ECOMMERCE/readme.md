# Dashboard de E-commerce - Análisis de Datos y  Publicación Resultados

Este proyecto consiste en realizar el analisis y visualización de resultados de los datos de e-commerce, basándose en el dataset público de comercio electrónico brasileño proporcionado por Olist. 
Fuente: Brazilian E-Commerce Public Dataset by Olist 
URL: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce.

## Contenido

- [Base de datos postgres: Almacena los datos estructuradamente para su posterior análisis.](#OLIST_ECOMMERCE/01_BaseDatosSQL)
- [Analisis descriptivo de los datos, realizado en PostgreSQL GIS y Python.](#características-del-proyecto)
- [Regresion lineal y Logistica.](#características-del-proyecto)
- [Dashboard interactivo desarrollado en Python utilizando Streamlit.](#características-del-proyecto)
  

## Características del Proyecto

- **Análisis de clientes y pedidos**: Número de clientes por estado, mapa de calor de ubicación de clientes, distribución de órdenes por estado del pedido.
- **Análisis de retrasos**: Distribución de retrasos en la entrega, boxplot de retrasos por método de pago, Q-Q plots de residuos de regresión lineal y Random Forest.
- **Información de productos y vendedores**: Radar chart para la cantidad de vendedores en las principales ciudades, visualización de categorías de productos mediante caras personalizadas.
- **Métodos de pago y evaluaciones**: Distribución de métodos de pago, valor de pagos por número de cuotas, análisis de reseñas.
- **Matriz de correlaciones**: Análisis de correlación entre variables clave.

## Requisitos

- **Python 3.x**
- **Bibliotecas Python**:
  - `streamlit`
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `seaborn`
  - `scikit-learn`
  - `scipy`
  - `psycopg2`
  - `SQLAlchemy`

## Instalación

A. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/tu_proyecto.git
   cd tu_proyecto
   ```
B. **Base de datos PostgreSQL **: 
    Base de datos PostgreSQL - PostGIS.   
C. ** Analisis y Regresión **:
    Archivos ipynb cuadernos jupyter para visualizar en Jupyter Anaconda, Visual Studio, etc.

D. **Ejecución del Dashboard **:
Para ejecutar el dashboard, asegúrate de estar en el directorio del proyecto y ejecutar el script de Streamlit (`dashboard.py`). Esto lanzará el dashboard en tu navegador web predeterminado.

## Descripción de las Secciones

1. **Resumen de Pedidos y Clientes**
   - Gráficos sobre la cantidad de clientes por estado y mapas de calor.
   - Métricas básicas sobre el total de pedidos y clientes.

2. **Análisis de Retrasos**
   - Histograma y boxplot de retrasos en la entrega.
   - Q-Q plots de residuos para evaluar los modelos de regresión lineal y Random Forest.

3. **Información de Productos y Vendedores**
   - Visualización de la distribución de vendedores y productos.
   - Radar chart y caras personalizadas para análisis gráfico.

4. **Métodos de Pago y Evaluaciones**
   - Distribución de métodos de pago mediante gráficos de torta.
   - Análisis de valor de pagos por número de cuotas y distribución de calificaciones.

5. **Matriz de Correlaciones**
   - Heatmap de correlaciones entre variables clave para análisis más profundo.

## Contribuciones

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del proyecto.
2. Crea una nueva rama (`feature/nueva_funcionalidad`).
3. Realiza tus modificaciones.
4. Haz un commit de tus cambios (`Añadir nueva funcionalidad`).
5. Haz push a la rama creada.
6. Abre un Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT. Para más detalles, consulta el archivo `LICENSE`.
