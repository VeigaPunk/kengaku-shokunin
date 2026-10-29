#!/usr/bin/env python3
"""Neutralize-one-check-at-a-time mutation harness for the frozen C1 counter.

Copies the counter (never edits the lane copy) into a scratch dir, applies one
source-level neutralization, runs --selftest, and reports which selftest cases
fail.  A case that still passes after its target check is neutralized is
VACUOUS with respect to that check.
"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

SRC = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans")
SCRATCH = Path("/fast/scratch/hyaku/kengaku-r53/C1RevCounter")
SCRATCH.mkdir(parents=True, exist_ok=True)
BASE_SRC = (SRC / "round53_c1_triage.py").read_text()

MUTATIONS = {
    "M1_disagree_threshold": [("and dis <= lim and", "and True and")],
    "M2_confirmed_is_true": [('if r.get("confirmed") is not True:', "if False:")],
    "M3_quote_len": [('len(norm(str(r.get("quote", "")))) < QUOTE_MIN_CHARS or norm(r["quote"]) not in span',
                      'len(norm(str(r.get("quote", "")))) < 0 or norm(r["quote"]) not in span')],
    "M4_quote_in_span": [('len(norm(str(r.get("quote", "")))) < QUOTE_MIN_CHARS or norm(r["quote"]) not in span',
                          'len(norm(str(r.get("quote", "")))) < QUOTE_MIN_CHARS or False')],
    "M5_reader_is_author": [('elif not r.get("reader") or r["reader"] in info["authors"] or r["reader"].startswith("KengakuR53"):',
                              "elif False:")],
    "M6_report_digest": [('elif not rep.is_file() or sha256_file(rep) != r.get("report_sha256") or r["reader"] not in str(rep):',
                           "elif False:")],
    "M7_report_names_task": [('elif r["task"] not in rep.read_text(encoding="utf-8", errors="replace"):',
                               "elif False:")],
    "M8_url_example_org": [('elif not re.match(r"https?://[^/\\s]+\\.[^/\\s]+/", str(r.get("url", "")) + "/") or "example.org" in r["url"]:',
                            "elif False:")],
    "M9_fetch_digest": [('if sha256_file(f) != r.get(key + "_sha256"):', "if False:")],
    "M10_sweep_len2": [("if not isinstance(sw, list) or len(sw) < 2:", "if not isinstance(sw, list) or len(sw) < 0:")],
    "M11_blob_match": [("elif blob_sha1(f.read_bytes()) == blobs.get(p):", "elif True:")],
    "M12_population_sha": [('pop_ok = sha256_file(pop_p) == cfg["POP_SHA"]', "pop_ok = True")],
    "M13_author_seat_label": [("or set(r[\"labelers\"]) & authors", "or False")],
    "M14_two_distinct_labelers": [('len(set(r["labelers"])) != 2', 'len(set(r["labelers"])) < 0')],
    "M15_classifier_sha": [('sha_ok = sha256_file(clf) == d.get("classifier_sha256")', "sha_ok = True")],
    "M16_prior_art_new_at_least_1": [("and new >= 1", "and new >= 0")],
    "M17_capture_absent_counted_as_match": [("if not f.is_file():\n                absent += 1", "if not f.is_file():\n                absent += 0")],
    "M18_contested_limit": [("and len(contested) <= ORACLE_MAX_CONTESTED * n", "and True")],
    "M19_control_min": [("CONTROL_MIN = 10", "CONTROL_MIN = 0")],
    "M20_confirm_min": [("CONFIRM_MIN = 3", "CONFIRM_MIN = 0")],
    "M21_url_min": [("URL_MIN = 3", "URL_MIN = 0")],
    "M22_tests_total": [('n == cfg["TESTS_TOTAL"]', "True")],
    "M23_extra_labels_allowed": [("and not extra and", "and True and")],
    "M24_bad_label_rows_allowed": [("and not bad and", "and True and")],
}


def run_selftest(src_text: str, tag: str):
    d = Path(tempfile.mkdtemp(prefix=f"mut-{tag}-", dir=str(SCRATCH)))
    (d / "round53_c1_triage.py").write_text(src_text)
    shutil.copy(SRC / "round53_c1_extract.py", d / "round53_c1_extract.py")
    env = dict(os.environ, TMPDIR=str(SCRATCH))
    p = subprocess.run([sys.executable, str(d / "round53_c1_triage.py"), "--selftest"],
                       capture_output=True, text=True, env=env, timeout=900)
    shutil.rmtree(d, ignore_errors=True)
    fails = []
    for line in p.stdout.splitlines():
        if line.startswith("SELFTEST ") and line.rstrip().endswith("FAIL"):
            fails.append(line.split()[1])
    tail = [l for l in p.stdout.splitlines() if l.startswith("SELFTEST cases=")]
    return {"tag": tag, "rc": p.returncode, "failed_cases": fails, "summary": tail[-1] if tail else ""}


def main():
    results = []
    base = run_selftest(BASE_SRC, "baseline")
    results.append(base)
    print("baseline:", json.dumps(base))
    for name, subs in MUTATIONS.items():
        src = BASE_SRC
        applied = True
        for old, new in subs:
            if old not in src:
                applied = False
                break
            src = src.replace(old, new, 1)
        if not applied:
            results.append({"tag": name, "error": "pattern not found"})
            print(name, "PATTERN-NOT-FOUND")
            continue
        r = run_selftest(src, name)
        r["tag"] = name
        results.append(r)
        print(name, "->", json.dumps(r))
    (SCRATCH / "mutation_results.json").write_text(json.dumps(results, indent=1))
    print("WROTE", SCRATCH / "mutation_results.json")


if __name__ == "__main__":
    main()
