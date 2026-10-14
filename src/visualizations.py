import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def monthly_sales_chart(data: pd.DataFrame):
    fig = px.line(
        data, x="InvoiceMonth", y="SalesAmount", markers=True,
        title="Monthly Gross Sales", labels={"InvoiceMonth": "Month", "SalesAmount": "Gross sales (£)"}
    )
    fig.update_layout(xaxis_tickangle=-35, margin=dict(l=20, r=20, t=55, b=20))
    return fig


def bar_chart(data: pd.DataFrame, x: str, y: str, title: str):
    fig = px.bar(data, x=x, y=y, title=title, labels={x: "", y: "Gross sales (£)"})
    fig.update_layout(xaxis_tickangle=-35, margin=dict(l=20, r=20, t=55, b=70))
    return fig


def segment_scatter(data: pd.DataFrame):
    fig = px.scatter(
        data, x="Frequency", y="Monetary", color="Segment",
        hover_data=["CustomerID", "Recency"],
        title="Customer Segments: Purchase Frequency vs Monetary Value",
        labels={"Frequency": "Number of orders", "Monetary": "Gross purchase value (£)"}
    )
    fig.update_layout(margin=dict(l=20, r=20, t=55, b=20))
    return fig
