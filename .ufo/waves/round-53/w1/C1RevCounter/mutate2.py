#!/usr/bin/env python3
"""Second mutation batch: checks that SHOULD be covered by a selftest case but are not.

Neutralizing a check that no selftest case protects leaves failures=0 -> that check
has no selftest coverage (a coverage gap, i.e. a vacuous selftest battery for it).
"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

SRC = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans")
SCRATCH = Path("/fast/scratch/hyaku/kengaku-r53/C1RevCounter")
BASE_SRC = (SRC / "round53_c1_triage.py").read_text()

MUTATIONS = {
    "N1_never_read_guard": [('and not seen_before(t["task"], texts)', "and True")],
    "N2_r52_confirmations_exclusion": [('and t["task"] not in r52_conf', "and True")],
    "N3_candidate_membership": [('elif r["task"] not in cand or tid not in {x["id"] for x in cand[r["task"]]}:', "elif False:")],
    "N4_duplicate_task": [('elif r["task"] in seen_tasks:', "elif False:")],
    "N5_task_id_matches_index": [('elif t is None or t["task"] != r.get("task"):', "elif False:")],
    "N6_freeze_order": [('order = git(lane, "merge-base", "--is-ancestor", c_fz, c_lab)[0] == 0', "order = True")],
    "N7_author_seats_nonempty": [('ok = sha_ok and order and bool(info["authors"])', "ok = sha_ok and order")],
    "N8_reader_KengakuR53_prefix": [('or r["reader"].startswith("KengakuR53")', "or False")],
    "N9_known_names_task": [('elif v == "phenomenon-known" and not any(n in text for n in tests_of.get(task, [])) and task not in text:',
                             'elif v == "phenomenon-known" and not any(n in text for n in tests_of.get(task, [])) and False:')],
    "N10_sweep_names_task": [('if st is None or task in st or any(n in st for n in tests_of.get(task, [])):', "if st is None:")],
    "N11_sweep_digest": [('if sha256_file(f) != r.get(key + "_sha256"):', "if False:")],
    "N12_quote_word_min": [("not (8 <= len(q.split()) <= 25)", "not (0 <= len(q.split()) <= 25)")],
    "N13_quote_word_max": [("not (8 <= len(q.split()) <= 25)", "not (8 <= len(q.split()) <= 999)")],
    "N14_quote_in_archive": [("or q not in norm(text)", "or False")],
    "N15_confirm_quote_20_chars": [("QUOTE_MIN_CHARS = 20", "QUOTE_MIN_CHARS = 0")],
    "N16_covered_equals_confirmed": [("ok = covered == set(confirmed)", "ok = True")],
    "N17_no_rejected_rows": [("and not rej", "and True")],
    "N18_index_sha_pin": [('idx_ok = sha256_file(idx_p) == cfg["TESTS_INDEX_SHA"]', "idx_ok = True")],
    "N19_pin_tree_sha": [('pin_ok = sha256_file(pin_p) == cfg["PIN_TREE_SHA"]', "pin_ok = True")],
    "N20_excluded_blob": [("and exc_ok and n_paths ==", "and True and n_paths ==")],
    "N21_absent_count": [("absent += 1", "absent += 0")],
    "N22_file_count_184": [('and n_paths == cfg["CAPTURES_EXPECTED"] + 1', "and True")],
    "X1_disagree_and_control_neutralised": [
        ("and dis <= lim and", "and True and"),
        ("ctl_ok = dis52 >= CONTROL_RATIO * max(dis, 1) and dis52 >= CONTROL_MIN", "ctl_ok = True"),
    ],
    "X2_leg2_only_disagree_removed": [("and dis <= lim and", "and True and")],
}


def run_selftest(src_text, tag):
    d = Path(tempfile.mkdtemp(prefix=f"mut2-{tag}-", dir=str(SCRATCH)))
    (d / "round53_c1_triage.py").write_text(src_text)
    shutil.copy(SRC / "round53_c1_extract.py", d / "round53_c1_extract.py")
    env = dict(os.environ, TMPDIR=str(SCRATCH))
    p = subprocess.run([sys.executable, str(d / "round53_c1_triage.py"), "--selftest"],
                       capture_output=True, text=True, env=env, timeout=900)
    shutil.rmtree(d, ignore_errors=True)
    fails = [l.split()[1] for l in p.stdout.splitlines()
             if l.startswith("SELFTEST ") and l.rstrip().endswith("FAIL")]
    tail = [l for l in p.stdout.splitlines() if l.startswith("SELFTEST cases=")]
    return {"tag": tag, "rc": p.returncode, "failed_cases": fails, "summary": tail[-1] if tail else ""}


res = []
for name, subs in MUTATIONS.items():
    src = BASE_SRC
    ok = True
    for old, new in subs:
        if old not in src:
            ok = False
            break
        src = src.replace(old, new, 1)
    if not ok:
        res.append({"tag": name, "error": "pattern not found"})
        print(name, "PATTERN-NOT-FOUND")
        continue
    r = run_selftest(src, name)
    r["tag"] = name
    res.append(r)
    print(name, "->", json.dumps(r))
(SCRATCH / "mutation_results_2.json").write_text(json.dumps(res, indent=1))
print("WROTE", SCRATCH / "mutation_results_2.json")
