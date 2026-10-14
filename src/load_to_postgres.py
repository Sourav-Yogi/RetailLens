"""Optional utility: load cleaned CSV into PostgreSQL using DATABASE_URL from .env."""
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from src.data_loader import PROCESSED_DATA_PATH, load_or_prepare_data

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def main():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise SystemExit("Set DATABASE_URL in .env before loading to PostgreSQL.")

    df = load_or_prepare_data()
    export = df.rename(columns={
        "InvoiceNo": "invoice_no", "StockCode": "stock_code",
        "Description": "description", "Quantity": "quantity",
        "InvoiceDate": "invoice_date", "UnitPrice": "unit_price",
        "CustomerID": "customer_id", "Country": "country",
        "IsCancellation": "is_cancellation", "SalesAmount": "sales_amount",
        "InvoiceMonth": "invoice_month", "InvoiceHour": "invoice_hour",
        "IsReturnOrNegativeQuantity": "is_return_or_negative_quantity",
        "IsNonPositivePrice": "is_nonpositive_price",
    })
    engine = create_engine(database_url)
    export.to_sql("retail_transactions", engine, if_exists="replace", index=False, chunksize=5000, method="multi")
    print(f"Loaded {len(export):,} rows into retail_transactions.")


if __name__ == "__main__":
    main()
