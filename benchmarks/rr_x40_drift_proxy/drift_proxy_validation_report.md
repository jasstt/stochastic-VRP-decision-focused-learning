# Drift Proxy Validation Report

## Proxy Definition

The proxy uses only candidate-level fast outputs available before full confirmation: primary-score gap, route cost deviation, planned load-ratio deviation, route-count mismatch, fast stockout deviation, fast shortfall deviation, and fast load-penalty deviation.

It does not use full-scenario LP results.

## Validation Summary

- High drift threshold: stockout relative drift > 0.05
- Validation rows: 482
- Decision: proxy failed as a useful production gate; full LP confirmation should remain mandatory

| Proxy Threshold | Rows | Actual High Drift Rows | Predicted High Drift Rows | True Positives | False Positives | False Negatives | Precision | False Negative Rate | Potential Full-LP Reduction | Proxy Reliable Under FN Rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 482 | 6 | 318 | 3 | 315 | 3 | 0.00943396 | 0.5 | 0.340249 | no |
| 0.15 | 482 | 6 | 266 | 3 | 263 | 3 | 0.0112782 | 0.5 | 0.448133 | no |
| 0.2 | 482 | 6 | 211 | 3 | 208 | 3 | 0.014218 | 0.5 | 0.562241 | no |
| 0.25 | 482 | 6 | 146 | 2 | 144 | 4 | 0.0136986 | 0.666667 | 0.697095 | no |
| 0.3 | 482 | 6 | 68 | 0 | 68 | 6 | 0 | 1 | 0.858921 | no |

## Interpretation

- If false negative rate exceeds 10%, the proxy is not safe: it would skip candidates that later show high full-confirmation drift.
- A threshold that marks nearly every row high-risk is technically safe but not useful because it does not reduce full-LP calls.
- Current OR-Tools does not expose a native `random_seed` field in this environment. Seeded variants are implemented through reproducible search-cost perturbation, with route costs still reported on the original distance matrix. A future validation round should repeat this with a native-seed OR-Tools build if available.
