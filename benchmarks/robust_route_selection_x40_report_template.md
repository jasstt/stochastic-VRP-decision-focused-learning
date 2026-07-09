# Robust Route Selection X40 Report Template

Bu taslak, X40 `run_robust_route_selection --confirm-winners-full-scenario`
sonucu geldikten sonra rapor dilinin hipotezi zorlamadan yazılması icin
hazirlandi. Kaynak dersler:

- `benchmarks/proxy_cvrplib_x_v4/scenario_reduction_bias_report.md`
- `benchmarks/robust_route_selection_stability_smoke/robust_route_selection_report.md`
- `sector-stability-tolerance` smoke raporu

## Scope

Bu kosu, OR-Tools route candidate setini ayni stochastic decision layer uzerinden
domain bazinda skorlar ve her `Instance x Domain` icin bir winner secer.

- Dataset: `benchmarks/proxy_cvrplib_x_v4`
- Provider: `[ortools-only / ortools+vroom]`
- LP backend: `[pulp_cbc]`
- Fast screening: `--lp-planning-scenario-limit 60`
- Full confirmation: `--confirm-winners-full-scenario`
- Score metric: `[mean_total_cost / stockout_rate / ...]`
- Instances attempted: `[N]`
- Instances with at least one feasible route candidate: `[N]`
- Winner rows: `[N]`
- Full-confirmed winner rows: `[N]`

## Executive Finding

Kisa karar cumlesi burada olacak:

> X40 kosusunda robust route selection, `[X/Y]` winner row icin full-scenario
> confirmation uretti; bunlarin `[A/B]` tanesi `Strict Stability Safe` oldu.
> Domain-specific winner diversity `[gozlendi / gozlenmedi / sinirli kaldı]`.

Bu cumle sadece full confirmation sonucu geldikten sonra doldurulmali.

## Certified Winner Rate

`Certified Winner Rate`, sadece secilmis winner row'lari uzerinden hesaplanir:

```text
certified_winner_rate =
    strict_stability_safe_winner_rows / full_confirmed_winner_rows
```

Yorum kurali:

- `Strict Stability Safe = yes`: winner decision-ready kabul edilebilir.
- `Metric Stability Safe = yes` ama `Ranking Stable = no`: winner metric olarak
  yakin olabilir, fakat domain ranking flip nedeniyle final iddia risklidir.
- `Confirm Feasible = no`: karar verdiren sonuc degil; final full run veya
  route/provider ayari gerekir.

### Certified Winner Summary

| Metric | Value |
| --- | --- |
| Winner rows | `[N]` |
| Full-confirmed winner rows | `[N]` |
| Metric-safe winner rows | `[N]` |
| Ranking-stable winner rows | `[N]` |
| Strict stability safe winner rows | `[N]` |
| Certified winner rate | `[PCT]` |

## Domain Winner Diversity

Domain winner diversity, ayni instance icinde farkli domain'lerin farkli route
candidate'lari secip secmedigini olcer.

Onerilen instance-level metrik:

```text
winner_diversity =
    unique_winning_candidates_in_instance / confirmed_domains_in_instance
```

Yorum kurali:

- `unique_winning_candidates > 1`: domain objective route kararini degistirdi;
  bu, domain-aware route selection icin pozitif sinyaldir.
- `unique_winning_candidates = 1`: bu instance/candidate set/score metric
  altinda sector-specific route switching gozlenmedi. Bu, modeli curutmez;
  yalnizca mevcut aday havuzunda ortak winner'in baskin oldugunu soyler.
- Diversity sadece `Strict Stability Safe` winner'lar uzerinden ayrica
  raporlanmali. Unsafe winner diversity karar-ready bulgu degildir.

### Diversity Summary

| Metric | Value |
| --- | --- |
| Instances with confirmed winners | `[N]` |
| Instances with certified winners | `[N]` |
| Instances with domain winner diversity | `[N]` |
| Instances with certified domain winner diversity | `[N]` |
| Mean winner diversity | `[VALUE]` |
| Top repeated winning candidate | `[CANDIDATE]` |

### Per-Instance Diversity Table

| Instance | Confirmed Domains | Unique Winners | Winner Diversity | Certified Unique Winners | Certified Diversity | Interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| `[instance]` | `[N]` | `[N]` | `[VALUE]` | `[N]` | `[VALUE]` | `[diverse/common/unsafe]` |

## Feasibility and Coverage Warning

Bu bolum mutlaka yazilmali. Winner diversity veya certified rate, yalnizca
feasible ve confirmed satirlar uzerinden anlamlidir.

Rapor dili:

> Infeasible high-quantile/robust candidates are part of the result, not rows to
> hide. They show when the tested fleet capacity cannot support that demand
> profile.

Kontrol edilecek alanlar:

- Candidate rows
- Route feasible rows
- LP feasible rows
- Candidate feasible rows
- Winner rows
- Full confirmation feasible rows
- Instances with no feasible candidate
- Domains with missing winner rows

### Coverage Table

| Domain | Candidate Rows | Candidate Feasible Rows | Winner Rows | Confirm Feasible Rows | Strict Safe Rows | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| atm | `[N]` | `[N]` | `[N]` | `[N]` | `[N]` | `[note]` |
| cargo | `[N]` | `[N]` | `[N]` | `[N]` | `[N]` | `[note]` |
| cold_chain | `[N]` | `[N]` | `[N]` | `[N]` | `[N]` | `[note]` |
| grocery | `[N]` | `[N]` | `[N]` | `[N]` | `[N]` | `[note]` |

## Stability Gate Interpretation

Metric-safe olmak tek basina yeterli degildir. Sector-stability testinin ana
dersi: stockout/cost drift dusuk olsa bile domain ranking flip varsa final
iddia risklidir.

Karar tablosu:

| Condition | Report Status | Language |
| --- | --- | --- |
| Confirm feasible + metric-safe + ranking-stable | Certified / decision-ready | "winner certified under full-scenario confirmation" |
| Confirm feasible + metric-safe + ranking flip | Not decision-ready | "metric drift is small, but ranking instability blocks the final claim" |
| Confirm feasible + metric drift exceeded | Not decision-ready | "full scenario changed the winner metrics beyond tolerance" |
| Confirmation infeasible | Not decision-ready | "winner requires full rerun or provider/candidate investigation" |

## Correct Sentence

Sonuca gore birini sec:

1. Diversity varsa:

> X40 OR-Tools-only kosusunda, domain-aware stochastic route selection bazi
> instance'larda farkli sector objective'leri icin farkli route winner'lari
> uretmistir; ancak decision-ready iddia yalnizca full-scenario confirmation
> sonrasi `Strict Stability Safe` kalan winner row'lar icin gecerlidir.

2. Diversity yoksa:

> X40 OR-Tools-only kosusunda, mevcut candidate set ve score metric altinda
> domain winner diversity gozlenmedi; buna ragmen stability gate, ortak
> winner'larin hangi satirlarda decision-ready oldugunu ayirmistir.

3. Diversity var ama unsafe ise:

> X40 kosusunda domain winner diversity aday sinyali verdi, fakat ranking flip
> veya metric drift nedeniyle bu sinyal henuz decision-ready bulgu degildir.

## Not Yet Correct Sentence

Asagidaki cumleler sonuc ne olursa olsun dogrudan yazilmamali:

- "Fast mode full scenario ile esdegerdir."
- "Metric-safe winner her zaman final karar icin guvenlidir."
- "Domain-aware selection her instance'ta farkli route secer."
- "OR-Tools candidate setinde kazanan route global optimumdur."
- "Winner diversity yoksa domain adapter'lar etkisizdir."
- "Ranking flip olsa bile mean_total_cost dusukse sonuc guvenlidir."

## If the Result Is Weak

Eger X40 sonucu zayifsa veya diversity yoksa rapor bunu net soylemeli:

> Bu kosu, domain-specific route switching iddiasini guclendirmedi. Muhtemel
> nedenler: candidate route havuzu yeterince cesitli degil, score metric
> domain farkini bastiriyor, OR-Tools-only provider izolasyonu route topolojisi
> farkini sinirliyor veya tested instances kapasite baskisi nedeniyle ayni
> feasible adaylara daraliyor.

Sonraki adim onerileri:

- Candidate seti genislet: daha fazla time limit, randomized seed, veya VROOM
  provider eklentisi.
- Score metric sensitivity calistir: `mean_total_cost`, `stockout_rate`,
  `mean_domain_loss`, `cvar90_total_cost`.
- Diversity analizini yalnizca `Strict Stability Safe` winner'larla tekrar et.

## If the Result Is Strong

Eger X40 sonucu gucluyse rapor yine temkinli kalmali:

> Bu, domain-aware route selection icin guclu bir gozlemsel sinyaldir; fakat
> henuz tum sektorler veya tum routing provider'lar icin genel kanit degildir.
> Provider switch ve perturbation stability ayri dogrulanmalidir.

Eklenmesi gereken kontroller:

- Certified diversity rate
- Provider sensitivity
- Score metric sensitivity
- Instance-size bucket ozeti
- Feasibility bias: diversity sadece kolay feasible instance'larda mi cikiyor?

## N / Feasibility / A.5 Warning

Bu rapor korelasyon testi degilse A.5 bootstrap zorunlu degildir, fakat dil
disiplini ayni kalmali:

- `n < 15`: "diagnostic signal" de, "kanıt" deme.
- Dengesiz feasibility varsa yuzdeleri tum X40 uzerinden ve feasible subset
  uzerinden ayri ver.
- Bir domain veya instance bucket cok az temsil ediliyorsa genelleme yapma.
- Full confirmation olmadan final README sayisi yazma.

## Recommended Final Paragraph

> Robust route selection, route solver'in yerine gecen yeni bir solver degil;
> mevcut route candidate'larini sector-specific stochastic objective ile
> skorlayan ve stability gate ile karar guvenilirligini ayiran bir decision
> layer'dir. X40 sonucunun ana degeri, sadece kimin kazandigi degil, hangi
> winner'larin full-scenario confirmation sonrasi decision-ready kaldigidir.
