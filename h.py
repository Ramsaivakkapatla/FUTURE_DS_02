# ==============================
# 1. IMPORT LIBRARIES
# ==============================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# 2. LOAD DATA
# ==============================
df = pd.read_csv("C:/Users/Ramsai vakkapatla/Downloads/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Preview
print(df.head())

# ==============================
# 3. DATA CLEANING
# ==============================

# Convert TotalCharges to numeric
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# Fill missing values
df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)

# Convert Churn to binary
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

# ==============================
# 4. BASIC METRICS
# ==============================

total_customers = len(df)
churned_customers = df['Churn'].sum()
churn_rate = (churned_customers / total_customers) * 100

print(f"Total Customers: {total_customers}")
print(f"Churned Customers: {churned_customers}")
print(f"Churn Rate: {churn_rate:.2f}%")

# ==============================
# 5. TENURE GROUPING
# ==============================

def tenure_group(x):
    if x <= 3:
        return "0-3 months"
    elif x <= 12:
        return "3-12 months"
    elif x <= 24:
        return "1-2 years"
    else:
        return "2+ years"

df['TenureGroup'] = df['tenure'].apply(tenure_group)

# ==============================
# 6. CHURN BY SEGMENT
# ==============================

churn_by_contract = df.groupby('Contract')['Churn'].mean()
churn_by_payment = df.groupby('PaymentMethod')['Churn'].mean()
churn_by_tenure = df.groupby('TenureGroup')['Churn'].mean()

print("\nChurn by Contract:\n", churn_by_contract)
print("\nChurn by Payment Method:\n", churn_by_payment)
print("\nChurn by Tenure Group:\n", churn_by_tenure)

# ==============================
# 7. VISUALIZATIONS
# ==============================

# --- Churn Distribution ---
plt.figure()
df['Churn'].value_counts().plot(kind='bar')
plt.title("Churn Distribution")
plt.xlabel("Churn (0 = No, 1 = Yes)")
plt.ylabel("Count")
plt.show()

# --- Churn by Contract ---
plt.figure()
churn_by_contract.plot(kind='bar')
plt.title("Churn Rate by Contract Type")
plt.ylabel("Churn Rate")
plt.show()

# --- Churn by Tenure Group ---
plt.figure()
churn_by_tenure.plot(kind='bar')
plt.title("Churn Rate by Tenure Group")
plt.ylabel("Churn Rate")
plt.show()

# --- Monthly Charges vs Tenure ---
plt.figure()
plt.scatter(df['tenure'], df['MonthlyCharges'])
plt.title("Monthly Charges vs Tenure")
plt.xlabel("Tenure")
plt.ylabel("Monthly Charges")
plt.show()

# ==============================
# 8. COHORT ANALYSIS (BASIC)
# ==============================

# Create fake signup month (if not available)
df['SignupMonth'] = pd.to_datetime('2020-01-01') + pd.to_timedelta(df['tenure'], unit='M')

df['CohortMonth'] = df['SignupMonth'].dt.to_period('M')

cohort = df.groupby(['CohortMonth', 'TenureGroup'])['Churn'].mean().unstack()

print("\nCohort Table:\n", cohort)

# ==============================
# 9. KEY INSIGHTS (AUTO PRINT)
# ==============================

print("\n--- Key Insights ---")

if churn_by_contract.idxmax():
    print(f"Highest churn in contract type: {churn_by_contract.idxmax()}")

if churn_by_tenure.idxmax():
    print(f"Highest churn in tenure group: {churn_by_tenure.idxmax()}")

print("Customers with shorter tenure are more likely to churn.")
print("Monthly contract users typically show higher churn risk.")