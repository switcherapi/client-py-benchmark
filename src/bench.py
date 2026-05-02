""" CLI entrypoint for running a single SDK benchmark with pyperf. """

from __future__ import annotations

import argparse
import sys

import pyperf

from benchmark_core import (
    build_benchmark_stats,
    create_benchmark_case,
    render_summary_table,
    run_benchmark_case,
)
from registry import get_adapter_registration, list_adapter_registrations

def build_parser():
    """ Create the CLI parser for custom benchmark arguments. """
    parser = argparse.ArgumentParser(
        prog="python src\\bench.py",
        description="Benchmark a single Client SDK package per invocation.",
        add_help=False,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "pyperf runner arguments are also supported. Example:\n"
            "  python src\\bench.py --sdk switcher-client --processes 10 --values 5"
        ),
    )
    parser.add_argument("--sdk", help="Registered SDK adapter ID to benchmark.")
    parser.add_argument(
        "--list-sdks",
        action="store_true",
        help="List the registered SDK benchmark adapters.",
    )
    parser.add_argument(
        "-h",
        "--help",
        action="store_true",
        help="Show this help message.",
    )
    return parser

def format_available_sdks():
    """ Render the registered SDK adapters for console output. """
    lines = ["Registered SDK adapters:"]
    for registration in list_adapter_registrations():
        lines.append(f"  {registration.sdk_id} - {registration.display_name}")
    return "\n".join(lines)

def main(argv=None):
    """ Run the requested SDK benchmark and render a console summary. """
    parser = build_parser()
    cli_args, pyperf_args = parser.parse_known_args(argv)

    if cli_args.help:
        print(parser.format_help())
        print(format_available_sdks())
        return 0

    if cli_args.list_sdks:
        print(format_available_sdks())
        return 0

    if not cli_args.sdk:
        parser.error("--sdk is required unless --list-sdks is used.")
        return 1

    registration = get_adapter_registration(cli_args.sdk)

    runner = pyperf.Runner(
        program_args=[sys.argv[0], "--sdk", registration.sdk_id],
        metadata={"sdk": registration.sdk_id},
    )
    runner.parse_args(pyperf_args)

    benchmark_case = create_benchmark_case(registration)
    benchmark = runner.bench_time_func(
        registration.display_name,
        run_benchmark_case,
        benchmark_case,
        inner_loops=1,
        metadata={"sdk_display_name": registration.display_name},
    )

    if benchmark is not None and not runner.args.worker and benchmark.get_nvalue(): # type: ignore
        print()
        print(render_summary_table(build_benchmark_stats(benchmark)))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
