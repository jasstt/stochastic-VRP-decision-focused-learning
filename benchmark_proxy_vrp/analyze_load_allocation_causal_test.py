from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

from .analyze_stockout_mechanisms import _markdown_table, _solve_anchor
from .cvrplib import customer_view, load_instance_json
from .domain_adapters import available_adapters, get_adapter
from .ortools_baselines import build_plans
from .scenario_reduction import scenario_reduction_summary, select_representative_scenarios
from .stochastic_engine import FixedRouteProblem, StochasticDecisionEngine, available_lp_backends, evaluate_solution


PROVIDER_LABELS = {"ortools": "OR-Tools", "vroom": "VROOM"}
PROVIDER_KEYS = {"OR-Tools": "ortools", "VROOM": "vroom"}
SCENARIOS = [
    ("OR-Tools route + OR-Tools allocation", "ortools", "ortools", "baseline"),
    ("OR-Tools route + VROOM allocation", "ortools", "vroom", "intervention"),
    ("VROOM route + VROOM allocation", "vroom", "vroom", "baseline"),
    ("VROOM route + OR-Tools allocation", "vroom", "ortools", "intervention"),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a load-allocation intervention test for stockout shifts.")
    parser.add_argument("--data-dir", default="benchmarks/proxy_cvrplib_x_v4")
    parser.add_argument("--out-dir", default="benchmarks/proxy_cvrplib_x_v4")
    parser.add_argument("--domains", nargs="+", default=available_adapters())
    parser.add_argument("--anchor-plan", default="proxy_mean_or_tools")
    parser.add_argument("--fallback-anchor-plan", default="nominal_or_tools")
    parser.add_argument("--time-limit-sec", type=int, default=20)
    parser.add_argument("--lp-time-limit-sec", type=int, default=30)
    parser.add_argument("--lp-backend", choices=available_lp_backends(), default="pulp_cbc")
    parser.add_argument(
        "--lp-planning-scenario-limit",
        type=int,
        default=None,
        help="Use a deterministic total-demand-stratified subset for faster LP diagnostics.",
    )
    parser.add_argument("--vroom-url", default="http://localhost:3000")
    parser.add_argument("--ambiguity-epsilon", type=float, default=1e-6)
    parser.add_argument("--start-index", type=int, default=0, help="Zero-based instance start index after sorting.")
    parser.add_argument("--max-instances", type=int, default=None)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    results, audit = _run_interventions(args, data_dir)
    results = _attach_similarity(results, args.ambiguity_epsilon)
    scenario_summary = _scenario_summary(results)
    domain_summary = _domain_summary(results)

    audit.to_csv(out_dir / "load_allocation_causal_test_audit.csv", index=False)
    results.to_csv(out_dir / "load_allocation_causal_test_results.csv", index=False)
    scenario_summary.to_csv(out_dir / "load_allocation_causal_test_summary.csv", index=False)
    domain_summary.to_csv(out_dir / "load_allocation_causal_test_domain_summary.csv", index=False)
    _write_report(
        out_dir / "load_allocation_causal_test_report.md",
        audit=audit,
        results=results,
        scenario_summary=scenario_summary,
        domain_summary=domain_summary,
    )

    print("Scenario summary")
    print(scenario_summary.to_string(index=False))
    print("\nDomain summary")
    print(domain_summary.to_string(index=False))
    print(f"\nSaved {out_dir / 'load_allocation_causal_test_report.md'}")


def _run_interventions(args: argparse.Namespace, data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    engine = StochasticDecisionEngine(lp_backend=args.lp_backend)
    rows = []
    audit_rows = []
    instance_paths = sorted(data_dir.glob("*/instance.json"))
    if args.start_index:
        instance_paths = instance_paths[args.start_index :]
    if args.max_instances is not None:
        instance_paths = instance_paths[: args.max_instances]

    for position, instance_json in enumerate(instance_paths, start=1):
        instance = load_instance_json(instance_json)
        print(f"[{position}/{len(instance_paths)}] {instance.name}: solving anchors", flush=True)
        instance_dir = instance_json.parent
        nominal, _ = customer_view(instance)
        history = pd.read_csv(instance_dir / "proxy_demand_history.csv").drop(columns=["date"]).to_numpy()
        lp_history = select_representative_scenarios(history, args.lp_planning_scenario_limit)
        lp_scenario_summary = scenario_reduction_summary(history, lp_history)
        scenarios = np.load(instance_dir / "proxy_saa_scenarios.npy")
        node_meta = pd.read_csv(instance_dir / "proxy_node_meta.csv")
        plans = build_plans(history, nominal)
        anchors = {
            "ortools": _solve_anchor(
                instance,
                plans,
                args.anchor_plan,
                args.fallback_anchor_plan,
                "ortools",
                args.time_limit_sec,
                args.vroom_url,
            ),
            "vroom": _solve_anchor(
                instance,
                plans,
                args.anchor_plan,
                args.fallback_anchor_plan,
                "vroom",
                args.time_limit_sec,
                args.vroom_url,
            ),
        }
        route_counts = {provider: len(route_set.routes) if route_set.feasible else 0 for provider, route_set in anchors.items()}
        common_anchor_feasible = anchors["ortools"].feasible and anchors["vroom"].feasible
        same_route_count = common_anchor_feasible and route_counts["ortools"] == route_counts["vroom"]
        audit_rows.append(
            {
                "Instance": instance.name,
                "Customers": instance.n_customers,
                "OR-Tools Anchor Feasible": anchors["ortools"].feasible,
                "VROOM Anchor Feasible": anchors["vroom"].feasible,
                "Common Anchor Feasible": common_anchor_feasible,
                "OR-Tools Route Count": route_counts["ortools"],
                "VROOM Route Count": route_counts["vroom"],
                "Same Route Count": same_route_count,
            }
        )
        if not common_anchor_feasible:
            print(f"[{position}/{len(instance_paths)}] {instance.name}: skipped, no common anchor", flush=True)
            continue

        print(f"[{position}/{len(instance_paths)}] {instance.name}: running domain interventions", flush=True)
        for domain_name in args.domains:
            adapter = get_adapter(domain_name)
            problems = {
                provider: adapter.build_problem(
                    instance=instance,
                    anchor_routes=route_set,
                    planning_scenarios=lp_history,
                    evaluation_scenarios=scenarios,
                    node_meta=node_meta,
                )
                for provider, route_set in anchors.items()
            }
            baseline = {
                provider: engine.solve(problem, time_limit_sec=args.lp_time_limit_sec)
                for provider, problem in problems.items()
            }
            if not baseline["ortools"].feasible or not baseline["vroom"].feasible:
                for scenario_name, route_source, allocation_source, scenario_type in SCENARIOS:
                    rows.append(
                        _empty_row(
                            instance.name,
                            domain_name,
                            scenario_name,
                            scenario_type,
                            route_source,
                            allocation_source,
                            "baseline_lp_infeasible",
                        )
                    )
                continue

            route_targets = {
                provider: _route_load_targets(problems[provider].route_groups, baseline[provider].loads)
                for provider in problems
            }
            for scenario_name, route_source, allocation_source, scenario_type in SCENARIOS:
                row_base = {
                    "Instance": instance.name,
                    "Domain": domain_name,
                    "Scenario": scenario_name,
                    "Scenario Type": scenario_type,
                    "Route Source": PROVIDER_LABELS[route_source],
                    "Allocation Source": PROVIDER_LABELS[allocation_source],
                    "OR-Tools Route Count": route_counts["ortools"],
                    "VROOM Route Count": route_counts["vroom"],
                    "Same Route Count": same_route_count,
                    **lp_scenario_summary,
                }
                if route_source == allocation_source:
                    solution = baseline[route_source]
                    metrics = evaluate_solution(problems[route_source], solution.loads)
                    rows.append(
                        {
                            **row_base,
                            "Feasible": True,
                            "Reason": "",
                            "Route Cost": problems[route_source].route_cost,
                            "LP Backend": args.lp_backend,
                            "Planned Load Total": float(np.sum(solution.loads)),
                            "Runtime Sec": solution.runtime_sec,
                            **metrics,
                        }
                    )
                    continue
                if not same_route_count:
                    rows.append({**row_base, **_skip_payload("route_count_mismatch")})
                    continue
                try:
                    forced_targets = _match_allocation_targets(
                        allocation_targets=route_targets[allocation_source],
                        target_baseline_targets=route_targets[route_source],
                        route_capacity=float(instance.capacity),
                    )
                    hybrid_problem: FixedRouteProblem = replace(
                        problems[route_source],
                        name=f"{domain_name}_engine_{route_source}_routes_{allocation_source}_allocation",
                        route_load_targets=forced_targets,
                    )
                    solution = engine.solve(hybrid_problem, time_limit_sec=args.lp_time_limit_sec)
                    if not solution.feasible:
                        rows.append({**row_base, **_skip_payload(solution.reason or "hybrid_lp_infeasible")})
                        continue
                    metrics = evaluate_solution(hybrid_problem, solution.loads)
                    rows.append(
                        {
                            **row_base,
                            "Feasible": True,
                            "Reason": "",
                            "Route Cost": hybrid_problem.route_cost,
                            "LP Backend": args.lp_backend,
                            "Planned Load Total": float(np.sum(solution.loads)),
                            "Runtime Sec": solution.runtime_sec,
                            **metrics,
                        }
                    )
                except ValueError as exc:
                    rows.append({**row_base, **_skip_payload(str(exc))})
        print(f"[{position}/{len(instance_paths)}] {instance.name}: done", flush=True)

    return pd.DataFrame(rows), pd.DataFrame(audit_rows)


def _route_load_targets(route_groups: list[list[int]], loads: np.ndarray) -> np.ndarray:
    return np.asarray([float(np.sum(loads[cols])) for cols in route_groups], dtype=float)


def _match_allocation_targets(
    allocation_targets: np.ndarray,
    target_baseline_targets: np.ndarray,
    route_capacity: float,
) -> list[float]:
    if len(allocation_targets) != len(target_baseline_targets):
        raise ValueError("route_count_mismatch")
    if np.any(allocation_targets > route_capacity + 1e-3):
        raise ValueError("allocation_target_exceeds_capacity")

    allocation_targets = np.clip(np.asarray(allocation_targets, dtype=float), 0.0, route_capacity)
    source_sorted = np.sort(allocation_targets)[::-1]
    target_order = np.argsort(np.asarray(target_baseline_targets, dtype=float))[::-1]
    out = np.zeros(len(source_sorted), dtype=float)
    for rank, target_idx in enumerate(target_order):
        out[int(target_idx)] = source_sorted[rank]
    return out.tolist()


def _attach_similarity(results: pd.DataFrame, epsilon: float) -> pd.DataFrame:
    if results.empty:
        return results
    out = results.copy()
    out["OR-Tools Stockout"] = np.nan
    out["VROOM Stockout"] = np.nan
    out["Abs Distance to OR-Tools"] = np.nan
    out["Abs Distance to VROOM"] = np.nan
    out["Baseline Stockout Gap"] = np.nan
    out["Closer To"] = ""
    out["Allocation Source Closer"] = False
    out["Route Source Closer"] = False
    out["Movement Fraction to Allocation"] = np.nan

    baseline_lookup = {}
    feasible = out[out["Feasible"] == True]
    for (instance, domain), group in feasible.groupby(["Instance", "Domain"]):
        base = {}
        for provider_label in ("OR-Tools", "VROOM"):
            rows = group[
                (group["Route Source"] == provider_label)
                & (group["Allocation Source"] == provider_label)
                & (group["Scenario Type"] == "baseline")
            ]
            if not rows.empty:
                base[provider_label] = float(rows.iloc[0]["stockout_rate"])
        if set(base) == {"OR-Tools", "VROOM"}:
            baseline_lookup[(instance, domain)] = base

    for idx, row in out.iterrows():
        key = (row["Instance"], row["Domain"])
        if key not in baseline_lookup or not bool(row.get("Feasible", False)):
            continue
        base = baseline_lookup[key]
        stockout = float(row["stockout_rate"])
        dist_or = abs(stockout - base["OR-Tools"])
        dist_vroom = abs(stockout - base["VROOM"])
        gap = abs(base["OR-Tools"] - base["VROOM"])
        out.at[idx, "OR-Tools Stockout"] = base["OR-Tools"]
        out.at[idx, "VROOM Stockout"] = base["VROOM"]
        out.at[idx, "Abs Distance to OR-Tools"] = dist_or
        out.at[idx, "Abs Distance to VROOM"] = dist_vroom
        out.at[idx, "Baseline Stockout Gap"] = gap
        if gap <= epsilon:
            closer = "uninformative_baselines_tied"
        elif abs(dist_or - dist_vroom) <= epsilon:
            closer = "tie"
        elif dist_or < dist_vroom:
            closer = "OR-Tools"
        else:
            closer = "VROOM"
        out.at[idx, "Closer To"] = closer
        route_source = str(row["Route Source"])
        allocation_source = str(row["Allocation Source"])
        out.at[idx, "Allocation Source Closer"] = closer == allocation_source
        out.at[idx, "Route Source Closer"] = closer == route_source
        if route_source in base and allocation_source in base:
            denominator = base[allocation_source] - base[route_source]
            if abs(denominator) > epsilon:
                out.at[idx, "Movement Fraction to Allocation"] = (stockout - base[route_source]) / denominator
    return out


def _scenario_summary(results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for scenario, group in results.groupby("Scenario", sort=False):
        feasible = group[group["Feasible"] == True]
        informative = feasible[feasible["Closer To"].isin(["OR-Tools", "VROOM", "tie"])]
        rows.append(
            {
                "Scenario": scenario,
                "Scenario Type": str(group["Scenario Type"].iloc[0]),
                "Rows": int(len(group)),
                "Feasible Rows": int(len(feasible)),
                "Informative Rows": int(len(informative)),
                "Mean Stockout": _mean(feasible, "stockout_rate"),
                "Mean Abs Distance to OR-Tools": _mean(feasible, "Abs Distance to OR-Tools"),
                "Mean Abs Distance to VROOM": _mean(feasible, "Abs Distance to VROOM"),
                "OR-Tools Closer Share": _share(informative, "Closer To", "OR-Tools"),
                "VROOM Closer Share": _share(informative, "Closer To", "VROOM"),
                "Allocation Source Closer Share": _bool_share(informative, "Allocation Source Closer"),
                "Route Source Closer Share": _bool_share(informative, "Route Source Closer"),
                "Mean Movement Fraction to Allocation": _mean(informative, "Movement Fraction to Allocation"),
            }
        )
    return pd.DataFrame(rows)


def _domain_summary(results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (domain, scenario), group in results.groupby(["Domain", "Scenario"], sort=False):
        feasible = group[group["Feasible"] == True]
        informative = feasible[feasible["Closer To"].isin(["OR-Tools", "VROOM", "tie"])]
        rows.append(
            {
                "Domain": domain,
                "Scenario": scenario,
                "Scenario Type": str(group["Scenario Type"].iloc[0]),
                "Rows": int(len(group)),
                "Feasible Rows": int(len(feasible)),
                "Informative Rows": int(len(informative)),
                "Mean Stockout": _mean(feasible, "stockout_rate"),
                "Allocation Source Closer Share": _bool_share(informative, "Allocation Source Closer"),
                "Route Source Closer Share": _bool_share(informative, "Route Source Closer"),
                "Mean Movement Fraction to Allocation": _mean(informative, "Movement Fraction to Allocation"),
            }
        )
    return pd.DataFrame(rows)


def _write_report(
    path: Path,
    audit: pd.DataFrame,
    results: pd.DataFrame,
    scenario_summary: pd.DataFrame,
    domain_summary: pd.DataFrame,
) -> None:
    total_instances = int(audit["Instance"].nunique()) if not audit.empty else 0
    common = audit[audit["Common Anchor Feasible"] == True]
    same_count = common[common["Same Route Count"] == True]
    intervention_summary = scenario_summary[scenario_summary["Scenario Type"] == "intervention"].copy()
    verdict, a8_status = _causal_verdict(intervention_summary)
    skip_reasons = (
        results[(results["Scenario Type"] == "intervention") & (results["Feasible"] == False)]
        .groupby("Reason", dropna=False)
        .size()
        .rename("Count")
        .reset_index()
        .sort_values("Count", ascending=False)
    )

    requested = scenario_summary[
        [
            "Scenario",
            "Mean Abs Distance to OR-Tools",
            "Mean Abs Distance to VROOM",
            "OR-Tools Closer Share",
            "VROOM Closer Share",
            "Feasible Rows",
            "Informative Rows",
        ]
    ].rename(
        columns={
            "Mean Abs Distance to OR-Tools": "Stockout similarity to real OR-Tools (lower distance)",
            "Mean Abs Distance to VROOM": "Stockout similarity to real VROOM (lower distance)",
        }
    )

    text = f"""# Load Allocation Causal Test Report

## Müdahale Tasarımı

Bu test korelasyon değil, müdahale testidir. Önce OR-Tools ve VROOM route setleri aynı instance üzerinde çözüldü. Sonra her domain için baseline stochastic engine tekrar çalıştırıldı ve her provider'ın route-level planlanan yük toplamları çıkarıldı.

Müdahale şu şekilde uygulandı:

- `OR-Tools route + VROOM allocation`: OR-Tools route grupları sabit kaldı, route-level toplam yük hedefleri VROOM baseline çözümünden alındı.
- `VROOM route + OR-Tools allocation`: VROOM route grupları sabit kaldı, route-level toplam yük hedefleri OR-Tools baseline çözümünden alındı.
- Route etiketleri provider'lar arasında anlamsız olduğu için allocation vektörleri büyükten küçüğe sıralanıp hedef provider'ın büyükten küçüğe route yüklerine eşlendi.
- Aktif route sayısı eşit olmayan instance-domain satırları müdahale için elendi; aksi halde "allocation kaynağı" ile "route sayısı" karışacaktı.

## Dataset ve Feasibility

Çalıştırılan set: {total_instances} CVRPLIB X instance.

Ortak anchor-feasible instance sayısı: {len(common)}.

Aktif route sayısı eşit olan ortak anchor-feasible instance sayısı: {len(same_count)}.

{_markdown_table(audit)}

## Müdahale Sonucu

| Senaryo | Stockout (gerçek OR-Tools'a benzerlik) | Stockout (gerçek VROOM'a benzerlik) |
|---|---:|---:|
{_requested_rows(requested)}

Ayrıntılı scenario özeti:

{_markdown_table(scenario_summary)}

Müdahale uygulanabilirliği:

{_markdown_table(skip_reasons) if not skip_reasons.empty else "Tüm müdahale satırları feasible çözüldü."}

Domain bazlı özet:

{_markdown_table(domain_summary)}

## Nedensellik Değerlendirmesi

{verdict}

Bu değerlendirme `r` veya p-value kullanmaz. Ana ölçü, hibrit stockout'un route kaynağına mı yoksa allocation kaynağına mı daha yakın olduğudur.

## A.8'in Nihai Durumu

{a8_status}

## Doğru Cümle

{_right_sentence(intervention_summary)}

## Henüz Doğru Olmayan Cümle

Load allocation, her domain ve her instance için tek başına stockout farkını tamamen belirler.

## Sonraki Adım

Müdahale sonucu kısmi veya belirsiz kaldıysa, sıradaki test route topology'nin daha ince özelliklerini ayırmalıdır: route uzunluğu dağılımı, route içi yüksek-demand müşteri konumu, first-improvement/best-improvement benzeri solver heuristic farkları ve route-level marginal capacity slack birlikte ölçülmelidir.
"""
    path.write_text(text, encoding="utf-8")


def _causal_verdict(intervention_summary: pd.DataFrame) -> tuple[str, str]:
    if intervention_summary.empty:
        return (
            "Müdahale koşusu uygulanabilir satır üretmedi; nedensellik iddiası test edilemedi.",
            "A.8 açık kalır; common-feasible ve same-route-count koşulu sağlanmadan müdahale testi yorumlanamaz.",
        )
    allocation_share = float(intervention_summary["Allocation Source Closer Share"].mean())
    route_share = float(intervention_summary["Route Source Closer Share"].mean())
    movement = float(intervention_summary["Mean Movement Fraction to Allocation"].mean())
    if allocation_share >= 0.6 and movement >= 0.6:
        return (
            f"Hibritler allocation kaynağına route kaynağından daha yakın çıktı. Ortalama allocation-source closer share {allocation_share:.3f}, route-source closer share {route_share:.3f}, movement fraction {movement:.3f}. Bu, load allocation'ın nedensel mekanizma olarak güçlü biçimde desteklendiğini gösterir.",
            "A.8 kısmen çözüldü: stockout sıralamasındaki motor farkının ölçülen ana mekanizması route-level load allocation'dır. Yine de bu sonuç route-count eşit ve common-feasible alt küme için geçerlidir.",
        )
    if route_share >= 0.6 and movement <= 0.4:
        return (
            f"Hibritler allocation kaynağına değil route kaynağına yakın kaldı. Ortalama allocation-source closer share {allocation_share:.3f}, route-source closer share {route_share:.3f}, movement fraction {movement:.3f}. Bu, load allocation'ın tek başına nedensel mekanizma olmadığını gösterir.",
            "A.8 açık kalır: beş korelasyonel aday ve load-allocation müdahalesi kök nedeni kapatmadı. Routing algoritmasının daha ince topology/heuristic farkları araştırılmalıdır.",
        )
    return (
        f"Müdahale sonucu karışık çıktı. Ortalama allocation-source closer share {allocation_share:.3f}, route-source closer share {route_share:.3f}, movement fraction {movement:.3f}. Bu, load allocation'ın kısmi etkisi olabileceğini ama tek faktör olarak yeterli açıklama olmadığını gösterir.",
        "A.8 kısmen açık kalır: load allocation etkili bir mekanizma olabilir, fakat route topology veya solver heuristic farklarıyla birlikte çalışıyor gibi görünmektedir.",
    )


def _right_sentence(intervention_summary: pd.DataFrame) -> str:
    if intervention_summary.empty:
        return "Load allocation müdahalesi bu koşuda yeterli uygulanabilir satır üretmedi; nedensellik sonucu yok."
    allocation_share = float(intervention_summary["Allocation Source Closer Share"].mean())
    route_share = float(intervention_summary["Route Source Closer Share"].mean())
    if allocation_share > route_share:
        return "Müdahale hibritleri ortalamada allocation kaynağına daha yakın hareket etti; load allocation stockout farkında nedensel bir bileşen olarak desteklenir."
    if route_share > allocation_share:
        return "Müdahale hibritleri ortalamada route kaynağına daha yakın kaldı; load allocation tek başına nedensel açıklama değildir."
    return "Müdahale hibritleri allocation ve route kaynakları arasında net ayrışmadı; sonuç kısmi/belirsizdir."


def _requested_rows(frame: pd.DataFrame) -> str:
    lines = []
    for _, row in frame.iterrows():
        lines.append(
            "| "
            f"{row['Scenario']} | "
            f"{float(row['Stockout similarity to real OR-Tools (lower distance)']):.6f} | "
            f"{float(row['Stockout similarity to real VROOM (lower distance)']):.6f} |"
        )
    return "\n".join(lines)


def _empty_row(
    instance: str,
    domain: str,
    scenario: str,
    scenario_type: str,
    route_source: str,
    allocation_source: str,
    reason: str,
) -> dict[str, object]:
    return {
        "Instance": instance,
        "Domain": domain,
        "Scenario": scenario,
        "Scenario Type": scenario_type,
        "Route Source": PROVIDER_LABELS[route_source],
        "Allocation Source": PROVIDER_LABELS[allocation_source],
        **_skip_payload(reason),
    }


def _skip_payload(reason: str) -> dict[str, object]:
    return {
        "Feasible": False,
        "Reason": reason,
        "Route Cost": np.nan,
        "Planned Load Total": np.nan,
        "Runtime Sec": np.nan,
        "mean_total_cost": np.nan,
        "p90_total_cost": np.nan,
        "cvar90_total_cost": np.nan,
        "mean_shortfall": np.nan,
        "p90_shortfall": np.nan,
        "stockout_rate": np.nan,
        "mean_surplus": np.nan,
        "mean_domain_loss": np.nan,
        "mean_load_penalty_loss": np.nan,
    }


def _mean(frame: pd.DataFrame, column: str) -> float:
    if frame.empty or column not in frame:
        return float("nan")
    return float(pd.to_numeric(frame[column], errors="coerce").mean())


def _share(frame: pd.DataFrame, column: str, value: str) -> float:
    if frame.empty:
        return float("nan")
    return float((frame[column] == value).mean())


def _bool_share(frame: pd.DataFrame, column: str) -> float:
    if frame.empty:
        return float("nan")
    return float(frame[column].astype(bool).mean())


if __name__ == "__main__":
    main()
