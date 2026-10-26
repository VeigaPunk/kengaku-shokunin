# R43CritClaims — claims attack (kengaku r43 w1, critic)

Attacked: frozen claims `plans/round-43-claims.md` (freeze 02753f260805e2e45b05af22145da00f91671364) and the controls
under `.ufo/waves/round-43/claims/`. Focus: can a do-nothing or junk artifact reach either frozen predicate; is every
control discriminating; for C2/V10, is the DECISIVE-map filler measuring reading or copying; C1/C2 causal separability;
lowest-axis honesty.

All measurement runs were executed inside the round-43 envelope (`claims/envelope.sh`), scratch
`/fast/scratch/hyaku/kengaku-r43/R43CritClaims`, on a `--shared` clone of the lane at `$S/lane` (toplevel verified =
`$S/lane`). Evidence files (sha256) live in `corpus/…` and `build/R43CritClaims/`:
`copycat.out 00ecf04b97c2c2fef68b27223a0c19a1702a5cf3f273d75e7670482754a7773c`,
`junkbat.out c5f636d7ec837a47baf98f0d325496aca855b3ccc56061c04f6ca3e02b40853d`,
`junkbat2.out 3cd696cdcb52e57390bed02023c41c087dd011dfb2e16c43a62f6ca7265f9041`.

## 1. C2/V10: a junk artifact REACHES the frozen predicate (defect 1)

The claim (`round-43-claims.md:104-105`, `round43_c2_verify.py:44-45`) says V10 is "the content a receipt does not
carry" and that "a filler that copies the receipt cannot pass V10 without reading the captures". I built a filler that
passes V9 **and** V10 with zero grader understanding: it imports the frozen counter itself (`c2_filler_control.py`
already imports it the same way), reads the counter's public `DECISIVE` map
(`round43_c2_verify.py:330-343`), and per case cites the **first** decisive line with a quote made of a mechanical
middle-token window of that line. No semantics anywhere.

ENVELOPE line (copycat.out):
```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r43/R43CritClaims/env /fast/scratch/hyaku/kengaku-r43/R43CritClaims/env --bind /fast/scratch/hyaku/kengaku-r43/R43CritClaims/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /fast/scratch/hyaku/kengaku-r43/R43CritClaims/copycat_filler.py --lane /fast/scratch/hyaku/kengaku-r43/R43CritClaims/lane --work /fast/scratch/hyaku/kengaku-r43/R43CritClaims/w
ENVELOPE start 19:09:19 cwd=/home/vgpnk/Projects/shokunin
...
COPYCAT V9 ok case_rows=12/12 bad=0
COPYCAT V10 ok mechanism_rows=12/12 bad=0
ENVELOPE end 19:09:21 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
The mechanism rows it generated (vacuous or broken fragments, mechanically cut from the decisive line):
```
nop: test_outputs.py:24 quote='import attack'
oracle-solve-sh: solve.sh:59 quote='candidates ='
wrong-key: test_outputs.py:30 quote='feal_in_c.get_keys()[5] =='
oracle-off-by-one: test_outputs.py:30 quote='feal_in_c.get_keys()[5] =='
return-str: test_outputs.py:30 quote='feal_in_c.get_keys()[5] =='
cheat-import-get_keys: feal_module.c:25 quote='py_get_keys(PyObject* self,'
cheat-always-equal: test_outputs.py:30 quote='feal_in_c.get_keys()[5] =='
cheat-sysmodules-shadow: test_outputs.py:24 quote='import attack'
cheat-patch-get_keys: test_outputs.py:29 quote='stolen ='
cheat-exit-zero: test.sh:17 quote='uvx \'
cheat-clock-seed: feal.c:65 quote='= rand()'
slow-oracle-45s: test_outputs.py:29 quote='stolen ='
```
5/12 cases need **no capture read at all**: their quote is a ≥2-word phrase lifted verbatim from the counter's own
public comments (`round43_c2_verify.py:331-342`), which is already verbatim on a decisive line (`nop` "import attack";
`wrong-key`/`oracle-off-by-one`/`return-str`/`cheat-always-equal` "get_keys()[5] == stolen").

**What V10 measures:** fidelity to the counter's frozen `DECISIVE` map (cap:line ∈ map) plus a ≥2-word verbatim
substring. **What V10 cannot see:** (a) whether the writer read the captures vs copied the counter — the map is public
and the fill is one line copy; (b) quote semantics — a broken fragment (`feal_in_c.get_keys()[5] ==`, `stolen =`,
`uvx \`, `= rand()`) passes; (c) whether the cited line is causally relevant to the case — e.g. `slow-oracle-45s`
(the time cheat) cites `test_outputs.py:29` (the `attack()` call) rather than `task.toml:22` (`timeout_sec`, also
decisive), and the filler's rule picks whichever comes first; (d) anything about the verdict — V10 never links the row
to the case's `violates=` tags or observed pass/fail. The check is a copy-fidelity gate, not a reading/understanding
gate. The frozen claim's sentence "cannot pass V10 without reading the captures" is therefore only mechanically true
(7/12 rows need one captured line's bytes); the *understanding* claim fails.

The control's "content" mirror passes because it hand-picks meaningful quotes; my copycat shows the pass does not
require meaning.

## 2. C1: do-nothing / junk artifacts CANNOT reach the predicate (controls discriminate)

- Do-nothing module at the contract (empty `FIXTURES = []`, valid e):
```
ENVELOPE start 19:08:53 ...
BATTERY fixtures=0 wrong=0 tampered=0 sidechannel=0
MUTANTS total=9 killed=0 survived=9 invalid=0 null_detected=0 unattributed=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 19:08:54 exit=1 ... unchanged
```
- Misdeclared junk (empty dir, anchor, `expect=accept`, really exits 2): `FIXTURE j1 ... WRONG`, `BATTERY
  fixtures=1 wrong=1`, `killed=0`, exit 1 (junkbat2.out). A trivially-empty-dir fixture declared `expect=error` is
  coincidentally correct (`observed_rc=2`) and still kills nothing — surviving mutants need a genuine behavioral
  difference. Legs f (span executed) and g (site record differs from twice-stable reference) block do-nothing kills.
- Frozen controls all match their claim text: `control-c1-nothing.txt` (`killed=0 survived=9`), witness-as-battery
  (pass, 9/9), no-mutants (fail), attribution (unattributed=9), value (unattributed=9), tool-edited (PINS
  mismatched=1, 6 invalid), hostile h1-h6 closed under the round-43 counter. The only acknowledged reachability is the
  witness module copied as a battery — documented as a limit with non-author review (`round-43-claims.md:70-71`).

## 3. Control discrimination, C2

`control-c2-nothing.txt`: `checks=10 defects=7` (V2,V3,V4,V7,V8,V9,V10), exit 1 — do-nothing red, matches claim.
`control-c2-informed-filler.txt`: filler → V9+V10 DEFECT, informed → V9 ok / V10 DEFECT (7/12 rows on the nondecisive
assert line), content → V9+V10 ok, `red-as-required`. The control set is self-consistent **and** my copycat shows the
"content" row is not a lower bound on filler sophistication — the same V10 pass is achievable with zero meaning. The
discrimination question is not whether V10 fires on a receipt-only filler (it does) but whether it measures what the
claim says it measures (it does not, §1).

## 4. Causal separability

Input sets are disjoint in work products: C1 reads only the two tools + `plans/battery43` + fixture repos built from
nothing (`round43_c1_verify.py:2-6,64-72`); C2 reads captures, spec, gate, probe, dry table, receipt, entry, SOURCES,
README, PROVINCE and the git history of the claims/receipt (`round43_c2_verify.py:11-50`). Each fails red with the
other's deliverable absent (both do-nothing controls), so "each passes with the other's work wholly absent" holds.
One shared artifact exists: `plans/order_check.py` is calibrated by C1 **and** consumed by C2's V8
(`round43_c2_verify.py:35-36`). Within the freeze (tools immutable) this is not a feedback loop; if a future round
edited order_check, both counters would move — the claims do not name this shared pin. Verdict: separable as claimed,
with that one named shared pin.

## 5. Lowest-axis honesty

The claim transparently chooses coverage at the tie (7=7) with a stated tie-break (pinned local source + offline
sandbox vs novelty's dated prior-art; `round-43-claims.md:22-27`) and scopes C2 as "judged on its counter, not on a
score move", explicitly carrying no novelty claim (`:119`). The one unverified premise is the cited `F42CritPlanNext`
D4 third-party prior-art finding; nothing in local evidence contradicts it. The framing is honest; the V10 overstatement
in §1 is the only place where the claim's wording exceeds what its counter enforces.

## Defects (n=3)

1. **C2/J10 gameable by counter-copying** — a junk artifact (no grader understanding) reaches the frozen C2 predicate;
   the counter's public `DECISIVE` map is the oracle for passing V10 (copycat.out: V9 ok, V10 ok, exit 0).
2. **Quote semantics unconstrained** — any ≥2-word verbatim substring passes, including broken mid-expression fragments
   and causally irrelevant first-map-entry lines (`slow-oracle-45s` cites the call line, not the timeout line).
3. **No verdict/role link in V10** — the row is never checked against the case's `violates=` tags, predicted/observed
   verdict, or the reason the line is decisive; relevance is asserted by the map, which the filler reads from the
   counter itself.

Smallest safe corrections (for L1 consideration, not executed): (i) in the claims' V10 sentence, replace "without
reading the captures" with "without the counter's DECISIVE map" (the construct is a fidelity gate); (ii) optionally harden
V10 with a uniqueness/coverage rule such as requiring the quote to contain a token of the case's tag-carrying sentence
or requiring the chosen line to be the *only* decisive line for cases with multiple candidates — this would catch the
broken fragments; (iii) keep DECISIVE frozen as is (not widened after data). No claim text or counter change was made.

VERDICT: claims-attack-defects-3-v10-filler-pass
