# CVRPLIB raw benchmark snapshot

This folder stores a small, reproducible CVRP benchmark seed set downloaded
from CVRPLIB.

Source:

- CVRPLIB homepage: https://vrp.atd-lab.inf.puc-rio.br/index.php/en/
- Instance download pattern used by the site:
  `https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/instance/{id}`
- Solution download pattern used by the site:
  `https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/instanceSolution/{id}`

Initial instances:

| Instance | CVRPLIB id | Reason |
| --- | ---: | --- |
| A-n32-k5 | 4 | Small Augerat CVRP with known optimum |
| B-n31-k5 | 6 | Similar scale, different geometry/demand structure |
| E-n13-k4 | 54 | Tiny explicit-distance sanity check |
| P-n19-k2 | 76 | Small two-vehicle case for fast smoke tests |

The proxy demand generator deliberately uses only information available before
optimization: nominal benchmark demand, depot distance, and generic day-level
shocks. It is not fitted to SPO+ or to any baseline outcome.

