#!/usr/bin/env python3
"""Round-49 C2 counter (v4): the round-46 TB2 `polyglot-c-py` package admitted under a Q40 re-frozen counter.

The graded surface is unchanged from round 46 (plans/round-46-claims.md §C3): one file
`/app/polyglot/main.py.c` executed by two toolchains, three fixed points, an exact-directory precondition,
graded by `tests/test_outputs.py` at terminal-bench-2 `2fd12b88aafdd04a52c298e3940bcb189f9766d6`. Round 49
claims its **admission**, not a new class (plans/round-49-claims.md §C2).

Frozen predicate (same sentence in plans/round-49-claims.md §C2 and in this receipt label):
  C2 passes iff `python3 plans/round49_c2_verify.py --lane .` prints `checks=<V> defects=0`, then
  `PREDICATE R49-C2 pass`, exit 0, on a clean clone of the landing tip.

Contract = `plans/round46_c3_verify.py` at its round-46 digest, imported (never copied, so a change to the
imported file is a setup error, not a silent change of what this counter certifies), plus four frozen deltas.
The import reads this round's inputs through a pin re-point applied at load time (`load_base`): SPEC_REL,
SPEC_SHA256, DRY_REL, DRY_SHA256, PROBE_REL, PROBE_SHA256, GATE_REL, GATE_SHA256 and CLAIMS_REL are replaced
before any leg runs, and the layer above that patches nothing else.

  V7 (Q24 fix, replaces the imported V7). Before any label is derived, this leg positively verifies, from the
     frozen tables alone: (i) every frozen tag (the `TAG` lines of the frozen dry table) is cited by at least one
     committed receipt case `violates=` token; (ii) the two tags the round-46 failure named — `both-print` and
     `toolchain` — are in the frozen set and each is so cited; (iii) every `## Requirement map` row parses to
     the header's column count and to the canonical table shape (`| 'instruction.md:N' | 'tag' | label | cases |`).
     Rows that fail (iii) are defects even when the derived-label rule would have ignored them — round 46's
     `both-print`/`toolchain` rows were skipped by an unanchored regex and reported only as "missing".
     The imported label rule (enforced/unenforced/partly, DERIVED from the receipt) and the citation rule are
     then applied unchanged.

  V8 (Q30/Q40 fix, replaces the imported V8 AND the round-48 inherited-receipt rule). Three frozen controls —
     `base` (the tree with `plans/polyglot_c_py_probe.py` removed), `filler` (the committed round-46 filler
     package) and `echo` (the frozen dry table copied over the receipt) — are run through the package gate
     **with `--rerun` omitted**, so the gate's `P10` (fresh probe re-run) clause does not exist in the run: any
     `P10` line at all in a control's output is a defect. Each control must be *refused* by the gate (exit 1),
     never accepted, and never error. The control receipts committed under `.ufo/waves/round-49/claims/` (paths
     frozen at stage 2) must print `PREDICATE R49-C2 fail`, must carry no `P10` line and no executed-probe
     `CASE … observed=` line, and each must pass `plans/order_check.py` against the round-49 claims.
     The package's own receipt is now this round's fresh evidence, and its order is verified from `git log`
     (the round-48 rule — "the receipt was added at or before the freeze" — is gone; an inherited receipt could
     never satisfy an amended V7 table):
       * stage 2 is the first commit that adds `plans/round49_c2_verify.py` (the counter and its pins land
         together at stage 2, plans/round-49-claims.md §Freeze shape);
       * stage 3 is the first commit that adds the receipt path the spec names;
       * stage 3 must be its own commit — never the stage-2 commit — and must be a descendant of stage 2
         (`git merge-base --is-ancestor <stage2> <stage3>`);
       * the stage-3 commit must carry the receipt's pin in the same commit: `receipt_sha256` of the spec blob
         at stage 3 equals the sha256 of the receipt blob at stage 3 (the pin is what makes that commit the
         stage-3 commit rather than "some later commit that touched the file");
       * the receipt must carry `CASE … observed=` lines, and every `CASE` line in it must carry `observed=`
         (a dry table or a filler receipt is refused);
       * the receipt being measured must be the blob that the stage-3 commit landed: a receipt edited after
         its landing commit makes the pin and the ordering describe bytes nobody measured, so it is a DEFECT.

  V15 (new, preconditions dry-run). Before any leg scores, every frozen input digest is resolved and every
     leg's frozen table is parsed. A missing, pending-pin or tamper-pinned input is a DEFECT *of the legs that
     read it*: those legs are not executed and print the precondition reason, so a missing file is a named
     defect and never a traceback. V15 itself is ok only when nothing is blocked.

  V14 (new, mutation battery). `<N>` fresh mutants of committed package bytes (capture, entry, receipt, dry
     table, spec, probe) declared in `plans/mutants49/plan.json` (payload path + digest + target per mutant,
     authored by wave-1 mutation-tester seats). Each payload's digest is re-measured, each target must be one of
     the frozen package bytes, and the mutant is applied to a symlink mirror of the lane, never to the lane. A
     mutant is *caught* iff at least one substantive leg (V3/V4/V7/V9/V10/V12) that was ok on the unmutated
     mirror becomes DEFECT on the mutant; a mutant the frozen spec pin refuses outright (the package no longer
     loads) is caught by every content leg, since a leg that cannot run is a defect and never a pass. The leg
     reports the legs that were already DEFECT at baseline, because a broken baseline cannot measure anything.
     Fewer than the frozen floor caught prints `MUTATION DEFECT` and the leg fails.

Ordering (QUALITY Q30, plans/round-49-claims.md §C2): no probe of this package runs before the stage-3 commit
lands the receipt. `--dry` is the stage-check: it scores every leg except V2 (the only leg that runs the probe,
via the gate's P10 and the V11 predictor sandboxes' package path), prints `PREDICATE R49-C2 dry` — never `pass`
— and exits 1. `--control {base,filler,echo}` builds that control's mirror, measures the same legs with V2
excluded, and prints a fail receipt: it is the command that produces a stage-2 control receipt, and it cannot
execute P10.

Exit: 0 pass · 1 fail (also dry/control) · 2 setup error.

Named limits.
  * V14 measures the mutants it is given: payload digests, targets and the pinned count are checked, but the
    claim that a human/seat authored them against the committed bytes is not machine-checkable here.
  * V8's live gate run proves a control is refused with P10 absent; it does not prove the committed control
    receipt was produced by that exact command. The receipt is checked for the fail predicate, for P10 absence
    and for ordering, so a receipt from a P10-carrying run cannot pass.
  * V8's ordering rule reads the receipt's pin from the spec's `receipt_sha256` (the round-46 package schema).
    A stage-3 commit that lands a receipt without filling that pin is a DEFECT here even if the receipt itself
    is genuine: the pin is the artefact that lets the next reader tie the receipt to the commit that made it.
  * V8's stage-2 anchor is the counter file itself; landing the counter in a commit that is not the stage-2
    amendment (for example one commit before the pins are filled) moves the anchor and is visible in the note.
  * V7's row-shape rule needs a header row naming `Instruction line` and `Tag`; a map with no header is a
    defect, and a row carrying `instruction.md:` that does not match the canonical shape is a defect.
  * The imported V11 predictor rules and their named limit stand unchanged (a small hand-coded verdict table is
    not distinguishable from a reader by sample equivalence alone; non-author review stays part of admission).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

# ---- frozen literals ---------------------------------------------------------------------------
BASE_REL = "plans/round46_c3_verify.py"
BASE_SHA256 = "a971c24dd5d0cb880e97ad4dd80315fcf58afaa02f8cffb5cc2e803aa292a8d4"  # round-46 bytes, unedited

SPEC_REL = "plans/pkg-spec-r49.json"
SPEC_SHA256 = "<PIN:stage-2>"  # sha256 of the r49 spec with its receipt_sha256 value masked (round-46 rule)
PROBE_REL = "plans/polyglot_c_py_probe.py"
PROBE_SHA256 = "<PIN:stage-2>"  # the amended probe revision's digest, pinned at stage 2
DRY_REL = "corpus/evidence/round49/polyglot-c-py-dry-cases.txt"
DRY_SHA256 = "<PIN:stage-2>"  # the amended dry table's digest, pinned at stage 2
GATE_REL = "plans/pkg_gate.py"
GATE_SHA256 = "ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41"  # round-45/46 bytes, unedited
ORDER_REL = "plans/order_check.py"
CLAIMS_REL = "plans/round-49-claims.md"
COUNTER_REL = "plans/round49_c2_verify.py"  # the stage-2 anchor: this file, landed with its pins

MUT_PLAN_REL = "plans/mutants49/plan.json"
MUT_N = "<PIN:stage-2>"      # stage-2 literal: the number of frozen mutants
MUT_FLOOR = "<PIN:stage-2>"  # stage-2 literal: the catch floor (claims freeze it at >= N/2)

CONTROL_ORDER = ("base", "filler", "echo")
CONTROL_RECEIPTS = {name: "<PIN:stage-2>" for name in CONTROL_ORDER}  # stage-2 pins, lane-relative

NAMED_TAGS = ("both-print", "toolchain")  # the two tags the round-46 V7 failure named
SUBSTANTIVE = ("V3", "V4", "V7", "V9", "V10", "V12")

# What the legs and the gate read: a control/mutation mirror costs a few symlinks, never a copy of the lane.
# The capture directory and the spec-named files are appended from the spec at mirror time.
MIRROR_DIRS = ("corpus/knowledge", "plans/filler46", "plans/mutants49")
MIRROR_FILES = ("corpus/SOURCES.md", "corpus/README.md", "PROVINCE.md", SPEC_REL, GATE_REL, PROBE_REL,
                ORDER_REL, BASE_REL, CLAIMS_REL, DRY_REL)

GATE_P10 = re.compile(r"^\s*(?:gate:\s*)?P10\b")
CASE_OBSERVED = re.compile(r"^\s*CASE\s+\S+.*\bobserved=")
SEPARATOR = re.compile(r":?-{2,}:?")


class SetupError(Exception):
    """An instrument that is not the frozen instrument: exit 2, never a silent pass."""


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def load_base(lane):
    """Import the round-46 counter at its frozen digest, then re-point its input pins at this round's inputs."""
    path = pathlib.Path(lane) / BASE_REL
    got = sha256(path)
    if got != BASE_SHA256:
        raise SetupError(f"{BASE_REL} is not at its round-46 digest: got {got} want {BASE_SHA256}")
    spec = importlib.util.spec_from_file_location("round46_c3_verify_r49c2", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # The bytes above are the frozen contract; only the inputs move. Every imported leg reads its paths and
    # pins through these module globals, so this is the whole of the delta's reach into the import.
    mod.SPEC_REL = SPEC_REL
    mod.SPEC_SHA256 = SPEC_SHA256
    mod.DRY_REL = DRY_REL
    mod.DRY_SHA256 = DRY_SHA256
    mod.PROBE_REL = PROBE_REL
    mod.PROBE_SHA256 = PROBE_SHA256
    mod.GATE_REL = GATE_REL
    mod.GATE_SHA256 = GATE_SHA256
    mod.CLAIMS_REL = CLAIMS_REL
    return mod


# ---- the requirement map's own shape rule (V7 delta) -------------------------------------------

def map_rows(text):
    """(header column count, data rows) for `## Requirement map`; (None, []) when the section or header is absent."""
    m = re.search(r"^## Requirement map\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        return None, []
    header, rows = None, []
    for line in m.group(1).splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cells and all(SEPARATOR.fullmatch(c) for c in cells):
            continue
        if header is None and any("Instruction line" in c for c in cells) and any(c == "Tag" for c in cells):
            header = len(cells)
            continue
        rows.append((cells, line))
    return header, rows


def v7(base, pkg):
    """Positive preconditions over the frozen tables, then the imported label/citation rule."""
    try:
        tags, _ids = base.dry_table(pkg)
    except (OSError, ValueError) as e:
        return False, f"dry table unusable: {e}"
    receipt = base.text_or_none(pkg.receipt)
    entry = base.text_or_none(pkg.entry)
    if receipt is None or entry is None:
        return False, "receipt or entry absent"
    parsed = base.receipt_cases(receipt)
    bad = []
    violated = {t: sorted(cid for cid, (_o, v) in parsed.items() if t in v) for t in tags}
    # (i) every frozen tag is cited by at least one committed case `violates=` token
    for t in sorted(tags):
        if not violated[t]:
            bad.append(f"{t}:no committed case carries violates={t}")
    # (ii) the two tags the round-46 failure named
    for t in NAMED_TAGS:
        if t not in tags:
            bad.append(f"{t}:not a frozen tag")
        elif not violated[t]:
            bad.append(f"{t}:unexercised-by-any-case")
    # (iii) every row parses to the header's column count and to the canonical shape
    header, rows = map_rows(entry)
    if header is None:
        return False, "no parsable '## Requirement map' header (needs 'Instruction line' and 'Tag' columns)"
    seen = {}
    for cells, line in rows:
        if len(cells) != header:
            bad.append(f"row parses to {len(cells)} cells not {header}: {line.strip()[:40]!r}")
        m = base.MAP_ROW.match(line)
        if not m:
            if "instruction.md:" in line:
                bad.append(f"row not in canonical shape: {line.strip()[:50]!r}")
            continue
        ln, tag, label, rest = m.groups()
        seen[tag] = seen.get(tag, 0) + 1
        if tag not in tags:
            bad.append(f"{tag}:not a frozen tag")
            continue
        if tags[tag] != f"instruction.md:{ln}":
            bad.append(f"{tag}:line {ln} is not the frozen {tags[tag]}")
        if not violated[tag]:
            bad.append(f"{tag}:no receipt case violates it")
            continue
        want = base.derive({parsed[c][0] for c in violated[tag]})
        if label != want:
            bad.append(f"{tag}:labelled {label}, receipt derives {want}")
        cited = re.findall(r"`([a-z0-9_-]+)`", rest)
        if not cited or any(c not in violated[tag] for c in cited):
            bad.append(f"{tag}:cites no case or a case that does not violate it")
    missing = sorted(set(tags) - set(seen))
    dup = sorted(t for t, n in seen.items() if n > 1)
    if missing:
        bad.append(f"tags missing={missing}")
    if dup:
        bad.append(f"tags duplicated={dup}")
    note = (f"rows={len(rows)} tags={len(tags)} violated={sum(1 for t in tags if violated[t])}/{len(tags)}"
            f" bad={len(bad)}")
    return not bad, note + (f" first={bad[0]}" if bad else "")


# ---- mirrors: what the legs read, symlinked; the lane is never written --------------------------

def _dedupe(items):
    out = []
    for item in items:
        if item and item not in out:
            out.append(item)
    return out


def mirror(lane, dest, spec_rel=SPEC_REL):
    """A read-through mirror: directories are copied (a mutant must never write through a dir symlink into the
    lane), individual files are symlinked and replaced by a real file only when a mutant installs one."""
    lane = pathlib.Path(lane)
    dest = pathlib.Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    dirs, files = list(MIRROR_DIRS), list(MIRROR_FILES)
    try:
        s = json.loads((lane / spec_rel).read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        s = {}
    if isinstance(s, dict):
        dirs.append(str(s.get("capture_dir", "")))
        files.extend(str(s.get(k, "")) for k in ("entry", "receipt", "readme", "sources"))
    for rel in _dedupe(dirs):
        src = lane / rel
        if src.is_dir():
            (dest / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src, dest / rel, dirs_exist_ok=True)
    for rel in _dedupe(files):
        src = lane / rel
        if src.is_file() and not (dest / rel).exists():  # a copied directory already carries its own files
            (dest / rel).parent.mkdir(parents=True, exist_ok=True)
            os.symlink(src, dest / rel)
    return dest


def unlink_any(p):
    if p.is_symlink() or p.exists():
        p.unlink()


def control_tree(lane, work, name, pkg_spec_rel=SPEC_REL):
    """The frozen control tree for `name`, built as a symlink mirror of `lane`."""
    tree = mirror(lane, pathlib.Path(work) / f"ctl-{name}", pkg_spec_rel)
    if name == "base":
        unlink_any(tree / PROBE_REL)  # the base tree: no plans/polyglot_c_py_probe.py
    elif name == "echo":
        spec = json.loads((tree / pkg_spec_rel).read_text())
        receipt = tree / spec["receipt"]
        data = (tree / DRY_REL).read_bytes()
        unlink_any(receipt)
        receipt.write_bytes(data)  # the frozen dry table copied over the receipt
    return tree


def gate_control(base, tree, name):
    """Run the package gate on a control tree with `--rerun` omitted: the P10 leg does not exist."""
    spec = (tree / base.FILLER_SPEC) if name == "filler" else (tree / SPEC_REL)
    argv = [sys.executable, str(tree / GATE_REL), "package", "--root", str(tree), "--spec", str(spec)]
    r = subprocess.run(argv, capture_output=True, text=True, timeout=1800)
    p10 = [l for l in r.stdout.splitlines() if GATE_P10.match(l)]
    return r, p10


def order(root, receipt_rel):
    r = subprocess.run([sys.executable, str(pathlib.Path(root) / ORDER_REL), "--lane", str(root),
                        "--claims", CLAIMS_REL, "--receipt", receipt_rel],
                       capture_output=True, text=True, timeout=300)
    return r, r.returncode == 0 and "ORDER RESULT PASS" in r.stdout.splitlines()


def git(root, *args):
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return r.returncode, r.stdout


def git_bytes(root, *args):
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    return r.returncode, r.stdout


def first_commit(root, rel):
    """The oldest commit that adds `rel`; '' when never added."""
    rc, out = git(root, "log", "--reverse", "--diff-filter=A", "--format=%H", "--", rel)
    lines = out.split() if rc == 0 else []
    return lines[0] if lines else ""


def blob_bytes(root, commit, rel):
    """The bytes of `rel` at `commit`; None when the commit does not carry it."""
    rc, out = git_bytes(root, "show", f"{commit}:{rel}")
    return out if rc == 0 else None


def v8(base, root, work):
    """Pre-receipt controls with P10 disabled, the ordering receipt that pins each control, and the frozen
    stage-3 rule for the package receipt: first-commit == the stage-3 commit, a descendant of stage 2."""
    root = pathlib.Path(root)
    bad = []
    try:
        receipt_rel = json.loads((root / SPEC_REL).read_text())["receipt"]
    except (OSError, KeyError, UnicodeDecodeError, json.JSONDecodeError) as e:
        return False, f"spec unreadable: {e}"
    # The package receipt is this round's fresh evidence: it must have landed at stage 3, after the stage-2
    # commit that landed this counter, and the stage-3 commit must carry its pin.
    stage2 = first_commit(root, COUNTER_REL)
    stage3 = first_commit(root, receipt_rel)
    note_order = f"stage2={stage2[:12] or 'none'} stage3={stage3[:12] or 'none'}"
    if not stage2:
        bad.append(f"no commit adds the stage-2 counter {COUNTER_REL} (the ordering anchor is absent)")
    if not stage3:
        bad.append(f"no commit adds the receipt {receipt_rel} (the stage-3 landing is absent)")
    if stage2 and stage3:
        if stage2 == stage3:
            bad.append("the receipt's first commit is the stage-2 commit (stage 3 must be its own commit)")
        elif git(root, "merge-base", "--is-ancestor", stage2, stage3)[0] != 0:
            bad.append(f"receipt first-commit {stage3[:12]} is not a descendant of the stage-2 commit {stage2[:12]}")
        spec_at3 = blob_bytes(root, stage3, SPEC_REL)
        receipt_at3 = blob_bytes(root, stage3, receipt_rel)
        if spec_at3 is None or receipt_at3 is None:
            bad.append("the first commit adding the receipt carries neither the receipt nor its spec pin")
        else:
            try:
                pin = json.loads(spec_at3.decode("utf-8")).get("receipt_sha256", "")
            except (UnicodeDecodeError, json.JSONDecodeError):
                pin = ""
            got = hashlib.sha256(receipt_at3).hexdigest()
            if pin != got:
                bad.append(f"the first commit adding the receipt does not carry its pin "
                           f"(receipt_sha256={str(pin)[:12] or 'absent'} blob={got[:12]})")
            if sha256(root / receipt_rel) != got:
                bad.append("the receipt being measured is not the blob the stage-3 commit landed "
                           "(a receipt edited after its landing commit)")
    text = base.text_or_none(root / receipt_rel) or ""
    cases = [l for l in text.splitlines() if l.strip().startswith("CASE ")]
    observed = [l for l in cases if CASE_OBSERVED.match(l)]
    if not cases:
        bad.append("the receipt carries no CASE lines (no measured run)")
    elif len(observed) != len(cases):
        bad.append(f"receipt CASE lines without observed=: {len(cases) - len(observed)}/{len(cases)}")
    gates = []
    for name in CONTROL_ORDER:  # the gate half: P10-omitted runs, measured on every invocation
        tree = control_tree(root, work, name)
        r3, p10 = gate_control(base, tree, name)
        gates.append(f"{name}:exit={r3.returncode},p10={len(p10)}")
        if p10:
            bad.append(f"{name}:gate printed a P10 line with --rerun omitted")
        if r3.returncode != 1:
            bad.append(f"{name}:gate exit={r3.returncode} (a control must be refused, not accepted or error)")
    for name in CONTROL_ORDER:  # the ordering half: the committed receipt each control pins
        rel = CONTROL_RECEIPTS[name]
        if not base.ready(rel):
            bad.append(f"{name}:control receipt pending (stage-2 pin)")
            continue
        ctext = base.text_or_none(root / rel)
        if ctext is None:
            bad.append(f"{name}:control receipt absent: {rel}")
            continue
        if "PREDICATE R49-C2 fail" not in ctext:
            bad.append(f"{name}:receipt does not print the fail predicate")
        if any(GATE_P10.match(l) for l in ctext.splitlines()):
            bad.append(f"{name}:receipt shows a P10 line (the control executed the gate's P10)")
        if any(CASE_OBSERVED.match(l) for l in ctext.splitlines()):
            bad.append(f"{name}:receipt shows an executed probe case")
        r2, ok2 = order(root, rel)
        if not ok2:
            hits = [l.strip() for l in r2.stdout.splitlines() if l.startswith("ORDER HIT")]
            bad.append(f"{name}:order exit={r2.returncode} {hits[0][:80] if hits else ''}".strip())
    note = (f"controls={len(CONTROL_ORDER)} gates={' '.join(gates)} {note_order}"
            f" cases={len(cases)} observed={len(observed)} bad={len(bad)}")
    return not bad, note + (" " + " | ".join(bad[:3]) if bad else "")


# ---- V14: mutation battery over the committed package bytes ------------------------------------

def load_plan(root):
    try:
        plan = json.loads((pathlib.Path(root) / MUT_PLAN_REL).read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(plan, dict) or not isinstance(plan.get("mutants"), list):
        return None
    return plan


def mutable_bytes(root, base):
    """The set of lane-relative paths a mutant may target: the package's own committed bytes."""
    try:
        spec = json.loads((pathlib.Path(root) / SPEC_REL).read_text())
        capdir = spec["capture_dir"]
        return {SPEC_REL, spec["entry"], spec["receipt"], DRY_REL, PROBE_REL} \
            | {f"{capdir}/{name}" for name in base.CAPTURES}
    except (OSError, KeyError, UnicodeDecodeError, json.JSONDecodeError):
        return set()


def substantive(base, pkg):
    """The substantive content legs, one bool each; a leg that raises is a defect, never a pass."""
    table = {
        "V3": lambda: base.v3(pkg),
        "V4": lambda: base.v4(pkg),
        "V7": lambda: v7(base, pkg),
        "V9": lambda: base.v9(pkg),
        "V10": lambda: base.v10(pkg),
        "V12": lambda: base.v12(pkg),
    }
    out = {}
    for name in SUBSTANTIVE:
        try:
            ok, _note = table[name]()
        except Exception:  # a leg that cannot run cannot certify the mutant
            ok = False
        out[name] = ok
    return out


def install_mutation(tree, rel, data):
    p = pathlib.Path(tree) / rel
    parts = pathlib.PurePosixPath(rel)
    if parts.is_absolute() or ".." in parts.parts:
        raise ValueError(f"mutation target escapes the mirror: {rel}")
    parent = p.parent.resolve()
    root = pathlib.Path(tree).resolve()
    if parent != root and root not in parent.parents:
        raise ValueError(f"mutation target's directory escapes the mirror: {rel} -> {parent}")
    unlink_any(p)  # a symlink would otherwise write through into the lane
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


def restore_mutation(tree, root, rel):
    p = pathlib.Path(tree) / rel
    unlink_any(p)
    os.symlink(pathlib.Path(root) / rel, p)


def sha256_of_payload(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def v14(base, root, work):
    if not (base.ready(MUT_N) and base.ready(MUT_FLOOR)):
        return False, "mutation literals pending (stage-2 pins MUT_N and MUT_FLOOR)"
    try:
        n, floor = int(MUT_N), int(MUT_FLOOR)
    except ValueError:
        return False, f"mutation literals are not integers: N={MUT_N!r} floor={MUT_FLOOR!r}"
    plan = load_plan(root)
    if plan is None:
        return False, f"mutation plan absent or unparsable: {MUT_PLAN_REL}"
    muts = plan["mutants"]
    if len(muts) != n:
        return False, f"plan mutants={len(muts)} but the frozen N={n}"
    mutable = mutable_bytes(root, base)
    if not mutable:
        return False, "spec unreadable: the mutable-byte set is empty"
    tree = mirror(root, pathlib.Path(work) / "mut")
    try:
        base_map = substantive(base, base.real_pkg(tree))
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as e:
        return False, f"mutation mirror unusable: {e}"
    caught, notes = [], []
    for m in muts:
        name = str(m.get("name", "?"))
        target = str(m.get("target", ""))
        payload_rel = str(m.get("payload", ""))
        why = []
        if target not in mutable:
            why.append("target is not a frozen package byte")
        try:
            payload = (pathlib.Path(root) / payload_rel).read_bytes()
        except OSError:
            payload = None
            why.append("payload unreadable")
        if payload is not None and sha256_of_payload(payload) != str(m.get("sha256", "")):
            why.append("payload digest differs from the plan")
        if why:
            notes.append(f"{name}:unmeasurable({';'.join(why)})")
            continue
        unreadable = False
        try:
            install_mutation(tree, target, payload)
            try:
                pkg_m = base.real_pkg(tree)
            except (ValueError, OSError, KeyError, json.JSONDecodeError):
                # a frozen spec pin refuses the mutant: every content leg reads the package and cannot run,
                # which the imported counter scores as a defect, never a pass
                got, unreadable = {leg: False for leg in SUBSTANTIVE}, True
            else:
                got = substantive(base, pkg_m)
        except Exception as e:  # a mutant the counter cannot even install proves nothing about sensitivity
            notes.append(f"{name}:unmeasurable(install {type(e).__name__}: {e})")
            continue
        finally:
            restore_mutation(tree, root, target)
        flipped = [leg for leg in SUBSTANTIVE if base_map[leg] and not got[leg]]
        if flipped:
            caught.append(name)
            notes.append(f"{name}:caught({','.join(flipped)})" + (" package-unreadable" if unreadable else ""))
        else:
            notes.append(f"{name}:CLEAN")
    ok = len(caught) >= floor
    if not ok:
        print("MUTATION DEFECT")
    baseline_bad = sorted(leg for leg, good in base_map.items() if not good)
    note = (f"mutants={len(muts)} caught={len(caught)} floor={floor}"
            f" baseline_defects={','.join(baseline_bad) or 0} " + " ".join(notes))
    return ok, note


# ---- V15: preconditions dry-run ----------------------------------------------------------------

def preconditions(base, tree, pkg):
    """Resolve every frozen input and parse every leg's frozen table before any leg scores."""
    root = pathlib.Path(tree)  # the tree being measured (the lane, or a control mirror of it)
    blocked = {}
    counts = {"inputs": 0, "tables": 0}

    def need(legs, ok, what):
        counts["inputs"] += 1
        if not ok:
            for leg in legs:
                blocked.setdefault(leg, what)

    def parse(legs, fn, what):
        counts["tables"] += 1
        try:
            ok = bool(fn())
        except Exception:
            ok = False
        if not ok:
            for leg in legs:
                blocked.setdefault(leg, what)

    # Real-package pins exist only for the pinned package; a control package has no probe or capture pin.
    if pkg.pinned:
        need(("V1", "V10", "V12"), all(sha256(pathlib.Path(pkg.capdir) / n) == d for n, d in base.CAPTURES.items()),
             "a capture does not resolve to its frozen digest")
        need(("V2", "V5"), base.ready(PROBE_SHA256) and sha256(root / PROBE_REL) == PROBE_SHA256,
             "the probe pin is pending, or the probe is absent or not at its frozen digest")
        need(("V4", "V5", "V7", "V10"), base.ready(DRY_SHA256) and sha256(pkg.dry) == DRY_SHA256,
             "the dry-table pin is pending, or the table is absent or not at its frozen digest")
    need(("V2", "V8"), base.ready(GATE_SHA256) and sha256(root / GATE_REL) == GATE_SHA256,
         "the gate is not at its frozen digest")
    receipt = base.text_or_none(pkg.receipt)
    need(("V4", "V7", "V9", "V10"), receipt is not None, "the receipt is unreadable")
    entry = base.text_or_none(pkg.entry)
    need(("V4", "V7", "V9", "V10", "V11"), entry is not None, "the entry is unreadable")
    need(("V3", "V6", "V9", "V12"), base.text_or_none(pkg.registry) is not None, "the source registry is unreadable")
    need(("V9",), base.text_or_none(pkg.readme) is not None, "the README is unreadable")
    need(("V9",), (root / "PROVINCE.md").is_file(), "PROVINCE.md is absent")
    need(("V8",), (root / ORDER_REL).is_file(), "order_check.py is absent")
    need(("V8",), (root / CLAIMS_REL).is_file(), f"{CLAIMS_REL} is absent")

    def tags_cases():
        tags, ids = base.dry_table(pkg)
        return tags and ids

    parse(("V4", "V7", "V10"), tags_cases, "the frozen dry table parses to zero tags or zero cases")
    parse(("V4", "V7", "V9", "V10"), lambda: base.receipt_cases(receipt or ""), "the receipt parses to zero CASE lines")
    parse(("V7",), lambda: map_rows(entry or "")[0] is not None, "the requirement map has no parsable header")
    parse(("V9",), lambda: re.search(r"^## Case table\n", entry or "", re.M), "the case table is absent")
    parse(("V10",), lambda: re.search(r"^## Mechanism\n", entry or "", re.M), "the mechanism section is absent")
    parse(("V11",), lambda: len(base.PRED_BLOCK.findall(
        (base.PRED_SECTION.search(entry or "") or [None, ""])[1])) == 1,
          "the predictor section does not hold exactly one python block")
    if base.ready(MUT_N) and base.ready(MUT_FLOOR):
        parse(("V14",), lambda: load_plan(root) is not None, f"the mutation plan is absent or unparsable: {MUT_PLAN_REL}")
    note = f"inputs={counts['inputs']} tables={counts['tables']} blocked={len(blocked)}"
    return not blocked, note, blocked


# ---- driver ------------------------------------------------------------------------------------

def run_legs(base, root, lane, pkg, work, which):
    table = {
        "V1": lambda: base.v1(pkg),
        "V2": lambda: base.v2(lane, pkg, work),
        "V3": lambda: base.v3(pkg),
        "V4": lambda: base.v4(pkg),
        "V5": lambda: base.v5(lane, pkg),
        "V6": lambda: base.v6(pkg),
        "V7": lambda: v7(base, pkg),
        "V8": lambda: v8(base, root, pathlib.Path(work) / "gate"),
        "V9": lambda: base.v9(pkg),
        "V10": lambda: base.v10(pkg),
        "V11": lambda: base.v11(pkg, work),
        "V12": lambda: base.v12(pkg),
        "V13": lambda: base.v13(lane, work),
        "V14": lambda: v14(base, root, pathlib.Path(work) / "mutation"),
        "V15": lambda: None,
    }
    blocked = {}
    if "V15" in which:
        ok15, note15, blocked = preconditions(base, lane, pkg)
        print(f"V15 {'ok' if ok15 else 'DEFECT'} {note15}")
        res = [("V15", ok15, note15)]
    else:
        res = []
    for name in which:
        if name == "V15":
            continue
        if name in blocked:
            ok, note = False, f"precondition: {blocked[name]}"
        else:
            try:
                ok, note = table[name]()
            except Exception as e:  # a leg that cannot run is a defect, never a pass
                ok, note = False, f"error {type(e).__name__}: {e}"
        print(f"{name} {'ok' if ok else 'DEFECT'} {note}")
        res.append((name, ok, note))
    return res


LEGS = ("V15", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11", "V12", "V13", "V14")


def main(argv=None):
    ap = argparse.ArgumentParser(description="round-49 C2 counter (v4) — TB2 polyglot-c-py package admission")
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    ap.add_argument("--dry", action="store_true",
                    help="stage-check: score every leg except V2 (the probe re-run); never prints `pass`, exits 1")
    ap.add_argument("--control", choices=CONTROL_ORDER, default=None,
                    help="measure a frozen control tree instead of the package; never prints `pass`, exits 1")
    a = ap.parse_args(argv)
    root = pathlib.Path(a.lane).resolve()
    if a.work:
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    try:
        base = load_base(root)
    except SetupError as e:
        print(f"SETUP {e}")
        print("PREDICATE R49-C2 fail")
        return 2
    dry = a.dry or bool(a.control)
    which = [leg for leg in LEGS if not (dry and leg == "V2")]
    rc, head = git(root, "rev-parse", "HEAD")
    print(f"REV {head.strip() if rc == 0 else 'none (not a git work tree)'} lane={root}")
    with tempfile.TemporaryDirectory(prefix="k49-c2-", dir=a.work) as work:
        lane = root
        if a.control:
            lane = control_tree(root, work, a.control)
            print(f"CONTROL {a.control} tree={lane} p10=disabled")
        try:
            pkg = base.filler_pkg(lane) if a.control == "filler" else base.real_pkg(lane)
        except (ValueError, OSError, KeyError, json.JSONDecodeError) as e:
            print(f"PACKAGE unreadable: {e}")
            defects = 0
            for name in which:
                if name == "V13":
                    try:
                        ok, note = base.v13(lane, work)
                    except Exception as e2:
                        ok, note = False, f"error {type(e2).__name__}: {e2}"
                else:
                    ok, note = False, f"package unreadable: {e}"
                defects += not ok
                print(f"{name} {'ok' if ok else 'DEFECT'} {note}")
            print(f"checks={len(which)} defects={defects}")
            print(f"PREDICATE R49-C2 {'fail' if defects else 'dry'}")
            return 1
        res = run_legs(base, root, lane, pkg, work, which)
        defects = sum(1 for _n, ok, _note in res if not ok)
        print(f"checks={len(res)} defects={defects}")
        if defects:
            print("PREDICATE R49-C2 fail")
            return 1
        if dry:
            print("PREDICATE R49-C2 dry")  # a stage-check is structurally clean; it is never an admission
            return 1
        print("PREDICATE R49-C2 pass")
        return 0


if __name__ == "__main__":
    sys.exit(main())
