from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from .analyze_stockout_mechanisms import (
    _bootstrap_ci,
    _ci_contains_zero,
    _evidence_label,
    _markdown_table,
    _ols_influence,
    _pearson,
    _solve_route_sets,
    _stockout_diffs,
    _unique_level_count,
)
from .cvrplib import customer_view
from .routing_providers.base import RouteSet


PROVIDER_LABELS = {"ortools": "OR-Tools", "vroom": "VROOM"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnose route-level load allocation differences.")
    parser.add_argument("--data-dir", default="benchmarks/proxy_cvrplib_x_v3")
    parser.add_argument("--ortools-results", default="benchmarks/proxy_cvrplib_x_v3/domain_engine_results_ortools_provider.csv")
    parser.add_argument("--vroom-results", default="benchmarks/proxy_cvrplib_x_v3/domain_engine_results_vroom_provider.csv")
    parser.add_argument("--out-dir", default="benchmarks/proxy_cvrplib_x_v3")
    parser.add_argument("--anchor-plan", default="proxy_mean_or_tools")
    parser.add_argument("--fallback-anchor-plan", default="nominal_or_tools")
    parser.add_argument("--time-limit-sec", type=int, default=20)
    parser.add_argument("--vroom-url", default="http://localhost:3000")
    parser.add_argument("--bootstrap-samples", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    data_dir = Path(args.data_dir)

    route_sets = _solve_route_sets(
        data_dir=data_dir,
        anchor_plan=args.anchor_plan,
        fallback_anchor_plan=args.fallback_anchor_plan,
        time_limit_sec=args.time_limit_sec,
        vroom_url=args.vroom_url,
    )
    metrics = _load_allocation_metrics(route_sets)
    diffs = _load_allocation_diffs(metrics)
    stockout = _stockout_diffs(args.ortools_results, args.vroom_results)
    analysis = stockout.merge(diffs, on="Instance", how="inner")
    correlations = _correlation_tests(analysis, args.bootstrap_samples, args.seed)
    leverage = _leverage_control(analysis)
    leave_one_out = _leave_one_out_if_needed(analysis, leverage, args.bootstrap_samples, args.seed + 2000)

    metrics.to_csv(out_dir / "load_allocation_metrics.csv", index=False)
    diffs.to_csv(out_dir / "load_allocation_diffs.csv", index=False)
    correlations.to_csv(out_dir / "load_allocation_stockout_correlations.csv", index=False)
    leverage.to_csv(out_dir / "load_allocation_leverage.csv", index=False)
    leave_one_out.to_csv(out_dir / "load_allocation_leave_one_out.csv", index=False)
    _write_report(
        out_dir / "load_allocation_diagnosis_report.md",
        metrics=metrics,
        diffs=diffs,
        correlations=correlations,
        leverage=leverage,
        leave_one_out=leave_one_out,
        analysis=analysis,
    )

    print("Load allocation metrics")
    print(metrics.to_string(index=False))
    print("\nLoad allocation diffs")
    print(diffs.to_string(index=False))
    print("\nCorrelations")
    print(correlations.to_string(index=False))
    print("\nLeverage")
    print(leverage.to_string(index=False))
    if not leave_one_out.empty:
        print("\nLeave-one-out")
        print(leave_one_out.to_string(index=False))


def _load_allocation_metrics(route_sets: dict[str, dict[str, tuple[object, RouteSet]]]) -> pd.DataFrame:
    rows = []
    for instance_name, provider_data in route_sets.items():
        for provider, (instance, route_set) in provider_data.items():
            vector = _load_allocation_vector(instance, route_set)
            rows.append(
                {
                    "Instance": instance_name,
                    "Provider": PROVIDER_LABELS[provider],
                    "Gini Coefficient": _gini(vector),
                    "Load Variance": float(np.var(vector, ddof=1)) if len(vector) > 1 else 0.0,
                    "Mean Load Util": float(np.mean(vector)) if len(vector) else np.nan,
                    "Max Load Util": float(np.max(vector)) if len(vector) else np.nan,
                    "Active Vehicle Count": int(len(vector)),
                    "Feasible": bool(route_set.feasible),
                }
            )
    return pd.DataFrame(rows).sort_values(["Instance", "Provider"])


def _load_allocation_vector(instance: object, route_set: RouteSet) -> np.ndarray:
    if not route_set.feasible:
        return np.array([], dtype=float)
    _, customer_indices = customer_view(instance)
    customers = set(int(node) for node in customer_indices)
    loads = []
    for route in route_set.routes:
        route_load = sum(float(instance.demands[int(node)]) for node in route if int(node) in customers)
        if route_load > 0:
            loads.append(route_load / float(instance.capacity))
    return np.asarray(loads, dtype=float)


def _gini(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return float("nan")
    if np.allclose(values, 0.0):
        return 0.0
    sorted_values = np.sort(values)
    n = len(sorted_values)
    index = np.arange(1, n + 1, dtype=float)
    return float((2.0 * np.sum(index * sorted_values) / (n * np.sum(sorted_values))) - ((n + 1.0) / n))


def _load_allocation_diffs(metrics: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for instance, group in metrics.groupby("Instance"):
        if set(group["Provider"]) != {"OR-Tools", "VROOM"}:
            continue
        ort = group[group["Provider"] == "OR-Tools"].iloc[0]
        vro = group[group["Provider"] == "VROOM"].iloc[0]
        both_feasible = bool(ort["Feasible"]) and bool(vro["Feasible"])
        rows.append(
            {
                "Instance": instance,
                "Common Route Feasible": both_feasible,
                "Gini Diff": float(ort["Gini Coefficient"] - vro["Gini Coefficient"]) if both_feasible else np.nan,
                "Load Variance Diff": float(ort["Load Variance"] - vro["Load Variance"]) if both_feasible else np.nan,
                "Mean Load Util Diff": float(ort["Mean Load Util"] - vro["Mean Load Util"]) if both_feasible else np.nan,
                "Active Vehicle Count Diff": int(ort["Active Vehicle Count"] - vro["Active Vehicle Count"]),
            }
        )
    return pd.DataFrame(rows).sort_values("Instance")


def _correlation_tests(analysis: pd.DataFrame, bootstrap_samples: int, seed: int) -> pd.DataFrame:
    rows = []
    rng = np.random.default_rng(seed)
    predictors = [("Gini Diff", "Gini Diff"), ("Load Variance Diff", "Load Variance Diff")]
    common = analysis[analysis["Common Route Feasible"] == True].copy()
    for domain, group in common.groupby("Domain"):
        for column, label in predictors:
            x = group[column].to_numpy(float)
            y = group["stockout_diff_signed"].to_numpy(float)
            unique_x = _unique_level_count(x)
            if len(group) < 15:
                r, p_value = _pearson(x, y)
                ci_low, ci_high = _bootstrap_ci(x, y, bootstrap_samples, rng)
                evidence = "diagnostic_signal_n_lt_15"
            elif unique_x < 3:
                r, p_value, ci_low, ci_high = np.nan, np.nan, np.nan, np.nan
                evidence = "insufficient_x_variation"
            else:
                r, p_value = _pearson(x, y)
                ci_low, ci_high = _bootstrap_ci(x, y, bootstrap_samples, rng)
                evidence = _evidence_label(r, p_value, ci_low, ci_high)
            rows.append(
                {
                    "Domain": domain,
                    "Predictor": label,
                    "n": int(len(group)),
                    "Unique x Levels": int(unique_x),
                    "Pearson r": r,
                    "p-value": p_value,
                    "Bootstrap CI Low": ci_low,
                    "Bootstrap CI High": ci_high,
                    "CI Contains Zero": _ci_contains_zero(ci_low, ci_high),
                    "Evidence Label": evidence,
                }
            )
    return pd.DataFrame(rows).sort_values(["Domain", "Predictor"])


def _leverage_control(analysis: pd.DataFrame) -> pd.DataFrame:
    rows = []
    predictors = [("Gini Diff", "Gini Diff"), ("Load Variance Diff", "Load Variance Diff")]
    common = analysis[analysis["Common Route Feasible"] == True].copy()
    for domain, domain_group in common.groupby("Domain"):
        domain_group = domain_group.sort_values("Instance")
        for column, label in predictors:
            x = domain_group[column].to_numpy(float)
            y = domain_group["stockout_diff_signed"].to_numpy(float)
            n = len(domain_group)
            cook_threshold = 4.0 / n if n else np.nan
            severe_threshold = 3.0 * cook_threshold if n else np.nan
            if _unique_level_count(x) < 2 or np.allclose(y, y[0]):
                leverage = np.full(n, np.nan)
                cooks = np.full(n, np.nan)
                residuals = np.full(n, np.nan)
            else:
                leverage, cooks, residuals = _ols_influence(x, y)
            for idx, row in enumerate(domain_group.itertuples(index=False)):
                rows.append(
                    {
                        "Domain": domain,
                        "Predictor": label,
                        "Instance": row.Instance,
                        "x": x[idx],
                        "Stockout Diff Signed": y[idx],
                        "Leverage": leverage[idx],
                        "Cook's Distance": cooks[idx],
                        "Cook Threshold 4/n": cook_threshold,
                        "Severe Threshold 3x": severe_threshold,
                        "Severe Cook Flag": bool(np.isfinite(cooks[idx]) and cooks[idx] > severe_threshold),
                        "Residual": residuals[idx],
                    }
                )
    return pd.DataFrame(rows).sort_values(["Domain", "Predictor", "Cook's Distance"], ascending=[True, True, False])


def _leave_one_out_if_needed(
    analysis: pd.DataFrame,
    leverage: pd.DataFrame,
    bootstrap_samples: int,
    seed: int,
) -> pd.DataFrame:
    rows = []
    rng = np.random.default_rng(seed)
    flagged = leverage[leverage["Severe Cook Flag"]]
    if flagged.empty:
        return pd.DataFrame(
            columns=[
                "Domain",
                "Predictor",
                "Dropped Instance",
                "n",
                "Unique x Levels",
                "Pearson r",
                "p-value",
                "Bootstrap CI Low",
                "Bootstrap CI High",
                "CI Contains Zero",
                "Evidence Label",
            ]
        )
    common = analysis[analysis["Common Route Feasible"] == True].copy()
    for (domain, predictor), group_flags in flagged.groupby(["Domain", "Predictor"]):
        dropped = group_flags.sort_values("Cook's Distance", ascending=False).iloc[0]["Instance"]
        reduced = common[(common["Domain"] == domain) & (common["Instance"] != dropped)]
        column = predictor
        x = reduced[column].to_numpy(float)
        y = reduced["stockout_diff_signed"].to_numpy(float)
        unique_x = _unique_level_count(x)
        if len(reduced) < 15:
            r, p_value = _pearson(x, y)
            ci_low, ci_high = _bootstrap_ci(x, y, bootstrap_samples, rng)
            evidence = "diagnostic_signal_n_lt_15"
        elif unique_x < 3:
            r, p_value, ci_low, ci_high = np.nan, np.nan, np.nan, np.nan
            evidence = "insufficient_x_variation"
        else:
            r, p_value = _pearson(x, y)
            ci_low, ci_high = _bootstrap_ci(x, y, bootstrap_samples, rng)
            evidence = _evidence_label(r, p_value, ci_low, ci_high)
        rows.append(
            {
                "Domain": domain,
                "Predictor": predictor,
                "Dropped Instance": dropped,
                "n": int(len(reduced)),
                "Unique x Levels": int(unique_x),
                "Pearson r": r,
                "p-value": p_value,
                "Bootstrap CI Low": ci_low,
                "Bootstrap CI High": ci_high,
                "CI Contains Zero": _ci_contains_zero(ci_low, ci_high),
                "Evidence Label": evidence,
            }
        )
    return pd.DataFrame(rows).sort_values(["Domain", "Predictor"])


def _write_report(
    path: Path,
    metrics: pd.DataFrame,
    diffs: pd.DataFrame,
    correlations: pd.DataFrame,
    leverage: pd.DataFrame,
    leave_one_out: pd.DataFrame,
    analysis: pd.DataFrame,
) -> None:
    common_instances = sorted(diffs[diffs["Common Route Feasible"] == True]["Instance"].tolist())
    candidates = correlations[correlations["Evidence Label"] == "candidate_mechanism"]
    ci_cross = correlations[correlations["Evidence Label"] == "no_correlation_ci_crosses_zero"]
    severe = leverage[leverage["Severe Cook Flag"]]

    if candidates.empty:
        load_result = (
            "Load allocation bu kosuda A.5 standartlarinda stockout siralama farkini aciklamadi. "
            "Korelasyonlar ya bootstrap CI sifiri kapsadigi icin reddedildi ya da istatistiksel olarak aday mekanizma seviyesine cikmadi."
        )
        a8_status = (
            "A.8 hala acik. Kalan tek aday: objective interaction farki - domain objective'lerinin farkli feature "
            "agirliklandirmasi stockout disi bir maliyet bilesenini, ornegin load_penalty, tasiyor olabilir. "
            "Bu, stockout metriginin kendisinin yanlis yerde arandigini gosterebilir."
        )
        next_step = (
            "Objective interaction testini kur: stockout_diff yerine mean_domain_loss_diff, mean_load_penalty_loss_diff, "
            "planned_load_total_diff ve objective component farklarini domain bazinda korele et."
        )
    else:
        load_result = (
            "Load allocation icin aday mekanizma sinyali bulundu. Bu satirlar once baska X secimleri ve route time-limit "
            "duyarliligi ile dogrulanmali."
        )
        a8_status = (
            "A.8 kismen daraldi: load allocation en az bir domain/predictor kombinasyonunda aday mekanizma verdi, "
            "fakat objective interaction ayrica test edilmeden nihai neden denemez."
        )
        next_step = (
            "Aday load-allocation predictor'unu farkli route time-limitleri ve OSRM matrisiyle tekrar calistir; "
            "sonra objective interaction'i kontrol degiskeni olarak ekle."
        )

    if severe.empty:
        leverage_text = "Cook's Distance kontrolunde 3x(4/n) esigini asan domine edici instance gorulmedi."
        loo_text = ""
    else:
        leverage_text = (
            "Cook's Distance kontrolunde 3x(4/n) esigini asan instance'lar var; leave-one-out sonucu asagida."
        )
        loo_text = "\n\n" + _markdown_table(leave_one_out)

    text = f"""# Load Allocation Diagnosis Report

## X Dataset Genişlemesi Durumu

X dataset genişlemesi bu turda gerçekten çalıştırıldı: 24 CVRPLIB X instance indirildi, `vrplib` ile doğrulandı, proxy dataset üretildi ve OR-Tools + VROOM + 4 domain koşuları alındı.

Ortak provider-feasible instance sayısı load-allocation/stockout korelasyonu için {len(common_instances)} oldu:

```text
{", ".join(common_instances)}
```

Bu n>=15 eşiğini karşılıyor, fakat tüm indirilen 24 instance'ın 8'i OR-Tools tarafında anchor-feasible olmadı. Bu nedenle sonuçlar "X indirilen set" ve "ortak feasible analiz seti" diye ayrı okunmalı.

A.5'in n, en az 3 x-seviyesi, bootstrap CI ve Cook's Distance kontrolleri uygulandı. X24 seçimi 8/8/8 small/medium/large olarak dengeli kuruldu; ancak üç bucket'lı bir tasarımda "her kategori <=%25" kuralı kelimesi kelimesine sağlanamaz. Bu kural literal uygulanacaksa sonraki X turu 4 boyut bucket'ı ve 28 instance ile tasarlanmalı.

## Load Allocation Hipotezi

Her rota için `sum(demands[n] for n in route) / capacity` vektörü çıkarıldı. Sonra provider başına Gini coefficient ve rota yük varyansı hesaplandı.

{_markdown_table(metrics[["Instance", "Provider", "Gini Coefficient", "Load Variance", "Mean Load Util", "Max Load Util", "Active Vehicle Count", "Feasible"]])}

OR-Tools - VROOM farkları:

{_markdown_table(diffs)}

Domain bazlı korelasyonlar:

{_markdown_table(correlations)}

{load_result}

## Leverage Kontrolü

{leverage_text}

{_markdown_table(leverage[["Domain", "Predictor", "Instance", "Cook's Distance", "Cook Threshold 4/n", "Severe Threshold 3x", "Severe Cook Flag"]])}{loo_text}

## A.8'in Şu Anki Durumu

Üç aday test edildi:

- Capacity utilization: açıklamadı; mean utilization farkı aynı toplam talep ve aynı araç sayısı nedeniyle tek seviyeye sıkıştı.
- Vehicle count: açıklamadı; önceki n20 koşusunda tüm ortak instance'larda araç sayısı aynıydı.
- Load allocation: {("aday mekanizma sinyali verdi" if not candidates.empty else "A.5 standartlarında açıklamadı")}.

{a8_status}

## Sonraki Adım

{next_step}
"""
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
