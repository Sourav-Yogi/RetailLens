-- 1. Gross sales by month (excludes cancellations, returns and non-positive prices)
SELECT invoice_month, SUM(sales_amount) AS gross_sales
FROM retail_transactions
WHERE NOT is_cancellation
  AND quantity > 0
  AND unit_price > 0
GROUP BY invoice_month
ORDER BY invoice_month;

-- 2. Top products by gross sales
SELECT description, SUM(sales_amount) AS gross_sales, SUM(quantity) AS units_sold
FROM retail_transactions
WHERE NOT is_cancellation
  AND quantity > 0
  AND unit_price > 0
GROUP BY description
ORDER BY gross_sales DESC
LIMIT 10;

-- 3. Country-level gross sales
SELECT country, SUM(sales_amount) AS gross_sales
FROM retail_transactions
WHERE NOT is_cancellation
  AND quantity > 0
  AND unit_price > 0
GROUP BY country
ORDER BY gross_sales DESC;

-- 4. Number of transactions with missing customer IDs
SELECT COUNT(*) AS rows_without_customer_id
FROM retail_transactions
WHERE customer_id IS NULL;
