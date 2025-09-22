import re
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go

# load data & rename columns
csv_loan    = pd.read_csv("path/LuxuryLoanPortfolio.csv", delimiter=",")
rename_dict = {
                col: re.sub(r'\W+', '_', col.strip().lower()).strip('_')
                for col in csv_loan.columns
                }
loan_porto  = csv_loan.rename(columns=rename_dict)

#----------------- YEARLY CUST DIST PER PURPOSE------------------

## add kolom year
loan_porto['funded_date'] = pd.to_datetime(loan_porto['funded_date'])
loan_porto['loan_year'] = loan_porto['funded_date'].dt.year

## aggregate cust per tahun & purpose
loan_grouped = (
                loan_porto.groupby(['loan_year', 'purpose'])['loan_id']
                .nunique()
                .reset_index(name='total_cust')
                )     
## Grouped bar
fig_purpose = px.bar(
    loan_grouped,
    x="loan_year",
    y="total_cust",
    color="purpose",
    title="Yearly Customer Distribution per Loan Purpose (2012–2019)",
    barmode="group",
    labels={"loan_year": "Year", "total_cust": "Total Customers", "purpose": "Loan Purpose" }
)


# ------------------ YEARLY CUST GROWTH RATE ------------------
## total customer per tahun
customers_per_year = (
                    loan_porto.groupby('loan_year')['loan_id']
                    .nunique()
                    .reset_index(name='total_cust')
                    )

## growth rate (%)
customers_per_year['growth_rate'] = customers_per_year['total_cust'].pct_change() * 100


fig_growth = go.Figure()

## bar for  total customer
fig_growth.add_trace(go.Bar(
    x=customers_per_year['loan_year'],
    y=customers_per_year['total_cust'],
    name='Total Customers',
    yaxis='y1'
))

## line for growth rate
fig_growth.add_trace(go.Scatter(
    x=customers_per_year['loan_year'],
    y=customers_per_year['growth_rate'],
    mode='lines+markers',
    name='Growth Rate (%)',
    yaxis='y2'
))

fig_growth.update_layout(
    title="Yearly Loan Customers & Growth Rate",
    xaxis=dict(title="Year"),
    yaxis=dict(title="Total Customers", side="left"),
    yaxis2=dict(title="Growth Rate (%)", overlaying="y", side="right"),
    legend=dict(x=0.5, y=1.1, orientation="h", xanchor="center"),
)


# -------------- LTV Ratio - Top 10 Building Class Categories --------------
loan_porto  = csv_loan.rename(columns=rename_dict)
loan_porto['ltv_ratio'] = loan_porto['loan_balance'] / loan_porto['property_value']

## get top-10 building class categories
top_classes = (
                loan_porto['building_class_category']
                .value_counts()
                .nlargest(10)
                .index
                )
df_top = loan_porto[loan_porto['building_class_category'].isin(top_classes)]

ltv_summary = (
    df_top.groupby("building_class_category")["ltv_ratio"]
    .median()
    .reset_index()
    .sort_values("ltv_ratio", ascending=True)
)

## horizontal bar
fig_ltv = px.bar(
    ltv_summary,
    x="ltv_ratio",
    y="building_class_category",
    orientation="h", 
    title="Median Loan-to-Value (LTV) Ratio - Top 10 Building Class Categories",
    labels={"ltv_ratio": "Median LTV Ratio", "building_class_category": "BUilding Class Category"}
)

fig_ltv.update_layout(
    yaxis=dict(categoryorder="total ascending")
)



# -------- Build dash ---------
app = dash.Dash(__name__)

## Layout
app.layout = html.Div([
    html.H1("Loan Portfolio Dashboard", style={"textAlign": "center"}),

    html.Div([
        dcc.Graph(figure=fig_purpose),
        dcc.Graph(figure=fig_growth),
        dcc.Graph(figure=fig_ltv)
    ])
])

if __name__ == '__main__':
    app.run(port=8060)