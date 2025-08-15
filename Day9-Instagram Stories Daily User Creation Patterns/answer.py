import pandas as pd
import numpy as np

# importing data
stories_data = pd.read_csv(
    "stories_data.csv",
    dtype={"user_id": "string", "story_count": "Int64"},
    parse_dates=["story_date"]
)


# Question 1
stories_data['story_date'] = pd.to_datetime(
    stories_data['story_date'],
    errors='coerce',
    dayfirst=False
)

stories_data['story_date'] = stories_data['story_date'].dt.strftime('%Y-%m-%d')

stories_data['story_date'] = pd.to_datetime(stories_data['story_date'])

print(stories_data)

# Question 2
user_story_counts = stories_data.groupby(
    ['user_id', 'story_date'],
    as_index=False
)['story_count'].sum()

percentile_users = stories_data.groupby(
    'story_date',
    as_index=False
).agg(
    p25=('story_count', lambda x: np.percentile(x, 25)),
    p50=('story_count', lambda x: np.percentile(x, 50)),
    p75=('story_count', lambda x: np.percentile(x, 75))
)

print(percentile_users)

# Question 3
stories_per_day = stories_data.groupby(
    ['user_id', 'story_date'],
    as_index=False
)['story_count'].sum()

more_than_ten = stories_per_day.query("story_count >= 10")

n_users = len(np.unique(more_than_ten['user_id']))

total_unique_users = len(np.unique(stories_per_day['user_id']))

print((n_users / total_unique_users) * 100)
