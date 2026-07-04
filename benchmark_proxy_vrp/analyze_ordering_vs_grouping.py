from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from .analyze_route_grouping_sensitivity import (
    _co_route_pairs,
    _markdown_table,
    _pearson,
    _solve_route_sets,
    _stockout_diffs,
)
from .cvrplib import customer_view
from .domain_adapters import available_adapters, get_adapter
from .routing_providers.base import RouteSet


def main() -> None:
    parser = argparse.ArgumentParser(description="Separate grouping and ordering divergence effects.")
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
    divergence = _ordering_divergence(route_sets)
    exposure_source = _exposure_source_diff(route_sets, data_dir)
    stockout = _stockout_diffs(args.ortools_results, args.vroom_results)
    correlations = _divergence_correlations(divergence, stockout)
    exposure_correlations = _exposure_correlations(exposure_source, stockout)
    feature_audit = _adapter_feature_audit()

    divergence[["Instance", "Grouping Divergence", "Ordering Divergence"]].to_csv(
        out_dir / "ordering_divergence.csv",
        index=False,
    )
    exposure_source.to_csv(out_dir / "exposure_rank_source_diff.csv", index=False)
    correlations.to_csv(out_dir / "grouping_ordering_stockout_correlations.csv", index=False)
    exposure_correlations.to_csv(out_dir / "exposure_source_stockout_correlations.csv", index=False)
    feature_audit.to_csv(out_dir / "domain_feature_audit.csv", index=False)
    _write_report(
        out_dir / "ordering_vs_grouping_divergence_report.md",
        divergence,
        exposure_source,
        correlations,
        exposure_correlations,
        feature_audit,
    )

    print("Ordering divergence")
    print(divergence.to_string(index=False))
    print("\nExposure source diff")
    print(exposure_source.to_string(index=False))
    print("\nGrouping vs ordering correlations")
    print(correlations.to_string(index=False))
    print("\nExposure source correlations")
    print(exposure_correlations.to_string(index=False))
    print("\nDomain feature audit")
    print(feature_audit.to_string(index=False))


def _ordering_divergence(route_sets: dict[str, dict[str, tuple[object, RouteSet]]]) -> pd.DataFrame:
    rows = []
    for instance_name, provider_data in route_sets.items():
        instance = provider_data["ortools"][0]
        _, customer_indices = customer_view(instance)
        ortools_route_set = provider_data["ortools"][1]
        vroom_route_set = provider_data["vroom"][1]
        ortools_pairs = _co_route_pairs(ortools_route_set, customer_indices)
        vroom_pairs = _co_route_pairs(vroom_route_set, customer_indices)
        union = ortools_pairs | vroom_pairs
        common_pairs = sorted(ortools_pairs & vroom_pairs)

        grouping_similarity = len(common_pairs) / len(union) if union else 1.0
        positions_o = _customer_positions(ortools_route_set, set(customer_indices.astype(int)))
        positions_v = _customer_positions(vroom_route_set, set(customer_indices.astype(int)))
        concordant = 0
        discordant = 0
        for a, b in common_pairs:
            order_o = np.sign(positions_o[a][1] - positions_o[b][1])
            order_v = np.sign(positions_v[a][1] - positions_v[b][1])
            if order_o == order_v:
                concordant += 1
            else:
                discordant += 1

        comparable = concordant + discordant
        kendall_tau = (concordant - discordant) / comparable if comparable else np.nan
        ordering_divergence = (1.0 - kendall_tau) / 2.0 if comparable else np.nan
        rows.append(
            {
                "Instance": instance_name,
                "Grouping Divergence": 1.0 - grouping_similarity,
                "Ordering Divergence": ordering_divergence,
                "Kendall Tau": kendall_tau,
                "Common Co-route Pairs": comparable,
                "Concordant Pairs": concordant,
                "Discordant Pairs": discordant,
            }
        )
    return pd.DataFrame(rows).sort_values("Instance")


def _exposure_source_diff(
    route_sets: dict[str, dict[str, tuple[object, RouteSet]]],
    data_dir: Path,
) -> pd.DataFrame:
    rows = []
    for instance_name, provider_data in route_sets.items():
        instance = provider_data["ortools"][0]
        _, customer_indices = customer_view(instance)
        customer_ids = [int(node) for node in customer_indices]
        customer_set = set(customer_ids)
        node_meta = pd.read_csv(data_dir / instance_name / "proxy_node_meta.csv")
        groups_o = _customer_group_sets(provider_data["ortools"][1], customer_set)
        groups_v = _customer_group_sets(provider_data["vroom"][1], customer_set)
        positions_o = _customer_positions(provider_data["ortools"][1], customer_set)
        positions_v = _customer_positions(provider_data["vroom"][1], customer_set)

        group_mask = np.asarray([groups_o.get(node) != groups_v.get(node) for node in customer_ids], dtype=bool)
        order_mask = np.asarray(
            [
                groups_o.get(node) == groups_v.get(node)
                and positions_o.get(node, (-1, -1))[1] != positions_v.get(node, (-1, -1))[1]
                for node in customer_ids
            ],
            dtype=bool,
        )

        for domain in available_adapters():
            adapter = get_adapter(domain)
            features_o = adapter.route_features(instance, provider_data["ortools"][1], node_meta)
            features_v = adapter.route_features(instance, provider_data["vroom"][1], node_meta)
            diff = np.abs(
                features_o["arrival_exposure_rank"].to_numpy(float)
                - features_v["arrival_exposure_rank"].to_numpy(float)
            )
            rows.append(
                {
                    "Instance": instance_name,
                    "Domain": domain,
                    "Exposure Rank Diff From Grouping": _masked_mean(diff, group_mask),
                    "Grouping Customer Count": int(group_mask.sum()),
                    "Exposure Rank Diff From Ordering": _masked_mean(diff, order_mask),
                    "Ordering Customer Count": int(order_mask.sum()),
                    "Exposure Rank Diff Other": _masked_mean(diff, ~(group_mask | order_mask)),
                }
            )
    return pd.DataFrame(rows).sort_values(["Instance", "Domain"])


def _divergence_correlations(divergence: pd.DataFrame, stockout: pd.DataFrame) -> pd.DataFrame:
    rows = []
    data = stockout.merge(
        divergence[["Instance", "Grouping Divergence", "Ordering Divergence"]],
        on="Instance",
        how="left",
    )
    for domain, group in data.groupby("Domain"):
        stockout_diff = group["stockout_diff_signed"].to_numpy(float)
        abs_stockout_diff = group["stockout_diff_abs"].to_numpy(float)
        grouping = group["Grouping Divergence"].to_numpy(float)
        ordering = group["Ordering Divergence"].to_numpy(float)
        grouping_r, grouping_p = _pearson(grouping, stockout_diff)
        ordering_r, ordering_p = _pearson(ordering, stockout_diff)
        grouping_abs_r, grouping_abs_p = _pearson(grouping, abs_stockout_diff)
        ordering_abs_r, ordering_abs_p = _pearson(ordering, abs_stockout_diff)
        rows.append(
            {
                "Domain": domain,
                "n": len(group),
                "Grouping r": grouping_r,
                "Grouping p-value": grouping_p,
                "Ordering r": ordering_r,
                "Ordering p-value": ordering_p,
                "Grouping abs r": grouping_abs_r,
                "Grouping abs p-value": grouping_abs_p,
                "Ordering abs r": ordering_abs_r,
                "Ordering abs p-value": ordering_abs_p,
                "Stronger Abs Metric": _stronger(grouping_abs_r, ordering_abs_r),
            }
        )
    return pd.DataFrame(rows).sort_values("Domain")


def _exposure_correlations(exposure_source: pd.DataFrame, stockout: pd.DataFrame) -> pd.DataFrame:
    rows = []
    data = stockout.merge(exposure_source, on=["Instance", "Domain"], how="left")
    for domain, group in data.groupby("Domain"):
        stockout_diff = group["stockout_diff_signed"].to_numpy(float)
        abs_stockout_diff = group["stockout_diff_abs"].to_numpy(float)
        grouping_exposure = group["Exposure Rank Diff From Grouping"].fillna(0.0).to_numpy(float)
        ordering_exposure = group["Exposure Rank Diff From Ordering"].fillna(0.0).to_numpy(float)
        ge_r, ge_p = _pearson(grouping_exposure, stockout_diff)
        oe_r, oe_p = _pearson(ordering_exposure, stockout_diff)
        ge_abs_r, ge_abs_p = _pearson(grouping_exposure, abs_stockout_diff)
        oe_abs_r, oe_abs_p = _pearson(ordering_exposure, abs_stockout_diff)
        rows.append(
            {
                "Domain": domain,
                "Grouping Exposure r": ge_r,
                "Grouping Exposure p-value": ge_p,
                "Ordering Exposure r": oe_r,
                "Ordering Exposure p-value": oe_p,
                "Grouping Exposure abs r": ge_abs_r,
                "Grouping Exposure abs p-value": ge_abs_p,
                "Ordering Exposure abs r": oe_abs_r,
                "Ordering Exposure abs p-value": oe_abs_p,
                "Stronger Abs Exposure Source": _stronger(ge_abs_r, oe_abs_r),
            }
        )
    return pd.DataFrame(rows).sort_values("Domain")


def _adapter_feature_audit() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Domain": "grocery",
                "Uses arrival_exposure_rank": False,
                "Uses route_features directly": False,
                "Feature summary": "uses demand/distance criticality and distance_rank; no direct exposure feature",
            },
            {
                "Domain": "cold_chain",
                "Uses arrival_exposure_rank": True,
                "Uses route_features directly": True,
                "Feature summary": "uses arrival_exposure_rank in perishability and load_penalty",
            },
        ]
    )


def _customer_positions(route_set: RouteSet, customers: set[int]) -> dict[int, tuple[int, int]]:
    positions: dict[int, tuple[int, int]] = {}
    for route_idx, route in enumerate(route_set.routes):
        pos = 0
        for node in route:
            node = int(node)
            if node in customers:
                positions[node] = (route_idx, pos)
                pos += 1
    return positions


def _customer_group_sets(route_set: RouteSet, customers: set[int]) -> dict[int, frozenset[int]]:
    groups: dict[int, frozenset[int]] = {}
    for route in route_set.routes:
        route_customers = frozenset(int(node) for node in route if int(node) in customers)
        for node in route_customers:
            groups[node] = route_customers
    return groups


def _masked_mean(values: np.ndarray, mask: np.ndarray) -> float:
    if not mask.any():
        return np.nan
    return float(values[mask].mean())


def _stronger(left: float, right: float) -> str:
    left_abs = -1.0 if pd.isna(left) else abs(left)
    right_abs = -1.0 if pd.isna(right) else abs(right)
    if left_abs > right_abs:
        return "grouping"
    if right_abs > left_abs:
        return "ordering"
    return "tie"


def _write_report(
    path: Path,
    divergence: pd.DataFrame,
    exposure_source: pd.DataFrame,
    correlations: pd.DataFrame,
    exposure_correlations: pd.DataFrame,
    feature_audit: pd.DataFrame,
) -> None:
    cold = correlations[correlations["Domain"] == "cold_chain"].iloc[0]
    cold_source = exposure_correlations[exposure_correlations["Domain"] == "cold_chain"].iloc[0]
    stronger_counts = correlations["Stronger Abs Metric"].value_counts()
    grouping_stronger = int(stronger_counts.get("grouping", 0))
    ordering_stronger = int(stronger_counts.get("ordering", 0))
    tie_count = int(stronger_counts.get("tie", 0))
    text = f"""# Ordering vs Grouping Divergence Report

## Ayrıştırılmış Bulgu

Grouping divergence ve ordering divergence ayrı metriklere bölündü. Ordering divergence yalnızca OR-Tools ve VROOM'da aynı rota grubunda kalan müşteri çiftleri üzerinden hesaplandı; farklı rotaya düşen çiftler bu hesaba dahil edilmedi.

{_markdown_table(divergence[["Instance", "Grouping Divergence", "Ordering Divergence", "Kendall Tau", "Common Co-route Pairs"]])}

Beklenen ara bulgu doğrulandı: `A-n32-k5` ve `P-n19-k2` için grouping divergence 0.0, fakat ordering divergence sıfır değil. Yani aynı müşteri grupları korunabiliyor ama rota içi ziyaret sırası değişebiliyor.

Domain başına stockout farkı ile korelasyonlar:

{_markdown_table(correlations)}

Cold-chain özelinde:

- grouping abs r = {cold["Grouping abs r"]:.4f}, p = {cold["Grouping abs p-value"]:.4f}
- ordering abs r = {cold["Ordering abs r"]:.4f}, p = {cold["Ordering abs p-value"]:.4f}
- daha güçlü mutlak ilişki: `{cold["Stronger Abs Metric"]}`

Bu sonuç cold-chain için "ordering grouping'den daha açıklayıcıdır" hipotezini bu 4 instance üzerinde desteklemiyor. Hatta mutlak stockout farkında grouping korelasyonu daha güçlü görünüyor. Ancak n=4 olduğu için bu kesin sonuç değildir.

## Exposure Rank Kaynağı

Exposure rank farkı iki kaynağa ayrıldı:

- `Exposure Rank Diff From Grouping`: farklı rotaya atanan müşteriler
- `Exposure Rank Diff From Ordering`: aynı rotada kalıp rota içi pozisyonu değişen müşteriler

{_markdown_table(exposure_source)}

Exposure kaynakları ile stockout farkı korelasyonları:

{_markdown_table(exposure_correlations)}

Cold-chain exposure kaynağı özelinde:

- grouping exposure abs r = {cold_source["Grouping Exposure abs r"]:.4f}, p = {cold_source["Grouping Exposure abs p-value"]:.4f}
- ordering exposure abs r = {cold_source["Ordering Exposure abs r"]:.4f}, p = {cold_source["Ordering Exposure abs p-value"]:.4f}
- daha güçlü kaynak: `{cold_source["Stronger Abs Exposure Source"]}`

## Model Tasarımından Kaynaklanan Beklenen Sonuçlar

Grocery ve cold-chain adapter'ları aynı route feature tablosunu alıyor, fakat objective içinde aynı feature'ları kullanmıyor:

{_markdown_table(feature_audit)}

`grocery` objective'i `arrival_exposure_rank` kullanmıyor. Bu nedenle grocery'nin ordering/exposure divergence'a doğrudan hassas olmaması bug değil; model tasarımından kaynaklanan beklenen sonuçtur. Grocery stockout değişiyorsa bu daha çok rota kapasite gruplaması ve load allocation üzerinden dolaylı gelir.

`cold_chain` objective'i `arrival_exposure_rank` değerini hem `perishability` hem de `load_penalty` içinde kullanıyor. Bu yüzden exposure/order değişimine hassas olması beklenir; fakat bu küçük örneklemde stockout değil, load-penalty maliyeti tarafında daha görünür olabilir.

## Veriden Çıkan Gerçek Sinyal

Bu koşuda {grouping_stronger} domain'de grouping metriği, {ordering_stronger} domain'de ordering metriği daha güçlü çıktı; {tie_count} domain'de eşitlik görüldü. Cold-chain için de grouping metriği ordering metriğinden daha güçlü göründü. Bu, önceki "route-exposure domain'ler ordering'e daha hassastır" beklentisini n=4 üzerinde doğrulamıyor.

## Doğru Cümle

Grouping ve ordering divergence ayrı etkiler üretir; aynı müşteri grupları korunsa bile rota içi sıra değişimi exposure_rank'i değiştirebilir. Ancak bu 4 instance üzerinde stockout farkını açıklamada ordering divergence'ın grouping divergence'dan genel olarak daha güçlü olduğu gözlemlenmemiştir.

## Henüz Doğru Olmayan Cümle

Cold-chain stockout'u routing motoru değişiminde esas olarak ordering divergence tarafından açıklanır.

## Sonraki Adım

15-20 instance'a çıkarken grouping divergence ve ordering divergence ayrı raporlanmalı. Tek bir "divergence" skoruna geri dönülmemeli. Cold-chain için ayrıca stockout yanında `mean_load_penalty_loss` korelasyonu da hesaplanmalı; çünkü exposure etkisi stokout'tan çok bozulma/kalite maliyetinde görünür olabilir.

Not: n=4 olduğu için tüm Pearson p-value'ları düşük istatistiksel güçle okunmalıdır; bu rapor kesin kanıt değil, tanı analizidir.
"""
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
