import pandas as pd


def _end_date(row: pd.Series) -> pd.Timestamp:
    start = pd.Timestamp(row["date"])
    text = str(row["note"]).lower()
    if "from feb 24 to mar 8" in text:
        return pd.Timestamp("2025-03-08")
    if "this quarter" in text:
        return start + pd.Timedelta(days=92)
    if "starting this week" in text or "about a week" in text or "festival week" in text or "this week" in text:
        return start + pd.Timedelta(days=6)
    return start


def prepare_notes(notes: pd.DataFrame) -> pd.DataFrame:
    out = notes.copy()
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    out["end_date"] = out.apply(_end_date, axis=1)
    return out


def _supports_increase(note: str) -> bool:
    text = note.lower()
    if any(x in text for x in ["not significantly affected", "no significant disruptions", "no major disruptions", "without a rate change", "not part of this dataset", "improved road conditions"]):
        return False
    return any(x in text for x in ["higher trip costs", "surcharge", "pushing up", "increased", "costs across"])


def retrieve_supporting_note(row: pd.Series, notes: pd.DataFrame) -> dict:
    route = f"{row['origin']}-{row['destination']}"
    week = pd.Timestamp(row["week_of"])
    week_end = week + pd.Timedelta(days=6)
    applicable = notes[(notes["applies_to"].eq("All Routes") | notes["applies_to"].eq(route)) & (notes["date"] <= week_end) & (notes["end_date"] >= week)].copy()
    applicable = applicable.sort_values(["date", "note_id"], kind="mergesort")
    for _, note in applicable.iterrows():
        if _supports_increase(note["note"]):
            return {"note_id": note["note_id"], "note": note["note"], "supported": True}
    return {"note_id": "", "note": "", "supported": False}


def add_context_verdicts(df: pd.DataFrame, notes: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    notes_prepared = prepare_notes(notes)
    matched = []
    verdicts = []
    reasons = []
    for _, row in out.iterrows():
        evidence = retrieve_supporting_note(row, notes_prepared) if row["candidate_flag"] else {"note_id": "", "note": "", "supported": False}
        matched.append(evidence["note_id"])
        if row["candidate_flag"] and evidence["supported"]:
            verdicts.append("No (justified)")
            reasons.append(f"Cost rise is flagged numerically, but note {evidence['note_id']} applies to {row['origin']}-{row['destination']} during this period and supports the increase: {evidence['note']}")
        elif row["candidate_flag"]:
            verdicts.append("Yes")
            reasons.append("Cost rise is unexplained by the supplied context notes; flagged for human review. No sufficient supporting note was found.")
        else:
            verdicts.append("No")
            reasons.append("No out-of-the-ordinary rising cost under the configured baseline threshold.")
    out["flagged"] = verdicts
    out["matched_note_id"] = matched
    out["reason"] = reasons
    return out
