# R31SrcS092a — S092 (Harbor) `VerifierConfig.environment_mode`, pinned 6099b8cf

Seat: leaf scout. Question: locate `VerifierConfig.environment_mode`, its description, its
declared default, and bound what the file alone can establish. Access date **2026-10-25**.

## Fetch identity

| item | value |
|---|---|
| URL | `https://raw.githubusercontent.com/laude-institute/harbor/6099b8cf2bfbbb3e7ff1eb2163bfc4524dbd9ba5/src/harbor/models/task/config.py` |
| commit | `6099b8cf2bfbbb3e7ff1eb2163bfc4524dbd9ba5` (matches the round's pinned revision) |
| HTTP / bytes | `200` / `39055` |
| sha256 (whole file) | `ac9f5d19e2cd311b2fe1c9d885c89fe21a98270613ae4546640b823540bf2163` |
| lines | `1060` |
| local copy | `/tmp/r31-R31SrcS092a/config.py` |
| sha256 (excerpt lines 587–595) | `1e6cc175ae3c453751d1e53f19919c0a3baf5feacca6e1fd18bd5b34d760f9b4` |

Commands used: `curl -sS -o config.py …`; `sha256sum config.py`; `wc -lc config.py`;
`awk 'NR>=578 && NR<=600'`; `grep -n "environment_mode" config.py` (4 hit lines: 587, 621, 625, 627).
No clone, no tree API call, no write outside `/tmp/r31-R31SrcS092a/` and this report.

## (a) Exact line range

- `class VerifierConfig(PhaseNetworkPolicyConfig):` — **config.py:580**
- `environment_mode` field declaration (whole `Field(...)` call) — **config.py:587–595**
  - `environment_mode: VerifierEnvironmentMode | None = Field(` — **config.py:587** (byte offset 20608)
  - `default=None,` — **config.py:588**
  - `description=(` — **config.py:589**; the four string literals — **config.py:590–593**; `),` — **config.py:594**; `)` — **config.py:595**
- Enum backing the type: `class VerifierEnvironmentMode(str, Enum)` — **config.py:573**, members `SHARED = "shared"` **:576**, `SEPARATE = "separate"` **:577**
- Sibling field that restates the same rule: `environment: EnvironmentConfig | None` — **config.py:596–605** (rule sentence at **:600–605**)
- The only validator that touches the field: `_validate_mode_env_consistency` — **config.py:616–628** (raises at **:620–627**)

## (b) Verbatim description text

As written in the source (four adjacent literals, config.py:590–593):

```
"Whether the verifier runs in the agent's environment ('shared') "
"or in a dedicated container ('separate'). When omitted: defaults "
"to 'separate' if a verifier 'environment' is set, otherwise "
"'shared'."
```

Concatenated (28 whitespace words), byte-identical to the staged entry's blockquote at
`benchmark-verifier-execution-model.md:19–21` after stripping the `> ` prefixes (checked
programmatically: `entry contains desc verbatim after stripping blockquote: True`):

> Whether the verifier runs in the agent's environment ('shared') or in a dedicated container ('separate'). When omitted: defaults to 'separate' if a verifier 'environment' is set, otherwise 'shared'.

## (c) Default-resolution quote (13 whitespace words)

> When omitted: defaults to 'separate' if a verifier 'environment' is set, otherwise 'shared'.

Substring of (b) starting at the word `When`; verified present in the concatenated literal.
Two-branch rule: `separate` **iff** `[verifier.environment]` is set, else `shared`.

## (d) Declared default is `None` — and what that implies

- Yes: `default=None` at **config.py:588**, type `VerifierEnvironmentMode | None` at **config.py:587**.
  So the Pydantic attribute value is the sentinel `None`, not a member of the enum, whenever the task
  does not write the key.
- `None` therefore means **"unspecified"**, not "shared" and not "separate". The effective mode is a
  decision taken downstream of deserialization. Nothing in this file converts `None` into
  `SHARED`/`SEPARATE`: `environment_mode` occurs at only four lines (587, 621, 625, 627), and the
  validator at 616–628 only *rejects* one combination (`SHARED` + `environment` set → `ValueError`,
  message at 625–627); it never rewrites the field. No `model_config` / `exclude_none` /
  `populate_by_name` appears anywhere in the file (`grep` returned nothing), so this file also does
  not establish how `None` serialises back out to `task.toml`.
- The second doc statement agrees with the first and adds the forward direction: setting
  `environment` *without* `environment_mode` "implies `environment_mode='separate'`"
  (**config.py:600–602**), and setting it *with* `environment_mode='separate'` is allowed while
  `'shared'` conflicts (**config.py:603–605**, enforced at 620–627). Both statements are prose.

## What this source can and cannot establish on its own

**Can establish (observed, this file at this commit):**
1. The field exists, its type is `VerifierEnvironmentMode | None`, its declared default is `None`
   (587–588), and the enum has exactly two members, `shared` and `separate` (573–577).
2. The documented resolution rule, stated twice in the same file: separate iff a verifier
   `environment` is set, otherwise shared (590–593; restated 600–605).
3. That the model itself will not error when the key is omitted (default `None` passes the only
   validator), and the single documented illegal combination (620–627).

**Cannot establish (a description string is not the resolution code):**
1. **That any code implements the rule.** The resolution site is not in this file. A reader holding
   only `config.py` cannot show that `None` becomes `SHARED`/`SEPARATE` anywhere, nor where
   `environment_mode` is consumed to choose the verifier container. Locating it requires the verifier
   runtime module(s) at the same commit (the entry's S092 `source:` line also cites `Verifier.verify`,
   which is *not* in this file).
2. **The premise "neither benchmark opts in".** That is a property of the two task trees
   (S100, S093), not of Harbor; this file cannot speak to any `task.toml`.
3. **Which mode actually produced a given score.** Mode selection at run time, plus any replay path,
   is outside this file.
4. Whether `None` is omitted from serialised `task.toml` output (no model config here).

Consequence for the entry: its sentence "So the default is **SHARED**"
(`benchmark-verifier-execution-model.md:23`) is true only of tasks with no `[verifier.environment]`;
the description's first branch makes `separate` the default when that section exists. The entry's
next clause ("opt-in by writing a `[verifier.environment]` section") is consistent with the rule; the
unconditional "the default is SHARED" phrasing drops a branch of the very sentence it quotes. The
quoted span itself is **found verbatim at the pinned revision** — the citation survives C1's kill
rule for S092.

## Registry / gate observations (context for main, not edits)

- `grep -n "S092" corpus/SOURCES.md` at lane tip returned **no match**: the S092 row is not yet in
  the registry (C1's `rows_present=3` still owes it). Observed 2026-10-25, no write made.
- C3 binding note: the entry's `source:` line 2 cites a **repo-root** URL
  (`https://github.com/laude-institute/harbor`), not a file URL. For `--url-map` to bind this row's
  capture to the document the quote was read in, the map entry must be the file-level URL used above
  (`…/6099b8cf…/src/harbor/models/task/config.py`), i.e. the row URL is under-specified relative to
  the quote's true origin.
- Tool installs this run: none.

VERDICT: S092 PASSES the quote-location test — `VerifierConfig.environment_mode` at config.py:587–595 (description 590–593) contains the staged entry's quote verbatim at commit 6099b8cf (file sha256 `ac9f5d19…bf2163`, 39055 bytes) — but the description is documentation, not resolution code: `None` (line 588) is an unspecified sentinel that this file never resolves, so the entry's "default is SHARED" is supportable only as "shared when no `[verifier.environment]` is set" and the claim that the harness *resolves* the mode this way remains unproven by S092's cited file alone.
