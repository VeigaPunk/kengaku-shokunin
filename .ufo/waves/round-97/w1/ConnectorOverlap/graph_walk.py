import sys
from rdflib import Graph, Namespace
from rdflib.namespace import RDF
UNI = Namespace("http://university.org/ontology/")
g = Graph(); g.parse("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round97/graders/sparql-university/tests/university_graph_test.ttl", format="ttl")
REF = "2025-08-16"
def students(dept):
    q = """PREFIX uni: <http://university.org/ontology/>
    SELECT (COUNT(DISTINCT ?s) AS ?n) WHERE {
      ?c uni:isTaughtIn ?d . ?s uni:isEnrolledIn ?c ; uni:hasEnrollmentDate ?e .
      OPTIONAL { ?s uni:hasGraduationDate ?gd }
      FILTER(?e <= "%s"^^<http://www.w3.org/2001/XMLSchema#date> && (!BOUND(?gd) || ?gd > "%s"^^<http://www.w3.org/2001/XMLSchema#date>))
    }""" % (REF, REF)
    r = list(g.query(q.replace("?d", "<%s>" % dept)))
    return int(r[0][0])
rows = []
for p in g.subjects(RDF.type, UNI.Person):
    roles = list(g.objects(p, UNI.role))
    if not roles or not str(roles[0]).startswith("Professor"): continue
    name = str(list(g.objects(p, UNI.hasName))[0])
    depts = list(g.objects(p, UNI.worksIn))
    info = []
    for d in depts:
        u = list(g.objects(d, UNI.belongsTo))[0]
        c = str(list(g.objects(u, UNI.locatedInCountry))[0])
        info.append((str(d).rsplit("/",1)[-1], c, students(d)))
    rows.append((name, info))
EU = {"AT","BE","BG","HR","CY","CZ","DK","EE","FI","FR","DE","GR","HU","IE","IT","LV","LT","LU","MT","NL","PL","PT","RO","SK","SI","ES","SE"}
print("professor | departments(name,country,students) | has_eu | max_dept | aggregate | pass_perdept | pass_aggregate | pass_perdept_noEU")
for name, info in sorted(rows):
    has_eu = any(c in EU for _, c, _ in info)
    mx = max([n for _, _, n in info] or [0])
    agg = sum(n for _, _, n in info)
    print(f"{name} | {info} | {has_eu} | {mx} | {agg} | {mx>10} | {agg>10} | {mx>10}")
