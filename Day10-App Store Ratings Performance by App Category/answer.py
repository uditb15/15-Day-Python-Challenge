import pandas as pd
import numpy as np

# importing data
app_ratings = pd.read_csv(
    "app_ratings.csv",
    dtype={
        "app_id": "string",
        "category": "string",
        "rating": "string"
    },
    parse_dates=["review_date"]
)

# Question 1
app_ratings['rating'] = app_ratings['rating'].str.strip()

app_ratings['rating'] = app_ratings['rating'].str.replace(",", '.')

app_ratings['rating'] = app_ratings['rating'].replace(
    ["not available", "five"],
    pd.NA
)

app_ratings['rating'] = app_ratings['rating'].astype('float')

print(app_ratings['rating'].head(5))


# Question 2

app_ratings['rating'] = app_ratings['rating'].astype('float')

print(app_ratings.head(5))
print(app_ratings.tail(5))

# Question 3

rating_summ = app_ratings.dropna().groupby('category', as_index=False).agg(
    {
        'rating': ['mean', np.median, 'std']
    }
)

rating_summ.columns = ['category', 'mean', 'median', 'std']

print(rating_summ)
