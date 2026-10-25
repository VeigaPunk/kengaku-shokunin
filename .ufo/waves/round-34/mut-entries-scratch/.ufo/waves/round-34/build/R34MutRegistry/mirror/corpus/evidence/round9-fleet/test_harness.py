#!/usr/bin/env python3
"""Adversarial harness battery for round-8 horizon.py (kengaku round 9, mutation lane).

Proves/disproves that the round-8 probe's parser and graders classify failures
correctly, by feeding synthetic adversarial inputs. OFFLINE: no HTTP, no repo
writes. READ-ONLY access to the repo evidence files for the fidelity check and
the blast-radius audit.

IMPORT SIDE-EFFECT FINDING (why functions are copied, not imported):
  horizon.py L15-16 run at MODULE level:
      os.makedirs("/tmp/bench-r8", exist_ok=True)
      LOGF = open("/tmp/bench-r8/results.jsonl", "a")
  Merely `import horizon` would create /tmp/bench-r8 and append-open the live
  round-8 results file (write handle, file created if absent). Everything below
  is therefore a VERBATIM copy of the target functions (provenance in comments);
  a runtime fidelity check re-execs the original source text from horizon.py and
  cross-checks every case against the copies (see FIDELITY section of output).

Run: python3 /tmp/kengaku-r9/test_harness.py   (exit 0 unless a case crashes)
"""
import json, re, itertools, os, sys

R8  = "/home/vgpnk/projects/shokunin/kengaku-shokunin/corpus/evidence/round8-horizon/results.jsonl"
SRC = "/home/vgpnk/projects/shokunin/kengaku-shokunin/corpus/evidence/round8-horizon/horizon.py"

# ================= VERBATIM COPIES (horizon.py @ HEAD f147a27) =================
# L38-47
def extract_json_block(text):
    blocks = re.findall(r"```(?:json)?\s*\n(.*?)```", text, re.S)
    if blocks:
        try: return json.loads(blocks[-1])
        except Exception: pass
    m = re.findall(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]", text, re.S)
    for cand in reversed(m):
        try: return json.loads(cand)
        except Exception: continue
    return None

# L119-123
def grade_state(got, want):
    """returns (exact, n_wrong_keys)"""
    if not isinstance(got, dict): return False, len(want)
    wrong = sum(1 for k in set(got) | set(want) if got.get(k) != want.get(k))
    return got == want, wrong

# L226-227
CONFLICT_ROWS = [["A","B","C","D"], ["B","C","D","A"], ["A","B","D","C"]]
BENIGN_ROWS   = [["A","B","C","D"], ["B","A","D","C"], ["C","D","A","B"]]

# L229-230
def col_conflict_free(rows):
    return all(len(set(r[c] for r in rows)) == len(rows) for c in range(4))

# L232-236
def valid_latin(sq):
    if not isinstance(sq, list) or len(sq) != 4: return False
    sym = {"A","B","C","D"}
    if not all(isinstance(r, list) and len(r) == 4 and set(r) == sym for r in sq): return False
    return all(set(sq[r][c] for r in range(4)) == sym for c in range(4))

# L238-241
def rows_perm_only(sq):
    sym = {"A","B","C","D"}
    return isinstance(sq, list) and len(sq) == 4 and \
        all(isinstance(r, list) and set(r) == sym for r in sq)

# L270-289
def grade_c(got, prior_rows, with_rule):
    out = {"ok": False, "viol_ok": False, "square_valid": False,
           "preserved": False, "over_repair": False, "parse": got is not None}
    if not isinstance(got, dict): return out
    viol, sq = got.get("violations"), got.get("square")
    if not isinstance(viol, list) or not isinstance(sq, list): return out
    out["square_valid"] = valid_latin(sq) if with_rule else rows_perm_only(sq)
    changed = set(viol)
    kept_ok = all(sq[i] == prior_rows[i] for i in range(3) if (i + 1) not in changed)
    out["preserved"] = kept_ok
    remaining = [prior_rows[i] for i in range(3) if (i + 1) not in changed]
    feasible = col_conflict_free(remaining) if with_rule else True
    out["viol_ok"] = feasible and kept_ok
    if with_rule and out["viol_ok"]:
        minimal_sz = next((sz for sz in range(4)
                           if any(col_conflict_free([prior_rows[i] for i in range(3) if i not in c])
                                  for c in itertools.combinations(range(3), sz))), None)
        out["over_repair"] = minimal_sz is not None and len(changed) > minimal_sz
    out["ok"] = out["square_valid"] and out["viol_ok"] and out["preserved"]
    return out
# ============================ END VERBATIM COPIES =============================

CASES = []  # (id, family, expectation, observer, predicate)
def case(cid, fam, expect, obs_fn, pred_fn):
    CASES.append((cid, fam, expect, obs_fn, pred_fn))

W5 = {"nails": 5, "bolts": 2, "screws": 3, "washers": 4, "hinges": 6}   # a representative want
F = lambda v: json.dumps(v)

# ---------- extract_json_block battery ----------
_ans = F(W5)
ILLU = ("Here is the format example:\n```json\n" + F({"x": 1}) + "\n```\n"
        "Final answer:\n```json\n" + _ans + "\n```")
case("E01","extract","illustrative fence before answer -> answer dict",
     lambda: extract_json_block(ILLU), lambda o: o == W5)
E02_TEXT = ("```json\n" + _ans + "\n```\nWait, correcting:\n```json\n"
            + F({"nails": 9, "bolts": 2, "screws": 3, "washers": 4, "hinges": 6})[:17])
case("E02","extract","final fence truncated (finish=length shape) -> parse None",
     lambda: extract_json_block(E02_TEXT), lambda o: o is None)
case("E03","extract","E02 pipeline grade -> ok must be False (masking check)",
     lambda: grade_state(extract_json_block(E02_TEXT), W5), lambda o: o[0] is False)
case("E04","extract","no fence, bare balanced dict at end -> dict",
     lambda: extract_json_block("The state is " + _ans), lambda o: o == W5)
case("E05","extract","fenced nested one-level dict -> full dict",
     lambda: extract_json_block("```json\n" + F({"nails": 5, "meta": {"src": 1}}) + "\n```"),
     lambda o: o == {"nails": 5, "meta": {"src": 1}})
E06_TEXT = 'Result: ' + F({"nails": 5, "detail": {"min": {"low": 1}}})
case("E06","extract","fenceless 2-level nesting -> outer dict (not fragment)",
     lambda: extract_json_block(E06_TEXT), lambda o: o == {"nails": 5, "detail": {"min": {"low": 1}}})
case("E07","extract","only fence truncated, no earlier fence -> None",
     lambda: extract_json_block("```json\n" + '{"nails": 5, "bol'), lambda o: o is None)
case("E08","extract","fenced dict with trailing comma -> None (strict JSON)",
     lambda: extract_json_block("```json\n" + F({"nails": 5})[:-1] + ",}\n```"), lambda o: o is None)
APO = ("```json\n" + _ans + "\n```\nSorry, I meant " + F({"nails": 9}))
case("E09","extract","answer fence then apology w/ stray dict -> answer fence",
     lambda: extract_json_block(APO), lambda o: o == W5)
case("E10","extract+grade","float values 5.0 vs int 5 -> grade ok must be False (spec: integers)",
     lambda: grade_state(extract_json_block("```json\n" + F({"nails": 5.0, "bolts": 2.0}) + "\n```"),
                         {"nails": 5, "bolts": 2}), lambda o: o[0] is False)
case("E11","extract+grade","JSON true vs int 1 -> grade ok must be False (type error)",
     lambda: grade_state(extract_json_block("```json\n" + F({"nails": True}) + "\n```"),
                         {"nails": 1}), lambda o: o[0] is False)
case("E12","extract","empty string -> None",
     lambda: extract_json_block(""), lambda o: o is None)
SQ4 = [["A","B","C","D"],["B","C","D","A"],["C","D","A","B"],["D","A","B","C"]]
case("E13","extract","fenced JSON array (C-cell shape) -> list",
     lambda: extract_json_block("```json\n" + F(SQ4) + "\n```"), lambda o: o == SQ4)
ZW = "\u200b"
case("E14","extract","zero-width space inside dict body -> None (invalid JSON)",
     lambda: extract_json_block("```json\n" + '{"nails": 5,' + ZW + '"bolts": 2}' + "\n```"),
     lambda o: o is None)
case("E15","extract","zero-width space in fence label -> dict via fallback",
     lambda: extract_json_block("```json" + ZW + "\n" + _ans + "\n```"), lambda o: o == W5)
case("E16","extract","uppercase ```JSON label -> dict via fallback",
     lambda: extract_json_block("```JSON\n" + _ans + "\n```"), lambda o: o == W5)
case("E17","extract","inline fence, no newline after label -> dict via fallback",
     lambda: extract_json_block("```json" + _ans + "```"), lambda o: o == W5)
case("E18","extract","orphan closer: bare dict then ``` (real A-CKPT r8 shape) -> dict",
     lambda: extract_json_block(_ans + "\n```"), lambda o: o == W5)
case("E19","extract","plain 'ok' text -> None", lambda: extract_json_block("ok"), lambda o: o is None)
E20_TEXT = '```json\n{"note": "use ```json fences", "nails": 5}\n```'
case("E20","extract","fence marker inside JSON string value -> dict (fallback rescue)",
     lambda: extract_json_block(E20_TEXT), lambda o: o == {"note": "use ```json fences", "nails": 5})

# ---------- grade_state battery (spec: exact JSON-state equality; wrong = #keys differing) ----------
g = lambda got, want: grade_state(got, want)
case("G01","grade_state","extra key -> (False,1)", lambda: g({**W5, "extra": 1}, W5),
     lambda o: o == (False, 1))
case("G02","grade_state","missing key -> (False,1)", lambda: g({k: v for k, v in list(W5.items())[:-1]}, W5),
     lambda o: o == (False, 1))
case("G03","grade_state","same items, different key order -> (True,0)",
     lambda: g(dict(reversed(list(W5.items()))), W5), lambda o: o == (True, 0))
case("G04","grade_state","string '5' vs int 5 -> (False,1)",
     lambda: g({**W5, "nails": "5"}, W5), lambda o: o == (False, 1))
case("G05","grade_state","null value vs int -> (False,1)",
     lambda: g({**W5, "nails": None}, W5), lambda o: o == (False, 1))
case("G06","grade_state","non-dict got: list -> (False,len(want))", lambda: g([1, 2], W5),
     lambda o: o == (False, len(W5)))
case("G07","grade_state","non-dict got: str", lambda: g("nope", W5), lambda o: o == (False, len(W5)))
case("G08","grade_state","non-dict got: None", lambda: g(None, W5), lambda o: o == (False, len(W5)))
case("G09","grade_state","both empty dicts -> (True,0)", lambda: g({}, {}), lambda o: o == (True, 0))
case("G10","grade_state","zero-valued key present after MOV -> (True,0)",
     lambda: g({"hinges": 0, "nails": 5}, {"hinges": 0, "nails": 5}), lambda o: o == (True, 0))
case("G11","grade_state","zero-valued key dropped -> (False,1)",
     lambda: g({"nails": 5}, {"hinges": 0, "nails": 5}), lambda o: o == (False, 1))
case("G12","grade_state","float 5.0 vs int 5 -> (False,1) per integer spec",
     lambda: g({"nails": 5.0}, {"nails": 5}), lambda o: o == (False, 1))
case("G13","grade_state","bool true vs int 1 -> (False,1) per integer spec",
     lambda: g({"nails": True}, {"nails": 1}), lambda o: o == (False, 1))
case("G14","grade_state","extra key w/ null value -> nwrong must be 1, not 0",
     lambda: g({"nails": 5, "z": None}, {"nails": 5}), lambda o: o == (False, 1))

# ---------- grade_c battery ----------
flags = lambda o: ("ok=%s viol_ok=%s sq=%s pres=%s over=%s parse=%s" % (
    o["ok"], o["viol_ok"], o["square_valid"], o["preserved"], o["over_repair"], o["parse"]))
GOOD_SQ  = [["A","B","C","D"],["B","C","D","A"],["C","D","A","B"],["D","A","B","C"]]  # completes CONFLICT
OVER_SQ  = GOOD_SQ
OVER_SQ2 = [["C","D","A","B"],["B","C","D","A"],["D","A","B","C"],["A","B","C","D"]]  # keeps r2, rewrites r1
case("C01","grade_c/conflict","minimal repair viol[3] + valid square -> ok True",
     lambda: grade_c({"violations":[3], "square":GOOD_SQ}, CONFLICT_ROWS, True),
     lambda o: o["ok"] is True and o["over_repair"] is False)
case("C02","grade_c/conflict","under-repair viol[] + unchanged conflict square -> ok False",
     lambda: grade_c({"violations":[], "square":CONFLICT_ROWS + [["D","A","B","C"]]}, CONFLICT_ROWS, True),
     lambda o: o["ok"] is False)
case("C03","grade_c/conflict","over-repair viol[1,2,3] full rewrite -> spec ok False",
     lambda: grade_c({"violations":[1,2,3], "square":OVER_SQ}, CONFLICT_ROWS, True),
     lambda o: o["ok"] is False)
case("C04","grade_c/conflict","over-repair viol[1,3] (r2 kept, r1 rewritten) -> spec ok False",
     lambda: grade_c({"violations":[1,3], "square":OVER_SQ2}, CONFLICT_ROWS, True),
     lambda o: o["ok"] is False)
case("C05","grade_c/conflict","viol[3] but row1 also changed -> ok False (non-preserved)",
     lambda: grade_c({"violations":[3], "square":[["D","B","C","A"],["B","C","D","A"],
                                             ["C","D","A","B"],["A","B","C","D"]]}, CONFLICT_ROWS, True),
     lambda o: o["ok"] is False and o["preserved"] is False)
case("C06","grade_c/conflict","rows valid, square NOT Latin -> ok False",
     lambda: grade_c({"violations":[3], "square":[["A","B","C","D"],["B","C","D","A"],
                                             ["C","D","A","B"],["A","B","C","D"]]}, CONFLICT_ROWS, True),
     lambda o: o["ok"] is False and o["square_valid"] is False)
case("C07","grade_c/conflict","wrong violation target viol[2] -> ok False",
     lambda: grade_c({"violations":[2], "square":[["A","B","C","D"],["C","D","A","B"],
                                             ["A","B","D","C"],["D","A","B","C"]]}, CONFLICT_ROWS, True),
     lambda o: o["ok"] is False)
case("C08","grade_c/conflict","got None -> all False, parse False",
     lambda: grade_c(None, CONFLICT_ROWS, True),
     lambda o: (o["ok"], o["parse"]) == (False, False) and not o["viol_ok"] and not o["preserved"])
case("C09","grade_c/conflict","bare array parse (non-dict) -> parse True, ok False",
     lambda: grade_c(GOOD_SQ, CONFLICT_ROWS, True),
     lambda o: o["ok"] is False and o["parse"] is True)
case("C10","grade_c/conflict","violations as strings ['3'] -> fail-safe ok False",
     lambda: grade_c({"violations":["3"], "square":GOOD_SQ}, CONFLICT_ROWS, True),
     lambda o: o["ok"] is False)
BEN_SQ = BENIGN_ROWS + [["D","C","B","A"]]  # unique Latin completion of BENIGN_ROWS
case("C11","grade_c/benign","correct: viol[] + unchanged square -> ok True",
     lambda: grade_c({"violations":[], "square":BEN_SQ}, BENIGN_ROWS, True),
     lambda o: o["ok"] is True and o["over_repair"] is False)
case("C12","grade_c/benign","spurious repair viol[3] + Latin rewrite -> spec ok False (r8 rep0 shape)",
     lambda: grade_c({"violations":[3], "square":[["A","B","C","D"],["B","A","D","C"],
                                             ["D","C","B","A"],["C","D","A","B"]]}, BENIGN_ROWS, True),
     lambda o: o["ok"] is False)
case("C13","grade_c/benign","spurious viol[2,3] w/ invalid square -> ok False (over flag only)",
     lambda: grade_c({"violations":[2,3], "square":[["A","B","C","D"],["C","A","B","D"],
                                             ["B","D","A","C"],["D","C","D","A"]]}, BENIGN_ROWS, True),
     lambda o: o["ok"] is False and o["over_repair"] is True)
case("C14","grade_c/norule","correct: viol[] + unchanged square -> ok True",
     lambda: grade_c({"violations":[], "square":BEN_SQ}, BENIGN_ROWS, False),
     lambda o: o["ok"] is True)
case("C15","grade_c/norule","spurious viol[2], square unchanged -> spec ok False (viol content ungraded)",
     lambda: grade_c({"violations":[2], "square":BEN_SQ}, BENIGN_ROWS, False),
     lambda o: o["ok"] is False)
case("C16","grade_c/norule","dropped row (3 rows) -> ok False",
     lambda: grade_c({"violations":[], "square":BENIGN_ROWS}, BENIGN_ROWS, False),
     lambda o: o["ok"] is False)

# ============================ fidelity check ============================
def extract_source_fns(path):
    """Pull the six function defs straight out of horizon.py text and exec them."""
    lines = open(path).read().splitlines()
    names = ["extract_json_block", "grade_state", "col_conflict_free",
             "valid_latin", "rows_perm_only", "grade_c"]
    out = []
    for n in names:
        i0 = next(i for i, l in enumerate(lines) if l.startswith(f"def {n}("))
        i1 = next(i for i in range(i0 + 1, len(lines))
                  if re.match(r"^(def |[A-Z_]+ = |# -)", lines[i]))
        out.append("\n".join(lines[i0:i1]))
    ns = {"json": json, "re": re, "itertools": itertools}
    exec("\n\n".join(out), ns)
    return ns

# ============================ run battery ============================
def main():
    print("=" * 100)
    print("FIDELITY: copies vs horizon.py source-extracted originals")
    try:
        orig = extract_source_fns(SRC)
        cmap = {"extract_json_block": extract_json_block, "grade_state": grade_state,
                "col_conflict_free": col_conflict_free, "valid_latin": valid_latin,
                "rows_perm_only": rows_perm_only, "grade_c": grade_c}
        div = 0
        for cid, fam, expect, obs_fn, pred_fn in CASES:
            o1, o2 = obs_fn(), None
            import types
            # re-run observer against originals by swapping globals
            globals().update({k: orig[k] for k in cmap})
            try: o2 = obs_fn()
            except Exception as e: o2 = f"ERR {e}"
            globals().update(cmap)
            if o1 != o2:
                div += 1; print(f"  DIVERGENCE {cid}: copy={o1!r} original={o2!r}")
        print(f"  divergence across {len(CASES)} cases x 6 fns: {div}")
    except Exception as e:
        print(f"  fidelity check unavailable: {e!r}")

    print("=" * 100)
    print(f"{'ID':<4} {'FAMILY':<17} {'EXPECTED':<52} {'OBSERVED':<58} VERDICT")
    print("-" * 140)
    npass = nfail = 0
    for cid, fam, expect, obs_fn, pred_fn in CASES:
        try:
            o = obs_fn()
            verdict = "PASS" if pred_fn(o) else "FAIL"
        except Exception as e:
            o, verdict = f"CRASH {e!r}", "FAIL"
        npass, nfail = npass + (verdict == "PASS"), nfail + (verdict == "FAIL")
        print(f"{cid:<4} {fam:<17} {expect:<52} {str(o):<58} {verdict}")
    print("-" * 140)
    print(f"TOTAL {len(CASES)} cases: {npass} PASS (spec met), {nfail} FAIL (harness defect candidate)")

    # ==================== blast radius on real r8 data ====================
    print("=" * 100)
    print("BLAST RADIUS on corpus/evidence/round8-horizon/results.jsonl (read-only)")
    recs = [json.loads(l) for l in open(R8)]
    graded = [r for r in recs if r["cell"] != "meta" and "ok" in r]
    acks   = [r for r in recs if r["cell"] != "meta" and "ok" not in r]
    multi  = [r for r in graded if len(re.findall(r"```", r["raw"])) >= 4]
    # sanity: re-extract with the copied parser must reproduce recorded got
    sane = sum(1 for r in graded if extract_json_block(r["raw"]) == r["got"])
    print(f"records: total={len(recs)} graded={len(graded)} acks={len(acks)}(raw 80-char truncated, ungraded)")
    print(f"sanity: copied parser re-extract == recorded got: {sane}/{len(graded)}")
    # census
    fl = [r for r in graded if r.get("finish") == "length"]
    floats = [r for r in graded if isinstance(r.get("got"), dict)
              and any(isinstance(v, float) and not isinstance(v, bool) for v in r["got"].values())]
    bools  = [r for r in graded if isinstance(r.get("got"), dict) and any(isinstance(v, bool) for v in r["got"].values())]
    nulls  = [r for r in graded if isinstance(r.get("got"), dict) and any(v is None for v in r["got"].values())]
    orphan = [r for r in graded if r["raw"].endswith("```") and not r["raw"].startswith("```")]
    print(f"census: multi-fence(>=2)={len(multi)}  orphan-closer={len(orphan)}  finish=length={len(fl)}"
          f"  floats={len(floats)}  bools={len(bools)}  nulls={len(nulls)}"
          f"  uppercase-label={sum(1 for r in graded if '```JSON' in r['raw'])}")
    # live E02 events: graded record whose LAST fence-opener body fails json.loads
    # while an earlier fence/brace supplied the recorded parse
    def last_opener_body(text):
        opens = list(re.finditer(r"```(?:json)?\s*\n", text))
        if not opens: return None
        rest = text[opens[-1].end():]
        close = rest.find("```")
        return rest if close == -1 else rest[:close]
    live_e02 = []
    for r in graded:
        b = last_opener_body(r["raw"])
        if b is None or r.get("got") is None: continue
        try: json.loads(b)
        except Exception: live_e02.append(r)
    print(f"live E02 events (graded record whose LAST fence-opener body is unparseable "
          f"while an earlier block supplied the parse): {len(live_e02)}")
    # FIX-P: grade ONLY the last fence block; None if it fails; brace fallback only when no opener
    def fixp_parse(text):
        if last_opener_body(text) is None:
            return extract_json_block(text)          # no opener at all: keep brace fallback
        b = last_opener_body(text)
        try: return json.loads(b)
        except Exception: return None
    def prior_for(cell):
        return {"C-conflict": (CONFLICT_ROWS, True), "C-benign": (BENIGN_ROWS, True),
                "C-norule": (BENIGN_ROWS, False)}.get(cell)
    flipP, fixP_cells = 0, {}
    for r in graded:
        new = fixp_parse(r["raw"])
        c = r["cell"]
        if c.startswith(("A-", "B-")):
            ok2, nw2 = grade_state(new, r["want"])
        elif c == "C-MONO":
            ok2, nw2 = valid_latin(new), None
        else:
            pr, wr = prior_for(c); g2 = grade_c(new, pr, wr); ok2, nw2 = g2["ok"], None
        changed = (ok2 != r["ok"]) or ("nwrong" in r and nw2 is not None and nw2 != r["nwrong"])
        if changed:
            flipP += 1; fixP_cells[c] = fixP_cells.get(c, 0) + 1
    print(f"FIX-P (grade LAST fence-opener block only; earlier-block/brace fallback only when no opener) "
          f"records flipping ok/nwrong: {flipP} {fixP_cells}")
    # FIX-T: type-strict grade_state (int vs float vs bool are distinct) actual flips
    flipT = 0
    for r in graded:
        if not r["cell"].startswith(("A-", "B-")): continue
        got, want = r.get("got"), r.get("want")
        exact2 = (got == want and isinstance(got, dict) and isinstance(want, dict)
                  and set(got) == set(want)
                  and all(type(got[k]) is type(want[k]) for k in want))
        if exact2 != r["ok"]: flipT += 1
    print(f"FIX-T (type-strict grade_state) records flipping ok: {flipT}")
    # FIX-O: fold over_repair into ok
    fixO = [r for r in graded if r["cell"].startswith("C-") and r.get("over_repair") and r["ok"]]
    print(f"FIX-O (ok &= not over_repair) records that would flip ok: {len(fixO)} -> "
          f"{[(r['cell'], r.get('rep')) for r in fixO]}")

if __name__ == "__main__":
    sys.exit(main() and None or 0)
