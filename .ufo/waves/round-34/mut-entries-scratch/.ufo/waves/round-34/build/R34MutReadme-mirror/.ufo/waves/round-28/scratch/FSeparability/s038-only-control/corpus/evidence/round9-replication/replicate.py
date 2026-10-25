#!/usr/bin/env python3
"""Planning-horizon probe v2 — post-critic fixes applied.
vs 127.0.0.1:34113, bare chat/completions, temp 0.2, no tools.
Fixes: checkpoint-INC (no self-copy scaffold), seeds>reps, pinned minimal system
prompt, single-digit deltas, 2x2 hint x clean for B, corrupted key always exercised,
historical-value corruption, 3-way outcome coding, C ordering rule pinned,
C-norule baseline cell, last-fence parser, max_tokens 8192.
"""
import json, urllib.request, random, time, re, os, itertools

BASE = "http://127.0.0.1:34113/v1/chat/completions"
OUT = "/tmp/bench-r8"
TEMP = 0.2
MAXTOK = 8192
os.makedirs(OUT, exist_ok=True)
LOGF = open(f"{OUT}/results.jsonl", "a")

SYSTEM = ("You are an evaluation target. Reply with exactly one fenced "
          "```json code block and no other text — unless the user asks you to reply 'ok'.")

def call(messages):
    body = {"model": "local", "messages": [{"role":"system","content":SYSTEM}] + messages,
            "temperature": TEMP, "max_tokens": MAXTOK}
    req = urllib.request.Request(BASE, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=300) as r:
        resp = json.load(r)
    dt = time.time() - t0
    ch = resp["choices"][0]
    return {"content": ch["message"]["content"],
            "finish_reason": ch.get("finish_reason"),
            "usage": resp.get("usage", {}), "wall_s": round(dt, 2)}

def log(rec):
    LOGF.write(json.dumps(rec) + "\n"); LOGF.flush()

def extract_json_block(text):
    blocks = re.findall(r"```(?:json)?\s*\n(.*?)```", text, re.S)
    if blocks:
        try: return json.loads(blocks[-1])
        except Exception: pass
    m = re.findall(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]", text, re.S)
    for cand in reversed(m):
        try: return json.loads(cand)
        except Exception: continue
    return None

# ---------- problem generation ----------
KEYS = ["nails", "bolts", "screws", "washers", "hinges"]

def sim_apply(state, op):
    s = dict(state); kind = op[0]
    if kind == "SET": s[op[1]] = op[2]
    elif kind == "ADD": s[op[1]] += op[2]
    elif kind == "SUB": s[op[1]] -= op[2]
    elif kind == "MOV": s[op[2]] += s[op[1]]; s[op[1]] = 0
    elif kind == "DEL": del s[op[1]]
    elif kind == "NEW": s[op[1]] = op[2]
    return s

def op_str(op):
    if op[0] in ("SET", "ADD", "SUB", "NEW"): return f"{op[0]} {op[1]} {op[2]}"
    if op[0] == "MOV": return f"MOV {op[1]} {op[2]}"
    return f"DEL {op[1]}"

def tail_touched(ops, mid=7):
    t = {o[1] for o in ops[mid:]}
    t |= {o[2] for o in ops[mid:] if o[0] == "MOV"}
    return t

def gen_problem(seed, _depth=0):
    rng = random.Random(seed)
    init = {k: rng.randint(3, 30) for k in KEYS}
    extra = ["brackets", "rivets", "gaskets"]
    state, ops = dict(init), []
    while len(ops) < 10:
        live = list(state); roll = rng.random()
        if roll < 0.18:
            op = ("SET", rng.choice(live), rng.randint(0, 30))
        elif roll < 0.45:
            op = ("ADD", rng.choice(live), rng.randint(1, 9))
        elif roll < 0.65:
            c = [k for k in live if state[k] > 0]
            if not c: continue
            k = rng.choice(c); op = ("SUB", k, rng.randint(1, min(9, state[k])))
        elif roll < 0.80:
            if len(live) < 2: continue
            a, b = rng.sample(live, 2)
            if state[a] == 0: continue
            op = ("MOV", a, b)
        elif roll < 0.90:
            if len(live) < 4: continue
            op = ("DEL", rng.choice(live))
        else:
            if not extra: continue
            op = ("NEW", extra.pop(0), rng.randint(2, 9))
        if op[0] in ("SET", "ADD", "SUB", "DEL") and op[1] not in state: continue
        if op[0] == "NEW" and op[1] in state: continue
        state = sim_apply(state, op); ops.append(op)
    kinds = {o[0] for o in ops}
    if "DEL" not in kinds or "MOV" not in kinds or len(tail_touched(ops)) < 2:
        return gen_problem(seed + 977, _depth + 1)
    return init, ops

def states_along(init, ops, n=None):
    s, out = dict(init), []
    for op in (ops if n is None else ops[:n]):
        s = sim_apply(s, op); out.append(s)
    return out

RULES = """Inventory ledger. State = JSON object mapping part names to integer counts.
Operations (operands always name existing keys):
- SET k v : set k to v          - ADD k v : add v to k
- SUB k v : subtract v from k   - MOV a b : b += a, a stays present at 0
- DEL k   : remove key k        - NEW k v : add new key k with count v
Output the state exactly: all keys currently present (including zeros), integer values, any order."""

def grade_state(got, want):
    """returns (exact, n_wrong_keys)"""
    if not isinstance(got, dict): return False, len(want)
    wrong = sum(1 for k in set(got) | set(want) if got.get(k) != want.get(k))
    return got == want, wrong

# ---------- probe A ----------
def run_inc(pid, init, ops, proto):
    """proto: 'INC' = full state every turn; 'CKPT' = acks except checkpoints 4,7,10"""
    ckpts = {4, 7, 10}
    msgs = [{"role": "user", "content":
             RULES + f"\nInitial state: {json.dumps(init)}\nNext operation: {op_str(ops[0])}\nOutput the FULL state after applying it."}]
    truth = states_along(init, ops)
    onset, ckpt_oks, key_errs = None, [], []
    for i, op in enumerate(ops):
        r = call(msgs)
        msgs.append({"role": "assistant", "content": r["content"]})
        turn_no = i + 1
        graded = (proto == "INC") or (turn_no in ckpts)
        if graded:
            got = extract_json_block(r["content"])
            exact, nwrong = grade_state(got, truth[i])
            if not exact and onset is None: onset = turn_no
            ckpt_oks.append(exact); key_errs.append(nwrong)
            log({"cell": f"A-{proto}", "pid": pid, "turn": turn_no, "ok": exact,
                 "nwrong": nwrong, "got": got, "want": truth[i],
                 "finish": r["finish_reason"], "usage": r["usage"],
                 "wall_s": r["wall_s"], "raw": r["content"]})
        else:
            log({"cell": f"A-{proto}-ack", "pid": pid, "turn": turn_no,
                 "raw": r["content"][:80], "finish": r["finish_reason"],
                 "usage": r["usage"], "wall_s": r["wall_s"]})
        if i + 1 < len(ops):
            if proto == "CKPT" and (i + 2) not in ckpts:
                ask = "Reply 'ok'."
            elif proto == "CKPT":
                ask = "CHECKPOINT — output the FULL state now."
            else:
                ask = "Output the FULL state after applying it."
            msgs.append({"role": "user", "content":
                         f"Next operation: {op_str(ops[i+1])}\n{ask}"})
    final_exact = ckpt_oks[-1] if ckpt_oks else None
    return {"final_ok": final_exact, "onset": onset,
            "ckpt_acc": sum(ckpt_oks) / len(ckpt_oks), "key_errs": key_errs}

def run_mono(pid, init, ops):
    oplist = "\n".join(f"{i+1}. {op_str(o)}" for i, o in enumerate(ops))
    msgs = [{"role": "user", "content":
             RULES + f"\nInitial state: {json.dumps(init)}\nApply these operations in order:\n{oplist}\nOutput the FINAL state only."}]
    r = call(msgs)
    want = states_along(init, ops)[-1]
    got = extract_json_block(r["content"])
    exact, nwrong = grade_state(got, want)
    log({"cell": "A-MONO", "pid": pid, "turn": 1, "ok": exact, "nwrong": nwrong,
         "got": got, "want": want, "finish": r["finish_reason"],
         "usage": r["usage"], "wall_s": r["wall_s"], "raw": r["content"]})
    return {"final_ok": exact}

# ---------- probe B ----------
def run_b(pid, init, ops, corrupt_mode, cond):
    """corrupt_mode: 'corrupt'|'clean'; cond: 'plain'|'hint'"""
    mid = 7
    correct = states_along(init, ops, mid)
    state_mid = dict(correct[-1])
    corrupt_field, corrupt_val = None, None
    if corrupt_mode == "corrupt":
        cand = [k for k in tail_touched(ops, mid) if k in state_mid]
        rng = random.Random(pid * 31)
        k = rng.choice(cand) if cand else rng.choice(list(state_mid))
        # corruption = an earlier historical value of that key (plausible drift)
        for j in range(mid - 2, -1, -1):
            hv = correct[j].get(k)
            if hv is not None and hv != state_mid[k]:
                corrupt_val = hv; break
        if corrupt_val is None:
            corrupt_val = state_mid[k] + 5
        state_mid[k] = corrupt_val
        corrupt_field = k
    oplist_first = "\n".join(f"{i+1}. {op_str(o)}" for i, o in enumerate(ops[:mid]))
    oplist_rest = "\n".join(f"{i+mid+1}. {op_str(o)}" for i, o in enumerate(ops[mid:]))
    msgs = [{"role": "user", "content":
             RULES + f"\nInitial state: {json.dumps(init)}\nApply operations 1-{mid} in order; after EACH, output the full state.\n{oplist_first}"}]
    body = [f"After operation {i+1}:\n```json\n{json.dumps(s)}\n```"
            for i, s in enumerate(correct[:-1])]
    body.append(f"After operation {mid}:\n```json\n{json.dumps(state_mid)}\n```")
    msgs.append({"role": "assistant", "content": "\n".join(body)})
    tail = (f"Now apply operations {mid+1}-{len(ops)} in order and output the FINAL state.\n{oplist_rest}")
    if cond == "hint":
        tail += ("\nNote: if the previous state is inconsistent with the operations "
                 "already applied, correct it rather than propagating the error.")
    msgs.append({"role": "user", "content": tail})
    r = call(msgs)
    want = states_along(init, ops)[-1]
    got = extract_json_block(r["content"])
    # 3-way: corrected (=sim from true mid) / propagated (=sim from corrupt mid) / other
    sim_corrupt = states_along(state_mid, ops[mid:])[-1] if corrupt_mode == "corrupt" else None
    exact = got == want
    outcome = "corrected" if exact else ("propagated" if got == sim_corrupt else "other")
    healed = corrupt_mode == "clean" or (isinstance(got, dict) and got.get(corrupt_field) == want.get(corrupt_field))
    log({"cell": f"B-{corrupt_mode}-{cond}", "pid": pid, "turn": 1, "ok": exact,
         "outcome": outcome, "corrupt_field": corrupt_field,
         "corrupt_from": corrupt_val, "healed": healed,
         "got": got, "want": want, "finish": r["finish_reason"],
         "usage": r["usage"], "wall_s": r["wall_s"], "raw": r["content"]})
    return {"ok": exact, "outcome": outcome}

# ---------- probe C ----------
CONFLICT_ROWS = [["A","B","C","D"], ["B","C","D","A"], ["A","B","D","C"]]   # unique minimal removal {3}
BENIGN_ROWS   = [["A","B","C","D"], ["B","A","D","C"], ["C","D","A","B"]]   # consistent; r4 forced [D,C,B,A]

def col_conflict_free(rows):
    return all(len(set(r[c] for r in rows)) == len(rows) for c in range(4))

def valid_latin(sq):
    if not isinstance(sq, list) or len(sq) != 4: return False
    sym = {"A","B","C","D"}
    if not all(isinstance(r, list) and len(r) == 4 and set(r) == sym for r in sq): return False
    return all(set(sq[r][c] for r in range(4)) == sym for c in range(4))

def rows_perm_only(sq):
    sym = {"A","B","C","D"}
    return isinstance(sq, list) and len(sq) == 4 and \
        all(isinstance(r, list) and set(r) == sym for r in sq)

ORDER_NOTE = ("Rows are kept in emission order; a row is a violation iff it "
              "conflicts with the already-kept rows; earlier rows are never removed.")

def run_c(name, rows, with_rule, rep):
    msgs = [{"role": "user", "content":
             "We are building a 4x4 grid over symbols A,B,C,D. Rule: each ROW must contain each symbol exactly once. I will ask for rows one at a time; reply with the row as a JSON array in a fenced json block."}]
    for i, row in enumerate(rows):
        msgs.append({"role": "user", "content": f"Row {i+1}?"})
        msgs.append({"role": "assistant", "content": f"```json\n{json.dumps(row)}\n```"})
    if with_rule:
        ask = ("New rule, effective immediately: each COLUMN must also contain each symbol exactly once "
               "(a Latin square). Re-check the rows already emitted under the new rule. " + ORDER_NOTE +
               " Reply with {\"violations\": [row numbers needing change], \"square\": [[r1],[r2],[r3],[r4]]} "
               "— the COMPLETE corrected square, keeping every already-emitted row that does not need to change.")
    else:
        ask = ("Emit row 4 and re-emit the complete square. Reply with "
               "{\"violations\": [], \"square\": [[r1],[r2],[r3],[r4]]} — the complete square "
               "keeping every already-emitted row unchanged.")
    msgs.append({"role": "user", "content": ask})
    r = call(msgs)
    got = extract_json_block(r["content"])
    grade = grade_c(got, rows, with_rule)
    log({"cell": f"C-{name}", "rep": rep, "turn": 1, **grade, "got": got,
         "finish": r["finish_reason"], "usage": r["usage"],
         "wall_s": r["wall_s"], "raw": r["content"]})
    return grade

def grade_c(got, prior_rows, with_rule):
    out = {"ok": False, "viol_ok": False, "square_valid": False,
           "preserved": False, "over_repair": False, "parse": got is not None}
    if not isinstance(got, dict): return out
    viol, sq = got.get("violations"), got.get("square")
    if not isinstance(viol, list) or not isinstance(sq, list): return out
    out["square_valid"] = valid_latin(sq) if with_rule else rows_perm_only(sq)
    changed = set(viol)
    kept_ok = all(sq[i] == prior_rows[i] for i in range(3) if (i + 1) not in changed)
    out["preserved"] = kept_ok
    remaining = [prior_rows[i] for i in range(3) if (i + 1) not in changed]
    feasible = col_conflict_free(remaining) if with_rule else True
    out["viol_ok"] = feasible and kept_ok
    if with_rule and out["viol_ok"]:
        minimal_sz = next((sz for sz in range(4)
                           if any(col_conflict_free([prior_rows[i] for i in range(3) if i not in c])
                                  for c in itertools.combinations(range(3), sz))), None)
        out["over_repair"] = minimal_sz is not None and len(changed) > minimal_sz
    out["ok"] = out["square_valid"] and out["viol_ok"] and out["preserved"]
    return out

def run_c_mono(rep):
    msgs = [{"role": "user", "content":
        "Emit a complete 4x4 Latin square over symbols A,B,C,D (each row and each column a permutation), as a fenced json list of 4 rows."}]
    r = call(msgs)
    got = extract_json_block(r["content"])
    ok = valid_latin(got)
    log({"cell": "C-MONO", "rep": rep, "turn": 1, "ok": ok, "square_valid": ok,
         "got": got, "finish": r["finish_reason"], "usage": r["usage"],
         "wall_s": r["wall_s"], "raw": r["content"]})
    return {"ok": ok}

# ---------- schedule: interleave cells to decorrelate burst state ----------
def main():
    NSEEDS_A, NSEEDS_B, NREP_C = 10, 8, 4
    probs = {pid: gen_problem(700 + pid * 13) for pid in range(1, NSEEDS_A + 1)}
    for pid, (init, ops) in probs.items():
        log({"cell": "meta", "pid": pid, "init": init,
             "ops": [list(o) for o in ops], "truth": states_along(init, ops),
             "tail_touched": sorted(tail_touched(ops))})
    summ = {}
    def add(k, v): summ.setdefault(k, []).append(v)
    plan = []
    for pid in probs:                      # interleaved across cells per seed
        plan += [("A-INC", pid), ("A-MONO", pid), ("A-CKPT", pid)]
    for pid in range(1, NSEEDS_B + 1):
        for m, c in [("corrupt","plain"),("corrupt","hint"),
                     ("clean","plain"),("clean","hint")]:
            plan.append(("B", pid, m, c))
    for rep in range(NREP_C):
        plan += [("C-conflict", rep), ("C-benign", rep),
                 ("C-norule", rep), ("C-MONO", rep)]
    for i, job in enumerate(plan):
        try:
            if job[0] == "A-INC":
                res = run_inc(job[1], *probs[job[1]], "INC"); add("A-INC", res["final_ok"])
            elif job[0] == "A-CKPT":
                res = run_inc(job[1], *probs[job[1]], "CKPT"); add("A-CKPT", res["final_ok"])
            elif job[0] == "A-MONO":
                res = run_mono(job[1], *probs[job[1]]); add("A-MONO", res["final_ok"])
            elif job[0] == "B":
                res = run_b(job[1], *probs[job[1]], job[2], job[3])
                add(f"B-{job[2]}-{job[3]}", res["ok"])
            elif job[0] == "C-conflict":
                add("C-conflict", run_c("conflict", CONFLICT_ROWS, True, job[1])["ok"])
            elif job[0] == "C-benign":
                add("C-benign", run_c("benign", BENIGN_ROWS, True, job[1])["ok"])
            elif job[0] == "C-norule":
                add("C-norule", run_c("norule", BENIGN_ROWS, False, job[1])["ok"])
            elif job[0] == "C-MONO":
                add("C-MONO", run_c_mono(job[1])["ok"])
        except Exception as e:
            log({"cell": "error", "job": job, "err": repr(e)})
        print(f"[{i+1}/{len(plan)}] {job}", flush=True)
    print("\n=== SUMMARY ===")
    for k, v in summ.items():
        ok = sum(1 for x in v if x); print(f"{k}: {ok}/{len(v)}")

if __name__ == "__main__":
    main()
