# FreightTiger Case Study — Project Overview

## 1. Problem statement

FreightTiger wants to monitor shipping costs and identify route-week combinations where the cost of moving goods appears unusually high. A cost increase may be justified by events such as fuel-price changes, flooding, festivals, or surcharges, or it may require human investigation.

The project builds a deterministic assistant that calculates weekly shipping cost per tonne-kilometre, compares each route with its own recent history and with peer routes, detects unusual increases, and explains flagged results using the supplied context notes.

The case-study requirements were taken from `FreightTiger_Intern_CaseStudy.docx`. The requested PDF was not present in the workspace.

## 2. Main requirements

- Validate `shipment_records.csv` and `context_notes.csv` without modifying the source files.
- Group shipments by origin, destination, and the supplied `route_type`.
- Use Monday-to-Sunday calendar weeks and represent each week by its Monday date.
- Calculate weighted weekly cost per tonne-kilometre:

  `sum(freight_cost_inr) / sum(quantity_tonnes * distance_km)`

- Compare each route-week with:
  - the mean of up to the eight immediately preceding observed route-week costs;
  - the same-week average of other routes having the same `route_type`.
- Detect positive cost increases using a configurable 20% threshold. The threshold is an implementation assumption because the brief does not define a numeric threshold.
- Check context notes for exact route/date applicability and reject non-supportive or irrelevant evidence.
- Cite the original note ID when a supporting explanation exists.
- Produce the required eight-column CSV output.
- Keep the results deterministic, testable, and reproducible.

A vector database or LLM is not required for the core calculations. The project uses lightweight deterministic retrieval because the supplied context file contains only a small number of explicit, dated notes.

## 3. Implementation summary

The implementation is a pandas-based Python pipeline:

1. **Load and validate data** — required files, columns, dates, numeric values, missing values, invalid values, and duplicates are checked.
2. **Aggregate weekly costs** — valid shipments are assigned to Monday-starting weeks and aggregated by route and route type.
3. **Calculate baselines** — historical and peer-route comparison values are calculated without future-data leakage.
4. **Detect anomalies** — positive changes at or above the configured threshold become numerical candidates.
5. **Retrieve context** — route scope, date overlap, and explicit supporting/non-supporting language are evaluated.
6. **Generate output** — deterministic explanations, note IDs, flags, and comparison text are written to the output CSV.
7. **Evaluate** — data-quality and evaluation reports are written, and automated tests verify the main behaviors.

## 4. Code files

| File | Responsibility |
|---|---|
| `main.py` | Starts the pipeline using paths relative to the project root. |
| `src/config.py` | Stores input/output paths, history-window size, and anomaly threshold. |
| `src/data_loader.py` | Loads CSV files, validates schemas and records, and creates the data-quality report. |
| `src/aggregation.py` | Assigns Monday week starts and calculates weighted weekly cost per tonne-kilometre. |
| `src/baselines.py` | Calculates the trailing eight-week history and same-week peer baselines. |
| `src/anomaly_detection.py` | Calculates percentage changes and numerical candidate flags. |
| `src/context_retrieval.py` | Matches route/date context notes and creates evidence-grounded verdicts. |
| `src/output_writer.py` | Formats and writes the required output and quality-report CSV files. |
| `src/pipeline.py` | Connects all processing stages and writes the evaluation report. |
| `tests/` | Contains unit, regression, data-validation, retrieval, and end-to-end tests. |
| `docs/requirements_analysis.md` | Records the requirements checklist, traceability, findings, and assumptions. |
| `output/` | Stores generated analysis, quality, and evaluation reports. |

## 5. Code flow

```text
shipment_records.csv + context_notes.csv
                |
                v
        data_loader.py
   validation and quality report
                |
                v
        aggregation.py
  route-week weighted cost values
                |
                v
         baselines.py
 history and peer comparisons
                |
                v
     anomaly_detection.py
  numerical candidate flags
                |
                v
     context_retrieval.py
 evidence checks and explanations
                |
                v
       output_writer.py
 required analysis CSV + reports
```

`main.py` creates the `Config` object and calls `run_pipeline()` in `src/pipeline.py`. The pipeline stages run in the order shown above.

## 6. Setup and run

From the project root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the application:

```powershell
python main.py
```

Run the tests:

```powershell
python -m pytest -q
```

Generated files:

- `output/freight_cost_analysis.csv` — route-week analysis and explanations.
- `output/data_quality_report.csv` — input validation counts and rejection reasons.
- `output/evaluation_report.txt` — output checks and LLM usage accounting.

The original input files are not overwritten. The core project requires no API key, hosted model, vector database, or network connection.
