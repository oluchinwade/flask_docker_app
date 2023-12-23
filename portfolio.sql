-- kill other connections
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'e_commerce' AND pid <> pg_backend_pid();

-- (re)create the database
DROP DATABASE IF EXISTS e_commerce;
CREATE DATABASE e_commerce;

-- connecting via psql
\c e_commerce

-- database configuration
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE vendors(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
);

CREATE TABLE products(
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    description TEXT,
    amount INT NOT NULL,
    vendor_id INT,
    CONSTRAINT fk_vendors_products
    FOREIGN KEY (vendor_id)
    REFERENCES vendors (id)
);

CREATE TABLE orders(
    id SERIAL PRIMARY KEY,
    amount INT NOT NULL,
    date_time TIMESTAMP,
    user_id INT,
    CONSTRAINT fk_users_orders
    FOREIGN KEY (user_id)
    REFERENCES users (id)
);

CREATE TABLE product_order(
    product_id INT,
    order_id INT,
    amount INT NOT NULL,
    date_time TIMESTAMP,
    PRIMARY KEY (product_id, order_id)
    CONSTRAINT fk_products_orders
        FOREIGN KEY (product_id)
        REFERENCES products (id),
    CONSTRAINT fk_orders_products
        FOREIGN KEY (order_id)
        REFERENCES orders (id)
);