# Independent re-implementation (ExecC1) - does NOT import the probe BUILDER.
# Reads only: committed documents/, solution placement.tsv + summary.csv + invoices-json/
# Args: case-id  app-root  docs-dir  solution-dir
import csv, io, os, shutil, sys, json
case, app, docs, sol = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
os.makedirs(os.path.join(app, "invoices"), exist_ok=True)
os.makedirs(os.path.join(app, "other"), exist_ok=True)
with open(os.path.join(sol, "summary.csv"), newline="") as f:
    rows = list(csv.reader(f))
header, body = rows[0], rows[1:]
placement = []
with open(os.path.join(sol, "placement.tsv")) as f:
    for line in f:
        line = line.rstrip("\n")
        if line.strip():
            d, name, _h = line.split("\t")
            placement.append((d, name))
inv_names = sorted(n for d, n in placement if d == "invoices")
first_inv = inv_names[0]
total_rows = [r for r in body if r[0] == "total"]
assert len(total_rows) == 1, total_rows
first_row = [r for r in body if r[0] == first_inv]
assert len(first_row) == 1

def move_all(transfers=None, keep_in_docs=False):
    # transfers: {name: destdir}
    for d, name in placement:
        dest = (transfers or {}).get(name, d)
        if keep_in_docs:
            # C07: copy into documents/keep, then move originals
            keep = os.path.join(app, "documents", "keep")
            os.makedirs(keep, exist_ok=True)
            shutil.copyfile(os.path.join(docs, name), os.path.join(keep, name))
        shutil.move(os.path.join(docs, name), os.path.join(app, dest, name))
    for jf in sorted(os.listdir(os.path.join(sol, "invoices-json"))):
        shutil.copyfile(os.path.join(sol, "invoices-json", jf), os.path.join(app, "invoices", jf))

def write_summary(table, prefix=""):
    buf = io.StringIO()
    csv.writer(buf).writerows(table)
    with open(os.path.join(app, "invoices", "summary.csv"), "w", newline="", encoding="utf-8") as f:
        f.write(prefix + buf.getvalue())

if case == "C03":
    # eleven total rows -> summary = header + 11 copies of the single total row
    move_all()
    write_summary([header] + total_rows * 11)
elif case == "C04":
    # ten copies of one invoice row + total row
    move_all()
    write_summary([header] + first_row * 10 + total_rows)
elif case == "C07":
    # copies kept in /app/documents/keep/ (documents not empty after moves)
    move_all(keep_in_docs=True)
    shutil.copyfile(os.path.join(sol, "summary.csv"), os.path.join(app, "invoices", "summary.csv"))
elif case == "C08":
    # duplicate invoice copy inside /app/invoices/
    move_all()
    shutil.copyfile(os.path.join(sol, "summary.csv"), os.path.join(app, "invoices", "summary.csv"))
    shutil.copyfile(os.path.join(app, "invoices", first_inv), os.path.join(app, "invoices", "copy-" + first_inv))
else:
    raise SystemExit("unsupported case " + case)
print("BUILT", case, "first_invoice=", first_inv, "total=", total_rows[0])
