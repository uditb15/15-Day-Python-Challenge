import pandas as pd

# loading data
import pandas as pd

fct_guest_spending = pd.read_csv(
    "fct_guest_spending.csv",
    dtype={
        "guest_id": "int64",
        "park_experience_type": "string",
        "amount_spent": "float64"
    },
    parse_dates=["visit_date"]
)


# Question 1
# Step 1: Filter July 2024 data
july_data = (
    fct_guest_spending
    [
        (fct_guest_spending['visit_date'].dt.year == 2024) &
        (fct_guest_spending['visit_date'].dt.month == 7)
    ]
)

# Step 2: Calculating average amount spent per guest per visit per experience
avg_spending = (
    july_data.groupby('park_experience_type')['amount_spent']
    .mean()
    .reset_index()
    .rename(columns={'amount_spent': 'avg_spending_per_visit'})
)

# Step 3: Get full list of park experience types from original data
all_types = pd.DataFrame(
    {
        'park_experience_type': fct_guest_spending['park_experience_type'].unique()
    }
)

# Step 4: Left join so that we get all park_experience_types
result = pd.merge(all_types, avg_spending,
                  on='park_experience_type', how='left').fillna(0.0)

print(result)

# Question 2

# Step 1: Filter for August 2024
aug_data = (
    fct_guest_spending
    [
        (fct_guest_spending['visit_date'].dt.year == 2024) &
        (fct_guest_spending['visit_date'].dt.month == 8)
    ]
)

# Step 2: Aggregate total spending per guest per visit_date
guest_visits = aug_data.groupby(['guest_id', 'visit_date'], as_index=False)[
    'amount_spent'].sum()

# Step 3: Guests with more than one visit
visit_counts = guest_visits['guest_id'].value_counts()
multi_visit_guests = visit_counts[visit_counts > 1].index
multi_visit_data = guest_visits[guest_visits['guest_id'].isin(
    multi_visit_guests)]

# Step 4: Get first and last visit dates
first_last = (
    multi_visit_data.groupby('guest_id')
    .agg(
        first_visit_date=('visit_date', 'min'),
        last_visit_date=('visit_date', 'max')
    )
    .reset_index()
)

# Step 5: Merge with aggregated guest_visits to get spending
first_spending = (
    guest_visits
    .merge(first_last[['guest_id', 'first_visit_date']], left_on=['guest_id', 'visit_date'], right_on=['guest_id', 'first_visit_date'])[['guest_id', 'amount_spent']]
    .rename(columns={'amount_spent': 'first_spending'})
)

last_spending = (
    guest_visits
    .merge(first_last[['guest_id', 'last_visit_date']], left_on=['guest_id', 'visit_date'], right_on=['guest_id', 'last_visit_date'])[['guest_id', 'amount_spent']]
    .rename(columns={'amount_spent': 'last_spending'})
)

# Step 6: Merge and calculate difference
spending_diff = pd.merge(first_spending, last_spending, on='guest_id')
spending_diff['spending_difference'] = spending_diff['last_spending'] - \
    spending_diff['first_spending']

print(spending_diff[['guest_id', 'spending_difference']])


# September data
september_data = fct_guest_spending[
    (fct_guest_spending['visit_date'].dt.year == 2024) &
    (fct_guest_spending['visit_date'].dt.month == 9)
]

# Step 2: Finding total spending by each guest
guests_spending = september_data.groupby('guest_id', as_index=False)[
    'amount_spent'].sum()

# Define spending bins and labels
bins = [0, 50, 100, float('inf')]
labels = ['Low', 'Medium', 'High']

# Categorize guests based on total spending
guests_spending['spending_segment'] = pd.cut(
    guests_spending['amount_spent'],
    labels=labels,
    bins=bins,
    include_lowest=True,
    right=False
)

# Filter out guests who did not spend anything
guests_spending = guests_spending.query('amount_spent > 0')

# Final result
print(guests_spending[['guest_id', 'spending_segment']])

# Question 3

# September data
september_data = fct_guest_spending[
    (fct_guest_spending['visit_date'].dt.year == 2024) &
    (fct_guest_spending['visit_date'].dt.month == 9)
]

# Step 2: Finding total spending by each guest
guests_spending = september_data.groupby('guest_id', as_index=False)[
    'amount_spent'].sum()

# Define spending bins and labels
bins = [0, 50, 100, float('inf')]
labels = ['Low', 'Medium', 'High']

# Categorize guests based on total spending
guests_spending['spending_segment'] = pd.cut(
    guests_spending['amount_spent'],
    labels=labels,
    bins=bins,
    include_lowest=True,
    right=False
)

# Filter out guests who did not spend anything
guests_spending = guests_spending.query('amount_spent > 0')

# Final result
print(guests_spending[['guest_id', 'spending_segment']])
