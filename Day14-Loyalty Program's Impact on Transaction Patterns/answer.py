import pandas as pd
import numpy as np

# importing data
# Read customers.csv with specified dtypes
dim_customers = pd.read_csv(
    "customers.csv",
    dtype={
        "customer_id": "int64",
        "is_loyalty_member": "boolean"
    }
)

# Read transactions.csv with specified dtypes
fct_transactions = pd.read_csv(
    "fct_transactions.csv",
    dtype={
        "transaction_id": "int64",
        "customer_id": "int64",
        "transaction_value": "float64"
    },
    parse_dates=["transaction_date"]
)


# Question 1
merged = pd.merge(fct_transactions, dim_customers, on='customer_id')

july_trans = merged.query(
    "transaction_date >= '2024-07-01' & transaction_date <= '2024-07-31'"
)

unique_trans_made = july_trans.groupby('is_loyalty_member', as_index=False).agg(
    {
        'transaction_id': 'nunique'
    }
)

print(unique_trans_made)

# Question 2
july_trans = merged.query(
    "transaction_date >= '2024-07-01' & transaction_date <= '2024-07-31'"
)

july_trans['is_loyalty_member'] = july_trans['is_loyalty_member'].astype('int')

avg_transaction_value_both = (
    july_trans.groupby('is_loyalty_member', as_index=False)[
        'transaction_value']
    .mean()
    .rename(columns={'transaction_value': 'average_transaction_value'})
).round(2)

print(avg_transaction_value_both)

# Question 3

july_trans['is_loyalty_member'] = july_trans['is_loyalty_member'].astype('int')

avg_trans_value = (
    july_trans.groupby('is_loyalty_member', as_index=False)[
        'transaction_value']
    .mean()
    .rename(columns={
        'transaction_value': 'average_transaction_value'
    })
).round(2)

loyal_avg_trans_value = avg_trans_value.query(
    "is_loyalty_member == 1"
)['average_transaction_value'].values

nonloyal_avg_trans_value = avg_trans_value.query(
    "is_loyalty_member == 0"
)['average_transaction_value'].values

percentage_diff = np.round(
    ((loyal_avg_trans_value - nonloyal_avg_trans_value) /
     nonloyal_avg_trans_value) * 100,
    2
)

difference = pd.DataFrame(
    {
        'percentage_difference': percentage_diff
    }
)

print(difference)
