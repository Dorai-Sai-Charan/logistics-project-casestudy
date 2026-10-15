from pathlib import Path
import pandas as pd
from src.data_loader import load_inputs


def test_supplied_inputs_are_valid():
    root = Path(__file__).resolve().parents[1]
    loaded = load_inputs(root / "shipment_records.csv", root / "context_notes.csv")
    assert len(loaded.shipments) == 2940
    assert int(loaded.quality_report.loc[loaded.quality_report.metric == "rejected_rows", "value"].iloc[0]) == 0


def test_invalid_file_has_actionable_error(tmp_path):
    try:
        load_inputs(tmp_path / "missing.csv", tmp_path / "notes.csv")
    except FileNotFoundError as exc:
        assert "Required input file not found" in str(exc)
    else:
        raise AssertionError("Expected missing-file error")
