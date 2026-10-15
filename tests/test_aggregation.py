import pandas as pd
from src.aggregation import aggregate_weekly, monday_week_start


def test_monday_week_and_weighted_cost():
    df = pd.DataFrame({"shipment_id": ["a", "b"], "origin": ["A", "A"], "destination": ["B", "B"], "route_type": ["Short", "Short"], "quantity_tonnes": [2, 1], "distance_km": [10, 20], "freight_cost_inr": [100, 100], "shipment_date": pd.to_datetime(["2024-01-01", "2024-01-07"])})
    result = aggregate_weekly(df)
    assert result.loc[0, "week_of"] == pd.Timestamp("2024-01-01")
    assert result.loc[0, "cost_per_tonne_km"] == 200 / 40


def test_week_boundary_is_monday_to_sunday():
    values = pd.Series(pd.to_datetime(["2024-01-07", "2024-01-08"]))
    assert list(monday_week_start(values)) == [pd.Timestamp("2024-01-01"), pd.Timestamp("2024-01-08")]
