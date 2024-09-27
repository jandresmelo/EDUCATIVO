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

# Configuración de la conexión a la base de datos
db_config = {
    'dbname': 'olist_ecommerce',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

# Título del Dashboard
st.title("Dashboard de E-commerce de Olist")

# Sección 1: Mapa de Ubicación de Clientes
st.header("Mapa de Ubicación de Clientes")
st.write("Visualización de la ubicación de los clientes con base en su código postal.")

try:
    # Conexión a la base de datos y consulta para obtener datos de geolocalización
    conn = psycopg2.connect(**db_config)
    query_geolocation = """
    SELECT 
        geolocation_state as estado,
        AVG(geolocation_lat) AS lat_centroide,
        AVG(geolocation_lng) AS lng_centroide
    FROM 
        olist_geolocation   
    GROUP BY 
       geolocation_state
    ORDER BY 
       geolocation_state;
    """
    df_geolocation = pd.read_sql_query(query_geolocation, conn)
    conn.close()

    # Crear el mapa
    m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)
    for _, row in df_geolocation.iterrows():
        folium.Marker(
            location=[row['lat_centroide'], row['lng_centroide']],
            popup=f"Estado: {row['estado']}"
        ).add_to(m)
    
    # Mostrar el mapa
    st.map(m)

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")

# Sección 2: Análisis de Clientes por Estado
st.header("Número de Clientes por Estado")

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

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")

# Sección 3: Análisis de Órdenes
st.header("Estado de las Órdenes y Retrasos en la Entrega")

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

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")

# Sección 4: Análisis de Precios y Retrasos
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

except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")

# Sección 5: Análisis de Revisión del Cliente
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

# Sección 6: Modelo de Regresión Lineal
st.header("Modelo de Regresión Lineal para Predecir la Puntuación de la Reseña")

# Convertir 'delivery_delay' a días como número flotante y ajustar los datos
df_price_delay['delivery_delay'] = df_price_delay['delivery_delay'].astype(float)
X = df_price_delay[['price', 'delivery_delay']]
y = df_price_delay['delivery_delay']

# Dividir en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Instanciar y ajustar el modelo
model = LinearRegression()
model.fit(X_train, y_train)

# Realizar predicciones
y_pred = model.predict(X_test)

# Mostrar los resultados
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
st.write(f"Error Cuadrático Medio (MSE): {mse}")
st.write(f"Coeficiente de Determinación (R²): {r2}")

# Sección 7: Análisis del Modelo
st.header("Análisis del Modelo de Random Forest")

# Instanciar el modelo de Random Forest
rf_model = RandomForestRegressor(random_state=42, n_estimators=100)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

# Métricas del modelo de Random Forest
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)
st.write(f"Random Forest - MSE: {mse_rf}")
st.write(f"Random Forest - R²: {r2_rf}")

# Finalizar la aplicación
st.success("Dashboard completado exitosamente.")