import pandas as pd

ROUTE_COLUMNS = ["origin", "destination", "route_type"]


def monday_week_start(values: pd.Series) -> pd.Series:
    dates = pd.to_datetime(values)
    return dates - pd.to_timedelta(dates.dt.weekday, unit="D")


def aggregate_weekly(shipments: pd.DataFrame) -> pd.DataFrame:
    df = shipments.copy()
    df["week_of"] = monday_week_start(df["shipment_date"])
    df["tonne_km"] = df["quantity_tonnes"] * df["distance_km"]
    grouped = (df.groupby(ROUTE_COLUMNS + ["week_of"], as_index=False)
        .agg(total_freight_cost_inr=("freight_cost_inr", "sum"), total_tonne_km=("tonne_km", "sum"), shipment_count=("shipment_id", "count")))
    grouped["cost_per_tonne_km"] = grouped["total_freight_cost_inr"] / grouped["total_tonne_km"]
    grouped.loc[grouped["total_tonne_km"] <= 0, "cost_per_tonne_km"] = float("nan")
    return grouped.sort_values(ROUTE_COLUMNS + ["week_of"], kind="mergesort").reset_index(drop=True)
