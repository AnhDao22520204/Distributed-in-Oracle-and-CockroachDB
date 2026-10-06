CREATE TABLE IF NOT EXISTS stores (
    store_id INT PRIMARY KEY DEFAULT unique_rowid(),
    store_name VARCHAR(100) NOT NULL,
    address VARCHAR(200) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    phone VARCHAR(20),
    opening_date TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS category (
    category_id INT PRIMARY KEY DEFAULT unique_rowid(),
    category_name VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS supplier (
    supplier_id INT PRIMARY KEY DEFAULT unique_rowid(),
    supplier_name VARCHAR(100) NOT NULL,
    contact_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS product_base (
    product_id INT PRIMARY KEY DEFAULT unique_rowid(),
    product_name VARCHAR(100) NOT NULL,
    category_id INT NOT NULL REFERENCES category(category_id),
    supplier_id INT NOT NULL REFERENCES supplier(supplier_id),
    unit_price DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS product_extra (
    product_id INT PRIMARY KEY REFERENCES product_base(product_id),
    description VARCHAR(200),
    manufacturer VARCHAR(100),
    warranty_period VARCHAR(50),
    origin_country VARCHAR(50),
    created_date TIMESTAMP NOT NULL DEFAULT now(),
    last_updated TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS customer_base (
    customer_id INT PRIMARY KEY DEFAULT unique_rowid(),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    registration_date TIMESTAMP NOT NULL DEFAULT now(),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS customer_extra (
    customer_id INT PRIMARY KEY REFERENCES customer_base(customer_id),
    address VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    loyalty_points INT NOT NULL DEFAULT 0,
    last_purchase_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS employee (
    employee_id INT PRIMARY KEY DEFAULT unique_rowid(),
    store_id INT NOT NULL REFERENCES stores(store_id),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL,
    hire_date TIMESTAMP NOT NULL,
    salary DECIMAL(10,2) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INT PRIMARY KEY DEFAULT unique_rowid(),
    store_id INT NOT NULL REFERENCES stores(store_id),
    product_id INT NOT NULL REFERENCES product_base(product_id),
    quantity INT NOT NULL CHECK (quantity >= 0),
    last_updated TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS invoice (
    invoice_id INT PRIMARY KEY DEFAULT unique_rowid(),
    store_id INT NOT NULL REFERENCES stores(store_id),
    customer_id INT NOT NULL REFERENCES customer_base(customer_id),
    employee_id INT NOT NULL REFERENCES employee(employee_id),
    invoice_date TIMESTAMP NOT NULL DEFAULT now(),
    total_amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'COMPLETED'
);

CREATE TABLE IF NOT EXISTS invoice_detail (
    detail_id INT PRIMARY KEY DEFAULT unique_rowid(),
    invoice_id INT NOT NULL REFERENCES invoice(invoice_id),
    product_id INT NOT NULL REFERENCES product_base(product_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS salary (
    salary_id INT PRIMARY KEY DEFAULT unique_rowid(),
    employee_id INT NOT NULL REFERENCES employee(employee_id),
    store_id INT NOT NULL REFERENCES stores(store_id),
    base_salary DECIMAL(10,2) NOT NULL,
    bonus DECIMAL(10,2) NOT NULL DEFAULT 0,
    payment_date TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS payment (
    payment_id INT PRIMARY KEY DEFAULT unique_rowid(),
    invoice_id INT NOT NULL REFERENCES invoice(invoice_id),
    payment_date TIMESTAMP NOT NULL DEFAULT now(),
    amount DECIMAL(12,2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'COMPLETED'
);

CREATE INDEX IF NOT EXISTS idx_inventory_store_product
    ON inventory(store_id, product_id);
CREATE INDEX IF NOT EXISTS idx_invoice_store_date
    ON invoice(store_id, invoice_date);
CREATE INDEX IF NOT EXISTS idx_invoice_detail_invoice
    ON invoice_detail(invoice_id);
CREATE INDEX IF NOT EXISTS idx_payment_invoice
    ON payment(invoice_id);
