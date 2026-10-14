import streamlit as st
from src.data_loader import load_or_prepare_data
from src.feature_engineering import build_rfm_features
from src.customer_segmentation import segment_customers
from src.visualizations import segment_scatter

st.set_page_config(page_title="Customer Segmentation | RetailLens", page_icon="👥", layout="wide")
st.title("Customer Segmentation")
st.caption("RFM feature engineering and K-Means clustering.")

@st.cache_data(show_spinner="Loading data...")
def get_data():
    return load_or_prepare_data()

df = get_data()
rfm = build_rfm_features(df)
cluster_count = st.slider("Number of customer segments", min_value=2, max_value=6, value=4)

try:
    labeled, profile, score = segment_customers(rfm, n_clusters=cluster_count)
except ValueError as exc:
    st.error(str(exc))
    st.stop()

if score is not None:
    st.metric("Silhouette score", f"{score:.3f}", help="Higher is generally better, but interpret this alongside the segment profiles.")
else:
    st.info("Silhouette score unavailable for this dataset size or clustering result.")

st.plotly_chart(segment_scatter(labeled), use_container_width=True)
st.subheader("Segment profiles")
st.dataframe(profile.round(2), use_container_width=True, hide_index=True)

st.subheader("Customer-level results")
st.dataframe(labeled, use_container_width=True, hide_index=True)
csv = labeled.to_csv(index=False).encode("utf-8")
st.download_button("Download customer segments (CSV)", data=csv, file_name="retaillens_customer_segments.csv", mime="text/csv")
