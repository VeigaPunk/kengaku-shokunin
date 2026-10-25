#!/usr/bin/env python3
"""Author-side, read-only falsification probe for BUILD case377.

Reimplements only evaluators.py URLEvaluator L187-236 with stdlib urllib.parse.
No upstream import/exec/eval, no network, no production instrument import.
Run: python3 -B probe.py
"""
import json
import urllib.parse as up

RAW = "plans/fixtures/r28/webarena/config_files/test.raw.json"
MAP_HOST = "map.invalid:3000"
BASE = "http://" + MAP_HOST


def raw_task():
    tasks = json.load(open(RAW, encoding="utf-8"))
    t = [x for x in tasks if x["task_id"] == 377]
    assert len(t) == 1
    return t[0]


def clean_url(url):
    return str(url).rstrip("/")


def parse_url(url):
    p = up.urlparse(url)
    return p.netloc + p.path, up.parse_qs(p.query)


def score(ref_urls, pred_url):
    refs = [clean_url(u) for u in ref_urls]
    ref_base_paths, ref_queries = [], {}
    for u in refs:
        base, query = parse_url(u)
        ref_base_paths.append(base)
        for k, v in query.items():
            ref_queries.setdefault(k, set()).update(v)
    pred_base, pred_query = parse_url(clean_url(pred_url))
    base_score = float(any(r in pred_base for r in ref_base_paths))
    query_score = 1.0
    for k, possible in ref_queries.items():
        query_score *= float(any(v in pred_query.get(k, []) for v in possible))
    return base_score, query_score, base_score * query_score


def retuple(t):
    return tuple(round(x, 6) for x in t)


# Hypothetical final URLs of the build's static probe (scratch/Task377/urlparse-probe.txt).
# Expected tuples here are (base, query, product), derived independently.
BUILD_ROWS = [
    ("exact_reference", "/search?query=restaurants%20near%20CMU%20ArtPark%20Lab", (1, 1, 1)),
    ("fragment", "/search?query=restaurants%20near%20CMU%20ArtPark%20Lab#map=17/40.44/-79.94", (1, 1, 1)),
    ("plus_space", "/search?query=restaurants+near+CMU+ArtPark+Lab", (1, 1, 1)),
    ("extra_query_key", "/search?query=restaurants+near+CMU+ArtPark+Lab&foo=1", (1, 1, 1)),
    ("capitalised", "/search?query=Restaurants%20near%20CMU%20ArtPark%20Lab", (1, 0, 0)),
    ("all_lowercase", "/search?query=restaurants%20near%20cmu%20artpark%20lab", (1, 0, 0)),
    ("typo_only", "/search?query=resturants%20near%20CMU%20ArtPark%20Lab", (1, 0, 0)),
    ("around_only", "/search?query=restaurants%20around%20CMU%20ArtPark%20Lab", (1, 0, 0)),
    ("singular", "/search?query=restaurant%20near%20CMU%20ArtPark%20Lab", (1, 0, 0)),
    ("trailing_space", "/search?query=restaurants%20near%20CMU%20ArtPark%20Lab%20", (1, 0, 0)),
    ("location_only", "/search?query=CMU%20ArtPark%20Lab", (1, 0, 0)),
    ("node_result", "/node/123", (0, 0, 0)),
    ("https_path_slash", "https://" + MAP_HOST + "/search/?query=restaurants%20near%20CMU%20ArtPark%20Lab", (1, 1, 1)),
    ("path_prefix_search", "/prefix/search?query=restaurants%20near%20CMU%20ArtPark%20Lab", (0, 1, 0)),
    ("path_searchX", "/searchX?query=restaurants%20near%20CMU%20ArtPark%20Lab", (1, 1, 1)),
    ("repeated_query", "/search?query=x&query=restaurants%20near%20CMU%20ArtPark%20Lab", (1, 1, 1)),
]

# The build's printed triples, read from urlparse-probe.txt L4-L19. On every row except L17
# the printed order is (query, base, product); L17 prints (0,0,1) where the arithmetic gives
# (query 1, base 0, product 0) = (1,0,0).
BUILD_ARTIFACT = [
    (1, 1, 1), (1, 1, 1), (1, 1, 1), (1, 1, 1),
    (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0),
    (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 0, 0),
    (1, 1, 1), (0, 0, 1), (1, 1, 1), (1, 1, 1),
]

EXTRA_ROWS = [
    ("port_3001", "http://map.invalid:3001/search?query=restaurants%20near%20CMU%20ArtPark%20Lab", (0, 1, 0)),
    ("default_port_omitted", "http://map.invalid/search?query=restaurants%20near%20CMU%20ArtPark%20Lab", (0, 1, 0)),
    ("different_host", "http://other.invalid:3000/search?query=restaurants%20near%20CMU%20ArtPark%20Lab", (0, 1, 0)),
    ("pct_encoded_letters", BASE + "/search?query=%72estaurants%20near%20CMU%20ArtPark%20Lab", (1, 1, 1)),
    ("intent_literal", BASE + "/search?query=resturants%20around%20CMU%20ArtPark%20Lab", (1, 0, 0)),
    ("missing_query", BASE + "/search", (1, 0, 0)),
    ("post_search_update_kept", BASE + "/search?query=restaurants%20near%20CMU%20ArtPark%20Lab&zoom=12#map", (1, 1, 1)),
]


def main():
    t = raw_task()
    print("task_id", t["task_id"])
    print("sites", t["sites"])
    print("intent", json.dumps(t["intent"]))
    print("intent_template_id", t["intent_template_id"])
    print("eval_types", t["eval"]["eval_types"])
    print("reference_answers", t["eval"]["reference_answers"])
    print("program_html", t["eval"]["program_html"])
    print("url_note", t["eval"]["url_note"])
    print("reference_url", t["eval"]["reference_url"])
    print("require_login", t["require_login"], "storage_state", t["storage_state"],
          "require_reset", t["require_reset"], "geolocation", t["geolocation"])
    print()

    raw_ref = t["eval"]["reference_url"]
    print("raw_unsubstituted", parse_url(clean_url(raw_ref)))
    ref = raw_ref.replace("__MAP__", BASE)
    print("substituted_reference", ref)
    print("ref_base", parse_url(clean_url(ref))[0])
    print()

    print("-- build-probe row parity: computed (base, query, product) --")
    mismatches = 0
    artifact_mismatches = 0
    for idx, (name, path, expect) in enumerate(BUILD_ROWS):
        pred = path if path.startswith("http") else BASE + path
        got = score([ref], pred)
        ok = retuple(got) == tuple(float(x) for x in expect)
        mismatches += (not ok)
        # artifact columns are (query, base, product)
        qbp = (round(got[1], 0), round(got[0], 0), round(got[2], 0))
        art = tuple(float(x) for x in BUILD_ARTIFACT[idx])
        art_ok = qbp == art
        artifact_mismatches += (not art_ok)
        print(f"{name:26} got(b,q,p)={retuple(got)} expect={expect} "
              f"artifact(q,b,p)={art} {'OK' if art_ok else 'ARTIFACT-MISMATCH'}")
    print("expected_arithmetic_mismatches", mismatches)
    print("artifact_rows_mismatching_arithmetic", artifact_mismatches)
    print()

    print("-- added controls (base, query, product) --")
    for name, pred, expect in EXTRA_ROWS:
        got = score([ref], pred)
        print(f"{name:26} got={retuple(got)} expect={expect}")
    print()

    print("-- reference-substitution controls --")
    for name, sub in [
        ("host_with_trailing_slash", BASE + "//search?query=restaurants%20near%20CMU%20ArtPark%20Lab"),
        ("raw_unsubstituted", "__MAP__/search?query=restaurants%20near%20CMU%20ArtPark%20Lab"),
        ("host_port_changed", "http://map.invalid:3001/search?query=restaurants%20near%20CMU%20ArtPark%20Lab"),
    ]:
        got = score([sub], BASE + "/search?query=restaurants%20near%20CMU%20ArtPark%20Lab")
        print(f"{name:26} ref_base={parse_url(clean_url(sub))[0]!r} got={retuple(got)}")


if __name__ == "__main__":
    main()
