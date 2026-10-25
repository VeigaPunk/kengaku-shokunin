# ExecGraderAdapters — r26 build, read-only probe (KengakuR26-2.ExecGraderAdapters-4)
Base: `git archive e0037a8da268 | tar -x -C /tmp/kengaku-r26-ExecGraderAdapters-probe/base` (grader.py sha256 90c87c8865022681b1249a42ea580726932d2e97ec0de43e0c89efe0e5ae941f). The four result files have no diff between f11bffbf and e0037a8 (`git diff --stat` output is empty) and match the live tree byte for byte. The probe output has sha256 0b082b654640316e568e518269b9a74ca58c79eec8d0b1e347f4cdd8a1236ab7 whether ROOT is the snapshot or the live tree.
1. **Baseline reproduces on every record.** All 1964 records carrying `raw`+`ok` (r8 188, r9 128, r11 320, r12 1328) re-grade to their stored `ok` under grader.py's own routing: 0 non-reproducing, 1021 stored PASS. Every other stored verdict field also re-derives: `got` 1964/1964 (extracted object == stored `got`), `want` 1948/1948, `nwrong` 1916/1916, grade_c fields 12/12, `square_valid` 16/16. The meta builders ran 54 checks with 0 mismatches.
2. **Who grades what.** grade_state: every A-* cell, 1676 records (r8/r9 :387, r11 :1027, r12 family 1 :2489). The 32 r8 B-* records also count as grade_state: grader.py computes their ok as `got == want` (:468), which equals grade_state's ok on 32/32, and in general because want is always a dict (grade_state returns `got == want` for dicts, False otherwise). grade_seq: r12 T-DENSE/T-SPARSE, 240 (:2489). grade_c: r8 C-conflict/C-benign/C-norule, 12 (:492). **r8 C-MONO (4) is graded by valid_latin (:500-501; summary :533-535), not grade_c**, so the Rec enum {state,seq,c} has no exact slot for it.
3. **Mis-routes hide as exclusions** (TRAP line). B-* with want=truth[turn-1] reproduce 14/32; A-MONO with truth[turn-1], 80/82; T-* through grade_state, 223/240; C-MONO through grade_c, 0/4. Each mis-route flips exactly the stored PASSes (18, 2 and 17), or all 4 for C-MONO. The pre-registration excludes non-reproducing records, so every one of these mis-routes would still exit 0, only with `excluded>0`. Recommendation: grader_perturb.py should pin `population=1964 excluded=0` and exit 1 otherwise.
4. **Coordination (peer messages only).** ExecPerturbCore replied that it labels C-MONO grader='c' and dispatches valid_latin by cell. ExecPopulationManifest's TSV matches (c/include) and flags the choice as an L1 decision: c+valid_latin, a `latin` id, or exclusion. I did not message ExecPerturbOracle, to keep it independent. L1 should confirm one convention so all three seats count C-MONO the same way.
5. **Rec gaps.** C-* records have no `pid` (they carry `rep` 0-3) and no `want` (their inputs are c_specs). B-* records have no `nwrong`. A-MONO, B-* and C-* all store turn=1, although A-MONO and B-* grade against truth[-1]. 212 graded records have turn=1 (A-INC 82, A-MONO 82, B 32, C 16; from a turn census of the same files in this session), so D1's "previous turn's truth" needs an explicit rule for them. That rule belongs to ExecFamilyEdges' item.
- r8 A-INC/A-CKPT/A-MONO and all r9 A-*: truth = build_meta :355 `states_along(meta.init, meta.ops)`, cross-checked against gen_problem (seed 700+13·pid :414, 2000+29·pid :585) at :350-354 and against the stored meta truth at :356. want = truth[turn-1], or truth[-1] for A-MONO (:385). Graded by grade_state :387 in replay_a_records :367.
- r8 B-* (turn 1): same truth (meta via recs_meta_lookup :431). want = truth[-1] (:435); ok = `got == want` (:468); no nwrong. Summary recompute at :520-527.
- r11 A-CKPT4710/A-CKPT710: truth from _build_meta :994 (seed 3000+41·pid :837-838, called at :1421). want = truth[turn-1] (:1025). Graded by grade_state :1027 in _replay_graded :1006.
- r12 A-* (family 1): truth from _check_meta_f1 :2301 (seed 3000+41·pid :1551-1552; r11 meta identity at :2337-2348). want = _want_for :2269-2275 (A-MONO → tr[-1]). Graded by grade_state :2489 in _check_replay :2463.
- r12 T-DENSE/T-SPARSE (family 2): truth = seq_states_along(meta2.init, meta2.ops) at :2399 (:2107). _check_meta_f2 returns {} unless probe_r12.py's gen_seq_problem loads (:2369-2374). want = _want_for tr[turn-1]. Graded by grade_seq :2115-2121 via :2489.
- r8 C-cells (grade_c inputs, c_specs :483-484): C-conflict = (CONFLICT_ROWS :116 = ABCD/BCDA/ABDC, with_rule=True); C-benign = (BENIGN_ROWS :117 = ABCD/BADC/CDAB, with_rule=True); C-norule = (BENIGN_ROWS, with_rule=False). No want. Replay at :487-497, summary at :528-532. C-MONO uses valid_latin(got) at :498-504 and :533-535, with no prior_rows.
### Script `/tmp/kengaku-r26-ExecGraderAdapters-probe/regrade_probe.py` (27 lines, sha256 dd8b4a3892e40ef7031f8e1d555e63f629e546da60fcf1e0fcea0595079bffda); `python3 <script>` exits 0
```python
import collections as co, hashlib, json, os, sys; sys.dont_write_bytecode = True; ROOT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/kengaku-r26-ExecGraderAdapters-probe/base"; sys.path.insert(0, ROOT); import grader as g  # noqa: E401,E402,E702 (main() is __name__-guarded)
F = {"r8": "corpus/evidence/round8-horizon/results.jsonl", "r9": "corpus/evidence/round9-replication/results-r9.jsonl", "r11": "corpus/evidence/round11-power/results-r11.jsonl", "r12": "corpus/evidence/round12-ladder/results-r12.jsonl"}
B = {k: open(os.path.join(ROOT, v), "rb").read() for k, v in F.items()}; L = {k: [(i, json.loads(s)) for i, s in enumerate(b.decode("utf-8").splitlines(), 1) if s.strip()] for k, b in B.items()}; R, rep = {k: [r for _, r in v] for k, v in L.items()}, g.Report()
T = {"r8": g.build_meta(R["r8"], rep, "r8", range(1, 11), lambda p: 700 + p * 13), "r9": g.build_meta(R["r9"], rep, "r9", range(101, 109), lambda p: 2000 + p * 29), "r11": g._build_meta(R["r11"], rep, g.R11_PIDS, g.r11_seed),  # :414,:585 -> :355; :1421 -> :994
     "r12a": g._check_meta_f1(R["r12"], rep, g.R12_PIDS_1, g.R11_JSONL), "r12t": g._check_meta_f2(R["r12"], rep, g.R12_PIDS_2, g.R12_MACHINERY)}  # :4062 -> :2301; :4063 -> :2399 (returns {} unless probe_r12.py loads, :2369-2374)
CS = {"C-conflict": (g.CONFLICT_ROWS, True), "C-benign": (g.BENIGN_ROWS, True), "C-norule": (g.BENIGN_ROWS, False)}  # c_specs :483-484, rows :116-117
print("PIN", " ".join(f"{k}={hashlib.sha256(b).hexdigest()}" for k, b in B.items()), f"\nMETA checks={rep.checks} mismatches={len(rep.mismatches)}\nCSPEC", {c: f"with_rule={w} prior_rows={'/'.join(map(''.join, rows))}" for c, (rows, w) in CS.items()})
route = lambda t, c: "seq" if t == "r12" and c in g.F2_ARMS else "c" if c in CS else "latin" if c == "C-MONO" else "state"  # noqa: E731  :2489 | :492 | :501 | :387,:468,:1027,:2489
def want(t, r, last=True):  # last=False: the naive truth[turn-1] rule for B-*/A-MONO (trap counterfactual only)
    c, p, n = r["cell"], r["pid"], r["turn"]; tr = T[("r12t" if c in g.F2_ARMS else "r12a") if t == "r12" else t][p]
    if t == "r12" and last: return g._want_for(c, p, n, T["r12t" if c in g.F2_ARMS else "r12a"])  # :2269-2275 (MONO -> tr[-1], else tr[turn-1])
    return tr[-1] if last and (c.startswith("B-") or c == "A-MONO") else tr[n - 1]  # B :435; A-MONO :385; A-* :385 / r11 :1025
tal, fld, trap, bad = co.defaultdict(co.Counter), co.Counter(), co.defaultdict(list), []; S = lambda suf: sum(v for tc in tal.values() for x, v in tc.items() if x.endswith(suf))  # noqa: E731
for t, line, r in ((t, i, r) for t, rows in L.items() for i, r in rows if "ok" in r and "raw" in r):
    c, got = r["cell"], g.extract_json_block(r["raw"]); k = route(t, c); cmp = {"got": (got, r["got"])}  # extractor :121-134
    if k in ("state", "seq"):
        w = want(t, r); ok, nw = (g.grade_state if k == "state" else g.grade_seq)(got, w); cmp.update({"want": (w, r["want"])}, **({"nwrong": (nw, r["nwrong"])} if "nwrong" in r else {}))
        if c.startswith("B-"): cmp["B:grade_state.ok==(got==want)"] = (ok, got == w); ok = got == w; trap["B-* want=truth[turn-1]"].append(g.grade_state(got, want(t, r, False))[0] == r["ok"])  # :468
        if c == "A-MONO": trap["A-MONO want=truth[turn-1]"].append(g.grade_state(got, want(t, r, False))[0] == r["ok"])
        if k == "seq": trap["T-* via grade_state"].append(g.grade_state(got, w)[0] == r["ok"])
    elif k == "c": o = g.grade_c(got, *CS[c]); ok = o.pop("ok"); cmp.update({f: (v, r[f]) for f, v in o.items()})  # :492-497
    else: ok = g.valid_latin(got); cmp["square_valid"] = (ok, r["square_valid"]); trap["C-MONO via grade_c"].append(g.grade_c(got, g.BENIGN_ROWS, True)["ok"] == r["ok"])  # :500-504; prior_rows moot: non-dict got returns at :250-251
    tc = tal[(t, k)]; tc[c + ":n"] += 1; tc[c + ":rep"] += ok == r["ok"]; tc[c + ":P"] += r["ok"] is True
    for f, (a, b) in cmp.items(): fld[f + ":n"] += 1; fld[f + ":rep"] += a == b  # noqa: E701,E702
    if ok != r["ok"] or type(r["ok"]) is not bool or any(a != b for a, b in cmp.values()): bad.append((F[t], line, c, r.get("pid", r.get("rep")), r["turn"]))  # noqa: E701
for (t, k), tc in tal.items(): print(f"REGRADE {t}/{k}: " + " · ".join(f"{c} {tc[c + ':rep']}/{tc[c + ':n']} P{tc[c + ':P']}" for c in dict.fromkeys(x.rsplit(":", 1)[0] for x in tc)))  # noqa: E701
print("FIELDS", ", ".join(f"{f[:-2]} {fld[f[:-2] + ':rep']}/{fld[f]}" for f in fld if f.endswith(":n")), f"\nTOTAL records={S(':n')} ok_reproduced={S(':rep')} stored_PASS={S(':P')} non_reproducing={len(bad)} {bad[:5]}\nTRAP (mis-route -> ok reproduced)", "; ".join(f"{k} {sum(v)}/{len(v)}" for k, v in sorted(trap.items())))
```
```text
PIN r8=bd986e5e8c9b415aa2b0073fa8fed784282c9dbeb19055d34475e662792e2204 r9=c20158bdef148b322501341e539b2383d84de4179618fd46b801379c11affbcb r11=918bf7aa3030baa954c16a20830f078738147ce7cc002768e5ab922ad38f51ad r12=ad9c88e79068fa2833c90f071ec6da4035ff37371ff95d84f581dd4e8db842f1 
META checks=54 mismatches=0
CSPEC {'C-conflict': 'with_rule=True prior_rows=ABCD/BCDA/ABDC', 'C-benign': 'with_rule=True prior_rows=ABCD/BADC/CDAB', 'C-norule': 'with_rule=False prior_rows=ABCD/BADC/CDAB'}
REGRADE r8/state: A-INC 100/100 P81 · A-MONO 10/10 P0 · A-CKPT 30/30 P13 · B-corrupt-plain 8/8 P3 · B-corrupt-hint 8/8 P3 · B-clean-plain 8/8 P6 · B-clean-hint 8/8 P6
REGRADE r8/c: C-conflict 4/4 P4 · C-benign 4/4 P1 · C-norule 4/4 P4
REGRADE r8/latin: C-MONO 4/4 P4
REGRADE r9/state: A-INC 80/80 P60 · A-MONO 8/8 P0 · A-CKPT4710 24/24 P10 · A-CKPT710 16/16 P5
REGRADE r11/state: A-CKPT710 128/128 P41 · A-CKPT4710 192/192 P95
REGRADE r12/state: A-INC 640/640 P522 · A-CKPT4710 192/192 P94 · A-CKPT710 128/128 P40 · A-CKPT10 64/64 P10 · A-MONO 64/64 P2
REGRADE r12/seq: T-SPARSE 96/96 P7 · T-DENSE 144/144 P10
FIELDS got 1964/1964, want 1948/1948, nwrong 1916/1916, B:grade_state.ok==(got==want) 32/32, viol_ok 12/12, square_valid 16/16, preserved 12/12, over_repair 12/12, parse 12/12 
TOTAL records=1964 ok_reproduced=1964 stored_PASS=1021 non_reproducing=0 []
TRAP (mis-route -> ok reproduced) A-MONO want=truth[turn-1] 80/82; B-* want=truth[turn-1] 14/32; C-MONO via grade_c 0/4; T-* via grade_state 223/240
```
VERDICT: All 1964 raw+ok records reproduce their stored ok (0 excluded) under grader.py's routing: state 1708, seq 240, grade_c 12, valid_latin 4. Open items: C-MONO needs one agreed 'c'+valid_latin convention, and mis-routes stay silent unless the instrument pins excluded=0.
Installs: none (stdlib python3 only). Files written: this report only; scratch is in /tmp/kengaku-r26-ExecGraderAdapters-probe/.
