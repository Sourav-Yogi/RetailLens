import pandas as pd
from src.data_cleaning import clean_data
from src.feature_engineering import build_rfm_features


def test_rfm_features_are_created_for_known_customers():
    raw = pd.DataFrame({
        "InvoiceNo": ["100", "100", "101", "102"],
        "StockCode": ["A", "B", "A", "A"],
        "Description": ["Item A", "Item B", "Item A", "Item A"],
        "Quantity": [2, 1, 3, 1],
        "InvoiceDate": pd.to_datetime(["2011-01-01", "2011-01-01", "2011-01-10", "2011-01-15"]),
        "UnitPrice": [5.0, 4.0, 5.0, 5.0],
        "CustomerID": [123.0, 123.0, 123.0, None],
        "Country": ["UK", "UK", "UK", "UK"],
    })
    cleaned = clean_data(raw)
    rfm = build_rfm_features(cleaned)
    assert list(rfm.columns) == ["CustomerID", "Recency", "Frequency", "Monetary"]
    assert len(rfm) == 1
    assert rfm.iloc[0]["Frequency"] == 2
