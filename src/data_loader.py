from dataclasses import dataclass
from pathlib import Path
import pandas as pd

REQUIRED_SHIPMENT_COLUMNS = ["shipment_id", "origin", "destination", "route_type", "material", "quantity_tonnes", "distance_km", "freight_cost_inr", "shipment_date", "transporter"]
REQUIRED_NOTE_COLUMNS = ["note_id", "date", "applies_to", "note"]
NUMERIC_COLUMNS = ["quantity_tonnes", "distance_km", "freight_cost_inr"]


@dataclass
class LoadedData:
    shipments: pd.DataFrame
    notes: pd.DataFrame
    quality_report: pd.DataFrame


def _require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Required input file not found: {path}")


def _validate_columns(df: pd.DataFrame, required: list[str], path: Path) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in {path.name}: {missing}")


def load_inputs(shipments_path: Path, notes_path: Path) -> LoadedData:
    _require_file(shipments_path)
    _require_file(notes_path)
    shipments_raw = pd.read_csv(shipments_path)
    notes = pd.read_csv(notes_path)
    _validate_columns(shipments_raw, REQUIRED_SHIPMENT_COLUMNS, shipments_path)
    _validate_columns(notes, REQUIRED_NOTE_COLUMNS, notes_path)

    df = shipments_raw.copy()
    reasons = pd.Series("", index=df.index, dtype="object")
    for col in NUMERIC_COLUMNS:
        converted = pd.to_numeric(df[col], errors="coerce")
        reasons = reasons.mask(converted.isna(), reasons + f"invalid {col};")
        df[col] = converted
    dates = pd.to_datetime(df["shipment_date"], errors="coerce")
    reasons = reasons.mask(dates.isna(), reasons + "invalid shipment_date;")
    df["shipment_date"] = dates
    for col in ["shipment_id", "origin", "destination", "route_type", "material", "transporter"]:
        reasons = reasons.mask(df[col].isna() | (df[col].astype(str).str.strip() == ""), reasons + f"missing {col};")
    for col in ["quantity_tonnes", "distance_km", "freight_cost_inr"]:
        reasons = reasons.mask(df[col].notna() & (df[col] <= 0), reasons + f"nonpositive {col};")
    reasons = reasons.mask(df.duplicated(keep=False), reasons + "duplicate full record;")
    invalid = reasons.str.len().gt(0)
    quality = pd.DataFrame({"metric": ["input_rows", "valid_rows", "rejected_rows", "duplicate_rows"], "value": [len(df), int((~invalid).sum()), int(invalid.sum()), int(df.duplicated(keep=False).sum())]})
    reason_counts = reasons[invalid].str.rstrip(";").value_counts()
    if not reason_counts.empty:
        quality = pd.concat([quality, pd.DataFrame({"metric": [f"rejection_reason:{k}" for k in reason_counts.index], "value": reason_counts.values})], ignore_index=True)
    valid = df.loc[~invalid].copy()
    if valid.empty:
        raise ValueError("No valid shipment records remain after validation.")
    return LoadedData(valid, notes, quality)
