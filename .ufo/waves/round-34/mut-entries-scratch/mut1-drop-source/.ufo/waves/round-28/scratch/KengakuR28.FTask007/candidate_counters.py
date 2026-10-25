"""Author-side independent census of the candidate's inventory counters (round28 FTask007).

Reads pinned test.raw.json as data only; imports no production/alternate oracle and executes
no upstream code. Asserts the literal numbers printed in
.ufo/waves/round-28/drafts/webarena-task-spec-audit.md:59-60,72,101-108 and the task-7 stratum facts
in .ufo/waves/round-28/build/Task007.md:26.
"""
import collections
import json
import sys


def stratum(task):
    return (tuple(sorted(task["sites"])), tuple(sorted(task["eval"]["eval_types"])))


def main(raw_path: str) -> int:
    raw = json.load(open(raw_path))
    ids = [t["task_id"] for t in raw]
    assert len(raw) == 812 and len(set(ids)) == 812 and sorted(ids) == list(range(812))

    sets = collections.Counter(tuple(sorted(t["eval"]["eval_types"])) for t in raw)
    assert sets == {
        ("string_match",): 325,
        ("program_html",): 282,
        ("url_match",): 66,
        ("string_match", "url_match"): 10,
        ("program_html", "url_match"): 129,
    }, sets

    strata = collections.defaultdict(list)
    for t in raw:
        strata[stratum(t)].append(t["task_id"])
    assert len(strata) == 27, len(strata)

    ordered = sorted(strata)
    minima = [min(strata[s]) for s in ordered]
    assert minima[:16] == [389, 590, 132, 173, 44, 552, 681, 791, 556, 356, 7, 377, 759, 424, 97, 399]
    assert minima[:16] == json.load(open("plans/fixtures/r28/webarena/selected-task-ids.json"))

    ops = collections.Counter()
    targets = 0
    reqops = collections.Counter()
    loc = collections.Counter()
    urls = collections.Counter()
    for t in raw:
        ra = t["eval"].get("reference_answers")
        if isinstance(ra, dict):
            for k in ra:
                ops[k] += 1
        for ph in t["eval"].get("program_html") or []:
            targets += 1
            L = ph.get("locator") or ""
            if L == "":
                loc["full-page"] += 1
            elif L.startswith("func:"):
                loc["helper"] += 1
            else:
                loc["javascript"] += 1
            u = ph.get("url") or ""
            if u == "last":
                urls["last"] += 1
            elif u.startswith("func:"):
                urls["helper"] += 1
            else:
                urls["navigation"] += 1
            for k in (ph.get("required_contents") or {}):
                reqops[k] += 1
    assert ops == {"exact_match": 45, "must_include": 176, "fuzzy_match": 118}, ops
    assert targets == 651 and reqops == {"must_include": 463, "exact_match": 188}, (targets, reqops)
    assert loc == {"full-page": 105, "javascript": 524, "helper": 22}, loc
    assert urls == {"last": 238, "navigation": 338, "helper": 75}, urls

    t7 = [t for t in raw if t["task_id"] == 7][0]
    t9 = [t for t in raw if t["task_id"] == 9][0]
    grp = [t for t in raw if stratum(t) == (("map",), ("string_match",))]
    assert len(grp) == 89 and min(t["task_id"] for t in grp) == 7
    mix = collections.Counter(tuple(sorted(t["eval"]["reference_answers"])) for t in grp)
    assert mix == {("fuzzy_match",): 43, ("must_include",): 31, ("exact_match",): 13,
                   ("fuzzy_match", "must_include"): 2}, mix
    assert t7["eval"]["reference_answers"]["exact_match"] == \
        t9["eval"]["reference_answers"]["must_include"][0]
    assert t7["eval"]["eval_types"] == ["string_match"] and t7["eval"]["reference_url"] == "" \
        and t7["eval"]["program_html"] == [] and t7["eval"]["string_note"] == ""
    assert t7["intent_template_id"] == 79 and t9["intent_template_id"] == 79

    print("812/812 IDs0-811:", True)
    print("eval-type sets:", dict(sets))
    print("strata:", len(strata), "first16 minima:", minima[:16])
    print("string operators:", dict(ops))
    print("program_html targets:", targets, "required_contents:", dict(reqops))
    print("locator classes:", dict(loc))
    print("target URL classes:", dict(urls))
    print("task7 stratum: 89 tasks, min id 7; key mix:", dict(mix))
    print("task7 exact reference == task9 must_include[0]:", True)
    print("assertions: ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
