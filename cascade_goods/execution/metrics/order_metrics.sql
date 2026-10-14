-- SQLite.
-- UTC placement dates: inclusive start, exclusive end. Refunded purchases count.
SELECT COUNT(DISTINCT o.order_id) AS completed_orders,
    COUNT(DISTINCT o.customer_id) AS purchasing_customers,
    CASE WHEN COUNT(o.adjusted_revenue) = COUNT(o.order_id)
         THEN 1.0 * SUM(o.adjusted_revenue) / NULLIF(COUNT(o.order_id), 0)
         ELSE NULL
    END AS net_average_order_value
FROM orders AS o
JOIN customers AS c ON o.customer_id = c.customer_id
WHERE o.order_status = 'Completed'
  AND lower(trim(CAST(c.is_test_account AS TEXT))) IN ('false', '0')
  AND c.email_domain IS NOT NULL
  AND lower(trim(c.email_domain)) NOT IN ('cascadegoods.com', 'qa.cascadegoods.test')
  AND o.order_date >= :start_date
  AND o.order_date < :end_date;
