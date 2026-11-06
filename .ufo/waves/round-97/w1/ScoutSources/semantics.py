#!/usr/bin/env python3
"""Independent semantic check of the S317-S322 'teaches' claims against the fetched bytes.

Runs the grader's own test logic (a scratch copy of test_outputs.py with only the two
absolute paths repointed) over the reference query and six declared variants.
"""
import os
import re
import shutil
import subprocess
import sys

ROOT = "/fast/scratch/hyaku/kengaku-r97/ScoutSources"
HTTP = os.path.join(ROOT, "http")
WORK = os.path.join(ROOT, "semantics")
TEST_GRAPH = os.path.join(HTTP, "S318__university_graph_test.ttl")
AGENT_GRAPH = os.path.join(HTTP, "S322__university_graph.ttl")
TEST_PY = os.path.join(HTTP, "S317__test_outputs.py")

os.makedirs(WORK, exist_ok=True)

# scratch copy of the grader test with only the two absolute paths repointed
src = open(TEST_PY, encoding="utf-8").read()
patched = src.replace('Path("/app/solution.sparql")', f'Path("{WORK}/solution.sparql")')
patched = patched.replace('Path("/tests/university_graph_test.ttl")', f'Path("{TEST_GRAPH}")')
assert patched != src
open(os.path.join(WORK, "test_outputs.py"), "w", encoding="utf-8").write(patched)

REFERENCE = open(os.path.join(HTTP, "S319__solve.sh"), encoding="utf-8").read()
REFERENCE = REFERENCE.split("<< 'EOF' > /app/solution.sparql\n", 1)[1].rsplit("\nEOF", 1)[0]

# C05: drop the EU criterion (euDepartment/euUniversity/euCountry/VALUES block)
c05 = REFERENCE.replace("""             uni:worksIn ?euDepartment ;
""", "")
c05 = c05.replace("""  # Department belongs to university in Europe
  ?euDepartment uni:belongsTo ?euUniversity .
  ?euUniversity uni:locatedInCountry ?euCountry .
  VALUES ?euCountry {
  "AT" "BE" "BG" "HR" "CY" "CZ" "DK" "EE" "FI" "FR"
  "DE" "GR" "HU" "IE" "IT" "LV" "LT" "LU" "MT" "NL"
  "PL" "PT" "RO" "SK" "SI" "ES" "SE"
  }
""", "")
assert "euDepartment" not in c05 and "VALUES" not in c05

# C06: NOW() instead of the fixed reference date
c06 = REFERENCE.replace('"2025-08-16"^^xsd:date', "NOW()")
assert c06 != REFERENCE

# C09: per-department count (at least one department >10), then the professor's countries
c09 = """PREFIX uni: <http://university.org/ontology/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?professorName (GROUP_CONCAT(DISTINCT ?country; separator=", ") AS ?countries)
WHERE {
  {
    SELECT ?professorName ?department
    WHERE {
      ?professor a uni:Person ;
                 uni:hasName ?professorName ;
                 uni:role ?role ;
                 uni:worksIn ?department .
      FILTER(STRSTARTS(?role, "Professor"))
      ?class uni:isTaughtIn ?department .
      ?student uni:isEnrolledIn ?class ;
               uni:hasEnrollmentDate ?enrollDate .
      OPTIONAL { ?student uni:hasGraduationDate ?gradDate }
      FILTER( ?enrollDate <= "2025-08-16"^^xsd:date &&
              (!BOUND(?gradDate) || ?gradDate > "2025-08-16"^^xsd:date) )
    }
    GROUP BY ?professorName ?department
    HAVING(COUNT(DISTINCT ?student) > 10)
  }
  ?professor uni:hasName ?professorName ;
             uni:worksIn ?departmentForCountries .
  ?departmentForCountries uni:belongsTo ?university .
  ?university uni:locatedInCountry ?country .
}
GROUP BY ?professorName
"""

# C10: literal VALUES answer, no graph pattern
c10 = """PREFIX uni: <http://university.org/ontology/>
SELECT ?professorName ?countries
WHERE {
  VALUES (?professorName ?countries) {
    ("Giorgos Stamou" "GR, US")
    ("Chrysoula Zerva" "PT, GR")
    ("Aristotle Tympas" "GR")
    ("Alex Dimakis" "US, ES, CH")
  }
}
"""

# C11: duplicate rows (the whole reference query as a subquery, UNION itself)
_inner = REFERENCE.split("PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n", 1)[1].strip()
c11 = """PREFIX uni: <http://university.org/ontology/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?professorName ?countries
WHERE {
  { %s }
  UNION
  { %s }
}
""" % (_inner, _inner)

# C12: extra projected column
c12 = REFERENCE.replace(
    'SELECT ?professorName (GROUP_CONCAT(DISTINCT ?country; separator=", ") AS ?countries)',
    'SELECT ?professorName (GROUP_CONCAT(DISTINCT ?country; separator=", ") AS ?countries) (COUNT(DISTINCT ?student) AS ?n)')

# C17: agent-graph literal answer
c17 = """PREFIX uni: <http://university.org/ontology/>
SELECT ?professorName ?countries
WHERE {
  VALUES (?professorName ?countries) {
    ("Aristotle Tympas" "GR")
    ("Orfeas Menis" "GR")
    ("Pepe Attanasio" "IT")
  }
}
"""

VARIANTS = {
    "reference": REFERENCE,
    "C05_eu_agnostic": c05,
    "C06_now": c06,
    "C09_per_department": c09,
    "C10_literal": c10,
    "C11_duplicate_rows": c11,
    "C12_extra_column": c12,
    "C17_agent_graph_literal": c17,
}

results = {}
for name, query in VARIANTS.items():
    open(os.path.join(WORK, "solution.sparql"), "w", encoding="utf-8").write(query)
    p = subprocess.run(
        [os.path.join(ROOT, "G/bin/python"), "-m", "pytest", "-q", "--no-header",
         os.path.join(WORK, "test_outputs.py")],
        capture_output=True, text=True, cwd=WORK,
        env={"PATH": "/usr/bin:/bin", "HOME": WORK, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    tail = [l for l in p.stdout.splitlines() if l.strip()][-1] if p.stdout.strip() else ""
    results[name] = {"rc": p.returncode, "summary": tail}
    print(f"{name:26s} rc={p.returncode}  {tail}")

# graph facts behind the teaches cells
sys.path.insert(0, os.path.join(ROOT, "G/lib/python3.13/site-packages"))
from rdflib import Graph, Namespace  # noqa: E402

UNI = Namespace("http://university.org/ontology/")
g = Graph().parse(TEST_GRAPH, format="ttl")
dates = sorted(str(o) for s, p, o in g.triples((None, UNI.hasGraduationDate, None)))
print("\nTEST_GRAPH graduation dates:", len(dates), "min", dates[0] if dates else None,
      "max", dates[-1] if dates else None)
enroll = sorted(str(o) for s, p, o in g.triples((None, UNI.hasEnrollmentDate, None)))
print("TEST_GRAPH enrollment dates:", len(enroll), "min", enroll[0], "max", enroll[-1])

# professors: name, role, departments (with country), and per-department >10 student counts
q = """PREFIX uni: <http://university.org/ontology/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?name ?role (GROUP_CONCAT(DISTINCT ?country; separator=",") AS ?countries)
WHERE {
  ?p a uni:Person ; uni:hasName ?name ; uni:role ?role ; uni:worksIn ?d .
  ?d uni:belongsTo ?u . ?u uni:locatedInCountry ?country .
  FILTER(STRSTARTS(?role, "Professor"))
}
GROUP BY ?name ?role ORDER BY ?name"""
for row in g.query(q):
    print("PROF", row.name, "|", row.role, "|", row.countries)

q2 = """PREFIX uni: <http://university.org/ontology/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?name ?dept (COUNT(DISTINCT ?student) AS ?n)
WHERE {
  ?p a uni:Person ; uni:hasName ?name ; uni:role ?role ; uni:worksIn ?dept .
  FILTER(STRSTARTS(?role, "Professor"))
  ?class uni:isTaughtIn ?dept .
  ?student uni:isEnrolledIn ?class ; uni:hasEnrollmentDate ?e .
  OPTIONAL { ?student uni:hasGraduationDate ?gd }
  FILTER(?e <= "2025-08-16"^^xsd:date && (!BOUND(?gd) || ?gd > "2025-08-16"^^xsd:date))
}
GROUP BY ?name ?dept ORDER BY DESC(?n)"""
print("\nPER-DEPARTMENT counts (>10 only):")
for row in g.query(q2):
    if int(row.n) > 10:
        print("  ", row.name, row.dept, int(row.n))

import json
json.dump(results, open(os.path.join(ROOT, "semantics.json"), "w"), indent=2)
