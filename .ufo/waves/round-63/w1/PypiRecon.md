# PypiRecon — R63-C1 / R63-C2 recon (round 63, w1)

Seat dir: `.ufo/waves/round-63/w1/recon/` — files `recon.md` (full detail, every value with its
command), `S228-pypi-test_outputs.py`, `S229-pep-0503.html`, `legs-sandboxed.txt`, `k2-stderr.txt`.
Date 2026-11-03. Scratch `/fast/scratch/hyaku/kengaku-r63/PypiRecon` removed.

## Verdicts

| item | verdict |
|---|---|
| lane `test_outputs.py` / `test.sh` vs frozen + `SHA256SUMS` 134/135 | **MATCH** both (`82c63517…`, `d2b1220e…`) |
| S228 live (pin `2fd12b88`) | **sha MATCH** `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c`, `cmp` byte-identical to the capture |
| S228 quotes | `localhost:8080` L**18**, L**30**; `vectorops==0.1.0` L**31**, L**50**; **`pip install --index-url` absent as a string** (argv split per line; `--index-url` alone = L**29**) |
| S229 live | opened, sha `5b97cb7e…c453c4f`; quote “The format of this URL is /<project>/ where the <project> is replaced by the normalized name for that project” **L166–167**, section `Specification` (L140); last-modified **yes**, L260 `2025-08-20 21:30:45 UTC` |
| bwrap loopback | `loopback-ok`, exit 0; `bind 127.0.0.1:8080` inside bwrap ok |
| eight-member census | 8 rows in `recon.md` §9 (files+`wc -l`, endpoints, `grep -n`) |
| leg vector in a private netns | **P/F/F/F** = frozen; K2 `CalledProcessError`, K3 `AssertionError`, K4 `(from versions: 0.2.0)` |

## Two findings the L1 must act on

1. **8080 is contended across seats — C1 can be a false P.** Observed a sibling index satisfy my
   K1 (served sha `82579705…` ≠ my `0e2c37a9…`, my server having died on `EADDRINUSE`), and a
   sibling answering a naive K2 → **P**. Five foreign PIDs on 8080 in ~20 min. `bwrap --unshare-net`
   fixes it (host cannot see or reach the sandbox's 8080; without it `1.1.1.1:443` is reachable).
   Not a rule change: the probe must unshare and record PID+served-sha, which is what the frozen
   K1 clause already demands.
2. **K2's predicate clause is not literally greppable.** pip 26.2.1 renders
   `HTTPConnection(host='localhost', port=8080)`; `grep -c -F 'localhost:8080'` on the captured
   stderr = **0**, `port=8080` = 5. The literal appears only in the `CalledProcessError` argv.
   Implement the clause against argv/host+port or C1 fails on a correct leg.

Minor: base sha in the claims header prints `c78749a5565dfd…`; the real object is
`c78749a565dfd186f10a1d8ac98e19dac2429666` (`git rev-parse`). Lane `test.sh` pins
uv 0.9.5/py3.13/pip 25.2; host offers uv 0.13.0 + 3.14.8 venv, and a 3.14 venv has **no
setuptools/wheel** (wheel must be hand-built via `zipfile`). Loopback HTTP needs no
`--trusted-host`; a non-loopback plain-HTTP index is refused. No host `pip.conf` anywhere
(no index-config leak), but `~/.ssh`, `~/.config/gh`, `~/.omp` exist (never read).

For C2: 16 classes, counts summing to 89, `network-service=8` executed **0** today, 4 classes at
`executed=0`; base `SKILL.md` has **0** class rows (`git show c78749a5:SKILL.md`); insert the new
section between L58 and `## Benchmark anti-patterns` (L60). `plans/round63_c1_pypi_probe.py`,
`plans/round63_gate_checks.py`, `corpus/evidence/round63/pypi-probe.txt`,
`corpus/knowledge/tb2-network-service-offline-grader.md` **do not exist yet** — citing them as
receipt pointers fails resolution until they land, so land the probe before the SKILL rows.

Tool installs: none (no pacman, no uv/npx install needed).
