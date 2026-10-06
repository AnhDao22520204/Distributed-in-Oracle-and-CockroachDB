USE ecommerce;

INSERT INTO stores (id, name, address, city, country)
SELECT
    gs,
    'Store ' || gs::STRING,
    (100 + gs)::STRING || ' Nguyen Trai',
    (ARRAY['Ha Noi','TP.HCM','Da Nang','Hai Phong','Can Tho','Hue'])[((gs - 1) % 6) + 1],
    'Vietnam'
FROM generate_series(1, 100) AS t(gs)
ON CONFLICT (id) DO NOTHING;

INSERT INTO users (id, name, email, password)
SELECT
    gs,
    'User ' || gs::STRING,
    'user' || gs::STRING || '@example.com',
    md5(gs::STRING)
FROM generate_series(1, 10000) AS t(gs)
ON CONFLICT (id) DO NOTHING;

INSERT INTO products (id, name, price, store_id)
SELECT
    gs,
    'Product ' || gs::STRING,
    (100000 + (gs % 19900000))::DECIMAL(12,2),
    ((gs - 1) % 100) + 1
FROM generate_series(1, 10000) AS t(gs)
ON CONFLICT (id) DO NOTHING;

INSERT INTO inventory (id, store_id, product_id, quantity)
SELECT
    gs,
    ((gs - 1) % 100) + 1,
    gs,
    100 + (gs % 900)
FROM generate_series(1, 10000) AS t(gs)
ON CONFLICT (id) DO NOTHING;

INSERT INTO invoices
    (id, user_id, store_id, invoice_number, created_at, total_amount, status)
SELECT
    gs,
    ((gs - 1) % 10000) + 1,
    ((gs - 1) % 100) + 1,
    'INV-' || gs::STRING,
    now() - ((gs % 365)::STRING || ' days')::INTERVAL,
    (100000 + (gs % 19900000))::DECIMAL(14,2),
    'completed'
FROM generate_series(1, 1000000) AS t(gs)
ON CONFLICT (id) DO NOTHING;

INSERT INTO invoice_details
    (id, invoice_id, product_id, quantity, unit_price, total_price)
SELECT
    gs,
    ((gs - 1) % 1000000) + 1,
    ((gs - 1) % 10000) + 1,
    ((gs - 1) % 5) + 1,
    (100000 + (gs % 5000000))::DECIMAL(12,2),
    (((gs - 1) % 5) + 1) *
        (100000 + (gs % 5000000))::DECIMAL(12,2)
FROM generate_series(1, 3000000) AS t(gs)
ON CONFLICT (id) DO NOTHING;

INSERT INTO reviews
    (id, user_id, product_id, rating, comment, created_at)
SELECT
    gs,
    ((gs - 1) % 10000) + 1,
    ((gs - 1) % 10000) + 1,
    ((gs - 1) % 5) + 1,
    'Synthetic review ' || gs::STRING,
    now() - ((gs % 90)::STRING || ' days')::INTERVAL
FROM generate_series(1, 10000) AS t(gs)
ON CONFLICT (id) DO NOTHING;

INSERT INTO payments
    (id, invoice_id, amount, payment_date, status)
SELECT
    gs,
    gs,
    (100000 + (gs % 19900000))::DECIMAL(18,2),
    now() - ((gs % 365)::STRING || ' days')::INTERVAL,
    'completed'
FROM generate_series(1, 1000000) AS t(gs)
ON CONFLICT (id) DO NOTHING;
