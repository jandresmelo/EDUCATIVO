
-- CREAR BASE DE DATOS 
--- Brazilian E-Commerce Public Dataset by Olist
--- https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

-- Crear base de datos en shell
--- CREATE DATABASE olist_ecommerce;
--- \c olist_ecommerce
--- CREATE EXTENSION postgis;

-- 1) Crear Tablas
--- Tabla de clientes
CREATE TABLE public.olist_order_customers (
	customer_id varchar NOT NULL,
	customer_unique_id varchar NULL,
	customer_zip_code_prefix int4 NULL,
	customer_city varchar NULL,
	customer_state varchar NULL,
	"location" public.geography(point, 4326) NULL,
	CONSTRAINT olist_order_customers_pkey PRIMARY KEY (customer_id)
);

ALTER TABLE public.olist_order_customers OWNER TO postgres;
GRANT ALL ON TABLE public.olist_order_customers TO postgres;

--- Tabla de geolocalización
CREATE TABLE public.olist_geolocation (
	geolocation_id serial4 NOT NULL,
	zip_code_prefix int4 NULL,
	geolocation_lat float8 NULL,
	geolocation_lng float8 NULL,
	geolocation_city varchar NULL,
	geolocation_state varchar NULL,
	geom public.geography(point, 4326) NULL,
	CONSTRAINT olist_geolocation_pkey PRIMARY KEY (geolocation_id)
);

ALTER TABLE public.olist_geolocation OWNER TO postgres;
GRANT ALL ON TABLE public.olist_geolocation TO postgres;

--- Tabla de vendedores
CREATE TABLE public.olist_sellers (
	seller_id varchar NOT NULL,
	seller_zip_code_prefix int4 NULL,
	seller_city varchar NULL,
	seller_state varchar NULL,
	"location" public.geography(point, 4326) NULL,
	CONSTRAINT olist_sellers_pkey PRIMARY KEY (seller_id)
);

ALTER TABLE public.olist_sellers OWNER TO postgres;
GRANT ALL ON TABLE public.olist_sellers TO postgres;

--- Tabla de productos
CREATE TABLE public.olist_products (
	product_id varchar NOT NULL,
	product_category_name varchar NULL,
	product_name_lenght int4 NULL,
	product_description_lenght int4 NULL,
	product_photos_qty int4 NULL,
	product_weight_g int4 NULL,
	product_length_cm int4 NULL,
	product_height_cm int4 NULL,
	product_width_cm int4 NULL,
	CONSTRAINT olist_products_pkey PRIMARY KEY (product_id)
);

ALTER TABLE public.olist_products OWNER TO postgres;
GRANT ALL ON TABLE public.olist_products TO postgres;

--- Tabla de pedidos
CREATE TABLE public.olist_orders (
	order_id varchar NOT NULL,
	customer_id varchar NULL,
	order_status varchar NULL,
	order_purchase_timestamp timestamp NULL,
	order_approved_at timestamp NULL,
	order_delivered_carrier_date timestamp NULL,
	order_delivered_customer_date timestamp NULL,
	order_estimated_delivery_date timestamp NULL,
	CONSTRAINT olist_orders_pkey PRIMARY KEY (order_id)
);

ALTER TABLE public.olist_orders OWNER TO postgres;
GRANT ALL ON TABLE public.olist_orders TO postgres;

ALTER TABLE public.olist_orders ADD CONSTRAINT olist_orders_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.olist_order_customers(customer_id);

--- Tabla de items de pedido
CREATE TABLE public.olist_order_items (
	order_item_id serial4 NOT NULL,
	order_id varchar NOT NULL,
	product_id varchar NOT NULL,
	seller_id varchar NULL,
	shipping_limit_date timestamp NULL,
	price float8 NULL,
	freight_value float8 NULL,
	CONSTRAINT olist_order_items_pkey PRIMARY KEY (order_id, order_item_id, product_id)
);

ALTER TABLE olist_order_items DROP CONSTRAINT olist_order_items_pkey;
ALTER TABLE olist_order_items ADD PRIMARY KEY (order_id, order_item_id, product_id);

ALTER TABLE public.olist_order_items ADD CONSTRAINT olist_order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.olist_orders(order_id);
ALTER TABLE public.olist_order_items ADD CONSTRAINT olist_order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.olist_products(product_id);
ALTER TABLE public.olist_order_items ADD CONSTRAINT olist_order_items_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.olist_sellers(seller_id);


--- Tabla de pagos
CREATE TABLE public.olist_order_payments (
	payment_id serial4 NOT NULL,
	order_id varchar NULL,
	payment_sequential int4 NULL,
	payment_type varchar NULL,
	payment_installments int4 NULL,
	payment_value float8 NULL,
	CONSTRAINT olist_order_payments_pkey PRIMARY KEY (payment_id)
);

ALTER TABLE public.olist_order_payments OWNER TO postgres;
GRANT ALL ON TABLE public.olist_order_payments TO postgres;

ALTER TABLE public.olist_order_payments ADD CONSTRAINT olist_order_payments_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.olist_orders(order_id);


--- Tabla de reseñas
CREATE TABLE public.olist_order_reviews (
	review_id varchar NOT NULL,
	order_id varchar NULL,
	review_score int4 NULL,
	review_comment_title varchar NULL,
	review_comment_message text NULL,
	review_creation_date timestamp NULL,
	review_answer_timestamp timestamp NULL,
	CONSTRAINT olist_order_reviews_pkey PRIMARY KEY (review_id)
);

ALTER TABLE public.olist_order_reviews OWNER TO postgres;
GRANT ALL ON TABLE public.olist_order_reviews TO postgres;

ALTER TABLE public.olist_order_reviews ADD CONSTRAINT olist_order_reviews_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.olist_orders(order_id);

--- Tabla de traducciones de categorías de productos
CREATE TABLE public.product_category_name_translation (
	product_category_name varchar NOT NULL,
	product_category_name_english varchar NULL,
	CONSTRAINT product_category_name_translation_pkey PRIMARY KEY (product_category_name)
);


-- 2) Importar datos .csv con manejo para duplicados


--- 1. Importar tabla olist_order_customers - Registros: 99441
copy olist_order_customers(customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state) 
FROM 'D:\UCOMPENSAR\Datos\olist_customers_dataset.csv' DELIMITER ',' CSV HEADER;

--- 2. Importar tabla olist_geolocation - Registros: 1000163
copy olist_geolocation(zip_code_prefix, geolocation_lat, geolocation_lng, geolocation_city, geolocation_state) 
FROM 'D:\UCOMPENSAR\Datos\olist_geolocation_dataset.csv' DELIMITER ',' CSV HEADER;

--- 3. Importar tabla olist_sellers - Registros: 3095
copy olist_sellers(seller_id, seller_zip_code_prefix, seller_city, seller_state) 
FROM 'D:\UCOMPENSAR\Datos\olist_sellers_dataset.csv' DELIMITER ',' CSV HEADER;

--- 4. Importar tabla olist_products - Registros: 32951
copy olist_products(product_id, product_category_name, product_name_lenght, product_description_lenght, product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm) 
FROM 'D:\UCOMPENSAR\Datos\olist_products_dataset.csv' DELIMITER ',' CSV HEADER;

--- 5. Importar tabla olist_orders - Registros: 99441
copy olist_orders(order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date) 
FROM 'D:\UCOMPENSAR\Datos\olist_orders_dataset.csv' DELIMITER ',' CSV HEADER;

--- 6. Importar tabla olist_order_items - Registros: 112650
copy olist_order_items(order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value) 
FROM 'D:\UCOMPENSAR\Datos\olist_order_items_dataset.csv' DELIMITER ',' CSV HEADER;

--- 7. Importar tabla olist_order_payments - Registros: 103886
copy olist_order_payments(order_id, payment_sequential, payment_type, payment_installments, payment_value) 
FROM 'D:\UCOMPENSAR\Datos\olist_order_payments_dataset.csv' DELIMITER ',' CSV HEADER;

--- 8. Importar y manejar duplicados en olist_order_reviews
--- Crear una tabla temporal
CREATE TEMP TABLE temp_order_reviews AS 
SELECT * FROM olist_order_reviews WHERE false;

--- Importar los datos en la tabla temporal
copy temp_order_reviews FROM 'D:\UCOMPENSAR\Datos\olist_order_reviews_dataset.csv' DELIMITER ',' CSV HEADER;

--- Eliminar duplicados en la tabla temporal
DELETE FROM temp_order_reviews
WHERE ctid NOT IN (
    SELECT min(ctid)
    FROM temp_order_reviews
    GROUP BY review_id
);

--- Insertar los datos en la tabla final, manejando duplicados - Registros: 98410
INSERT INTO olist_order_reviews
SELECT * FROM temp_order_reviews
ON CONFLICT (review_id) DO NOTHING;

--- 9. Importar tabla product_category_name_translation - Registros: 71
copy product_category_name_translation(product_category_name, product_category_name_english) 
FROM 'D:\UCOMPENSAR\Datos\product_category_name_translation.csv' DELIMITER ',' CSV HEADER;

--- Cargue finalizado, calidad de la importación de datos

SELECT 
    relname AS table_name, 
    n_live_tup AS row_count
FROM 
    pg_stat_user_tables
ORDER BY 
    n_live_tup DESC;


-- 3) Asignar Coordenadas

--- Actualizar la columna geom



--- Crear tabla temporal
CREATE TEMP TABLE temp_zip_code_coor AS
SELECT 
    zip_code_prefix,
    MODE() WITHIN GROUP (ORDER BY geolocation_lat) AS most_frequent_lat,
    MODE() WITHIN GROUP (ORDER BY geolocation_lng) AS most_frequent_lng
FROM 
    public.olist_geolocation
GROUP BY 
    zip_code_prefix;

--- Agregar coordenadas

UPDATE public.olist_geolocation g
SET geom = ST_SetSRID(ST_MakePoint(tzc.most_frequent_lng, tzc.most_frequent_lat), 4326)
FROM temp_zip_code_coor tzc
WHERE g.zip_code_prefix = tzc.zip_code_prefix
RETURNING *;
UPDATE public.olist_order_customers c
SET location = ST_SetSRID(ST_MakePoint(tzc.most_frequent_lng, tzc.most_frequent_lat), 4326)
FROM temp_zip_code_coor tzc
WHERE c.customer_zip_code_prefix = tzc.zip_code_prefix
returning *;

UPDATE public.olist_sellers s
SET location = ST_SetSRID(ST_MakePoint(tzc.most_frequent_lng, tzc.most_frequent_lat), 4326)
FROM temp_zip_code_coor tzc
WHERE s.seller_zip_code_prefix = tzc.zip_code_prefix
RETURNING *;



