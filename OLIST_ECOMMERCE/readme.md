# Dashboard de E-commerce - Análisis de Datos y  Publicación Resultados

Este proyecto consiste en realizar el analisis y visualización de resultados de los datos de e-commerce, basándose en el dataset público de comercio electrónico brasileño proporcionado por Olist. 
Fuente: Brazilian E-Commerce Public Dataset by Olist 
URL: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce.

## Contenido

El proyecto está organizado en las siguientes secciones, cada una de ellas alojada en un subdirectorio específico dentro del repositorio:

1. **Datos descargados**:  
   Contiene los datasets originales utilizados en el proyecto. Esta sección almacena los datos sin procesar tal como fueron descargados desde la fuente.  
   Ubicación: `OLIST_ECOMMERCE/00_DatosDescargados`

2. **Base de datos PostgreSQL**:  
   Almacena los datos estructuradamente para su posterior análisis. Incluye la configuración de la base de datos PostgreSQL con extensiones GIS para manejar datos geoespaciales y realizar consultas complejas.  
   Ubicación: `OLIST_ECOMMERCE/01_BaseDatosSQL`

3. **Análisis descriptivo de los datos**:  
   Contiene los scripts y notebooks que realizan el análisis exploratorio y descriptivo de los datos, utilizando tanto PostgreSQL GIS como Python. Esta sección incluye visualizaciones, estadísticas descriptivas y mapas geoespaciales.  
   Ubicación: `OLIST_ECOMMERCE/02_AnalisisPython`

4. **Regresión lineal y logística**:  
   Desarrolla los modelos de regresión lineal y logística para predecir diferentes variables de interés. Incluye la implementación de los modelos, la evaluación del rendimiento y la interpretación de los resultados.  
   Ubicación: `OLIST_ECOMMERCE/03_Regresión`

5. **Dashboard interactivo**:  
   Un dashboard interactivo desarrollado en Python utilizando Streamlit. Este dashboard permite a los usuarios explorar los datos de manera dinámica y visualizar los principales resultados del análisis.  
   Ubicación: `OLIST_ECOMMERCE/04_Dashboard`

6. **Documento del proyecto**:  
   Proporciona una descripción detallada del proyecto, incluyendo el objetivo, metodología, resultados y conclusiones. Este documento sirve como una guía completa para entender el desarrollo y los hallazgos del proyecto.  
   Ubicación: `OLIST_ECOMMERCE/05_Documento`

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
