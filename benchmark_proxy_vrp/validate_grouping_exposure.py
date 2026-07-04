from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from .analyze_route_grouping_sensitivity import _markdown_table, _pearson, _stockout_diffs


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate grouping-exposure vs stockout correlation on n20.")
    parser.add_argument("--n4-correlations", default="exposure_source_stockout_correlations.csv")
    parser.add_argument("--n20-exposure-source", default="benchmarks/proxy_cvrplib_n20/exposure_rank_source_diff.csv")
    parser.add_argument(
        "--n20-ortools-results",
        default="benchmarks/proxy_cvrplib_n20/domain_engine_results_ortools_provider.csv",
    )
    parser.add_argument(
        "--n20-vroom-results",
        default="benchmarks/proxy_cvrplib_n20/domain_engine_results_vroom_provider.csv",
    )
    parser.add_argument("--out-dir", default="benchmarks/proxy_cvrplib_n20")
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    n4 = pd.read_csv(args.n4_correlations)
    n20_data = _merged_n20_data(args.n20_exposure_source, args.n20_ortools_results, args.n20_vroom_results)
    n20_correlations = _n20_correlations(n20_data)
    comparison = _comparison(n4, n20_correlations)
    bootstrap = _bootstrap_ci(n20_data, args.bootstrap_samples, args.seed)

    comparison.to_csv(out_dir / "n4_n20_grouping_exposure_comparison.csv", index=False)
    bootstrap.to_csv(out_dir / "grouping_exposure_bootstrap_ci.csv", index=False)
    _write_report(
        out_dir / "grouping_exposure_validation_n20_report.md",
        comparison,
        bootstrap,
        args.bootstrap_samples,
    )
    print("n=4 -> n=20 comparison")
    print(comparison.to_string(index=False))
    print("\nBootstrap")
    print(bootstrap.to_string(index=False))


def _merged_n20_data(
    exposure_source_path: str,
    ortools_results_path: str,
    vroom_results_path: str,
) -> pd.DataFrame:
    exposure_source = pd.read_csv(exposure_source_path)
    stockout = _stockout_diffs(ortools_results_path, vroom_results_path)
    data = stockout.merge(exposure_source, on=["Instance", "Domain"], how="inner")
    data["grouping_exposure_diff"] = data["Exposure Rank Diff From Grouping"].fillna(0.0)
    data["ordering_exposure_diff"] = data["Exposure Rank Diff From Ordering"].fillna(0.0)
    return data


def _n20_correlations(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for domain, group in data.groupby("Domain"):
        x = group["grouping_exposure_diff"].to_numpy(float)
        y = group["stockout_diff_signed"].to_numpy(float)
        r, p_value = _pearson(x, y)
        rows.append(
            {
                "Domain": domain,
                "n": len(group),
                "n20 r": r,
                "n20 p": p_value,
                "n20 mean grouping exposure diff": float(x.mean()),
                "n20 mean signed stockout diff": float(y.mean()),
            }
        )
    return pd.DataFrame(rows).sort_values("Domain")


def _comparison(n4: pd.DataFrame, n20: pd.DataFrame) -> pd.DataFrame:
    n4_small = n4[
        [
            "Domain",
            "Grouping Exposure r",
            "Grouping Exposure p-value",
        ]
    ].rename(
        columns={
            "Grouping Exposure r": "n4 r",
            "Grouping Exposure p-value": "n4 p",
        }
    )
    comparison = n4_small.merge(n20, on="Domain", how="inner")
    comparison["Direction preserved?"] = comparison.apply(
        lambda row: _direction_preserved(row["n4 r"], row["n20 r"]),
        axis=1,
    )
    return comparison[
        [
            "Domain",
            "n4 r",
            "n4 p",
            "n",
            "n20 r",
            "n20 p",
            "Direction preserved?",
            "n20 mean grouping exposure diff",
            "n20 mean signed stockout diff",
        ]
    ].rename(columns={"n": "n20 n"})


def _direction_preserved(left: float, right: float) -> str:
    if pd.isna(left) or pd.isna(right):
        return "unknown"
    if np.sign(left) == np.sign(right):
        return "yes"
    return "no"


def _bootstrap_ci(data: pd.DataFrame, samples: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for domain, group in data.groupby("Domain"):
        x = group["grouping_exposure_diff"].to_numpy(float)
        y = group["stockout_diff_signed"].to_numpy(float)
        observed_r, observed_p = _pearson(x, y)
        boot = []
        n = len(group)
        for _ in range(samples):
            indices = rng.integers(0, n, n)
            r, _ = _pearson(x[indices], y[indices])
            if not np.isnan(r):
                boot.append(r)
        if boot:
            ci_low, ci_high = np.percentile(boot, [2.5, 97.5])
            valid_samples = len(boot)
        else:
            ci_low = ci_high = np.nan
            valid_samples = 0
        contains_zero = bool(ci_low <= 0.0 <= ci_high) if not np.isnan(ci_low) else True
        rows.append(
            {
                "Domain": domain,
                "n": n,
                "Observed r": observed_r,
                "Observed p-value": observed_p,
                "Bootstrap CI low": float(ci_low),
                "Bootstrap CI high": float(ci_high),
                "Valid bootstrap samples": valid_samples,
                "CI contains zero": contains_zero,
                "Interpretation": (
                    "correlation not distinguishable from zero"
                    if contains_zero
                    else "correlation differs from zero at 95% bootstrap CI"
                ),
            }
        )
    return pd.DataFrame(rows).sort_values("Domain")


def _write_report(
    path: Path,
    comparison: pd.DataFrame,
    bootstrap: pd.DataFrame,
    bootstrap_samples: int,
) -> None:
    significant = bootstrap[bootstrap["CI contains zero"] == False]["Domain"].tolist()
    if significant:
        correct_sentence = (
            "Grouping-kaynaklı exposure rank farkı ile stockout arasındaki ilişki "
            f"{', '.join(significant)} domainlerinde n=20 koşusunda da yön sinyali verdi; "
            "bu domainlerde bootstrap %95 güven aralığı sıfırı içermedi."
        )
        next_step = (
            "Sinyal belirli domainlerde korunduğu için, bu domainlerde instance sayısını daha da büyütüp "
            "route grouping exposure etkisini maliyet bileşenlerine ayırmak gerekir. Cold-chain için "
            "stockout yanında `mean_load_penalty_loss` korelasyonu özellikle raporlanmalı."
        )
    else:
        correct_sentence = (
            "Grouping-kaynaklı exposure rank farkı ile stockout arasındaki ilişki n=20 koşusunda "
            "kesin istatistiksel destek kazanmadı; bootstrap %95 güven aralıkları sıfırı içeriyor."
        )
        next_step = (
            "Öncelik artık bu iddiayı büyütmek değil, n=4 koşusundaki güçlü p-value'ların neden "
            "şiştiğini açıklamak olmalı. Bunun için instance ailesi, kapasite baskısı ve signed/absolute "
            "stockout farkı ayrı ayrı stratify edilmeli. Cold-chain için stockout yanında "
            "`mean_load_penalty_loss` korelasyonu ayrıca test edilmeli."
        )

    n20_preserved = int((comparison["Direction preserved?"] == "yes").sum())
    text = f"""# Grouping Exposure Validation n20 Report

## n=4 -> n=20 Karşılaştırması

Bu rapor, `exposure_rank_diff_from_grouping -> stockout_diff` ilişkisini 20 coordinate-capable CVRPLIB instance üzerinde yeniden test eder. `stockout_diff`, OR-Tools stockout minus VROOM stockout olarak hesaplandı. n=4 sonuçları geçmiş küçük koşudan, n=20 sonuçları yeni validation setinden alınmıştır.

{_markdown_table(comparison)}

Yön koruması: {n20_preserved}/4 domain.

## Bootstrap Güven Aralıkları

Her domain için Pearson r, {bootstrap_samples} bootstrap resample ile %95 güven aralığına alındı.

{_markdown_table(bootstrap)}

## Doğru Cümle

{correct_sentence}

## Henüz Doğru Olmayan Cümle

Bu bulgu farklı VRP problem ailelerine genellenir. Bu hâlâ doğru değil; VRPTW, multi-depot, pickup-delivery ve gerçek yol zamanı belirsizliği ayrı test edilmedi.

## Sonraki Adım

{next_step}
"""
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
