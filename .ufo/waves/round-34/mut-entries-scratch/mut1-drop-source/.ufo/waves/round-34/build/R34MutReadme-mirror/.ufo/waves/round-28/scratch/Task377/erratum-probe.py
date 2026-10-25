# Labelled stdlib-only re-run of the original urlparse-probe.txt print order (product, base, query).
# Reimplements evaluators.py L187-236 arithmetic with urllib.parse; no upstream import, no network.
import urllib.parse as up

H = "http://map.invalid:3000"
REF = H + "/search?query=restaurants%20near%20CMU%20ArtPark%20Lab"


def pu(u):
    p = up.urlparse(u.rstrip("/"))
    return p.netloc + p.path, up.parse_qs(p.query)


rb, rq = pu(REF)
CANDS = [
    ("orig:17 prefix path", H + "/prefix/search?query=restaurants%20near%20CMU%20ArtPark%20Lab"),
    ("orig:4 exact ref", REF),
    ("orig:8 capitalised", H + "/search?query=Restaurants%20near%20CMU%20ArtPark%20Lab"),
    ("D1 https scheme", REF.replace("http://", "https://")),
    ("D1 port 3001", REF.replace(":3000", ":3001")),
    ("D1 port omitted", REF.replace(":3000", "")),
    ("D2 extra key + fragment", REF + "&zoom=12#map=17/40.44/-79.94"),
    ("D2 result page", H + "/node/123"),
]
print("label\tproduct\tbase\tquery\turl")
for label, c in CANDS:
    pb, pq = pu(c)
    base = float(rb in pb)
    q = 1.0
    for k, vs in rq.items():
        q *= float(any(v in pq.get(k, []) for v in vs))
    print(f"{label}\t{int(base * q)}\t{int(base)}\t{int(q)}\t{c}")
