from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd

from .cvrplib import customer_view, load_instance_json
from .ortools_baselines import build_plans, vehicle_count_from_name
from .routing_providers import OrToolsProvider, VroomProvider, instance_to_provider_inputs
from .routing_providers.base import RouteSet


PROVIDERS = ("ortools", "vroom")
PROVIDER_LABELS = {"ortools": "OR-Tools", "vroom": "VROOM"}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Diagnose capacity-utilization and vehicle-count explanations for stockout ranking shifts."
    )
    parser.add_argument("--data-dir", default="benchmarks/proxy_cvrplib_n20")
    parser.add_argument("--manifest", default="benchmarks/proxy_cvrplib_n20/manifest.csv")
    parser.add_argument(
        "--ortools-results",
        default="benchmarks/proxy_cvrplib_n20/domain_engine_results_ortools_provider.csv",
    )
    parser.add_argument(
        "--vroom-results",
        default="benchmarks/proxy_cvrplib_n20/domain_engine_results_vroom_provider.csv",
    )
    parser.add_argument("--out-dir", default=".")
    parser.add_argument("--anchor-plan", default="proxy_mean_or_tools")
    parser.add_argument("--fallback-anchor-plan", default="nominal_or_tools")
    parser.add_argument("--time-limit-sec", type=int, default=5)
    parser.add_argument("--vroom-url", default="http://localhost:3000")
    parser.add_argument("--bootstrap-samples", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=42)
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
    utilization = _capacity_utilization_metrics(route_sets)
    vehicle_diff = _vehicle_count_diff(utilization)
    stockout = _stockout_diffs(args.ortools_results, args.vroom_results)
    analysis = _analysis_frame(utilization, vehicle_diff, stockout)
    correlations = _correlation_tests(
        analysis,
        bootstrap_samples=args.bootstrap_samples,
        seed=args.seed,
    )
    leverage = _leverage_control(analysis)
    leave_one_out = _leave_one_out_if_needed(
        analysis,
        leverage,
        bootstrap_samples=args.bootstrap_samples,
        seed=args.seed + 1000,
    )
    audit = _dataset_audit(args.manifest)

    utilization.to_csv(out_dir / "capacity_utilization_metrics.csv", index=False)
    vehicle_diff.to_csv(out_dir / "vehicle_count_diff.csv", index=False)
    correlations.to_csv(out_dir / "stockout_mechanism_correlations.csv", index=False)
    leverage.to_csv(out_dir / "stockout_mechanism_leverage.csv", index=False)
    leave_one_out.to_csv(out_dir / "stockout_mechanism_leave_one_out.csv", index=False)
    audit.to_csv(out_dir / "stockout_mechanism_dataset_audit.csv", index=False)
    _write_report(
        out_dir / "stockout_mechanism_diagnosis_report.md",
        audit=audit,
        utilization=utilization,
        vehicle_diff=vehicle_diff,
        correlations=correlations,
        leverage=leverage,
        leave_one_out=leave_one_out,
    )

    print("Capacity utilization metrics")
    print(utilization.to_string(index=False))
    print("\nVehicle count diff")
    print(vehicle_diff.to_string(index=False))
    print("\nCorrelation tests")
    print(correlations.to_string(index=False))
    print("\nLeverage")
    print(leverage.to_string(index=False))
    if not leave_one_out.empty:
        print("\nLeave-one-out")
        print(leave_one_out.to_string(index=False))
    print("\nDataset audit")
    print(audit.to_string(index=False))


def _capacity_utilization_metrics(route_sets: dict[str, dict[str, tuple[object, RouteSet]]]) -> pd.DataFrame:
    rows = []
    for instance_name, provider_data in route_sets.items():
        for provider in PROVIDERS:
            instance, route_set = provider_data[provider]
            route_utils = _route_utilizations(instance, route_set)
            active_vehicle_count = len(route_utils)
            rows.append(
                {
                    "Instance": instance_name,
                    "Provider": PROVIDER_LABELS[provider],
                    "Mean Util": float(np.mean(route_utils)) if route_utils else np.nan,
                    "Util Variance": float(np.var(route_utils, ddof=1)) if len(route_utils) > 1 else 0.0,
                    "Max Util": float(np.max(route_utils)) if route_utils else np.nan,
                    "Active Vehicle Count": active_vehicle_count,
                    "Feasible": bool(route_set.feasible),
                }
            )
    return pd.DataFrame(rows).sort_values(["Instance", "Provider"])


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
            "ortools": (
                instance,
                _solve_anchor(
                    instance,
                    plans,
                    anchor_plan,
                    fallback_anchor_plan,
                    "ortools",
                    time_limit_sec,
                    vroom_url,
                ),
            ),
            "vroom": (
                instance,
                _solve_anchor(
                    instance,
                    plans,
                    anchor_plan,
                    fallback_anchor_plan,
                    "vroom",
                    time_limit_sec,
                    vroom_url,
                ),
            ),
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


def _route_utilizations(instance: object, route_set: RouteSet) -> list[float]:
    if not route_set.feasible:
        return []
    _, customer_indices = customer_view(instance)
    customers = set(int(node) for node in customer_indices)
    utilizations = []
    for route in route_set.routes:
        route_load = sum(float(instance.demands[int(node)]) for node in route if int(node) in customers)
        if route_load > 0:
            utilizations.append(route_load / float(instance.capacity))
    return utilizations


def _vehicle_count_diff(utilization: pd.DataFrame) -> pd.DataFrame:
    counts = utilization.pivot(index="Instance", columns="Provider", values="Active Vehicle Count").reset_index()
    counts["Diff"] = counts["OR-Tools"] - counts["VROOM"]
    return counts[["Instance", "OR-Tools", "VROOM", "Diff"]].sort_values("Instance")


def _analysis_frame(utilization: pd.DataFrame, vehicle_diff: pd.DataFrame, stockout: pd.DataFrame) -> pd.DataFrame:
    util_pivot = utilization.pivot(index="Instance", columns="Provider", values="Mean Util").reset_index()
    util_pivot["capacity_utilization_diff"] = util_pivot["OR-Tools"] - util_pivot["VROOM"]
    data = stockout.merge(
        util_pivot[["Instance", "capacity_utilization_diff"]],
        on="Instance",
        how="left",
    ).merge(
        vehicle_diff[["Instance", "Diff"]].rename(columns={"Diff": "vehicle_count_diff"}),
        on="Instance",
        how="left",
    )
    return data


def _correlation_tests(analysis: pd.DataFrame, bootstrap_samples: int, seed: int) -> pd.DataFrame:
    rows = []
    rng = np.random.default_rng(seed)
    predictors = [
        ("capacity_utilization_diff", "Capacity Util Diff"),
        ("vehicle_count_diff", "Vehicle Count Diff"),
    ]
    for domain, group in analysis.groupby("Domain"):
        for column, label in predictors:
            x = group[column].to_numpy(float)
            y = group["stockout_diff_signed"].to_numpy(float)
            unique_x = _unique_level_count(x)
            if len(group) < 15:
                evidence = "diagnostic_signal_n_lt_15"
                r, p_value = _pearson(x, y)
                ci_low, ci_high = _bootstrap_ci(x, y, bootstrap_samples, rng)
            elif unique_x < 3:
                evidence = "insufficient_x_variation"
                r, p_value, ci_low, ci_high = np.nan, np.nan, np.nan, np.nan
            else:
                r, p_value = _pearson(x, y)
                ci_low, ci_high = _bootstrap_ci(x, y, bootstrap_samples, rng)
                evidence = _evidence_label(r, p_value, ci_low, ci_high)
            rows.append(
                {
                    "Domain": domain,
                    "Predictor": label,
                    "n": len(group),
                    "Unique x Levels": unique_x,
                    "Pearson r": r,
                    "p-value": p_value,
                    "Bootstrap CI Low": ci_low,
                    "Bootstrap CI High": ci_high,
                    "CI Contains Zero": _ci_contains_zero(ci_low, ci_high),
                    "Evidence Label": evidence,
                }
            )
    return pd.DataFrame(rows).sort_values(["Domain", "Predictor"])


def _bootstrap_ci(x: np.ndarray, y: np.ndarray, samples: int, rng: np.random.Generator) -> tuple[float, float]:
    if len(x) < 3:
        return float("nan"), float("nan")
    values = []
    n = len(x)
    for _ in range(samples):
        idx = rng.integers(0, n, n)
        sample_x = x[idx]
        sample_y = y[idx]
        if _unique_level_count(sample_x) < 2 or np.allclose(sample_y, sample_y[0]):
            continue
        r, _ = _pearson(sample_x, sample_y)
        if np.isfinite(r):
            values.append(r)
    if not values:
        return float("nan"), float("nan")
    return float(np.percentile(values, 2.5)), float(np.percentile(values, 97.5))


def _evidence_label(r: float, p_value: float, ci_low: float, ci_high: float) -> str:
    if not np.isfinite(r) or not np.isfinite(p_value) or not np.isfinite(ci_low) or not np.isfinite(ci_high):
        return "not_estimable"
    if _ci_contains_zero(ci_low, ci_high):
        return "no_correlation_ci_crosses_zero"
    if p_value < 0.05:
        return "candidate_mechanism"
    return "directional_signal_ci_excludes_zero_but_p_ge_0_05"


def _ci_contains_zero(ci_low: float, ci_high: float) -> bool:
    if not np.isfinite(ci_low) or not np.isfinite(ci_high):
        return False
    return ci_low <= 0.0 <= ci_high


def _leverage_control(analysis: pd.DataFrame) -> pd.DataFrame:
    rows = []
    predictors = [
        ("capacity_utilization_diff", "Capacity Util Diff"),
        ("vehicle_count_diff", "Vehicle Count Diff"),
    ]
    for domain, group in analysis.groupby("Domain"):
        group = group.sort_values("Instance")
        for column, label in predictors:
            x = group[column].to_numpy(float)
            y = group["stockout_diff_signed"].to_numpy(float)
            n = len(group)
            cook_threshold = 4.0 / n if n else np.nan
            severe_threshold = 3.0 * cook_threshold if n else np.nan
            if _unique_level_count(x) < 2 or np.allclose(y, y[0]):
                leverage = np.full(n, np.nan)
                cooks = np.full(n, np.nan)
                residuals = np.full(n, np.nan)
            else:
                leverage, cooks, residuals = _ols_influence(x, y)
            for idx, row in enumerate(group.itertuples(index=False)):
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


def _ols_influence(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    design = np.column_stack([np.ones(len(x)), x])
    beta = np.linalg.lstsq(design, y, rcond=None)[0]
    fitted = design @ beta
    residuals = y - fitted
    hat = design @ np.linalg.pinv(design.T @ design) @ design.T
    leverage = np.diag(hat)
    p = design.shape[1]
    dof = len(x) - p
    mse = float(residuals @ residuals / dof) if dof > 0 else np.nan
    if not np.isfinite(mse) or np.isclose(mse, 0.0):
        cooks_distance = np.full(len(x), np.nan)
    else:
        cooks_distance = (residuals**2 / (p * mse)) * leverage / ((1.0 - leverage) ** 2)
    return leverage, cooks_distance, residuals


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
    for key, group_flags in flagged.groupby(["Domain", "Predictor"]):
        domain, predictor = key
        top = group_flags.sort_values("Cook's Distance", ascending=False).iloc[0]
        column = "capacity_utilization_diff" if predictor == "Capacity Util Diff" else "vehicle_count_diff"
        reduced = analysis[(analysis["Domain"] == domain) & (analysis["Instance"] != top["Instance"])]
        x = reduced[column].to_numpy(float)
        y = reduced["stockout_diff_signed"].to_numpy(float)
        unique_x = _unique_level_count(x)
        if len(reduced) < 15:
            evidence = "diagnostic_signal_n_lt_15"
            r, p_value = _pearson(x, y)
            ci_low, ci_high = _bootstrap_ci(x, y, bootstrap_samples, rng)
        elif unique_x < 3:
            evidence = "insufficient_x_variation"
            r, p_value, ci_low, ci_high = np.nan, np.nan, np.nan, np.nan
        else:
            r, p_value = _pearson(x, y)
            ci_low, ci_high = _bootstrap_ci(x, y, bootstrap_samples, rng)
            evidence = _evidence_label(r, p_value, ci_low, ci_high)
        rows.append(
            {
                "Domain": domain,
                "Predictor": predictor,
                "Dropped Instance": top["Instance"],
                "n": len(reduced),
                "Unique x Levels": unique_x,
                "Pearson r": r,
                "p-value": p_value,
                "Bootstrap CI Low": ci_low,
                "Bootstrap CI High": ci_high,
                "CI Contains Zero": _ci_contains_zero(ci_low, ci_high),
                "Evidence Label": evidence,
            }
        )
    return pd.DataFrame(rows).sort_values(["Domain", "Predictor"])


def _dataset_audit(manifest_path: str) -> pd.DataFrame:
    manifest = pd.read_csv(manifest_path)
    manifest["family"] = manifest["name"].astype(str).str[0]
    manifest["size_bucket"] = manifest["nodes"].map(_size_bucket)
    rows = []
    rows.extend(_audit_category(manifest, "family"))
    rows.extend(_audit_category(manifest, "size_bucket"))
    out = pd.DataFrame(rows)
    out["A.5 <=25%"] = out["Share"] <= 0.25
    return out.sort_values(["Category Type", "Category"])


def _audit_category(manifest: pd.DataFrame, column: str) -> list[dict[str, object]]:
    total = len(manifest)
    rows = []
    for category, count in manifest[column].value_counts().sort_index().items():
        rows.append(
            {
                "Category Type": column,
                "Category": category,
                "Count": int(count),
                "Total": int(total),
                "Share": float(count / total) if total else np.nan,
            }
        )
    return rows


def _size_bucket(nodes: int) -> str:
    if int(nodes) < 20:
        return "small_n_lt_20"
    if int(nodes) <= 50:
        return "medium_20_50"
    return "large_51_99"


def _unique_level_count(values: np.ndarray) -> int:
    finite = values[np.isfinite(values)]
    return int(len(np.unique(np.round(finite, 12))))


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


def _pearson(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    finite = np.isfinite(x) & np.isfinite(y)
    x = x[finite]
    y = y[finite]
    n = len(x)
    if n < 3 or np.allclose(x, x[0]) or np.allclose(y, y[0]):
        return float("nan"), float("nan")
    x_centered = x - x.mean()
    y_centered = y - y.mean()
    denom = math.sqrt(float(np.sum(x_centered**2) * np.sum(y_centered**2)))
    if np.isclose(denom, 0.0):
        return float("nan"), float("nan")
    r = float(np.sum(x_centered * y_centered) / denom)
    r = max(-1.0, min(1.0, r))
    if abs(r) >= 1.0:
        return r, 0.0
    df = n - 2
    t_squared = (r * r * df) / max(1.0e-15, 1.0 - r * r)
    x_beta = df / (df + t_squared)
    p_value = _regularized_incomplete_beta(x_beta, 0.5 * df, 0.5)
    return r, float(max(0.0, min(1.0, p_value)))


def _regularized_incomplete_beta(x: float, a: float, b: float) -> float:
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    log_bt = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log1p(-x)
    bt = math.exp(log_bt)
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _beta_continued_fraction(a, b, x) / a
    return 1.0 - bt * _beta_continued_fraction(b, a, 1.0 - x) / b


def _beta_continued_fraction(a: float, b: float, x: float) -> float:
    max_iter = 200
    eps = 3.0e-14
    tiny = 1.0e-300
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


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


def _write_report(
    path: Path,
    audit: pd.DataFrame,
    utilization: pd.DataFrame,
    vehicle_diff: pd.DataFrame,
    correlations: pd.DataFrame,
    leverage: pd.DataFrame,
    leave_one_out: pd.DataFrame,
) -> None:
    n_instances = int(vehicle_diff["Instance"].nunique())
    failed_audit = audit[~audit["A.5 <=25%"]]
    candidate_rows = correlations[correlations["Evidence Label"] == "candidate_mechanism"]
    ci_cross_rows = correlations[correlations["Evidence Label"] == "no_correlation_ci_crosses_zero"]
    insufficient_rows = correlations[correlations["Evidence Label"] == "insufficient_x_variation"]
    severe = leverage[leverage["Severe Cook Flag"]]
    mechanism_found = not candidate_rows.empty

    if mechanism_found:
        a8_update = "\n".join(
            [
                "A.8'deki acik soru kismen cevaplandi: asagidaki mekanizma adaylari A.5 kosullarinda bootstrap CI sifiri dislamistir:",
                _markdown_table(
                    candidate_rows[
                        [
                            "Domain",
                            "Predictor",
                            "n",
                            "Pearson r",
                            "p-value",
                            "Bootstrap CI Low",
                            "Bootstrap CI High",
                            "Evidence Label",
                        ]
                    ]
                ),
            ]
        )
        correct_sentence = (
            "Capacity utilization veya vehicle count farki, en az bir domain icin stockout farkina aday aciklayici "
            "mekanizma olarak gorulmustur; ancak dataset denge uyarilari nedeniyle genelleme sinirlidir."
        )
        next_step = (
            "Aday mekanizma bulunan domainlerde ayni testi daha dengeli X/v3 secimiyle tekrarla; sonra route-level "
            "load allocation farkini ayni A.5 denetimleriyle test et."
        )
    else:
        a8_update = (
            "Capacity utilization ve vehicle count farki da stockout siralamasini aciklamiyor. "
            "Kalan adaylar (load allocation, objective interaction) icin ayri calisma gerekir. "
            "A.8 acik kalmaya devam ediyor."
        )
        correct_sentence = (
            "Bu n=20 tani kosusunda capacity utilization farki ve aktif arac sayisi farki, stockout siralamasinin "
            "motora gore neden degistigini A.5 standartlarinda aciklamadi."
        )
        next_step = (
            "Route-level load allocation farkini test eden bir sonraki tani calismasini kur: rota basina yuk payi, "
            "route-level shortfall contribution ve domain objective bilesenlerini OR-Tools/VROOM farki olarak olc."
        )

    if failed_audit.empty:
        audit_sentence = (
            f"Veri seti n={n_instances} ve raporlanan kategori auditinde hicbir kategori %25 sinirini asmiyor."
        )
    else:
        audit_sentence = (
            f"Veri seti n={n_instances}; ancak mevcut repo icinde X/v3 secimi bulunmadigi icin hazir n=20 set kullanildi. "
            "Kategori auditinde %25 sinirini asan gruplar var. Bu nedenle sonuc A.5'in n, x-seviyesi, bootstrap ve "
            "leverage disiplinini uygular; fakat stratification maddesi icin sinirli okunmalidir."
        )

    if severe.empty:
        leverage_text = "Cook's Distance kontrolunde 3x(4/n) esigini asan domine edici instance gorulmedi."
        loo_text = ""
    else:
        leverage_text = (
            "Cook's Distance kontrolunde 3x(4/n) esigini asan instance-predictor-domain kombinasyonlari bulundu. "
            "Bu satirlar icin leave-one-out testi de raporlandi."
        )
        loo_text = "\n\nLeave-one-out sonucu:\n\n" + _markdown_table(
            leave_one_out[
                [
                    "Domain",
                    "Predictor",
                    "Dropped Instance",
                    "n",
                    "Unique x Levels",
                    "Pearson r",
                    "p-value",
                    "Bootstrap CI Low",
                    "Bootstrap CI High",
                    "Evidence Label",
                ]
            ]
        )

    text = f"""# Stockout Mechanism Diagnosis Report

## Test Edilen Hipotezler

1. Capacity utilization farki -> stockout farkini acikliyor mu?
2. Vehicle count / aktif rota sayisi farki -> stockout farkini acikliyor mu?

Bu turda route-level load allocation ve objective interaction test edilmedi; bunlar A.8'in kalan adaylari olarak bir sonraki tura birakildi.

## Veri Seti ve A.5 Kontrolu

{audit_sentence}

{_markdown_table(audit)}

## Capacity Utilization ve Vehicle Count Ciktilari

Capacity utilization rota bazinda `toplam rota talebi / arac kapasitesi` olarak hesaplandi; instance seviyesinde ortalama, varyans ve maksimum raporlandi.

{_markdown_table(utilization[["Instance", "Provider", "Mean Util", "Util Variance", "Max Util", "Active Vehicle Count"]])}

Aktif arac sayisi farki:

{_markdown_table(vehicle_diff)}

## Bulgular

A.5 kurallari uygulandi: n<15 ise tani sinyali, x degiskeninde en az 3 farkli seviye yoksa korelasyon raporlanmadi, bootstrap CI sifiri kapsiyorsa "korelasyon yok" olarak isaretlendi.

{_markdown_table(correlations)}

Bu kosuda {len(candidate_rows)} aday mekanizma satiri bulundu. {len(ci_cross_rows)} satirda bootstrap CI sifiri kapsadigi icin korelasyon yok dendi; {len(insufficient_rows)} satirda x varyasyonu yetersiz oldugu icin korelasyon raporlanmadi.

Onemli teknik ayrim: mean utilization farkinin sifira dusmesi beklenebilir. Iki motor ayni toplam talebi ayni aktif arac sayisina boldugunde instance-level ortalama doluluk matematiksel olarak ayni kalir. Buna ragmen `Util Variance` ve `Max Util` satirlarinda farklar goruluyor; bu farklar bu turun mean-utilization hipotezinden cok route-level load allocation adayina aittir ve bir sonraki tani calismasinda ayrica test edilmelidir.

## Leverage Kontrolu

{leverage_text}

{_markdown_table(leverage[["Domain", "Predictor", "Instance", "Cook's Distance", "Cook Threshold 4/n", "Severe Threshold 3x", "Severe Cook Flag"]])}{loo_text}

## A.8'in Guncellenmis Hali

{a8_update}

## Dogru Cumle

{correct_sentence}

## Henuz Dogru Olmayan Cumle

"Stockout siralamasinin motora gore degismesi capacity utilization farkindan veya aktif arac sayisi farkindan kaynaklanir."

## Sonraki Adim

{next_step}
"""
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
