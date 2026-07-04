from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

from .cvrplib import customer_view, load_instance_json
from .domain_adapters import available_adapters, get_adapter
from .ortools_baselines import build_plans, vehicle_count_from_name
from .routing_providers import OrToolsProvider, VroomProvider, instance_to_provider_inputs
from .routing_providers.base import RouteSet


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze route grouping sensitivity across routing providers.")
    parser.add_argument("--data-dir", default="benchmarks/proxy_cvrplib")
    parser.add_argument("--ortools-results", default="benchmarks/proxy_cvrplib/domain_engine_results_ortools_provider.csv")
    parser.add_argument("--vroom-results", default="benchmarks/proxy_cvrplib/domain_engine_results_vroom_provider.csv")
    parser.add_argument("--out-dir", default=".")
    parser.add_argument("--anchor-plan", default="proxy_mean_or_tools")
    parser.add_argument("--fallback-anchor-plan", default="nominal_or_tools")
    parser.add_argument("--time-limit-sec", type=int, default=5)
    parser.add_argument("--vroom-url", default="http://localhost:3000")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    route_sets = _solve_route_sets(
        data_dir=data_dir,
        anchor_plan=args.anchor_plan,
        fallback_anchor_plan=args.fallback_anchor_plan,
        time_limit_sec=args.time_limit_sec,
        vroom_url=args.vroom_url,
    )
    divergence = _route_grouping_divergence(route_sets)
    exposure_diff = _exposure_rank_diff(route_sets, data_dir)
    stockout = _stockout_diffs(args.ortools_results, args.vroom_results)
    correlations = _correlations(divergence, stockout)
    sensitivity = _domain_sensitivity(divergence, stockout)

    divergence[["Instance", "Divergence Score"]].to_csv(out_dir / "route_grouping_divergence.csv", index=False)
    exposure_diff.to_csv(out_dir / "exposure_rank_diff.csv", index=False)
    correlations.to_csv(out_dir / "route_grouping_stockout_correlations.csv", index=False)
    sensitivity.to_csv(out_dir / "domain_stockout_sensitivity.csv", index=False)
    _write_report(out_dir / "route_grouping_sensitivity_report.md", divergence, exposure_diff, correlations, sensitivity)

    print("Route grouping divergence")
    print(divergence.to_string(index=False))
    print("\nExposure rank diff")
    print(exposure_diff.to_string(index=False))
    print("\nCorrelations")
    print(correlations.to_string(index=False))
    print("\nDomain sensitivity")
    print(sensitivity.to_string(index=False))


def _solve_route_sets(
    data_dir: Path,
    anchor_plan: str,
    fallback_anchor_plan: str,
    time_limit_sec: int,
    vroom_url: str,
) -> dict[str, dict[str, tuple[object, RouteSet]]]:
    out: dict[str, dict[str, tuple[object, RouteSet]]] = {}
    for instance_json in sorted(data_dir.glob("*/instance.json")):
        instance = load_instance_json(instance_json)
        nominal, _ = customer_view(instance)
        history = pd.read_csv(instance_json.parent / "proxy_demand_history.csv").drop(columns=["date"]).to_numpy()
        plans = build_plans(history, nominal)
        out[instance.name] = {
            "ortools": (instance, _solve_anchor(instance, plans, anchor_plan, fallback_anchor_plan, "ortools", time_limit_sec, vroom_url)),
            "vroom": (instance, _solve_anchor(instance, plans, anchor_plan, fallback_anchor_plan, "vroom", time_limit_sec, vroom_url)),
        }
    return out


def _solve_anchor(
    instance,
    plans: dict[str, np.ndarray],
    anchor_plan: str,
    fallback_anchor_plan: str,
    provider_name: str,
    time_limit_sec: int,
    vroom_url: str,
) -> RouteSet:
    preferred = _solve_with_provider(instance, plans[anchor_plan], anchor_plan, provider_name, time_limit_sec, vroom_url)
    if preferred.feasible:
        return preferred
    return _solve_with_provider(instance, plans[fallback_anchor_plan], fallback_anchor_plan, provider_name, time_limit_sec, vroom_url)


def _solve_with_provider(
    instance,
    planned_loads: np.ndarray,
    method: str,
    provider_name: str,
    time_limit_sec: int,
    vroom_url: str,
) -> RouteSet:
    nodes, demands, distance_matrix = instance_to_provider_inputs(instance, planned_loads)
    if provider_name == "ortools":
        provider = OrToolsProvider(method=method, time_limit_sec=time_limit_sec)
    elif provider_name == "vroom":
        provider = VroomProvider(vroom_url=vroom_url, method=method, timeout_sec=max(5, time_limit_sec + 5))
    else:
        raise ValueError(f"Unknown provider: {provider_name}")
    return provider.solve(
        nodes=nodes,
        demands=demands,
        vehicle_capacity=float(instance.capacity),
        num_vehicles=vehicle_count_from_name(instance.name),
        distance_matrix=distance_matrix,
    )


def _route_grouping_divergence(route_sets: dict[str, dict[str, tuple[object, RouteSet]]]) -> pd.DataFrame:
    rows = []
    for instance_name, provider_data in route_sets.items():
        instance = provider_data["ortools"][0]
        _, customer_indices = customer_view(instance)
        ortools_pairs = _co_route_pairs(provider_data["ortools"][1], customer_indices)
        vroom_pairs = _co_route_pairs(provider_data["vroom"][1], customer_indices)
        union = ortools_pairs | vroom_pairs
        similarity = len(ortools_pairs & vroom_pairs) / len(union) if union else 1.0
        rows.append(
            {
                "Instance": instance_name,
                "Divergence Score": 1.0 - similarity,
                "Jaccard Similarity": similarity,
                "OR-Tools Co-route Pairs": len(ortools_pairs),
                "VROOM Co-route Pairs": len(vroom_pairs),
            }
        )
    return pd.DataFrame(rows).sort_values("Instance")


def _co_route_pairs(route_set: RouteSet, customer_indices: np.ndarray) -> set[tuple[int, int]]:
    customers = set(int(node) for node in customer_indices)
    pairs: set[tuple[int, int]] = set()
    for route in route_set.routes:
        route_customers = [int(node) for node in route if int(node) in customers]
        for a, b in combinations(sorted(route_customers), 2):
            pairs.add((a, b))
    return pairs


def _exposure_rank_diff(route_sets: dict[str, dict[str, tuple[object, RouteSet]]], data_dir: Path) -> pd.DataFrame:
    rows = []
    for instance_name, provider_data in route_sets.items():
        instance = provider_data["ortools"][0]
        node_meta = pd.read_csv(data_dir / instance_name / "proxy_node_meta.csv")
        for domain in available_adapters():
            adapter = get_adapter(domain)
            ortools_features = adapter.route_features(instance, provider_data["ortools"][1], node_meta)
            vroom_features = adapter.route_features(instance, provider_data["vroom"][1], node_meta)
            diff = np.abs(
                ortools_features["arrival_exposure_rank"].to_numpy(float)
                - vroom_features["arrival_exposure_rank"].to_numpy(float)
            )
            rows.append(
                {
                    "Instance": instance_name,
                    "Domain": domain,
                    "Avg Rank Diff": float(diff.mean()),
                    "Std Dev": float(diff.std(ddof=1)) if len(diff) > 1 else 0.0,
                }
            )
    return pd.DataFrame(rows).sort_values(["Instance", "Domain"])


def _stockout_diffs(ortools_results: str, vroom_results: str) -> pd.DataFrame:
    ortools = pd.read_csv(ortools_results)
    vroom = pd.read_csv(vroom_results)
    merged = ortools[["instance", "domain", "stockout_rate"]].merge(
        vroom[["instance", "domain", "stockout_rate"]],
        on=["instance", "domain"],
        suffixes=("_ortools", "_vroom"),
    )
    merged["stockout_diff_signed"] = merged["stockout_rate_ortools"] - merged["stockout_rate_vroom"]
    merged["stockout_diff_abs"] = merged["stockout_diff_signed"].abs()
    return merged.rename(columns={"instance": "Instance", "domain": "Domain"})


def _correlations(divergence: pd.DataFrame, stockout: pd.DataFrame) -> pd.DataFrame:
    rows = []
    data = stockout.merge(divergence[["Instance", "Divergence Score"]], on="Instance", how="left")
    for domain, group in data.groupby("Domain"):
        x = group["Divergence Score"].to_numpy(float)
        y = group["stockout_diff_signed"].to_numpy(float)
        abs_y = group["stockout_diff_abs"].to_numpy(float)
        signed_r, signed_p = _pearson(x, y)
        abs_r, abs_p = _pearson(x, abs_y)
        rows.append(
            {
                "Domain": domain,
                "n": len(group),
                "Pearson r (signed)": signed_r,
                "p-value (signed)": signed_p,
                "Pearson r (abs)": abs_r,
                "p-value (abs)": abs_p,
                "Mean Abs Stockout Diff": float(abs_y.mean()),
            }
        )
    return pd.DataFrame(rows).sort_values("Domain")


def _pearson(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    if len(x) < 2 or np.allclose(x, x[0]) or np.allclose(y, y[0]):
        return float("nan"), float("nan")
    result = pearsonr(x, y)
    return float(result.statistic), float(result.pvalue)


def _domain_sensitivity(divergence: pd.DataFrame, stockout: pd.DataFrame) -> pd.DataFrame:
    threshold = float(divergence["Divergence Score"].median())
    data = stockout.merge(divergence[["Instance", "Divergence Score"]], on="Instance", how="left")
    data["high_divergence"] = data["Divergence Score"] >= threshold
    return (
        data.groupby("Domain")
        .agg(
            avg_abs_stockout_diff=("stockout_diff_abs", "mean"),
            avg_abs_stockout_diff_high_divergence=(
                "stockout_diff_abs",
                lambda values: float(values[data.loc[values.index, "high_divergence"]].mean()),
            ),
            max_abs_stockout_diff=("stockout_diff_abs", "max"),
        )
        .reset_index()
        .sort_values("avg_abs_stockout_diff_high_divergence", ascending=False)
    )


def _write_report(
    path: Path,
    divergence: pd.DataFrame,
    exposure_diff: pd.DataFrame,
    correlations: pd.DataFrame,
    sensitivity: pd.DataFrame,
) -> None:
    strongest = correlations.loc[correlations["Pearson r (abs)"].abs().idxmax()]
    sensitivity_order = " > ".join(sensitivity["Domain"].tolist())
    text = f"""# Route Grouping Sensitivity Report

## Bulgu

Route grouping farki ile stockout degisimi arasinda net ama zayif-orneklemli bir yon sinyali gozlemlendi. En onemli sinir: n=4 instance. Bu nedenle sonucu istatistiksel kanit olarak degil, hipotez olusturan bir tani testi olarak okumak gerekir.

Route grouping divergence:

{_markdown_table(divergence[["Instance", "Divergence Score"]])}

Exposure rank farki domain bazinda ayni cikti, cunku mevcut adapter'lar ayni route feature uretimini paylasiyor. Cold-chain bu feature'i objective icinde dogrudan kullaniyor; grocery ise mevcut implementasyonda exposure rank'i dogrudan kullanmiyor.

Onemli ayrim: `A-n32-k5` ve `P-n19-k2` icin grouping divergence 0.0 cikti, fakat exposure rank diff sifir degil. Bu, iki motorun ayni musteri gruplarini koruyup rota icindeki ziyaret sirasini degistirebildigini gosterir. Dolayisiyla route grouping divergence tek basina cold-chain etkisini aciklamaya yetmez; route order / exposure divergence da ayrica izlenmelidir.

{_markdown_table(exposure_diff)}

Pearson korelasyonlari:

{_markdown_table(correlations)}

Domain hassasiyeti, ortalama mutlak stockout farkina gore. `High divergence`, instance divergence skorunun medyan veya ustunde oldugu durumlar olarak tanimlandi:

{_markdown_table(sensitivity)}

En guclu mutlak korelasyon `{strongest["Domain"]}` domain'inde goruldu: r={strongest["Pearson r (abs)"]:.4f}, p={strongest["p-value (abs)"]:.4f}. p-value n=4 nedeniyle guvenilir karar siniri olarak kullanilmamalidir.

High-divergence instance'larda mutlak stockout hassasiyeti sirasi:

```text
{sensitivity_order}
```

Beklenti cold_chain/grocery > cargo/atm idi. Veri bunu tam dogrulamadi. Bu kosuda en hassas domain'ler `atm` ve `cargo` tarafina kaydi; cold_chain orta seviyede, grocery en dusuk seviyede kaldi. Bunun nedeni, mevcut grocery objective'inin route exposure'i dogrudan kullanmamasi ve cold_chain'in exposure'a duyarli olsa da load-penalty uzerinden farki daha cok maliyete yansitmasi olabilir. Yani route grouping farki stockout'u etkiliyor, ancak etki beklenen domain siralamasini otomatik uretmiyor.

## Doğru Cümle

Route grouping farki ile stockout degisimi arasinda zayif/orta duzeyde bir iliski gozlemlenmistir, ancak n=4 instance ile bu istatistiksel olarak kesin degildir.

## Henüz Doğru Olmayan Cümle

Route-exposure'a bagimli domain'ler motora karsi her zaman daha hassastir.

## Sonraki Adım

Bu hipotezi dogrulamak icin en az 15-20 instance ile ayni analiz tekrarlanmali. Ek olarak, route grouping divergence ile route order/exposure divergence ayrilmali; cunku ayni musteri gruplari korunsa bile ziyaret sirasi degisince cold_chain gibi domain'lerde load-penalty ve stockout davranisi degisebilir.
"""
    path.write_text(text, encoding="utf-8")


def _markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda value: "" if pd.isna(value) else f"{value:.4f}")
    headers = [str(col) for col in display.columns]
    rows = [[str(value) for value in row] for row in display.to_numpy()]
    widths = [
        max(len(headers[idx]), *(len(row[idx]) for row in rows)) if rows else len(headers[idx])
        for idx in range(len(headers))
    ]
    header = "| " + " | ".join(headers[idx].ljust(widths[idx]) for idx in range(len(headers))) + " |"
    separator = "| " + " | ".join("-" * widths[idx] for idx in range(len(headers))) + " |"
    body = [
        "| " + " | ".join(row[idx].ljust(widths[idx]) for idx in range(len(headers))) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


if __name__ == "__main__":
    main()
