import pandas as pd
from src.data_cleaning import clean_data


def sample_data():
    return pd.DataFrame({
        "InvoiceNo": ["100", "100", "C101", "102"],
        "StockCode": ["A", "A", "B", "C"],
        "Description": ["Item A", "Item A", "Item B", None],
        "Quantity": [2, 2, -1, 3],
        "InvoiceDate": pd.to_datetime(["2011-01-01", "2011-01-01", "2011-01-02", "2011-01-03"]),
        "UnitPrice": [5.0, 5.0, 2.0, 1.0],
        "CustomerID": [123.0, 123.0, None, 456.0],
        "Country": ["UK", "UK", "UK", "France"],
    })


def test_clean_data_drops_exact_duplicates_and_missing_descriptions():
    cleaned = clean_data(sample_data())
    assert len(cleaned) == 2
    assert cleaned["Description"].notna().all()


def test_clean_data_adds_expected_features():
    cleaned = clean_data(sample_data())
    assert "SalesAmount" in cleaned.columns
    assert "IsCancellation" in cleaned.columns
    assert "InvoiceMonth" in cleaned.columns
    assert cleaned.loc[cleaned["InvoiceNo"] == "C101", "IsCancellation"].iloc[0]
