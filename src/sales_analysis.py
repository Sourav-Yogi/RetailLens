import pandas as pd


def eligible_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Return positive sales lines excluding cancellation invoices and invalid prices."""
    mask = (
        ~df["IsCancellation"].astype(bool)
        & (pd.to_numeric(df["Quantity"], errors="coerce") > 0)
        & (pd.to_numeric(df["UnitPrice"], errors="coerce") > 0)
    )
    return df.loc[mask].copy()


def get_sales_summary(df: pd.DataFrame) -> dict:
    sales = eligible_sales(df)
    return {
        "gross_sales": float(sales["SalesAmount"].sum()),
        "orders": int(sales["InvoiceNo"].nunique()),
        "customers": int(sales["CustomerID"].nunique()),
        "products": int(sales["StockCode"].nunique()),
        "sales_lines": int(len(sales)),
    }


def monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    sales = eligible_sales(df)
    result = (
        sales.groupby("InvoiceMonth", as_index=False)["SalesAmount"]
        .sum()
        .sort_values("InvoiceMonth")
    )
    return result


def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    sales = eligible_sales(df)
    return (
        sales.groupby("Description", as_index=False)
        .agg(SalesAmount=("SalesAmount", "sum"), UnitsSold=("Quantity", "sum"))
        .sort_values("SalesAmount", ascending=False)
        .head(n)
        .reset_index(drop=True)
    )


def top_countries(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    sales = eligible_sales(df)
    return (
        sales.groupby("Country", as_index=False)["SalesAmount"]
        .sum()
        .sort_values("SalesAmount", ascending=False)
        .head(n)
        .reset_index(drop=True)
    )


def return_summary(df: pd.DataFrame) -> pd.DataFrame:
    returns = df.loc[df["Quantity"] < 0].copy()
    if returns.empty:
        return pd.DataFrame(columns=["Country", "ReturnValue", "ReturnLines"])
    returns["ReturnValue"] = returns["SalesAmount"].abs()
    return (
        returns.groupby("Country", as_index=False)
        .agg(ReturnValue=("ReturnValue", "sum"), ReturnLines=("Quantity", "size"))
        .sort_values("ReturnValue", ascending=False)
    )
