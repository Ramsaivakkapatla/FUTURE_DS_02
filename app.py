# =========================================
# TELCO CUSTOMER CHURN DASHBOARD (FINAL FIX)
# =========================================
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
import os

# =========================================
# CONSTANTS
# =========================================
COLORS = {
    "primary": "#3266ad",
    "danger": "#A32D2D",
    "warning": "#BA7517",
    "success": "#0F6E56",
    "bg": "#F8F8F6",
    "card_bg": "#FFFFFF",
    "text": "#2C2C2A",
    "muted": "#888780",
    "border": "#D3D1C7",
}

CHART_LAYOUT = dict(
    font_family="Arial",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(t=16, b=16, l=16, r=16),
)

# =========================================
# LOAD DATA (FIXED PATH)
# =========================================
def load_data():
    base = os.path.dirname(__file__)
    file_path = os.path.join(base, "Telco-Customer-Churn.csv")

    df = pd.read_csv(file_path)

    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())

    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    bins = [0, 3, 12, 24, 60, 100]
    labels = ["0-3m", "3-12m", "1-2y", "2-5y", "5y+"]
    df["TenureGroup"] = pd.cut(df["tenure"], bins=bins, labels=labels)

    return df


df = load_data()

# =========================================
# KPIs
# =========================================
total_customers = len(df)
churn_rate = round(df["Churn"].mean() * 100, 1)
avg_tenure = round(df["tenure"].mean(), 1)

# =========================================
# APP INIT (ONLY ONCE)
# =========================================
app = Dash(__name__)
server = app.server   # REQUIRED

# =========================================
# CHART FUNCTIONS
# =========================================
def contract_chart(data):
    d = data.groupby("Contract")["Churn"].mean().reset_index()
    return px.bar(d, x="Contract", y="Churn")

def tenure_chart(data):
    d = data.groupby("TenureGroup", observed=True)["Churn"].mean().reset_index()
    return px.bar(d, x="TenureGroup", y="Churn")

def scatter_chart(data):
    return px.scatter(data, x="tenure", y="MonthlyCharges", color="Churn")

def pie_chart(data):
    return px.pie(data, names="Churn")

# =========================================
# LAYOUT (CRITICAL)
# =========================================
app.layout = html.Div([
    html.H1("Customer Churn Dashboard"),

    html.Div([
        html.H3(f"Total Customers: {total_customers}"),
        html.H3(f"Churn Rate: {churn_rate}%"),
        html.H3(f"Avg Tenure: {avg_tenure}")
    ]),

    dcc.Dropdown(
        id="filter",
        options=[{"label": "All", "value": "All"}] +
                [{"label": i, "value": i} for i in df["Contract"].unique()],
        value="All"
    ),

    dcc.Graph(id="contract"),
    dcc.Graph(id="tenure"),
    dcc.Graph(id="scatter"),
    dcc.Graph(id="pie")
])

# =========================================
# CALLBACK
# =========================================
@app.callback(
    Output("contract", "figure"),
    Output("tenure", "figure"),
    Output("scatter", "figure"),
    Output("pie", "figure"),
    Input("filter", "value")
)
def update(value):
    filtered = df if value == "All" else df[df["Contract"] == value]

    return (
        contract_chart(filtered),
        tenure_chart(filtered),
        scatter_chart(filtered),
        pie_chart(filtered)
    )

# =========================================
# RUN
# =========================================
app = Dash(__name__)
server = app.server 


if __name__ == "__main__":
    app.run(debug=True)
