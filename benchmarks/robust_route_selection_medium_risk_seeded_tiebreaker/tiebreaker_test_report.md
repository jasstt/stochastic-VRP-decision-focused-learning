# Robust Route Tie-Breaker Test

## Scope

- Run dir: `benchmarks/robust_route_selection_medium_risk_seeded_mean_domain_loss`
- Primary score metric: `mean_domain_loss`
- Primary relative tolerance: `0.01`
- Tie-breaker: `stockout_drift`
- Tie-breaker candidates were full-confirmed before final selection.

## Summary

- Near-tied candidate rows: 440
- Near-tied full-confirmation rows: 440
- Tie-breaker winner rows: 96
- Strict-safe winner rows: 52
- Winner domain-specific instances: 20
- Fully certified instances: 13
- Certified domain-specific instances: 10

## Instance Summary

| Instance | Winner Domains | Winner Unique Route Plans | Winner Domain-Specific | Strict-Safe Domains | Certified Unique Route Plans | Fully Certified Instance | Certified Domain-Specific |
| --- | --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | 4 | 2 | yes | 0 | 0 | no | no |
| X-n110-k13 | 4 | 2 | yes | 0 | 0 | no | no |
| X-n115-k10 | 4 | 2 | yes | 0 | 0 | no | no |
| X-n120-k6 | 4 | 4 | yes | 4 | 4 | yes | yes |
| X-n129-k18 | 4 | 3 | yes | 4 | 3 | yes | yes |
| X-n134-k13 | 4 | 3 | yes | 4 | 3 | yes | yes |
| X-n139-k10 | 4 | 3 | yes | 0 | 0 | no | no |
| X-n143-k7 | 4 | 4 | yes | 4 | 4 | yes | yes |
| X-n162-k11 | 4 | 2 | yes | 0 | 0 | no | no |
| X-n167-k10 | 4 | 2 | yes | 4 | 2 | yes | yes |
| X-n181-k23 | 4 | 2 | yes | 0 | 0 | no | no |
| X-n186-k15 | 4 | 1 | no | 4 | 1 | yes | no |
| X-n190-k8 | 4 | 3 | yes | 4 | 3 | yes | yes |
| X-n204-k19 | 4 | 2 | yes | 0 | 0 | no | no |
| X-n209-k16 | 4 | 1 | no | 0 | 0 | no | no |
| X-n223-k34 | 4 | 3 | yes | 0 | 0 | no | no |
| X-n228-k23 | 4 | 1 | no | 4 | 1 | yes | no |
| X-n237-k14 | 4 | 3 | yes | 4 | 3 | yes | yes |
| X-n242-k48 | 4 | 2 | yes | 0 | 0 | no | no |
| X-n251-k28 | 4 | 1 | no | 4 | 1 | yes | no |
| X-n261-k13 | 4 | 3 | yes | 4 | 3 | yes | yes |
| X-n275-k28 | 4 | 3 | yes | 4 | 3 | yes | yes |
| X-n280-k17 | 4 | 2 | yes | 0 | 0 | no | no |
| X-n284-k15 | 4 | 3 | yes | 4 | 3 | yes | yes |

## Ranking Stability

| Instance | Domains | Fast Ranking | Full Ranking | Ranking Flip | Stockout Spearman | Ranking Note |
| --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | 4 | atm > grocery > cargo > cold_chain | cargo > atm > grocery > cold_chain | yes | 0.4 |  |
| X-n110-k13 | 4 | cargo > atm > grocery > cold_chain | cargo > cold_chain > atm > grocery | yes | 0.4 |  |
| X-n115-k10 | 4 | grocery > cargo > atm > cold_chain | cargo > atm > grocery > cold_chain | yes | 0.4 |  |
| X-n120-k6 | 4 | cargo > cold_chain > grocery > atm | cargo > cold_chain > grocery > atm | no | 1 |  |
| X-n129-k18 | 4 | grocery > atm > cold_chain > cargo | grocery > atm > cold_chain > cargo | no | 1 |  |
| X-n134-k13 | 4 | atm > grocery > cold_chain > cargo | atm > grocery > cold_chain > cargo | no | 1 |  |
| X-n139-k10 | 4 | atm > grocery > cold_chain > cargo | grocery > atm > cargo > cold_chain | yes | 0.6 |  |
| X-n143-k7 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cargo > cold_chain | no | 1 |  |
| X-n162-k11 | 4 | cargo > atm > cold_chain > grocery | cargo > cold_chain > atm > grocery | yes | 0.8 |  |
| X-n167-k10 | 4 | atm > cargo > grocery > cold_chain | atm > cargo > grocery > cold_chain | no | 1 |  |
| X-n181-k23 | 4 | grocery > cargo > atm > cold_chain | grocery > atm > cargo > cold_chain | yes | 0.8 |  |
| X-n186-k15 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cargo > cold_chain | no | 1 |  |
| X-n190-k8 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cargo > cold_chain | no | 1 |  |
| X-n204-k19 | 4 | cargo > atm > grocery > cold_chain | grocery > cargo > atm > cold_chain | yes | 0.4 |  |
| X-n209-k16 | 4 | atm > cargo > grocery > cold_chain | atm > grocery > cargo > cold_chain | yes | 0.8 |  |
| X-n223-k34 | 4 | atm > grocery > cold_chain > cargo | grocery > atm > cold_chain > cargo | yes | 0.8 |  |
| X-n228-k23 | 4 | atm > grocery > cold_chain > cargo | atm > grocery > cold_chain > cargo | no | 1 |  |
| X-n237-k14 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n242-k48 | 4 | atm > grocery > cold_chain > cargo | grocery > atm > cold_chain > cargo | yes | 0.8 |  |
| X-n251-k28 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cargo > cold_chain | no | 1 |  |
| X-n261-k13 | 4 | grocery > atm > cargo > cold_chain | grocery > atm > cargo > cold_chain | no | 1 |  |
| X-n275-k28 | 4 | atm > cargo > grocery > cold_chain | atm > cargo > grocery > cold_chain | no | 1 |  |
| X-n280-k17 | 4 | atm > cargo > grocery > cold_chain | cargo > atm > grocery > cold_chain | yes | 0.8 |  |
| X-n284-k15 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cargo > cold_chain | no | 1 |  |

## Interpretation

- This is a medium-risk subset diagnostic, not a full X40 replacement.
- The primary objective remains `mean_domain_loss`; stockout drift only breaks near ties.
- If certified diversity improves without increasing ranking flips, this is a safer next direction.
