import pandas as pd
from src.context_retrieval import prepare_notes, retrieve_supporting_note


def make_row(route="Chennai-Bangalore", week="2025-02-24"):
    origin, destination = route.split("-")
    return pd.Series({"origin": origin, "destination": destination, "week_of": pd.Timestamp(week)})


def test_route_and_date_specific_support():
    notes = pd.DataFrame([{ "note_id": "N1", "date": "2025-02-24", "applies_to": "Chennai-Bangalore", "note": "Flooding forced detours and higher trip costs from Feb 24 to Mar 8." }])
    result = retrieve_supporting_note(make_row(), prepare_notes(notes))
    assert result["note_id"] == "N1"


def test_non_supportive_and_wrong_route_are_not_matches():
    notes = pd.DataFrame([
        {"note_id": "N1", "date": "2025-02-24", "applies_to": "Delhi-Jaipur", "note": "Flooding forced higher trip costs."},
        {"note_id": "N2", "date": "2025-02-24", "applies_to": "Chennai-Bangalore", "note": "Costs were not significantly affected."},
    ])
    result = retrieve_supporting_note(make_row(), prepare_notes(notes))
    assert result["note_id"] == ""


def test_all_routes_positive_note_matches():
    notes = pd.DataFrame([{ "note_id": "N3", "date": "2025-05-05", "applies_to": "All Routes", "note": "Diesel prices rose nationwide, pushing up transportation costs across all routes." }])
    result = retrieve_supporting_note(make_row("Mumbai-Pune", "2025-05-05"), prepare_notes(notes))
    assert result["note_id"] == "N3"
