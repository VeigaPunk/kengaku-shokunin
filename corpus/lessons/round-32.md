# Round 32 — round-31 closure, assimilation refusal, and catalog freshness probe (2026-10-25)

## Gate

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| `benchmark-grader-semantics.md` | **Refused this round** | The proposed entry is supported by source reads, but its staged S094/S097 rows collide with existing registry ids, and staged S101/S102 also collide with live rows. SOURCES contract rule 2 forbids reusing ids; the append was not admitted. Flip: prepare new non-colliding rows in a later round and repeat census and gate checks. |
| C3 catalog refresh | **Measurement landed; claim failed as declared** | Live endpoints were probed and schema deltas recorded, but the frozen counter's after condition cannot pass with the observed nonzero HF delta; do not relabel this as a pass. |

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| collision / admission | `corpus/SOURCES.md` duplicate id census: S094, S097, S101, S102 collide with existing registry entries | `FxEntryTruth`, `FxRowMutations`, census exit 1 | Keep staged candidates rejected; never append colliding ids. |
| counter | `plans/catalog_probe.py --selftest` failure from repeated `mkdir` without `exist_ok=True` | local run after the counter repair | Use idempotent fixture directory creation; preserve test coverage of missing receipt and valid receipt. |
| scope | `FxFailOpen.md` and `FxEntryTruth.md`: credential-load fallthrough returns implicit `None`, not a universal fail-open | falsify reviewers | Narrow the entry and source row to distinguish caught exceptions from credential failures. |
| landing | `corpus/evidence/round32/catalogs/after.txt` is a summary receipt, not retained raw API responses | `FxSentinel.md`, `FxEvidence.md` | Preserve raw response bytes and digests in the lane if the C3 observation is to be independently rechecked. |

## Round-31 routed defects

The round-31 verifier spot-check remains the source of the routed D1–D6 items. The CLI receipt and gate registry row were repaired on disk; the report phantom-hash and lesson errata remain unlanded at this point. `R31FxEntryBar` is recorded as a missing falsify report, not as a successful seat.

## Assimilation

The shokuknow grader-semantics candidate was **not admitted**: four staged identifiers collide with the lane registry. Existing S094/S097/S101/S102 source rows remain authoritative. No registry append was accepted; the staged rows are recorded as rejected, and the C1 counter's census failure is preserved as the refusal evidence. The S094 staged row also misstated the executed tolerance and log-check behavior, and the S097 staged quote omitted one `L`.

## C3 catalog probe

Observed on 2026-10-25: Hugging Face default list response had 50 items and omitted four fields present with `?full=true` (`author`, `sha`, `lastModified`, `gated`); OpenRouter returned 467 items with the twelve fields checked. Summary receipt: `corpus/evidence/round32/catalogs/after.txt`; independent probe report: `.ufo/waves/round-32/falsify/FxC3DiffTruth.md`. This is an observation with nonzero delta, not a passing C3 claim: the frozen C3 predicate is **failed as declared**.

## Disclosures, dead seats, and open questions

- Falsify wave: 34 seats dispatched; reports live under `.ufo/waves/round-32/falsify/`.
- `R31FxEntryBar`: no committed report in the round-31 registry; recorded as dead/unreported.
- C1: entry draft exists but is not admitted; do not count it as a corpus expansion.
- C3: after counter predicate cannot pass honestly with the observed HF delta; preserve failure, do not change frozen predicates.
- No tools installed or updated.
