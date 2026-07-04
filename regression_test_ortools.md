# OR-Tools Provider Regression Test

Status: PASS

Command:

```bash
python -c "<direct solve_cvrp_ortools vs OrToolsProvider comparison>"
```

Test setup:

- Dataset: `benchmarks/proxy_cvrplib`
- Instances:
  - `A-n32-k5`
  - `B-n31-k5`
  - `E-n13-k4`
  - `P-n19-k2`
- Plan: `nominal_or_tools`
- Direct solver: `solve_cvrp_ortools(...)`
- Provider solver: `OrToolsProvider(...).solve(...)`
- Required tolerance: `1e-6`

| Instance | Direct feasible | Provider feasible | Direct route_cost | Provider total_cost | Result |
|---|---:|---:|---:|---:|---|
| A-n32-k5 | True | True | 784.0 | 784.0 | PASS |
| B-n31-k5 | True | True | 672.0 | 672.0 | PASS |
| E-n13-k4 | True | True | 247.0 | 247.0 | PASS |
| P-n19-k2 | True | True | 212.0 | 212.0 | PASS |

Conclusion: wrapping the existing OR-Tools logic in `OrToolsProvider` did not change feasibility or route cost on the four CVRPLIB smoke instances.
