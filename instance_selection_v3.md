# Instance Selection v3

This file records the actually downloaded CVRPLIB X-set expansion used by the load-allocation diagnostic.

The `vrplib` Python package is installed and used to validate the downloaded VRPLIB files. Downloads are performed through the official CVRPLIB instance endpoints because `vrplib==2.2.0` provides readers/writers, not a downloader API.

## Bucket Counts

| Bucket | Count |
| --- | --- |
| large | 8 |
| medium | 8 |
| small | 8 |

## Capacity Pressure Quantiles

| Quantile | Capacity pressure |
| --- | --- |
| 0.2500 | 0.9444 |
| 0.5000 | 0.9733 |
| 0.7500 | 0.9841 |

## Selected Instances

| Instance | CVRPLIB id | Bucket | Nodes | Customers | Vehicles | Capacity | Capacity pressure | Best known cost | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n101-k25 | 158 | small | 101 | 100 | 25 | 206 | 0.9994 | 27591 | Small X baseline; many vehicles relative to size. |
| X-n106-k14 | 159 | small | 106 | 105 | 14 | 600 | 0.9362 | 26362 | Small X case with moderate fleet count. |
| X-n110-k13 | 160 | small | 110 | 109 | 13 | 66 | 0.9510 | 14971 | Small X case with tight capacity and lower vehicle count. |
| X-n115-k10 | 161 | small | 115 | 114 | 10 | 169 | 0.9083 | 12747 | Small X case with lower vehicle count. |
| X-n120-k6 | 162 | small | 120 | 119 | 6 | 21 | 0.9444 | 13332 | Small X case with very low fleet count. |
| X-n125-k30 | 163 | small | 125 | 124 | 30 | 188 | 0.9816 | 55539 | Small X case with high route count. |
| X-n129-k18 | 164 | small | 129 | 128 | 18 | 39 | 0.9473 | 28940 | Small X boundary case. |
| X-n134-k13 | 165 | small | 134 | 133 | 13 | 643 | 0.9834 | 10916 | Additional small X case added to reach an 8/8/8 X stratification. |
| X-n153-k22 | 169 | medium | 153 | 152 | 22 | 144 | 0.9684 | 21220 | Medium X entry point after the small bucket. |
| X-n157-k13 | 170 | medium | 157 | 156 | 13 | 12 | 1.0000 | 16876 | Medium case with small capacity and lower fleet count. |
| X-n162-k11 | 171 | medium | 162 | 161 | 11 | 1174 | 0.9442 | 14138 | Medium case with high capacity and lower route count. |
| X-n167-k10 | 172 | medium | 167 | 166 | 10 | 133 | 0.9293 | 20557 | Medium case with low vehicle count. |
| X-n172-k51 | 173 | medium | 172 | 171 | 51 | 161 | 0.9855 | 45607 | Medium case with many active routes. |
| X-n176-k26 | 174 | medium | 176 | 175 | 26 | 142 | 0.9837 | 47812 | Medium case with moderate-high route count. |
| X-n181-k23 | 175 | medium | 181 | 180 | 23 | 8 | 0.9783 | 25569 | Medium boundary case. |
| X-n190-k8 | 177 | medium | 190 | 189 | 8 | 138 | 0.9447 | 16980 | Additional medium X case added to reach an 8/8/8 X stratification. |
| X-n223-k34 | 184 | large | 223 | 222 | 34 | 37 | 0.9809 | 40437 | Large X case kept below 250 nodes for executable diagnostics. |
| X-n228-k23 | 185 | large | 228 | 227 | 23 | 154 | 0.9819 | 25742 | Large case with moderate fleet count. |
| X-n233-k16 | 186 | large | 233 | 232 | 16 | 631 | 0.9997 | 19230 | Large case with lower route count. |
| X-n237-k14 | 187 | large | 237 | 236 | 14 | 18 | 0.9365 | 27042 | Additional large X case below 250 nodes for executable diagnostics. |
| X-n242-k48 | 188 | large | 242 | 241 | 48 | 28 | 0.9851 | 82751 | Large case with high route count. |
| X-n247-k50 | 189 | large | 247 | 246 | 50 | 134 | 0.9254 | 37274 | Additional large X case with high route count. |
| X-n251-k28 | 190 | large | 251 | 250 | 28 | 69 | 0.9664 | 38684 | Large case around 250 nodes. |
| X-n256-k16 | 191 | large | 256 | 255 | 16 | 1225 | 0.9956 | 18839 | Largest selected case in this executable X diagnostic. |
