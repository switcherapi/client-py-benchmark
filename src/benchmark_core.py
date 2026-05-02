""" Core benchmark helpers for SDK adapters and result summaries. """

from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Callable

import pyperf

from sdks.sdk_bench import SdkBench
from registry import AdapterRegistration

@dataclass
class BenchmarkCase:
    """ Prepared SDK benchmark state for one worker process. """

    sdk_id: str
    display_name: str
    factory: Callable[[], SdkBench]
    adapter: SdkBench | None = None

@dataclass(frozen=True)
class BenchmarkStats:
    """ Computed benchmark statistics for console reporting. """

    display_name: str
    average_seconds: float
    iterations_per_second: float
    minimum_seconds: float
    maximum_seconds: float
    p75_seconds: float
    p99_seconds: float
    p995_seconds: float

def create_benchmark_case(registration: AdapterRegistration):
    """ Create a benchmark case that will initialize lazily per worker. """
    return BenchmarkCase(
        sdk_id=registration.sdk_id,
        display_name=registration.display_name,
        factory=registration.factory,
    )

def ensure_benchmark_case_ready(benchmark_case: BenchmarkCase):
    """ Initialize the benchmark adapter once per worker before timing starts. """
    if benchmark_case.adapter is None:
        benchmark_case.adapter = benchmark_case.factory()

    return benchmark_case.adapter

def run_benchmark_case(loops, benchmark_case: BenchmarkCase):
    """ Run the SDK operation inside the pyperf timed loop. """
    adapter = ensure_benchmark_case_ready(benchmark_case)
    start = time.perf_counter()
    for _ in range(loops):
        adapter.run()
    return time.perf_counter() - start

def build_benchmark_stats(benchmark: pyperf.Benchmark):
    """ Compute the reported statistics from a pyperf benchmark result. """
    average_seconds = benchmark.mean()
    return BenchmarkStats(
        display_name=benchmark.get_name(),
        average_seconds=average_seconds,
        iterations_per_second=1 / average_seconds,
        minimum_seconds=benchmark.percentile(0),
        maximum_seconds=benchmark.percentile(100),
        p75_seconds=benchmark.percentile(75),
        p99_seconds=benchmark.percentile(99),
        p995_seconds=benchmark.percentile(99.5),
    )

def format_duration(seconds):
    """ Format a benchmark duration using ns, us, or ms units. """
    absolute_seconds = abs(seconds)
    if absolute_seconds < 1e-6:
        return f"{seconds * 1_000_000_000:.2f} ns"
    if absolute_seconds < 1e-3:
        return f"{seconds * 1_000_000:.2f} us"
    return f"{seconds * 1_000:.2f} ms"

def render_summary_table(stats: BenchmarkStats):
    """ Render the required statistics as a compact console table. """
    rows = (
        ("SDK", stats.display_name),
        ("Time/iteration (avg)", format_duration(stats.average_seconds)),
        ("Iterations/s", f"{stats.iterations_per_second:,.2f}"),
        ("Min", format_duration(stats.minimum_seconds)),
        ("Max", format_duration(stats.maximum_seconds)),
        ("p75", format_duration(stats.p75_seconds)),
        ("p99", format_duration(stats.p99_seconds)),
        ("p99.5", format_duration(stats.p995_seconds)),
    )

    left_width = max(len("Metric"), *(len(label) for label, _ in rows))
    right_width = max(len("Value"), *(len(value) for _, value in rows))

    lines = [
        "Benchmark summary",
        f"{'Metric'.ljust(left_width)}  {'Value'.rjust(right_width)}",
        f"{'-' * left_width}  {'-' * right_width}",
    ]
    lines.extend(
        f"{label.ljust(left_width)}  {value.rjust(right_width)}"
        for label, value in rows
    )
    return "\n".join(lines)
