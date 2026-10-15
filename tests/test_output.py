import pandas as pd
from src.output_writer import OUTPUT_COLUMNS, to_output_frame


def test_output_contract():
    df = pd.DataFrame([{ "origin": "A", "destination": "B", "week_of": pd.Timestamp("2024-01-01"), "cost_per_tonne_km": 1.234, "history_change": 0.2, "peer_change": None, "flagged": "Yes", "matched_note_id": "", "reason": "review" }])
    out = to_output_frame(df)
    assert list(out.columns) == OUTPUT_COLUMNS
    assert out.iloc[0].route == "A-B"
    assert out.iloc[0].cost_per_tonne_km == 1.23
