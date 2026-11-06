# ExecImage — R96-C1 falsifiable hypothesis: agent-side venv faithfulness

Hypothesis: 'the replay's agent-side venv is a faithful model of the task image for the 17 cases'.

## Method
Docker was usable without sudo on this host. Pulled `alexgshaw/multi-source-data-merger:20251031`
(task.toml:30 `docker_image`), recorded its digest, ran `solution/solve.sh` inside the real image,
copied out `/app/merged_users.parquet` + `conflicts.json`, graded them via the replay's grader-side
harness and via real pytest, and compared to C01. Also tested the weaker pyarrow 17→22 dtype
round-trip hypothesis for C07/C09.

## Findings
1. Image digest `sha256:8b32782078ff7383a1b4e5d3cecca8ce287e30f50bb4c0e5db009a18064e666e`,
   788 MB (221 MB compressed). Pulled with `docker pull`, rc 0, no sudo needed.
2. Image internals: python 3.11.14, pandas 2.2.3, pyarrow 17.0.0, numpy 2.3.4. The venv uses
   python 3.11.17 (same minor), pandas 2.2.3, pyarrow 17.0.0 — identical pins — but numpy **2.4.6**
   (unpinned on both sides; resolved at install time).
3. `/data` file hashes inside the image are byte-identical to the lane capture (all three sha256
   match the frozen PINS in `plans/round-96-claims.md`).
4. `solve.sh` inside the real image: rc 0, 4 users, 3 conflicts.
   Outputs are **byte-identical** to a venv run (`39c8e4f4…` parquet, `bce88c82…` conflicts.json).
   The numpy 2.3.4 vs 2.4.6 difference does not affect these outputs.
5. Grading container outputs with grader-side venv (python 3.13.16, pandas 2.3.3, pyarrow 22.0.0):
   `PAYLOAD P,P,P,1` — matches predicted C01 `P,P,P,1`.
   Real pytest (8.4.1, same venv, `/app` bind-mounted): **3 passed in 2.32s**, rc 0.
6. Weaker hypothesis (pyarrow 17 write → pyarrow 22 read): dtypes identical to same-version write
   (user_id int64, rest object/string); `df.equals()` True. C07 float64 set/selection behaviour and
   C09 datetime64 inequality reproduce exactly under pyarrow 22 reads.

## Verdict
Hypothesis **holds** for C01. No defect found that would flip any of the 17 cases: the agent-side
venv faithfully models the task image for the positive control, and the cross-version parquet
behaviour the 17-case table depends on (C07/C09) is version-stable.

## Note (info, not a finding against the claim)
The probe stamps `ENV_SIDE python,pandas,pyarrow,numpy 3.11.17 2.2.3 17.0.0 **2.4.6**`, while the
task image actually runs numpy **2.3.4**. Both are unpinned (`pip install pandas==2.2.3 pyarrow==17.0.0`
resolves whatever numpy is current), so this churn is expected and the byte-identical outputs show it
is harmless here. Not a frozen-instrument change request; recorded for completeness.

## Disk / cleanup
Image removed (`docker rmi`, rc 0); net disk 0. Scratch dir removed before yield.

## Files written
- `.ufo/waves/round-96/w1/ExecImage.md` (this report; trailer path relative to lane root)
- `.ufo/waves/round-96/w1/ExecImage/report.md`
- `.ufo/waves/round-96/w1/ExecImage/image-receipt.txt`
- `.ufo/waves/round-96/w1/ExecImage/pytest-receipt.txt`
- `.ufo/waves/round-96/w1/ExecImage/c01-comparison.txt`
