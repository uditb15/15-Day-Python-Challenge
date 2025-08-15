# Loading data

import pandas as pd

dim_product = pd.read_csv(
    "dim_product.csv",
    dtype={
        "product_id": "int64",
        "product_name": "string",
        "product_category": "string"
    }
)

fct_ad_performance = pd.read_csv(
    "fct_ad_performance.csv",
    dtype={
        "ad_id": "int64",
        "product_id": "int64",
        "clicks": "int64",
        "impressions": "int64"
    },
    parse_dates=["recorded_date"]
)


# Question 1
# Filter products by category
prods = dim_product[dim_product['product_category'].str.contains(
    "Electronics")]

# Filter ad performance data for October 2024
activity_october = fct_ad_performance[
    fct_ad_performance['recorded_date'].dt.strftime("%Y-%m") == '2024-10'
]

# Merge filtered datasets on 'product_id'
joined = pd.merge(prods, activity_october, on='product_id')

# Calculate average CTR (Click-Through Rate)
joined = joined.assign(average_ctr=joined['clicks'] / joined['impressions'])

# Optional: Filter specific columns if needed (unclear in your snippet)
# joined = joined.filter(items=['product_category', 'average_ctr'])

# Group by product category and compute mean CTR
result = joined.groupby('product_category', as_index=False)[
    'average_ctr'].mean().round(4)

# View result
print(result)


# Question 2
# average ctr by product category
activity_october = fct_ad_performance[
    fct_ad_performance['recorded_date'].dt.strftime("%Y-%m") == '2024-10'
]

joined = pd.merge(dim_product, activity_october, on='product_id')

joined = joined.assign(
    average_ctr=joined['clicks'] / joined['impressions']
).filter(items=['product_category', 'average_ctr'])

electronics_oct_ctr = joined.groupby(
    'product_category', as_index=False
)['average_ctr'].mean().round(4)

# overall average ctr
activity_october['ctr'] = activity_october['clicks'] / \
    activity_october['impressions']
avg_overall_ctr_oct = activity_october['ctr'].mean()

# ctr greater than overall average ctr
print(electronics_oct_ctr[electronics_oct_ctr['average_ctr'] > avg_overall_ctr_oct].rename(
    columns={
        'average_ctr': 'category_ctr'
    }
)
)

# Question 3

# Average CTR by product_category
activity_october = fct_ad_performance[
    fct_ad_performance['recorded_date'].dt.strftime("%Y-%m") == '2024-10'
]

joined = pd.merge(dim_product, activity_october, on='product_id')

joined = joined.assign(
    average_ctr=joined['clicks'] / joined['impressions']
).filter(items=['product_category', 'average_ctr'])

electronics_oct_ctr = joined.groupby(
    'product_category', as_index=False
)['average_ctr'].mean()

# overall average CTR
activity_october = fct_ad_performance[
    fct_ad_performance['recorded_date'].dt.strftime("%Y-%m") == '2024-10'
]

activity_october['ctr'] = activity_october['clicks'] / \
    activity_october['impressions']
avg_overall_ctr_oct = activity_october['ctr'].mean()

# Categories with CTR greater than overall average CTR
ctr_category_greater = electronics_oct_ctr[
    electronics_oct_ctr['average_ctr'] > avg_overall_ctr_oct
]

# percentage difference
ctr_category_greater['percentage_difference'] = (
    (ctr_category_greater['average_ctr'] -
     avg_overall_ctr_oct) / avg_overall_ctr_oct
) * 100

ctr_category_greater['percentage_difference'] = ctr_category_greater['percentage_difference'].round(
    2)

ctr_category_greater = (
    ctr_category_greater
    .rename(columns={'average_ctr': 'category_ctr'}
            )
)

ctr_category_greater['category_ctr'] = ctr_category_greater['category_ctr'].round(
    4)

print(ctr_category_greater)
