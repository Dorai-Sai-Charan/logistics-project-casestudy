# Requirements analysis

## Source inspection
The workspace contains `FreightTiger_Intern_CaseStudy.docx`; the requested PDF was not present. The DOCX was extracted from its XML and is treated as the authoritative case-study brief. Supplied inputs are `shipment_records.csv` (2,940 records), `context_notes.csv` (10 notes), and `sample_output_format_v2.csv`.

## Checklist and traceability

| Requirement from brief | Implementation | Verification |
|---|---|---|
| Group by origin, destination, and supplied route_type | `src/aggregation.py` | `tests/test_aggregation.py` |
| Monday-Sunday weeks and Monday `week_of` | `monday_week_start` | `tests/test_aggregation.py` |
| Weighted cost = total freight / total tonne-km | `aggregate_weekly` | `tests/test_aggregation.py` |
| Trailing eight prior weekly observations, no look-ahead | `src/baselines.py` | `tests/test_baselines.py` |
| Same-week, same-route_type peer mean excluding target | `src/baselines.py` | `tests/test_baselines.py` |
| Flag unusual positive rise | configurable 20% threshold in `src/config.py` / `anomaly_detection.py` | `tests/test_anomaly_detection.py` |
| Check notes before final verdict and cite exact note ID | `src/context_retrieval.py` | `tests/test_context_retrieval.py` |
| Exact sample output header/order | `src/output_writer.py` | `tests/test_output.py` |
| Lightweight evaluation and reproducibility | `src/pipeline.py`, `output/evaluation_report.txt` | `tests/test_pipeline.py` and three-run hash comparison |
| README, code, output, reproducibility, token/cost log | `README.md`, `src/`, `output/` | final inspection |

## Data quality findings
- Shipment schema has ten expected columns; all 2,940 rows are valid under the implemented policy.
- No nulls, nonpositive numeric fields, invalid dates, or full duplicate shipment records were found.
- Dates span 2024-01-01 through 2025-12-28.
- Route types are Short, Medium, and Long. Route type is never inferred from distance.
- The supplied sample output has the expected eight-column header, but at least one example reason contains an unquoted comma and is not parseable by strict CSV readers. It is not modified; the implementation uses its visible header contract and emits valid CSV.

## Explicit implementation choices and ambiguities
1. The brief does not provide a numeric anomaly threshold. A 20% positive increase versus either available baseline is used, centralized and configurable. This is an implementation assumption, not an official case-study rule.
2. Rows with no historical or peer baseline are not flagged solely due to missing history.
3. Only existing route-week observations are emitted; missing weeks are not fabricated or treated as zero.
4. A supporting context note must match the exact route (or All Routes), overlap the route week, and contain explicit positive cost-impact language. Explicit exclusions, negligible/no-impact statements, and normal/stable statements are rejected as support.
5. No LLM is used because deterministic retrieval and templates satisfy the evidence and explanation requirements without API cost or nondeterminism.
6. The requested PDF is unavailable; the DOCX is the source used for requirements extraction.
