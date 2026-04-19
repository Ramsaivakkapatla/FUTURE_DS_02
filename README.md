# FUTURE_DS_02
📊 Telco Customer Churn Dashboard
An interactive web dashboard built with Plotly Dash to analyze and visualize customer churn patterns for a telecom company. Deployed live on Render.
🔗 Live Demo: https://customerretentionchurn.onrender.com

📸 Preview

Dashboard showing KPI cards, churn by contract type, tenure groups, monthly charges scatter plot, and churn distribution donut chart.


📁 Dataset
IBM Telco Customer Churn Dataset

Source: Kaggle — Telco Customer Churn
File: WA_Fn-UseC_-Telco-Customer-Churn.csv
Rows: 7,043 customers | Columns: 21 features

Key columns used:
ColumnDescriptionChurnWhether the customer left (Yes/No)ContractContract type (Month-to-month, One year, Two year)tenureNumber of months the customer has stayedMonthlyChargesMonthly charge amountTotalChargesTotal amount charged

📊 Dashboard Features
KPI Cards

Total Customers — count of all accounts
Churn Rate (%) — percentage of customers who churned
Average Tenure — average months a customer stayed
Average Monthly Charge — mean monthly billing amount

Charts
ChartDescriptionChurn rate by contract typeBar chart comparing churn across contract categoriesChurn rate by tenure groupBar chart across 5 tenure buckets (0–3m, 3–12m, 1–2y, 2–5y, 5y+)Monthly charges vs tenureScatter plot coloured by churn statusChurn distributionDonut chart of churned vs retained customers
Filters

Contract type dropdown — filter all 4 charts simultaneously by contract


🛠️ Tech Stack
ToolPurposePython 3.14Core languageDash 4.1Web framework for the dashboardPlotly 6.7Interactive chartsPandas 3.0Data loading and transformationGunicornWSGI server for productionRenderCloud deployment platform
