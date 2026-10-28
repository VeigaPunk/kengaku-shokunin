# C2ExecRowFacts — round 52 wave 1

## Result

Derived per-instrument facts for all 28 paths reported `MISSING` by the frozen C2 counter. The machine-readable artifact is `facts.json` beside this report (28 top-level instrument objects; SHA-256 `6deb2176d319d07f442532e21eee6c138aae8bb8e9ecfc30362f9ec3748d9fce`). The requested scratch copy was `/fast/scratch/hyaku/kengaku-r52/C2ExecRowFacts/facts.json`; it was copied here before scratch cleanup.

- Counter output: `ADVERTISED total=72`, `REGISTERED total=44 rows=46`, `MISSING 28`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 1` (`order-check`), predicate fail / exit 1.
- Facts derived: 28/28; could not derive an instrument-level fact: none. Dynamic path expressions are explicitly retained as dynamic in `file_writes`, rather than guessed as concrete paths.
- `--selftest` declared: 12/28; their observed output and exit status are in the JSON. Others are explicitly marked as lacking the flag.
- Network: `catalog_probe.py` makes external HTTP requests to Hugging Face and OpenRouter. `attrib_probe.py` uses HTTPConnection to loopback (127.0.0.1) only; `round51_surfaces.py` makes loopback-only HTTP/port probes. `round35_c1_verify.py` and `round36_c2_verify.py` contain pinned raw-GitHub URL text but no network call. Remaining scripts have no network requirement detected.
- Script exit behavior contradicting its own docstring: none found. Several older counters return failure on the measured base-tip tree; this is consistent with their documented fail verdict, not a contradiction. In particular, round35 C1, round36 C2, round45 C2, and round46 C3 returned 1 on their documented failure findings. `tb2_grader_probe.py` returned 0 when invoked as documented with Biopython 1.85.

## Commands run

Commands below were run from the indicated directory; all probes used a scratch copy/clone, not the live lane tree for script execution.

1. From `/home/vgpnk/Projects/shokunin/kengaku-shokunin`:
   - `python3 plans/round52_c2_registry.py --lane .`
   - `du -sh .`
   - `git rev-parse --show-toplevel`
   - `python3 -V`
2. Scratch setup and copy:
   - `mkdir -p /fast/scratch/hyaku/kengaku-r52/C2ExecRowFacts/tmp`
   - `cp -a /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r52/C2ExecRowFacts/lane`
   - `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r52/C2ExecRowFacts/base`
   - `git -C /fast/scratch/hyaku/kengaku-r52/C2ExecRowFacts/base checkout -q 30801b479e3418c11089b8586178b6960216f364`
3. From `/fast/scratch/hyaku/kengaku-r52/C2ExecRowFacts`:
   - `python3 extract_ast.py lane facts_ast.json $(cat targets.txt)`
   - `python3 probe_runtime.py` (help/default probes against the scratch copy; `TMPDIR` explicitly set by the driver)
   - `python3 extract_selftest.py`
   - `python3 probe_selftest.py`
   - `python3 extract_writes.py`
   - `python3 probe_base_tip.py` (canonical `--lane .` invocations for the previously nonzero/default-error cases on the pristine base-tip clone)
   - `uv run --no-project --with biopython==1.85 python3 -c "import Bio; print('biopython ok', Bio.__version__)"`
   - `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` (executed by the probe driver from the base-tip clone)
4. Counts/checks on the facts artifact:
   - AST-derived flags were combined with `--help` output to include subparser flags not displayed by top-level help.
   - The completed facts object contains 28 instruments and 12 selftest-enabled instruments.

## Evidence and caveats

At the exact base tip `30801b479e3418c11089b8586178b6960216f364`, `round35_c1_verify.py` printed `V4 DEFECT knowledge files=55 index rows=54 (want 42/42)`, `round36_c2_verify.py` printed `W4 DEFECT knowledge files=55 index rows=54 (want equal and >=43)`, `round45_c2_verify.py` failed its frozen gate, and `round46_c3_verify.py` failed its predicate; these are recorded as observed exit codes and output tails in `facts.json`, not treated as selftest/docstring contradictions. The initial working-copy probe included then-present untracked wave marker files, so those runs were not used to characterize clean-tree behavior; base-tip reruns are retained separately where applicable.

`uv 0.13.0` executed the documented ephemeral `--with biopython==1.85` invocation (package channel: PyPI; reason: the instrument's docstring requires Biopython). No persistent tool installation was performed.

Scratch cleanup: completed before handoff; the retained artifact is the report-directory copy of `facts.json`.
