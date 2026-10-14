import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


FEATURES = ["Recency", "Frequency", "Monetary"]


def segment_customers(rfm: pd.DataFrame, n_clusters: int = 4, random_state: int = 42):
    """Fit K-Means to log-transformed RFM features and return labeled data plus metrics."""
    if len(rfm) < n_clusters:
        raise ValueError(f"Need at least {n_clusters} customers to create {n_clusters} clusters.")

    result = rfm.copy()
    X = result[FEATURES].astype(float).clip(lower=0)
    X_log = np.log1p(X)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_log)

    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    result["Segment"] = model.fit_predict(X_scaled)

    score = None
    if n_clusters > 1 and len(result) > n_clusters:
        score = float(silhouette_score(X_scaled, result["Segment"]))

    profile = (
        result.groupby("Segment", as_index=False)
        .agg(
            Customers=("CustomerID", "nunique"),
            AvgRecency=("Recency", "mean"),
            AvgFrequency=("Frequency", "mean"),
            AvgMonetary=("Monetary", "mean"),
            TotalMonetary=("Monetary", "sum"),
        )
        .sort_values("TotalMonetary", ascending=False)
    )
    return result, profile, score
