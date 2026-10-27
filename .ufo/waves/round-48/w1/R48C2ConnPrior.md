# R48C2ConnPrior — task-grader ownership finding

**Axis:** coverage. **Measured revision:** none; no scored counter or probe was run. **Verdict:** scoped ownership finding only; no R48-C2 admission claim.

## Finding

The sibling lane PROVINCE evidence identifies **no sibling owner for analysis or execution of this task-grader surface**. Kengaku PROVINCE explicitly assigns static LLM-evaluation interpretation and offline execution of pinned Terminal-Bench graders to kengaku's Core (rounds 35–38, lines 230–300; later continuation should be interpreted narrowly by each task). It routes distinct supporting practices outward: verification-fixture craft to tameshi, research method to chousa, prompt craft to kotoba, and seat arrangement to kumitate (lines 262–263). These are adjacent practices, not ownership of grader analysis/execution. It also expressly distinguishes offline captured-grader behavior on lane-authored synthetic inputs from running Terminal-Bench, task images, or real submissions (lines 232–240).

Sibling province checks:
- `kasegi-shokunin/PROVINCE.md:45-51` labels kengaku as the adjacent LLM evaluation/benchmarks lane; it does not claim grader ownership.
- `kaidoku-shokunin/PROVINCE.md:97-118` defines reverse engineering of shipped artifacts and marks source-available reconstruction of ordinary repositories as unowned/adjacent, not task-grader ownership.
- `kake-shokunin/PROVINCE.md:3-6,38-47` owns web properties/publishing and routes browser/crawler discipline to tabi; unrelated to static grader interpretation/execution.
- `kengaku-shokunin/PROVINCE.md:19-20,123-143,230-263` is the direct evidence of its own grader surface and reported-out adjacent roles.

**Scoped disposition:** do not transfer or absorb grader analysis/execution as a sibling-owned task. Keep this item within kengaku's stated static-grader scope. Do not expand it into benchmark runtime, model/agent performance, hosted judge, task validity, or real-submission claims; those are explicitly excluded/open in the cited kengaku province passages.

## Evidence and limits

Local source URLs: `file:///home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md`, `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md`, `file:///home/vgpnk/Projects/shokunin/kake-shokunin/PROVINCE.md`, `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/PROVINCE.md`; accessed 2026-10-27. Located quotes (each <=25 words):
- Kasegi line 50: “kengaku — LLM evaluation and benchmarks”
- Kaidoku lines 108-109: “Source-available reconstruction of ordinary repositories … (unowned).”
- Kake line 40: “tabi drives browsers and owns client-side crawler discipline”
- Kengaku lines 232-234: “static interpretation and offline synthetic-fixture execution of one pinned Terminal-B 2.0 grader”

Exact commands run:
1. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD` → `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767` (current checkout only; not the frozen base).
2. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin ls-tree -r --name-only HEAD .ufo/waves/round-48/w1` → no output.
3. Read round-48 claims and round-46 spotcheck; read sibling PROVINCE paths above; searched wave registry for task-grader references. Registry contains a sibling R48C2Scope scout assignment to distinguish grader interpretation from benchmark/runtime/model performance, but the requested ownership question is resolved by the PROVINCE evidence.

No freeze verification or scored run was needed for this ownership-only item. Limit: province declarations establish documented lane scope, not external or unrecorded ownership. No tools installed or updated.