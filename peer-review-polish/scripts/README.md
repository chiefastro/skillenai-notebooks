# Analysis scripts

Everything needed to reproduce the report in the parent folder, in the order it was run.

## Configuration

Scripts read paths from environment variables so nothing is hardcoded:

| Variable | Default | Purpose |
|---|---|---|
| `PRP_DATA` | `_data` | Where collected notes are read from and written to |
| `PRP_OUT` | `.` | Where figures and CSVs are written |
| `PRP_DENYLIST` | `../synthetic-breakout-may-2026/network_domains_seed.csv` | Content-farm denylist, for judge calibration |
| `SKILLENAI_INSIGHTS_API_KEY` | — | Skillenai API (calibration corpus only) |
| `ANTHROPIC_API_KEY` | — | The blind LLM judge |

## Pipeline

```bash
export PRP_DATA=_data

# 1. Collect reviews and meta-reviews from OpenReview (no account needed)
python openreview_collect.py --kind review \
    --venues ICLR.cc/2024/Conference ICLR.cc/2025/Conference ICLR.cc/2026/Conference \
             NeurIPS.cc/2023/Conference NeurIPS.cc/2024/Conference NeurIPS.cc/2025/Conference \
    --out $PRP_DATA/reviews.jsonl
python openreview_collect.py --kind meta --out $PRP_DATA/meta.jsonl

# 2. Venue size (German tank estimator on submission numbers in signatures)
python openreview_collect.py --estimate-volume --in $PRP_DATA/reviews.jsonl

# 3. Typography, LLM-vocabulary and rhetorical tell panel, by venue-year
python typography_and_tells.py

# 4. Non-native English markers
python esl_markers.py

# 5. Blind LLM judge on reviews (costs Anthropic API credits)
python llm_judge.py

# 6. Judge calibration against known machine and known human content
python calibration_collect.py
python calibration_judge.py

# 7. Figures
python plot_report.py
python plot_calibration.py
```

## Notes on the scripts

`openreview_collect.py` carries the access constraints in its docstring — the important
one is that OpenReview search **requires a query term**, so corpora are assembled from
many terms and deduplicated. That is valid for per-review text properties and **not**
valid for estimating venue totals, which is why step 2 exists separately.

`tell_patterns.py` holds the regex tiers and is imported by the other tell scripts rather
than run directly. Tiers are kept separate on purpose: typography is high-precision
evidence of composition outside the review box, while register-ambiguous words like
`robust` and `comprehensive` are normal reviewer vocabulary and are never headlined.

`llm_judge.py` and `calibration_judge.py` use structured outputs, never JSON parsed out of
prose. Both ask the judge for its `signal_type` so circularity with the typography finding
can be checked — that check is what makes the judge independent evidence rather than a
restatement.

`esl_markers.py` uses only constructions that are genuinely ungrammatical. An earlier
version included patterns like `paper proposes`, which matches the perfectly correct
"**This** paper proposes", and `proposed method`, which matches "**the** proposed method".
Both are high-frequency and reversed the sign of the result before being caught.
