-- Optional PostgreSQL table for cleaned transaction records.
CREATE TABLE IF NOT EXISTS retail_transactions (
    invoice_no TEXT NOT NULL,
    stock_code TEXT NOT NULL,
    description TEXT,
    quantity INTEGER NOT NULL,
    invoice_date TIMESTAMP NOT NULL,
    unit_price NUMERIC(12, 4) NOT NULL,
    customer_id BIGINT,
    country TEXT NOT NULL,
    is_cancellation BOOLEAN NOT NULL,
    sales_amount NUMERIC(14, 4) NOT NULL,
    invoice_month TEXT NOT NULL,
    invoice_hour SMALLINT NOT NULL,
    is_return_or_negative_quantity BOOLEAN NOT NULL,
    is_nonpositive_price BOOLEAN NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_retail_invoice_date ON retail_transactions(invoice_date);
CREATE INDEX IF NOT EXISTS idx_retail_customer_id ON retail_transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_retail_country ON retail_transactions(country);
