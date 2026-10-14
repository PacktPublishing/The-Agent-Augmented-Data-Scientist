-- SQLite.
-- UTC placement dates: inclusive start, exclusive end. Returned units count.
WITH qualifying_orders AS (
    SELECT o.order_id
    FROM orders AS o
    JOIN customers AS c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'Completed'
      AND lower(trim(CAST(c.is_test_account AS TEXT))) IN ('false', '0')
      AND c.email_domain IS NOT NULL
      AND lower(trim(c.email_domain)) NOT IN ('cascadegoods.com', 'qa.cascadegoods.test')
      AND o.order_date >= :start_date
      AND o.order_date < :end_date
),
units_by_order AS (
    SELECT i.order_id, SUM(i.quantity) AS purchased_units
    FROM order_items AS i
    JOIN qualifying_orders AS o ON i.order_id = o.order_id
    GROUP BY i.order_id
)
SELECT CASE WHEN COUNT(u.order_id) = COUNT(o.order_id)
            THEN 1.0 * SUM(u.purchased_units) / NULLIF(COUNT(o.order_id), 0)
            ELSE NULL
       END AS units_per_transaction
FROM qualifying_orders AS o
LEFT JOIN units_by_order AS u ON o.order_id = u.order_id;
