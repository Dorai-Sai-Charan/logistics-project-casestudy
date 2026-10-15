import pandas as pd
from src.anomaly_detection import classify_anomalies


def test_threshold_and_missing_baseline_behavior():
    df = pd.DataFrame({"cost_per_tonne_km": [120, 119, 80, 120], "historical_baseline": [100, 100, 100, None], "peer_baseline": [None, None, 100, 0]})
    out = classify_anomalies(df, threshold=0.20)
    assert list(out.candidate_flag) == [True, False, False, False]
    assert list(out.flagged) == ["Yes", "No", "No", "No"]
