import pandas as pd

# loading data
ice_cream_sales_data = pd.read_csv(
    "ice_cream_sales_data.csv",
    dtype={
        "transaction_id": "string",
        "product_name": "string",
        "sales_volume": "Int64",
        "temperature": "float64"
    },
    parse_dates=["sale_date"]
)

# Question 1
clean_data = ice_cream_sales_data.drop_duplicates()
print(clean_data)


# Question 2

# Extract transaction month from the sale_date column
clean_data['tran_month'] = clean_data['sale_date'].dt.month

# Define bins and labels for temperature ranges
bins = [float('-inf'), 60, 70, 80, 90, 100, float('inf')]
labels = [
    'Less than 60 degrees',
    '60 to less than 70 degrees',
    '70 to less than 80 degrees',
    '80 to less than 90 degrees',
    '90 to less than 100 degrees',
    '100 degrees or more'
]

# Categorize temperature into defined bins
clean_data['temp_bin'] = pd.cut(
    clean_data['temperature'],
    bins=bins,
    labels=labels,
    right=True
)

# Create a pivot table summarizing sales volume by month and temperature bin
pivot_table_temp_month = pd.pivot_table(
    clean_data,
    values='sales_volume',
    index='tran_month',
    columns='temp_bin',
    aggfunc='sum',
    fill_value=0.0
)

# Print the pivot table
print(pivot_table_temp_month)


# Question 3

# Convert sale_date to datetime
clean_data['sale_date'] = pd.to_datetime(
    clean_data['sale_date'], errors='coerce')

# Extract transaction month from the sale date
clean_data['tran_month'] = clean_data['sale_date'].dt.month

# Calculate total monthly sales
monthly_sales = clean_data.groupby('tran_month', as_index=False)[
    'sales_volume'].sum()

# Calculate quartiles and IQR
monthly_sales['q1'] = monthly_sales['sales_volume'].quantile(0.25)
monthly_sales['q3'] = monthly_sales['sales_volume'].quantile(0.75)
monthly_sales['iqr'] = monthly_sales['q3'] - monthly_sales['q1']

# Calculate bounds for outlier detection
monthly_sales['lower_bound'] = monthly_sales['q1'] - \
    (1.5 * monthly_sales['iqr'])
monthly_sales['upper_bound'] = monthly_sales['q3'] + \
    (1.5 * monthly_sales['iqr'])

# Flag outliers based on bounds
monthly_sales['is_outlier'] = (
    (monthly_sales['sales_volume'] < monthly_sales['lower_bound']) |
    (monthly_sales['sales_volume'] > monthly_sales['upper_bound'])
)

# Extract outlier months and their sales volumes
outliers_df = (
    monthly_sales
    .query("is_outlier == True")
    .filter(items=['tran_month', 'sales_volume'])
    .rename(columns={'tran_month': 'month'})
)

# Display the outliers DataFrame
print(outliers_df)
