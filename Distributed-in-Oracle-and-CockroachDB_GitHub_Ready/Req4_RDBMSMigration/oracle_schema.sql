CREATE TABLE stores (
    store_id NUMBER PRIMARY KEY,
    store_name VARCHAR2(100) NOT NULL,
    address VARCHAR2(200) NOT NULL,
    city VARCHAR2(50) NOT NULL,
    state VARCHAR2(50) NOT NULL,
    zip_code VARCHAR2(20) NOT NULL,
    phone VARCHAR2(20),
    opening_date DATE NOT NULL,
    status VARCHAR2(20) DEFAULT 'ACTIVE' NOT NULL
);

CREATE TABLE category (
    category_id NUMBER PRIMARY KEY,
    category_name VARCHAR2(50) NOT NULL,
    description VARCHAR2(200),
    status VARCHAR2(20) DEFAULT 'ACTIVE' NOT NULL
);

CREATE TABLE supplier (
    supplier_id NUMBER PRIMARY KEY,
    supplier_name VARCHAR2(100) NOT NULL,
    contact_name VARCHAR2(100),
    email VARCHAR2(100),
    phone VARCHAR2(20),
    address VARCHAR2(200),
    city VARCHAR2(50),
    state VARCHAR2(50),
    zip_code VARCHAR2(20),
    status VARCHAR2(20) DEFAULT 'ACTIVE' NOT NULL
);

CREATE TABLE product_base (
    product_id NUMBER PRIMARY KEY,
    product_name VARCHAR2(100) NOT NULL,
    category_id NUMBER NOT NULL REFERENCES category(category_id),
    supplier_id NUMBER NOT NULL REFERENCES supplier(supplier_id),
    unit_price NUMBER(10,2) NOT NULL,
    status VARCHAR2(20) DEFAULT 'ACTIVE' NOT NULL
);

CREATE TABLE product_extra (
    product_id NUMBER PRIMARY KEY REFERENCES product_base(product_id),
    description VARCHAR2(200),
    manufacturer VARCHAR2(100),
    warranty_period VARCHAR2(50),
    origin_country VARCHAR2(50),
    created_date DATE DEFAULT SYSDATE NOT NULL,
    last_updated DATE DEFAULT SYSDATE NOT NULL
);

CREATE TABLE customer_base (
    customer_id NUMBER PRIMARY KEY,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    email VARCHAR2(100) UNIQUE,
    phone VARCHAR2(20),
    registration_date DATE DEFAULT SYSDATE NOT NULL,
    status VARCHAR2(20) DEFAULT 'ACTIVE' NOT NULL
);

CREATE TABLE customer_extra (
    customer_id NUMBER PRIMARY KEY REFERENCES customer_base(customer_id),
    address VARCHAR2(200),
    city VARCHAR2(50),
    state VARCHAR2(50),
    zip_code VARCHAR2(20),
    loyalty_points NUMBER DEFAULT 0 NOT NULL,
    last_purchase_date DATE
);

CREATE TABLE employee (
    employee_id NUMBER PRIMARY KEY,
    store_id NUMBER NOT NULL REFERENCES stores(store_id),
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    position VARCHAR2(50) NOT NULL,
    hire_date DATE NOT NULL,
    salary NUMBER(10,2) NOT NULL,
    email VARCHAR2(100),
    phone VARCHAR2(20),
    status VARCHAR2(20) DEFAULT 'ACTIVE' NOT NULL
);

CREATE TABLE inventory (
    inventory_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    store_id NUMBER NOT NULL REFERENCES stores(store_id),
    product_id NUMBER NOT NULL REFERENCES product_base(product_id),
    quantity NUMBER NOT NULL CHECK (quantity >= 0),
    last_updated DATE DEFAULT SYSDATE NOT NULL
);

CREATE TABLE invoice (
    invoice_id NUMBER PRIMARY KEY,
    store_id NUMBER NOT NULL REFERENCES stores(store_id),
    customer_id NUMBER NOT NULL REFERENCES customer_base(customer_id),
    employee_id NUMBER NOT NULL REFERENCES employee(employee_id),
    invoice_date DATE DEFAULT SYSDATE NOT NULL,
    total_amount NUMBER(12,2) NOT NULL,
    status VARCHAR2(20) DEFAULT 'COMPLETED' NOT NULL
);

CREATE TABLE invoice_detail (
    detail_id NUMBER PRIMARY KEY,
    invoice_id NUMBER NOT NULL REFERENCES invoice(invoice_id),
    product_id NUMBER NOT NULL REFERENCES product_base(product_id),
    quantity NUMBER NOT NULL CHECK (quantity > 0),
    unit_price NUMBER(10,2) NOT NULL
);

CREATE TABLE salary (
    salary_id NUMBER PRIMARY KEY,
    employee_id NUMBER NOT NULL REFERENCES employee(employee_id),
    store_id NUMBER NOT NULL REFERENCES stores(store_id),
    base_salary NUMBER(10,2) NOT NULL,
    bonus NUMBER(10,2) DEFAULT 0 NOT NULL,
    payment_date DATE NOT NULL
);

CREATE TABLE payment (
    payment_id NUMBER PRIMARY KEY,
    invoice_id NUMBER NOT NULL REFERENCES invoice(invoice_id),
    payment_date DATE DEFAULT SYSDATE NOT NULL,
    amount NUMBER(12,2) NOT NULL,
    payment_method VARCHAR2(20) NOT NULL,
    status VARCHAR2(20) DEFAULT 'COMPLETED' NOT NULL
);
