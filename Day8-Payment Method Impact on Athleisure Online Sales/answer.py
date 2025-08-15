import pandas as pd

# importing data
fct_transactions = pd.read_csv(
    "fct_transactions.csv",
    dtype={
        "transaction_id": "int64",
        "customer_id": "int64",
        "payment_method": "string",
        "order_value": "float64"
    },
    parse_dates=["transaction_date"]
)


# Question 1
fct_transactions['yearmon'] = (
    fct_transactions['transaction_date']
    .dt.to_period("M")
    .astype('str')
)

q2 = fct_transactions.query("yearmon <= '2025-06' & yearmon >= '2025-04'")

tran_counts = q2.groupby('payment_method', as_index=False)[
    'transaction_id'].count()
print(tran_counts)

# Question 2
fct_transactions['yearmon'] = (
    fct_transactions['transaction_date']
    .dt.to_period("M")
    .astype("str")
)

q2 = fct_transactions.query("yearmon >= '2025-04' & yearmon <= '2025-06'")

order_value_mean = q2.groupby('payment_method', as_index=False)[
    'order_value'].mean()

order_value_mean = (
    order_value_mean
    .rename(columns={
            'order_value': 'average_order_value'
            }
            )
)

order_value_mean = order_value_mean.sort_values(
    by='average_order_value',
    ascending=False
)

print(order_value_mean)

# Question 3
fct_transactions['yearmon'] = (
    fct_transactions['transaction_date']
    .dt.to_period("M")
    .astype("str")
)

q2 = fct_transactions.query("yearmon >= '2025-04' & yearmon <= '2025-06'")

credit_sales_total = q2.loc[q2['payment_method']
                            == 'credit_card', 'order_value'].sum()

switch_rate = 0.20
aov_increase = 0.15
predicted_sales_lift = credit_sales_total * switch_rate * aov_increase

df = pd.DataFrame(
    {
        "predicted_sales_lift": [predicted_sales_lift]
    }
)

print(df)
