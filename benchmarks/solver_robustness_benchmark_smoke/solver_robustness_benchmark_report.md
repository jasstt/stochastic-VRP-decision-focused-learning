# Solver Robustness Benchmark Report

## Scope

This benchmark sweeps routing provider, route time limit, LP backend, LP time limit, and LP scenario limit.
CBC through PuLP remains the default reference backend. OR-Tools GLOP/PDLP are reported as cross-checks.
GAMS is intentionally excluded from this branch.

## Baseline

Baseline = route provider `ortools`, route time limit `2s`, LP backend `pulp_cbc`, LP time limit `10s`, LP scenario limit `full`.

## A.5 Evidence Status

Rows: 48; feasible rows: 21; instances: 2; domains: 2. This run is classified as **diagnostic signal only**.

## Summary

| Route Provider | Route Time Limit Sec | LP Backend | LP Time Limit Sec | LP Scenario Limit | Rows | Feasible_Rows | Route_Feasible_Rows | LP_Feasible_Rows | Median_Total_Runtime_Sec | Mean_Total_Runtime_Sec | Feasibility_Rate | Compared_Rows | Median_Runtime_Speedup_vs_Baseline | Mean_Stockout_Drift_Abs | Max_Stockout_Drift_Abs | Mean_Objective_Drift_Rel | Max_Objective_Drift_Rel | Stockout_Drift_Mean_CI_Low | Stockout_Drift_Mean_CI_High | Objective_Drift_Rel_Mean_CI_Low | Objective_Drift_Rel_Mean_CI_High |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ortools | 2 | ortools_glop | 10 | 60 | 4 | 4 | 4 | 4 | 2.23069 | 2.24219 | 1 | 4 | 1.74739 | 0.00574462 | 0.0138333 | 0.0038107 | 0.00685322 | 0.0021371 | 0.0114234 | 0.00213671 | 0.00580229 |
| ortools | 2 | ortools_glop | 10 | full | 4 | 1 | 4 | 1 | 12.0118 | 11.8135 | 0.25 | 1 | 0.307781 | 0 | 0 | 6.41946e-10 | 6.41946e-10 | 0 | 0 | 6.41946e-10 | 6.41946e-10 |
| ortools | 2 | ortools_pdlp | 10 | 60 | 4 | 4 | 4 | 4 | 2.47893 | 2.47271 | 1 | 4 | 1.60755 | 0.00574462 | 0.0138333 | 0.00381075 | 0.00685295 | 0.0021371 | 0.0114234 | 0.00213682 | 0.00580212 |
| ortools | 2 | ortools_pdlp | 10 | full | 4 | 4 | 4 | 4 | 6.52467 | 7.08117 | 1 | 4 | 0.576012 | 0 | 0 | 2.2581e-07 | 4.80911e-07 | 0 | 0 | 7.2802e-08 | 4.04827e-07 |
| ortools | 2 | pulp_cbc | 10 | 60 | 4 | 4 | 4 | 4 | 2.16242 | 2.15773 | 1 | 4 | 1.79906 | 0.00574462 | 0.0138333 | 0.0038107 | 0.00685322 | 0.0021371 | 0.0114234 | 0.00213671 | 0.00580229 |
| ortools | 2 | pulp_cbc | 10 | full | 4 | 4 | 4 | 4 | 3.89561 | 3.8649 | 1 | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| vroom | 2 | ortools_glop | 10 | 60 | 4 | 0 | 0 | 0 |  |  | 0 |  |  |  |  |  |  |  |  |  |  |
| vroom | 2 | ortools_glop | 10 | full | 4 | 0 | 0 | 0 |  |  | 0 |  |  |  |  |  |  |  |  |  |  |
| vroom | 2 | ortools_pdlp | 10 | 60 | 4 | 0 | 0 | 0 |  |  | 0 |  |  |  |  |  |  |  |  |  |  |
| vroom | 2 | ortools_pdlp | 10 | full | 4 | 0 | 0 | 0 |  |  | 0 |  |  |  |  |  |  |  |  |  |  |
| vroom | 2 | pulp_cbc | 10 | 60 | 4 | 0 | 0 | 0 |  |  | 0 |  |  |  |  |  |  |  |  |  |  |
| vroom | 2 | pulp_cbc | 10 | full | 4 | 0 | 0 | 0 |  |  | 0 |  |  |  |  |  |  |  |  |  |  |

## Drift Against Baseline

| Instance | Domain | Route Provider | Route Time Limit Sec | LP Backend | LP Time Limit Sec | LP Scenario Limit | Runtime Speedup vs Baseline | Stockout Drift Abs | Objective Drift Rel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A-n32-k5 | atm | ortools | 2 | ortools_glop | 10 | 60 | 1.66824 | 0.00145161 | 0.00411617 |
| A-n32-k5 | cold_chain | ortools | 2 | ortools_glop | 10 | 60 | 1.83346 | 0.00419355 | 0.00685322 |
| B-n31-k5 | atm | ortools | 2 | ortools_glop | 10 | 60 | 1.56322 | 0.0035 | 0.0016239 |
| B-n31-k5 | cold_chain | ortools | 2 | ortools_glop | 10 | 60 | 1.82655 | 0.0138333 | 0.00264952 |
| B-n31-k5 | atm | ortools | 2 | ortools_glop | 10 | full | 0.307781 | 0 | 6.41946e-10 |
| A-n32-k5 | atm | ortools | 2 | ortools_pdlp | 10 | 60 | 1.54407 | 0.00145161 | 0.0041164 |
| A-n32-k5 | cold_chain | ortools | 2 | ortools_pdlp | 10 | 60 | 1.67103 | 0.00419355 | 0.00685295 |
| B-n31-k5 | atm | ortools | 2 | ortools_pdlp | 10 | 60 | 1.32251 | 0.0035 | 0.00162403 |
| B-n31-k5 | cold_chain | ortools | 2 | ortools_pdlp | 10 | 60 | 1.73578 | 0.0138333 | 0.00264961 |
| A-n32-k5 | atm | ortools | 2 | ortools_pdlp | 10 | full | 0.4053 | 0 | 2.23025e-07 |
| A-n32-k5 | cold_chain | ortools | 2 | ortools_pdlp | 10 | full | 0.702697 | 0 | 2.27277e-08 |
| B-n31-k5 | atm | ortools | 2 | ortools_pdlp | 10 | full | 0.509776 | 0 | 4.80911e-07 |
| B-n31-k5 | cold_chain | ortools | 2 | ortools_pdlp | 10 | full | 0.642248 | 0 | 1.76578e-07 |
| A-n32-k5 | atm | ortools | 2 | pulp_cbc | 10 | 60 | 1.74738 | 0.00145161 | 0.00411617 |
| A-n32-k5 | cold_chain | ortools | 2 | pulp_cbc | 10 | 60 | 1.93992 | 0.00419355 | 0.00685322 |
| B-n31-k5 | atm | ortools | 2 | pulp_cbc | 10 | 60 | 1.62253 | 0.0035 | 0.0016239 |
| B-n31-k5 | cold_chain | ortools | 2 | pulp_cbc | 10 | 60 | 1.85074 | 0.0138333 | 0.00264952 |
| A-n32-k5 | atm | ortools | 2 | pulp_cbc | 10 | full | 1 | 0 | 0 |
| A-n32-k5 | cold_chain | ortools | 2 | pulp_cbc | 10 | full | 1 | 0 | 0 |
| B-n31-k5 | atm | ortools | 2 | pulp_cbc | 10 | full | 1 | 0 | 0 |
| B-n31-k5 | cold_chain | ortools | 2 | pulp_cbc | 10 | full | 1 | 0 | 0 |

## Correlation Diagnostics

| X Metric | Y Metric | N | Unique X Levels | Pearson r | Permutation p-value | Bootstrap CI Low | Bootstrap CI High | A5 Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Route Time Limit Sec | Stockout Drift Abs | 21 | 1 |  |  |  |  | insufficient x variation; correlation not reported |
| LP Time Limit Sec | Stockout Drift Abs | 21 | 1 |  |  |  |  | insufficient x variation; correlation not reported |
| LP Planning Scenarios | Stockout Drift Abs | 21 | 2 |  |  |  |  | insufficient x variation; correlation not reported |
| Route Time Limit Sec | Objective Drift Rel | 21 | 1 |  |  |  |  | insufficient x variation; correlation not reported |
| LP Time Limit Sec | Objective Drift Rel | 21 | 1 |  |  |  |  | insufficient x variation; correlation not reported |
| LP Planning Scenarios | Objective Drift Rel | 21 | 2 |  |  |  |  | insufficient x variation; correlation not reported |

## Interpretation Rules

- Treat n<15 runs as smoke diagnostics, not proof.
- Do not report a correlation when the x variable has fewer than 3 distinct levels.
- If a bootstrap confidence interval includes zero, treat the relationship as unstable.
- A solver variant is a safe default candidate only if feasibility stays high and stockout/objective drift remain near zero.
- Final README/report claims should use full planning scenarios even when `limit=60` is acceptable for exploration.
