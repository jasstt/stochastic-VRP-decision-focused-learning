from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from .analyze_route_grouping_sensitivity import _markdown_table, _pearson, _stockout_diffs


ORIGINAL_N4 = ["A-n32-k5", "B-n31-k5", "E-n13-k4", "P-n19-k2"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnose the false positive grouping-exposure n=4 signal.")
    parser.add_argument("--n4-exposure-source", default="exposure_rank_source_diff.csv")
    parser.add_argument(
        "--n4-ortools-results",
        default="benchmarks/proxy_cvrplib/domain_engine_results_ortools_provider.csv",
    )
    parser.add_argument(
        "--n4-vroom-results",
        default="benchmarks/proxy_cvrplib/domain_engine_results_vroom_provider.csv",
    )
    parser.add_argument("--n20-exposure-source", default="benchmarks/proxy_cvrplib_n20/exposure_rank_source_diff.csv")
    parser.add_argument(
        "--n20-ortools-results",
        default="benchmarks/proxy_cvrplib_n20/domain_engine_results_ortools_provider.csv",
    )
    parser.add_argument(
        "--n20-vroom-results",
        default="benchmarks/proxy_cvrplib_n20/domain_engine_results_vroom_provider.csv",
    )
    parser.add_argument("--n20-manifest", default="benchmarks/proxy_cvrplib_n20/manifest.csv")
    parser.add_argument("--out-dir", default=".")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    n4 = _analysis_frame(args.n4_exposure_source, args.n4_ortools_results, args.n4_vroom_results)
    n20 = _analysis_frame(args.n20_exposure_source, args.n20_ortools_results, args.n20_vroom_results)
    n20 = n20.merge(
        pd.read_csv(args.n20_manifest)[["name", "nodes", "customers"]],
        left_on="Instance",
        right_on="name",
        how="left",
    ).drop(columns=["name"])
    n20["Size Stratum"] = n20["nodes"].map(_size_stratum)

    leverage = _n4_leverage(n4)
    leave_one_out = _leave_one_out(n4)
    stratum = _stratum_correlations(n20)
    comparison = _set_comparison(n4, n20)

    leverage.to_csv(out_dir / "false_positive_n4_leverage.csv", index=False)
    leave_one_out.to_csv(out_dir / "false_positive_leave_one_out.csv", index=False)
    stratum.to_csv(out_dir / "false_positive_size_strata.csv", index=False)
    comparison.to_csv(out_dir / "false_positive_set_comparison.csv", index=False)
    _write_report(out_dir / "false_positive_mechanism_report.md", leverage, leave_one_out, stratum, comparison)

    print("n4 leverage")
    print(leverage.to_string(index=False))
    print("\nleave-one-out")
    print(leave_one_out.to_string(index=False))
    print("\nsize strata")
    print(stratum.to_string(index=False))
    print("\nset comparison")
    print(comparison.to_string(index=False))


def _analysis_frame(exposure_path: str, ortools_results: str, vroom_results: str) -> pd.DataFrame:
    exposure = pd.read_csv(exposure_path)
    stockout = _stockout_diffs(ortools_results, vroom_results)
    data = stockout.merge(exposure, on=["Instance", "Domain"], how="inner")
    data["grouping_exposure_diff"] = data["Exposure Rank Diff From Grouping"].fillna(0.0)
    data["stockout_diff_signed"] = data["stockout_diff_signed"].astype(float)
    data["stockout_diff_abs"] = data["stockout_diff_signed"].abs()
    return data


def _n4_leverage(n4: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for domain, group in n4.groupby("Domain"):
        group = group.sort_values("Instance")
        x = group["grouping_exposure_diff"].to_numpy(float)
        y = group["stockout_diff_signed"].to_numpy(float)
        leverage, cooks_distance, residuals = _ols_influence(x, y)
        r, p_value = _pearson(x, y)
        for idx, row in enumerate(group.itertuples(index=False)):
            rows.append(
                {
                    "Domain": domain,
                    "Instance": row.Instance,
                    "Grouping Exposure Diff": x[idx],
                    "Stockout Diff Signed": y[idx],
                    "Pearson r full n4": r,
                    "Pearson p full n4": p_value,
                    "Leverage": leverage[idx],
                    "Cook's Distance": cooks_distance[idx],
                    "Residual": residuals[idx],
                    "High Cook Flag": cooks_distance[idx] > 1.0,
                }
            )
    return pd.DataFrame(rows).sort_values(["Domain", "Cook's Distance"], ascending=[True, False])


def _ols_influence(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    design = np.column_stack([np.ones(len(x)), x])
    beta = np.linalg.lstsq(design, y, rcond=None)[0]
    fitted = design @ beta
    residuals = y - fitted
    hat = design @ np.linalg.inv(design.T @ design) @ design.T
    leverage = np.diag(hat)
    p = design.shape[1]
    dof = len(x) - p
    mse = float(residuals @ residuals / dof) if dof > 0 else np.nan
    if not np.isfinite(mse) or np.isclose(mse, 0.0):
        cooks_distance = np.full(len(x), np.nan)
    else:
        cooks_distance = (residuals**2 / (p * mse)) * leverage / ((1.0 - leverage) ** 2)
    return leverage, cooks_distance, residuals


def _leave_one_out(n4: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for domain, group in n4.groupby("Domain"):
        full_x = group["grouping_exposure_diff"].to_numpy(float)
        full_y = group["stockout_diff_signed"].to_numpy(float)
        full_r, full_p = _pearson(full_x, full_y)
        for instance in ORIGINAL_N4:
            reduced = group[group["Instance"] != instance]
            x = reduced["grouping_exposure_diff"].to_numpy(float)
            y = reduced["stockout_diff_signed"].to_numpy(float)
            r, p_value = _pearson(x, y)
            unique_x = len(np.unique(np.round(x, 12)))
            rows.append(
                {
                    "Domain": domain,
                    "Dropped Instance": instance,
                    "n remaining": len(reduced),
                    "unique x remaining": unique_x,
                    "Pearson r after drop": r,
                    "Pearson p after drop": p_value,
                    "Full n4 r": full_r,
                    "Full n4 p": full_p,
                    "Degenerate Design": unique_x < 3,
                    "Note": (
                        "only one non-zero grouping level remains"
                        if unique_x < 3
                        else "n=3, unstable but not single-level"
                    ),
                }
            )
    return pd.DataFrame(rows).sort_values(["Domain", "Dropped Instance"])


def _stratum_correlations(n20: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for domain, domain_group in n20.groupby("Domain"):
        for stratum, group in domain_group.groupby("Size Stratum"):
            x = group["grouping_exposure_diff"].to_numpy(float)
            y = group["stockout_diff_signed"].to_numpy(float)
            r, p_value = _pearson(x, y)
            rows.append(
                {
                    "Domain": domain,
                    "Size Stratum": stratum,
                    "n": len(group),
                    "Instance Count": group["Instance"].nunique(),
                    "Pearson r": r,
                    "p-value": p_value,
                    "Mean Grouping Exposure Diff": float(np.mean(x)),
                    "Mean Signed Stockout Diff": float(np.mean(y)),
                    "Unique x count": len(np.unique(np.round(x, 12))),
                    "Interpretable": len(group) >= 3 and len(np.unique(np.round(x, 12))) >= 2,
                }
            )
    order = {"small_n_lt_20": 0, "medium_20_50": 1, "large_51_99": 2}
    out = pd.DataFrame(rows)
    out["_order"] = out["Size Stratum"].map(order)
    return out.sort_values(["Domain", "_order"]).drop(columns=["_order"])


def _set_comparison(n4: pd.DataFrame, n20: pd.DataFrame) -> pd.DataFrame:
    n4_instances = set(ORIGINAL_N4)
    frames = [
        ("original_n4", n4),
        ("n20_overlap_with_original", n20[n20["Instance"].isin(n4_instances)]),
        ("n20_remainder", n20[~n20["Instance"].isin(n4_instances)]),
    ]
    rows = []
    for label, frame in frames:
        for domain, group in frame.groupby("Domain"):
            x = group["grouping_exposure_diff"].to_numpy(float)
            y = group["stockout_diff_signed"].to_numpy(float)
            r, p_value = _pearson(x, y)
            rows.append(
                {
                    "Set": label,
                    "Domain": domain,
                    "Rows": len(group),
                    "Instances": group["Instance"].nunique(),
                    "Pearson r": r,
                    "p-value": p_value,
                    "Mean x": float(np.mean(x)) if len(x) else np.nan,
                    "Mean y": float(np.mean(y)) if len(y) else np.nan,
                    "Max x": float(np.max(x)) if len(x) else np.nan,
                    "Max y": float(np.max(y)) if len(y) else np.nan,
                }
            )
    return pd.DataFrame(rows).sort_values(["Domain", "Set"])


def _size_stratum(nodes: int) -> str:
    if nodes < 20:
        return "small_n_lt_20"
    if nodes <= 50:
        return "medium_20_50"
    return "large_51_99"


def _write_report(
    path: Path,
    leverage: pd.DataFrame,
    leave_one_out: pd.DataFrame,
    stratum: pd.DataFrame,
    comparison: pd.DataFrame,
) -> None:
    influence_summary = (
        leverage.groupby("Instance")
        .agg(
            mean_leverage=("Leverage", "mean"),
            max_cooks_distance=("Cook's Distance", "max"),
            mean_cooks_distance=("Cook's Distance", "mean"),
            high_cook_domains=("High Cook Flag", "sum"),
            mean_grouping_exposure=("Grouping Exposure Diff", "mean"),
            mean_stockout_diff=("Stockout Diff Signed", "mean"),
        )
        .reset_index()
        .sort_values("max_cooks_distance", ascending=False)
    )
    top = influence_summary.iloc[0]
    degenerate_after_e = leave_one_out[leave_one_out["Dropped Instance"] == "E-n13-k4"]
    stratum_short = stratum[
        [
            "Domain",
            "Size Stratum",
            "Instance Count",
            "Pearson r",
            "p-value",
            "Mean Grouping Exposure Diff",
            "Mean Signed Stockout Diff",
            "Interpretable",
        ]
    ]
    comparison_short = comparison[
        [
            "Set",
            "Domain",
            "Instances",
            "Pearson r",
            "p-value",
            "Mean x",
            "Mean y",
            "Max x",
            "Max y",
        ]
    ]
    text = f"""# False Positive Mechanism Report

## Bulgu

n=4 koşusundaki güçlü korelasyonu en çok sürükleyen instance `{top["Instance"]}`. Bu instance'ın ortalama leverage skoru {top["mean_leverage"]:.4f}, maksimum Cook's Distance değeri {top["max_cooks_distance"]:.4f}. Cook's Distance için pratik eşik `4/n = 1.0`; `{top["Instance"]}` dört domain'in {int(top["high_cook_domains"])}/4'ünde bu eşiğin çok üstünde.

Mekanizma şu: n=4 verisinde iki instance (`A-n32-k5`, `P-n19-k2`) grouping exposure değerinde 0 noktasına oturuyor, `B-n31-k5` küçük bir x değeri veriyor, `E-n13-k4` ise tek yüksek-x nokta olarak aynı anda yüksek pozitif stockout farkı üretiyor. Bu yapı, özellikle n=4 gibi küçük örneklemde regresyon çizgisini tek bir yüksek-x/high-y noktasına bağlayıp sahte güçlü korelasyon yaratıyor.

### n=4 Influence Özeti

{_markdown_table(influence_summary)}

### Leave-One-Out

`E-n13-k4` çıkarıldığında korelasyon sayısını mekanik olarak okumak doğru değil; kalan tasarımda sadece iki x seviyesi kalıyor ve yüksek-x bölgesi tamamen kayboluyor. Bu yüzden bazı domainlerde r değeri `-1` veya `1` gibi görünse bile bu istatistiksel kanıt değil, üç noktalı dejenere geometri.

{_markdown_table(degenerate_after_e)}

## Instance Büyüklüğü Testi

n=20 setinde stratum sonuçları küçük instance hipotezini tek başına doğrulamıyor. Katı `n<20` küçük stratumunda yalnızca 2 instance var ve grouping exposure x değeri değişmediği için korelasyon hesaplanamıyor. Orta ve büyük stratumlar ise ters yönlü davranıyor: orta stratum çoğunlukla negatif, büyük stratum çoğunlukla pozitif ama p-value'lar genel olarak güçlü değil.

{_markdown_table(stratum_short)}

## n=4 ile n20 Geri Kalanı Karşılaştırması

n=20 geri kalanında max grouping exposure yüksek kalmasına rağmen signed stockout farkı aynı yönde büyümüyor. Bu, n=4 sinyalinin genel bir exposure mekanizması değil, orijinal küçük setteki nokta yerleşiminden kaynaklanan bir regresyon yanılsaması olduğunu destekliyor.

{_markdown_table(comparison_short)}

## Metodolojik Ders

n=4 gibi çok küçük örneklemlerde tek bir instance istatistiksel sonucu domine edebilir. Bu sadece bu VRP benchmarkı için değil, projenin diğer iddiaları için de geçerli: quantum/klasik kıyas, stochastic loading, OSRM etkisi veya domain adapter etkisi fark etmez; örneklem küçükse bir problem ailesi, bir kapasite baskısı seviyesi veya tek bir uç instance tüm sonucu taşıyabilir. Bu yüzden küçük örneklem sonuçları "kanıt" değil, en fazla hipotez üretici tanı sinyali olarak yazılmalı.

## Doğru Cümle

n=4 koşusundaki güçlü `grouping exposure -> stockout` korelasyonu, esas olarak `E-n13-k4` instance'ının yüksek leverage/Cook's Distance etkisi ve kalan üç noktanın zayıf x çeşitliliği tarafından üretilmiş bir küçük örneklem yanılsamasıdır.

## Sonraki Adım

Instance seçimi yaparken minimum örneklem büyüklüğü kuralı uygulanmalı: tek bir kategoriden, örneğin çok küçük/çok büyük instance'lardan gelen örnek sayısı toplam örneklemin %25'ini geçmemeli. Ayrıca her stratumda en az 5 instance ve en az 3 farklı grouping exposure seviyesi yoksa domain bazlı Pearson korelasyonu iddia olarak sunulmamalı.
"""
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
