# Drift Proxy Validation Report

## Proxy Definition

The proxy uses only candidate-level fast outputs available before full confirmation: primary-score gap, route cost deviation, planned load-ratio deviation, route-count mismatch, fast stockout deviation, fast shortfall deviation, and fast load-penalty deviation.

It does not use full-scenario LP results.

## Validation Summary

- High drift threshold: stockout relative drift > 0.05
- Validation rows: 440
- Decision: proxy failed as a useful production gate; full LP confirmation should remain mandatory

| Proxy Threshold | Rows | Actual High Drift Rows | Predicted High Drift Rows | True Positives | False Positives | False Negatives | Precision | False Negative Rate | Potential Full-LP Reduction | Proxy Reliable Under FN Rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 440 | 6 | 349 | 4 | 345 | 2 | 0.0114613 | 0.333333 | 0.206818 | no |
| 0.15 | 440 | 6 | 293 | 4 | 289 | 2 | 0.0136519 | 0.333333 | 0.334091 | no |
| 0.2 | 440 | 6 | 232 | 4 | 228 | 2 | 0.0172414 | 0.333333 | 0.472727 | no |
| 0.25 | 440 | 6 | 166 | 2 | 164 | 4 | 0.0120482 | 0.666667 | 0.622727 | no |
| 0.3 | 440 | 6 | 91 | 0 | 91 | 6 | 0 | 1 | 0.793182 | no |

## Interpretation

- If false negative rate exceeds 10%, the proxy is not safe: it would skip candidates that later show high full-confirmation drift.
- A threshold that marks nearly every row high-risk is technically safe but not useful because it does not reduce full-LP calls.
- Current OR-Tools does not expose a native `random_seed` field in this environment. Seeded variants are implemented through reproducible search-cost perturbation, with route costs still reported on the original distance matrix. A future validation round should repeat this with a native-seed OR-Tools build if available.
