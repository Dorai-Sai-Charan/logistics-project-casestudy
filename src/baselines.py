import pandas as pd
from .aggregation import ROUTE_COLUMNS


def add_baselines(weekly: pd.DataFrame, history_weeks: int = 8) -> pd.DataFrame:
    df = weekly.copy().sort_values(ROUTE_COLUMNS + ["week_of"], kind="mergesort").reset_index(drop=True)
    history = df.groupby(ROUTE_COLUMNS, sort=False)["cost_per_tonne_km"].transform(
        lambda s: s.shift(1).rolling(history_weeks, min_periods=1).mean()
    )
    df["historical_baseline"] = history
    peer_key = ["route_type", "week_of"]
    totals = df.groupby(peer_key)["cost_per_tonne_km"].transform("sum")
    counts = df.groupby(peer_key)["cost_per_tonne_km"].transform("count")
    df["peer_baseline"] = (totals - df["cost_per_tonne_km"]) / (counts - 1)
    df.loc[counts <= 1, "peer_baseline"] = float("nan")
    return df.sort_values(ROUTE_COLUMNS + ["week_of"], kind="mergesort").reset_index(drop=True)
