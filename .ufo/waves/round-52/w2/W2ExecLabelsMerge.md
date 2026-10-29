# W2ExecLabelsMerge — report (kengaku r52 wave 2)

Attacked/produced: merge of wave-1 blind labels into counter shape. Source:
`.ufo/waves/round-52/w1/C1ExecBlindLabels/labels.json` (present; sole label source — no other wave-1 seat produced labels, none invented).

Commands: read `labels_agreement()` (plans/round52_c1_grader_audit.py:260-283), then a python3 validator: every task in
`plans/round52-tasks.json` (89), no duplicates, class in {V0..V4}, rows rewritten as `{"labels":[{task,class,why}]}`.
Result file: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ExecLabelsMerge/labels.json`
(sha256 174c3f6c241125c6a5fefadd4a5521b604e1462bf170ee3fd44f23a06d8522f2 — byte-identical to the w1 file; no re-labelling).

Measured: 30 labels (0-based sorted-index multiples of 3 over 89 tasks). Histogram V1=1 V2=18 V3=11 V4=0 V0=0.
Prefix-24 subset (labels-prefix24.json) is a strict subset of the 30 (verified). `sanitize-git-repo` (excluded capture) is NOT among the labelled tasks.
`corpus/evidence/round52/labels.json` does not exist in the lane yet (L1 integrates; I did not write it).

Blindness: labels were produced blind to classifier OUTPUT (records.json / notes.json / counter run), per the w1 report. NOT fully blind to
the classifier RULE: the seat read the counter source regexes and cross-checked with a mechanical claims-vocabulary pass (30/30 agreed). So agreement
measures hand-reading vs rule on frozen vocabulary, not an independent construct. The first-match order in the w1 report text (V1→V2→V3→V4) matches the
counter's classify() effective order (V1, V2, V3, V4, V0); no divergence. I did not run the counter, so the agreement figure is unmeasured here.
Caveat: pytorch-model-recovery labelled V1 on vocabulary grounds though the grader is substantively strict (w1 noted) — a vocabulary-gap label, expected to agree with classifier.

Attack landed? n/a (merge); no defect found in the labels file shape. Scratch dir removed.
