# S251 anchor — Git `git-rev-parse` documentation

- URL opened: `https://git-scm.com/docs/git-rev-parse`
- Access date: 2026-11-04 UTC (L1 `KengakuR75`)
- HTTP: 200, 122459 bytes
- Capture: `corpus/evidence/round75/sources/git-rev-parse.html`
- sha256: `00e3b1aaf8ae9df59a7a6bb8224e19e825c628b7a0cd69a4f03aeda79c2be587`
- Document title: `Git - git-rev-parse Documentation`
- Anchor: the `--verify` entry of the OPTIONS section, capture line 2720.

Located quote (18 words, capture lines 2720-2721):

> “Verify that exactly one parameter is provided, and that it can be turned into a raw 20-byte SHA-1”

Scope of the admit: the syntax and the acceptance semantics of `git rev-parse --verify <rev>` —
i.e. that a revision argument is checked and resolved to an object id, erroring out otherwise.
It does NOT establish ancestry (`git merge-base --is-ancestor`, a separate command), does not
establish that a stored hash names a *commit* rather than another object type (the `^{commit}`
dereference suffix documented later on the same page does), and says nothing about whether the
receipt that carries a hash was produced from a clean tree.

Why it is load-bearing for R75-C2: `plans/round75_c2_registry_audit.py` stamps receipts with
`LANE_TIP <40-hex>` and refuses a stamp that `git rev-parse --verify --quiet <hex>^{commit}`
cannot resolve, then proves ancestry with `git merge-base --is-ancestor`. The reject candidate —
"a 40-hex string in a receipt proves the receipt measured that revision" — is refused because
`--verify` proves only resolvability, not that the named tree produced the printed numbers; the
instrument's `WORKTREE` line and the clean-clone production of receipts carry that part, and the
lesson records it as a limit rather than a proof.
