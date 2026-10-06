CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

CREATE TABLE IF NOT EXISTS stores (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    store_id INT REFERENCES stores(id),
    stock_alert_threshold INT DEFAULT 10,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS inventory (
    id INT PRIMARY KEY,
    store_id INT NOT NULL REFERENCES stores(id),
    product_id INT NOT NULL REFERENCES products(id),
    quantity INT NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    last_updated TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS invoices (
    id INT PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    store_id INT NOT NULL REFERENCES stores(id),
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT now(),
    total_amount DECIMAL(14,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS invoice_details (
    id INT PRIMARY KEY,
    invoice_id INT NOT NULL REFERENCES invoices(id),
    product_id INT NOT NULL REFERENCES products(id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(12,2) NOT NULL,
    total_price DECIMAL(14,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS reviews (
    id INT PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    product_id INT NOT NULL REFERENCES products(id),
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment STRING,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS payments (
    id INT PRIMARY KEY,
    invoice_id INT NOT NULL REFERENCES invoices(id),
    amount DECIMAL(18,2) NOT NULL,
    payment_date TIMESTAMP DEFAULT now(),
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE INDEX IF NOT EXISTS idx_products_store ON products(store_id);
CREATE INDEX IF NOT EXISTS idx_inventory_store_product ON inventory(store_id, product_id);
CREATE INDEX IF NOT EXISTS idx_invoices_store_created ON invoices(store_id, created_at);
CREATE INDEX IF NOT EXISTS idx_invoice_details_invoice ON invoice_details(invoice_id);
CREATE INDEX IF NOT EXISTS idx_reviews_product_created ON reviews(product_id, created_at);
CREATE INDEX IF NOT EXISTS idx_payments_invoice ON payments(invoice_id);
