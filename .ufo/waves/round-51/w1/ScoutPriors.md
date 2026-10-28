# ScoutPriors — prior art for the C1 instrument

Seat: ScoutPriors (scout). Axis judged: adjacency. Question: is "a manifest of declared surfaces probed by a committed counter, with a dated-absence rule and a resolve floor" standard practice, and where is it documented?

Ruling up front: **INCREMENTAL**. Not NOVEL-INSTRUMENT, not KNOWN. This is input to novelty honesty. It is not a claim that round 51 invented a new class, and it is not a claim that a named spec already states this predicate.

## Axes

1. Source primacy — quotes come from pages fetched this seat, not from search snippets.
2. Piece coverage — manifest-plus-probe, dated absence, and resolve floor scored separately.
3. Ruling honesty — known pieces do not make the conjunction known; a missing conjunction does not make the class novel.
4. Quote fidelity — the deciding line is a sentence that was fetched.

## Instrument under test

Read at the lane tip. `plans/round51_surfaces.py` and `plans/round51-surfaces.json` are byte-identical to the stage-1 freeze (blob `6107c605925310ed64433b1f27d3459e8836ed43` at both commits; `git diff --stat` from the freeze to `HEAD` on those two files plus `plans/round-51-claims.md` was empty).

The counter's frozen predicate (`plans/round51_surfaces.py` lines 11–20) is the object of the check:

- every entry's probe result equals its recorded `state` (STALE 0);
- every recorded `state` equals the row's prose (DRIFT 0);
- every absent entry's row matches `ABSENT\s+(\d{4}-\d{2}-\d{2})` or the row is UNVERDICTED (`ABSENT_RE`, lines 40 and 201–204);
- `observed_present >= resolve_floor` (`resolve_floor` is `13` in `plans/round51-surfaces.json`); the docstring says declaring everything absent drives the count below the floor recorded before any repair.

## Commands

Read-only git, cwd not used (absolute `-C`):

```
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format='%H %ci %s' e07f131cf7037e58a21db6e1f3986cf401ad257c
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format='%H %ci %s' HEAD
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff --stat e07f131cf7037e58a21db6e1f3986cf401ad257c HEAD -- plans/round51_surfaces.py plans/round51-surfaces.json plans/round-51-claims.md
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse e07f131cf7037e58a21db6e1f3986cf401ad257c:plans/round51_surfaces.py HEAD:plans/round51_surfaces.py
```

Observed:

```
4090c3db79d11279ab5e5121ba25e74aa316e6e7
4090c3db79d11279ab5e5121ba25e74aa316e6e7
e07f131cf7037e58a21db6e1f3986cf401ad257c 2026-10-28 15:09:28 -0300 round-51: stage-1 freeze — C1 surface-truth counter+manifest, C2 routing counter, claims, before receipts
4090c3db79d11279ab5e5121ba25e74aa316e6e7 2026-10-28 15:15:05 -0300 round-51: v2 wave spec (64 seats) + validated dispatch payload
6107c605925310ed64433b1f27d3459e8836ed43
6107c605925310ed64433b1f27d3459e8836ed43
```

The diff stat printed nothing. Fetches were HTTP reads of the URLs below. No package was installed (pacman is paused; nothing was required). Scratch `/fast/scratch/hyaku/kengaku-r51/ScoutPriors` was created empty and removed before yield. The counter itself was not re-run; the before receipt is not this seat's measurement.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

## What is already standard

| Piece of the instrument | Fetched source | What that source actually requires |
| --- | --- | --- |
| Versioned manifest of desired state, checked against observation | OpenGitOps Principles 1.0.0 | Declarative desired state, stored immutably, continuously reconciled |
| A committed probe of a declared target (exec / HTTP / TCP) | Kubernetes probes; Prometheus blackbox | Periodic diagnostic; success or failure |
| A date on a status transition, including to not-ready | Kubernetes `meta/v1` Condition | `lastTransitionTime` when status flips |
| A numeric floor that fails the check | coverage.py `--fail-under`; Kubernetes PodDisruptionBudget | Coverage below MIN exits 2; voluntary eviction must leave a minimum number of pods |
| An inventory plus an independent audit | ACM badging v1.1 | Human badges; metrics explicitly left unspecified |
| Standardized re-run of a declared eval set, with gaps named in prose | HELM (arXiv:2211.09110); Pineau et al., JMLR 22(164), 2021 | Living benchmark / Yes-No checklist, not a dated-absence counter |

### Drift / health-check specs

OpenGitOps Principles v1.0.0, fetched from `https://raw.githubusercontent.com/open-gitops/documents/v1.0.0/PRINCIPLES.md` (same four principles on `https://opengitops.dev/`):

> 1. **Declarative** — A system managed by GitOps must have its desired state expressed declaratively.
> 2. **Versioned and Immutable** — Desired state is stored in a way that enforces immutability, versioning and retains a complete version history.
> 4. **Continuously Reconciled** — Software agents continuously observe actual system state and attempt to apply the desired state.

That is the class this counter sits in: a committed declaration, compared to a live probe. It does not say the declaration is a table of documentation rows, and it does not define absence, a date, or a floor.

Kubernetes probe concept page, `https://kubernetes.io/docs/concepts/workloads/pods/probes/` (page last modified 2026-06-30):

> Kubernetes lets you define probes to continuously monitor the health of containers in a Pod. A probe is a diagnostic performed periodically by the kubelet on a container. To perform a diagnostic, the kubelet either executes code within the container or makes a network request.

The same page defines the four mechanisms the C1 counter also uses in miniature (`exec`, `httpGet`, `tcpSocket`, plus gRPC): "The diagnostic is considered successful if the command exits with a status code of 0" / "if the response has a status code greater than or equal to 200 and less than 400" / "if the port is open." Failure is a result (`Success` / `Failure` / `Unknown`), not a required `ABSENT <ISO date>` left inside the desired-state text. "If a container does not provide a particular probe, the kubelet always considers the result as `Success`." Dropping a probe does not fail a dated-absence check.

Prometheus multi-target exporter guide, `https://prometheus.io/docs/guides/multi-target-exporter/`, on the blackbox exporter: the probe result is a gauge, `probe_success`, "Displays whether or not the probe was a success." Targets are parameters of a scrape, not rows that must stay declared once they go absent.

### Dated status, not dated absence inside the declaration

Kubernetes Condition reference, `https://kubernetes.io/docs/reference/kubernetes-api/definitions/condition-v1-meta/` (generated API reference, last modified 2026-08-26):

> lastTransitionTime is the last time the condition transitioned from one status to another. This should be when the underlying condition changed. If that is not known, then using the time when the API field changed is acceptable.

`status` is "one of True, False, Unknown." The date is a field of the observed condition. It is not a token the desired-state document must carry or else the audit is UNVERDICTED, and deleting the object deletes the date with it. The C1 rule (instrument lines 201–204) is stricter and pointed the other way: the human-facing row in `PROVINCE.md` must still contain `ABSENT` plus an ISO date after the surface is gone.

### Floors that fail a check, and the hole in them

coverage.py 7.16.2 reference, `https://coverage.readthedocs.io/en/7.16.2/commands/cmd_report.html`:

> `--fail-under=MIN` Exit with a status of 2 if the total coverage is less than MIN.

That is a committed threshold on a measured count. It is a percentage of executed statements. Deleting the unexecuted lines raises the percentage. It does not count "surfaces that still resolve," and it has no dated-absence rule.

Kubernetes disruptions, `https://kubernetes.io/docs/concepts/workloads/pods/disruptions/`:

> A PDB limits the number of Pods of a replicated application that are down simultaneously from voluntary disruptions. For example, a quorum-based application would like to ensure that the number of replicas running is never brought below the number needed for a quorum.

The same page states the bypass that the C1 floor is written to close:

> Not all voluntary disruptions are constrained by Pod Disruption Budgets. For example, deleting deployments or pods bypasses Pod Disruption Budgets.

`resolve_floor` (instrument lines 19–20 and 219–223) fails the predicate when every row is dated absent, i.e. when the declaration is edited so that nothing resolves. A PDB does not.

### Reproducibility checklist (ACM)

ACM Artifact Review and Badging, Version 1.1, 24 August 2020, fetched from `https://www.acm.org/publications/policies/artifact-review-and-badging-current`:

> Documented: At minimum, an inventory of artifacts is included, and sufficient description provided to enable the artifacts to be exercised.

An inventory is required for the Functional badge. The same document refuses to fix the metric:

> What specific metrics should be used to assess quality? Current grassroots efforts to evaluate artifacts and formally test replicability have answered these questions in different ways. We believe that it is still too early to establish more specific guidelines for artifact and replicability review.

Artifacts Available requires a public archival repository, not a probe. There is no dated-absence marker and no resolve floor. A missing artifact simply does not receive the badge; the paper is not required to keep a dated tombstone of it.

### LLM-eval reproducibility

Holistic Evaluation of Language Models, Liang et al., arXiv:2211.09110, submitted 2022-11-16. Abstract fetched from `https://arxiv.org/abs/2211.09110`:

> Then we select a broad subset based on coverage and feasibility, noting what's missing or underrepresented (e.g. question answering for neglected English dialects, metrics for trustworthiness).

and:

> For full transparency, we release all raw model prompts and completions publicly for further analysis, as well as a general modular toolkit. We intend for HELM to be a living benchmark for the community, continuously updated with new scenarios, metrics, and models.

"Noting what's missing" is prose. HELM's own move is to *select a subset* (coverage of core scenarios was 17.9% before, 96.0% after, on the scenarios HELM chose). That is the opposite of a floor that forbids the present-set from shrinking, and it is not a machine check that an undated absence is UNVERDICTED.

Pineau et al., JMLR 22(164):1–20, 2021, landing page `https://jmlr.org/papers/v22/20-303.html` (abstract only; the PDF body was not fetched):

> Reproducibility, that is obtaining similar results as presented in a paper or talk, using the same code and data (when available), is a necessary step to verify the reliability of research findings.

The program they describe is "a code submission policy, a community-wide reproducibility challenge, and the inclusion of the Machine Learning Reproducibility checklist." That is a human checklist over papers, not a counter over a lane's declared host surfaces.

## Deciding line

The line that blocks **KNOWN** is ACM's, because the nearest reproducibility standard says the metric is intentionally not specified:

> What specific metrics should be used to assess quality? [...] We believe that it is still too early to establish more specific guidelines for artifact and replicability review.

The line that blocks **NOVEL-INSTRUMENT** is OpenGitOps principle 4, because the class (versioned desired state, continuously compared to observed state) is already a published principle:

> Software agents continuously observe actual system state and attempt to apply the desired state.

No sentence fetched from those sources, from the Kubernetes Condition or probe pages, from the PodDisruptionBudget page, from coverage.py's `--fail-under` text, from the Prometheus blackbox guide, from the HELM abstract, or from the Pineau abstract, states the conjunction the counter actually implements: one committed manifest, probed by a committed program, where an absent row without `ABSENT <ISO date>` is its own failure, and where `observed_present` must stay at or above a floor frozen before repair so that dating every row absent still fails.

That conjunction is the increment. The round must not call the instrument a new class, and must not call the predicate a restatement of ACM, HELM, GitOps, or a health probe.

## Limits

- Targeted fetches, not a literature census. [INFERENCE] another internal runbook or a spec this seat did not open could still state the conjunction. The ruling is "not in the fetched primary sources," which is the evidence bar this item set (at least three: a drift/health spec, ACM badging, one LLM-eval paper). Six primary documents were fetched.
- Pineau is cited from the JMLR abstract page only. The checklist items inside the PDF were not quoted.
- HELM is cited from the arXiv abstract, not from a methods section of the PDF.
- OpenGitOps reconciliation *applies* desired state; C1 only *reports* drift. The mapping is the declare-and-compare class, not identity of mechanism.
- C2 (routing attribution) was out of scope for this prior-art question.
- No tool was installed or upgraded.

VERDICT: INCREMENTAL
