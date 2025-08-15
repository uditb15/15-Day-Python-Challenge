import pandas as pd


# Define column types
dtypes_dic = {
    'customer_id': 'string',
    'region': 'string',
    'demographic_group': 'string',
    'pre_order_quantity': 'Int64'
}

# Read the CSV file
pre_sale_data = pd.read_csv(
    'pre_sale_data.csv',
    dtype=dtypes_dic,
    parse_dates=['pre_order_date'],
    keep_default_na=True
)

# Question 1
percent_missing = (
    pre_sale_data
    .isna()
    .any(axis=1)
    .sum() / len(pre_sale_data)
) * 100

print(percent_missing)

clean_data = pre_sale_data.dropna()
print(clean_data)

# Question 2

# Extract month from the pre_order_date
clean_data['pre_order_month'] = clean_data['pre_order_date'].dt.month

# Group by month, region, and demographic group, then sum the pre_order_quantity
monthly_summary = (
    clean_data
    .groupby(['pre_order_month', 'region', 'demographic_group'])['pre_order_quantity']
    .sum()
)

print(monthly_summary)

# Question 3

# Extract month and year-month from pre_order_date
clean_data['pre_order_month'] = clean_data['pre_order_date'].dt.month
clean_data['pre_order_yearmon'] = clean_data['pre_order_date'].dt.to_period(
    "M")

# Filter July and August data and aggregate by region
july_data = (
    clean_data[clean_data['pre_order_yearmon'].astype(str) == "2024-07"]
    .groupby('region')['pre_order_quantity']
    .sum()
    .reset_index()
)

august_data = (
    clean_data[clean_data['pre_order_yearmon'].astype(str) == "2024-08"]
    .groupby('region')['pre_order_quantity']
    .sum()
    .reset_index()
)

# Merge July and August data and calculate percent change
july_aug_joined = pd.merge(
    july_data, august_data,
    on='region',
    suffixes=("_july", "_august")
)

july_aug_joined['percent_change'] = (
    (july_aug_joined['pre_order_quantity_august'] - july_aug_joined['pre_order_quantity_july']) /
    july_aug_joined['pre_order_quantity_july']
) * 100

# Predict September sales using August sales and percent change
july_aug_joined['september_sales_prediction'] = (
    july_aug_joined['pre_order_quantity_august'] *
    (july_aug_joined['percent_change'] / 100 + 1)
)

# Select and rename final output
september_sales = july_aug_joined[['region', 'september_sales_prediction']]
september_sales = september_sales.rename(columns={
    'september_sales_prediction': 'September'
})

print(september_sales)
