#!/usr/bin/env python3
"""Wall-clock benchmarks for parallel guardrail engines (local, no HTTP).

Run from repository root::

    python scripts/bench_guardrails.py

Uses ``time.perf_counter`` over N iterations; reports min / p50 / p95 / max in ms.
Numbers are **machine-specific** — use for relative comparison and regression
detection, not SLA claims.

Source: https://dev.to/conwayresearch/comment/35p1m · GitHub #9.
"""

from __future__ import annotations

import argparse
import asyncio
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

TEXT_SHORT = "What is the refund policy?"
TEXT_LONG = " ".join([TEXT_SHORT] * 50)
OUTPUT_SHORT = "Refunds are available within 30 days with a receipt."
OUTPUT_LONG = " ".join([OUTPUT_SHORT] * 40)


async def bench_input(label: str, text: str, n: int) -> None:
    from agentguard.input_guardrails.engine import evaluate_input

    times: list[float] = []
    for _ in range(n):
        t0 = time.perf_counter()
        await evaluate_input(text)
        times.append((time.perf_counter() - t0) * 1000)
    times.sort()
    p50 = statistics.median(times)
    p95 = times[max(0, int(0.95 * (len(times) - 1)))]
    print(
        f"evaluate_input[{label}] n={n} "
        f"p50={p50:.2f}ms p95={p95:.2f}ms min={min(times):.2f}ms max={max(times):.2f}ms"
    )


async def bench_output(label: str, text: str, ctx: str, n: int) -> None:
    from agentguard.output_validation.engine import validate_output

    times: list[float] = []
    for _ in range(n):
        t0 = time.perf_counter()
        await validate_output(text, context_text=ctx)
        times.append((time.perf_counter() - t0) * 1000)
    times.sort()
    p50 = statistics.median(times)
    p95 = times[max(0, int(0.95 * (len(times) - 1)))]
    print(
        f"validate_output[{label}] n={n} "
        f"p50={p50:.2f}ms p95={p95:.2f}ms min={min(times):.2f}ms max={max(times):.2f}ms"
    )


async def main() -> None:
    p = argparse.ArgumentParser(description="Benchmark guardrail engines")
    p.add_argument("-n", type=int, default=40, help="iterations per scenario")
    args = p.parse_args()
    n = max(5, args.n)
    await bench_input("short", TEXT_SHORT, n)
    await bench_input("long", TEXT_LONG, n)
    await bench_output("short", OUTPUT_SHORT, OUTPUT_SHORT, n)
    await bench_output("long", OUTPUT_LONG, OUTPUT_SHORT, n)


if __name__ == "__main__":
    asyncio.run(main())
