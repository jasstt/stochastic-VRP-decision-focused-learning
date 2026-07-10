# Risk Isolation Decision Report

## Bulgu

Risk isolation passed: certified diversity is not only a high-risk artifact. Clean subset counts are mean_domain_loss=3, stockout_rate=3.

| Score Metric | Risk Isolation Group | Instances | Winner Domain-Specific Instances | Fully Certified Instances | Certified Domain-Specific Instances | Certified Diversity Share | Certified Domain-Specific Instance List |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mean_domain_loss | anchor_feasible_medium_risk | 24 | 5 | 12 | 3 | 0.25 | X-n134-k13, X-n143-k7, X-n190-k8 |
| mean_domain_loss | high_risk_or_anchor_infeasible | 4 | 2 | 2 | 2 | 1 | X-n214-k11, X-n233-k16 |
| mean_total_cost | anchor_feasible_medium_risk | 24 | 0 | 16 | 0 | 0 |  |
| mean_total_cost | high_risk_or_anchor_infeasible | 4 | 0 | 1 | 0 | 0 |  |
| stockout_rate | anchor_feasible_medium_risk | 24 | 6 | 13 | 3 | 0.230769 | X-n134-k13, X-n190-k8, X-n261-k13 |
| stockout_rate | high_risk_or_anchor_infeasible | 4 | 0 | 1 | 0 | 0 |  |

## Karar

Risk izolasyonu gecildi. `mean_domain_loss` ile devam etmek guvenli temel uzerinde duruyor. Sonraki adim: candidate pool genisletme ve multi-objective tie-breaker.

- Branch status: `KISMEN/POSITIVE_DIAGNOSTIC`
- Max clean certified diversity: `3`
- Medium-risk instance count: `24`

## Onceki Turlar

- TUR 1 post-hoc: `mean_total_cost` domain-specific choice uretmedi; `mean_domain_loss` ve `stockout_rate` re-ranking sinyali verdi.
- TUR 2 real run: `mean_domain_loss` ve `stockout_rate` gercek kosuda domain-specific winner uretirken strict-safe oran %50'ye dustu.
- TUR 3 risk isolation: temiz subset'te certified diversity yukaridaki tabloda ayrildi.

## Baseline Comparison

| Score Metric | Domain-Specific Instances | Fully Certified Instances | Certified Domain-Specific Instances | Ranking Flip Rate | Top Route Plan Share |
| --- | --- | --- | --- | --- | --- |
| mean_total_cost | 0 | 17 | 0 | 0.392857 | 0.928571 |
| mean_domain_loss | 7 | 14 | 5 | 0.5 | 0.535714 |
| stockout_rate | 6 | 14 | 3 | 0.5 | 0.616071 |

## Sonraki Adim

Candidate pool genisletme ve tie-breaker testi yalnizca `anchor_feasible_medium_risk` subset'inde calistirilacak.

## Gorev 4 Takip Sonucu

Risk izolasyonu pozitif ciktigi icin candidate pool genisletme ve tie-breaker testi calistirildi.

| Test | Candidate rows | Candidate feasible rows | Winner domain-specific instances | Fully certified instances | Certified domain-specific instances | Ranking flip rate | Strict-safe rows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Medium-risk baseline `mean_domain_loss` | 1056 | 360 | 5 / 24 | 12 | 3 | n/a | n/a |
| Seeded candidate pool | 1536 | 700 | 6 / 24 | 10 | 0 | 12 / 24 | 45 / 96 |
| Seeded pool + stockout-drift tie-breaker | 1536 | 700 | 20 / 24 | 13 | 10 | 11 / 24 | 52 / 96 |

Takip sonucu: candidate pool tek basina yeterli olmadi; stockout-drift tie-breaker certified diversity'yi 10 instance'a cikardi. Buna ragmen ranking flip 11 / 24 kaldigi icin branch PASS degil; durum `KISMEN/STRONG_DIAGNOSTIC`.
