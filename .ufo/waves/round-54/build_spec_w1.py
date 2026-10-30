#!/usr/bin/env python3
"""Build the round-54 wave-1 (v2, 64 seats) spec. Run from the lane repo root."""
import json

GODSPEED = "/skill:godspeed\n\nYou are a Godspeed-enabled subagent.\n\n1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n3. **Keep moves that improve any axis and harm none.**\n4. **Don't aim — let the frontier walk itself.**\n\n## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.\n"

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
WAVE = "kengaku-r54-w1"

CONTEXT = f"""# Goal
kengaku round 54 (hyaku run 12), ONE v2 wave (build + attack together), lane repo {LANE}. L1 = KengakuR54.
The round's two claims are FROZEN in {LANE}/plans/round-54-claims.md (commit 17f90355c3ec17dcf15f7980d83f1943ae428fe5)
— READ IT IN FULL FIRST; it binds every seat. Its predicates, thresholds, controls and kill rules never change after a
seat has scored. The claims file's bytes are the C1 anchor digest: NOBODY edits that file; amendments would go to a
separate plans/round-54-amendments.md, and only the L1 writes one.

- **R54-C1 (novelty 8->9)** — externally anchored measurement freeze. Counter
  `{LANE}/plans/round54_c1_anchor.py` (frozen, --selftest 8/8). Anchor dir
  `{LANE}/corpus/evidence/round54/anchor/` (claims.ots stamped 2026-10-30T10:49:37Z over digest
  d7aa05c8fcd4aff2ec6f1b606c4e5072d1082b51da8d1c091e2ed1df0d995eb8; header.bin + >=2 explorer receipts are the
  upgrade seat's deliverable). OTS venv: /fast/scratch/hyaku/kengaku-r54/l1/venv/otsenv (opentimestamps-client 0.8.0;
  you may reinstall your own via uv if you prefer — record tool/version/channel).
- **R54-C2 (calibration 9->10)** — every registry row declared at its ENTRY argv, hermetically executed; the
  selected-argv laundering route closed. Counter `{LANE}/plans/round54_c2_entrytruth.py` (--selftest 7/7),
  ledger `{LANE}/plans/round54-entrytruth.json` (committed; built by the frozen builder
  `{LANE}/plans/round54_build_entrytruth.py` over clean clone 17f90355). Controls
  `{LANE}/plans/round54_c2_controls.py` (--route-only demonstrated the r53 laundering route BEFORE data;
  --closed and --env-poison show closure). The round-53 counter, its ledger and SKILL.md are frozen artifacts:
  never edit plans/round53_c2_tipstate.py, plans/round53-tipstate.json, plans/round53_c1_triage.py, SKILL.md,
  or plans/round-54-claims.md.

# Contract (every seat)
- Write scope: your report and any files you produce go ONLY under {LANE}/.ufo/waves/round-54/w1/<YourName>/
  (create the dir) plus scratch. You NEVER run a mutating git/jj command anywhere, never commit, never push, never
  touch .ufo/state/, .ufo/watchdog.log, MANIFEST.json, the fleet repo root, scripts/, templates/, or any sibling
  repo. Production-file proposals (counter edits, ledger edits beyond your brief, SOURCES rows, knowledge entries)
  land as files in your wave dir; the L1 integrates them. The ONLY seats allowed to write inside the lane tree
  outside .ufo/ are the ones whose item explicitly names the exact destination path — even then, never git/jj.
- Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.
- Scratch discipline (operator directive 2026-10-25): every clone/work tree/fixture of yours lives under
  /fast/scratch/hyaku/kengaku-r54/<YourName>/ (mkdir -p; TMPDIR and mkdtemp(dir=...) point there explicitly;
  /tmp holds files < 50 MB only). One live clone per seat: git clone --shared or git worktree add. Delete your
  scratch dir before you yield (trap EXIT / finally), receipts copied into your wave dir first. Check
  /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status before a heavy pass; on ENOSPC report the free
  space you saw and stop.
- Git fixtures: create ONLY in your scratch root as D=$(mktemp -d -p /fast/scratch/hyaku/kengaku-r54/<YourName>) &&
  git -C "$D" init -q; every later git call names -C "$D"; verify `git -C "$D" rev-parse --show-toplevel` == "$D"
  before the first commit; commit identity inside fixtures may be any throwaway, but NEVER run git commit/jj with a
  throwaway identity outside "$D".
- Secrets (CORPUS.md rule 8): no credential material, tokens, cookies or op:// references anywhere. OTS/explorer
  network calls carry only the 32-byte digest of a public repo file — never file contents.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task — read
  /home/vgpnk/.omp/agent/RULES.md first; official channels only; record tool/version/channel/reason in your report.
  **pacman guard: ALL pacman transactions are PAUSED host-wide** — install via uv tool / npx / an official binary in
  ~/.local/bin. Never pacman -Sy/-Syu/-U/-R, never downgrade, never restart a host service.
- Depth: an executor seat may spawn ONE read-only labrat probe for a falsifiable hypothesis (the only permitted
  child seat); every other role is a leaf; nobody runs a swarm.
- Role decides routing; never pass a model parameter. Never message agent://all.
- A seat that finds nothing reports the command that produced the absence. Never fabricate a number, quote or URL.

# Frozen facts you may rely on
- Base tip 6c919180260ea545589c2c0a007a06f554b529d3; freeze (stage-1) 17f90355c3ec17dcf15f7980d83f1943ae428fe5
  (claims + counters + before receipts; remote-verified).
- Before receipts: corpus/evidence/round54/c1-before.txt (anchor absent, exit 1), corpus/evidence/round54/c2-before-dry.txt
  (ledger absent, exit 1). Route receipts run pre-data: r53 counter PASSes a forged fixture whose entry exits 1
  (laundering route open); r54 counter flags it LAUNDERED and hermetic env blocks a poisoned GIT_CONFIG_GLOBAL
  (.ufo/waves/round-54/claims/ once the L1 lands them).
- Registry: 78 rows (SKILL.md ## Gate/probe registry). The entrytruth ledger declares every row's ENTRY argv and
  observed exit on a clean 17f90355 clone.
"""

A = ["novelty"]
B = ["calibration"]
X = ["novelty", "calibration"]

items = []


def add(name, role, axes, text):
    items.append({"name": name, "role": role, "axes": axes, "item": GODSPEED + text})


# ---------------- executors: infrastructure (5)
add("E1AnchorConfirm", "executor", A, f"""# Target
kengaku round 54 seat E1AnchorConfirm (executor). R54-C1 novelty axis.
# Item
Drive the OpenTimestamps proof to a Bitcoin attestation and land the external-pin artifacts.
1. Upgrade the pending proof until confirmed: OTS=/fast/scratch/hyaku/kengaku-r54/l1/venv/otsenv/bin;
   $OTS/python {LANE}/plans/round54_c1_anchor.py upgrade --anchor {LANE}/corpus/evidence/round54/anchor
   --ots-bin $OTS/ots (repeat over ~30-60 min while doing step 2; ots upgrade exit 0 = confirmed).
2. Extract the attestation height (python: parse the proof with the venv's opentimestamps library; print height
   and attested digest). Fetch, into scratch first: the block hash by height and the raw 80-byte hex header from
   https://blockstream.info/api/block-height/<H> then /block/<hash>/header, and the same two values from
   https://mempool.space/api/block-height/<H> and /block/<hash>/header. Compare the two sources' hashes byte-for-byte.
3. Write {LANE}/corpus/evidence/round54/anchor/header.bin (the 80 raw bytes) and two receipt files
   {LANE}/corpus/evidence/round54/anchor/block-explorer-1.json / -2.json, each:
   {{"source":"blockstream.info"|"mempool.space","url":"<exact API url>","height":H,"hash":"<display hex>",
   "time":<block unix time>,"fetched_at":"<ISO UTC>","http_status":200}}. Do NOT edit anchor.json or claims.ots.
4. Run the frozen command WITHOUT --controls (venv python, --source a fresh shared clone of {LANE} at its
   current tip, --work your scratch) and record stdout+exit. If a leg fails, report exactly which and why —
   do not patch anything.
5. If the proof is STILL pending after your retries, say so explicitly with the last upgrade output; the L1
   finishes confirmation post-wave. Never fabricate a receipt: a receipt whose bytes you did not fetch is a
   fabrication-class finding against yourself.
# Acceptance
header.bin (80 bytes) + two agreeing receipts from two distinct sources exist in your wave dir (copies) and, when
step 3 wrote them, in the anchor dir; the verify run output and exit code are in your report; upgrade logs included.
""")

add("E2LedgerRefine", "executor", B, f"""# Target
kengaku round 54 seat E2LedgerRefine (executor). R54-C2 calibration axis.
# Item
Refine the truthful reasons of RED rows in the committed entrytruth ledger.
1. Read {LANE}/plans/round54-entrytruth.json. For every row with entry_state=="red": run its entry_argv yourself
   (hermetic env: python3 -c helper or reuse {LANE}/plans/round54_c2_entrytruth.py hermetic_env via a small driver
   in your scratch) in a shared clone of {LANE} at its current tip; read the actual output.
2. Write a refined ledger copy {LANE}/.ufo/waves/round-54/w1/E2LedgerRefine/round54-entrytruth-refined.json where
   ONLY the "reason" (>=10 real words naming the actual cause, e.g. 'the gate requires --summary; bare entry mode
   prints usage') and "evidence" (verbatim fragment from YOUR observed output) fields differ. NEVER change
   entry_argv, entry_exit or entry_state — those are measured values from the frozen builder; a mismatch between
   your observation and the declared exit is a FINDING (report name, declared, observed), not an edit.
3. Sanity: python3 - <<'EOF' json.load your file; count red rows; print any row where your observed exit differs
   from the declared one.
# Acceptance
refined ledger in your wave dir + the mismatch list (expected: none) + 3 example before/after reason pairs.
""")

add("E3R52RegistryFix", "executor", X, f"""# Target
kengaku round 54 seat E3R52RegistryFix (executor). Routed-defect repair (logged work, NOT a scored claim):
the round-52 carried fixes named by two verifier spot-checks.
# Item
1. Read {LANE}/corpus/lessons/round-52-verifier-spotcheck.md and {LANE}/corpus/lessons/round-53-verifier-spotcheck.md
   item 7 ('SELFTEST-UNBACKED negation fix, K5/K7 unfrozen controls') and {LANE}/plans/round52_c2_registry.py +
   {LANE}/plans/round52_c2_registry.py --selftest.
2. Implement, IN YOUR WAVE DIR ({LANE}/.ufo/waves/round-54/w1/E3R52RegistryFix/), a patched copy of
   round52_c2_registry.py that fixes the span-scoped SELFTEST-UNBACKED negation (a gate whose advertised selftest
   is unbacked must be flagged for the whole advertised span, not only where the checker last looked) and adds the
   K5/K7 controls as committed control fixtures with red expected values. Run old vs patched --selftest and one
   live --lane run each; record both outputs.
3. Red-before: show the OLD counter missing the defect the patch catches (command + output), then the patched one
   catching it. Diff old vs patched: the only delta is the fix + controls.
4. Do NOT write inside the lane tree outside your wave dir. The L1 integrates the patch after review.
# Acceptance
patched counter + control fixtures + red/green receipts in your wave dir; one-paragraph description of the exact
negation bug and its fix.
""")

add("E4MigrationAudit", "executor", B, f"""# Target
kengaku round 54 seat E4MigrationAudit (executor). R54-C2 MIGRATION leg.
# Item
Compute and justify the MIGRATION numbers the landing will report.
1. Load {LANE}/plans/round53-tipstate.json (r53 declarations) and {LANE}/plans/round54-entrytruth.json.
   Compute: rows where r53 declared green with kind in (selftest, help) AND the entrytruth row declares
   entry_state red (call each a REDECLARED row); rows where r53 declared green kind=entry AND entrytruth red
   (a REGRESSION candidate — must be empty; if not, report as a finding, never edit).
2. For every REDECLARED row: one line with r53 argv/kind vs entry argv/exit and the red reason — this is the
   laundered-then-honest backlog. Save {LANE}/.ufo/waves/round-54/w1/E4MigrationAudit/migration.json +
   migration.md (counts + table). Print the total count as 'REDECLARED <n>'.
3. Cross-check 5 sampled rows against the live registry script cells (name, script path) — mismatches are findings.
# Acceptance
migration.json + migration.md with the counts and the 5-row cross-check; numbers pasted in your report.
""")

add("E5CensusGate", "executor", X, f"""# Target
kengaku round 54 seat E5CensusGate (executor). Frontier-step infrastructure + assimilation guard.
# Item
1. Assimilation id-collision check (addendum §10, receipt only, no registry writes): run EXACTLY the commands in
   {LANE}/plans/round-54-claims.md §'Id collision' — i.e.
   A={LANE}/.ufo/waves/round-54/assimilation; mkdir -p "$A";
   grep -oE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}' {LANE}/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids";
   same over /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md > "$A/staged-ids";
   comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"; wc -l all three; paste the counts.
2. Interpret: collisions nonempty and how large. If > 20 collisions write the sentence 'MASS-ID-DRIFT: adoption
   closed this round; L0 question owed' plus the top-5 colliding ids. Copy the three files into your wave dir as
   receipts. Do NOT edit SOURCES.md or any shokuknow file (read-only external root).
3. Census tooling receipt: run
   /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku;
   record exit code + last line + the W04 warning count. Save as census-mid.txt in your wave dir.
4. Prove the guard once (Q42-style): in scratch build a mini registry with one 3-space-indented row whose id
   collides with a staged id, run the same grep pipeline on it, and show the collision IS caught (the 0-3-space
   anchor works); paste command + output.
# Acceptance
receipts (reg-ids/staged-ids/collisions counts, census-mid.txt, mini-registry proof) in your wave dir.
""")

# ---------------- executors: ledger row audits (26 seats x 3 rows)
REG_ROWS = ["adoption-check", "anchor-digest-check", "attrib-probe", "benchmark-spec-audit", "build-pmars-probe",
            "catalog-probe", "config-projection", "constraints-probe", "coverage-census", "db-wal-probe",
            "defect-ledger", "extraction-policy-compare", "feal-linear-probe", "feal-probe", "fibsqrt-probe",
            "gate-flip-check", "gate-timing", "git-leak-probe", "git-webserver-probe", "grader-perturb",
            "hermetic-grader", "interval-reverdict", "ledger-tip", "mutant-direction-check", "order-check",
            "package-gate", "password-recovery-probe", "polyglot-c-py-probe", "regex-log-probe",
            "registry-reference-check", "round-close-check", "round28-census", "round30-defects",
            "round31-c1-literals", "round31-defects", "round33-c1-literals", "round33-defects",
            "round35-c1-coverage", "round35-hardening", "round36-c1-battery", "round36-c2", "round37-c1-mutants",
            "round37-c2", "round38-c1-mutants", "round38-c2", "round39-c1-audit", "round39-c1-mutants",
            "round39-c2", "round40-c1-mutants", "round40-c2", "round41-c1-mutants", "round41-c2",
            "round42-c1-mutants", "round42-c2", "round43-c1-mutants", "round43-c2", "round44-c1-mutants",
            "round44-c2", "round45-c1", "round45-c2", "round46-c1", "round46-c2", "round46-c3", "round50-c1",
            "round50-c2", "round51-routing", "round51-surfaces", "round52-c1", "round52-c2", "round53-c1",
            "round53-c2", "routed-findings", "scratch-root-guard", "sources-adopt", "stage-scan",
            "state-assertion-check", "tb2-grader-probe", "tip-receipts"]
for i in range(26):
    chunk = REG_ROWS[i * 3:(i + 1) * 3]
    add(f"E6RowAudit{i+1:02d}", "executor", B, f"""# Target
kengaku round 54 seat E6RowAudit{i+1:02d} (executor). R54-C2 re-verification duty: rows {chunk}.
# Item
Independent re-execution audit of three committed ledger rows (frozen builder measured them; you re-derive).
1. Read your three rows in {LANE}/plans/round54-entrytruth.json (entry_argv, entry_exit, entry_state, reason,
   evidence) and the matching SKILL.md registry cells.
2. In a shared clone of {LANE} at its current tip (scratch), run each row's entry_argv under the counter's
   hermetic env (driver script in your scratch importing
   {LANE}/plans/round54_c2_entrytruth.py hermetic_env; TMPDIR under your scratch). timeout 600 per row.
3. Per row record: declared exit vs your observed exit, and whether the declared evidence fragment (red rows)
   appears in your observed output. A row is CONFIRMED only when both match. Mismatches and unrun rows are
   findings with the exact command + output tail.
4. Also verify the argv is entry mode (no --selftest/--help/--dry/--version) and the script path exists in the
   clone. Save {LANE}/.ufo/waves/round-54/w1/E6RowAudit{i+1:02d}/audit.json + audit.md.
# Acceptance
audit.json with 3 verdict lines (name, declared, observed, fragment-match, verdict) + commands in audit.md;
paste the 3 verdicts in your report.
""")

# ---------------- executors: no-harm + capability + determinism + digest chain (4)
add("E7NoharmR53C1", "executor", X, f"""# Target
kengaku round 54 seat E7NoharmR53C1 (executor). No-axis-harm evidence: the frozen r53 C1 triage at the landing tip.
# Item
1. Shared clone of {LANE} at its current tip (scratch). Run
   python3 plans/round53_c1_triage.py --lane . --work <scratch> (see its argparse for exact flags; use --help
   first) and record stdout + exit. Expected: the r53 frozen predicate still passes at the tip (PINS 183,
   ORACLE 305/305, prior-art rows 20, PREDICATE R53-C1 pass, exit 0) — the round-54 work must not have moved it.
2. If anything changed vs the r53 final receipt (compare with {LANE}/.ufo/waves/round-53/claims/c1-final.txt
   values), report the exact differing lines as findings. NEVER edit any file.
3. Also run plans/round53_c1_triage.py --selftest (or its documented equivalent) and record.
# Acceptance
both outputs + exit codes in your report; one line 'R53-C1 at landing tip: UNCHANGED|CHANGED (details)'.
""")

add("E8NoharmR53C2", "executor", B, f"""# Target
kengaku round 54 seat E8NoharmR53C2 (executor). No-axis-harm evidence: the frozen r53 C2 tip-state counter.
# Item
1. Shared clone of {LANE} at its current tip (scratch). Run
   python3 plans/round53_c2_tipstate.py --lane . --source <clone> --work <scratch> --jobs 3 --timeout 900
   and record stdout + exit (this executes 78 declared argvs — expect several minutes; do not interrupt).
2. Expected: the r53 frozen predicate still passes at the tip (executed=78 mismatched=0 evidence_missing=0,
   declared green 66 / red 12 — values may shift ONLY if a declared argv's exit genuinely moved; any shift is a
   finding with the row name, never an edit). Compare with {LANE}/.ufo/waves/round-53/claims/c2-final.txt.
3. Note in one line whether SKILL.md, plans/round53-tipstate.json and plans/round53_c2_tipstate.py are
   byte-identical to {LANE} at 17f90355 (git diff --stat 17f90355..HEAD -- SKILL.md plans/round53-tipstate.json
   plans/round53_c2_tipstate.py must be empty).
# Acceptance
counter output + exit; the diff --stat line; one line 'R53-C2 at landing tip: UNCHANGED|CHANGED (details)'.
""")

add("E9CapabilityRun", "executor", A, f"""# Target
kengaku round 54 seat E9CapabilityRun (executor). Capability demonstration: externally-anchored freeze.
# Item
Produce the end-to-end demonstration a capabilities-table row needs (AXES.md: a row enters only through a round
that demonstrates the capability RUNNING).
1. In scratch: copy the anchor dir to your scratch, then run the FULL frozen command including --controls with
   --source a fresh shared clone of {LANE}: record stdout + exit. The controls section must print
   'CONTROLS forged=4 failed=4'.
2. Determinism: run the same command 5 times; stdout must be identical across runs except no variable content
   (there should be none — the counter prints no timestamps; verify byte-equality with cmp/sha256 over the 5
   outputs). Paste the 5 hashes.
3. Forged-integrity bonus (read-only): flip byte 5 of a COPY of claims.ots in scratch and show verify (with
   --controls pointed at your scratch anchor copy via --anchor) fails; restore nothing in the lane tree.
4. Save everything under {LANE}/.ufo/waves/round-54/w1/E9CapabilityRun/ (receipts + the 5 hashes).
# Acceptance
one capability line 'externally-anchored freeze: runs, verifies, controls fail-as-required (receipts at ...)'.
""")

add("E10DigestChain", "executor", A, f"""# Target
kengaku round 54 seat E10DigestChain (executor). C1 BINDING leg deep-check.
# Item
1. Verify the digest chain independently of the counter: compute sha256 of
   `git -C <shared clone of {LANE}> show 17f90355c3ec17dcf15f7980d83f1943ae428fe5:plans/round-54-claims.md`;
   of the same path at the current tip; of the working file at {LANE}/plans/round-54-claims.md; and read the
   digest recorded in {LANE}/corpus/evidence/round54/anchor/anchor.json. All four must equal
   d7aa05c8fcd4aff2ec6f1b606c4e5072d1082b51da8d1c091e2ed1df0d995eb8. Paste each computed digest.
2. Parse the proof independently (venv python + opentimestamps library in YOUR scratch): print the proof's
   file digest, the set of attestations by type, and — if the Bitcoin attestation is present — its height.
   Report whether the file digest matches the chain and whether the attested digest is reachable from the file
   digest by walking the op tree (write your own 20-line walker; do not reuse the counter's).
3. Confirm plans/round-54-claims.md has exactly one commit touching it since 6c919180
   (git log --oneline 6c919180..HEAD -- plans/round-54-claims.md) — the freeze is single-commit, never amended.
4. Save the walker script + outputs in your wave dir.
# Acceptance
four digests, the independent walker output, and the single-commit proof in your report.
""")

# ---------------- scribes (3)
add("S1KnowledgeEntry", "scribe", A, f"""# Target
kengaku round 54 seat S1KnowledgeEntry (scribe). Draft the C1 knowledge entry.
# Item
Draft {LANE}/.ufo/waves/round-54/w1/S1KnowledgeEntry/external-anchor-freeze.md — a corpus/knowledge entry in
the lane's house style (read 2-3 existing entries first, e.g. corpus/knowledge/tb2-presence-only-triage.md and
corpus/knowledge/fixture-honest-geometry.md): opens with the provenance trio (source: S-rows to be S198+ —
placeholder ids marked TBD with the URL; verified-at: 2026-10-30; recheck: 180d), then:
- the construct: a measurement freeze witnessed outside the lane's writable state (OpenTimestamps ->
  Bitcoin block header), what it removes (the coordinated-history forgery of w3/C1CritOracle2), and what it does
  NOT claim (no content audit, no anti-reorg absolutism beyond Bitcoin consensus, explorer receipts are fetched
  witnesses not trustless verification);
- the instrument: plans/round54_c1_anchor.py legs (BINDING/ATTESTATION/EXTERNAL-PIN/CONTROLS) with the frozen
  command, the four controls, and the falsification conditions;
- measured facts ONLY with their commands (digest d7aa05c8..., stamp time, attestation height if known, ledger
  REDECLARED count TBD-marked);
- limits + a falsifiable claim sentence. Bounded, no universal clauses. 60-90 lines max.
# Acceptance
the draft file + a 5-line summary of what it claims and cites.
""")

add("S2SourcesRows", "scribe", B, f"""# Target
kengaku round 54 seat S2SourcesRows (scribe). Draft the SOURCES.md rows opened this round.
# Item
Draft {LANE}/.ufo/waves/round-54/w1/S2SourcesRows/rows.md with candidate registry rows (11-column contract,
CORPUS.md 'SOURCES.md' section) for the sources ACTUALLY OPENED this round for C1's prior-art leg. Read
{LANE}/corpus/SOURCES.md first for the exact schema and existing ids (next id is S198; never invent ids — mark
'TBD-S198' style placeholders; the L1 assigns). For each row: id, source title + canonical URL, kind (docs/paper/
tool/spec), tier (A for primary OTS docs/spec; B for expert write-ups), scope, anchor (exact section + revision +
access date), teaches (one grounded benefit), status mined, opened 2026-10-30, recheck (180d/on-release), used-by
(the knowledge entry path). Candidates (open each BEFORE writing its row; a row is a claim):
- https://opentimestamps.org/ (landing page + docs links)
- https://github.com/opentimestamps/opentimestamps-client (README: verify/upgrade semantics)
- https://github.com/opentimestamps/python-opentimestamps (core: BitcoinBlockHeaderAttestation, merkle ops)
- any preregistration/timestamping source the scouts fetched (coordinate with their wave-dir receipts; cite the
  seat's fetched-bytes path). Include for each: the <=25-word located quote + its exact location (the Gate-block
  material). 3-6 rows expected. No credential material. Every cell must survive the 11-column parse (no | in cells).
# Acceptance
rows.md with 3-6 draft rows + per-row Gate block (URL, access date 2026-10-30, located quote + location).
""")

add("S3LessonLogDrafts", "scribe", X, f"""# Target
kengaku round 54 seat S3LessonLogDrafts (scribe). Draft the round-54 lesson skeleton and LOG entry.
# Item
1. Read {LANE}/corpus/lessons/round-53.md (shape to mirror) and the frozen claims file. Draft
   {LANE}/.ufo/waves/round-54/w1/S3LessonLogDrafts/round-54.md: sections Gate (candidates/admitted/rejected with
   reasons — mark TBD where measurement pending), Mistakes (one row PRE-FILLED: class selected-argv-laundering ·
   evidence .ufo/waves/round-53/w3/C2CritPredicate2.md + claims/c2-route-r53.txt · captured-by Q42/Q43 · fix =
   plans/round54_c2_entrytruth.py, counted only once shown able to fail — cite the route receipt as the red-before),
   Limits, Assimilation (TBD: expect 'none — mass id drift' per E5's receipts).
2. Draft LOG.md append text (LOG round-54 entry): what the round declared, the freeze commit, the anchor digest,
   wave shape TBD, verdicts TBD. House style: read LOG.md's round-53 entry first.
3. Draft the SCORECARD round-54 section skeleton (claims table with before→after cells marked MEASURED-TBD).
   Save as scorecard-draft.md.
# Acceptance
three draft files; no numbers invented — every unfilled cell carries TBD + the command that will fill it.
""")

# ---------------- scouts (5)
add("SC1PriorArt", "scout", A, f"""# Target
kengaku round 54 seat SC1PriorArt (scout). C1 prior-art pricing (the novelty leg's fetched URLs).
# Item
Bounded search, question: 'Is anchoring research/measurement preregistration digests in a public blockchain
(OpenTimestamps or equivalent) published practice?' Search arXiv + web (site:arxiv.org opentimestamps;
blockchain-anchored preregistration; 'OpenTimestamps' research data timestamping; OSF preregistration timestamp
integrity). Fetch 3-6 primary pages (receipts: save each URL's bytes or an excerpt + access date + located quote
into your wave dir fetched/). For each fetched source write a verdict line: what it documents and whether it
covers (a) anchoring a digest before measurement, (b) verifying via block header + explorer receipts, (c) use for
adversarial integrity of an eval pipeline's freeze. Verdicts: known / adjacent / not-found — with quotes. A
negative claim carries its sweep (queries + counts + stop rationale). Save
{LANE}/.ufo/waves/round-54/w1/SC1PriorArt/prior-art.md.
# Acceptance
prior-art.md with >=3 fetched URLs, quotes, verdicts; the sweep counts pasted in your report.
""")

add("SC2OtsDocs", "scout", A, f"""# Target
kengaku round 54 seat SC2OtsDocs (scout). Open the OpenTimestamps primaries for the SOURCES rows.
# Item
Fetch and open (receipts under {LANE}/.ufo/waves/round-54/w1/SC2OtsDocs/fetched/): https://opentimestamps.org/,
https://github.com/opentimestamps/opentimestamps-client (README), https://github.com/opentimestamps/python-opentimestamps
(README + core/notary.py BitcoinBlockHeaderAttestation docstring). For each: exact URL + access date 2026-10-30 +
one <=25-word located quote with its location (file/section) + what it teaches for C1 (tier A candidates: primary
docs/source). Also fetch one independent explanation of Bitcoin merkle verification (e.g. developer.bitcoin.org
reference or bitcoin wiki 'Block hashing algorithm') — quote the merkle-root field location in an 80-byte header.
Save rows-material.md with one block per source. No login walls; skip anything behind one.
# Acceptance
rows-material.md with 4+ source blocks (URL, date, quote, location, teaches) + fetched bytes/paths.
""")

add("SC3ForgeRead", "scout", X, f"""# Target
kengaku round 54 seat SC3ForgeRead (scout). Attack-vector map: what the round-53 attacks actually showed.
# Item
Read {LANE}/.ufo/waves/round-53/w3/C1CritOracle2.md and C2CritPredicate2.md IN FULL (and skim
C1CritNeverRead.md for scope hygiene). Produce {LANE}/.ufo/waves/round-54/w1/SC3ForgeRead/vectors.md: a numbered
vector table — for each demonstrated attack: (a) what it did, (b) which C1/C2 leg or control now covers it (name
the exact leg: BINDING / ATTESTATION / EXTERNAL-PIN / CONTROLS-a-d; entry-mode argv / hermetic env / LAUNDERED
branch / EVIDENCE fragment), (b2) whether that coverage is claimed in plans/round-54-claims.md (quote the line),
(c) any vector NO leg covers (a routed gap — the critics will try to reproduce these). No fixes; mapping only.
# Acceptance
vectors.md with the table; gaps list pasted in your report.
""")

add("SC4BtcHeader", "scout", A, f"""# Target
kengaku round 54 seat SC4BtcHeader (scout). Ground-truth for the EXTERNAL-PIN leg.
# Item
1. Independently confirm the block whose height you can read from the anchor proof IF already confirmed
   ({LANE}/corpus/evidence/round54/anchor/claims.ots — parse height with the venv library, else report pending):
   fetch the block hash + header hex from https://mempool.space/api/block-height/<H> and
   https://blockstream.info/api/block/<hash>/header, and a third source https://api.blockchain.info/hblock?... or
   https://blockchain.info/rawblock/<hash> (whichever answers; record exact URLs). Compare sha256d(header) (double
   sha256, display = reversed hex) against the hash each source reports — the derivation itself is the check.
2. Write {LANE}/.ufo/waves/round-54/w1/SC4BtcHeader/header-check.md: source URLs, fetch times, header hex,
   computed sha256d, agreement table. If the proof is pending: document the derivation on the LATEST block instead
   (height from mempool.space/tips) so the math is still evidenced, and say the C1 block check is pending.
# Acceptance
header-check.md with the derivation table; pasted conclusion line.
""")

add("SC5SpotcheckDebt", "scout", X, f"""# Target
kengaku round 54 seat SC5SpotcheckDebt (scout). Round-53 spot-check debts this round must honor.
# Item
Read {LANE}/corpus/lessons/round-53-verifier-spotcheck.md items 1-10. For each of items 1, 2, 3, 4, 7 (C1
integrity, argv laundering + git-config contamination, never-read vs never-examined, incomplete mutation
detectors, carried r52 fixes): one row naming (a) the debt, (b) which round-54 artifact addresses it (counter leg,
control, E3's patch, mutation seats) or 'not addressed this round' with the reason. Also confirm item 6 (coverage
cap L0s) is still unanswered in /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md (grep the three kengaku
questions; quote their lines). Save {LANE}/.ufo/waves/round-54/w1/SC5SpotcheckDebt/debts.md.
# Acceptance
debts.md with the five coverage rows + the L0 grep evidence.
""")

# ---------------- reviewers (4)
add("R1C1Counter", "reviewer", A, f"""# Target
kengaku round 54 seat R1C1Counter (reviewer). Correctness review of plans/round54_c1_anchor.py against the
frozen claims file (READ plans/round-54-claims.md §Claim 1 first).
# Item
1. Line-by-line review of {LANE}/plans/round54_c1_anchor.py: does every predicate leg in the claims file map to
   code that actually runs? Name each leg -> function -> line. Flag: legs claimed but not implemented; checks a
   forged input could bypass; silent except-blocks that swallow a failure into success; the time-ordering legs
   (stamped_at skew, block_time < now); the CONTROLS wiring (does a control that passes actually fail the
   predicate?).
2. Run --selftest (venv python at /fast/scratch/hyaku/kengaku-r54/l1/venv/otsenv/bin/python) and confirm 8/8;
   then review each selftest case: does it test what its name says? A case that cannot fail is a finding.
3. Review the ATTESTATION walk (_collect_digests): does it reject a tree whose attested digest is unreachable
   from the file digest? Write a 30-line adversarial check in scratch if needed (no lane edits).
4. Save {LANE}/.ufo/waves/round-54/w1/R1C1Counter/review.md with findings classified BLOCKER/MAJOR/MINOR/NIT.
# Acceptance
review.md with the leg->code map table + classified findings; blockers pasted in your report.
""")

add("R2C2Counter", "reviewer", B, f"""# Target
kengaku round 54 seat R2C2Counter (reviewer). Correctness review of plans/round54_c2_entrytruth.py +
plans/round54_c2_controls.py + plans/round54_build_entrytruth.py against plans/round-54-claims.md §Claim 2.
# Item
1. Leg map: REGISTRY / LEDGER / EXEC / MIGRATION / ENV — each claims-file leg -> code -> line. Flag gaps: e.g.
   can a declared green row with a modified-then-restored argv slip through (chosen-field trust)? Is entry_mode_ok
   bypassable (uv wrapping, flag case, '=' forms, argv after '--')? Does hermetic_env actually scrub all GIT_*
   vars (including GIT_CONFIG_COUNT_) and pin the rest? Is TIMEOUT counted as mismatch (it must fail the
   predicate)?
2. Run --selftest (expect 7/7) and --dry against {LANE} (the committed ledger) and record.
3. Review the builder's candidate selection for a bias that would mislabel an entry (e.g. preferring exit 0 of a
   --summary variant when the true bare entry is broken) — is 'chosen' recorded honestly?
4. Save {LANE}/.ufo/waves/round-54/w1/R2C2Counter/review.md; findings BLOCKER/MAJOR/MINOR/NIT.
# Acceptance
review.md + the two run receipts; blockers pasted.
""")

add("R3KnowledgeSources", "reviewer", A, f"""# Target
kengaku round 54 seat R3KnowledgeSources (reviewer). Review the drafted knowledge entry + SOURCES rows drafts
against the corpus bars.
# Item
Read {LANE}/corpus/QUALITY.md (Q1-Q8, Q26, Q34) and CORPUS.md rules. Then review
{LANE}/.ufo/waves/round-54/w1/S1KnowledgeEntry/external-anchor-freeze.md and S2SourcesRows/rows.md:
- provenance trio present and correct-shaped? counts carry commands? quotes located (<=25 words, named spot)?
- no credential material, no universal clauses, falsifiable or marked opinion;
- SOURCES rows: 11-column parse (write the awk NF!=13 check over the draft rows), tier justified, no | in cells,
  id placeholders do not collide with real ids, used-by paths plausible;
- overclaim hunt: any sentence asserting more than a committed receipt shows (e.g. 'unforgeable') is a finding —
  propose the bounded wording instead.
Save {LANE}/.ufo/waves/round-54/w1/R3KnowledgeSources/review.md with per-file verdict + findings.
# Acceptance
review.md; every finding quotes the offending line and proposes replacement text.
""")

add("R4R52Fix", "reviewer", X, f"""# Target
kengaku round 54 seat R4R52Fix (reviewer). Review E3R52RegistryFix's patched counter before the L1 integrates it.
# Item
Read {LANE}/.ufo/waves/round-54/w1/E3R52RegistryFix/ (patched round52_c2_registry.py + controls + receipts).
Verify: (a) diff vs the original is exactly the span-scoped negation fix + K5/K7 controls — nothing else moved;
(b) the red-before receipt actually shows the old counter missing the defect and the patched one catching it
(re-run both yourself in scratch on the same fixture if the receipts are unclear); (c) the patched --selftest
still covers all old cases (count them) and the new ones; (d) the fix does not alter any verdict for currently
green rows (run the patched counter --dry --lane {LANE} in scratch; must equal the old counter's --dry output).
Save {LANE}/.ufo/waves/round-54/w1/R4R52Fix/review.md with verdict INTEGRATE / DO-NOT-INTEGRATE + reasons.
# Acceptance
review.md with the verdict and the evidence commands.
""")

# ---------------- critics (5)
add("C1Forge", "critic", A, f"""# Target
kengaku round 54 seat C1Forge (critic). Falsify R54-C1: make a forged anchor pass. All work in scratch; nothing
in the lane tree is edited; the frozen counter is imported unmodified.
# Item
Read plans/round-54-claims.md §Claim 1. Attack {LANE}/plans/round54_c1_anchor.py:
1. Byte surgery on a COPY of claims.ots (scratch): flips in op args, in the attestation height varuint, in the
   pending-attestation URIs; truncations; appended trailing garbage. Goal: any mutation that still verifies.
2. Substitute digests: run verify against a claims file you modified in your scratch clone (digest mismatch must
   fail — prove it); a real proof over a DIFFERENT file (must fail BINDING).
3. Time attacks: set anchor.json stamped_at to a value AFTER the block time (must fail TIME); to a value far
   before (must pass skew but is that meaningful? report what the skew actually proves).
4. Header attacks: a header.bin with a flipped merkle-root byte (must fail); a header from a different block
   (must fail EXTERNAL-PIN against receipts).
Every attack: command + output + verdict 'blocked by <leg>' or 'PASSED (CLAIM-DEAD <detail>)'. A pass you can
reproduce twice is a kill shot — report it prominently. Save {LANE}/.ufo/waves/round-54/w1/C1Forge/attacks.md.
# Acceptance
attacks.md with the full matrix; any PASSED result pasted first in your report.
""")

add("C2Launder", "critic", B, f"""# Target
kengaku round 54 seat C2Launder (critic). Falsify R54-C2: build a ledger row that passes the r54 counter while
its true entry behaviour disagrees with the declaration.
# Item
Read plans/round-54-claims.md §Claim 2 + the counter's static legs. Attack in scratch with fixture lanes:
1. Argv shapes: ['uv','run','python3',script], ['python3',script,'--summary'] (a mode whose exit differs from
   bare), ['python3','-O',script], flags after '--', '--lane=.' form, unicode look-alikes of '--selftest'. Does
   entry_mode_ok admit any argv that is NOT the plain entry? Does the counter's hermetic run then disagree with
   what a stranger running the registry cell would see?
2. Ledger tricks: extra fields the counter ignores (does 'kind' exist in r54 schema? a row claiming
   entry_state green with entry_exit 0 while a '--summary' arg makes it green but the bare entry red); duplicate
   JSON keys (the no_dup hook — does it fire?); a row whose script differs in case from the registry cell.
3. Env tricks: a fixture gate reading GIT_CONFIG_COUNT/GIT_CONFIG_KEY_0 (multi-key config injection) or
   .git/config INSIDE the clone (repo-local config is NOT scrubbed — is that a hole the claims file's wording
   covers? quote the exact frozen sentence and judge honestly).
Each: command + output + verdict 'closed by <leg>' or 'PASSED (CLAIM-DEAD <detail>)'. Save
{LANE}/.ufo/waves/round-54/w1/C2Launder/attacks.md.
# Acceptance
attacks.md matrix; PASSED results pasted first.
""")

add("C3ClaimsSizing", "critic", X, f"""# Target
kengaku round 54 seat C3ClaimsSizing (critic). Falsify the CLAIMS THEMSELVES before landing.
# Item
Read {LANE}/plans/round-54-claims.md end to end, then {LANE}/SCORECARD.md's round-52/53 sections + §Scoring rubric.
1. Do the declared before→after + counting commands bind what the SCORECARD rows will say? Find any sentence a
   do-nothing control also satisfies (C1 before receipt is 'anchor absent' — could a round that does nothing
   produce the same receipt and still pass some leg? Quote which).
2. Universal-clause hunt: 'every artifact pointer', 'no axis harmed' — is the harm check enumerated (which axes,
   which commands) or asserted?
3. Novelty leg: does C1 satisfy the rubric's three legs as written (new construct the lane could not previously
   observe / in-repo instrument / prior-art verdict with fetched URL)? Which leg is weakest and what evidence
   will decide it (cite the rubric line)?
4. Causally separable: name the exact commands that verify C1 with C2 reverted (git revert of the C2 files) and
   vice versa; if you cannot, that is a finding.
5. Lowest-axis rule: coverage 7 capped by open L0s — verify the cap questions are really open (grep
   /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md) and the round's §Axis choice honestly states the route-around.
Save {LANE}/.ufo/waves/round-54/w1/C3ClaimsSizing/sizing.md.
# Acceptance
sizing.md findings; the separability commands pasted.
""")

add("C4MigrationHonesty", "critic", B, f"""# Target
kengaku round 54 seat C4MigrationHonesty (critic). Audit the MIGRATION story: no row silently greened.
# Item
1. From {LANE}/plans/round53-tipstate.json + round54-entrytruth.json build the 78-row cross table (r53
   kind/state/exit vs r54 entry argv/state/exit). Any row where r53 declared green (any kind) and r54 declares
   green via a DIFFERENT argv — is the green claim still true at the entry argv? (E4's migration.json covers
   red ones; you hunt the green ones: a row green at --selftest and green at entry is fine; green at selftest
   but entry_argv declared from a --summary variant with exit 0 while bare entry is red is laundering-in-place.)
2. Sample 8 green-at-entry rows and re-run their entry argv hermetically in a scratch clone: confirm exit 0.
3. Check every red entrytruth row: reason >=10 words, evidence fragment verbatim in a re-run output (3 sampled).
4. REDECLARED count: recompute it yourself from the two ledgers; it must equal E4's number (cross-check when its
   file exists; else compute and save yours for the L1).
Save {LANE}/.ufo/waves/round-54/w1/C4MigrationHonesty/audit.md with the cross table summary + verdicts.
# Acceptance
audit.md; any laundering-in-place row pasted as CLAIM-DEAD evidence.
""")

add("C5Separability", "critic", X, f"""# Target
kengaku round 54 seat C5Separability (critic). Prove or break claim separability and the harm check.
# Item
1. Simulate C2 reverted: in a scratch clone at the current tip, delete plans/round54-entrytruth.json +
   plans/round54_c2_entrytruth.py + plans/round54_c2_controls.py + plans/round54_build_entrytruth.py (scratch
   copy only) — does the C1 frozen command still run to its predicate (anchor legs independent of those files)?
   Run it; paste output. Then the reverse: delete anchor dir + plans/round54_c1_anchor.py — does the C2 counter
   still run (--dry + full run in scratch)? Paste.
2. No shared production bytes: git diff 17f90355..HEAD --stat — list every file the round touched and mark which
   claim (if any) owns it; a file owned by both is a finding (claims file says none must exist).
3. Harm check enumeration: which non-claimed axes could this round's landing move? Name the command that would
   show each unchanged (freshness: surface probes; depth: SKILL.md line count; operability: registry --dry;
   adjacency: PROVINCE diff). Run the cheap ones and paste.
Save {LANE}/.ufo/waves/round-54/w1/C5Separability/separability.md.
# Acceptance
separability.md with both revert-run outputs and the harm-command table.
""")

# ---------------- mutation-testers (4)
add("M1C1Mutants", "mutation-tester", A, f"""# Target
kengaku round 54 seat M1C1Mutants (mutation-tester). Mutation battery for plans/round54_c1_anchor.py.
# Item
Write >=10 witnessed mutants (copies in scratch; the lane file is never edited): (1) skip the merkle-root
comparison; (2) accept Litecoin/pending attestations as bitcoin; (3) drop the height floor; (4) drop the
stamped_at skew check; (5) accept any single explorer receipt; (6) skip the double-sha256 -> receipt-hash
comparison; (7) treat verify exceptions as pass in controls; (8) weaken BINDING to prefix-match; (9) drop the
freeze-rev ancestor check; (10) compare digest against HEAD only (drop freeze rev). For each: kill direction
(silence/mirror, Q29/Q33 style), the selftest/control case that must catch it, and the observed run: mutant rc +
which check fired. A mutant no committed check catches is a SURVIVOR — the finding names the missing case.
Save {LANE}/.ufo/waves/round-54/w1/M1C1Mutants/mutants.md + mutant patches.
# Acceptance
mutants.md table (id, mutation, direction, detector, result); survivors listed first.
""")

add("M2C2Mutants", "mutation-tester", B, f"""# Target
kengaku round 54 seat M2C2Mutants (mutation-tester). Mutation battery for plans/round54_c2_entrytruth.py.
# Item
>=10 witnessed mutants (scratch copies): (1) entry_mode_ok allows --selftest; (2) allows --help; (3) hermetic_env
keeps caller GIT_CONFIG_GLOBAL; (4) skips the empty-gitconfig pin; (5) LAUNDERED branch removed (falls into
MISMATCH only — does any leg then fail? the predicate must still fail via laundered>0 OR mismatch>0: which?);
(6) evidence check dropped for red rows; (7) TIMEOUT counted as green; (8) extra rows in ledger ignored; (9)
missing rows tolerated (missing>0 still passes); (10) clean-tree check dropped. For each: direction + the
selftest case or control expected to kill it + observed result. Survivors named with the missing case.
Save {LANE}/.ufo/waves/round-54/w1/M2C2Mutants/mutants.md + patches.
# Acceptance
mutants.md table; survivors first.
""")

add("M3BuilderMutants", "mutation-tester", B, f"""# Target
kengaku round 54 seat M3BuilderMutants (mutation-tester). Mutation battery for
plans/round54_build_entrytruth.py (the ledger's provenance).
# Item
>=6 witnessed mutants (scratch copies, fixture lane of 3-4 gates in scratch): (1) prefer exit 0 candidate even
when it is the --summary variant (mislabeled entry); (2) treat TIMEOUT as exit 0; (3) drop 'chosen' honesty
(always 'r53-entry'); (4) evidence fragment taken from the wrong candidate's output; (5) red reason auto-filled
below 10 words; (6) skip the second candidate entirely when the first exits 2 (usage). For each: does the committed
ledger show the corruption (would R2/C4/E2 catch it)? Name the detector or the missing one.
Save {LANE}/.ufo/waves/round-54/w1/M3BuilderMutants/mutants.md + patches.
# Acceptance
mutants.md table; survivors first.
""")

add("M4R52FixMutants", "mutation-tester", X, f"""# Target
kengaku round 54 seat M4R52FixMutants (mutation-tester). Mutation-test E3's patched registry counter.
# Item
After E3R52RegistryFix lands its files: >=6 witnessed mutants of the patched counter (scratch copies): remove the
span-scoping (revert to the old bug), weaken K5, weaken K7, skip the new control fixtures, invert the new
negation, treat unbacked-selftest as warning-only. For each: red/green expected vs observed (the K5/K7 fixtures
must catch (1)(2)(3)(5); the selftest must catch (4)(6) if E3 added cases). Survivors = E3 must extend before the
L1 integrates. Save {LANE}/.ufo/waves/round-54/w1/M4R52FixMutants/mutants.md.
# Acceptance
mutants.md; if E3's files are absent when you run, say so and mutate the ORIGINAL counter to reconfirm the old
bug's shape (still useful evidence).
""")

# ---------------- sentinels (2)
add("SN1OtsNetwork", "sentinel", A, f"""# Target
kengaku round 54 seat SN1OtsNetwork (sentinel). Safety review of the OTS/explorer surface.
# Item
1. Enumerate every network call the round makes: plans/round54_c1_anchor.py (stamp/upgrade -> ots CLI ->
  calendars), E1/SC4 explorer fetches, SC1/SC2 fetches. For each: what leaves the host (answer: only the
  32-byte digest of a public file — verify no file CONTENTS, paths, usernames or tokens are embedded in what ots
  sends: read the ots client source in the venv site-packages for the submission payload).
2. Inbound risk: claims.ots/header.bin/explorer JSONs are untrusted bytes parsed by the counter and the library —
  deserialization-bomb / recursion risk? The library has a recursion limit — confirm (grep it) and note the
  counter's exposure. Try a hostile deep-nesting proof in scratch (bounded size) — must be rejected, not hang.
3. No credentials anywhere: grep the round's artifacts for token/key/secret patterns (report counts, no values).
Save {LANE}/.ufo/waves/round-54/w1/SN1OtsNetwork/safety.md. Verdict SAFE / UNSAFE with reasons.
# Acceptance
safety.md; verdict pasted.
""")

add("SN2FixtureHygiene", "sentinel", B, f"""# Target
kengaku round 54 seat SN2FixtureHygiene (sentinel). Fixture/scratch hygiene audit for the round's seats.
# Item
1. Read the wave context's git-fixture rule + QUALITY.md Q32. Audit the wave dirs under
   {LANE}/.ufo/waves/round-54/w1/ as they fill: any seat writing outside its own dir or outside scratch? Any
   fixture repo created OUTSIDE /fast/scratch/hyaku/kengaku-r54/ ? (find by .git dirs newer than today 10:00 under
   /fast/scratch + the lane tree excluding .git — report paths + owner by dir name.)
2. Scratch discipline: /tmp entries >50MB created today (du -sh /tmp/* 2>/dev/null | sort -h | tail) — flag any
   belonging to this round's seats (names containing r54/kengaku). Disk-guard status before your pass
   (/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status).
3. Confirm no seat process ran a mutating git/jj in the LANE (git -C {LANE} reflog is out of scope — instead:
   git -C {LANE} status --porcelain must show only expected wave-dir files; paste it).
Save {LANE}/.ufo/waves/round-54/w1/SN2FixtureHygiene/hygiene.md. This seat runs LATE in its wave lifecycle
(check the wave dirs after most seats reported; if dirs are still empty, audit scratch + the lane status only and
say which checks you could not run).
# Acceptance
hygiene.md with findings or a clean bill per check.
""")

# ---------------- revengers (2)
add("RV1Oracle2Replay", "revenger", A, f"""# Target
kengaku round 54 seat RV1Oracle2Replay (revenger). Re-attack the round-53 C1 integrity hole against the new anchor.
# Item
Read {LANE}/.ufo/waves/round-53/w3/C1CritOracle2.md. Rebuild (scratch) the smallest coordinated-history forgery
it demonstrated: a clone whose claims-file bytes and internal pins disagree but whose r53-style FREEZE leg passes.
Then run the r54 C1 counter's verify against that forged clone as --source: BINDING must fail (the anchored
digest is pinned to the REAL freeze rev, which the forged clone's history does not contain). Demonstrate with
commands + outputs. Then the honest question: could a forger who ALSO possesses the real freeze rev 17f90355
(i.e. the real claims bytes) still forge anything? Only the digest itself is public — what does the anchor
actually witness and what not? State it in two sentences (content vs existence). Save
{LANE}/.ufo/waves/round-54/w1/RV1Oracle2Replay/replay.md.
# Acceptance
replay.md with the forged-clone construction, the verify failure, and the witness-scope statement.
""")

add("RV2ArgvReplay", "revenger", B, f"""# Target
kengaku round 54 seat RV2ArgvReplay (revenger). Replay the r53 argv-laundering + contamination attacks against
the r54 counters.
# Item
Read {LANE}/.ufo/waves/round-53/w3/C2CritPredicate2.md. Reproduce its two demonstrated routes in scratch:
(a) selected-argv laundering — fixture gate red at entry, green at selftest; the r53 counter passes (you may
reuse plans/round54_c2_controls.py --route-only to confirm), then the SAME fixture ledger pattern in r54 form
must FAIL with LAUNDERED. (b) git-config contamination — the poison-GIT_CONFIG_GLOBAL route against the r53 env
(reuse --env-poison) and its absence under hermetic_env. Then extend: poison via GIT_CONFIG_SYSTEM (hermetic_env
pins /dev/null — prove it holds), via repo-local .git/config in the CLONE (find whether any audited gate reads
it; if one does, that is a finding with the gate name — the frozen claims file's hermeticity sentence covers
global/system only: quote it). Save {LANE}/.ufo/waves/round-54/w1/RV2ArgvReplay/replay.md.
# Acceptance
replay.md: routes reproduced, r54 closures demonstrated, the repo-local-config verdict.
""")

# ---------------- connectors (2)
add("CN1SiblingOverlap", "connector", X, f"""# Target
kengaku round 54 seat CN1SiblingOverlap (connector). Sibling-overlap scan for the round's two instruments.
# Item
1. Scan sibling repos at their current tips for an externally-anchored freeze or a registry entry-truth counter:
   ls /home/vgpnk/Projects/*-shokunin; grep -rl -i 'opentimestamps\\|blockchain\\|anchor.*freeze\\|entry.*truth\\|
   entry_argv' over their plans/, tools/, corpus/knowledge/ (bounded; skip .git). For hits: read enough to rule
   duplicate vs adjacent (name repo, path, one-line what it does).
2. Also check kasegi's mutation-battery and tameshi's fixture method for overlap with the round's CONTROLS legs
   (r37 precedent: 'mutation testing of a lane's own gate is a fleet-wide pattern').
3. Report-outs: anything a sibling owns that this round's report should route (e.g. if kumitate owns
   'hermetic gate execution' patterns) — one line each with the evidence path. Save
   {LANE}/.ufo/waves/round-54/w1/CN1SiblingOverlap/overlap.md.
# Acceptance
overlap.md with the scan commands, hit table, duplicate/adjacent ruling per hit.
""")

add("CN2CrossSource", "connector", X, f"""# Target
kengaku round 54 seat CN2CrossSource (connector). Cross-claim / cross-source pattern scan.
# Item
1. As wave dirs fill, scan {LANE}/.ufo/waves/round-54/w1/*/ for patterns spanning claims: the same attack landing
   on both C1 and C2 (e.g. time/trust confusion), sources fetched by two seats (dedupe for the SOURCES rows),
   findings that contradict each other (name both seats).
2. Check the round's claims-file 'Inherited context honored' list against the actual wave output: any seat
   re-labelling TB2 tests as novel (forbidden)? any claim drifting toward 'unforgeable' wording?
3. Produce {LANE}/.ufo/waves/round-54/w1/CN2CrossSource/patterns.md: (a) duplicated fetches -> one owner each;
   (b) contradictions -> the two seats + your read; (c) routed-out items -> owner lane + path. This seat runs
   MID-WAVE: if dirs are sparse, audit what exists and say so.
# Acceptance
patterns.md; contradictions pasted.
""")

# ---------------- simplifier (1)
add("SP1CounterSimplify", "simplifier", X, f"""# Target
kengaku round 54 seat SP1CounterSimplify (simplifier). Simplify without behaviour change.
# Item
Review {LANE}/plans/round54_c1_anchor.py and plans/round54_c2_entrytruth.py for dead weight (unused imports,
dead branches, duplicated helpers) WITHOUT changing behaviour: produce patched copies in your wave dir + a diff
narrative. Prove behaviour-identity: run old vs new --selftest for both counters (byte-compare outputs) and, for
the C2 counter, --dry against {LANE} twice (old/new outputs byte-equal). If a simplification is NOT provably
identity-preserving, drop it and say why. The L1 integrates only if R1/R2 verdicts are clean AND your identity
proofs hold. Save {LANE}/.ufo/waves/round-54/w1/SP1CounterSimplify/ under simplification notes + patches.
# Acceptance
diff narrative + the four identity receipts.
""")

add("C6KillRules", "critic", X, f"""# Target
kengaku round 54 seat C6KillRules (critic). Attack the kill rules and the no-harm claim.
# Item
Read plans/round-54-claims.md §kill rules + §harm for both claims, and the fleet claim-sizing lessons (addendum
§9: a target a do-nothing control cannot reach; freeze one predicate).
1. Kill-rule reachability: for each declared kill rule, is there a concrete command a closure could RUN that
   fires it? Write the command for each (e.g. 'pending at integration' -> the upgrade retry log is the evidence).
   A kill rule with no runnable trigger is a finding.
2. Do-nothing control reachability: enumerate what a do-nothing L1 (no wave, no landing) would produce for each
   before receipt and each control receipt — confirm none of the AFTER predicates is reachable without the round's
   specific artifacts (anchor with bitcoin attestation at >800000 height + two agreeing explorer receipts; ledger
   with 78 executed entry rows). Quote the exact after-state line a forger would have to fabricate.
3. No-harm: read the r53 final receipts' numbers; name the two landing-tip re-runs (E7/E8) and what result would
   constitute harm for each axis; check the claims file's harm watch section covers them (quote gaps).
Save {LANE}/.ufo/waves/round-54/w1/C6KillRules/killrules.md.
# Acceptance
killrules.md; unrunnable kill rules pasted first.
""")

add("R5LedgerStatic", "reviewer", B, f"""# Target
kengaku round 54 seat R5LedgerStatic (reviewer). Static schema + honesty review of the committed entrytruth ledger.
# Item
Review {LANE}/plans/round54-entrytruth.json as a document (not its execution):
1. Schema: every row has exactly the fields entry_argv/entry_exit/entry_state/(reason/evidence when red)/chosen/sec;
   no duplicate keys (strict parse); 78 rows == registry names (set equality); argvs are entry mode per
   round54_c2_entrytruth.entry_mode_ok (import it); script in each argv matches the SKILL.md registry cell.
2. Red reasons: >=10 words, name a cause (not a paraphrase of 'it exited nonzero'); evidence fragments non-empty
   and <200 chars. Green rows carry no reason/evidence (noise = finding).
3. chosen-field honesty: rows with chosen=='r53-entry' — confirm the argv really equals the r53 ledger's entry
   argv (cross-load plans/round53-tipstate.json); rows with 'lane-dot'/'bare' — confirm the argv difference is
   exactly the --lane flag (or r53 override).
4. Produce {LANE}/.ufo/waves/round-54/w1/R5LedgerStatic/review.md: verdict CLEAN / DEFECTS with a row-name list.
# Acceptance
review.md; defect rows pasted.
""")

add("C7PriorArtPrices", "critic", A, f"""# Target
kengaku round 54 seat C7PriorArtPrices (critic). Falsify the prior-art verdicts (the novelty leg's soft spot).
# Item
After SC1PriorArt + SC2OtsDocs report: read their wave dirs' fetched/ + verdicts. Attack:
1. Re-open 3 of their fetched URLs yourself (fresh fetch; compare bytes/excerpt). Any quote not located where
   claimed is a finding (quote, location, what you found).
2. Contest each verdict: 'known' must cite a source that ACTUALLY anchors measurement-preregistration digests
   (a generic blockchain-paper cite does not cover C1's construct — is the lane's instrument still instrument-new?
   rubric: replication vs contribution); 'not-found' must carry the full query sweep — run ONE extra query of your
   own design and report whether it flips any verdict.
3. The claims file's honesty clause: 'if prior art shows Bitcoin-anchored preregistration freezes are published
   practice, the honest verdict is replication/instrument-new and the score holds at 8' — judge whether the fetched
   evidence forces that clause to fire (cite lines).
Save {LANE}/.ufo/waves/round-54/w1/C7PriorArtPrices/pricing.md.
# Acceptance
pricing.md; any flipped verdict pasted first.
""")

spec = {
    "wave": WAVE,
    "milestone": "kengaku round 54 wave 1 (v2, build+attack): externally-anchored freeze (R54-C1, novelty 8->9) "
                 "and entry-truth registry counter (R54-C2, calibration 9->10), plus frontier-step and no-harm evidence",
    "reportDir": ".ufo/waves/round-54/w1",
    "maxLanes": 66,
    "axes": ["novelty", "calibration"],
    "context": CONTEXT,
    "items": items,
}
with open(".ufo/waves/round-54/w1-spec.json", "w") as f:
    json.dump(spec, f, indent=1, ensure_ascii=False)
roles = {}
for it in items:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
attack = roles.get("reviewer", 0) + roles.get("critic", 0) + roles.get("mutation-tester", 0) + roles.get("sentinel", 0)
print(json.dumps(roles, indent=0))
print(f"items={len(items)} attack={attack} share={attack/len(items):.3f}")
