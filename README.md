# About

This benchmark compares major Feature Flag SDKs against Switcher Client SDK for Python.<br>
Tests included in this benchmark are focused only on raw performance and do not reflect nor measure any other specific SDK capabilities.<br>
The goal is to gain more knowledge and define a baseline to improve Switcher Client SDK overall performance in the future releases.

## What is being measured

Each benchmark adapter represents one SDK package and one evaluation style:

| SDK | Strategy | What the timed call does |
| --- | --- | --- |
| `static-bool` | Local baseline | Reads a static environment-backed boolean |
| `switcher-client` | Local snapshot | Evaluates a flag loaded from remote API to an in-memory snapshot |
| `switcher-client (throttle)` | Local snapshot | Evaluates a flag loaded from remote API using inteligent throttling |
| `harness-featureflags` | Async initialization + local eval | Waits for initialization, then evaluates a boolean flag |
| `unleash-client` | Local cache | Evaluates a toggle from a pre-seeded cache |
| `optimizely-sdk` | SDK-managed data + local eval | Decides a feature for a prepared user context |
| `amplitude-experiment` | Local evaluation | Evaluates a local experiment flag for a prepared user |
| `splitio-client` | Static file | Evaluates a treatment from a pre-seeded Split.io static file |

## Benchmark approach

The runner uses `pyperf` to reduce noise and report stable statistics.

1. A single SDK adapter is selected with `--sdk`.
2. The adapter is created once per worker process.
3. The benchmark loop calls `run()` repeatedly.
4. `pyperf` aggregates multiple samples and reports summary metrics.

This keeps the comparison centered on **raw per-call evaluation performance**, which is the part most affected by SDK optimization choices such as local caches, snapshots, polling, streaming, and preloaded configuration.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

List supported SDK adapters:

```bash
python .\src\bench.py --list-sdks
```

Run one benchmark:

```bash
python .\src\bench.py --sdk switcher-client --processes 1 --values 5 --warmups 1 --min-time 1.0
```

The repository also includes convenience targets in `Makefile` for each SDK.

## Test settings

Current benchmark commands use these settings:

| Parameter | Example | Meaning |
| --- | --- | --- |
| `--sdk` | `switcher-client` | Selects which adapter/package to benchmark |
| `--processes` | `1` | Number of worker processes used by `pyperf`; more processes can reduce single-process bias but increase run time |
| `--values` | `5` | Number of measured values collected per worker; higher values usually improve confidence but take longer |
| `--warmups` | `1` | Number of warmup runs before measured samples; helps reduce cold-start distortion |
| `--min-time` | `1.0` | Minimum duration target for each sample in seconds; `pyperf` adjusts loop counts so each sample runs long enough to be meaningful |

## Reported metrics

The console summary produced by the benchmark includes:

| Metric | Meaning |
| --- | --- |
| `Time/iteration (avg)` | Average time spent per evaluation call |
| `Iterations/s` | Throughput in evaluations per second |
| `Min` | Fastest observed sample |
| `Max` | Slowest observed sample |
| `p75` | 75th percentile latency |
| `p99` | 99th percentile latency |
| `p99.5` | 99.5th percentile latency |

## Results

| SDK | Avg time/iteration | Iterations/s | Min | Max | p75 | p99 | p99.5 | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| static-bool | 201.83 ns | 4,954,621.25 | 201.46 ns | 202.08 ns | 202.04 ns | 202.08 ns | 202.08 ns | Mean +- std dev: 202 ns +- 0 ns |
| switcher-client (throttle) | 384.33 ns | 2,601,955.35 | 382.37 ns | 386.90 ns | 384.41 ns | 386.80 ns | 386.85 ns | Mean +- std dev: 384 ns +- 2 ns |
| switcher-client | 1.07 us | 937,193.29 | 1.06 us | 1.08 us | 1.07 us | 1.08 us | 1.08 us | Mean +- std dev: 1.07 us +- 0.01 us |
| harness-featureflags | 2.39 us | 417,896.17 | 2.39 us | 2.40 us | 2.39 us | 2.40 us | 2.40 us | Mean +- std dev: 2.39 us +- 0.00 us |
| unleash-client | 12.01 us | 83,289.10 | 11.99 us | 12.04 us | 12.02 us | 12.04 us | 12.04 us | Mean +- std dev: 12.0 us +- 0.0 us |
| amplitude-experiment | 21.35 us | 46,834.03 | 21.19 us | 21.79 us | 21.35 us | 21.78 us | 21.78 us | Mean +- std dev: 21.4 us +- 0.3 us |
| optimizely-sdk | 23.30 us | 42,917.41 | 23.04 us | 23.46 us | 23.46 us | 23.46 us | 23.46 us | Mean +- std dev: 23.3 us +- 0.2 us |
| splitio-client | 27.97 us | 35,751.92 | 27.78 us | 28.14 us | 28.13 us | 28.14 us | 28.14 us | Mean +- std dev: 28.0 us +- 0.2 us |

## Package footprint

The following package size metrics were collected per SDK package using `pip-weigh`:

| Package | Version | Total Size | Self Size |
| --- | --- | --- | --- |
| amplitude-experiment | 1.11.0 | 1.4 MB | 294.7 KB |
| switcher-client | 1.0.0 | 2.4 MB | 120.4 KB |
| splitio-client | 10.6.0 | 3.4 MB | 1.1 MB |
| harness-featureflags | 1.7.5 | 4.1 MB | 354.6 KB |
| optimizely-sdk | 5.5.0 | 4.1 MB | 729.1 KB |
| unleash-client | 6.7.0 | 10.3 MB | 126.7 KB |
