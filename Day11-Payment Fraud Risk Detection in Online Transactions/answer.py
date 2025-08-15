# Q1
import pandas as pd

# importing data
dim_risk_flags = pd.read_csv(
    "dim_risk_flags.csv",
    dtype={
        "risk_flag_id": "int",
        "transaction_id": "int",
        "risk_level": "string"
    }
)


fct_transactions = pd.read_csv(
    "fct_transactions.csv",
    dtype={
        "transaction_id": "int",
        "customer_email": "string",
        "transaction_amount": "float",
        "fraud_detection_score": "int"
    },
    parse_dates=["transaction_date"]
)


fct_transactions['tran_yearmon'] = (
    fct_transactions['transaction_date']
    .dt.to_period("M")
    .astype("str")
)

october_transactions = fct_transactions.query("tran_yearmon == '2024-10'")

exclude_domains = ('gmail.com', 'yahoo.com', 'hotmail.com')

excluded = october_transactions[
    ~october_transactions['customer_email'].str.endswith(exclude_domains)
]

print(len(excluded['transaction_id']))


# Q2
fct_transactions['tran_yearmon'] = (
    fct_transactions['transaction_date']
    .dt.to_period("M")
    .astype("str")
)

november_transactions = fct_transactions.query("tran_yearmon == '2024-11'")
november_transactions['transaction_amount'].fillna(0).mean()

high_risk = dim_risk_flags.query("risk_level == 'High'")
high_risk_trans = pd.merge(fct_transactions, high_risk, on="transaction_id")

day_counts = (
    high_risk_trans['transaction_date']
    .dt.day_name()
    .value_counts()
    .reset_index()
)

day_counts['rank'] = day_counts['count'].rank(method='dense', ascending=False)

print(day_counts.query("rank == 1").filter(
    items=['transaction_date', 'count']
).rename(
    columns={
        'transaction_date': 'day_of_week',
        'count': 'high_risk_transactions'
    }
)
)


# Q3
fct_transactions['tran_yearmon'] = (
    fct_transactions['transaction_date']
    .dt.to_period("M")
    .astype("str")
)

high_risk = dim_risk_flags.query("risk_level == 'High'")
dec_trans = fct_transactions.query("tran_yearmon == '2024-12'")

high_risk_trans = pd.merge(dec_trans, high_risk, on="transaction_id")

day_counts = (
    high_risk_trans['transaction_date']
    .dt.day_name()
    .value_counts()
    .reset_index(name='high_risk_transactions')
    .rename(columns={
        'transaction_date': 'day_of_week',
        'count': 'high_risk_transactions'
    })
)

day_counts['rank'] = day_counts['high_risk_transactions'].rank(ascending=False)

highest = day_counts.query("rank == 1").filter(
    items=['day_of_week', 'high_risk_transactions']
)

print(highest)
