from pathlib import Path
from src.config import Config
from src.pipeline import run_pipeline, write_evaluation_report


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    config = Config(data_dir=root, output_dir=root / "output")
    result = run_pipeline(config)
    write_evaluation_report(config, result)
    print(f"Wrote {len(result)} route-week rows to {config.output_path}")
