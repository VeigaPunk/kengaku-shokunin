import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, "plans")
import round97_sparql_probe as probe
from rdflib import Graph

SC = Path("/fast/scratch/hyaku/kengaku-r97/ReviewC1")
LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
cap = LANE / probe.CAP
box = probe.Box("/usr/bin/bwrap", [])
work = SC / "gapstage"

app = probe.stage(box, {"id": "GAP", "app": "solve"}, cap, work / "GAP")
solve_q = (app / "solution.sparql").read_text()
hidden = cap / "tests" / "university_graph_test.ttl"
agent = cap / "environment" / "university_graph.ttl"


def rows(q, graph=hidden):
    g = Graph()
    g.parse(graph, format="ttl")
    res = g.query(q)
    if res.type != "SELECT":
        return ("ASK", [])
    return (res.type, sorted(tuple(str(x) for x in r) for r in res))


REF = {("Giorgos Stamou", "GR, US"), ("Chrysoula Zerva", "PT, GR"),
       ("Aristotle Tympas", "GR"), ("Alex Dimakis", "US, ES, CH")}

r_solve = rows(solve_q)
print("A solve rows:", r_solve[1])
print("A solve == REF:", set(r_solve[1]) == REF)

noeu = probe.transform(solve_q, probe.VARIANTS["no-eu-filter"][1], "no-eu-filter")
r_noeu = rows(noeu)
print("B C05 no-eu == solve rows:", r_noeu[1] == r_solve[1])
print("B EU-added:", sorted(set(r_noeu[1]) - set(r_solve[1])),
      "EU-removed:", sorted(set(r_solve[1]) - set(r_noeu[1])))

sub = ('PREFIX uni: <http://university.org/ontology/>\n'
       'PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n'
       'SELECT ?dept (COUNT(DISTINCT ?student) AS ?n) WHERE { '
       '?class uni:isTaughtIn ?dept . ?student uni:isEnrolledIn ?class ; '
       'uni:hasEnrollmentDate ?d . OPTIONAL { ?student uni:hasGraduationDate ?gd } '
       'FILTER( ?d <= "2025-08-16"^^xsd:date && (!BOUND(?gd) || ?gd > "2025-08-16"^^xsd:date) ) } '
       'GROUP BY ?dept ORDER BY DESC(?n)')
g2 = Graph()
g2.parse(hidden, format="ttl")
print("C dept distinct-student counts@ref:", [(str(d), str(n)) for d, n in g2.query(sub)])

r_per = rows(probe.PER_DEPARTMENT)
print("D C09 per-department == solve rows:", r_per[1] == r_solve[1], "n=", len(r_per[1]))

for date in ("2025-08-16", "2026-11-06", "2027-01-01", "2030-06-01", "2100-01-01"):
    q = solve_q.replace(probe.REF_DATE, '"%s"^^xsd:date' % date)
    r = rows(q)
    print("E C06 fixed-date %s == REF: %s names=%s" %
          (date, set(r[1]) == REF, sorted(n for n, _ in r[1])))

q7 = probe.transform(solve_q, probe.VARIANTS["no-graduation-filter"][1], "ng")
r7 = rows(q7)
print("F C07 no-grad names:", sorted(n for n, _ in r7[1]))
q8 = probe.transform(solve_q, probe.VARIANTS["contains-professor"][1], "cp")
r8 = rows(q8)
print("G C08 contains names:", sorted(n for n, _ in r8[1]))
ra = rows(solve_q, agent)
print("H C17 solve-on-agent-graph names:", sorted(n for n, _ in ra[1]))
rh = rows(probe.AGENT_VALUES, agent)
print("H C17 agent-literal rows:", len(rh[1]))

qdiag = (solve_q
         .replace('SELECT ?professorName (GROUP_CONCAT(DISTINCT ?country; separator=", ") AS ?countries)',
                  'SELECT ?professorName (COUNT(DISTINCT ?student) AS ?nstu) (COUNT(?student) AS ?nrows)')
         .replace("\nHAVING(COUNT(DISTINCT ?student) > 10)", ""))
g3 = Graph()
g3.parse(hidden, format="ttl")
print("I professor->(distinct students, rows) no-HAVING:",
      {(str(a), str(b), str(c)) for a, b, c in g3.query(qdiag)})

# every declared transform anchors exactly once (probe already asserts); show byte deltas
for kind, (src, edits) in sorted(probe.VARIANTS.items()):
    if src == "solve" and edits and edits != [("@@UNION-SELF@@", "", 0)]:
        t = probe.transform(solve_q, edits, kind)
        import difflib
        delta = [l for l in difflib.unified_diff(solve_q.splitlines(), t.splitlines(), lineterm="", n=0)
                 if l[:1] in "+-" and l[:3] not in ("+++", "---")]
        print("J %s delta-lines=%d" % (kind, len(delta)))
print("DONE")
