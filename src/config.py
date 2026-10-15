from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    data_dir: Path
    output_dir: Path
    history_weeks: int = 8
    anomaly_threshold: float = 0.20

    @property
    def shipments_path(self) -> Path:
        return self.data_dir / "shipment_records.csv"

    @property
    def notes_path(self) -> Path:
        return self.data_dir / "context_notes.csv"

    @property
    def sample_output_path(self) -> Path:
        return self.data_dir / "sample_output_format_v2.csv"

    @property
    def output_path(self) -> Path:
        return self.output_dir / "freight_cost_analysis.csv"

    @property
    def quality_report_path(self) -> Path:
        return self.output_dir / "data_quality_report.csv"

    @property
    def evaluation_report_path(self) -> Path:
        return self.output_dir / "evaluation_report.txt"
