# LabratR76 — endpoint-status hypothesis

## Verdict and axes

**H1 CONFIRMED.** Axes: coverage (what an endpoint verdict actually covers), calibration (status versus service identity), preservation (zero production/substrate edits).

The endpoint leg measures HTTP responsiveness, not successful resource resolution or the declared service's identity. This is a **resolution limitation, not a falsification of the frozen claim's literal HTTP-status predicate**: the frozen claim says “an HTTP status for endpoints,” not a 2xx response, model-id match, or `owned_by` match. Do not silently strengthen that frozen predicate. The stronger interpretation “the declared model is actually present” is not established by this gate.

## Execution and retained evidence

Read the entire `plans/round-76-claims.md` before commands. No delegation/spawn interface was available; ran the explicitly assigned probe directly. No build, linter, formatter, full-lane gate, git mutation, tool install/update, or live model request was run. Python 3.14.8 was already available. No LSP interface was exposed; symbol inspection used source reads, not an empty LSP result.

One finite driver executed, with scratch cleanup trap:

```sh
bash -c 'S="$1"; trap '\''rm -rf -- "$S"'\'' EXIT; mkdir -p -- "$S" && python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-76/w1/LabratR76/probe.py "$S"' LabratR76 /fast/scratch/hyaku/kengaku-r76/LabratR76
```

Exit **0**, stderr empty. Cleanup observation: `SCRATCH_EXISTS_AFTER False`. The child fixture server terminated as requested: `SERVER_WAIT_RC -15` (intentional SIGTERM, not a gate exit).

Exact child server command:

```sh
/usr/bin/python3 -u -m http.server 0 --bind 127.0.0.1 --directory /fast/scratch/hyaku/kengaku-r76/LabratR76
```

The driver imported a byte-for-byte snapshot of the production resolver, called `resolve('endpoint', URL, scratch)` and `emit(scratch, 'worktree', receipt)` without modifying gate code, then exercised a finite 500-response server. No lane mirror or git fixture was created. `emit`'s read-only git metadata calls ran only against the scratch path.

Retained relative paths:
- `.ufo/waves/round-76/w1/LabratR76/probe.py`: exact executable driver, including the 500 response bytes and all function calls/commands.
- `.ufo/waves/round-76/w1/LabratR76/resolver-tested.py`: tested source snapshot; SHA-256 `f928b81db5309710e12a1373b13f091345797358a71c9cb3411b6d939057e7ff`.
- `.ufo/waves/round-76/w1/LabratR76/fixture-PROVINCE.md`: exact fixture rows.
- `.ufo/waves/round-76/w1/LabratR76/fixture-gate.txt`: unmodified gate receipt (fixture gate exit 0).
- `.ufo/waves/round-76/w1/LabratR76/probe.txt`: verbatim probe transcript.

### Counterexample bytes

```markdown
## Surfaces

| Surface | Path / endpoint | What this lane does with it |
|---|---|---|
| Declared model | `http://127.0.0.1:40039/missing-health` | model id `LFM3-1.7B`, `owned_by=llamacpp` |
| Declared model identity | `http://127.0.0.1:40039/v1/models` | model id `LFM3-1.7B`, `owned_by=llamacpp` |
```

The missing resource was deliberately not created. `/v1/models` was a static file served by Python, containing exactly these bytes (including final LF):

```python
b'{"object":"list","data":[{"id":"NOT-LFM3-1.7B","owned_by":"NOT-llamacpp"}]}\n'
```

Key output, verbatim:

```text
RESOLVE http://127.0.0.1:40039/missing-health ('present', 'http=404')
RESOLVE http://127.0.0.1:40039/v1/models ('present', 'http=200')
IDENTITY_RESPONSE_BYTES b'{"object":"list","data":[{"id":"NOT-LFM3-1.7B","owned_by":"NOT-llamacpp"}]}\n'
SURFACE 1 present http://127.0.0.1:40039/missing-health (http=404)
SURFACE 2 present http://127.0.0.1:40039/v1/models (http=200)
SURFACES total=2 present=2 absent=0 prose=0
AGREE agree=2 disagree=0
PREDICATE R76-C1 pass
FIXTURE_GATE_RC 0
RESOLVE_500 ('present', 'http=500')
```

### Live health probes

Exact commands:

```sh
curl --silent --show-error --max-time 5 --output /dev/null --write-out '%{http_code}' http://127.0.0.1:1234/health
curl --silent --show-error --max-time 5 --output /dev/null --write-out '%{http_code}' http://127.0.0.1:45669/health
```

First: stdout `200`, exit **0**, stderr empty. Second: stdout `000`, exit **7**, stderr:

```text
curl: (7) Failed to connect to 127.0.0.1:45669 after 0 ms: Could not connect to server
```

Resolver results, verbatim:

```text
LIVE_RESOLVE http://127.0.0.1:1234/health ('present', 'http=200')
LIVE_RESOLVE http://127.0.0.1:45669/health ('absent', 'http=000')
```

## Numbered findings

1. **MEDIUM — Status presence is weaker than resource/service presence.** Pointer: `plans/round76_c1_surface_resolver.py:154-167`, retained `resolver-tested.py`, `probe.txt`, and `fixture-gate.txt`. `HTTPError` becomes its numeric status and `resolve` rejects only the string `000`. Empirically both 404 and 500 are present; the two-row fixture passes with no defects. All other non-000 strings follow directly from that condition, not from an exhaustive status-code experiment. This does not trigger a frozen kill rule under its literal responsiveness semantics; it prevents reading the verdict as a success/health guarantee.

2. **MEDIUM — Identity is not checked.** Pointer: same resolver lines, `identity()` at 129-139, and `census()` at 193-204. Despite its name, `identity()` extracts only an anchor type/token. The HTTP leg reads `resp.status`, not JSON/body fields; the row's declared model id and `owned_by` are never compared. A generic Python server returning deliberately wrong values passes. The live 1234 health 200 is therefore evidence of responsiveness only, not current model identity.

3. **INFO — Live router/dead direct-server contrast reproduced.** Pointer: `probe.txt` `LIVE_RESULT`/`LIVE_RESOLVE` lines. Port 1234 health: 200/rc 0/present. Port 45669 health: 000/rc 7/absent. This experiment does not contradict the frozen row-4 absence interpretation, which selects the first endpoint.

## Smallest repair / scope boundary

For this frozen round, the smallest honest repair is clarification of the endpoint verdict's meaning: “an HTTP-speaking listener answered; resource success and service identity unverified.” Keep numeric HTTP status in the receipt; do not silently change the frozen gate or target.

If a separately authorized future predicate requires successful resource presence, the smallest logic change is to distinguish non-2xx responses from successful endpoints rather than mapping every non-000 status to present. **That change alone does not repair identity.** Declared model identity additionally requires a narrow `/v1/models` JSON comparison of the expected `id` and `owned_by`; a 2xx wrong-service response still fails that stronger requirement. These are recommendations only; no production repair was applied.

## Limits and risks

No full production C1/C2 gate or selftest/mutant battery was run. No assertion about final landing counts, current model identity, route ownership, or temporal stability is made. The fixture port is ephemeral and has been stopped. Source evidence is the retained hash, not an assertion that the moving worktree equals the frozen commit. The finite probe creates a disposable child HTTP server and thread, both stopped before completion; no persistent service/job remains. No secrets/session/token material was read.

## Self-evaluation

Accuracy 4/5: numeric and identity counterexamples retained, but no exhaustive status-code sweep (unnecessary for the exact source condition). Completeness 5/5: 404, 500, wrong identity, both live health codes, smallest repair and truth/resolution distinction delivered. Clarity 4/5: separates HTTP presence from identity, though command/receipt detail adds length. Actionability 4/5: exact counterexample and bounded repair supplied; stronger identity policy needs explicit future authorization. Conciseness 4/5: evidence retained verbatim, with unavoidable repetition between findings and transcript. Overall 4.2/5. Improvements: preserve the responsiveness/identity distinction in any integration summary; do not promote health 200 to a model-identity claim. Would the user agree? [INFERENCE] Yes, if the frozen HTTP-status scope is retained.
