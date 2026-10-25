# C3 probe attack — FxC3Probe

## Live run

Ran `python3 plans/catalog_probe.py --diff --lane .` in the lane repo. Full stdout and captured exit code:

```text
probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=ok
HF missing fields: author, sha, lastModified, gated
EXIT_CODE=1
```

The `entry=stale` branch is **not** exercised: the live result is `entry=ok`. The on-disk entry actually has `S101`, `S102`, and `verified-at: 2026-10-25` in lines 1–3 and names the receipts path in line 1. The observed live failure condition is nonempty HF schema delta (four missing fields), not a stale entry. This means the task description's “entry still stale” premise does not match the current draft on disk.

## Partial-failure attack

To avoid changing the lane, copied `plans/catalog_probe.py` to `/tmp/r32f-FxC3Probe/catalog_probe.py` and changed only the URL constant in that copy to `https://127.0.0.1:1/unreachable`. First run: bad HF URL, original OpenRouter URL. Output:

```text
probed=2026-10-25 hf=fail openrouter=fail hf_models=0 or_models=0 hf_schema_delta=0 or_schema_delta=0 entry=ok
EXIT_CODE=1
```

Then changed the scratch copy to restore the HF URL and make only the OpenRouter URL bad. Output was identical:

```text
probed=2026-10-25 hf=fail openrouter=fail hf_models=0 or_models=0 hf_schema_delta=0 or_schema_delta=0 entry=ok
EXIT_CODE=1
```

Both simulations exit nonzero and produce a distinct `fail` line. But they do **not** report partial success: whichever endpoint fails causes both source statuses and both counts to be reported as failed/zero. Source lines 74–79 show sequential fetches with no per-source exception handling; lines 102–107 catch any exception around the whole `probe()` call and set one shared status plus both counts to zero; lines 109–114 print that shared status for both sources. Thus a successful first endpoint is discarded if the second fails, and the reported endpoint attribution is inaccurate. This contradicts the frozen C3 kill-rule requirement to report partial results honestly when either endpoint is unreachable.

## Summary-line ambiguity

The single summary line is **not inherently ambiguous between overall probe `ok` and `fail`**: it includes both `hf=` and `openrouter=` status fields. However, on error both fields become `fail` regardless of which API failed, falsely implying both failed. Also, `ok` does not mean the overall command passes: the live run has `hf=ok openrouter=ok`, but exits 1 because the HF schema delta is 4. The line exposes that delta count, so the reason for failure is inferable, but it does not encode overall verdict/exit status itself.

## Finding and smallest safe correction

**Counterexample:** one endpoint failure erases the other endpoint's successful result and labels it failed. Impacted axis: freshness (C3 partial-failure honesty / kill rule); calibration is also implicated if this counter is used as evidence of which source was reachable. Smallest safe correction: isolate each endpoint's fetch/parse in its own `try`/`except`, retain each source's independent status/count/schema delta, and print an explicit unavailable status for only the failing source; preserve nonzero exit whenever either source fails. Re-run the one-URL-failed simulations after that correction.

VERDICT: <attack-finished>
