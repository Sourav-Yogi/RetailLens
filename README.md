# RetailLens — Customer & Sales Intelligence Platform

RetailLens is a compact analytics and machine-learning project using the UCI Online Retail dataset. It provides sales KPIs, product/country analysis, return visibility, and customer segmentation using RFM features and K-Means.

## Features
- Data cleaning and feature creation with Pandas
- Sales analysis by month, product, and country
- Customer RFM (Recency, Frequency, Monetary) features
- K-Means customer segmentation with silhouette score
- Interactive Streamlit and Plotly dashboard
- Optional PostgreSQL loading and SQL analysis queries
- Basic automated tests with pytest

## Dataset
Download `Online Retail.xlsx` from the [UCI Online Retail dataset](https://archive.ics.uci.edu/dataset/352/online+retail) and place it at `data/raw/Online Retail.xlsx`. Do not commit the dataset to GitHub.

## Setup with uv
```bash
uv sync
```

If you have not initialized uv in this folder yet:
```bash
uv init --bare --name retaillens
uv add pandas numpy openpyxl scikit-learn streamlit plotly sqlalchemy psycopg2-binary python-dotenv
uv add --dev pytest
```

## Run the dashboard
```bash
uv run streamlit run app.py
```

The first run reads the Excel workbook, cleans it, and saves `data/processed/cleaned_retail.csv`. Later runs load the processed CSV.

## Run tests
```bash
uv run pytest
```

## Optional PostgreSQL
1. Create a PostgreSQL database.
2. Copy `.env.example` to `.env` and set `DATABASE_URL`.
3. Load the processed data:
   ```bash
   uv run python src/load_to_postgres.py
   ```
4. Use `database/analysis_queries.sql` for sample queries.

## Metric definitions
- Gross sales: positive-quantity and positive-price lines excluding invoices whose invoice number starts with `C`.
- Gross sales are not profit or net revenue.
- Customer segmentation uses only rows with a known CustomerID.
- Returns and cancellation-related records are retained in the cleaned dataset for transparency, but excluded from the gross-sales KPI.
