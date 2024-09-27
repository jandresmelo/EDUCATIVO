--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

-- Started on 2024-09-27 16:32:34

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4296 (class 1262 OID 252030)
-- Name: olist_ecommerce; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE olist_ecommerce WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Colombia.1252';


ALTER DATABASE olist_ecommerce OWNER TO postgres;

\connect olist_ecommerce

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 226 (class 1259 OID 253270)
-- Name: olist_geolocation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.olist_geolocation (
    geolocation_id integer NOT NULL,
    zip_code_prefix integer,
    geolocation_lat double precision,
    geolocation_lng double precision,
    geolocation_city character varying,
    geolocation_state character varying,
    geom public.geography(Point,4326)
);


ALTER TABLE public.olist_geolocation OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 253262)
-- Name: olist_order_customers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.olist_order_customers (
    customer_id character varying NOT NULL,
    customer_unique_id character varying,
    customer_zip_code_prefix integer,
    customer_city character varying,
    customer_state character varying,
    location public.geography(Point,4326)
);


ALTER TABLE public.olist_order_customers OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 253305)
-- Name: olist_order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.olist_order_items (
    order_item_id integer NOT NULL,
    order_id character varying NOT NULL,
    product_id character varying NOT NULL,
    seller_id character varying,
    shipping_limit_date timestamp without time zone,
    price double precision,
    freight_value double precision
);


ALTER TABLE public.olist_order_items OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 253331)
-- Name: olist_order_payments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.olist_order_payments (
    payment_id integer NOT NULL,
    order_id character varying,
    payment_sequential integer,
    payment_type character varying,
    payment_installments integer,
    payment_value double precision
);


ALTER TABLE public.olist_order_payments OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 253344)
-- Name: olist_order_reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.olist_order_reviews (
    review_id character varying NOT NULL,
    order_id character varying,
    review_score integer,
    review_comment_title character varying,
    review_comment_message text,
    review_creation_date timestamp without time zone,
    review_answer_timestamp timestamp without time zone
);


ALTER TABLE public.olist_order_reviews OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 253292)
-- Name: olist_orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.olist_orders (
    order_id character varying NOT NULL,
    customer_id character varying,
    order_status character varying,
    order_purchase_timestamp timestamp without time zone,
    order_approved_at timestamp without time zone,
    order_delivered_carrier_date timestamp without time zone,
    order_delivered_customer_date timestamp without time zone,
    order_estimated_delivery_date timestamp without time zone
);


ALTER TABLE public.olist_orders OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 253285)
-- Name: olist_products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.olist_products (
    product_id character varying NOT NULL,
    product_category_name character varying,
    product_name_lenght integer,
    product_description_lenght integer,
    product_photos_qty integer,
    product_weight_g integer,
    product_length_cm integer,
    product_height_cm integer,
    product_width_cm integer
);


ALTER TABLE public.olist_products OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 253278)
-- Name: olist_sellers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.olist_sellers (
    seller_id character varying NOT NULL,
    seller_zip_code_prefix integer,
    seller_city character varying,
    seller_state character varying,
    location public.geography(Point,4326)
);


ALTER TABLE public.olist_sellers OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 255651)
-- Name: olist_ecommerce; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.olist_ecommerce AS
 SELECT o.order_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    c.customer_id,
    c.customer_zip_code_prefix,
    s.seller_id,
    s.seller_zip_code_prefix,
    oi.product_id,
    oi.price,
    oi.freight_value,
    r.review_score,
    p.payment_type,
    p.payment_installments,
    p.payment_value,
    op.product_category_name,
    og.geolocation_lat,
    og.geolocation_lng
   FROM (((((((public.olist_orders o
     JOIN public.olist_order_customers c ON (((o.customer_id)::text = (c.customer_id)::text)))
     JOIN public.olist_order_items oi ON (((o.order_id)::text = (oi.order_id)::text)))
     JOIN public.olist_products op ON (((oi.product_id)::text = (op.product_id)::text)))
     JOIN public.olist_sellers s ON (((oi.seller_id)::text = (s.seller_id)::text)))
     JOIN public.olist_order_reviews r ON (((o.order_id)::text = (r.order_id)::text)))
     JOIN public.olist_order_payments p ON (((o.order_id)::text = (p.order_id)::text)))
     JOIN public.olist_geolocation og ON ((s.seller_zip_code_prefix = og.zip_code_prefix)))
  WHERE ((c.customer_zip_code_prefix = og.zip_code_prefix) AND (o.order_delivered_customer_date IS NOT NULL));


ALTER TABLE public.olist_ecommerce OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 253269)
-- Name: olist_geolocation_geolocation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.olist_geolocation_geolocation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.olist_geolocation_geolocation_id_seq OWNER TO postgres;

--
-- TOC entry 4297 (class 0 OID 0)
-- Dependencies: 225
-- Name: olist_geolocation_geolocation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.olist_geolocation_geolocation_id_seq OWNED BY public.olist_geolocation.geolocation_id;


--
-- TOC entry 230 (class 1259 OID 253304)
-- Name: olist_order_items_order_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.olist_order_items_order_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.olist_order_items_order_item_id_seq OWNER TO postgres;

--
-- TOC entry 4298 (class 0 OID 0)
-- Dependencies: 230
-- Name: olist_order_items_order_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.olist_order_items_order_item_id_seq OWNED BY public.olist_order_items.order_item_id;


--
-- TOC entry 232 (class 1259 OID 253330)
-- Name: olist_order_payments_payment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.olist_order_payments_payment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.olist_order_payments_payment_id_seq OWNER TO postgres;

--
-- TOC entry 4299 (class 0 OID 0)
-- Dependencies: 232
-- Name: olist_order_payments_payment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.olist_order_payments_payment_id_seq OWNED BY public.olist_order_payments.payment_id;


--
-- TOC entry 235 (class 1259 OID 253356)
-- Name: product_category_name_translation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_category_name_translation (
    product_category_name character varying NOT NULL,
    product_category_name_english character varying
);


ALTER TABLE public.product_category_name_translation OWNER TO postgres;

--
-- TOC entry 4116 (class 2604 OID 253273)
-- Name: olist_geolocation geolocation_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_geolocation ALTER COLUMN geolocation_id SET DEFAULT nextval('public.olist_geolocation_geolocation_id_seq'::regclass);


--
-- TOC entry 4117 (class 2604 OID 253308)
-- Name: olist_order_items order_item_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_order_items ALTER COLUMN order_item_id SET DEFAULT nextval('public.olist_order_items_order_item_id_seq'::regclass);


--
-- TOC entry 4118 (class 2604 OID 253334)
-- Name: olist_order_payments payment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_order_payments ALTER COLUMN payment_id SET DEFAULT nextval('public.olist_order_payments_payment_id_seq'::regclass);


--
-- TOC entry 4122 (class 2606 OID 253277)
-- Name: olist_geolocation olist_geolocation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_geolocation
    ADD CONSTRAINT olist_geolocation_pkey PRIMARY KEY (geolocation_id);


--
-- TOC entry 4120 (class 2606 OID 253268)
-- Name: olist_order_customers olist_order_customers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_order_customers
    ADD CONSTRAINT olist_order_customers_pkey PRIMARY KEY (customer_id);


--
-- TOC entry 4130 (class 2606 OID 253329)
-- Name: olist_order_items olist_order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_order_items
    ADD CONSTRAINT olist_order_items_pkey PRIMARY KEY (order_id, order_item_id, product_id);


--
-- TOC entry 4132 (class 2606 OID 253338)
-- Name: olist_order_payments olist_order_payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_order_payments
    ADD CONSTRAINT olist_order_payments_pkey PRIMARY KEY (payment_id);


--
-- TOC entry 4134 (class 2606 OID 253350)
-- Name: olist_order_reviews olist_order_reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_order_reviews
    ADD CONSTRAINT olist_order_reviews_pkey PRIMARY KEY (review_id);


--
-- TOC entry 4128 (class 2606 OID 253298)
-- Name: olist_orders olist_orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_orders
    ADD CONSTRAINT olist_orders_pkey PRIMARY KEY (order_id);


--
-- TOC entry 4126 (class 2606 OID 253291)
-- Name: olist_products olist_products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_products
    ADD CONSTRAINT olist_products_pkey PRIMARY KEY (product_id);


--
-- TOC entry 4124 (class 2606 OID 253284)
-- Name: olist_sellers olist_sellers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_sellers
    ADD CONSTRAINT olist_sellers_pkey PRIMARY KEY (seller_id);


--
-- TOC entry 4136 (class 2606 OID 253362)
-- Name: product_category_name_translation product_category_name_translation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_category_name_translation
    ADD CONSTRAINT product_category_name_translation_pkey PRIMARY KEY (product_category_name);


--
-- TOC entry 4138 (class 2606 OID 253313)
-- Name: olist_order_items olist_order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_order_items
    ADD CONSTRAINT olist_order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.olist_orders(order_id);


--
-- TOC entry 4139 (class 2606 OID 253318)
-- Name: olist_order_items olist_order_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_order_items
    ADD CONSTRAINT olist_order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.olist_products(product_id);


--
-- TOC entry 4140 (class 2606 OID 253323)
-- Name: olist_order_items olist_order_items_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_order_items
    ADD CONSTRAINT olist_order_items_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.olist_sellers(seller_id);


--
-- TOC entry 4141 (class 2606 OID 253339)
-- Name: olist_order_payments olist_order_payments_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_order_payments
    ADD CONSTRAINT olist_order_payments_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.olist_orders(order_id);


--
-- TOC entry 4142 (class 2606 OID 253351)
-- Name: olist_order_reviews olist_order_reviews_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_order_reviews
    ADD CONSTRAINT olist_order_reviews_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.olist_orders(order_id);


--
-- TOC entry 4137 (class 2606 OID 253299)
-- Name: olist_orders olist_orders_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.olist_orders
    ADD CONSTRAINT olist_orders_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.olist_order_customers(customer_id);


-- Completed on 2024-09-27 16:32:34

--
-- PostgreSQL database dump complete
--

