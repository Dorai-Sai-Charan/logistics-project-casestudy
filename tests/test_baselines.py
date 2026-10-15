import pandas as pd
from src.baselines import add_baselines


def test_history_excludes_current_and_uses_prior_eight():
    rows = []
    for i, value in enumerate([1, 2, 3, 4, 5, 6, 7, 8, 9], start=1):
        rows.append({"origin": "A", "destination": "B", "route_type": "Short", "week_of": pd.Timestamp("2024-01-01") + pd.Timedelta(days=7 * i), "cost_per_tonne_km": value})
    out = add_baselines(pd.DataFrame(rows), 8)
    assert pd.isna(out.iloc[0].historical_baseline)
    assert out.iloc[8].historical_baseline == 4.5


def test_peer_excludes_target_and_isolates_type():
    df = pd.DataFrame([
        {"origin": "A", "destination": "B", "route_type": "Short", "week_of": pd.Timestamp("2024-01-01"), "cost_per_tonne_km": 10.0},
        {"origin": "C", "destination": "D", "route_type": "Short", "week_of": pd.Timestamp("2024-01-01"), "cost_per_tonne_km": 20.0},
        {"origin": "E", "destination": "F", "route_type": "Long", "week_of": pd.Timestamp("2024-01-01"), "cost_per_tonne_km": 100.0},
    ])
    out = add_baselines(df)
    assert out.iloc[0].peer_baseline == 20.0
    assert out.iloc[1].peer_baseline == 10.0
    assert pd.isna(out.iloc[2].peer_baseline)
