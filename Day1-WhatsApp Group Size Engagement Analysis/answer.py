import pandas as pd

# Question 1
dim_groups = pd.read_csv("data.csv",
                         dtype={
                             "group_id": "int",
                             "participant_count": "int",
                             "total_messages": "float"
                         },
                         parse_dates=["created_date"]
                         )
print(dim_groups[dim_groups['created_date'].dt.to_period(
    'M') == '2024-10'].participant_count.max())

# Question 2
print(dim_groups[dim_groups['created_date'].dt.to_period(
    'M') == '2024-10'].participant_count.mean())

# Question 3
print(dim_groups[dim_groups['created_date'].dt.to_period(
    'M') == '2024-10'].query("participant_count>50").total_messages.mean())
