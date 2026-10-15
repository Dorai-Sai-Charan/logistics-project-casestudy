from pathlib import Path
import numpy as np
import pandas as pd

OUTPUT_COLUMNS = ["route", "week_of", "cost_per_tonne_km", "vs_own_history", "vs_similar_routes", "flagged", "matched_note_id", "reason"]


def _format_change(value: float, label: str) -> str:
    if pd.isna(value):
        return ""
    return f"{value:+.1%} vs {label}"


def to_output_frame(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame({
        "route": df["origin"] + "-" + df["destination"],
        "week_of": pd.to_datetime(df["week_of"]).dt.strftime("%Y-%m-%d"),
        "cost_per_tonne_km": df["cost_per_tonne_km"].round(2),
        "vs_own_history": [_format_change(v, "this route's past average") for v in df["history_change"]],
        "vs_similar_routes": [_format_change(v, "similar-length routes this week") for v in df["peer_change"]],
        "flagged": df["flagged"],
        "matched_note_id": df["matched_note_id"].replace({np.nan: ""}),
        "reason": df["reason"],
    })
    return out[OUTPUT_COLUMNS]


def write_outputs(result: pd.DataFrame, quality: pd.DataFrame, output_path: Path, quality_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False, lineterminator="\n")
    quality.to_csv(quality_path, index=False, lineterminator="\n")
