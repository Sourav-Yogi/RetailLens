import streamlit as st
from src.data_loader import load_or_prepare_data
from src.sales_analysis import eligible_sales, monthly_sales, top_products, top_countries, return_summary
from src.visualizations import monthly_sales_chart, bar_chart

st.set_page_config(page_title="Sales Analysis | RetailLens", page_icon="📈", layout="wide")
st.title("Sales Analysis")
st.caption("Explore sales trends, product performance, and returns.")

@st.cache_data(show_spinner="Loading data...")
def get_data():
    return load_or_prepare_data()

df = get_data()
sales = eligible_sales(df)

start_date = sales["InvoiceDate"].min().date()
end_date = sales["InvoiceDate"].max().date()
date_range = st.date_input("Invoice date range", value=(start_date, end_date), min_value=start_date, max_value=end_date)

filtered = sales
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start, end = date_range
    filtered = sales[
        sales["InvoiceDate"].dt.date.between(start, end)
    ]

k1, k2, k3 = st.columns(3)
k1.metric("Gross sales", f"£{filtered['SalesAmount'].sum():,.0f}")
k2.metric("Orders", f"{filtered['InvoiceNo'].nunique():,}")
k3.metric("Units sold", f"{filtered['Quantity'].sum():,}")

st.plotly_chart(monthly_sales_chart(monthly_sales(filtered)), use_container_width=True)
left, right = st.columns(2)
with left:
    st.plotly_chart(bar_chart(top_products(filtered, 10), "Description", "SalesAmount", "Top 10 products"), use_container_width=True)
with right:
    st.plotly_chart(bar_chart(top_countries(filtered, 10), "Country", "SalesAmount", "Top 10 countries"), use_container_width=True)

with st.expander("Returns overview"):
    returns = return_summary(df)
    st.write("Return/negative-quantity lines are displayed separately and are not included in the gross-sales KPI.")
    st.dataframe(returns.head(15), use_container_width=True, hide_index=True)
