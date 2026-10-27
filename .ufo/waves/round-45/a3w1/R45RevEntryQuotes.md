# R45RevEntryQuotes — C2 entry quote review

Measured lane tip: `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (`git rev-parse HEAD`; read-only command).

## Located quotes — byte comparison

Command: `/usr/bin/python3 "$S/quote_check.py"` (scratch script; compares each parsed entry quote to the cited capture line/span, without stripping quote bytes). Output: `located-quotes verbatim: 19/19`; `word-range violations (3-25): none`. Each row was `OK`; capture line/quote hit locations:

| # | Citation | Match |
|---|---|---|
| 1 | instruction.md:2 | exact line |
| 2 | instruction.md:4 | exact line |
| 3 | instruction.md:6 | exact line |
| 4 | instruction.md:9 | substring |
| 5 | test_outputs.py:9 | exact after source indentation |
| 6 | test_outputs.py:14 | exact after source indentation |
| 7 | test_outputs.py:18 | exact after source indentation |
| 8 | test.sh:25 | exact line |
| 9 | test.sh:26 | exact after source indentation |
| 10 | setup.sh:25 | exact line |
| 11 | setup.sh:30 | exact line |
| 12 | setup.sh:36 | exact line |
| 13 | solve.sh:16 | exact line |
| 14 | solve.sh:62 | exact after source indentation |
| 15 | solve.sh:41 | verbatim substring; also occurs at :22 |
| 16 | Dockerfile:17 | exact line |
| 17 | README.md:31 | verbatim substring |
| 18 | task.toml:22-25 | exact line at :22 (also same text at :25) |
| 19 | task.toml:34 | exact line |

Capture SHA-256 values measured by the same command, compared against `plans/pkg-spec-r45.json` pins (all eight match):

| Source | SHA-256 | Pin |
|---|---|---|
| S149 `test_outputs.py` | `2dc14fc180734b6fbb0ee00f27c4f866071247b57a2217f579465ff8ed3bfc9e` | match |
| S150 `instruction.md` | `bc4f501148805bbccdb94a5c5b745f1ce9564f04ef0fe36bc37c3ca20b7810a5` | match |
| S151 `setup.sh` | `9fdde5d9cd74ae0d633bdd59e7249cc6d7385d27a98b1e2dbbeb11b05a6f2af8` | match |
| S152 `Dockerfile` | `6fabcb9e1fcb7155bf8cfe106c17f2dfa3344103e97960dab580c2444b6c9fe0` | match |
| S153 `test.sh` | `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` | match |
| S154 `README.md` | `122bf15ef4a6ede562f21453f9f1c452fc10a3048bac7d46a013adbac6a13add` | match |
| S155 `solve.sh` | `c5f9fc70b6bae40befdd0088dde1a3bc6e909852c9fbb36a617c627b7b8d804f` | match |
| S156 `task.toml` | `cfd0362d201b957796f9bf1c02cc75646250cb2bd107ec88c768bfcfd091b24b` | match |

The complete `sha256sum corpus/evidence/round45/tb2-password-recovery/*` output also showed the spec-pinned hashes above. No upstream refetch was performed.

## Mechanism — verbatim and decisive attribution

Command: `/usr/bin/python3 "$S/quote_check.py"`. Output: `mechanism verbatim: 16/16`; each quoted fragment is present on its cited capture line. One attribution is nevertheless incorrect: `empty-file` cites `test_outputs.py:16` as decisive. The same check produced `empty-file: guesses=[''] len>0 assert(:16)=PASSES membership(:18)=FAILS -> decisive line is :18, entry table says :16`. The entry’s Findings section correctly says `:18` decides this case, so its Mechanism row contradicts its own analysis.

## Source IDs and citation ranges

Command: `/usr/bin/python3 "$S/quote_check.py"`. Output: entry `source:` IDs are exactly `['S149', ..., 'S156']`; spec keys are exactly `['S149', ..., 'S156']`; `id sets equal: True`; `S-ids in body but not in a source: line: none`. All eight entry URLs match `raw_base + rows[sid].upstream`.

The entry’s source-line ranges are inaccurate/inconsistent with captures: S151 declares `setup.sh` lines 1–45 (43 actual lines); S152 declares Dockerfile 1–16 although the Located quote is at Dockerfile:17; S153 declares test.sh 1–31 (29 actual lines); S154 declares README.md 1–46 (33 actual lines); S155 declares solve.sh 1–70 (68 actual lines). S149’s cited line numbers and S150/S156 ranges are within their captures. Capture line counts and hashes were measured in the same script output. These range errors do not change the matching IDs or URLs, but make the entry’s source citations unreliable.

## Predictor — mismatch reproduced

The entry describes its Predictor as the grader’s exact rule after `read_text()` universal-newline conversion, but implements only `text.replace("\\r\\n", "\\n")`. Python `Path.read_text()` universal newlines also convert lone `\r` to `\n`.

Counterexample was executed inside the mandated envelope, using the captured `test_outputs.py` in the probe’s bwrap-style grader harness and executing the entry’s Predictor code verbatim on the same raw bytes. State bytes: `b"8XDP5Q2RT9ZK7VB3BV4WW54\\rWRONGDECOY0\\n"`. Output: captured grader `letters=PP -> PASS`; entry predictor `False`; universal-newline-corrected predicate `True` (`<< DIVERGES FROM GRADER`). Two additional states also diverged: answer followed by lone CR and decoy without final newline; and a decoy followed by lone CR then answer. Summary output: `states=9 predictor-vs-grader divergences=3`.

Required envelope receipt for that run:

```text
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45RevEntryQuotes/env /fast/scratch/hyaku/kengaku-r45/R45RevEntryQuotes/env --bind /fast/scratch/hyaku/kengaku-r45/R45RevEntryQuotes/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- env S=/fast/scratch/hyaku/kengaku-r45/R45RevEntryQuotes TMPDIR=/fast/scratch/hyaku/kengaku-r45/R45RevEntryQuotes /usr/bin/python3 /fast/scratch/hyaku/kengaku-r45/R45RevEntryQuotes/predictor_check.py
ENVELOPE start 00:32:20 cwd=/fast/scratch/hyaku/kengaku-r45/R45RevEntryQuotes
STATE lone-cr-mid: bytes=b'8XDP5Q2RT9ZK7VB3BV4WW54\rWRONGDECOY0\n'
  captured-grader (bwrap): letters=PP -> PASS  rc=0
  entry-predictor(text):   False   universal-newline-corrected: True   << DIVERGES FROM GRADER
summary: states=9 predictor-vs-grader divergences=3
ENVELOPE end 00:32:22 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

The grader source evidence is `corpus/evidence/round45/tb2-password-recovery/test_outputs.py:14,18`: `read_text().strip().split("\n")`, then exact membership. CRLF states agree; the demonstrated lone-CR states do not. This is a concrete false-negative in the entry’s claimed predictor rule, not a defect in the captured grader.

## Residual risk / verification gaps

No upstream URL was fetched; local capture bytes were compared to the spec’s expected SHA-256 pins. The source `source:` ID set and URL map are correct despite the inaccurate cited line ranges. This review does not re-run the full C2 probe or assess its other receipt/predictor checks.

VERDICT: entry-quotes-19/19-mechanism-16/16-predictor-mismatch
