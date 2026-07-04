# Instance Selection v2

This validation set contains 20 coordinate-capable CVRPLIB CVRP instances for the grouping-exposure stockout validation.

`E-n13-k4` is deliberately excluded because it is an explicit-distance instance without coordinates in the current raw snapshot; exposure-rank analysis needs coordinates. The strict CVRPLIB coordinate pool has very few truly tiny n<20 cases, so `P-n20-k2` and `P-n21-k2` are treated as boundary-small instances to keep a four-instance small stratum without reintroducing coordinate-less data.

## Bucket Counts

| Bucket | Count |
| --- | --- |
| large | 8 |
| medium | 8 |
| small | 4 |

## Capacity Pressure Coverage

- Low-pressure instances (`capacity_pressure <= 0.88`): 6
- High-pressure instances (`capacity_pressure >= 0.95`): 6

## Selected Instances

| Instance | CVRPLIB id | Bucket | Nodes | Customers | Vehicles | Capacity | Capacity pressure | Best known cost | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P-n16-k8 | 75 | small | 16 | 15 | 8 | 35 | 0.8786 | 450 | Small/high-vehicle-count edge case; low capacity pressure. |
| P-n19-k2 | 76 | small | 19 | 18 | 2 | 160 | 0.9688 | 212 | Existing coordinate-capable smoke instance; high capacity pressure. |
| P-n20-k2 | 77 | small | 20 | 19 | 2 | 160 | 0.9688 | 216 | Boundary-small coordinate instance; high capacity pressure. |
| P-n21-k2 | 78 | small | 21 | 20 | 2 | 160 | 0.9313 | 211 | Boundary-small coordinate instance used to avoid coordinate-less E-n13-k4. |
| E-n23-k3 | 56 | medium | 23 | 22 | 3 | 4500 | 0.7547 | 569 | Low capacity pressure medium case from a different CVRPLIB family. |
| B-n31-k5 | 6 | medium | 31 | 30 | 5 | 100 | 0.8240 | 672 | Existing coordinate-capable instance; low capacity pressure. |
| A-n32-k5 | 4 | medium | 32 | 31 | 5 | 100 | 0.8200 | 784 | Existing coordinate-capable instance; low capacity pressure. |
| A-n33-k5 | 5 | medium | 33 | 32 | 5 | 100 | 0.8920 | 661 | Medium Augerat A-family geometry. |
| B-n34-k5 | 32 | medium | 34 | 33 | 5 | 100 | 0.9140 | 788 | Medium B-family geometry with higher pressure than A-n32/B-n31. |
| B-n38-k6 | 34 | medium | 38 | 37 | 6 | 100 | 0.8533 | 805 | Medium B-family, low capacity pressure. |
| A-n45-k6 | 16 | medium | 45 | 44 | 6 | 100 | 0.9883 | 944 | Medium-high pressure A-family case. |
| P-n50-k8 | 85 | medium | 50 | 49 | 8 | 120 | 0.9906 | 631 | Medium P-family case with very high capacity pressure. |
| E-n51-k5 | 60 | large | 51 | 50 | 5 | 160 | 0.9712 | 521 | Large boundary case with high capacity pressure. |
| P-n55-k7 | 88 | large | 55 | 54 | 7 | 170 | 0.8756 | 568 | Large P-family case with lower capacity pressure. |
| A-n60-k9 | 23 | large | 60 | 59 | 9 | 100 | 0.9211 | 1354 | Large A-family case. |
| P-n60-k10 | 92 | large | 60 | 59 | 10 | 120 | 0.9450 | 744 | Large P-family case with different fleet count. |
| P-n65-k10 | 94 | large | 65 | 64 | 10 | 130 | 0.9377 | 792 | Large P-family case, moderate-high capacity pressure. |
| E-n76-k7 | 61 | large | 76 | 75 | 7 | 220 | 0.8857 | 682 | Large E-family case with lower pressure. |
| P-n76-k4 | 96 | large | 76 | 75 | 4 | 350 | 0.9743 | 593 | Large P-family case with high pressure and fewer vehicles. |
| B-n78-k10 | 53 | large | 78 | 77 | 10 | 100 | 0.9370 | 1221 | Largest selected B-family case under the 100-node target. |
