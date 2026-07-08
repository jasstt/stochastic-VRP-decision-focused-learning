# X Dataset Expansion Report

## Scope

The CVRPLIB X expansion was actually executed, not only designed. The selected set contains 24 instances with an 8/8/8 small/medium/large split. The proxy generator used the existing project pipeline with `history_rows=180`, `scenario_count=100`, seed `31415`, and CVRPLIB distance matrices.

`vrplib==2.2.0` was installed and used to validate downloaded VRPLIB files. Downloads used the official CVRPLIB instance and BKS endpoints because this `vrplib` release has readers/writers but no download API.

## Dataset Balance

| Bucket | instances | min_nodes | max_nodes | mean_capacity_pressure |
| ------ | --------- | --------- | --------- | ---------------------- |
| large  | 8         | 223       | 256       | 0.9714                 |
| medium | 8         | 153       | 190       | 0.9668                 |
| small  | 8         | 101       | 134       | 0.9565                 |

## Selected Instances

| name       | Bucket | nodes | customers | capacity | best_known_cost |
| ---------- | ------ | ----- | --------- | -------- | --------------- |
| X-n101-k25 | small  | 101   | 100       | 206      | 27591           |
| X-n106-k14 | small  | 106   | 105       | 600      | 26362           |
| X-n110-k13 | small  | 110   | 109       | 66       | 14971           |
| X-n115-k10 | small  | 115   | 114       | 169      | 12747           |
| X-n120-k6  | small  | 120   | 119       | 21       | 13332           |
| X-n125-k30 | small  | 125   | 124       | 188      | 55539           |
| X-n129-k18 | small  | 129   | 128       | 39       | 28940           |
| X-n134-k13 | small  | 134   | 133       | 643      | 10916           |
| X-n153-k22 | medium | 153   | 152       | 144      | 21220           |
| X-n157-k13 | medium | 157   | 156       | 12       | 16876           |
| X-n162-k11 | medium | 162   | 161       | 1174     | 14138           |
| X-n167-k10 | medium | 167   | 166       | 133      | 20557           |
| X-n172-k51 | medium | 172   | 171       | 161      | 45607           |
| X-n176-k26 | medium | 176   | 175       | 142      | 47812           |
| X-n181-k23 | medium | 181   | 180       | 8        | 25569           |
| X-n190-k8  | medium | 190   | 189       | 138      | 16980           |
| X-n223-k34 | large  | 223   | 222       | 37       | 40437           |
| X-n228-k23 | large  | 228   | 227       | 154      | 25742           |
| X-n233-k16 | large  | 233   | 232       | 631      | 19230           |
| X-n237-k14 | large  | 237   | 236       | 18       | 27042           |
| X-n242-k48 | large  | 242   | 241       | 28       | 82751           |
| X-n247-k50 | large  | 247   | 246       | 134      | 37274           |
| X-n251-k28 | large  | 251   | 250       | 69       | 38684           |
| X-n256-k16 | large  | 256   | 255       | 1225     | 18839           |

## Feasibility Health Check

| Provider                  | Total Instances | Feasible Instances | Feasible Domain Rows | Failed Instances                                                                               |
| ------------------------- | --------------- | ------------------ | -------------------- | ---------------------------------------------------------------------------------------------- |
| OR-Tools                  | 24              | 16                 | 64                   | X-n101-k25, X-n125-k30, X-n153-k22, X-n172-k51, X-n176-k26, X-n233-k16, X-n247-k50, X-n256-k16 |
| VROOM                     | 24              | 21                 | 84                   | X-n101-k25, X-n233-k16, X-n256-k16                                                             |
| Common OR-Tools and VROOM | 24              | 16                 | 64                   |                                                                                                |

Common feasible instances for OR-Tools and VROOM: 16.

```text
X-n106-k14, X-n110-k13, X-n115-k10, X-n120-k6, X-n129-k18, X-n134-k13, X-n157-k13, X-n162-k11, X-n167-k10, X-n181-k23, X-n190-k8, X-n223-k34, X-n228-k23, X-n237-k14, X-n242-k48, X-n251-k28
```

This is an important health result: VROOM solved more X anchors than OR-Tools under the selected limits. Therefore X-set claims should distinguish all downloaded instances (n=24) from common provider-feasible instances (n=16).

## Domain Cost Ranking

| Provider | Cost Ranking Low-to-High           |
| -------- | ---------------------------------- |
| OR-Tools | grocery < cargo < atm < cold_chain |
| VROOM    | grocery < cargo < atm < cold_chain |

Detailed provider/domain averages:

| Provider | domain     | feasible_instances | avg_mean_total_cost | avg_stockout_rate | avg_runtime_sec | avg_mean_load_penalty_loss |
| -------- | ---------- | ------------------ | ------------------- | ----------------- | --------------- | -------------------------- |
| OR-Tools | grocery    | 16                 | 28299.8361          | 0.4401            | 25.9346         | 0.0000                     |
| OR-Tools | cargo      | 16                 | 28419.5039          | 0.4398            | 28.5415         | 0.0000                     |
| OR-Tools | atm        | 16                 | 28704.2723          | 0.4414            | 27.7027         | 0.0000                     |
| OR-Tools | cold_chain | 16                 | 29125.4289          | 0.4361            | 26.8330         | 489.4032                   |
| VROOM    | grocery    | 21                 | 31240.0961          | 0.4461            | 8.4777          | 0.0000                     |
| VROOM    | cargo      | 21                 | 31408.0915          | 0.4489            | 10.3278         | 0.0000                     |
| VROOM    | atm        | 21                 | 31786.6677          | 0.4484            | 9.5307          | 0.0000                     |
| VROOM    | cold_chain | 21                 | 32286.4670          | 0.4403            | 8.9969          | 607.3659                   |

## Stockout Ranking

| Provider | Stockout Ranking High-to-Low       |
| -------- | ---------------------------------- |
| OR-Tools | atm > grocery > cargo > cold_chain |
| VROOM    | cargo > atm > grocery > cold_chain |

The domain cost ordering is broadly stable in the sense that `grocery` remains the cheapest and `cold_chain` remains the most expensive under both providers. Stockout ordering is not stable across providers, which preserves A.8 as a live mechanism question.

## Runtime

Runtime is reported from the project `runtime_sec` field per feasible provider-domain row. This includes the anchor route solve time plus that domain LP solve time; anchor time is repeated across the four domain rows, so these values should be read as per-row diagnostic runtime rather than exact end-to-end wall time.

| Provider | Bucket | Rows | Instances | Avg Runtime Sec Per Domain Row | P90 Runtime Sec Per Domain Row | Max Runtime Sec Per Domain Row |
| -------- | ------ | ---- | --------- | ------------------------------ | ------------------------------ | ------------------------------ |
| OR-Tools | large  | 20   | 5         | 29.3341                        | 32.9824                        | 35.1935                        |
| OR-Tools | medium | 20   | 5         | 28.7831                        | 30.8549                        | 39.0392                        |
| OR-Tools | small  | 24   | 6         | 24.2435                        | 26.2782                        | 26.9558                        |
| VROOM    | large  | 24   | 6         | 14.0449                        | 17.0188                        | 18.5548                        |
| VROOM    | medium | 32   | 8         | 9.4544                         | 12.1666                        | 13.2952                        |
| VROOM    | small  | 28   | 7         | 5.1564                         | 7.2534                         | 8.0707                         |
