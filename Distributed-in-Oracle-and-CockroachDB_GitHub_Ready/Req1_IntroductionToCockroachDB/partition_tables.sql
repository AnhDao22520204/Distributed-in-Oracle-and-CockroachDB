USE ecommerce;

-- Logical partition ranges used by the project:
-- 1..33, 34..66, 67..100.
-- Run only when your CockroachDB version/edition supports this syntax.

ALTER TABLE inventory ALTER PRIMARY KEY USING COLUMNS (store_id, id);
ALTER INDEX inventory@primary PARTITION BY RANGE (store_id) (
    PARTITION p1 VALUES FROM (1) TO (34),
    PARTITION p2 VALUES FROM (34) TO (67),
    PARTITION p3 VALUES FROM (67) TO (101)
);

ALTER TABLE invoices ALTER PRIMARY KEY USING COLUMNS (store_id, id);
ALTER INDEX invoices@primary PARTITION BY RANGE (store_id) (
    PARTITION p1 VALUES FROM (1) TO (34),
    PARTITION p2 VALUES FROM (34) TO (67),
    PARTITION p3 VALUES FROM (67) TO (101)
);

ALTER TABLE payments ALTER PRIMARY KEY USING COLUMNS (invoice_id, id);
ALTER INDEX payments@primary PARTITION BY RANGE (invoice_id) (
    PARTITION p1 VALUES FROM (1) TO (333334),
    PARTITION p2 VALUES FROM (333334) TO (666667),
    PARTITION p3 VALUES FROM (666667) TO (1000001)
);

-- Zone/locality constraints are intentionally not hard-coded because
-- node attributes differ between deployments.
