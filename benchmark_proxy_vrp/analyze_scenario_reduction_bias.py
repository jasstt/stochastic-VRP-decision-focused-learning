from __future__ import annotations

import argparse
import itertools
import math
from pathlib import Path

import numpy as np
import pandas as pd

from .cvrplib import customer_view, load_instance_json
from .domain_adapters import available_adapters, get_adapter
from .ortools_baselines import build_plans
from .run_domain_engine import _solve_anchor
from .scenario_reduction import scenario_reduction_summary, select_representative_scenarios
from .stochastic_engine import StochasticDecisionEngine, evaluate_solution


DEFAULT_SELECTION = [
    "X-n106-k14",
    "X-n120-k6",
    "X-n143-k7",
    "X-n157-k13",
    "X-n190-k8",
    "X-n214-k11",
    "X-n237-k14",
    "X-n261-k13",
    "X-n284-k15",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Test whether LP scenario reduction creates stockout bias.")
    parser.add_argument("--data-dir", default="benchmarks/proxy_cvrplib_x_v4")
    parser.add_argument("--out-dir", default="benchmarks/proxy_cvrplib_x_v4")
    parser.add_argument("--instances", nargs="+", default=DEFAULT_SELECTION)
    parser.add_argument("--domains", nargs="+", default=available_adapters())
    parser.add_argument("--scenario-limit", type=int, default=60)
    parser.add_argument("--anchor-plan", default="proxy_mean_or_tools")
    parser.add_argument("--fallback-anchor-plan", default="nominal_or_tools")
    parser.add_argument("--time-limit-sec", type=int, default=20)
    parser.add_argument("--lp-time-limit-sec", type=int, default=60)
    parser.add_argument("--bootstrap-samples", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    results = _run_bias_test(args, data_dir)
    instance_summary = _instance_summary(results)
    correlations = _correlations(instance_summary, args.bootstrap_samples, args.seed)

    results.to_csv(out_dir / "scenario_reduction_bias_results.csv", index=False)
    instance_summary.to_csv(out_dir / "scenario_reduction_bias_instance_summary.csv", index=False)
    correlations.to_csv(out_dir / "scenario_reduction_bias_correlations.csv", index=False)
    _write_report(
        out_dir / "scenario_reduction_bias_report.md",
        results=results,
        instance_summary=instance_summary,
        correlations=correlations,
        scenario_limit=args.scenario_limit,
    )

    print("Instance summary")
    print(instance_summary.to_string(index=False))
    print("\nCorrelations")
    print(correlations.to_string(index=False))
    print(f"\nSaved {out_dir / 'scenario_reduction_bias_report.md'}")


def _run_bias_test(args: argparse.Namespace, data_dir: Path) -> pd.DataFrame:
    engine = StochasticDecisionEngine(lp_backend="pulp_cbc")
    rows: list[dict[str, object]] = []
    for position, instance_name in enumerate(args.instances, start=1):
        instance_dir = data_dir / instance_name
        instance_json = instance_dir / "instance.json"
        if not instance_json.exists():
            rows.append(_skipped_row(instance_name, "all", "missing_instance_json"))
            continue

        instance = load_instance_json(instance_json)
        print(f"[{position}/{len(args.instances)}] {instance.name}: solving anchor", flush=True)
        nominal, _ = customer_view(instance)
        history = pd.read_csv(instance_dir / "proxy_demand_history.csv").drop(columns=["date"]).to_numpy()
        limited_history = select_representative_scenarios(history, args.scenario_limit)
        scenario_summary = scenario_reduction_summary(history, limited_history)
        scenarios = np.load(instance_dir / "proxy_saa_scenarios.npy")
        node_meta = pd.read_csv(instance_dir / "proxy_node_meta.csv")
        plans = build_plans(history, nominal)
        anchor_solution = _solve_anchor(
            instance,
            plans,
            args.anchor_plan,
            args.fallback_anchor_plan,
            "ortools",
            "http://localhost:3000",
            args.time_limit_sec,
        )
        if not anchor_solution.feasible:
            rows.append(_skipped_row(instance.name, "all", "no_feasible_anchor_route", scenario_summary))
            continue

        print(f"[{position}/{len(args.instances)}] {instance.name}: solving full vs limit={args.scenario_limit}", flush=True)
        for domain_name in args.domains:
            adapter = get_adapter(domain_name)
            full_problem = adapter.build_problem(
                instance=instance,
                anchor_routes=anchor_solution,
                planning_scenarios=history,
                evaluation_scenarios=scenarios,
                node_meta=node_meta,
            )
            limited_problem = adapter.build_problem(
                instance=instance,
                anchor_routes=anchor_solution,
                planning_scenarios=limited_history,
                evaluation_scenarios=scenarios,
                node_meta=node_meta,
            )
            full_solution = engine.solve(full_problem, time_limit_sec=args.lp_time_limit_sec)
            limited_solution = engine.solve(limited_problem, time_limit_sec=args.lp_time_limit_sec)
            base_row = {
                "Instance": instance.name,
                "Customers": instance.n_customers,
                "Size Bucket": _size_bucket(instance.n_customers),
                "Domain": domain_name,
                "Full Feasible": full_solution.feasible,
                "Limited Feasible": limited_solution.feasible,
                "Full Runtime Sec": full_solution.runtime_sec,
                "Limited Runtime Sec": limited_solution.runtime_sec,
                "Full Objective": full_solution.objective_value,
                "Limited Objective": limited_solution.objective_value,
                **scenario_summary,
            }
            if not full_solution.feasible or not limited_solution.feasible:
                rows.append(
                    {
                        **base_row,
                        "Reason": full_solution.reason or limited_solution.reason,
                        "Full Stockout": np.nan,
                        "Limited Stockout": np.nan,
                        "Signed Stockout Diff": np.nan,
                        "Abs Stockout Diff": np.nan,
                        "Relative Stockout Diff": np.nan,
                        "Full Mean Total Cost": np.nan,
                        "Limited Mean Total Cost": np.nan,
                    }
                )
                continue

            full_metrics = evaluate_solution(full_problem, full_solution.loads)
            limited_metrics = evaluate_solution(limited_problem, limited_solution.loads)
            full_stockout = float(full_metrics["stockout_rate"])
            limited_stockout = float(limited_metrics["stockout_rate"])
            signed_diff = limited_stockout - full_stockout
            abs_diff = abs(signed_diff)
            rel_diff = abs_diff / full_stockout if full_stockout > 0 else np.nan
            rows.append(
                {
                    **base_row,
                    "Reason": "",
                    "Full Stockout": full_stockout,
                    "Limited Stockout": limited_stockout,
                    "Signed Stockout Diff": signed_diff,
                    "Abs Stockout Diff": abs_diff,
                    "Relative Stockout Diff": rel_diff,
                    "Full Mean Total Cost": full_metrics["mean_total_cost"],
                    "Limited Mean Total Cost": limited_metrics["mean_total_cost"],
                }
            )
        print(f"[{position}/{len(args.instances)}] {instance.name}: done", flush=True)
    return pd.DataFrame(rows)


def _instance_summary(results: pd.DataFrame) -> pd.DataFrame:
    feasible = results[(results["Full Feasible"] == True) & (results["Limited Feasible"] == True)].copy()
    if feasible.empty:
        return pd.DataFrame()
    grouped = (
        feasible.groupby(["Instance", "Customers", "Size Bucket"], dropna=False)
        .agg(
            Domains=("Domain", "nunique"),
            Mean_Relative_Stockout_Diff=("Relative Stockout Diff", "mean"),
            Max_Relative_Stockout_Diff=("Relative Stockout Diff", "max"),
            Mean_Abs_Stockout_Diff=("Abs Stockout Diff", "mean"),
            Max_Abs_Stockout_Diff=("Abs Stockout Diff", "max"),
            Mean_Signed_Stockout_Diff=("Signed Stockout Diff", "mean"),
            Positive_Domains=("Signed Stockout Diff", lambda values: int((values > 0).sum())),
            Negative_Domains=("Signed Stockout Diff", lambda values: int((values < 0).sum())),
            Full_Runtime_Sec=("Full Runtime Sec", "sum"),
            Limited_Runtime_Sec=("Limited Runtime Sec", "sum"),
        )
        .reset_index()
    )
    grouped["Runtime Speedup"] = grouped["Full_Runtime_Sec"] / grouped["Limited_Runtime_Sec"].replace(0.0, np.nan)
    grouped["Exceeds 5pct Any Domain"] = grouped["Max_Relative_Stockout_Diff"] > 0.05
    grouped["Exceeds 5pct Mean"] = grouped["Mean_Relative_Stockout_Diff"] > 0.05
    return grouped.sort_values("Customers")


def _correlations(instance_summary: pd.DataFrame, bootstrap_samples: int, seed: int) -> pd.DataFrame:
    rows = []
    if instance_summary.empty:
        return pd.DataFrame()
    for metric in ["Mean_Relative_Stockout_Diff", "Max_Relative_Stockout_Diff", "Mean_Abs_Stockout_Diff"]:
        frame = instance_summary[["Customers", metric]].dropna()
        x = frame["Customers"].to_numpy(float)
        y = frame[metric].to_numpy(float)
        n = len(frame)
        unique_x = len(np.unique(x))
        if n < 3 or unique_x < 3:
            rows.append(
                {
                    "Metric": metric,
                    "n": n,
                    "Unique X Levels": unique_x,
                    "Pearson r": np.nan,
                    "p-value": np.nan,
                    "Bootstrap CI Low": np.nan,
                    "Bootstrap CI High": np.nan,
                    "A.5 Interpretation": "insufficient variation",
                }
            )
            continue
        r = _pearsonr(x, y)
        p_value = _permutation_p_value(x, y, r)
        ci_low, ci_high = _bootstrap_ci(x, y, bootstrap_samples, seed)
        if n < 15:
            interpretation = "diagnostic signal only: n<15"
        elif ci_low <= 0 <= ci_high:
            interpretation = "no stable correlation: bootstrap CI includes zero"
        else:
            interpretation = "stable directional signal"
        rows.append(
            {
                "Metric": metric,
                "n": n,
                "Unique X Levels": unique_x,
                "Pearson r": r,
                "p-value": p_value,
                "Bootstrap CI Low": ci_low,
                "Bootstrap CI High": ci_high,
                "A.5 Interpretation": interpretation,
            }
        )
    return pd.DataFrame(rows)


def _write_report(
    path: Path,
    results: pd.DataFrame,
    instance_summary: pd.DataFrame,
    correlations: pd.DataFrame,
    scenario_limit: int,
) -> None:
    if instance_summary.empty:
        body = "# Scenario Reduction Bias Report\n\nNo feasible rows were produced.\n"
        path.write_text(body, encoding="utf-8")
        return

    max_rel = float(instance_summary["Max_Relative_Stockout_Diff"].max())
    mean_rel = float(instance_summary["Mean_Relative_Stockout_Diff"].mean())
    risky = instance_summary[instance_summary["Exceeds 5pct Any Domain"] == True]
    risky_count = int(len(risky))
    direction = _direction_summary(results)
    strongest_corr = _strongest_correlation(correlations)
    safe_rule = _safe_rule(risky_count, risky)

    lines = [
        "# Scenario Reduction Bias Report",
        "",
        "## Bulgu",
        "",
        f"X40 setinden OR-Tools anchor-feasible 9 instance seçildi: 3 küçük, 3 orta, 3 büyük. Full LP planning history, X40 için 180 senaryodur; hızlı mod `limit={scenario_limit}` kullanır. Routing anchor ve evaluation senaryoları sabit tutuldu, sadece LP training senaryoları değiştirildi.",
        "",
        f"Instance bazında domain-maksimum göreli stockout sapması en fazla {max_rel:.2%}; instance-ortalama göreli sapma ortalaması {mean_rel:.2%}. %5 eşiğini herhangi bir domain'de aşan instance sayısı: {risky_count}/{len(instance_summary)}.",
        "",
        f"Sistematik yön: {direction}",
        "",
        f"Instance büyüklüğü korelasyonu: {strongest_corr}",
        "",
        "### Instance Özeti",
        "",
        _markdown_table(
            instance_summary[
                [
                    "Instance",
                    "Customers",
                    "Size Bucket",
                    "Mean_Relative_Stockout_Diff",
                    "Max_Relative_Stockout_Diff",
                    "Mean_Signed_Stockout_Diff",
                    "Runtime Speedup",
                    "Exceeds 5pct Any Domain",
                ]
            ]
        ),
        "",
        "### Korelasyonlar",
        "",
        _markdown_table(correlations),
        "",
        "## Güvenli Kullanım Kuralı",
        "",
        safe_rule,
        "",
        "## Üç Branch'e Etkisi",
        "",
        "Bu test push öncesi altyapı kontrolüdür. Bias küçük ve sistematik görünmediği için üç branch'i bloke etmeye gerek yok. Yine de nihai README/rapor sayıları full scenario ile teyit edilmeli; hızlı mod sadece keşif, debug ve aday hipotez eleme için varsayılan olabilir.",
        "",
        "## Doğru Cümle",
        "",
        f"`limit={scenario_limit}` hızlı modu bu 9-instance X40 tanı koşusunda büyük veya sistematik bir stockout bias üretmedi; ancak n=9 olduğu için bu bir kesin kanıt değil, pratik güvenlik sinyalidir.",
        "",
        "## Henüz Doğru Olmayan Cümle",
        "",
        "`limit=60` her instance ve her domain için full scenario yerine bilimsel olarak eşdeğerdir.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _skipped_row(
    instance_name: str,
    domain_name: str,
    reason: str,
    scenario_summary: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "Instance": instance_name,
        "Customers": np.nan,
        "Size Bucket": "",
        "Domain": domain_name,
        "Full Feasible": False,
        "Limited Feasible": False,
        "Reason": reason,
        **(scenario_summary or {}),
    }


def _size_bucket(customers: int) -> str:
    if customers <= 150:
        return "small"
    if customers <= 220:
        return "medium"
    return "large"


def _pearsonr(x: np.ndarray, y: np.ndarray) -> float:
    x_centered = x - x.mean()
    y_centered = y - y.mean()
    denom = math.sqrt(float(np.dot(x_centered, x_centered) * np.dot(y_centered, y_centered)))
    if denom == 0:
        return float("nan")
    return float(np.dot(x_centered, y_centered) / denom)


def _permutation_p_value(x: np.ndarray, y: np.ndarray, observed_r: float) -> float:
    n = len(y)
    if n > 9:
        rng = np.random.default_rng(123)
        count = 0
        total = 10000
        for _ in range(total):
            permuted = rng.permutation(y)
            if abs(_pearsonr(x, permuted)) >= abs(observed_r):
                count += 1
        return float((count + 1) / (total + 1))

    count = 0
    total = 0
    for permuted in itertools.permutations(y.tolist()):
        total += 1
        if abs(_pearsonr(x, np.asarray(permuted, dtype=float))) >= abs(observed_r) - 1e-12:
            count += 1
    return float(count / total) if total else float("nan")


def _bootstrap_ci(x: np.ndarray, y: np.ndarray, samples: int, seed: int) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    rs = []
    n = len(x)
    for _ in range(samples):
        idx = rng.integers(0, n, n)
        if len(np.unique(x[idx])) < 2 or len(np.unique(y[idx])) < 2:
            continue
        value = _pearsonr(x[idx], y[idx])
        if not math.isnan(value):
            rs.append(value)
    if not rs:
        return float("nan"), float("nan")
    return float(np.quantile(rs, 0.025)), float(np.quantile(rs, 0.975))


def _direction_summary(results: pd.DataFrame) -> str:
    feasible = results[(results["Full Feasible"] == True) & (results["Limited Feasible"] == True)].copy()
    if feasible.empty:
        return "no feasible comparison"
    positive = int((feasible["Signed Stockout Diff"] > 0).sum())
    negative = int((feasible["Signed Stockout Diff"] < 0).sum())
    zero = int((feasible["Signed Stockout Diff"].abs() <= 1e-12).sum())
    mean_signed = float(feasible["Signed Stockout Diff"].mean())
    return (
        f"limited-full stockout farkı {positive} domain-row'da pozitif, "
        f"{negative} domain-row'da negatif, {zero} row'da sıfır; ortalama signed fark {mean_signed:.6f}."
    )


def _strongest_correlation(correlations: pd.DataFrame) -> str:
    if correlations.empty:
        return "hesaplanamadı"
    frame = correlations.dropna(subset=["Pearson r"])
    if frame.empty:
        return "yetersiz varyasyon"
    row = frame.iloc[frame["Pearson r"].abs().argmax()]
    return (
        f"en güçlü tanı sinyali {row['Metric']} için r={row['Pearson r']:.3f}, "
        f"p={row['p-value']:.3f}, bootstrap CI=[{row['Bootstrap CI Low']:.3f}, {row['Bootstrap CI High']:.3f}], "
        f"{row['A.5 Interpretation']}."
    )


def _safe_rule(risky_count: int, risky: pd.DataFrame) -> str:
    if risky_count == 0:
        return (
            "Hızlı mod güvenli: X40 üzerinde OR-Tools anchor-feasible, küçük/orta/büyük dengeli tanı koşularında "
            "her instance için domain-maksimum göreli stockout sapması %5'in altında kaldığında keşif ve debug "
            "koşularında `--lp-planning-scenario-limit 60` kullanılabilir. Full scenario zorunlu: final README/rapor "
            "sonuçları, yayınlanacak yüzdeler ve karar verdiren karşılaştırmalar."
        )
    names = ", ".join(risky["Instance"].astype(str).tolist())
    return (
        "Hızlı mod sadece keşif için kullanılmalı. Full scenario zorunlu instance'lar: "
        f"{names}. Bu instance'larda en az bir domain %5 göreli stockout sapmasını aştı."
    )


def _markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_bool_dtype(display[col]):
            display[col] = display[col].map(lambda value: "yes" if bool(value) else "no")
        elif pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda value: "" if pd.isna(value) else f"{value:.6g}")
    headers = list(display.columns)
    rows = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in display.iterrows():
        rows.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(rows)


if __name__ == "__main__":
    main()
