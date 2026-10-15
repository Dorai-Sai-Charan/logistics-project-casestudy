from pathlib import Path
from src.config import Config
from src.pipeline import run_pipeline
from src.output_writer import OUTPUT_COLUMNS


def test_full_pipeline_contract(tmp_path):
    root = Path(__file__).resolve().parents[1]
    config = Config(root, tmp_path)
    result = run_pipeline(config)
    assert list(result.columns) == OUTPUT_COLUMNS
    assert len(result) > 0
    assert not result.duplicated(["route", "week_of"]).any()
    assert result["cost_per_tonne_km"].notna().all()


def test_visible_sample_cases_are_regressions(tmp_path):
    root = Path(__file__).resolve().parents[1]
    result = run_pipeline(Config(root, tmp_path))
    cases = result.set_index(["route", "week_of"])
    assert cases.loc[("Delhi-Jaipur", "2024-11-11"), "cost_per_tonne_km"] == 4.17
    assert cases.loc[("Delhi-Jaipur", "2024-11-11"), "flagged"] == "Yes"
    assert cases.loc[("Ahmedabad-Mumbai", "2025-01-20"), "matched_note_id"] == "N002"
    assert cases.loc[("Ahmedabad-Mumbai", "2025-01-20"), "flagged"] == "No (justified)"
    assert cases.loc[("Mumbai-Pune", "2025-09-15"), "matched_note_id"] == ""
    assert cases.loc[("Mumbai-Pune", "2025-09-15"), "flagged"] == "Yes"
