# Objective Interaction Diagnosis Report

## Scope

This report tests the remaining A.8 candidate: objective interaction. The analysis uses the executed CVRPLIB X24 expansion and the common OR-Tools/VROOM feasible subset. No new LP solve is required; this diagnostic compares already produced provider-domain result components.

Predictors are OR-Tools minus VROOM differences for route cost, planned load total, domain loss, load penalty loss, surplus, shortfall, and total cost. The target is signed stockout diff.

## Provider-Domain Difference Summary

| Domain     | n  | mean_stockout_diff | mean_route_cost_diff | mean_planned_load_total_diff | mean_domain_loss_diff | mean_load_penalty_loss_diff | mean_total_cost_diff |
| ---------- | -- | ------------------ | -------------------- | ---------------------------- | --------------------- | --------------------------- | -------------------- |
| atm        | 16 | -0.0069            | 1264.2500            | 12.5244                      | -33.1880              | 0.0000                      | 1231.0620            |
| cargo      | 16 | -0.0089            | 1264.2500            | 11.3149                      | -25.3762              | 0.0000                      | 1238.8738            |
| cold_chain | 16 | -0.0062            | 1264.2500            | 27.2782                      | -11.7084              | 5.8908                      | 1258.4324            |
| grocery    | 16 | -0.0065            | 1264.2500            | 24.3889                      | -12.7529              | 0.0000                      | 1251.4971            |

## Raw Correlations

| Domain     | Predictor                   | n  | Unique x Levels | Pearson r | p-value | Bootstrap CI Low | Bootstrap CI High | CI Contains Zero | Evidence Label                                    |
| ---------- | --------------------------- | -- | --------------- | --------- | ------- | ---------------- | ----------------- | ---------------- | ------------------------------------------------- |
| atm        | Mean Domain Loss Diff       | 16 | 16              | 0.3929    | 0.1323  | 0.2522           | 0.9560            | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 |
| atm        | Mean Load Penalty Loss Diff | 16 | 1               |           |         |                  |                   | False            | insufficient_x_variation                          |
| atm        | Mean Shortfall Diff         | 16 | 16              | 0.4097    | 0.1150  | 0.2602           | 0.9438            | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 |
| atm        | Mean Surplus Diff           | 16 | 16              | -0.0316   | 0.9075  | -0.6709          | 0.7501            | True             | no_correlation_ci_crosses_zero                    |
| atm        | Mean Total Cost Diff        | 16 | 16              | 0.2600    | 0.3309  | -0.1712          | 0.6114            | True             | no_correlation_ci_crosses_zero                    |
| atm        | Planned Load Total Diff     | 16 | 16              | -0.2719   | 0.3083  | -0.8019          | -0.0290           | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 |
| atm        | Route Cost Diff             | 16 | 16              | 0.2357    | 0.3794  | -0.2290          | 0.5862            | True             | no_correlation_ci_crosses_zero                    |
| cargo      | Mean Domain Loss Diff       | 16 | 16              | 0.3871    | 0.1386  | 0.2478           | 0.8662            | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 |
| cargo      | Mean Load Penalty Loss Diff | 16 | 1               |           |         |                  |                   | False            | insufficient_x_variation                          |
| cargo      | Mean Shortfall Diff         | 16 | 16              | 0.3956    | 0.1293  | 0.2523           | 0.8668            | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 |
| cargo      | Mean Surplus Diff           | 16 | 16              | 0.0164    | 0.9518  | -0.6233          | 0.6669            | True             | no_correlation_ci_crosses_zero                    |
| cargo      | Mean Total Cost Diff        | 16 | 16              | 0.0237    | 0.9305  | -0.4670          | 0.4652            | True             | no_correlation_ci_crosses_zero                    |
| cargo      | Planned Load Total Diff     | 16 | 16              | -0.2387   | 0.3732  | -0.7312          | 0.0283            | True             | no_correlation_ci_crosses_zero                    |
| cargo      | Route Cost Diff             | 16 | 16              | 0.0007    | 0.9978  | -0.4693          | 0.4215            | True             | no_correlation_ci_crosses_zero                    |
| cold_chain | Mean Domain Loss Diff       | 16 | 16              | 0.3939    | 0.1311  | 0.2754           | 0.8802            | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 |
| cold_chain | Mean Load Penalty Loss Diff | 16 | 16              | -0.3126   | 0.2384  | -0.7554          | 0.3175            | True             | no_correlation_ci_crosses_zero                    |
| cold_chain | Mean Shortfall Diff         | 16 | 16              | 0.4669    | 0.0682  | 0.3395           | 0.9817            | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 |
| cold_chain | Mean Surplus Diff           | 16 | 16              | -0.5039   | 0.0466  | -0.9495          | -0.3399           | False            | candidate_mechanism                               |
| cold_chain | Mean Total Cost Diff        | 16 | 16              | 0.3415    | 0.1955  | -0.0810          | 0.7005            | True             | no_correlation_ci_crosses_zero                    |
| cold_chain | Planned Load Total Diff     | 16 | 16              | -0.4976   | 0.0498  | -0.9625          | -0.3536           | False            | candidate_mechanism                               |
| cold_chain | Route Cost Diff             | 16 | 16              | 0.3356    | 0.2038  | -0.1033          | 0.6942            | True             | no_correlation_ci_crosses_zero                    |
| grocery    | Mean Domain Loss Diff       | 16 | 16              | 0.3986    | 0.1262  | 0.2785           | 0.9519            | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 |
| grocery    | Mean Load Penalty Loss Diff | 16 | 1               |           |         |                  |                   | False            | insufficient_x_variation                          |
| grocery    | Mean Shortfall Diff         | 16 | 16              | 0.4447    | 0.0844  | 0.3121           | 0.9741            | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 |
| grocery    | Mean Surplus Diff           | 16 | 16              | -0.4681   | 0.0674  | -0.8868          | -0.2938           | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 |
| grocery    | Mean Total Cost Diff        | 16 | 16              | 0.3047    | 0.2512  | -0.1489          | 0.6398            | True             | no_correlation_ci_crosses_zero                    |
| grocery    | Planned Load Total Diff     | 16 | 16              | -0.4796   | 0.0601  | -0.9312          | -0.3137           | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 |
| grocery    | Route Cost Diff             | 16 | 16              | 0.2946    | 0.2681  | -0.1547          | 0.6425            | True             | no_correlation_ci_crosses_zero                    |

Raw candidate rows: 2.

## Partial Correlations Controlling Load Allocation

Because load allocation already produced a strong candidate mechanism, objective interaction must be tested against that confound. The table below residualizes both the objective predictor and stockout diff against `Load Variance Diff`.

| Domain     | Predictor                   | Control            | n  | Unique x Levels | Pearson r | p-value | Bootstrap CI Low | Bootstrap CI High | CI Contains Zero | Evidence Label                                    |
| ---------- | --------------------------- | ------------------ | -- | --------------- | --------- | ------- | ---------------- | ----------------- | ---------------- | ------------------------------------------------- |
| atm        | Mean Domain Loss Diff       | Load Variance Diff | 16 | 16              | 0.0593    | 0.8273  | -0.6666          | 0.8311            | True             | no_correlation_ci_crosses_zero                    |
| atm        | Mean Load Penalty Loss Diff | Load Variance Diff | 16 | 1               |           |         |                  |                   | False            | insufficient_variation_or_n                       |
| atm        | Mean Shortfall Diff         | Load Variance Diff | 16 | 16              | 0.0265    | 0.9224  | -0.6897          | 0.8286            | True             | no_correlation_ci_crosses_zero                    |
| atm        | Mean Surplus Diff           | Load Variance Diff | 16 | 16              | 0.3997    | 0.1250  | -0.2431          | 0.9095            | True             | no_correlation_ci_crosses_zero                    |
| atm        | Mean Total Cost Diff        | Load Variance Diff | 16 | 16              | 0.2036    | 0.4495  | -0.4314          | 0.4897            | True             | no_correlation_ci_crosses_zero                    |
| atm        | Planned Load Total Diff     | Load Variance Diff | 16 | 16              | 0.4197    | 0.1056  | -0.2701          | 0.8499            | True             | no_correlation_ci_crosses_zero                    |
| atm        | Route Cost Diff             | Load Variance Diff | 16 | 16              | 0.2032    | 0.4505  | -0.4255          | 0.4846            | True             | no_correlation_ci_crosses_zero                    |
| cargo      | Mean Domain Loss Diff       | Load Variance Diff | 16 | 16              | 0.0893    | 0.7422  | -0.5030          | 0.6153            | True             | no_correlation_ci_crosses_zero                    |
| cargo      | Mean Load Penalty Loss Diff | Load Variance Diff | 16 | 1               |           |         |                  |                   | False            | insufficient_variation_or_n                       |
| cargo      | Mean Shortfall Diff         | Load Variance Diff | 16 | 16              | 0.0589    | 0.8285  | -0.5384          | 0.6199            | True             | no_correlation_ci_crosses_zero                    |
| cargo      | Mean Surplus Diff           | Load Variance Diff | 16 | 16              | 0.3187    | 0.2290  | -0.2893          | 0.6776            | True             | no_correlation_ci_crosses_zero                    |
| cargo      | Mean Total Cost Diff        | Load Variance Diff | 16 | 16              | -0.2717   | 0.3086  | -0.8858          | 0.3275            | True             | no_correlation_ci_crosses_zero                    |
| cargo      | Planned Load Total Diff     | Load Variance Diff | 16 | 16              | 0.3186    | 0.2292  | -0.2700          | 0.7140            | True             | no_correlation_ci_crosses_zero                    |
| cargo      | Route Cost Diff             | Load Variance Diff | 16 | 16              | -0.2805   | 0.2926  | -0.8990          | 0.3202            | True             | no_correlation_ci_crosses_zero                    |
| cold_chain | Mean Domain Loss Diff       | Load Variance Diff | 16 | 16              | 0.2955    | 0.2665  | -0.4244          | 0.8969            | True             | no_correlation_ci_crosses_zero                    |
| cold_chain | Mean Load Penalty Loss Diff | Load Variance Diff | 16 | 16              | -0.1744   | 0.5182  | -0.8844          | 0.6029            | True             | no_correlation_ci_crosses_zero                    |
| cold_chain | Mean Shortfall Diff         | Load Variance Diff | 16 | 16              | 0.2057    | 0.4446  | -0.6270          | 0.9244            | True             | no_correlation_ci_crosses_zero                    |
| cold_chain | Mean Surplus Diff           | Load Variance Diff | 16 | 16              | -0.0512   | 0.8505  | -0.8666          | 0.6538            | True             | no_correlation_ci_crosses_zero                    |
| cold_chain | Mean Total Cost Diff        | Load Variance Diff | 16 | 16              | 0.4548    | 0.0767  | 0.1889           | 0.7711            | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 |
| cold_chain | Planned Load Total Diff     | Load Variance Diff | 16 | 16              | -0.1146   | 0.6727  | -0.8909          | 0.6267            | True             | no_correlation_ci_crosses_zero                    |
| cold_chain | Route Cost Diff             | Load Variance Diff | 16 | 16              | 0.4508    | 0.0797  | 0.1829           | 0.7837            | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 |
| grocery    | Mean Domain Loss Diff       | Load Variance Diff | 16 | 16              | 0.1916    | 0.4772  | -0.6044          | 0.9120            | True             | no_correlation_ci_crosses_zero                    |
| grocery    | Mean Load Penalty Loss Diff | Load Variance Diff | 16 | 1               |           |         |                  |                   | False            | insufficient_variation_or_n                       |
| grocery    | Mean Shortfall Diff         | Load Variance Diff | 16 | 16              | 0.1300    | 0.6313  | -0.6189          | 0.9153            | True             | no_correlation_ci_crosses_zero                    |
| grocery    | Mean Surplus Diff           | Load Variance Diff | 16 | 16              | 0.1258    | 0.6425  | -0.8566          | 0.7479            | True             | no_correlation_ci_crosses_zero                    |
| grocery    | Mean Total Cost Diff        | Load Variance Diff | 16 | 16              | 0.3425    | 0.1941  | -0.0411          | 0.6410            | True             | no_correlation_ci_crosses_zero                    |
| grocery    | Planned Load Total Diff     | Load Variance Diff | 16 | 16              | 0.0143    | 0.9580  | -0.8730          | 0.6908            | True             | no_correlation_ci_crosses_zero                    |
| grocery    | Route Cost Diff             | Load Variance Diff | 16 | 16              | 0.3391    | 0.1988  | -0.0617          | 0.6321            | True             | no_correlation_ci_crosses_zero                    |

Partial candidate rows: 0.

## Leverage Control

Cook's Distance control found severe points; leave-one-out is reported below.

| Domain     | Predictor                   | Instance   | Cook's Distance | Cook Threshold 4/n | Severe Threshold 3x | Severe Cook Flag |
| ---------- | --------------------------- | ---------- | --------------- | ------------------ | ------------------- | ---------------- |
| atm        | Mean Domain Loss Diff       | X-n162-k11 | 7.3231          | 0.2500             | 0.7500              | True             |
| atm        | Mean Domain Loss Diff       | X-n115-k10 | 0.2269          | 0.2500             | 0.7500              | False            |
| atm        | Mean Domain Loss Diff       | X-n167-k10 | 0.1141          | 0.2500             | 0.7500              | False            |
| atm        | Mean Domain Loss Diff       | X-n120-k6  | 0.0956          | 0.2500             | 0.7500              | False            |
| atm        | Mean Domain Loss Diff       | X-n181-k23 | 0.0260          | 0.2500             | 0.7500              | False            |
| atm        | Mean Domain Loss Diff       | X-n110-k13 | 0.0139          | 0.2500             | 0.7500              | False            |
| atm        | Mean Domain Loss Diff       | X-n129-k18 | 0.0114          | 0.2500             | 0.7500              | False            |
| atm        | Mean Domain Loss Diff       | X-n134-k13 | 0.0084          | 0.2500             | 0.7500              | False            |
| atm        | Mean Domain Loss Diff       | X-n223-k34 | 0.0067          | 0.2500             | 0.7500              | False            |
| atm        | Mean Domain Loss Diff       | X-n228-k23 | 0.0058          | 0.2500             | 0.7500              | False            |
| atm        | Mean Domain Loss Diff       | X-n157-k13 | 0.0058          | 0.2500             | 0.7500              | False            |
| atm        | Mean Domain Loss Diff       | X-n106-k14 | 0.0054          | 0.2500             | 0.7500              | False            |
| atm        | Mean Domain Loss Diff       | X-n251-k28 | 0.0045          | 0.2500             | 0.7500              | False            |
| atm        | Mean Domain Loss Diff       | X-n237-k14 | 0.0031          | 0.2500             | 0.7500              | False            |
| atm        | Mean Domain Loss Diff       | X-n190-k8  | 0.0021          | 0.2500             | 0.7500              | False            |
| atm        | Mean Domain Loss Diff       | X-n242-k48 | 0.0000          | 0.2500             | 0.7500              | False            |
| atm        | Mean Load Penalty Loss Diff | X-n106-k14 |                 | 0.2500             | 0.7500              | False            |
| atm        | Mean Load Penalty Loss Diff | X-n110-k13 |                 | 0.2500             | 0.7500              | False            |
| atm        | Mean Load Penalty Loss Diff | X-n115-k10 |                 | 0.2500             | 0.7500              | False            |
| atm        | Mean Load Penalty Loss Diff | X-n120-k6  |                 | 0.2500             | 0.7500              | False            |
| atm        | Mean Load Penalty Loss Diff | X-n129-k18 |                 | 0.2500             | 0.7500              | False            |
| atm        | Mean Load Penalty Loss Diff | X-n134-k13 |                 | 0.2500             | 0.7500              | False            |
| atm        | Mean Load Penalty Loss Diff | X-n157-k13 |                 | 0.2500             | 0.7500              | False            |
| atm        | Mean Load Penalty Loss Diff | X-n162-k11 |                 | 0.2500             | 0.7500              | False            |
| atm        | Mean Load Penalty Loss Diff | X-n167-k10 |                 | 0.2500             | 0.7500              | False            |
| atm        | Mean Load Penalty Loss Diff | X-n181-k23 |                 | 0.2500             | 0.7500              | False            |
| atm        | Mean Load Penalty Loss Diff | X-n190-k8  |                 | 0.2500             | 0.7500              | False            |
| atm        | Mean Load Penalty Loss Diff | X-n223-k34 |                 | 0.2500             | 0.7500              | False            |
| atm        | Mean Load Penalty Loss Diff | X-n228-k23 |                 | 0.2500             | 0.7500              | False            |
| atm        | Mean Load Penalty Loss Diff | X-n237-k14 |                 | 0.2500             | 0.7500              | False            |
| atm        | Mean Load Penalty Loss Diff | X-n242-k48 |                 | 0.2500             | 0.7500              | False            |
| atm        | Mean Load Penalty Loss Diff | X-n251-k28 |                 | 0.2500             | 0.7500              | False            |
| atm        | Mean Shortfall Diff         | X-n162-k11 | 3.3652          | 0.2500             | 0.7500              | True             |
| atm        | Mean Shortfall Diff         | X-n115-k10 | 0.2331          | 0.2500             | 0.7500              | False            |
| atm        | Mean Shortfall Diff         | X-n167-k10 | 0.1111          | 0.2500             | 0.7500              | False            |
| atm        | Mean Shortfall Diff         | X-n120-k6  | 0.0968          | 0.2500             | 0.7500              | False            |
| atm        | Mean Shortfall Diff         | X-n181-k23 | 0.0258          | 0.2500             | 0.7500              | False            |
| atm        | Mean Shortfall Diff         | X-n110-k13 | 0.0147          | 0.2500             | 0.7500              | False            |
| atm        | Mean Shortfall Diff         | X-n129-k18 | 0.0111          | 0.2500             | 0.7500              | False            |
| atm        | Mean Shortfall Diff         | X-n134-k13 | 0.0083          | 0.2500             | 0.7500              | False            |
| atm        | Mean Shortfall Diff         | X-n223-k34 | 0.0064          | 0.2500             | 0.7500              | False            |
| atm        | Mean Shortfall Diff         | X-n157-k13 | 0.0055          | 0.2500             | 0.7500              | False            |
| atm        | Mean Shortfall Diff         | X-n228-k23 | 0.0054          | 0.2500             | 0.7500              | False            |
| atm        | Mean Shortfall Diff         | X-n251-k28 | 0.0042          | 0.2500             | 0.7500              | False            |
| atm        | Mean Shortfall Diff         | X-n237-k14 | 0.0029          | 0.2500             | 0.7500              | False            |
| atm        | Mean Shortfall Diff         | X-n190-k8  | 0.0025          | 0.2500             | 0.7500              | False            |
| atm        | Mean Shortfall Diff         | X-n106-k14 | 0.0018          | 0.2500             | 0.7500              | False            |
| atm        | Mean Shortfall Diff         | X-n242-k48 | 0.0000          | 0.2500             | 0.7500              | False            |
| atm        | Mean Surplus Diff           | X-n162-k11 | 0.7403          | 0.2500             | 0.7500              | False            |
| atm        | Mean Surplus Diff           | X-n106-k14 | 0.6741          | 0.2500             | 0.7500              | False            |
| atm        | Mean Surplus Diff           | X-n115-k10 | 0.1923          | 0.2500             | 0.7500              | False            |
| atm        | Mean Surplus Diff           | X-n167-k10 | 0.1412          | 0.2500             | 0.7500              | False            |
| atm        | Mean Surplus Diff           | X-n120-k6  | 0.0833          | 0.2500             | 0.7500              | False            |
| atm        | Mean Surplus Diff           | X-n181-k23 | 0.0269          | 0.2500             | 0.7500              | False            |
| atm        | Mean Surplus Diff           | X-n129-k18 | 0.0138          | 0.2500             | 0.7500              | False            |
| atm        | Mean Surplus Diff           | X-n134-k13 | 0.0110          | 0.2500             | 0.7500              | False            |
| atm        | Mean Surplus Diff           | X-n223-k34 | 0.0094          | 0.2500             | 0.7500              | False            |
| atm        | Mean Surplus Diff           | X-n157-k13 | 0.0083          | 0.2500             | 0.7500              | False            |
| atm        | Mean Surplus Diff           | X-n228-k23 | 0.0083          | 0.2500             | 0.7500              | False            |
| atm        | Mean Surplus Diff           | X-n110-k13 | 0.0081          | 0.2500             | 0.7500              | False            |
| atm        | Mean Surplus Diff           | X-n251-k28 | 0.0071          | 0.2500             | 0.7500              | False            |
| atm        | Mean Surplus Diff           | X-n237-k14 | 0.0055          | 0.2500             | 0.7500              | False            |
| atm        | Mean Surplus Diff           | X-n190-k8  | 0.0007          | 0.2500             | 0.7500              | False            |
| atm        | Mean Surplus Diff           | X-n242-k48 | 0.0004          | 0.2500             | 0.7500              | False            |
| atm        | Mean Total Cost Diff        | X-n115-k10 | 0.3448          | 0.2500             | 0.7500              | False            |
| atm        | Mean Total Cost Diff        | X-n120-k6  | 0.1694          | 0.2500             | 0.7500              | False            |
| atm        | Mean Total Cost Diff        | X-n167-k10 | 0.1278          | 0.2500             | 0.7500              | False            |
| atm        | Mean Total Cost Diff        | X-n181-k23 | 0.0598          | 0.2500             | 0.7500              | False            |
| atm        | Mean Total Cost Diff        | X-n162-k11 | 0.0471          | 0.2500             | 0.7500              | False            |
| atm        | Mean Total Cost Diff        | X-n157-k13 | 0.0274          | 0.2500             | 0.7500              | False            |
| atm        | Mean Total Cost Diff        | X-n228-k23 | 0.0153          | 0.2500             | 0.7500              | False            |
| atm        | Mean Total Cost Diff        | X-n134-k13 | 0.0150          | 0.2500             | 0.7500              | False            |
| atm        | Mean Total Cost Diff        | X-n129-k18 | 0.0129          | 0.2500             | 0.7500              | False            |
| atm        | Mean Total Cost Diff        | X-n106-k14 | 0.0111          | 0.2500             | 0.7500              | False            |
| atm        | Mean Total Cost Diff        | X-n251-k28 | 0.0079          | 0.2500             | 0.7500              | False            |
| atm        | Mean Total Cost Diff        | X-n242-k48 | 0.0069          | 0.2500             | 0.7500              | False            |
| atm        | Mean Total Cost Diff        | X-n110-k13 | 0.0051          | 0.2500             | 0.7500              | False            |
| atm        | Mean Total Cost Diff        | X-n237-k14 | 0.0039          | 0.2500             | 0.7500              | False            |
| atm        | Mean Total Cost Diff        | X-n223-k34 | 0.0038          | 0.2500             | 0.7500              | False            |
| atm        | Mean Total Cost Diff        | X-n190-k8  | 0.0000          | 0.2500             | 0.7500              | False            |
| atm        | Planned Load Total Diff     | X-n106-k14 | 22.3707         | 0.2500             | 0.7500              | True             |
| atm        | Planned Load Total Diff     | X-n115-k10 | 0.2339          | 0.2500             | 0.7500              | False            |
| atm        | Planned Load Total Diff     | X-n167-k10 | 0.1201          | 0.2500             | 0.7500              | False            |
| atm        | Planned Load Total Diff     | X-n120-k6  | 0.0900          | 0.2500             | 0.7500              | False            |
| atm        | Planned Load Total Diff     | X-n162-k11 | 0.0476          | 0.2500             | 0.7500              | False            |
| atm        | Planned Load Total Diff     | X-n181-k23 | 0.0266          | 0.2500             | 0.7500              | False            |
| atm        | Planned Load Total Diff     | X-n129-k18 | 0.0125          | 0.2500             | 0.7500              | False            |
| atm        | Planned Load Total Diff     | X-n110-k13 | 0.0118          | 0.2500             | 0.7500              | False            |
| atm        | Planned Load Total Diff     | X-n134-k13 | 0.0096          | 0.2500             | 0.7500              | False            |
| atm        | Planned Load Total Diff     | X-n223-k34 | 0.0081          | 0.2500             | 0.7500              | False            |
| atm        | Planned Load Total Diff     | X-n157-k13 | 0.0069          | 0.2500             | 0.7500              | False            |
| atm        | Planned Load Total Diff     | X-n228-k23 | 0.0069          | 0.2500             | 0.7500              | False            |
| atm        | Planned Load Total Diff     | X-n251-k28 | 0.0057          | 0.2500             | 0.7500              | False            |
| atm        | Planned Load Total Diff     | X-n237-k14 | 0.0042          | 0.2500             | 0.7500              | False            |
| atm        | Planned Load Total Diff     | X-n190-k8  | 0.0019          | 0.2500             | 0.7500              | False            |
| atm        | Planned Load Total Diff     | X-n242-k48 | 0.0001          | 0.2500             | 0.7500              | False            |
| atm        | Route Cost Diff             | X-n115-k10 | 0.3611          | 0.2500             | 0.7500              | False            |
| atm        | Route Cost Diff             | X-n120-k6  | 0.1758          | 0.2500             | 0.7500              | False            |
| atm        | Route Cost Diff             | X-n167-k10 | 0.1249          | 0.2500             | 0.7500              | False            |
| atm        | Route Cost Diff             | X-n181-k23 | 0.0616          | 0.2500             | 0.7500              | False            |
| atm        | Route Cost Diff             | X-n162-k11 | 0.0417          | 0.2500             | 0.7500              | False            |
| atm        | Route Cost Diff             | X-n157-k13 | 0.0281          | 0.2500             | 0.7500              | False            |
| atm        | Route Cost Diff             | X-n134-k13 | 0.0152          | 0.2500             | 0.7500              | False            |
| atm        | Route Cost Diff             | X-n129-k18 | 0.0130          | 0.2500             | 0.7500              | False            |
| atm        | Route Cost Diff             | X-n106-k14 | 0.0118          | 0.2500             | 0.7500              | False            |
| atm        | Route Cost Diff             | X-n251-k28 | 0.0081          | 0.2500             | 0.7500              | False            |
| atm        | Route Cost Diff             | X-n228-k23 | 0.0061          | 0.2500             | 0.7500              | False            |
| atm        | Route Cost Diff             | X-n110-k13 | 0.0057          | 0.2500             | 0.7500              | False            |
| atm        | Route Cost Diff             | X-n223-k34 | 0.0057          | 0.2500             | 0.7500              | False            |
| atm        | Route Cost Diff             | X-n242-k48 | 0.0052          | 0.2500             | 0.7500              | False            |
| atm        | Route Cost Diff             | X-n237-k14 | 0.0042          | 0.2500             | 0.7500              | False            |
| atm        | Route Cost Diff             | X-n190-k8  | 0.0000          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Domain Loss Diff       | X-n162-k11 | 6.2167          | 0.2500             | 0.7500              | True             |
| cargo      | Mean Domain Loss Diff       | X-n115-k10 | 0.2143          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Domain Loss Diff       | X-n120-k6  | 0.1262          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Domain Loss Diff       | X-n167-k10 | 0.0871          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Domain Loss Diff       | X-n181-k23 | 0.0518          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Domain Loss Diff       | X-n129-k18 | 0.0172          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Domain Loss Diff       | X-n228-k23 | 0.0127          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Domain Loss Diff       | X-n157-k13 | 0.0057          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Domain Loss Diff       | X-n251-k28 | 0.0052          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Domain Loss Diff       | X-n237-k14 | 0.0044          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Domain Loss Diff       | X-n106-k14 | 0.0042          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Domain Loss Diff       | X-n242-k48 | 0.0030          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Domain Loss Diff       | X-n110-k13 | 0.0020          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Domain Loss Diff       | X-n223-k34 | 0.0020          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Domain Loss Diff       | X-n134-k13 | 0.0004          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Domain Loss Diff       | X-n190-k8  | 0.0003          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Load Penalty Loss Diff | X-n106-k14 |                 | 0.2500             | 0.7500              | False            |
| cargo      | Mean Load Penalty Loss Diff | X-n110-k13 |                 | 0.2500             | 0.7500              | False            |
| cargo      | Mean Load Penalty Loss Diff | X-n115-k10 |                 | 0.2500             | 0.7500              | False            |
| cargo      | Mean Load Penalty Loss Diff | X-n120-k6  |                 | 0.2500             | 0.7500              | False            |
| cargo      | Mean Load Penalty Loss Diff | X-n129-k18 |                 | 0.2500             | 0.7500              | False            |
| cargo      | Mean Load Penalty Loss Diff | X-n134-k13 |                 | 0.2500             | 0.7500              | False            |
| cargo      | Mean Load Penalty Loss Diff | X-n157-k13 |                 | 0.2500             | 0.7500              | False            |
| cargo      | Mean Load Penalty Loss Diff | X-n162-k11 |                 | 0.2500             | 0.7500              | False            |
| cargo      | Mean Load Penalty Loss Diff | X-n167-k10 |                 | 0.2500             | 0.7500              | False            |
| cargo      | Mean Load Penalty Loss Diff | X-n181-k23 |                 | 0.2500             | 0.7500              | False            |
| cargo      | Mean Load Penalty Loss Diff | X-n190-k8  |                 | 0.2500             | 0.7500              | False            |
| cargo      | Mean Load Penalty Loss Diff | X-n223-k34 |                 | 0.2500             | 0.7500              | False            |
| cargo      | Mean Load Penalty Loss Diff | X-n228-k23 |                 | 0.2500             | 0.7500              | False            |
| cargo      | Mean Load Penalty Loss Diff | X-n237-k14 |                 | 0.2500             | 0.7500              | False            |
| cargo      | Mean Load Penalty Loss Diff | X-n242-k48 |                 | 0.2500             | 0.7500              | False            |
| cargo      | Mean Load Penalty Loss Diff | X-n251-k28 |                 | 0.2500             | 0.7500              | False            |
| cargo      | Mean Shortfall Diff         | X-n162-k11 | 2.8152          | 0.2500             | 0.7500              | True             |
| cargo      | Mean Shortfall Diff         | X-n115-k10 | 0.2214          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Shortfall Diff         | X-n120-k6  | 0.1278          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Shortfall Diff         | X-n167-k10 | 0.0837          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Shortfall Diff         | X-n181-k23 | 0.0519          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Shortfall Diff         | X-n129-k18 | 0.0169          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Shortfall Diff         | X-n228-k23 | 0.0159          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Shortfall Diff         | X-n157-k13 | 0.0055          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Shortfall Diff         | X-n251-k28 | 0.0050          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Shortfall Diff         | X-n237-k14 | 0.0041          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Shortfall Diff         | X-n242-k48 | 0.0033          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Shortfall Diff         | X-n110-k13 | 0.0023          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Shortfall Diff         | X-n223-k34 | 0.0018          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Shortfall Diff         | X-n106-k14 | 0.0017          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Shortfall Diff         | X-n134-k13 | 0.0009          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Shortfall Diff         | X-n190-k8  | 0.0002          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Surplus Diff           | X-n162-k11 | 0.8227          | 0.2500             | 0.7500              | True             |
| cargo      | Mean Surplus Diff           | X-n106-k14 | 0.7382          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Surplus Diff           | X-n115-k10 | 0.1791          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Surplus Diff           | X-n120-k6  | 0.1075          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Surplus Diff           | X-n167-k10 | 0.1012          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Surplus Diff           | X-n181-k23 | 0.0487          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Surplus Diff           | X-n129-k18 | 0.0191          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Surplus Diff           | X-n157-k13 | 0.0083          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Surplus Diff           | X-n251-k28 | 0.0078          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Surplus Diff           | X-n237-k14 | 0.0069          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Surplus Diff           | X-n228-k23 | 0.0054          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Surplus Diff           | X-n223-k34 | 0.0042          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Surplus Diff           | X-n134-k13 | 0.0026          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Surplus Diff           | X-n190-k8  | 0.0010          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Surplus Diff           | X-n110-k13 | 0.0006          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Surplus Diff           | X-n242-k48 | 0.0006          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Total Cost Diff        | X-n115-k10 | 0.3818          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Total Cost Diff        | X-n120-k6  | 0.1716          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Total Cost Diff        | X-n228-k23 | 0.1631          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Total Cost Diff        | X-n167-k10 | 0.0815          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Total Cost Diff        | X-n162-k11 | 0.0770          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Total Cost Diff        | X-n181-k23 | 0.0751          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Total Cost Diff        | X-n129-k18 | 0.0200          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Total Cost Diff        | X-n106-k14 | 0.0166          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Total Cost Diff        | X-n223-k34 | 0.0156          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Total Cost Diff        | X-n157-k13 | 0.0146          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Total Cost Diff        | X-n237-k14 | 0.0078          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Total Cost Diff        | X-n251-k28 | 0.0078          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Total Cost Diff        | X-n242-k48 | 0.0035          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Total Cost Diff        | X-n134-k13 | 0.0028          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Total Cost Diff        | X-n190-k8  | 0.0016          | 0.2500             | 0.7500              | False            |
| cargo      | Mean Total Cost Diff        | X-n110-k13 | 0.0009          | 0.2500             | 0.7500              | False            |
| cargo      | Planned Load Total Diff     | X-n106-k14 | 19.6837         | 0.2500             | 0.7500              | True             |
| cargo      | Planned Load Total Diff     | X-n115-k10 | 0.2163          | 0.2500             | 0.7500              | False            |
| cargo      | Planned Load Total Diff     | X-n120-k6  | 0.1169          | 0.2500             | 0.7500              | False            |
| cargo      | Planned Load Total Diff     | X-n167-k10 | 0.0845          | 0.2500             | 0.7500              | False            |
| cargo      | Planned Load Total Diff     | X-n181-k23 | 0.0506          | 0.2500             | 0.7500              | False            |
| cargo      | Planned Load Total Diff     | X-n162-k11 | 0.0481          | 0.2500             | 0.7500              | False            |
| cargo      | Planned Load Total Diff     | X-n129-k18 | 0.0183          | 0.2500             | 0.7500              | False            |
| cargo      | Planned Load Total Diff     | X-n228-k23 | 0.0090          | 0.2500             | 0.7500              | False            |
| cargo      | Planned Load Total Diff     | X-n157-k13 | 0.0070          | 0.2500             | 0.7500              | False            |
| cargo      | Planned Load Total Diff     | X-n251-k28 | 0.0066          | 0.2500             | 0.7500              | False            |
| cargo      | Planned Load Total Diff     | X-n237-k14 | 0.0056          | 0.2500             | 0.7500              | False            |
| cargo      | Planned Load Total Diff     | X-n223-k34 | 0.0031          | 0.2500             | 0.7500              | False            |
| cargo      | Planned Load Total Diff     | X-n110-k13 | 0.0018          | 0.2500             | 0.7500              | False            |
| cargo      | Planned Load Total Diff     | X-n134-k13 | 0.0016          | 0.2500             | 0.7500              | False            |
| cargo      | Planned Load Total Diff     | X-n242-k48 | 0.0013          | 0.2500             | 0.7500              | False            |
| cargo      | Planned Load Total Diff     | X-n190-k8  | 0.0004          | 0.2500             | 0.7500              | False            |
| cargo      | Route Cost Diff             | X-n115-k10 | 0.4022          | 0.2500             | 0.7500              | False            |
| cargo      | Route Cost Diff             | X-n120-k6  | 0.1759          | 0.2500             | 0.7500              | False            |
| cargo      | Route Cost Diff             | X-n228-k23 | 0.1313          | 0.2500             | 0.7500              | False            |
| cargo      | Route Cost Diff             | X-n167-k10 | 0.0805          | 0.2500             | 0.7500              | False            |
| cargo      | Route Cost Diff             | X-n181-k23 | 0.0762          | 0.2500             | 0.7500              | False            |
| cargo      | Route Cost Diff             | X-n162-k11 | 0.0623          | 0.2500             | 0.7500              | False            |
| cargo      | Route Cost Diff             | X-n129-k18 | 0.0201          | 0.2500             | 0.7500              | False            |
| cargo      | Route Cost Diff             | X-n223-k34 | 0.0192          | 0.2500             | 0.7500              | False            |
| cargo      | Route Cost Diff             | X-n106-k14 | 0.0166          | 0.2500             | 0.7500              | False            |
| cargo      | Route Cost Diff             | X-n157-k13 | 0.0143          | 0.2500             | 0.7500              | False            |
| cargo      | Route Cost Diff             | X-n237-k14 | 0.0080          | 0.2500             | 0.7500              | False            |
| cargo      | Route Cost Diff             | X-n251-k28 | 0.0078          | 0.2500             | 0.7500              | False            |
| cargo      | Route Cost Diff             | X-n134-k13 | 0.0027          | 0.2500             | 0.7500              | False            |
| cargo      | Route Cost Diff             | X-n242-k48 | 0.0024          | 0.2500             | 0.7500              | False            |
| cargo      | Route Cost Diff             | X-n190-k8  | 0.0014          | 0.2500             | 0.7500              | False            |
| cargo      | Route Cost Diff             | X-n110-k13 | 0.0013          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Domain Loss Diff       | X-n162-k11 | 204.2383        | 0.2500             | 0.7500              | True             |
| cold_chain | Mean Domain Loss Diff       | X-n115-k10 | 0.1959          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Domain Loss Diff       | X-n167-k10 | 0.1250          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Domain Loss Diff       | X-n120-k6  | 0.1125          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Domain Loss Diff       | X-n228-k23 | 0.0197          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Domain Loss Diff       | X-n106-k14 | 0.0125          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Domain Loss Diff       | X-n129-k18 | 0.0117          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Domain Loss Diff       | X-n110-k13 | 0.0110          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Domain Loss Diff       | X-n181-k23 | 0.0096          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Domain Loss Diff       | X-n223-k34 | 0.0082          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Domain Loss Diff       | X-n251-k28 | 0.0074          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Domain Loss Diff       | X-n134-k13 | 0.0055          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Domain Loss Diff       | X-n190-k8  | 0.0045          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Domain Loss Diff       | X-n237-k14 | 0.0031          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Domain Loss Diff       | X-n242-k48 | 0.0027          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Domain Loss Diff       | X-n157-k13 | 0.0010          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Load Penalty Loss Diff | X-n162-k11 | 0.3595          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Load Penalty Loss Diff | X-n115-k10 | 0.2606          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Load Penalty Loss Diff | X-n120-k6  | 0.1117          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Load Penalty Loss Diff | X-n167-k10 | 0.0910          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Load Penalty Loss Diff | X-n106-k14 | 0.0314          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Load Penalty Loss Diff | X-n134-k13 | 0.0277          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Load Penalty Loss Diff | X-n228-k23 | 0.0243          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Load Penalty Loss Diff | X-n129-k18 | 0.0125          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Load Penalty Loss Diff | X-n110-k13 | 0.0110          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Load Penalty Loss Diff | X-n181-k23 | 0.0099          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Load Penalty Loss Diff | X-n223-k34 | 0.0094          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Load Penalty Loss Diff | X-n190-k8  | 0.0049          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Load Penalty Loss Diff | X-n251-k28 | 0.0045          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Load Penalty Loss Diff | X-n242-k48 | 0.0034          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Load Penalty Loss Diff | X-n237-k14 | 0.0033          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Load Penalty Loss Diff | X-n157-k13 | 0.0012          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Shortfall Diff         | X-n162-k11 | 6.6838          | 0.2500             | 0.7500              | True             |
| cold_chain | Mean Shortfall Diff         | X-n115-k10 | 0.2092          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Shortfall Diff         | X-n120-k6  | 0.1193          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Shortfall Diff         | X-n167-k10 | 0.1154          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Shortfall Diff         | X-n228-k23 | 0.0189          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Shortfall Diff         | X-n110-k13 | 0.0146          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Shortfall Diff         | X-n129-k18 | 0.0104          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Shortfall Diff         | X-n181-k23 | 0.0085          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Shortfall Diff         | X-n223-k34 | 0.0073          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Shortfall Diff         | X-n190-k8  | 0.0064          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Shortfall Diff         | X-n251-k28 | 0.0048          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Shortfall Diff         | X-n134-k13 | 0.0046          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Shortfall Diff         | X-n237-k14 | 0.0022          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Shortfall Diff         | X-n242-k48 | 0.0018          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Shortfall Diff         | X-n106-k14 | 0.0011          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Shortfall Diff         | X-n157-k13 | 0.0005          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Surplus Diff           | X-n115-k10 | 0.2149          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Surplus Diff           | X-n106-k14 | 0.1824          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Surplus Diff           | X-n120-k6  | 0.1235          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Surplus Diff           | X-n167-k10 | 0.1073          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Surplus Diff           | X-n162-k11 | 0.0938          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Surplus Diff           | X-n228-k23 | 0.0184          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Surplus Diff           | X-n110-k13 | 0.0180          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Surplus Diff           | X-n129-k18 | 0.0096          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Surplus Diff           | X-n190-k8  | 0.0088          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Surplus Diff           | X-n181-k23 | 0.0079          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Surplus Diff           | X-n223-k34 | 0.0069          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Surplus Diff           | X-n134-k13 | 0.0034          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Surplus Diff           | X-n251-k28 | 0.0024          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Surplus Diff           | X-n237-k14 | 0.0016          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Surplus Diff           | X-n242-k48 | 0.0012          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Surplus Diff           | X-n157-k13 | 0.0002          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Total Cost Diff        | X-n115-k10 | 0.3127          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Total Cost Diff        | X-n120-k6  | 0.2310          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Total Cost Diff        | X-n167-k10 | 0.1318          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Total Cost Diff        | X-n162-k11 | 0.0603          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Total Cost Diff        | X-n181-k23 | 0.0393          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Total Cost Diff        | X-n157-k13 | 0.0183          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Total Cost Diff        | X-n129-k18 | 0.0125          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Total Cost Diff        | X-n134-k13 | 0.0123          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Total Cost Diff        | X-n251-k28 | 0.0104          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Total Cost Diff        | X-n106-k14 | 0.0077          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Total Cost Diff        | X-n237-k14 | 0.0030          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Total Cost Diff        | X-n228-k23 | 0.0022          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Total Cost Diff        | X-n110-k13 | 0.0020          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Total Cost Diff        | X-n242-k48 | 0.0012          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Total Cost Diff        | X-n223-k34 | 0.0008          | 0.2500             | 0.7500              | False            |
| cold_chain | Mean Total Cost Diff        | X-n190-k8  | 0.0002          | 0.2500             | 0.7500              | False            |
| cold_chain | Planned Load Total Diff     | X-n162-k11 | 0.6338          | 0.2500             | 0.7500              | False            |
| cold_chain | Planned Load Total Diff     | X-n115-k10 | 0.2146          | 0.2500             | 0.7500              | False            |
| cold_chain | Planned Load Total Diff     | X-n120-k6  | 0.1228          | 0.2500             | 0.7500              | False            |
| cold_chain | Planned Load Total Diff     | X-n167-k10 | 0.1105          | 0.2500             | 0.7500              | False            |
| cold_chain | Planned Load Total Diff     | X-n106-k14 | 0.0309          | 0.2500             | 0.7500              | False            |
| cold_chain | Planned Load Total Diff     | X-n228-k23 | 0.0185          | 0.2500             | 0.7500              | False            |
| cold_chain | Planned Load Total Diff     | X-n110-k13 | 0.0171          | 0.2500             | 0.7500              | False            |
| cold_chain | Planned Load Total Diff     | X-n129-k18 | 0.0098          | 0.2500             | 0.7500              | False            |
| cold_chain | Planned Load Total Diff     | X-n190-k8  | 0.0081          | 0.2500             | 0.7500              | False            |
| cold_chain | Planned Load Total Diff     | X-n181-k23 | 0.0080          | 0.2500             | 0.7500              | False            |
| cold_chain | Planned Load Total Diff     | X-n223-k34 | 0.0069          | 0.2500             | 0.7500              | False            |
| cold_chain | Planned Load Total Diff     | X-n134-k13 | 0.0037          | 0.2500             | 0.7500              | False            |
| cold_chain | Planned Load Total Diff     | X-n251-k28 | 0.0031          | 0.2500             | 0.7500              | False            |
| cold_chain | Planned Load Total Diff     | X-n237-k14 | 0.0017          | 0.2500             | 0.7500              | False            |
| cold_chain | Planned Load Total Diff     | X-n242-k48 | 0.0013          | 0.2500             | 0.7500              | False            |
| cold_chain | Planned Load Total Diff     | X-n157-k13 | 0.0003          | 0.2500             | 0.7500              | False            |
| cold_chain | Route Cost Diff             | X-n115-k10 | 0.3137          | 0.2500             | 0.7500              | False            |
| cold_chain | Route Cost Diff             | X-n120-k6  | 0.2328          | 0.2500             | 0.7500              | False            |
| cold_chain | Route Cost Diff             | X-n167-k10 | 0.1293          | 0.2500             | 0.7500              | False            |
| cold_chain | Route Cost Diff             | X-n162-k11 | 0.0586          | 0.2500             | 0.7500              | False            |
| cold_chain | Route Cost Diff             | X-n181-k23 | 0.0395          | 0.2500             | 0.7500              | False            |
| cold_chain | Route Cost Diff             | X-n157-k13 | 0.0184          | 0.2500             | 0.7500              | False            |
| cold_chain | Route Cost Diff             | X-n134-k13 | 0.0126          | 0.2500             | 0.7500              | False            |
| cold_chain | Route Cost Diff             | X-n129-k18 | 0.0125          | 0.2500             | 0.7500              | False            |
| cold_chain | Route Cost Diff             | X-n251-k28 | 0.0103          | 0.2500             | 0.7500              | False            |
| cold_chain | Route Cost Diff             | X-n106-k14 | 0.0079          | 0.2500             | 0.7500              | False            |
| cold_chain | Route Cost Diff             | X-n237-k14 | 0.0030          | 0.2500             | 0.7500              | False            |
| cold_chain | Route Cost Diff             | X-n110-k13 | 0.0021          | 0.2500             | 0.7500              | False            |
| cold_chain | Route Cost Diff             | X-n228-k23 | 0.0012          | 0.2500             | 0.7500              | False            |
| cold_chain | Route Cost Diff             | X-n242-k48 | 0.0011          | 0.2500             | 0.7500              | False            |
| cold_chain | Route Cost Diff             | X-n223-k34 | 0.0010          | 0.2500             | 0.7500              | False            |
| cold_chain | Route Cost Diff             | X-n190-k8  | 0.0003          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Domain Loss Diff       | X-n162-k11 | 43.9254         | 0.2500             | 0.7500              | True             |
| grocery    | Mean Domain Loss Diff       | X-n115-k10 | 0.2222          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Domain Loss Diff       | X-n120-k6  | 0.1153          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Domain Loss Diff       | X-n167-k10 | 0.0996          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Domain Loss Diff       | X-n181-k23 | 0.0190          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Domain Loss Diff       | X-n110-k13 | 0.0139          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Domain Loss Diff       | X-n228-k23 | 0.0139          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Domain Loss Diff       | X-n129-k18 | 0.0107          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Domain Loss Diff       | X-n106-k14 | 0.0092          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Domain Loss Diff       | X-n223-k34 | 0.0068          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Domain Loss Diff       | X-n251-k28 | 0.0055          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Domain Loss Diff       | X-n134-k13 | 0.0029          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Domain Loss Diff       | X-n157-k13 | 0.0026          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Domain Loss Diff       | X-n237-k14 | 0.0025          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Domain Loss Diff       | X-n190-k8  | 0.0023          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Domain Loss Diff       | X-n242-k48 | 0.0003          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Load Penalty Loss Diff | X-n106-k14 |                 | 0.2500             | 0.7500              | False            |
| grocery    | Mean Load Penalty Loss Diff | X-n110-k13 |                 | 0.2500             | 0.7500              | False            |
| grocery    | Mean Load Penalty Loss Diff | X-n115-k10 |                 | 0.2500             | 0.7500              | False            |
| grocery    | Mean Load Penalty Loss Diff | X-n120-k6  |                 | 0.2500             | 0.7500              | False            |
| grocery    | Mean Load Penalty Loss Diff | X-n129-k18 |                 | 0.2500             | 0.7500              | False            |
| grocery    | Mean Load Penalty Loss Diff | X-n134-k13 |                 | 0.2500             | 0.7500              | False            |
| grocery    | Mean Load Penalty Loss Diff | X-n157-k13 |                 | 0.2500             | 0.7500              | False            |
| grocery    | Mean Load Penalty Loss Diff | X-n162-k11 |                 | 0.2500             | 0.7500              | False            |
| grocery    | Mean Load Penalty Loss Diff | X-n167-k10 |                 | 0.2500             | 0.7500              | False            |
| grocery    | Mean Load Penalty Loss Diff | X-n181-k23 |                 | 0.2500             | 0.7500              | False            |
| grocery    | Mean Load Penalty Loss Diff | X-n190-k8  |                 | 0.2500             | 0.7500              | False            |
| grocery    | Mean Load Penalty Loss Diff | X-n223-k34 |                 | 0.2500             | 0.7500              | False            |
| grocery    | Mean Load Penalty Loss Diff | X-n228-k23 |                 | 0.2500             | 0.7500              | False            |
| grocery    | Mean Load Penalty Loss Diff | X-n237-k14 |                 | 0.2500             | 0.7500              | False            |
| grocery    | Mean Load Penalty Loss Diff | X-n242-k48 |                 | 0.2500             | 0.7500              | False            |
| grocery    | Mean Load Penalty Loss Diff | X-n251-k28 |                 | 0.2500             | 0.7500              | False            |
| grocery    | Mean Shortfall Diff         | X-n162-k11 | 5.2196          | 0.2500             | 0.7500              | True             |
| grocery    | Mean Shortfall Diff         | X-n115-k10 | 0.2312          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Shortfall Diff         | X-n120-k6  | 0.1196          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Shortfall Diff         | X-n167-k10 | 0.0947          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Shortfall Diff         | X-n181-k23 | 0.0184          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Shortfall Diff         | X-n110-k13 | 0.0160          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Shortfall Diff         | X-n228-k23 | 0.0131          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Shortfall Diff         | X-n129-k18 | 0.0099          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Shortfall Diff         | X-n223-k34 | 0.0061          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Shortfall Diff         | X-n251-k28 | 0.0043          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Shortfall Diff         | X-n190-k8  | 0.0036          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Shortfall Diff         | X-n134-k13 | 0.0023          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Shortfall Diff         | X-n157-k13 | 0.0020          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Shortfall Diff         | X-n237-k14 | 0.0020          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Shortfall Diff         | X-n106-k14 | 0.0014          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Shortfall Diff         | X-n242-k48 | 0.0001          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Surplus Diff           | X-n106-k14 | 1.4577          | 0.2500             | 0.7500              | True             |
| grocery    | Mean Surplus Diff           | X-n115-k10 | 0.2342          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Surplus Diff           | X-n120-k6  | 0.1224          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Surplus Diff           | X-n167-k10 | 0.0845          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Surplus Diff           | X-n181-k23 | 0.0179          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Surplus Diff           | X-n110-k13 | 0.0176          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Surplus Diff           | X-n228-k23 | 0.0126          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Surplus Diff           | X-n162-k11 | 0.0095          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Surplus Diff           | X-n129-k18 | 0.0092          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Surplus Diff           | X-n190-k8  | 0.0072          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Surplus Diff           | X-n223-k34 | 0.0059          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Surplus Diff           | X-n251-k28 | 0.0025          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Surplus Diff           | X-n134-k13 | 0.0017          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Surplus Diff           | X-n157-k13 | 0.0016          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Surplus Diff           | X-n237-k14 | 0.0015          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Surplus Diff           | X-n242-k48 | 0.0000          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Total Cost Diff        | X-n115-k10 | 0.3556          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Total Cost Diff        | X-n120-k6  | 0.2193          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Total Cost Diff        | X-n167-k10 | 0.1091          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Total Cost Diff        | X-n181-k23 | 0.0548          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Total Cost Diff        | X-n162-k11 | 0.0518          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Total Cost Diff        | X-n157-k13 | 0.0225          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Total Cost Diff        | X-n129-k18 | 0.0119          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Total Cost Diff        | X-n106-k14 | 0.0097          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Total Cost Diff        | X-n251-k28 | 0.0091          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Total Cost Diff        | X-n134-k13 | 0.0084          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Total Cost Diff        | X-n242-k48 | 0.0050          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Total Cost Diff        | X-n110-k13 | 0.0040          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Total Cost Diff        | X-n228-k23 | 0.0032          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Total Cost Diff        | X-n237-k14 | 0.0028          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Total Cost Diff        | X-n223-k34 | 0.0013          | 0.2500             | 0.7500              | False            |
| grocery    | Mean Total Cost Diff        | X-n190-k8  | 0.0000          | 0.2500             | 0.7500              | False            |
| grocery    | Planned Load Total Diff     | X-n115-k10 | 0.2391          | 0.2500             | 0.7500              | False            |
| grocery    | Planned Load Total Diff     | X-n106-k14 | 0.1523          | 0.2500             | 0.7500              | False            |
| grocery    | Planned Load Total Diff     | X-n120-k6  | 0.1235          | 0.2500             | 0.7500              | False            |
| grocery    | Planned Load Total Diff     | X-n162-k11 | 0.0950          | 0.2500             | 0.7500              | False            |
| grocery    | Planned Load Total Diff     | X-n167-k10 | 0.0879          | 0.2500             | 0.7500              | False            |
| grocery    | Planned Load Total Diff     | X-n110-k13 | 0.0181          | 0.2500             | 0.7500              | False            |
| grocery    | Planned Load Total Diff     | X-n181-k23 | 0.0178          | 0.2500             | 0.7500              | False            |
| grocery    | Planned Load Total Diff     | X-n228-k23 | 0.0124          | 0.2500             | 0.7500              | False            |
| grocery    | Planned Load Total Diff     | X-n129-k18 | 0.0091          | 0.2500             | 0.7500              | False            |
| grocery    | Planned Load Total Diff     | X-n190-k8  | 0.0061          | 0.2500             | 0.7500              | False            |
| grocery    | Planned Load Total Diff     | X-n223-k34 | 0.0056          | 0.2500             | 0.7500              | False            |
| grocery    | Planned Load Total Diff     | X-n251-k28 | 0.0028          | 0.2500             | 0.7500              | False            |
| grocery    | Planned Load Total Diff     | X-n134-k13 | 0.0017          | 0.2500             | 0.7500              | False            |
| grocery    | Planned Load Total Diff     | X-n157-k13 | 0.0015          | 0.2500             | 0.7500              | False            |
| grocery    | Planned Load Total Diff     | X-n237-k14 | 0.0014          | 0.2500             | 0.7500              | False            |
| grocery    | Planned Load Total Diff     | X-n242-k48 | 0.0000          | 0.2500             | 0.7500              | False            |
| grocery    | Route Cost Diff             | X-n115-k10 | 0.3607          | 0.2500             | 0.7500              | False            |
| grocery    | Route Cost Diff             | X-n120-k6  | 0.2223          | 0.2500             | 0.7500              | False            |
| grocery    | Route Cost Diff             | X-n167-k10 | 0.1075          | 0.2500             | 0.7500              | False            |
| grocery    | Route Cost Diff             | X-n181-k23 | 0.0553          | 0.2500             | 0.7500              | False            |
| grocery    | Route Cost Diff             | X-n162-k11 | 0.0493          | 0.2500             | 0.7500              | False            |
| grocery    | Route Cost Diff             | X-n157-k13 | 0.0227          | 0.2500             | 0.7500              | False            |
| grocery    | Route Cost Diff             | X-n129-k18 | 0.0120          | 0.2500             | 0.7500              | False            |
| grocery    | Route Cost Diff             | X-n106-k14 | 0.0099          | 0.2500             | 0.7500              | False            |
| grocery    | Route Cost Diff             | X-n251-k28 | 0.0091          | 0.2500             | 0.7500              | False            |
| grocery    | Route Cost Diff             | X-n134-k13 | 0.0084          | 0.2500             | 0.7500              | False            |
| grocery    | Route Cost Diff             | X-n242-k48 | 0.0044          | 0.2500             | 0.7500              | False            |
| grocery    | Route Cost Diff             | X-n110-k13 | 0.0042          | 0.2500             | 0.7500              | False            |
| grocery    | Route Cost Diff             | X-n237-k14 | 0.0029          | 0.2500             | 0.7500              | False            |
| grocery    | Route Cost Diff             | X-n223-k34 | 0.0017          | 0.2500             | 0.7500              | False            |
| grocery    | Route Cost Diff             | X-n228-k23 | 0.0014          | 0.2500             | 0.7500              | False            |
| grocery    | Route Cost Diff             | X-n190-k8  | 0.0000          | 0.2500             | 0.7500              | False            |

| Domain     | Predictor               | n  | Unique x Levels | Pearson r | p-value | Bootstrap CI Low | Bootstrap CI High | CI Contains Zero | Evidence Label                                    | Dropped Instance |
| ---------- | ----------------------- | -- | --------------- | --------- | ------- | ---------------- | ----------------- | ---------------- | ------------------------------------------------- | ---------------- |
| atm        | Mean Domain Loss Diff   | 15 | 15              | 0.4443    | 0.0971  | 0.3306           | 0.9716            | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 | X-n162-k11       |
| atm        | Mean Shortfall Diff     | 15 | 15              | 0.4262    | 0.1131  | 0.3031           | 0.9723            | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 | X-n162-k11       |
| atm        | Planned Load Total Diff | 15 | 15              | -0.4708   | 0.0765  | -0.8958          | 0.0379            | True             | no_correlation_ci_crosses_zero                    | X-n106-k14       |
| cargo      | Mean Domain Loss Diff   | 15 | 15              | 0.4094    | 0.1296  | 0.3076           | 0.9000            | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 | X-n162-k11       |
| cargo      | Mean Shortfall Diff     | 15 | 15              | 0.3829    | 0.1590  | 0.2483           | 0.9044            | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 | X-n162-k11       |
| cargo      | Mean Surplus Diff       | 15 | 15              | -0.2346   | 0.4001  | -0.7689          | 0.7701            | True             | no_correlation_ci_crosses_zero                    | X-n162-k11       |
| cargo      | Planned Load Total Diff | 15 | 15              | -0.4056   | 0.1336  | -0.8367          | 0.5857            | True             | no_correlation_ci_crosses_zero                    | X-n106-k14       |
| cold_chain | Mean Domain Loss Diff   | 15 | 15              | 0.6667    | 0.0066  | 0.3109           | 0.9272            | False            | candidate_mechanism                               | X-n162-k11       |
| cold_chain | Mean Shortfall Diff     | 15 | 15              | 0.4944    | 0.0610  | 0.3997           | 0.9900            | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 | X-n162-k11       |
| grocery    | Mean Domain Loss Diff   | 15 | 15              | 0.5647    | 0.0283  | 0.4642           | 0.9739            | False            | candidate_mechanism                               | X-n162-k11       |
| grocery    | Mean Shortfall Diff     | 15 | 15              | 0.4749    | 0.0736  | 0.3851           | 0.9836            | False            | directional_signal_ci_excludes_zero_but_p_ge_0_05 | X-n162-k11       |
| grocery    | Mean Surplus Diff       | 15 | 15              | -0.5468   | 0.0349  | -0.9451          | -0.4356           | False            | candidate_mechanism                               | X-n106-k14       |

## Finding

Objective-component diffs show associations with stockout in the raw correlations, but after controlling for Load Variance Diff they do not provide a clean independent mechanism. This supports the current view that route-level load allocation is the primary measured mechanism, while objective interaction remains a downstream or coupled effect rather than an independent explanation.

## Correct Sentence

Objective interaction is coupled with stockout changes, but on the current X24 common-feasible set it should not replace route-level load allocation as the primary measured mechanism unless it remains significant after controlling for load allocation.

## Next Step

Run a controlled model with both predictors in the same regression: `stockout_diff ~ load_variance_diff + objective_component_diff`, then repeat on a larger X set with a stronger non-demo LP backend or a route-feasible instance filter fixed before seeing outcomes.
