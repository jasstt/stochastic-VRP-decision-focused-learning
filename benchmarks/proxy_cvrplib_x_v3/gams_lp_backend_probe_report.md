# GAMS LP Backend Probe Report

## Finding

GAMS is installed and reachable through the MCP server:

```text
GAMS 54.2.0, Windows x86_64
License: GAMS Demo
Time-limited license stops working on: Nov 26, 2026
```

However, the installed license is a demo license. A synthetic LP probe matching the approximate size of one X-set stochastic allocation problem (`105 customers x 180 planning scenarios`) generated:

| Rows | Columns | Nonzeros | Result |
| ---: | ------: | -------: | --- |
| 38,162 | 38,267 | 114,587 | failed before solve |

GAMS terminated with:

```text
The model exceeds the demo license limits for linear models of more than 2000 rows or columns.
```

## Interpretation

In this environment, GAMS cannot be used to accelerate the project LPs unless the license is upgraded or a remote solver service is used. The bottleneck is not model syntax or solver choice; the model cannot pass license-size validation.

## Practical Consequence

For the current X24 diagnostics, objective-interaction analysis should use the already produced PuLP/CBC result CSVs. A `GamsDecisionEngine` backend should not be added yet because it would be untestable on the actual X-scale LPs under the installed license.

## When GAMS Would Help

GAMS could become useful if paired with a non-demo license and a strong LP solver such as CPLEX, Gurobi, XPRESS, or a capable commercial LP backend. It would matter most when scenario count increases from 100 to 200+ and the stochastic allocation LP, not routing, dominates runtime.
