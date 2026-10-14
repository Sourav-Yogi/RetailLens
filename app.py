from pathlib import Path
import streamlit as st
import plotly.express as px

from src.data_loader import RAW_DATA_PATH, PROCESSED_DATA_PATH, load_or_prepare_data
from src.sales_analysis import get_sales_summary, monthly_sales, top_products, top_countries
from src.visualizations import monthly_sales_chart, bar_chart

st.set_page_config(page_title="RetailLens", page_icon="🛍️", layout="wide")

st.title("RetailLens")
st.caption("Customer & Sales Intelligence Platform")

@st.cache_data(show_spinner="Loading retail data...")
def get_data():
    return load_or_prepare_data()

try:
    df = get_data()
except FileNotFoundError as exc:
    st.error(str(exc))
    st.info("Place the UCI file at data/raw/Online Retail.xlsx, then refresh this page.")
    st.stop()
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

summary = get_sales_summary(df)

st.subheader("Retail performance overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Gross sales", f"£{summary['gross_sales']:,.0f}")
c2.metric("Orders", f"{summary['orders']:,}")
c3.metric("Identified customers", f"{summary['customers']:,}")
c4.metric("Products", f"{summary['products']:,}")

left, right = st.columns(2)
with left:
    st.plotly_chart(monthly_sales_chart(monthly_sales(df)), width="stretch")
with right:
    country_data = top_countries(df, n=8)
    st.plotly_chart(bar_chart(country_data, "Country", "SalesAmount", "Top countries by gross sales"), use_container_width=True)

st.subheader("Top products")
products = top_products(df, n=10)
st.dataframe(products, width="stretch", hide_index=True)

with st.expander("Data notes and definitions"):
    st.markdown("""
    - **Gross sales** includes positive-quantity, positive-price lines from invoices not marked as cancellations.
    - It is not profit or final net revenue; returns and cancellations require separate treatment.
    - Customer analytics excludes rows without a CustomerID because they cannot be attributed to a known customer.
    - Use the pages in the sidebar for sales analysis and customer segmentation.
    """)
