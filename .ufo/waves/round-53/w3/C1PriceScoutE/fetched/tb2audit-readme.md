SOURCE-URL: https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/main/README.md
# Terminal-Bench 2 Audit

Tools for auditing and improving test coverage quality across the 89 challenges in Terminal-Bench 2.0.  See https://jonathanpgabor.substack.com/p/every-benchmark-is-broken for background.

## Overview

This repository contains:

- **`test_audit.py`** — Audits each challenge's test suite by sending the task description, container filesystem state, test code, and reference solution to an LLM, which rates coverage from 1-5.
- **`harden_tests.py`** — Takes audit results and generates improved tests for challenges that scored below a threshold.
- **`terminal_bench_2.py`** — The Inspect AI evaluation task definition for running Terminal-Bench 2.0 challenges.

## Setup

Requires Python 3.12+. Install dependencies with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

Set API keys for your chosen provider:

```bash
export ANTHROPIC_API_KEY=...
# or
export OPENAI_API_KEY=...
```

Docker must be running, as the audit tool pulls and inspects challenge container images.

## Usage

### Auditing Tests

```bash
# Audit all challenges using Claude
uv run python test_audit.py --provider anthropic

# Audit all challenges using GPT
uv run python test_audit.py --provider openai

# Audit a specific challenge
uv run python test_audit.py --challenge chess-best-move --provider anthropic

# Audit first 10 challenges with 4 parallel workers
uv run python test_audit.py --limit 10 --parallel 4 --provider anthropic
```

Results are saved to a timestamped directory under `audit_results/` containing:

| File | Description |
|------|-------------|
| `audit.txt` | Full LLM feedback for each challenge |
| `prompts.txt` | Prompts sent to the auditor |
| `ratings.json` | `{challenge_name: rating}` dictionary |
| `stats.json` | Summary statistics (average, distribution, etc.) |

### Hardening Tests

After an audit run, improve tests that scored at or below a threshold:

```bash
# Harden tests rated 3 or below (default threshold)
uv run python harden_tests.py --audit-dir audit_results/20260120_125158 --provider anthropic

# Use a stricter threshold
uv run python harden_tests.py --audit-dir audit_results/20260120_125158 --threshold 2 --provider anthropic
```

Results are saved to a timestamped directory under `harden_results/`.

### Running the Benchmark

The evaluation uses [Inspect AI](https://inspect.ai-safety-institute.org.uk/):

```bash
inspect eval terminal_bench_2.py
```

See `TERMINALBENCH.md` for full benchmark documentation.

## Challenge Structure

Each of the 89 challenges lives under `challenges/` with the following layout:

```
challenges/<name>/
├── eval.yaml              # Task description and variants
├── compose.yaml           # Docker container specification
├── tests/
│   ├── test_outputs.py    # Python test suite
│   └── test.sh            # Test runner script
└── solution/
    └── solve.sh           # Reference solution
```

## How the Audit Works

For each challenge, the auditor:

1. Reads the task description from `eval.yaml`
2. Pulls the Docker image and inspects the container filesystem (directory tree + key file contents)
3. Reads the test suite (`test_outputs.py` and any helper files)
4. Reads the reference solution (`solve.sh`)
5. Sends everything to an LLM with a prompt asking it to evaluate test coverage quality
6. Extracts a 1-5 rating from the response

The LLM rates coverage considering whether the tests:
- Verify correctness of the solution (not just that it runs)
- Cover edge cases and failure modes
- Are resistant to shortcut solutions that don't actually solve the task
