import pandas as pd
import numpy as np


# importing data
import pandas as pd

fct_trips = pd.read_csv(
    "fct_trips.csv",
    dtype={
        "trip_id": "int64",
        "driver_id": "int64",
        "rider_count": "int64",
        "ride_type": "string",
        "total_distance": "float64",
        "total_earnings": "float64"
    },
    parse_dates=["trip_date"]
)


# Question 1
uber_pool_q3_2024 = fct_trips.query(
    "trip_date >= '2024-07-01' & trip_date <= '2024-09-30' & rider_count > 2 & ride_type == 'UberPool'")

print(uber_pool_q3_2024['total_earnings'].mean())


# Question 2
uber_pool_morethan2_riders = fct_trips.query(
    "trip_date >= '2024-07-01' & trip_date <= '2024-09-30' & rider_count > 2 & ride_type == 'UberPool'"
)

uber_pool_morethan2_riders['earnings_per_mile'] = (
    uber_pool_morethan2_riders['total_earnings'] /
    uber_pool_morethan2_riders['total_distance']
)

print(uber_pool_morethan2_riders['earnings_per_mile'].mean())


# Question 3
uber_pool_all_riders = fct_trips.query(
    "trip_date >= '2024-07-01' & trip_date <= '2024-09-30' & ride_type == 'UberPool'"
)

earnings_distance_rider_count = (
    uber_pool_all_riders
    .groupby(['total_distance', 'rider_count'], as_index=False)['total_earnings']
    .mean()
    .sort_values(by='total_earnings', ascending=False)
)

earnings_distance_rider_count['earning_rank'] = earnings_distance_rider_count['total_earnings'].rank(
    method='dense',
    ascending=False
)

highest_avg_earnings = (
    earnings_distance_rider_count
    .query("earning_rank == 1")
    .filter(items=['rider_count', 'total_distance', 'total_earnings'])
    .rename(columns={'total_earnings': 'averge_earnings'})
)

print(highest_avg_earnings)
