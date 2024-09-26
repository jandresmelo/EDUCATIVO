
-- CONSULTA BASE DE DATOS 
--- Fuente Nombre: Brazilian E-Commerce Public Dataset by Olist
--- Fuente URL: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_type = 'BASE TABLE';


--- Tabla 1 - olist_geolocation: Información de geolocalización.
--- Tabla 2 - olist_order_customers: Información de los clientes.
--- Tabla 3 - olist_orders: : Contiene la información de los pedidos.
--- Tabla 4 - olist_order_items: Detalles de los artículos de cada pedido.
--- Tabla 5 - olist_products: Información de los productos.
--- Tabla 6 - olist_sellers: Información sobre los vendedores.
--- Tabla 7 - olist_order_payments: Información de pagos.
--- Tabla 8 - olist_order_reviews: Reseñas de los pedidos.
--- Tabla 9 - product_category_name_translation: traducciones de los nombres de las categorías de productos desde portugués a ingles.
--- Tabla 10 - spatial_ref_sys: Extensión de PostgreSQL que permite manejar datos geográficos.



-- 1) Tabla olist_geolocation: Información de geolocalización.

SELECT 
	geolocation_id, 
	geolocation_lat, 
	geolocation_lng 
FROM olist_geolocation;

select count(geolocation_id) 
from olist_geolocation

---- Resultado 1.000.163 registros localizados geográficamente.

--- Generalización puntos por estado
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
--- Resultado 27 estados.

-- 2) Tabla olist_order_customers: Información de los clientes.

--- Cuantos Clientes tiene cada estado

SELECT distinct 
    customer_state as estado, 
    COUNT(*) AS num_cliente
FROM 
    olist_order_customers
GROUP BY 
    customer_state
ORDER BY 
    num_cliente DESC;

---- Los estados que mas se encuentran clientes registrados son SP: São Paulo, RJ: Rio de Janeiro y MG: Minas Gerais

--- Consulta geográfica
   
SELECT 
        customer_city, 
        COUNT(*) AS num_cliente,
        AVG(ST_Y(location::geometry)) AS latitude,
        AVG(ST_X(location::geometry)) AS longitude
    FROM 
        olist_order_customers
    WHERE 
        location IS NOT NULL
    GROUP BY 
        customer_city
    ORDER BY 
        num_cliente DESC;
       
       
--- Ciudades con Más de 500 Pedidos en la Plataforma de E-commerce

SELECT 
    customer_city,
    COUNT(customer_id) AS CantidadPedidos
FROM 
    olist_order_customers
GROUP BY 
    customer_city
HAVING 
    COUNT(customer_id) > 500
ORDER BY 
    CantidadPedidos DESC;
   
--- Cantidad de Pedidos por Estado
SELECT  
        customer_city,
        customer_state,
        COUNT(customer_id) AS CantidadPedidos,
        AVG(ST_Y(location::geometry)) AS latitude,
        AVG(ST_X(location::geometry)) AS longitude
    FROM 
        public.olist_order_customers
    WHERE 
        location IS NOT NULL
    GROUP BY 
        customer_city, customer_state
    HAVING 
        COUNT(customer_id) > 1000
    ORDER BY 
        CantidadPedidos DESC;


   
-- 3) Tabla olist_orders: : Contiene la información de los pedidos.

--- Relación entre el estado del pedido y el retraso en la entrega

SELECT 
	order_status,
	COUNT(order_id) AS CantidadOrdenes
FROM 
	olist_orders
GROUP BY 
	order_status
ORDER BY 
	CantidadOrdenes DESC; 

--- Estado del Pedido y Retraso en la Entrega

SELECT 
	order_id, 
	order_status, 
	order_delivered_customer_date, 
	order_estimated_delivery_date
FROM olist_orders 
WHERE order_delivered_customer_date IS NOT NULL;

--- fechas de entrega estimadas vs  enregadas
SELECT 
	order_id,
	order_estimated_delivery_date,
	order_delivered_customer_date
FROM 
	olist_orders
WHERE 
	order_delivered_customer_date IS NOT NULL 
	AND order_estimated_delivery_date IS NOT NULL;

--- Relación entre Precio y Retraso de la Entrega

SELECT  o.order_id, 
        o.order_delivered_customer_date, 
        o.order_estimated_delivery_date, 
        oi.price
FROM olist_orders o
JOIN olist_order_items oi ON o.order_id = oi.order_id
WHERE o.order_delivered_customer_date IS NOT NULL;

   
-- 4) Tabla olist_order_items: Detalles de los artículos de cada pedido.

--- Envió y Precio del Producto
SELECT 
    shipping_limit_date as fecha_envío, 
    price as precio_producto 
FROM 
    olist_order_items;
   
--- Relación entre Año y Venta de Producto por Semestre.

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

-- 5) Tabla olist_products: Información de los productos.
   
   select distinct 
   product_category_name As categoria_producto,
   count(product_id) as cnt_productos
   media product_weight_g 
   from olist_products op
  where product_category_name is not null
 group by 1
order by cnt_productos desc;


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

   
-- 6) Tabla olist_sellers: Información sobre los vendedores.

--- Vendedores por ciudad 

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
   

-- 7) Tabla olist_order_payments: Información de pagos.

--- Pagos diferenciados por metodos pago.
SELECT DISTINCT 
	payment_type AS metodo_pago,
	ROUND(SUM(payment_value)) AS valor_pagos
FROM 
	olist_order_payments
WHERE 
	payment_type <> 'not_defined'
GROUP BY 
	metodo_pago;

----Pagos Tarjeta Credito vs Numero de cuotas
   
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
    porcentaje DESC;

---- Métodos de Pago y Retrasos de Entrega
SELECT p.payment_type,
       o.order_delivered_customer_date, 
       o.order_estimated_delivery_date
FROM olist_order_payments p
JOIN olist_orders o ON p.order_id = o.order_id
WHERE o.order_delivered_customer_date IS NOT NULL;


-- 8) Tabla olist_order_reviews: Reseñas de los pedidos.
--- Clasificacion de pedidos
SELECT 
    review_score as Calificacion,
    COUNT(review_id) AS Cantidad,
    ROUND(COUNT(review_id) * 100.0 / (SELECT COUNT(*) FROM olist_order_reviews)) AS Porcentaje
FROM 
    olist_order_reviews
GROUP BY 
    review_score
ORDER BY 
    review_score;      

dos.
   
   
-- Union de variables   


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
    o.order_delivered_customer_date IS NOT NULL;

"""
Descripción de las Variables

- order_id: Identificador único de cada pedido.
- order_delivered_customer_date: Fecha y hora en que el pedido fue entregado al cliente.
- order_estimated_delivery_date: Fecha estimada para la entrega del pedido según la plataforma.
- customer_zip: Código postal del cliente.
- seller_zip: Código postal del vendedor.
- distancia: Distancia entre el cliente y el vendedor en metros, calculada a partir de las coordenadas geográficas.
- review_score: Calificación otorgada por el cliente en una escala de 1 a 5.
- payment_type: Método de pago utilizado por el cliente (tarjeta de crédito, boleto, etc.).
- price: Precio del producto.
- delivery_delay: Diferencia en días entre la fecha de entrega real y la fecha estimada (negativo si se entregó antes).
"""

--- Consulta Calculo Distancia


SELECT o.order_id, o.order_delivered_customer_date, o.order_estimated_delivery_date, 
       c.customer_zip_code_prefix AS customer_zip, 
       s.seller_zip_code_prefix AS seller_zip,
       ST_Distance(c.location, s.location) AS distancia
FROM olist_orders o
JOIN olist_order_customers c ON o.customer_id = c.customer_id
JOIN olist_order_items oi ON o.order_id = oi.order_id
JOIN olist_sellers s ON oi.seller_id = s.seller_id
WHERE o.order_delivered_customer_date IS NOT NULL;


   
UPDATE public.olist_geolocation g
SET geom = ST_SetSRID(ST_MakePoint(tzc.most_frequent_lng, tzc.most_frequent_lat), 4326)
FROM temp_zip_code_coor tzc
WHERE g.zip_code_prefix = tzc.zip_code_prefix
RETURNING *;

-- Crear vista 

CREATE VIEW olist_ecommerce AS
SELECT 
    o.order_id,                             -- ID del pedido
    o.order_status,                         -- Estado del pedido
    o.order_purchase_timestamp,             -- Fecha de compra
    o.order_approved_at,                    -- Fecha de aprobación
    o.order_delivered_carrier_date,         -- Fecha de entrega al transportista
    o.order_delivered_customer_date,        -- Fecha de entrega al cliente
    o.order_estimated_delivery_date,        -- Fecha estimada de entrega
    c.customer_id,                          -- ID del cliente
    c.customer_zip_code_prefix,             -- Código postal del cliente
    s.seller_id,                            -- ID del vendedor
    s.seller_zip_code_prefix,               -- Código postal del vendedor
    oi.product_id,                          -- ID del producto
    oi.price,                               -- Precio del producto
    oi.freight_value,                       -- Valor del flete
    r.review_score,                         -- Puntuación de la reseña
    p.payment_type,                         -- Tipo de pago
    p.payment_installments,                 -- Número de cuotas
    p.payment_value,                        -- Valor del pago
    op.product_category_name,               -- Categoría del producto
    og.geolocation_lat,                     -- Latitud geográfica
    og.geolocation_lng                      -- Longitud geográfica
FROM
    olist_orders o
JOIN 
    olist_order_customers c ON o.customer_id = c.customer_id
JOIN 
    olist_order_items oi ON o.order_id = oi.order_id
JOIN 
    olist_products op ON oi.product_id = op.product_id 
JOIN 
    olist_sellers s ON oi.seller_id = s.seller_id
JOIN 
    olist_order_reviews r ON o.order_id = r.order_id
JOIN 
    olist_order_payments p ON o.order_id = p.order_id
JOIN 
    olist_geolocation og ON s.seller_zip_code_prefix = og.zip_code_prefix
WHERE
    c.customer_zip_code_prefix = og.zip_code_prefix AND
    o.order_delivered_customer_date IS NOT NULL;