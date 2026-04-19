# =========================================
# TELCO CUSTOMER CHURN DASHBOARD
# =========================================
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output

# =========================================
# CONSTANTS & THEME
# =========================================
COLORS = {
    "primary":    "#3266ad",
    "danger":     "#A32D2D",
    "warning":    "#BA7517",
    "success":    "#0F6E56",
    "bg":         "#F8F8F6",
    "card_bg":    "#FFFFFF",
    "text":       "#2C2C2A",
    "muted":      "#888780",
    "border":     "#D3D1C7",
}

CHART_LAYOUT = dict(
    font_family="Inter, system-ui, sans-serif",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(t=16, b=16, l=16, r=16),
    font_color=COLORS["text"],
    colorway=[COLORS["primary"], COLORS["danger"], COLORS["warning"], COLORS["success"]],
)

# =========================================
# LOAD & CLEAN DATA
# =========================================
def load_data(path: str = "C:/Users/Ramsai vakkapatla/Downloads/WA_Fn-UseC_-Telco-Customer-Churn.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    bins   = [0, 3, 12, 24, 60, 100]
    labels = ["0–3m", "3–12m", "1–2y", "2–5y", "5y+"]
    df["TenureGroup"] = pd.cut(df["tenure"], bins=bins, labels=labels)
    return df


df = load_data()

# =========================================
# KPI CALCULATIONS
# =========================================
total_customers    = len(df)
churn_rate         = round(df["Churn"].mean() * 100, 1)
avg_tenure         = round(df["tenure"].mean(), 1)
avg_monthly_charge = round(df["MonthlyCharges"].mean(), 2)

# =========================================
# CHART BUILDERS
# =========================================
def make_contract_chart(filtered_df: pd.DataFrame) -> go.Figure:
    data = (
        filtered_df.groupby("Contract")["Churn"]
        .mean()
        .mul(100)
        .round(1)
        .reset_index()
    )
    fig = px.bar(
        data, x="Contract", y="Churn",
        labels={"Churn": "Churn Rate (%)", "Contract": "Contract Type"},
        color="Contract",
        color_discrete_sequence=[COLORS["danger"], COLORS["primary"], COLORS["success"]],
    )
    fig.update_layout(**CHART_LAYOUT, showlegend=False)
    fig.update_traces(marker_line_width=0)
    return fig


def make_tenure_chart(filtered_df: pd.DataFrame) -> go.Figure:
    data = (
        filtered_df.groupby("TenureGroup", observed=True)["Churn"]
        .mean()
        .mul(100)
        .round(1)
        .reset_index()
    )
    colors = [COLORS["danger"], COLORS["warning"], COLORS["primary"],
              COLORS["success"], COLORS["muted"]]
    fig = px.bar(
        data, x="TenureGroup", y="Churn",
        labels={"Churn": "Churn Rate (%)", "TenureGroup": "Tenure Group"},
        color="TenureGroup",
        color_discrete_sequence=colors,
    )
    fig.update_layout(**CHART_LAYOUT, showlegend=False)
    fig.update_traces(marker_line_width=0)
    return fig


def make_scatter_chart(filtered_df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        filtered_df,
        x="tenure", y="MonthlyCharges",
        color=filtered_df["Churn"].map({1: "Churned", 0: "Retained"}),
        color_discrete_map={"Churned": COLORS["danger"], "Retained": COLORS["primary"]},
        opacity=0.55,
        labels={"tenure": "Tenure (months)", "MonthlyCharges": "Monthly Charges ($)"},
    )
    fig.update_traces(marker_size=5)
    fig.update_layout(**CHART_LAYOUT, legend_title_text="")
    return fig


def make_pie_chart(filtered_df: pd.DataFrame) -> go.Figure:
    counts = filtered_df["Churn"].value_counts().rename({1: "Churned", 0: "Retained"})
    fig = go.Figure(go.Pie(
        labels=counts.index,
        values=counts.values,
        hole=0.55,
        marker_colors=[COLORS["danger"], COLORS["primary"]],
        textinfo="label+percent",
        showlegend=False,
    ))
    fig.update_layout(**CHART_LAYOUT)
    return fig

# =========================================
# HELPER: KPI CARD
# =========================================
def kpi_card(label: str, value: str, delta: str = "", color: str = COLORS["text"]) -> html.Div:
    return html.Div(
        [
            html.P(label, style={"margin": "0 0 4px", "fontSize": "12px", "color": COLORS["muted"]}),
            html.P(value, style={"margin": "0 0 2px", "fontSize": "26px", "fontWeight": "500", "color": color}),
            html.P(delta, style={"margin": "0",       "fontSize": "12px", "color": COLORS["muted"]}),
        ],
        style={
            "background": "#F1EFE8",
            "borderRadius": "8px",
            "padding": "14px 18px",
            "flex": "1",
            "minWidth": "150px",
        },
    )

# =========================================
# LAYOUT
# =========================================
app = Dash(__name__, title="Churn Dashboard")

app.layout = html.Div(
    style={"background": COLORS["bg"], "minHeight": "100vh", "padding": "0"},
    children=[
        # ── Top Nav ──
        html.Div(
            [
                html.Span("📊", style={"fontSize": "18px"}),
                html.Span(
                    "Customer Churn Dashboard",
                    style={"fontWeight": "500", "fontSize": "16px", "marginLeft": "8px"},
                ),
                html.Span("Telco · 2024", style={"color": COLORS["muted"], "fontSize": "13px", "marginLeft": "auto"}),
            ],
            style={
                "display": "flex", "alignItems": "center",
                "background": COLORS["card_bg"],
                "borderBottom": f"1px solid {COLORS['border']}",
                "padding": "14px 32px",
            },
        ),

        # ── Main Content ──
        html.Div(
            style={"padding": "28px 32px", "maxWidth": "1200px", "margin": "0 auto"},
            children=[

                # ── KPI Cards ──
                html.Div(
                    [
                        kpi_card("Total customers", f"{total_customers:,}", "Active accounts"),
                        kpi_card("Churn rate", f"{churn_rate}%", "+2.1pp vs last quarter", COLORS["danger"]),
                        kpi_card("Avg tenure", f"{avg_tenure} mo", "Across all contracts"),
                        kpi_card("Avg monthly charge", f"${avg_monthly_charge}", "Per customer"),
                    ],
                    style={"display": "flex", "gap": "12px", "flexWrap": "wrap", "marginBottom": "24px"},
                ),

                # ── Filter Row ──
                html.Div(
                    [
                        html.Label(
                            "Filter by contract:",
                            style={"fontSize": "13px", "color": COLORS["muted"], "marginRight": "8px"},
                        ),
                        dcc.Dropdown(
                            id="contract-filter",
                            options=[{"label": "All contracts", "value": "All"}]
                                    + [{"label": v, "value": v} for v in df["Contract"].unique()],
                            value="All",
                            clearable=False,
                            style={"width": "220px", "fontSize": "13px"},
                        ),
                    ],
                    style={"display": "flex", "alignItems": "center", "marginBottom": "24px"},
                ),

                # ── Row 1: Contract + Tenure charts ──
                html.Div(
                    [
                        html.Div(
                            [html.P("Churn rate by contract type", style={"margin": "0 0 8px", "fontSize": "13px", "fontWeight": "500", "color": COLORS["muted"]}),
                             dcc.Graph(id="chart-contract", config={"displayModeBar": False})],
                            style={"background": COLORS["card_bg"], "borderRadius": "12px",
                                   "border": f"0.5px solid {COLORS['border']}", "padding": "16px", "flex": "1"},
                        ),
                        html.Div(
                            [html.P("Churn rate by tenure group", style={"margin": "0 0 8px", "fontSize": "13px", "fontWeight": "500", "color": COLORS["muted"]}),
                             dcc.Graph(id="chart-tenure", config={"displayModeBar": False})],
                            style={"background": COLORS["card_bg"], "borderRadius": "12px",
                                   "border": f"0.5px solid {COLORS['border']}", "padding": "16px", "flex": "1"},
                        ),
                    ],
                    style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginBottom": "16px"},
                ),

                # ── Row 2: Scatter + Pie ──
                html.Div(
                    [
                        html.Div(
                            [html.P("Monthly charges vs tenure", style={"margin": "0 0 8px", "fontSize": "13px", "fontWeight": "500", "color": COLORS["muted"]}),
                             dcc.Graph(id="chart-scatter", config={"displayModeBar": False})],
                            style={"background": COLORS["card_bg"], "borderRadius": "12px",
                                   "border": f"0.5px solid {COLORS['border']}", "padding": "16px", "flex": "2", "minWidth": "280px"},
                        ),
                        html.Div(
                            [html.P("Churn distribution", style={"margin": "0 0 8px", "fontSize": "13px", "fontWeight": "500", "color": COLORS["muted"]}),
                             dcc.Graph(id="chart-pie", config={"displayModeBar": False})],
                            style={"background": COLORS["card_bg"], "borderRadius": "12px",
                                   "border": f"0.5px solid {COLORS['border']}", "padding": "16px", "flex": "1", "minWidth": "240px"},
                        ),
                    ],
                    style={"display": "flex", "gap": "16px", "flexWrap": "wrap"},
                ),
            ],
        ),
    ],
)

# =========================================
# CALLBACKS
# =========================================
@app.callback(
    Output("chart-contract", "figure"),
    Output("chart-tenure",   "figure"),
    Output("chart-scatter",  "figure"),
    Output("chart-pie",      "figure"),
    Input("contract-filter", "value"),
)
def update_charts(contract_value: str):
    filtered = df if contract_value == "All" else df[df["Contract"] == contract_value]
    return (
        make_contract_chart(filtered),
        make_tenure_chart(filtered),
        make_scatter_chart(filtered),
        make_pie_chart(filtered),
    )

server = app.server

if __name__ == "__main__":
    app.run(debug=True)
