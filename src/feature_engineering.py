import pandas as pd
from src.sales_analysis import eligible_sales


def build_rfm_features(df: pd.DataFrame) -> pd.DataFrame:
    """Build Recency, Frequency and Monetary values for identifiable customers."""
    sales = eligible_sales(df)
    sales = sales.dropna(subset=["CustomerID"]).copy()
    if sales.empty:
        raise ValueError("No identifiable customers remain for RFM analysis.")

    sales["CustomerID"] = sales["CustomerID"].astype("int64")
    snapshot_date = sales["InvoiceDate"].max().normalize() + pd.Timedelta(days=1)

    rfm = (
        sales.groupby("CustomerID")
        .agg(
            LastPurchase=("InvoiceDate", "max"),
            Frequency=("InvoiceNo", "nunique"),
            Monetary=("SalesAmount", "sum"),
        )
        .reset_index()
    )
    rfm["Recency"] = (snapshot_date - rfm["LastPurchase"].dt.normalize()).dt.days
    return rfm[["CustomerID", "Recency", "Frequency", "Monetary"]].sort_values("CustomerID").reset_index(drop=True)
