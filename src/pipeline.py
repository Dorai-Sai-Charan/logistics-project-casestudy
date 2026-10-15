from pathlib import Path
import pandas as pd
from .aggregation import aggregate_weekly
from .anomaly_detection import classify_anomalies
from .baselines import add_baselines
from .config import Config
from .context_retrieval import add_context_verdicts
from .data_loader import load_inputs
from .output_writer import to_output_frame, write_outputs


def run_pipeline(config: Config) -> pd.DataFrame:
    loaded = load_inputs(config.shipments_path, config.notes_path)
    weekly = aggregate_weekly(loaded.shipments)
    baselined = add_baselines(weekly, config.history_weeks)
    classified = classify_anomalies(baselined, config.anomaly_threshold)
    contextualized = add_context_verdicts(classified, loaded.notes)
    output = to_output_frame(contextualized)
    write_outputs(output, loaded.quality_report, config.output_path, config.quality_report_path)
    return output


def write_evaluation_report(config: Config, output: pd.DataFrame) -> None:
    lines = [
        "FreightTiger evaluation report",
        f"output_rows={len(output)}",
        f"output_columns={','.join(output.columns)}",
        f"duplicate_route_week_rows={int(output.duplicated(['route','week_of']).sum())}",
        f"finite_cost_values={bool(output['cost_per_tonne_km'].map(lambda x: pd.notna(x) and pd.api.types.is_number(x)).all())}",
        f"justified_rows={int((output['flagged'] == 'No (justified)').sum())}",
        f"unexplained_flagged_rows={int((output['flagged'] == 'Yes').sum())}",
        "llm_calls=0",
        "llm_tokens=not applicable; deterministic core pipeline",
        "llm_cost=0; no provider is required",
    ]
    config.evaluation_report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
