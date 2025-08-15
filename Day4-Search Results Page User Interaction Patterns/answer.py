import pandas as pd

user_engagement_data = pd.read_csv("user_engagement_data.csv",
                                   dtype={
                                       "user_id": "string",
                                       "interaction_time": "float64",
                                       "search_results_displayed": "Int64"
                                   },
                                   parse_dates=["interaction_date"]
                                   )

# Question 1
duplicates = user_engagement_data.duplicated()
num_duplicates = duplicates.sum()
print(num_duplicates)
cleaned_data = user_engagement_data.drop_duplicates()
print(cleaned_data)


# Question 2
clean_data = user_engagement_data.drop_duplicates()

avg_interaction_by_results = (
    clean_data
    .groupby('search_results_displayed')['interaction_time']
    .mean()
    .reset_index()
)

print(avg_interaction_by_results)

# Question 3

avg_interaction_by_results = (
    cleaned_data
    .groupby('search_results_displayed')['interaction_time']
    .mean()
    .reset_index()
)

avg_interaction_by_results = avg_interaction_by_results.sort_values(
    by='interaction_time',
    ascending=False
)

print(
    'optimal search results per page is',
    avg_interaction_by_results.iloc[0]
)
