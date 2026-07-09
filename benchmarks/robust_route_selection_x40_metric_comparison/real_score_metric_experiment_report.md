# Real Score-Metric X40 Experiment Report

## Scope

Bu rapor, X40 OR-Tools-only robust-route-selection deneylerini karsilastirir. `mean_domain_loss` ve `stockout_rate` sonuclari post-hoc re-ranking degildir; her biri kendi `--score-metric` ayariyla route candidate scoring, stochastic LP allocation ve full-scenario winner confirmation adimlarini yeniden calistirdi.

| Score metric | Candidate rows | Candidate feasible rows | Winner rows | Winner instances | Full-confirmed rows |
| --- | ---: | ---: | ---: | ---: | ---: |
| `mean_total_cost` | 1760 | 456 | 112 | 28 | 112 |
| `mean_domain_loss` | 1760 | 456 | 112 | 28 | 112 |
| `stockout_rate` | 1760 | 456 | 112 | 28 | 112 |

No-winner instance listesi uc kosuda da ayni kaldi: `X-n101-k25`, `X-n125-k30`, `X-n148-k46`, `X-n153-k22`, `X-n172-k51`, `X-n176-k26`, `X-n195-k51`, `X-n200-k36`, `X-n247-k50`, `X-n256-k16`, `X-n266-k58`, `X-n270-k35`.

## Main Finding

Default `mean_total_cost`, route cost tarafindan domine ediliyor: 28 winner-producing instance'in hicbirinde domain-specific route switching yoktu.

`mean_domain_loss` ve `stockout_rate` bu sonucu degistirdi:

| Score metric | Domain-specific instances | Fully certified instances | Certified domain-specific instances | Top route plan share | Ranking flip rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| `mean_total_cost` | 0 / 28 | 17 | 0 / 17 | 92.9% | 39.3% |
| `mean_domain_loss` | 7 / 28 | 14 | 5 / 14 | 53.6% | 50.0% |
| `stockout_rate` | 6 / 28 | 14 | 3 / 14 | 61.6% | 50.0% |

Interpretation: objective secimi gercekten rota winner'ini degistiriyor. Bu sinyal post-hoc degil; full-confirmed real run ile tekrar goruldu. En guclu aday `mean_domain_loss`.

## Certified Diversity

`mean_domain_loss` altinda certified domain-specific route choice kalan instance'lar:

| Instance | Certified route plans | Audit risk | Anchor feasible |
| --- | ---: | --- | --- |
| `X-n134-k13` | 2 | medium | yes |
| `X-n143-k7` | 4 | medium | yes |
| `X-n190-k8` | 2 | medium | yes |
| `X-n214-k11` | 3 | high | yes |
| `X-n233-k16` | 2 | high | no |

`stockout_rate` altinda certified domain-specific route choice kalan instance'lar:

| Instance | Certified route plans | Audit risk | Anchor feasible |
| --- | ---: | --- | --- |
| `X-n134-k13` | 2 | medium | yes |
| `X-n190-k8` | 2 | medium | yes |
| `X-n261-k13` | 2 | medium | yes |

## Feasibility / Bias Check

Coverage uc kosuda ayni: 40 attempted instance, 456 feasible candidate row, 112 winner row. Bu iyi: yeni diversity, daha dar veya farkli bir feasible subset secildigi icin ortaya cikmadi.

Yine de capacity-pressure bias tamamen yok degil:

- Baseline no-winner instance'larin tamami high-risk/medium-capacity-pressure bolgesinde kaliyor.
- `mean_domain_loss` certified diversity'nin 2/5'i high-risk instance'lardan geliyor.
- `stockout_rate` certified diversity'nin 3/3'u medium-risk ve anchor-feasible instance'lardan geliyor.

Bu yuzden `mean_domain_loss` daha guclu gorunse de, high-risk katkisi ayrica kontrol edilmeli.

## Correct Sentence

X40 OR-Tools-only gercek deneylerinde, `mean_domain_loss` ve `stockout_rate` score metric'leri domain-specific route switching'i post-hoc seviyeden full-confirmed deney seviyesine tasidi; karar-ready iddia ise yalnizca `Strict Stability Safe` kalan subset icin gecerli. Bu subset'te `mean_domain_loss` 5, `stockout_rate` 3 certified domain-specific instance uretti.

## Not Yet Correct Sentence

"Domain-aware stochastic route selection her durumda default routing'i yener."

Bu desteklenmiyor. Yeni objective'ler rota secimini degistiriyor, fakat strict-safe oran %50'ye dustu ve ranking flip orani %50'ye cikti.

## Decision

Bir sonraki calismaya `mean_domain_loss` uzerinden devam etmek daha mantikli. Gerekce: default objective'e gore route-plan cesitliligini ciddi artirdi, top route plan dominance'i 92.9%'dan 53.6%'ya indirdi ve strict-safe subset'te 5 certified domain-specific instance birakti.

## Next Step

`mean_domain_loss` icin stability sorununu azaltmaya odaklan:

1. Candidate pool'u genislet: OR-Tools randomized seed / longer time-limit variant'lari ekle.
2. Winner secimini tek metrikten cok amacli hale getir: `mean_domain_loss` minimize ederken ranking stability veya stockout drift gate'i tie-breaker olarak kullan.
3. High-risk instance etkisini ayir: once anchor-feasible + medium-risk subset'te certified diversity'yi raporla, sonra high-risk rescue-plan bulgusunu ayri tartis.
