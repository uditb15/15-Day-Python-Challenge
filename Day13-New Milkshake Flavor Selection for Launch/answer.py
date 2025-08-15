import pandas as pd

# importing data
milkshake_ratings = pd.read_csv(
    "milkshake_ratings.csv",
    dtype={
        "customer_id": "string",
        "flavor": "string",
        "rating": "float"
    },
    parse_dates=["rating_date"]
)


# Q1
cleaned = milkshake_ratings[~milkshake_ratings.duplicated()]
print(cleaned.head())


# Q2
cleaned = milkshake_ratings[~milkshake_ratings.duplicated()]

flavor_mean = (
    cleaned
    .groupby('flavor', as_index=False, sort=False)['rating']
    .mean()
    .rename(
        columns={
            'rating': 'average_rating'
        }
    )
)

merged_flavors_clean = pd.merge(milkshake_ratings, flavor_mean, on='flavor')

print(merged_flavors_clean.head())

# Q3
cleaned = milkshake_ratings[~milkshake_ratings.duplicated()]
cleaned = cleaned[~cleaned['rating'].isna()]

flavor_mean = (
    cleaned
    .groupby('flavor', as_index=False, sort=False)['rating']
    .mean()
    .round(1)
    .rename(
        columns={
            'rating': 'average_rating'
        }
    )
)

merged_flavors_clean = pd.merge(cleaned, flavor_mean, on='flavor')

merged_flavors_clean['diff'] = (
    merged_flavors_clean['rating'] -
    merged_flavors_clean['average_rating']
).round(1)

print(merged_flavors_clean.head())
