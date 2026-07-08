# Instance Selection v3

This file records the actually downloaded CVRPLIB X-set expansion used by the load-allocation diagnostic.

The `vrplib` Python package is installed and used to validate the downloaded VRPLIB files. Downloads are performed through the official CVRPLIB instance endpoints because `vrplib==2.2.0` provides readers/writers, not a downloader API.

## Bucket Counts

| Bucket | Count |
| --- | --- |
| x100_143 | 10 |
| x148_190 | 10 |
| x195_237 | 10 |
| x242_284 | 10 |

## Capacity Pressure Quantiles

| Quantile | Capacity pressure |
| --- | --- |
| 0.2500 | 0.9467 |
| 0.5000 | 0.9794 |
| 0.7500 | 0.9877 |

## Selected Instances

| Instance | CVRPLIB id | Bucket | Nodes | Customers | Vehicles | Capacity | Capacity pressure | Best known cost | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n101-k25 | 158 | x100_143 | 101 | 100 | 25 | 206 | 0.9994 | 27591 | Small X baseline; many vehicles relative to size. |
| X-n106-k14 | 159 | x100_143 | 106 | 105 | 14 | 600 | 0.9362 | 26362 | Small X case with moderate fleet count. |
| X-n110-k13 | 160 | x100_143 | 110 | 109 | 13 | 66 | 0.9510 | 14971 | Small X case with tight capacity and lower vehicle count. |
| X-n115-k10 | 161 | x100_143 | 115 | 114 | 10 | 169 | 0.9083 | 12747 | Small X case with lower vehicle count. |
| X-n120-k6 | 162 | x100_143 | 120 | 119 | 6 | 21 | 0.9444 | 13332 | Small X case with very low fleet count. |
| X-n125-k30 | 163 | x100_143 | 125 | 124 | 30 | 188 | 0.9816 | 55539 | Small X case with high route count. |
| X-n129-k18 | 164 | x100_143 | 129 | 128 | 18 | 39 | 0.9473 | 28940 | Small X boundary case. |
| X-n134-k13 | 165 | x100_143 | 134 | 133 | 13 | 643 | 0.9834 | 10916 | Additional small X case from v3. |
| X-n139-k10 | 166 | x100_143 | 139 | 138 | 10 | 106 | 0.9802 | 13590 | New small X case for v4 density. |
| X-n143-k7 | 167 | x100_143 | 143 | 142 | 7 | 1190 | 0.8974 | 15700 | Upper edge of the first X-size band. |
| X-n148-k46 | 168 | x148_190 | 148 | 147 | 46 | 18 | 0.9867 | 43448 | High-vehicle case at the start of the second band. |
| X-n153-k22 | 169 | x148_190 | 153 | 152 | 22 | 144 | 0.9684 | 21220 | Medium X entry point after the small bucket. |
| X-n157-k13 | 170 | x148_190 | 157 | 156 | 13 | 12 | 1.0000 | 16876 | Medium case with small capacity and lower fleet count. |
| X-n162-k11 | 171 | x148_190 | 162 | 161 | 11 | 1174 | 0.9442 | 14138 | Medium case with high capacity and lower route count. |
| X-n167-k10 | 172 | x148_190 | 167 | 166 | 10 | 133 | 0.9293 | 20557 | Medium case with low vehicle count. |
| X-n172-k51 | 173 | x148_190 | 172 | 171 | 51 | 161 | 0.9855 | 45607 | Medium case with many active routes. |
| X-n176-k26 | 174 | x148_190 | 176 | 175 | 26 | 142 | 0.9837 | 47812 | Medium case with moderate-high route count. |
| X-n181-k23 | 175 | x148_190 | 181 | 180 | 23 | 8 | 0.9783 | 25569 | Medium boundary case. |
| X-n186-k15 | 176 | x148_190 | 186 | 185 | 15 | 974 | 0.9482 | 24145 | New medium case for v4 density. |
| X-n190-k8 | 177 | x148_190 | 190 | 189 | 8 | 138 | 0.9447 | 16980 | Upper edge of the second X-size band. |
| X-n195-k51 | 178 | x195_237 | 195 | 194 | 51 | 181 | 0.9975 | 44225 | High-route case at the start of the third band. |
| X-n200-k36 | 179 | x195_237 | 200 | 199 | 36 | 402 | 0.9856 | 58578 | Third-band case with moderate-high route count. |
| X-n204-k19 | 180 | x195_237 | 204 | 203 | 19 | 836 | 0.9528 | 19565 | Third-band case with moderate route count. |
| X-n209-k16 | 181 | x195_237 | 209 | 208 | 16 | 101 | 0.9573 | 30656 | Third-band case with lower route count. |
| X-n214-k11 | 182 | x195_237 | 214 | 213 | 11 | 944 | 0.9973 | 10856 | Third-band low-route case. |
| X-n219-k73 | 183 | x195_237 | 219 | 218 | 73 | 3 | 0.9954 | 117595 | Third-band high-route stress case. |
| X-n223-k34 | 184 | x195_237 | 223 | 222 | 34 | 37 | 0.9809 | 40437 | Large X case kept below 250 nodes for executable diagnostics. |
| X-n228-k23 | 185 | x195_237 | 228 | 227 | 23 | 154 | 0.9819 | 25742 | Large case with moderate fleet count. |
| X-n233-k16 | 186 | x195_237 | 233 | 232 | 16 | 631 | 0.9997 | 19230 | Large case with lower route count. |
| X-n237-k14 | 187 | x195_237 | 237 | 236 | 14 | 18 | 0.9365 | 27042 | Upper edge of the third X-size band. |
| X-n242-k48 | 188 | x242_284 | 242 | 241 | 48 | 28 | 0.9851 | 82751 | Fourth-band case with high route count. |
| X-n247-k50 | 189 | x242_284 | 247 | 246 | 50 | 134 | 0.9254 | 37274 | Fourth-band case with high route count. |
| X-n251-k28 | 190 | x242_284 | 251 | 250 | 28 | 69 | 0.9664 | 38684 | Fourth-band case around 250 nodes. |
| X-n256-k16 | 191 | x242_284 | 256 | 255 | 16 | 1225 | 0.9956 | 18839 | Fourth-band lower-route case. |
| X-n261-k13 | 192 | x242_284 | 261 | 260 | 13 | 1081 | 0.9522 | 26558 | Fourth-band low-route case. |
| X-n266-k58 | 193 | x242_284 | 266 | 265 | 58 | 35 | 0.9926 | 75478 | Fourth-band high-route stress case. |
| X-n270-k35 | 194 | x242_284 | 270 | 269 | 35 | 585 | 0.9973 | 35291 | Fourth-band moderate-high route case. |
| X-n275-k28 | 195 | x242_284 | 275 | 274 | 28 | 10 | 0.9786 | 21245 | Fourth-band moderate route case. |
| X-n280-k17 | 196 | x242_284 | 280 | 279 | 17 | 192 | 0.9905 | 33503 | Fourth-band lower-route case. |
| X-n284-k15 | 197 | x242_284 | 284 | 283 | 15 | 109 | 0.9339 | 20215 | Upper edge of the executable v4 set. |
