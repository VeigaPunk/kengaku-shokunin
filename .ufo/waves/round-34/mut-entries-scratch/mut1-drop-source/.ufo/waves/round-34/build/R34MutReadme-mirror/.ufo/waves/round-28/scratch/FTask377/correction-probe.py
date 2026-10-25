#!/usr/bin/env python3
"""Focused correction check for FTask377 D5 (2026-10-21).

The author's erratum (build/Task377.md:101-115) states the original heredoc printed
int(base*q), int(base), int(q) -> column order (product, base, query), not
(query, base, product). This script recomputes all 16 score rows of
scratch/Task377/urlparse-probe.txt under (product, base, query) using only stdlib
urllib.parse. No upstream import, no network.
"""
import urllib.parse as up

H = "http://map.invalid:3000"
REF = H + "/search?query=restaurants%20near%20CMU%20ArtPark%20Lab"

URLS = [
    "/search?query=restaurants%20near%20CMU%20ArtPark%20Lab",
    "/search?query=restaurants%20near%20CMU%20ArtPark%20Lab#map=17/40.44/-79.94",
    "/search?query=restaurants+near+CMU+ArtPark+Lab",
    "/search?query=restaurants+near+CMU+ArtPark+Lab&foo=1",
    "/search?query=Restaurants%20near%20CMU%20ArtPark%20Lab",
    "/search?query=restaurants%20near%20cmu%20artpark%20lab",
    "/search?query=resturants%20near%20CMU%20ArtPark%20Lab",
    "/search?query=restaurants%20around%20CMU%20ArtPark%20Lab",
    "/search?query=restaurant%20near%20CMU%20ArtPark%20Lab",
    "/search?query=restaurants%20near%20CMU%20ArtPark%20Lab%20",
    "/search?query=CMU%20ArtPark%20Lab",
    "/node/123",
    "https://map.invalid:3000/search/?query=restaurants%20near%20CMU%20ArtPark%20Lab",
    "/prefix/search?query=restaurants%20near%20CMU%20ArtPark%20Lab",
    "/searchX?query=restaurants%20near%20CMU%20ArtPark%20Lab",
    "/search?query=x&query=restaurants%20near%20CMU%20ArtPark%20Lab",
]

# Printed triples, urlparse-probe.txt L4-L19, in the artifact's actual order
# (product, base, query) per the author's erratum.
ARTIFACT_PBQ = [
    (1, 1, 1), (1, 1, 1), (1, 1, 1), (1, 1, 1),
    (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0),
    (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 0, 0),
    (1, 1, 1), (0, 0, 1), (1, 1, 1), (1, 1, 1),
]


def parse(u):
    p = up.urlparse(str(u).rstrip("/"))
    return p.netloc + p.path, up.parse_qs(p.query)


rb, rq = parse(REF)
mismatch = 0
print("label\tproduct\tbase\tquery\tartifact(product,base,query)\tstatus")
for i, rel in enumerate(URLS):
    pred = rel if rel.startswith("http") else H + rel
    pb, pq = parse(pred)
    base = float(rb in pb)
    q = 1.0
    for k, vs in rq.items():
        q *= float(any(v in pq.get(k, []) for v in vs))
    prod = base * q
    got = (int(prod), int(base), int(q))
    ok = got == tuple(ARTIFACT_PBQ[i])
    mismatch += (not ok)
    print(f"L{4+i}\t{got[0]}\t{got[1]}\t{got[2]}\t{ARTIFACT_PBQ[i]}\t{'OK' if ok else 'MISMATCH'}")
print("mismatch_count", mismatch)
