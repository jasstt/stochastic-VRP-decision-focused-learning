from __future__ import annotations

import argparse
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
from pandas.errors import EmptyDataError


MERGE_FILES = [
    "robust_route_candidate_results.csv",
    "robust_route_candidates.csv",
    "robust_route_winners.csv",
    "robust_route_winner_full_confirmation.csv",
    "robust_route_winner_ranking_stability.csv",
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run robust route selection in parallel instance chunks, then merge the CSV outputs. "
            "Unknown arguments are forwarded to benchmark_proxy_vrp.run_robust_route_selection."
        )
    )
    parser.add_argument("--data-dir", default="benchmarks/proxy_cvrplib_x_v4")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--instances", nargs="+", default=None)
    parser.add_argument("--chunks", type=int, default=4)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--python-executable", default=sys.executable)
    parser.add_argument("--route-cache-dir", default=None)
    parser.add_argument(
        "--route-cache-mode",
        choices=["readwrite", "readonly", "writeonly", "off"],
        default="readwrite",
    )
    args, forwarded = parser.parse_known_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    instances = _select_instances(Path(args.data_dir), args.instances)
    chunks = _split_chunks(instances, args.chunks)
    route_cache_dir = Path(args.route_cache_dir) if args.route_cache_dir else out_dir / "route_cache"
    started = time.perf_counter()

    manifest_rows = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = []
        for idx, chunk in enumerate(chunks):
            chunk_out = out_dir / f"chunk_{idx:02d}"
            command = _chunk_command(
                python_executable=args.python_executable,
                data_dir=args.data_dir,
                out_dir=chunk_out,
                instances=chunk,
                route_cache_dir=route_cache_dir,
                route_cache_mode=args.route_cache_mode,
                forwarded=forwarded,
            )
            futures.append(executor.submit(_run_command, command, chunk_out))
            manifest_rows.append(
                {
                    "Chunk": idx,
                    "Instances": " ".join(chunk),
                    "Instance Count": len(chunk),
                    "Out Dir": str(chunk_out),
                    "Command": " ".join(str(part) for part in command),
                }
            )

        failures = []
        for future in as_completed(futures):
            result = future.result()
            if result["returncode"] != 0:
                failures.append(result)

    pd.DataFrame(manifest_rows).to_csv(out_dir / "chunk_manifest.csv", index=False)
    if failures:
        _write_report(out_dir, instances, chunks, route_cache_dir, time.perf_counter() - started, failures)
        raise SystemExit(f"{len(failures)} chunk(s) failed; see {out_dir / 'chunked_run_report.md'}")

    merge_summary = _merge_outputs(out_dir, len(chunks))
    _write_report(out_dir, instances, chunks, route_cache_dir, time.perf_counter() - started, [], merge_summary)
    print(f"Saved merged chunked run to {out_dir}")


def _select_instances(data_dir: Path, requested: list[str] | None) -> list[str]:
    if requested:
        return list(requested)
    return sorted(path.parent.name for path in data_dir.glob("*/instance.json"))


def _split_chunks(instances: list[str], chunk_count: int) -> list[list[str]]:
    chunk_count = max(1, min(chunk_count, len(instances)))
    chunks = [[] for _ in range(chunk_count)]
    for idx, instance in enumerate(instances):
        chunks[idx % chunk_count].append(instance)
    return [chunk for chunk in chunks if chunk]


def _chunk_command(
    *,
    python_executable: str,
    data_dir: str,
    out_dir: Path,
    instances: list[str],
    route_cache_dir: Path,
    route_cache_mode: str,
    forwarded: list[str],
) -> list[str]:
    command = [
        python_executable,
        "-m",
        "benchmark_proxy_vrp.run_robust_route_selection",
        "--data-dir",
        data_dir,
        "--out-dir",
        str(out_dir),
        "--instances",
        *instances,
        "--route-cache-dir",
        str(route_cache_dir),
        "--route-cache-mode",
        route_cache_mode,
    ]
    command.extend(forwarded)
    return command


def _run_command(command: list[str], chunk_out: Path) -> dict[str, object]:
    chunk_out.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    completed = subprocess.run(command, cwd=Path.cwd(), text=True, capture_output=True)
    (chunk_out / "chunk_stdout.log").write_text(completed.stdout, encoding="utf-8")
    (chunk_out / "chunk_stderr.log").write_text(completed.stderr, encoding="utf-8")
    return {
        "returncode": completed.returncode,
        "runtime_sec": time.perf_counter() - started,
        "chunk_out": str(chunk_out),
    }


def _merge_outputs(out_dir: Path, chunk_count: int) -> list[dict[str, object]]:
    rows = []
    for filename in MERGE_FILES:
        frames = []
        for idx in range(chunk_count):
            path = out_dir / f"chunk_{idx:02d}" / filename
            if path.exists():
                try:
                    frame = pd.read_csv(path)
                except EmptyDataError:
                    continue
                frame["Source Chunk"] = idx
                frames.append(frame)
        if not frames:
            rows.append({"File": filename, "Rows": 0, "Status": "missing"})
            continue
        merged = pd.concat(frames, ignore_index=True)
        merged.to_csv(out_dir / filename, index=False)
        rows.append({"File": filename, "Rows": len(merged), "Status": "merged"})
    pd.DataFrame(rows).to_csv(out_dir / "chunk_merge_summary.csv", index=False)
    return rows


def _write_report(
    out_dir: Path,
    instances: list[str],
    chunks: list[list[str]],
    route_cache_dir: Path,
    runtime_sec: float,
    failures: list[dict[str, object]],
    merge_summary: list[dict[str, object]] | None = None,
) -> None:
    lines = [
        "# Parallel Robust Route Selection Chunk Run",
        "",
        f"- Instances: {len(instances)}",
        f"- Chunks: {len(chunks)}",
        f"- Route cache dir: `{route_cache_dir}`",
        f"- Wall runtime sec: {runtime_sec:.2f}",
        "",
        "## Chunk Sizes",
        "",
        _markdown_table(pd.DataFrame({"Chunk": list(range(len(chunks))), "Instance Count": [len(c) for c in chunks]})),
        "",
    ]
    if failures:
        lines.extend(["## Failures", "", _markdown_table(pd.DataFrame(failures)), ""])
    if merge_summary is not None:
        lines.extend(["## Merged Outputs", "", _markdown_table(pd.DataFrame(merge_summary)), ""])
    out_dir.joinpath("chunked_run_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    display = df.copy()
    rows = [
        "| " + " | ".join(str(col) for col in display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        rows.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(rows)


if __name__ == "__main__":
    main()
