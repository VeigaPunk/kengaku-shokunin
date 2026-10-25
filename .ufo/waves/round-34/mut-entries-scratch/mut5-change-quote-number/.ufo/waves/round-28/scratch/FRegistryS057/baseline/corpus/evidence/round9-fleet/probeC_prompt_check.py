# probeC_prompt_check.py — rebuild run_c()'s message lists offline (pure string ops) and diff cells.
import json
ROW1 = ("We are building a 4x4 grid over symbols A,B,C,D. Rule: each ROW must contain each symbol "
        "exactly once. I will ask for rows one at a time; reply with the row as a JSON array in a fenced json block.")
ORDER_NOTE = ("Rows are kept in emission order; a row is a violation iff it "
              "conflicts with the already-kept rows; earlier rows are never removed.")
FENCE = "```json\n{}\n```"
ASK = ("New rule, effective immediately: each COLUMN must also contain each symbol exactly once "
       "(a Latin square). Re-check the rows already emitted under the new rule. " + ORDER_NOTE +
       " Reply with {\"violations\": [row numbers needing change], \"square\": [[r1],[r2],[r3],[r4]]} "
       "\u2014 the COMPLETE corrected square, keeping every already-emitted row that does not need to change.")
NORULE = ("Emit row 4 and re-emit the complete square. Reply with "
          "{\"violations\": [], \"square\": [[r1],[r2],[r3],[r4]]} \u2014 the complete square "
          "keeping every already-emitted row unchanged.")

def msgs(rows, with_rule):
    m = [{"role": "user", "content": ROW1}]
    for i, row in enumerate(rows):
        m += [{"role": "user", "content": f"Row {i+1}?"},
              {"role": "assistant", "content": FENCE.format(json.dumps(row))}]
    return m + [{"role": "user", "content": ASK if with_rule else NORULE}]

CONFLICT = [["A","B","C","D"], ["B","C","D","A"], ["A","B","D","C"]]
BENIGN   = [["A","B","C","D"], ["B","A","D","C"], ["C","D","A","B"]]
a, b, n = msgs(BENIGN, True), msgs(CONFLICT, True), msgs(BENIGN, False)
ask_a, ask_b, ask_n = a[-1]["content"], b[-1]["content"], n[-1]["content"]
print("nmsgs", len(a), len(b), len(n))
print("final ask identical (benign vs conflict):", ask_a == ask_b, "| msg0 identical:", a[0]["content"] == b[0]["content"])
print("differing msg indices:", [i for i, (x, y) in enumerate(zip(a, b)) if x != y])
print("ORDER_NOTE in with_rule ask:", ORDER_NOTE in ask_a, "| in norule ask:", ORDER_NOTE in ask_n)
print("slot 'row numbers needing change' only in with_rule ask:", '"violations": [row numbers needing change]' in ask_a,
      "| empty-list literal only in norule ask:", '"violations": []' in ask_n)
print("re-check directive only in with_rule ask:", "Re-check the rows already emitted" in ask_a,
      "/ absent from norule ask:", "Re-check" not in ask_n)
print("ask chars: with_rule", len(ask_a), "norule", len(ask_n))