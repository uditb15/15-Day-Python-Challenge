import pandas as pd

# importing data
fct_sales = pd.read_csv(
    "fct_sales.csv",
    dtype={
        "sale_id": "int64",
        "celebrity_id": "int64",
        "product_id": "int64",
        "sale_amount": "float64"
    },
    parse_dates=["sale_date"]
)


# Question 1
# Ensure sale_date is in datetime format
fct_sales['sale_date'] = pd.to_datetime(fct_sales['sale_date'])

# Convert to year-month in 'YYYY-MM' string format
fct_sales['yearmon'] = fct_sales['sale_date'].dt.to_period("M").astype("str")

# Use string comparison with zero-padded months
q1_sales = fct_sales[
    (fct_sales['yearmon'] >= "2025-01") &
    (fct_sales['yearmon'] <= "2025-03")
]

na_df = q1_sales[q1_sales['sale_amount'].isna()]

print(na_df)

# Question 2
# Use string comparison
q1_sales = fct_sales[
    (fct_sales['yearmon'] >= "2025-01") &
    (fct_sales['yearmon'] <= "2025-03")
]

prod_celebrity_groups = (
    q1_sales
    .groupby(['celebrity_id', 'product_id'], as_index=False)
    .size()
    .filter(items=['celebrity_id', 'product_id'])
)

print(prod_celebrity_groups)

# Question 3
celebrity_collabs = (
    q1_sales
    .groupby(['celebrity_id', 'product_id'], as_index=False)['sale_amount']
    .sum()
    .sort_values(by='sale_amount', ascending=False)
    .rename(
        columns={
            'sale_amount': 'total_sales'
        }
    )
)

celebrity_collabs['ranking'] = celebrity_collabs['total_sales'].rank(
    method='dense', ascending=False
)

print(celebrity_collabs.query("ranking <= 3").filter(
    items=['celebrity_id', 'product_id', 'total_sales']
))
