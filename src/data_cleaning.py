import pandas as pd


REQUIRED_COLUMNS = [
    "InvoiceNo", "StockCode", "Description", "Quantity",
    "InvoiceDate", "UnitPrice", "CustomerID", "Country"
]


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply documented, reproducible cleaning and feature creation."""
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {missing_columns}")

    result = df.copy()
    result = result.drop_duplicates()
    result = result.dropna(subset=["Description"])

    result["InvoiceNo"] = result["InvoiceNo"].astype(str).str.strip()
    result["StockCode"] = result["StockCode"].astype(str).str.strip()
    result["Description"] = result["Description"].astype(str).str.strip()
    result["Country"] = result["Country"].astype(str).str.strip()
    result["InvoiceDate"] = pd.to_datetime(result["InvoiceDate"], errors="coerce")
    result["Quantity"] = pd.to_numeric(result["Quantity"], errors="coerce")
    result["UnitPrice"] = pd.to_numeric(result["UnitPrice"], errors="coerce")
    result["CustomerID"] = pd.to_numeric(result["CustomerID"], errors="coerce").astype("Int64")

    result = result.dropna(subset=["InvoiceDate", "Quantity", "UnitPrice"])
    result = result[result["Description"].ne("")].copy()

    result["IsCancellation"] = result["InvoiceNo"].str.upper().str.startswith("C")
    result["SalesAmount"] = result["Quantity"] * result["UnitPrice"]
    result["InvoiceMonth"] = result["InvoiceDate"].dt.to_period("M").astype(str)
    result["InvoiceHour"] = result["InvoiceDate"].dt.hour
    result["IsReturnOrNegativeQuantity"] = result["Quantity"] < 0
    result["IsNonPositivePrice"] = result["UnitPrice"] <= 0

    return result.reset_index(drop=True)


if __name__ == "__main__":
    from src.data_loader import load_raw_data, PROCESSED_DATA_PATH

    raw = load_raw_data()
    cleaned = clean_data(raw)
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Raw rows: {len(raw):,}")
    print(f"Cleaned rows: {len(cleaned):,}")
    print(f"Exact duplicates removed: {len(raw) - raw.drop_duplicates().shape[0]:,}")
    print(f"Missing CustomerID: {cleaned['CustomerID'].isna().sum():,}")
    print(f"Cancellation lines: {cleaned['IsCancellation'].sum():,}")
    print(f"Saved to: {PROCESSED_DATA_PATH}")
