import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import scipy.stats as stats
import streamlit as st
import streamlit.components.v1 as components

# Configuración de la conexión a la base de datos
db_config = {
    'dbname': 'olist_ecommerce',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

# Título del Dashboard
st.title("Resultados Analisis de Datos BD Olist E-commerce")
st.write("""
        Conjunto de datos públicos de comercio electrónico brasileño de pedidos realizados en Olist Store. 
        El conjunto de datos tiene información de 100 000 pedidos de 2016 a 2018 realizados en varios mercados de Brasil.
        Sus características permiten ver un pedido desde múltiples dimensiones: desde el estado del pedido, el precio, 
        el pago y el rendimiento del flete hasta la ubicación del cliente, los atributos del producto y, finalmente, 
        las reseñas escritas por los clientes. También publicamos un conjunto de datos de geolocalización que relaciona 
        los códigos postales brasileños con las coordenadas de latitud y longitud.
         
        Realizare la identificación de las áreas geográficas que presentan mayores demoras en las entregas de pedidos, 
        a través del análisis espacial de los datos de geolocalización de clientes y vendedores, junto con la información 
        sobre tiempos de entrega y costos de envío
    """)

# Sección 1: Mapa Estados Ubicación Clientes
st.header("Estados Ubicación Clientes")
st.write("Visualización de estados donde existen clientes.")

# Cargar el archivo HTML del mapa
try:
    with open("ubicacion_generalizada.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # Mostrar el mapa en el dashboard
    components.html(html_content, height=600)

# Descripción del gráfico
    st.write("""
        El mapa se contruye con una imagen del OpenStreetMap, representa la ubicación geográfica de los estados en Brasil donde existen 
        clientes de la plataforma e-commerce. Los marcadores indican la posición aproximada de cada estado.
        La representación refleja mayor concentración de clientes en las regiones sudeste y noreste del país, 
        con estados como São Paulo, Rio de Janeiro, y Minas Gerais, entre otros, destacándose como los principales mercados.
    """)

except Exception as e:
    st.error(f"Error al cargar el mapa: {e}")


# Sección 2: Mapa DUbicación de Clientes
st.header("Mapa de calor - Ubicación Clientes")
st.write(" Ubicación de clientes en Brasil. Los colores varían desde tonos de azul, verde y amarillo, indicando las áreas con diferentes concentraciones de clientes.")

# Cargar el archivo HTML del mapa
try:
    with open("clientes_estado_heatmap.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # Mostrar el mapa en el dashboard
    components.html(html_content, height=600)

# Añadir la descripción del gráfico
    st.write("""
        El mapa se contruye con una imagen del OpenStreetMap, la cual incluyendo detalles geográficos como ciudades, carreteras y áreas protegidas.
        El color Verdes/Amarillo: Indican una alta concentración de clientes en esa ubicación específica. Estos son los puntos de mayor densidad, donde se observa la mayor actividad de clientes.
        El color Azul: Indican una menor concentración de clientes, pero aún así significativa, estas zonas tienen menos actividad en comparación con las áreas más cálidas.
             """)
except Exception as e:
    st.error(f"Error al cargar el mapa: {e}")

# Sección 3: Análisis de Clientes por Estado
st.header("Número de Clientes por Estado")
st.write("Distribuyen los clientes de la plataforma e-commerce por estado, Sao Paulo como el principal mercado.")

try:
    conn = psycopg2.connect(**db_config)
    query_customers = """
    SELECT 
        customer_state AS estado, 
        COUNT(*) AS num_cliente
    FROM 
        olist_order_customers
    GROUP BY 
        customer_state
    ORDER BY 
        num_cliente DESC;
    """
    df_customers = pd.read_sql_query(query_customers, conn)
    conn.close()

    # Gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_customers['estado'], df_customers['num_cliente'], color='skyblue')
    ax.set_xlabel('Estado')
    ax.set_ylabel('Número de Clientes')
    ax.set_title('Número de Clientes por Estado')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Añadir la descripción del gráfico
    st.write("""
        El gráfico representa la distribución del número de clientes por estado en la plataforma de e-commerce. 
        El estado de Sao Paulo (SP) destaca como el principal mercado, con la mayor cantidad de clientes, seguido por Río de Janeiro (RJ) y Minas Gerais (MG). 
        Los estados con menor población de clientes incluyen Roraima (RR) y Amapá (AP), lo que sugiere una concentración de clientes en las áreas más pobladas y urbanizadas de Brasil.
    """)

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")

# Sección 4: Ciudades con Más de 500 Pedidos
st.header("Ciudades con Más de 500 Pedidos")
st.write("Esta sección muestra las ciudades con más de 500 pedidos realizados en la plataforma de e-commerce.")

try:
    # Conectar a la base de datos
    conn = psycopg2.connect(**db_config)

    # Consulta SQL
    query = """
    SELECT
        customer_city AS Ciudad,
        COUNT(customer_id) AS CantidadPedidos
    FROM
        olist_order_customers
    GROUP BY
        customer_city
    HAVING
        COUNT(customer_id) > 500
    ORDER BY
        CantidadPedidos DESC
    LIMIT 10;
    """
    
    # Ejecutar la consulta y cargar los resultados en un DataFrame
    df_cities = pd.read_sql_query(query, conn)
    conn.close()

    # Publicar la tabla en el dashboard
    st.subheader("Top 10 Ciudades con Más de 500 Pedidos")
    st.write("A continuación se presenta una tabla que destaca las ciudades con más de 500 pedidos en la plataforma. Estas ciudades son los principales mercados que concentran un gran volumen de transacciones.")
    
    st.dataframe(df_cities)  # Publicar la tabla en el dashboard usando st.dataframe()

    # Añadir la descripción de la tabla
    st.write("""
        La tabla muestra las 10 principales ciudades que han generado más de 500 pedidos en la plataforma de e-commerce. 
        Estas ciudades son puntos clave en la operación del comercio electrónico, concentrando la mayor actividad de compras.
        São Paulo es típicamente la ciudad con más actividad, seguida de otras grandes urbes como Rio de Janeiro y Belo Horizonte.
    """)

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")


# Sección 5: Análisis de Órdenes
st.header("Estado de las ordenes y retrasos en la entrega")

try:
    conn = psycopg2.connect(**db_config)
    query_orders = """
    SELECT 
        order_status,
        COUNT(order_id) AS cantidad_ordenes
    FROM 
        olist_orders
    GROUP BY 
        order_status
    ORDER BY 
        cantidad_ordenes DESC;
    """
    df_orders = pd.read_sql_query(query_orders, conn)
    conn.close()

    # Gráfico de barras para estados de las órdenes
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_orders['order_status'], df_orders['cantidad_ordenes'], color='skyblue')
    ax.set_xlabel('Estado de la Orden')
    ax.set_ylabel('Cantidad de Órdenes')
    ax.set_title('Cantidad de Órdenes por Estado')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Descripción del gráfico
    st.write("""
        El gráfico muestra la distribución de órdenes según su estado en la plataforma de e-commerce. 
        Se observa que la gran mayoría de las órdenes (alrededor de 100,000) han sido entregadas, 
        representando el estado predominante. Los demás estados, como "shipped", "canceled", y otros, 
        presentan una cantidad de órdenes significativamente menor, lo que indica que la mayoría de las 
        transacciones alcanzan su finalización exitosa con la entrega del pedido..
    """)

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")

# Sección 6: Estado del Pedido y Retraso en la Entrega
st.header("Estado del Pedido y Retraso en la Entrega")

try:
    conn = psycopg2.connect(**db_config)
    
    # Consulta SQL para obtener el estado de los pedidos y calcular el retraso en la entrega
    query_status_delay = """
    SELECT 
        order_id, 
        order_status, 
        order_delivered_customer_date, 
        order_estimated_delivery_date
    FROM 
        olist_orders 
    WHERE 
        order_delivered_customer_date IS NOT NULL;
    """
    
    # Ejecutar la consulta SQL y cargar los resultados en un DataFrame
    df_status = pd.read_sql_query(query_status_delay, conn)
    conn.close()

    # Calcular el retraso en la entrega (en días)
    df_status['delivery_delay'] = (
        pd.to_datetime(df_status['order_delivered_customer_date']) - pd.to_datetime(df_status['order_estimated_delivery_date'])
    ).dt.days

    # Configuración del gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    # Gráfico de violín para mostrar la distribución del retraso según el estado del pedido
    sns.violinplot(x='order_status', y='delivery_delay', data=df_status, inner="quartile", palette="Set2", ax=ax)

    # Ajustes del gráfico
    ax.set_title('Distribución de Retrasos por Estado del Pedido')
    ax.set_xlabel('Estado del Pedido')
    ax.set_ylabel('Retraso en días')
    ax.grid(True)
    plt.xticks(rotation=45)

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

    # Añadir una descripción del gráfico
    st.write("""
        La gráfica muestra la distribución de los retrasos en la entrega según el estado del pedido. 
        Se observa que, en general, los pedidos entregados tienen una distribución tanto de entregas anticipadas 
        (valores negativos de retraso) como de pequeños retrasos (valores positivos de retraso). 
        Por otro lado, los pedidos cancelados tienden a ser cancelados antes de la fecha estimada de entrega.
    """)

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")


# Sección 7: Distribución de Retrasos en la Entrega
st.header("Distribución de Retrasos en la Entrega")

try:
    # Conectar a la base de datos PostgreSQL
    conn = psycopg2.connect(
        dbname="olist_ecommerce",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432",
        options="-c client_encoding=UTF8"
    )

    # Consulta SQL para obtener las fechas de entrega estimadas y reales
    query = """
    SELECT
        order_id,
        order_estimated_delivery_date,
        order_delivered_customer_date
    FROM
        olist_orders
    WHERE
        order_delivered_customer_date IS NOT NULL
        AND order_estimated_delivery_date IS NOT NULL;
    """

    # Ejecutar la consulta y cargar los resultados en un DataFrame de Pandas
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Calcular el retraso en días como la diferencia entre la fecha de entrega real y la estimada
    df['delivery_delay'] = (pd.to_datetime(df['order_delivered_customer_date']) -
                            pd.to_datetime(df['order_estimated_delivery_date'])).dt.days

    # Verificar si la columna 'delivery_delay' se ha calculado correctamente
    if 'delivery_delay' in df.columns:
        # Visualización gráfica: Histograma de retrasos en las entregas
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(df['delivery_delay'], bins=20, color='skyblue', edgecolor='black')
        ax.set_title('Distribución de Retrasos en la Entrega')
        ax.set_xlabel('Días de Retraso (positivos = entregas tardías, negativos = entregas anticipadas)')
        ax.set_ylabel('Cantidad de Pedidos')
        ax.grid(True)

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)

        # Añadir una descripción del gráfico
        st.write("""
            La mayoría de las entregas se realizan antes de la fecha estimada, con un pico alrededor de los 10 a 30 días 
            antes de la entrega esperada..
        """)

    else:
        st.error("Error: La columna 'delivery_delay' no se calculó correctamente.")

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")

finally:
    if conn:
        conn.close()

# Sección 8: Detección de Atípicos en Retraso de Entrega
st.header("Detección de Atípicos en Retraso de Entrega")

try:
    # Conectar a la base de datos PostgreSQL
    conn = psycopg2.connect(
        dbname="olist_ecommerce",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432",
        options="-c client_encoding=UTF8"
    )

    # Consulta SQL para obtener las fechas de entrega estimadas y reales
    query = """
    SELECT 
        order_id,
        order_estimated_delivery_date,
        order_delivered_customer_date
    FROM 
        olist_orders
    WHERE 
        order_delivered_customer_date IS NOT NULL 
        AND order_estimated_delivery_date IS NOT NULL;
    """

    # Ejecutar la consulta y cargar los resultados en un DataFrame de Pandas
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Calcular el retraso en días como la diferencia entre la fecha de entrega real y la estimada
    df['delivery_delay'] = (pd.to_datetime(df['order_delivered_customer_date']) - 
                            pd.to_datetime(df['order_estimated_delivery_date'])).dt.days

    # Verificar si la columna 'delivery_delay' se ha calculado correctamente
    if 'delivery_delay' in df.columns:
        # Visualización gráfica: Boxplot para detectar outliers en los retrasos de entrega
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x=df['delivery_delay'], color='lightgreen', ax=ax)
        ax.set_title('Detección de Atípicos en Retraso de Entrega')
        ax.set_xlabel('Días de Retraso')
        ax.grid(True)

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)

        # Añadir una descripción del gráfico
        st.write("""
            La gráfica evidencia que la mayoría de las entregas se realizan en torno a la fecha estimada, 
            pero existen casos notables de entregas con retrasos o anticipaciones considerables, identificados 
            como outliers en la distribución.
        """)

    else:
        st.error("Error: La columna 'delivery_delay' no se calculó correctamente.")

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")

finally:
    if conn:
        conn.close()


# Sección 9: Análisis de Precios y Retrasos
st.header("Relación entre Precio y Retraso en la Entrega")

try:
    conn = psycopg2.connect(**db_config)
    query_price_delay = """
    SELECT  o.order_id, 
            o.order_delivered_customer_date, 
            o.order_estimated_delivery_date, 
            oi.price
    FROM olist_orders o
    JOIN olist_order_items oi ON o.order_id = oi.order_id
    WHERE o.order_delivered_customer_date IS NOT NULL;
    """
    df_price_delay = pd.read_sql_query(query_price_delay, conn)
    conn.close()

    # Calcular el retraso en días
    df_price_delay['delivery_delay'] = (
        pd.to_datetime(df_price_delay['order_delivered_customer_date']) - pd.to_datetime(df_price_delay['order_estimated_delivery_date'])
    ).dt.days

    # Gráfico de dispersión para precio vs retraso
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df_price_delay['price'], df_price_delay['delivery_delay'], color='blue', alpha=0.5)
    ax.set_xlabel('Precio del Producto')
    ax.set_ylabel('Retraso en días')
    ax.set_title('Relación entre Precio y Retraso en la Entrega')
    st.pyplot(fig)

    # Añadir una descripción del gráfico
    st.write("""
        Este gráfico de dispersión muestra la relación entre el precio del producto y el retraso en la entrega. 
        Se observa que la mayoría de los puntos se concentran en productos de bajo precio, generalmente por debajo de 1000 unidades monetarias. 
        Para estos productos, los retrasos en la entrega varían considerablemente, abarcando desde entregas anticipadas hasta entregas tardías. 
        A medida que el precio del producto aumenta, parece que la variabilidad en los retrasos disminuye, 
        sugiriendo que los productos más caros tienden a cumplir mejor con las fechas de entrega estimadas.
    """)

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")


# Sección 10: Relación entre Año y Venta de Producto por Semestre
st.header("Relación entre Año y Venta de Producto por Semestre")

try:
    conn = psycopg2.connect(**db_config)

    # Consulta SQL para obtener la venta de productos por semestre y año
    query_sales_semester = """
    SELECT 
        EXTRACT(YEAR FROM shipping_limit_date) AS anio,
        CASE 
            WHEN EXTRACT(MONTH FROM shipping_limit_date) <= 6 THEN '1 Semestre'
            ELSE '2 Semestre'
        END AS semestre,
        ROUND(SUM(price)) AS venta_producto,
        ROUND(SUM(freight_value)) AS costo_envio
    FROM 
        olist_order_items
    WHERE 
        EXTRACT(YEAR FROM shipping_limit_date) <> 2020
    GROUP BY 
        anio, semestre
    ORDER BY 
        anio, semestre;
    """
    
    # Ejecutar la consulta y leer los resultados en un DataFrame de Pandas
    df_sales_semester = pd.read_sql(query_sales_semester, conn)
    conn.close()

    # Graficar la relación entre año y venta de producto por semestre
    fig, ax = plt.subplots(figsize=(10, 6))
    for semestre in df_sales_semester['semestre'].unique():
        df_semestre = df_sales_semester[df_sales_semester['semestre'] == semestre]
        ax.plot(df_semestre['anio'], df_semestre['venta_producto'], marker='o', label=semestre)

    ax.set_title('Relación entre Año y Venta de Producto por Semestre')
    ax.set_xlabel('Año')
    ax.set_ylabel('Venta Producto (Sumatoria)')
    ax.set_xticks(df_sales_semester['anio'].unique())
    ax.grid(True)
    ax.legend(title='Semestre')
    st.pyplot(fig)

    # Añadir una descripción del gráfico
    st.write("""
        a) Año 2016: Durante este año, se observa un crecimiento inicial, pero limitado, en las ventas del segundo semestre, 
        mientras que no se registran ventas significativas en el primer semestre.
        
        b) Año 2017: Este año destaca por un fuerte incremento en las ventas durante el segundo semestre, alcanzando el pico 
        más alto de todo el período analizado. En contraste, el primer semestre de 2017 muestra ventas significativamente más bajas.
        
        c) Año 2018: En 2018, se aprecia una inversión en el comportamiento observado en 2017. El primer semestre muestra un 
        crecimiento notable, superando las ventas del segundo semestre del año anterior, mientras que el segundo semestre de 2018 
        muestra una caída considerable, llegando a niveles de ventas por debajo de los registrados en 2016.
    """)

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")

finally:
    if conn:
        conn.close()


# Sección 11: Análisis de Revisión del Cliente
st.header("Análisis de Reseñas y Puntuaciones")

try:
    conn = psycopg2.connect(**db_config)
    query_reviews = """
    SELECT 
        review_score as calificacion, 
        COUNT(review_id) AS cantidad, 
        ROUND(COUNT(review_id) * 100.0 / (SELECT COUNT(*) FROM olist_order_reviews)) AS porcentaje
    FROM 
        olist_order_reviews
    GROUP BY 
        review_score
    ORDER BY 
        review_score;
    """
    df_reviews = pd.read_sql_query(query_reviews, conn)
    conn.close()

    # Gráfico de barras para las calificaciones
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_reviews['calificacion'], df_reviews['cantidad'], color='orange')
    ax.set_xlabel('Calificación')
    ax.set_ylabel('Cantidad')
    ax.set_title('Distribución de Reseñas por Calificación')
    st.pyplot(fig)

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")

# Sección 12: Visualización de Información de Productos con Caras Personalizadas

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler

st.header("Visualización de Información de Productos con Caras Personalizadas")

# Conectar a la base de datos PostgreSQL
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/olist_ecommerce')

# Consulta SQL
query = """
SELECT 
    product_category_name AS categoria_producto,
    COUNT(product_id) AS cnt_productos,
    ROUND(AVG(product_weight_g)) AS media_peso
FROM 
    public.olist_products
WHERE 
    product_category_name IS NOT NULL
GROUP BY 
    product_category_name
ORDER BY 
    cnt_productos DESC;
"""

# Ejecutar la consulta y cargar los resultados en un DataFrame
df = pd.read_sql_query(query, engine)

# Normalizar las características para ajustarlas a las visualizaciones
scaler = MinMaxScaler()
df_normalized = pd.DataFrame(scaler.fit_transform(df[['media_peso', 'cnt_productos']]),
                             columns=['media_peso', 'cnt_productos'])

# Añadir la columna de categoría de producto nuevamente al DataFrame normalizado
df_normalized['categoria_producto'] = df['categoria_producto']

# Función para dibujar caras personalizadas basadas en características del producto
def draw_custom_face(ax, media_peso, cnt_productos, label):
    # Cara
    face = plt.Circle((0.5, 0.5), 0.4, color='orange', fill=True)
    ax.add_patch(face)

    # Ojos basados en el conteo de productos
    eye_y = 0.65
    eye_x_dist = 0.15 + 0.1 * cnt_productos 
    eye_size = 0.05 + 0.05 * cnt_productos  
    left_eye = plt.Circle((0.5 - eye_x_dist, eye_y), eye_size, color='black')
    right_eye = plt.Circle((0.5 + eye_x_dist, eye_y), eye_size, color='black')
    ax.add_patch(left_eye)
    ax.add_patch(right_eye)

    # Boca basada en el peso promedio del producto
    mouth_y = 0.35
    mouth_width = 0.2 + 0.2 * cnt_productos
    mouth_height = -0.1 * media_peso  
    ax.plot([0.5 - mouth_width / 2, 0.5 + mouth_width / 2], 
            [mouth_y, mouth_y + mouth_height], color='red', linewidth=2)

    # Etiqueta de la categoría del producto
    ax.text(0.5, -0.1, label, horizontalalignment='center', fontsize=12, fontweight='bold')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

# Crear figuras para cada categoría de producto
fig, axs = plt.subplots(nrows=5, ncols=5, figsize=(15, 15))
axs = axs.flatten()

for i, (index, row) in enumerate(df_normalized.iterrows()):
    if i >= len(axs):
        break
    draw_custom_face(axs[i], row['media_peso'], row['cnt_productos'], row['categoria_producto'])

plt.tight_layout()

# Mostrar el gráfico en Streamlit
st.pyplot(fig)

# Añadir una descripción del gráfico
st.write("""
    Esta visualización utiliza caras personalizadas para representar las características de los productos en diferentes categorías. 
    El tamaño de los ojos representa el número de productos en esa categoría, y la forma de la boca refleja el peso promedio de los productos.
""")

# Sección 13: Información sobre los Vendedores
st.header("Información sobre los Vendedores")
st.write("Distribución de vendedores en las principales ciudades donde opera la plataforma de e-commerce.")

# Crear la cadena de conexión con SQLAlchemy
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/olist_ecommerce')

# Ejecutar la consulta SQL y cargar los resultados en un DataFrame de Pandas
query = """
SELECT 
    seller_city AS ciudad,
    COUNT(seller_id) AS cnt_vendedores
FROM 
    public.olist_sellers
GROUP BY 
    seller_city
ORDER BY 
    cnt_vendedores DESC
LIMIT 5;
"""

try:
    df = pd.read_sql_query(query, engine)

    # Verificar que las columnas se cargaron correctamente
    st.write("Columnas cargadas:", df.columns.tolist())

    # Crear un gráfico de estrellas para las cinco ciudades con más vendedores
    def radar_chart(df):
        labels = df['ciudad']
        num_vars = len(labels)

        # Ángulos para cada eje en el gráfico de radar
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        # La primera ciudad se repite para cerrar el gráfico de radar
        stats = df['cnt_vendedores'].tolist()
        stats += stats[:1]
        angles += angles[:1]

        # Inicializar el gráfico de radar
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        ax.fill(angles, stats, color='skyblue', alpha=0.4)
        ax.plot(angles, stats, color='blue', linewidth=2)

        # Ajustar los atributos del gráfico
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, size=12, fontweight='bold')

        plt.title('Cantidad de Vendedores en las Principales Ciudades')
        st.pyplot(fig)

    # Crear el gráfico de radar
    radar_chart(df)

    # Descripción de la sección
    st.write("""
        a) Sao Paulo: Representada en la esquina derecha del gráfico, es la ciudad con la mayor cantidad de vendedores,
        lo que se refleja en la longitud del eje correspondiente.
        b) Rio de Janeiro: Ubicada en la parte superior izquierda del gráfico, es la segunda ciudad con más vendedores.
        c) Belo Horizonte: También a la izquierda, muestra un número menor de vendedores en comparación con Sao Paulo y Rio de Janeiro.
        d) Curitiba: En la parte superior, tiene una cantidad de vendedores similar a la de Belo Horizonte.
        e) Ribeirao Preto: En la parte inferior del gráfico, muestra la menor cantidad de vendedores entre las cinco ciudades..
    """)

except Exception as e:
    st.error(f"Error al conectar a la base de datos o al generar el gráfico: {e}")

# Sección 14: Información de Pagos
st.header("Métodos de Pago")
st.write ("El gráfico muestra la distribución de los métodos de pago utilizados por los clientes")

try:
    conn = psycopg2.connect(
        dbname="olist_ecommerce",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432",
        options="-c client_encoding=UTF8"
    )
    
    # Consulta SQL para obtener el método de pago y el valor de los pagos
    query = """
    SELECT DISTINCT 
        payment_type AS metodo_pago,
        ROUND(SUM(payment_value)) AS valor_pagos
    FROM 
        olist_order_payments
    WHERE 
        payment_type <> 'not_defined'
    GROUP BY 
        metodo_pago;
    """
    
    # Ejecutar la consulta y leer los resultados en un DataFrame de Pandas
    df = pd.read_sql_query(query, conn)
    
    # Cerrar la conexión
    conn.close()

    # Crear el gráfico de torta (pastel)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(df['valor_pagos'], labels=df['metodo_pago'], autopct='%1.1f%%', startangle=140)
    ax.set_title('Métodos de Pago')
    st.pyplot(fig)

    # Añadir una descripción del gráfico
    st.write("""
    La tarjeta de credito representa la mayor parte de los pagos, con un 78.3% del total.
    Boleto bancario: Es el segundo método más común, con un 17.9% de los pagos.
    Tarjeta de débito: Representa el 2.4% de los pagos, siendo un método menos frecuente.
Voucher: Con 1.4% del total, este es el método de pago menos utilizado entre los presentados.""")

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")

finally:
    # Asegurarse de que la conexión se cierra
    if conn:
        conn.close()


# Sección 15: Gráfico de Barras - Pagos con Tarjeta de Crédito vs. Número de Cuotas
st.header("Pagos con Tarjeta de Crédito por Número de Cuotas")
st.write("Gráfico de barras para visualizar el valor total de pagos en función del número de cuotas")
try:
    conn = psycopg2.connect(**db_config)
    
    # Consulta SQL para obtener el método de pago, número de cuotas, valor de pagos y porcentaje
    query = """
    SELECT 
        payment_type AS metodo_pago,
        payment_installments AS cuota,
        ROUND(SUM(payment_value)) AS valor_pagos,
        ROUND(CAST(SUM(payment_value) * 100.0 / SUM(SUM(payment_value)) OVER () AS numeric), 2) AS porcentaje
    FROM 
        olist_order_payments
    WHERE 
        payment_type = 'credit_card'
    GROUP BY 
        metodo_pago, cuota
    ORDER BY 
        cuota ASC;
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Agrupar cuotas entre 11 y 22
    df['cuota_grupo'] = df['cuota'].apply(lambda x: '11-22' if 11 <= x <= 22 else str(x))

    # Agrupar por cuota_grupo y sumar valores de pagos
    df_grouped = df.groupby('cuota_grupo').agg({'valor_pagos': 'sum'}).reset_index()

    # Ordenar por número de cuotas para visualización
    df_grouped['cuota_grupo'] = pd.Categorical(df_grouped['cuota_grupo'], 
                                               categories=sorted(df_grouped['cuota_grupo'], 
                                               key=lambda x: int(x.split('-')[0]) if '-' in x else int(x)), 
                                               ordered=True)

    # Crear el gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_grouped['cuota_grupo'], df_grouped['valor_pagos'], color='skyblue')

    # Añadir etiquetas y título
    ax.set_xlabel('Número de Cuotas')
    ax.set_ylabel('Valor Pagos (BRL)')
    ax.set_title('Valor de Pagos por Número de Cuotas (con Tarjeta de Crédito)')
    ax.grid(True)

    st.pyplot(fig)

    # Añadir una descripción del gráfico
    st.write("""
        El gráfico muestra la distribución del valor total de pagos realizados con tarjeta de crédito en función del número de cuotas. 
        Observamos que los pagos a 1 y 2 cuotas son los más comunes, representando la mayor parte del valor total de pagos.
    """)

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")

finally:
    if conn:
        conn.close()

# Sección 16: Métodos de Pago y Retrasos en la Entrega
st.header("Métodos de Pago y Retrasos en la Entrega")

try:
    conn = psycopg2.connect(**db_config)
    
    # Consulta SQL para obtener el método de pago y las fechas de entrega
    query_payments_delay = """
    SELECT p.payment_type, 
           o.order_delivered_customer_date, 
           o.order_estimated_delivery_date
    FROM olist_order_payments p
    JOIN olist_orders o ON p.order_id = o.order_id
    WHERE o.order_delivered_customer_date IS NOT NULL;
    """
    
    df_payments = pd.read_sql_query(query_payments_delay, conn)
    conn.close()

    # Calcular el retraso en la entrega (en días)
    df_payments['delivery_delay'] = (
        pd.to_datetime(df_payments['order_delivered_customer_date']) - pd.to_datetime(df_payments['order_estimated_delivery_date'])
    ).dt.days

    # Gráfico de caja y bigotes para mostrar la distribución de los retrasos por método de pago
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot([df_payments[df_payments['payment_type'] == payment]['delivery_delay'] for payment in df_payments['payment_type'].unique()],
               labels=df_payments['payment_type'].unique(), patch_artist=True)

    ax.set_title('Distribución de Retrasos por Método de Pago')
    ax.set_xlabel('Método de Pago')
    ax.set_ylabel('Retraso (días)')
    ax.grid(True)

    st.pyplot(fig)

    # Añadir una descripción del gráfico
    st.write("""
        Em el gráfico de caja y bigotes se observa la distribución de los retrasos en la entrega según el método de pago, 
        en promedio todos los métodos tienen entregas anticipadas, no se observan diferencias significativas entre 
        los métodos de pago. Existen valores atípicos notables, con algunas entregas extremadamente anticipadas o muy tardías, 
        lo que sugiere variabilidad en los tiempos de entrega independientemente del método de pago.
    """)

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")

finally:
    if conn:
        conn.close()

# Sección 17: Análisis de Reseñas de Pedidos
st.header("Análisis de Reseñas de Pedidos")

# Definir los detalles de la conexión
user = 'postgres'
password = 'postgres'
host = 'localhost'
port = '5432'
dbname = 'olist_ecommerce'

# Crear el engine usando SQLAlchemy
connection_string = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
engine = create_engine(connection_string)

try:
    # Definir y ejecutar la consulta SQL
    query1 = """
    SELECT 
        review_score as calificacion, 
        COUNT(review_id) as cantidad, 
        ROUND(COUNT(review_id) * 100.0 / (SELECT COUNT(*) FROM olist_order_reviews)) AS Porcentaje
    FROM 
        olist_order_reviews
    GROUP BY 
        review_score
    ORDER BY 
        review_score;
    """

    # Ejecutar la consulta y cargar los datos en un DataFrame
    opiniones_clientes = pd.read_sql_query(query1, engine)

    # Mostrar los datos en una tabla en Streamlit
    st.write("Distribución de Calificaciones de Reseñas:")
    st.dataframe(opiniones_clientes)

    # Crear un gráfico de barras para visualizar la distribución de calificaciones
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(opiniones_clientes['calificacion'], opiniones_clientes['Cantidad'], color='skyblue')
    ax.set_xlabel('calificación')
    ax.set_ylabel('cantidad de Reseñas')
    ax.set_title('Distribución de Reseñas por Calificación')
    plt.xticks(opiniones_clientes['calificacion'])
    plt.grid(True)
    st.pyplot(fig)

    # Añadir una descripción del análisis
    st.write("""
        El 58% de las calificaciones otorgadas por los clientes corresponde a la puntuación más alta (5), lo que indica un alto nivel de satisfacción.
        Un 11% de los clientes ha calificado con la puntuación más baja (0), lo que podría reflejar un grupo insatisfecho o con problemas significativos en su experiencia de compra.
        En total, solo el 14% de las calificaciones se encuentran entre 1 y 2, lo que muestra que los clientes tienden a polarizar sus opiniones, 
        otorgando muy pocas calificaciones bajas (entre 1 y 2).
    """)

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")

finally:
    # Asegurarse de que la conexión se cierra
    if engine:
        engine.dispose()


# Sección 18: Matriz de Correlación entre Variables
st.header("Matriz de Correlación entre Variables")

# Importar las bibliotecas necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Conectar a la base de datos PostgreSQL
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/olist_ecommerce')

try:
    # Ejecutar la consulta SQL y cargar los resultados en un DataFrame de Pandas
    query = """
    SELECT 
        o.order_id,                             -- ID del pedido (olist_orders)
        o.order_delivered_customer_date,        -- Fecha de entrega al cliente (olist_orders)
        o.order_estimated_delivery_date,        -- Fecha estimada de entrega (olist_orders)
        c.customer_zip_code_prefix AS customer_zip,  -- Código postal del cliente (olist_order_customers)
        s.seller_zip_code_prefix AS seller_zip,      -- Código postal del vendedor (olist_sellers)
        ST_Distance(c.location, s.location) AS distancia, -- Distancia entre el cliente y el vendedor (calculado con PostGIS)
        r.review_score,                        -- Puntuación de la reseña del pedido (olist_order_reviews)
        p.payment_type,                        -- Tipo de pago utilizado (olist_order_payments)
        oi.price                               -- Precio del producto (olist_order_items)
    FROM
        olist_orders o
    JOIN 
        olist_order_customers c ON o.customer_id = c.customer_id
    JOIN 
        olist_order_items oi ON o.order_id = oi.order_id
    JOIN 
        olist_sellers s ON oi.seller_id = s.seller_id
    JOIN 
        olist_order_reviews r ON o.order_id = r.order_id
    JOIN 
        olist_order_payments p ON o.order_id = p.order_id
    WHERE 
        o.order_delivered_customer_date IS NOT NULL
    LIMIT 1000;  -- Aumenté el límite para obtener una mejor visualización
    """

    # Cargar los datos en un DataFrame
    df = pd.read_sql_query(query, engine)

    # Filtrar solo las columnas numéricas para la matriz de correlación
    df_numeric = df.select_dtypes(include=[np.number])

    # Manejo de valores NaN (eliminación en este caso)
    df_numeric = df_numeric.dropna()

    # Calcular la matriz de correlación
    corr_matrix = df_numeric.corr()

    # Visualizar la matriz de correlación como un heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Matriz de Correlación entre Variables')
    st.pyplot(plt)

    # Añadir una descripción del análisis
    st.write("""
        1) Hay una alta correlación positiva entre el código postal del cliente y el del vendedor. por ello se identifica que que los clientes y vendedores 
        tienden a estar geográficamente cercanos
        2) Hay una correlación negativa significativa entre la distancia y la puntuación de la reseña. Los clientes que están más lejos del vendedor 
        tienden a dar peores puntuaciones, posiblemente debido a tiempos de entrega más largos o mayores costos de envío.
        price vs seller_zip (0.99):
        3) El precio tiene una correlación casi perfecta con el código postal del vendedor, ciertos vendedores en áreas específicas tienden a vender productos 
        a precios similares por ello se indica que los precios están asociados a ciertas regiones.
""")

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")

finally:
    # Asegurarse de que la conexión se cierra
    if engine:
        engine.dispose()


# Sección 19: Modelo de Regresión Lineal
st.header("Modelo de Regresión Lineal: Predicción del Puntaje de Reseña")

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Conectar a la base de datos PostgreSQL
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/olist_ecommerce')

try:
    # Consulta SQL para obtener datos relevantes
    query = """
    SELECT 
        s.seller_zip_code_prefix AS seller_zip, 
        oi.price, 
        (o.order_delivered_customer_date - o.order_estimated_delivery_date) AS delivery_delay, 
        r.review_score
    FROM 
        olist_orders o
    JOIN 
        olist_order_items oi ON o.order_id = oi.order_id
    JOIN 
        olist_sellers s ON oi.seller_id = s.seller_id
    JOIN 
        olist_order_reviews r ON o.order_id = r.order_id
    WHERE 
        o.order_delivered_customer_date IS NOT NULL 
        AND o.order_estimated_delivery_date IS NOT NULL;
    """
    
    # Cargar los datos en un DataFrame de Pandas
    df = pd.read_sql_query(query, engine)

    # Convertir 'delivery_delay' a días como número flotante
    df['delivery_delay'] = (df['delivery_delay']).dt.days

    # Definir las características (X) y la variable dependiente (y)
    X = df[['seller_zip', 'price', 'delivery_delay']]
    y = df['review_score']

    # Dividir en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Verificar los tipos de datos
    X_train['seller_zip'] = pd.to_numeric(X_train['seller_zip'], errors='coerce')
    X_test['seller_zip'] = pd.to_numeric(X_test['seller_zip'], errors='coerce')

    # Imputar valores nulos con ceros
    X_train = X_train.fillna(0)
    X_test = X_test.fillna(0)

    # Instanciar el modelo de regresión lineal
    model = LinearRegression()

    # Ajustar el modelo a los datos de entrenamiento
    model.fit(X_train, y_train)

    # Realizar predicciones sobre el conjunto de prueba
    y_pred = model.predict(X_test)

    # Calcular el Error Cuadrático Medio (MSE) y el Coeficiente de Determinación (R²)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Mostrar los resultados en el dashboard
    st.write(f"**Error Cuadrático Medio (MSE):** {mse:.2f}")
    st.write(f"**Coeficiente de Determinación (R²):** {r2:.2f}")

    # Visualizar los residuos
    residuos = y_test - y_pred
    plt.figure(figsize=(8, 6))
    sns.histplot(residuos, kde=True, bins=30, color='skyblue')
    plt.title('Distribución de los Residuos')
    plt.xlabel('Residuos')
    plt.ylabel('Frecuencia')
    st.pyplot(plt)


# Añadir una descripción del análisis
    st.write("""
        1) Concentración de Residuos: La mayor parte de los residuos está concentrada alrededor de 0, 
            lo que indica que el modelo predice razonablemente bien la mayoría de las veces, pero hay cierta dispersión.
             
        2) Distribución Asimétrica: Existe una asimetría en la distribución de los residuos, 
            con algunos valores concentrándose más hacia residuos ligeramente negativos, lo que podría sugerir que el 
             modelo tiende a subestimar ligeramente el puntaje de las reseñas en algunos casos.
             
        3) Picos en la Distribución: Los picos en torno a 0 y 1 indican que el modelo realiza 
             muchas predicciones con errores pequeños, pero también hay varias predicciones con errores moderados, 
             visibles en los picos secundarios..
""")
except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")

finally:
    # Cerrar la conexión
    if engine:
        engine.dispose()

# Sección 21: Ajuste del Modelo de Regresión Lineal y Obtención de Coeficientes
st.header("Ajuste del Modelo de Regresión Lineal y Obtención de Coeficientes")

try:
    # Ajustar el modelo a los datos de entrenamiento
    model.fit(X_train, y_train)

    # Obtener los coeficientes de la regresión
    coef = model.coef_
    intercept = model.intercept_

    # Mostrar los coeficientes e intercepto en Streamlit
    st.subheader("Coeficientes de la Regresión Lineal")
    coef_df = pd.DataFrame(coef, X_train.columns, columns=['Coeficientes'])
    st.write(coef_df)

    st.subheader("Intercepto del Modelo")
    st.write(f"Intercepto: {intercept}")

    # Descripción adicional
    st.write("""
        El modelo sugiere que el retraso en la entrega tiene un impacto negativo en la puntuación de las reseñas,
        mientras que el código postal del vendedor y el precio del producto no parecen influir significativamente 
        en la puntuación de las reseñas. Sin embargo, la magnitud del impacto del retraso es pequeña, y otros 
        factores no capturados por el modelo podrían estar influyendo en las calificaciones.
    """)

except Exception as e:
    st.error(f"Error al ajustar el modelo: {e}")

# Sección 20: Evaluación del Modelo de Random Forest
st.header("Evaluación del Modelo de Random Forest")

# Importar la clase RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor

# Instanciar el modelo de Random Forest
rf_model = RandomForestRegressor(random_state=42, n_estimators=100)

# Ajustar el modelo a los datos de entrenamiento
rf_model.fit(X_train, y_train)

# Realizar predicciones sobre el conjunto de prueba
y_pred_rf = rf_model.predict(X_test)

# Calcular el MSE y R² para el modelo de Random Forest
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

# Mostrar los resultados en el dashboard
st.write(f"**Random Forest - Error Cuadrático Medio (MSE):** {mse_rf}")
st.write(f"**Random Forest - Coeficiente de Determinación (R²):** {r2_rf}")

# Visualizar los residuos del modelo
plt.figure(figsize=(10, 6))
sns.histplot(y_test - y_pred_rf, kde=True, color='skyblue', bins=30)
plt.title('Distribución de los Residuos - Random Forest')
plt.xlabel('Residuos')
plt.ylabel('Frecuencia')
st.pyplot(plt)

# Descripción adicional
st.write("""
        El modelo de Random Forest tiene un rendimiento intermedio según los valores de MSE y R². 
        La distribución de los residuos muestra una tendencia a un ajuste decente, el bajo valor de R² 
        sugiere que el modelo no captura toda la complejidad del fenómeno que se está tratando de predecir. 
        Es por ello el modelo no lineal o más profundo pueda ser más adecuado para mejorar la precisión.
    """)
# Sección 22: Gráfico Q-Q plot para los residuos

st.header("Q-Q Plot de los Residuos - Random Forest")

import matplotlib.pyplot as plt
import scipy.stats as stats

# Calcular los residuos
residuos_rf = y_test - y_pred_rf

# Q-Q plot para los residuos del modelo Random Forest
plt.figure(figsize=(8, 6))
stats.probplot(residuos_rf, dist="norm", plot=plt)
plt.title('Q-Q Plot de los Residuos - Random Forest')
st.pyplot(plt)

# Añadir una breve explicación del Q-Q Plot
st.write("""
Los puntos en el Q-Q plot no siguen una línea recta, sino que se desvían significativamente de 
la línea roja diagonal (que representa la distribución normal). Esta curvatura indica que los 
residuos del modelo Random Forest no siguen una distribución normal.
""")

# Inserta el texto de copyright al final del dashboard
st.markdown("---")  # Línea horizontal para separar
st.markdown("© 2024. Jorge Andres Melo 2024. Programación en Ciencia de Datos.")

# Finalizar la aplicación
st.success("Análisis culminado.")

### Correr el comando: python -m streamlit run dashboard.py