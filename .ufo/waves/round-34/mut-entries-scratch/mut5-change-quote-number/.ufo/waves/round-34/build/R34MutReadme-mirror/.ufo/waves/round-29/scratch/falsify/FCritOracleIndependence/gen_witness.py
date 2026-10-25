#!/usr/bin/env python3
"""Upstream-authored reference oracle on the discriminating witnesses (FCritOracleIndependence).

Executes a byte-verified copy of the pinned generator in /tmp/fcoi_gen/<case>/ with a stub
browser_env.env_config holding synthetic *.invalid values (the real browser_env is never present or
imported), then compares the generator's own outputs with (a) the adopted hand fixtures' expected
values and (b) the seven oracle variants of discrimination.py. Never touches the lane except reading
pinned files. Does not import plans/config_projection.py.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import discrimination as disc  # noqa: E402

LANE = disc.LANE
GEN = LANE + "/plans/fixtures/r29/generate_test_data.py"
GEN_SHA = "45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd"
BASE = "/tmp/fcoi_gen"


def run_generator(case, raw, values):
    root = os.path.join(BASE, case)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root + "/scripts")
    os.makedirs(root + "/config_files")
    os.makedirs(root + "/browser_env")
    gen = open(GEN, "rb").read()
    assert hashlib.sha256(gen).hexdigest() == GEN_SHA
    open(root + "/scripts/generate_test_data.py", "wb").write(gen)
    open(root + "/config_files/test.raw.json", "w", encoding="utf-8").write(raw)
    open(root + "/browser_env/__init__.py", "w").write("")
    open(root + "/browser_env/env_config.py", "w").write("".join("%s = %r\n" % (k, v) for k, v in values.items()))
    env = {"PATH": "/usr/bin:/bin", "PYTHONPATH": root, "PYTHONDONTWRITEBYTECODE": "1", "LC_ALL": "C.UTF-8"}
    p = subprocess.run([sys.executable, "scripts/generate_test_data.py"], cwd=root, env=env, capture_output=True, text=True)
    files = sorted(f for f in os.listdir(root + "/config_files") if f not in ("test.raw.json",))
    per_index = []
    i = 0
    while os.path.exists("%s/config_files/%d.json" % (root, i)):
        per_index.append(json.load(open("%s/config_files/%d.json" % (root, i))))
        i += 1
    last = p.stderr.strip().splitlines()[-1] if p.stderr.strip() else ""
    return {"exit": p.returncode, "stderr_last_line": last, "written": files, "per_index": per_index,
            "test_json": open(root + "/config_files/test.json").read() if "test.json" in files else None}


def variant_outcome(variant, raw, values):
    try:
        data, naming = disc.VARIANTS[variant](raw, values)
    except ValueError as e:
        return ("decode_error", type(e).__name__)
    names = ["%s.json" % (i if naming == "index" else d["task_id"]) for i, d in enumerate(data)]
    return ("ok", names, data)


def main():
    H = disc.HAND
    oc = json.load(open(H + "cascade-order.case.json"))
    uc = json.load(open(H + "url-only.fixture.json"))
    ue = json.load(open(H + "url-only.expected.json"))
    ic = json.load(open(H + "index-shuffled-ids.fixture.json"))
    benign = json.load(open(disc.PROFILES))["distinct_origins"]["values"]
    quote_vals = dict(benign, GITLAB='http://gitlab.invalid/a"b')
    bs_vals = dict(benign, REDDIT="http://reddit.invalid/a\\nb")
    later_vals = dict(benign, GITLAB="http://gitlab.invalid/__MAP__")
    small = '[{"task_id":0,"start_url":"__GITLAB__"},{"task_id":1,"start_url":"__REDDIT__/p"}]'
    cases = {
        "cascade_order": (oc["raw_serialized_text"], oc["values"]),
        "url_only": (uc["raw_text"], uc["values"]),
        "index_shuffled": (ic["input_raw_text"], ic["profile_values"]),
        "own_quote_in_value": (small, quote_vals),
        "own_backslash_n_in_value": (small, bs_vals),
        "own_value_contains_later_token": (small, later_vals),
    }
    gen = {}
    for case, (raw, vals) in cases.items():
        g = run_generator(case, raw, vals)
        gen[case] = g
        print("GENERATOR %-32s exit=%d written=%s stderr_last=%r per_index=%s" % (
            case, g["exit"], g["written"], g["stderr_last_line"][:90], json.dumps(g["per_index"])[:200]))
    print("FIXTURE_EXPECTATION_vs_GENERATOR")
    print("cascade_order expected_parsed_value==generator:", gen["cascade_order"]["per_index"] == oc["expected_parsed_value"],
          "| expected_projected_text==generator test.json:", gen["cascade_order"]["test_json"] == oc["expected_projected_text"])
    print("url_only expected projection==generator:", gen["url_only"]["per_index"] == ue["projection"])
    exp_idx = [e["projected_task"] for e in ic["expected_records"]]
    exp_names = [e["output_filename"].split("/")[-1] for e in ic["expected_records"]]
    print("index_shuffled expected projected_task by ordinal==generator:", gen["index_shuffled"]["per_index"] == exp_idx,
          "| expected filenames==generator written:", sorted(exp_names) == sorted(f for f in gen["index_shuffled"]["written"] if f != "test.json"),
          "| generator 0.json task_id:", gen["index_shuffled"]["per_index"][0]["task_id"])
    print("VARIANT_vs_GENERATOR (agree = same decode outcome, same per-index objects, same filenames)")
    for variant in disc.VARIANTS:
        row = {}
        for case, (raw, vals) in cases.items():
            g = gen[case]
            out = variant_outcome(variant, raw, vals)
            if g["exit"] != 0:
                row[case] = "agree" if out[0] == "decode_error" else "DISAGREE(variant parsed)"
            elif out[0] != "ok":
                row[case] = "DISAGREE(variant decode_error)"
            else:
                ours = dict(zip(out[1], out[2]))
                theirs = {"%d.json" % i: obj for i, obj in enumerate(g["per_index"])}
                same = ours == theirs
                row[case] = "agree" if same else "DISAGREE"
        print("%-36s %s" % (variant, json.dumps(row)))


if __name__ == "__main__":
    main()
