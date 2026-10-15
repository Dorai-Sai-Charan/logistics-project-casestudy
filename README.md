# FreightTiger Smart Shipping-Cost Assistant

A deterministic pandas pipeline that identifies unusual weekly shipping-cost increases, compares them with route history and same-type peers, and grounds explanations in supplied context notes.

## Features
- Validates shipment and context schemas and writes a data-quality report.
- Aggregates valid shipments into Monday-starting route weeks using weighted tonne-kilometres.
- Computes the trailing eight prior weekly cost values and same-week same-`route_type` peer averages.
- Flags positive increases of at least the configurable 20% threshold versus either available baseline.
- Uses exact-route or `All Routes` note matching, date overlap, and explicit support/exclusion rules.
- Produces the required eight-column output CSV with stable ordering.
- Uses no LLM or network/API key for the core run; LLM calls and token cost are zero/not applicable.

## Setup and execution
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
python -m pytest -q
```

The generated files are `output/freight_cost_analysis.csv`, `output/data_quality_report.csv`, `output/evaluation_report.txt`, `output/reproducibility_check.txt`, and `output/token_cost_log.txt`. The original input files are never overwritten.

For WSL, use `source .venv/bin/activate` and run the same Python commands. The submitted WSL environment was placed on the native Linux filesystem and exposed through the project `.venv` link to avoid pip corruption on the mounted Windows drive.

## Calculations
For each route (`origin`, `destination`, `route_type`) and existing calendar week:

`cost_per_tonne_km = sum(freight_cost_inr) / sum(quantity_tonnes * distance_km)`.

History is the mean of up to the eight immediately preceding *observed* route-week costs, strictly before the current week. Missing calendar weeks are not zeros. The peer baseline is the mean of other routes with the same `route_type` in the same week; the target route is excluded.

The case brief does not specify a numeric threshold. This implementation assumes 20% and applies it when the current cost is at least 20% above either available positive baseline. Missing/zero baselines do not trigger flags. A numerical candidate with a genuine supporting note becomes `No (justified)`; otherwise it remains `Yes` for human review. Non-supportive notes never become matched evidence.

## Inputs and output
- `shipment_records.csv`: shipment-level records and supplied route type.
- `context_notes.csv`: dated route-specific or broad notes.
- `sample_output_format_v2.csv`: visible output header contract. The supplied examples contain an unquoted comma in one reason field, so the sample is not strict-CSV parseable; it is preserved unchanged.

Output columns, in exact order: `route`, `week_of`, `cost_per_tonne_km`, `vs_own_history`, `vs_similar_routes`, `flagged`, `matched_note_id`, `reason`.

## Evidence rules
A note is supporting only when its scope is exact or genuinely broad, its effective period overlaps the route week, and its text explicitly supports higher costs. Notes stating no/low impact, stable movement, dataset exclusion, or absorbed costs are not used to justify a rise. Exact source `note_id` values are preserved.

## Testing and reproducibility
The test suite uses hand-calculated synthetic datasets for aggregation, date boundaries, rolling history leakage, peer exclusion/type isolation, threshold boundaries, evidence scope/date/support rules, and output schema. To reproduce the submitted check:

```powershell
python main.py
Copy-Item output\freight_cost_analysis.csv output\run1.csv
python main.py
Copy-Item output\freight_cost_analysis.csv output\run2.csv
python main.py
Copy-Item output\freight_cost_analysis.csv output\run3.csv
Get-FileHash output\run1.csv,output\run2.csv,output\run3.csv -Algorithm SHA256
```

The three completed runs used identical inputs and configuration and produced identical output hashes. Their verified hashes are recorded in `output/reproducibility_check.txt`. Explanations are deterministic templates, so wording is also stable. The evaluation report records row counts, duplicate checks, and the no-LLM cost log; `output/token_cost_log.txt` provides the standalone submission log.

## Limitations and submission notes
The case-study brief supplied in the workspace is DOCX rather than the requested PDF; no claims are made about unavailable PDF-only requirements. The 20% anomaly threshold is a documented assumption because the brief defines comparison baselines but no numeric cutoff. Missing weeks are intentionally omitted rather than imputed. The project contains no optional question-answering UI because it is a stretch goal.
