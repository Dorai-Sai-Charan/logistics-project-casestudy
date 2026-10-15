import numpy as np
import pandas as pd


def _pct_change(current: float, baseline: float) -> float:
    if pd.isna(current) or pd.isna(baseline) or baseline <= 0:
        return float("nan")
    return (current - baseline) / baseline


def classify_anomalies(df: pd.DataFrame, threshold: float = 0.20) -> pd.DataFrame:
    out = df.copy()
    out["history_change"] = [_pct_change(a, b) for a, b in zip(out["cost_per_tonne_km"], out["historical_baseline"])]
    out["peer_change"] = [_pct_change(a, b) for a, b in zip(out["cost_per_tonne_km"], out["peer_baseline"])]
    out["candidate_flag"] = ((out["history_change"] >= threshold) | (out["peer_change"] >= threshold)).fillna(False)
    out["candidate_flag"] = out["candidate_flag"].astype(bool)
    out["flagged"] = np.where(out["candidate_flag"], "Yes", "No")
    return out
