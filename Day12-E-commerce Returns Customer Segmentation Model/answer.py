import pandas as pd


# importing the data
import pandas as pd

customer_returns = pd.read_csv(
    "customer_returns.csv",
    dtype={
        "customer_id": "string",
        "order_id": "string",
        "order_date": "string",
        "return_flag": "boolean",
        "order_amount": "float"
    }
)

# Q1
customer_returns['order_date'] = pd.to_datetime(
    customer_returns['order_date'],
    dayfirst=False,
    format='mixed'
)

customer_returns['order_yearmon'] = (
    customer_returns['order_date']
    .dt.to_period("M")
    .astype("str")
)

filtered_orders = customer_returns.query(
    "order_yearmon <= '2025-06' & order_date >= '2024-07'"
)

return_data = filtered_orders.query("return_flag == True")

print(return_data['customer_id'].unique())


# Q2
customer_returns['order_date'] = pd.to_datetime(
    customer_returns['order_date'],
    dayfirst=False,
    format='mixed'
)

customer_returns['order_month'] = customer_returns['order_date'].dt.month

customer_returns = customer_returns.set_index(['order_date', 'customer_id'])

customer_data = customer_returns.groupby(['customer_id', 'order_month']) \
    .size() \
    .reset_index()

print(customer_data)
