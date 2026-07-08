# LP Speed Diagnosis Report

## Tested Options

This pass tested two low-risk acceleration paths before changing the stochastic
model structure:

1. Solver backend swap inside `StochasticDecisionEngine`: `pulp_cbc`,
   `ortools_glop`, `ortools_pdlp`.
2. Deterministic total-demand-stratified planning scenario reduction with
   `--lp-planning-scenario-limit`.

## Backend Result

On the current environment, OR-Tools linear backends are numerically close to
CBC but do not speed up these LPs.

| Dataset | Domain(s) | Scenario Count | Backend | Median Solve Runtime |
|---|---:|---:|---|---:|
| A-n32-k5 | atm, cold_chain | 365 | pulp_cbc | 2.024s |
| A-n32-k5 | atm, cold_chain | 365 | ortools_glop | 11.866s |
| A-n32-k5 | atm, cold_chain | 365 | ortools_pdlp | 5.767s |
| X-n106-k14 | atm | 60 | pulp_cbc | 0.630s |
| X-n106-k14 | atm | 60 | ortools_glop | 2.389s |
| X-n106-k14 | atm | 60 | ortools_pdlp | 5.480s |

Interpretation: keep CBC as the default backend for now. GLOP/PDLP remain useful
as correctness cross-checks, not as the speed path.

## Scenario Reduction Result

Reducing only the LP planning scenarios to 60 gave the clearest acceleration.
Routing anchors and evaluation scenarios were unchanged.

| Dataset | Domain(s) | Full Solve | 60-Scenario Solve | Solve Speedup | Max Stockout Diff | Max Mean Cost Diff |
|---|---:|---:|---:|---:|---:|---:|
| A-n32-k5 | atm, cold_chain | 1.778s-2.270s | 0.154s-0.159s | 11.6x-14.3x | 0.00419 | 7.09 |
| X-n106-k14 | atm | 4.507s | 0.630s | 7.15x | 0.00143 | 31.19 |

These are diagnostic-scale results, not a proof that 60 scenarios is always
enough. The speed signal is strong enough to use this mode for iteration.

## Recommendation

Use:

```bash
--lp-backend pulp_cbc --lp-planning-scenario-limit 60
```

for fast exploratory diagnostics. Use full planning history for final
methodology/report numbers, or report the scenario-reduction accuracy check
next to the fast result.

## Next Step

If this is still too slow on 40-60 X instances, the next real speedup is not
another generic LP backend. It is a structured route-level allocator that uses
the separable shortage/surplus recourse form directly, with a separate treatment
for the CVaR term.
