from pathlib import Path
import pandas as pd
from src.data_cleaning import clean_data

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_retail.csv"


def load_raw_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the original UCI Online Retail Excel workbook."""
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {path}\n"
            "Download Online Retail.xlsx from the UCI Online Retail dataset "
            "and place it in data/raw/."
        )
    return pd.read_excel(path)


def load_or_prepare_data() -> pd.DataFrame:
    """Load processed CSV if available; otherwise clean the raw workbook and save it."""
    if PROCESSED_DATA_PATH.exists():
        df = pd.read_csv(PROCESSED_DATA_PATH, parse_dates=["InvoiceDate"])
        df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce").astype("Int64")
        return df

    raw = load_raw_data()
    cleaned = clean_data(raw)
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(PROCESSED_DATA_PATH, index=False)
    return cleaned
