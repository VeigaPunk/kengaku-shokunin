writer: KengakuR29-2.FSentinelSecrets-2
# Round 29 committed-file secret scan

## Scope and method

Axes checked: credential confidentiality, cookie/auth-state exposure, environment values, token material, and private/internal URL exposure. Scanned the changed paths from `ed26bdf5d924755697cd6812129be2fa441c42a3` to `56fd949a6478342531e61f4feecb4a685d831640`, reading each blob from the latter commit (not relying on the working tree).

Command used to enumerate the scope:

`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff --name-only ed26bdf5d924755697cd6812129be2fa441c42a3 56fd949a6478342531e61f4feecb4a685d831640`

Observed output: 226 paths. The scan fetched all 226 with `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 56fd949a6478342531e61f4feecb4a685d831640:<path>`; no missing blobs. Coverage was 6,308,823 bytes / 206,104 UTF-8 text lines; no NUL-containing or invalid-UTF-8 files.

## Findings

**Severity: Informational.** No credential, cookie, auth-state, environment-value, or usable token exposure found. URL scan found only synthetic/non-public test references described below; no credentialed URL, private/loopback/link-local IP, localhost, `.local`, `.internal`, `.lan`, or `.home` endpoint.

- **Credentials and environment:** 0 case-sensitive credential-like environment assignments; no `.env`, credential, auth-state, cookie-jar, or storage-state files. Structured JSON scan found no cookie/auth-state objects and no password, secret, cookie, authorization, or credential fields. The `token`/`tokens` fields are projection-analysis data (e.g. replacement/occurrence markers), not authentication credentials; no known provider-token, JWT, bearer/basic credential, or PEM private-key pattern matched.
- **URLs:** 8,198 URL occurrences use reserved `.invalid` hosts, consistent with the round's frozen synthetic profiles and their recorded projections. These are not private endpoints. A further 11 `http://` occurrences at the locations below use single-label/placeholder hosts. Their values are deliberately omitted: the governing handling instruction forbids recording private URLs. The contexts identify them as profile examples, cascade/escaping fixtures, oracle notes, and the instrument's self-test inputs.
  - `.ufo/waves/round-29/build/R29SimplifySourceContract.md:105,108` — 2 occurrences.
  - `.ufo/waves/round-29/build/R29Task389.md:213-214,251` — 3 occurrences.
  - `.ufo/waves/round-29/scratch/KengakuR28.R29Task389-2/oracle389.out:91,93` — 2 occurrences.
  - `.ufo/waves/round-29/scratch/KengakuR28.R29Task389-2/oracle389.py:512,528` — 2 occurrences.
  - `plans/config_projection.py:420` — 2 occurrences in self-test literals.

No other non-public URI classes matched. The 11 reported values are all `http://<single-label-host>` test/example values; their exact URLs are redacted rather than reproduced.

## Attack path, impact, and remediation

No credential-replay or authenticated access path was found. **[INFERENCE]** If a single-label example URL were copied into an active network client, resolver search domains could make it resolve to an unintended internal host; the reviewed occurrences are test/example data, and this scan did not observe a network action. Impact in the committed snapshot is limited to retaining those synthetic references. Smallest optional hygiene change outside this read-only review: use reserved `.invalid` hostnames for examples where the host itself is not under test. No remediation was made.

The production instrument source `plans/config_projection.py` was included in the blob scan; this assignment did not perform a behavior review. No tools were installed or updated.

## Follow-up: newly fetched upstream scratch copies

Scope: `.ufo/waves/round-29/scratch/falsify/FRevEnumerate/src/` — all 88 files (7,550,641 bytes), including the binary image files. This is separate from the earlier committed-path scan. No credential or URL values are reproduced below.

**Severity: High for the retained credential literals.** The copied `browser_env/env_config.py:32-40` contains a static `ACCOUNTS` map with username/password literals for five site accounts. `browser_env/auto_login.py:69-99` consumes those account fields in login flows and `:102` writes browser storage state. The consumer does not need to be executed for the account literals to be exposed in the retained source.

**Exact source copies to remove/redact from scratch (not needed for C1):**

- `.ufo/waves/round-29/scratch/falsify/FRevEnumerate/src/browser_env/env_config.py` — account credential literals at lines 32-40; literal site endpoint defaults at lines 44-50.
- `.ufo/waves/round-29/scratch/falsify/FRevEnumerate/src/browser_env/auto_login.py` — auth workflow consuming the account values and capable of writing storage-state files; companion to the credential map.
- `.ufo/waves/round-29/scratch/falsify/FRevEnumerate/src/setup_env.sh` — six exported internal/single-label site endpoint values at lines 28-33.
- `.ufo/waves/round-29/scratch/falsify/FRevEnumerate/src/config_files/test.raw.json` — account/account-list fields and 10 username-only URL-userinfo occurrences at lines 9197, 9202, 9226, 9231, 9255, 9260, 9284, 9289, 9313, and 9318. The parsed URLs had no password component; treat this as account-identifier-bearing task data, not confirmed password material.

**Additional endpoint-only source copy:** `.ufo/waves/round-29/scratch/falsify/FRevEnumerate/src/webarena-map-backend-boot-init.yaml` contains private/local endpoint probes at lines 248, 255, and 264; line 283 identifies the AWS link-local instance-metadata endpoint, with shell command substitutions invoking `curl` at lines 285-289. No credentials were detected in that file; remove/redact it too if the cleanup boundary includes real/private endpoint values. `browser_env/env_config.py` is already listed above for its endpoints.

Observed corroboration: the bounded scan found one `OPENAI_API_KEY` environment reference in `parallel_run.sh:8`, not a literal value; no provider token, JWT, private-key block, or cookie/auth-state object was present. `evaluation_harness/helper_functions.py` references the imported account map but adds no credential literal. No authentication or network request was attempted.

Exploit path: a reader of the retained source can obtain the static account values and pair them with the included login workflow. **[INFERENCE]** If any literals remain valid or are reused, this could permit access to the corresponding benchmark accounts; validity was not tested. The endpoint-bearing files additionally reveal internal benchmark endpoints and metadata-service usage.

Smallest remediation: remove the four exact source copies above from scratch; also remove/redact the metadata-endpoint YAML if endpoint disclosure is in scope. Revoke or rotate the account literals if they may be live. No files outside this report were changed.

At the initial follow-up scan, these source copies were present; the bounded final absence recheck below supersedes the pending-cleanup status.

## Final bounded absence recheck

Only the five previously flagged `FRevEnumerate/src` paths were checked, individually, for either a filesystem entry or symlink (`[ -e path ] || [ -L path ]`). All five checks returned ABSENT:

- `.ufo/waves/round-29/scratch/falsify/FRevEnumerate/src/browser_env/env_config.py`
- `.ufo/waves/round-29/scratch/falsify/FRevEnumerate/src/browser_env/auto_login.py`
- `.ufo/waves/round-29/scratch/falsify/FRevEnumerate/src/setup_env.sh`
- `.ufo/waves/round-29/scratch/falsify/FRevEnumerate/src/config_files/test.raw.json`
- `.ufo/waves/round-29/scratch/falsify/FRevEnumerate/src/webarena-map-backend-boot-init.yaml`

The bounded check agrees with `corpus/evidence/round29-calibration/credential-copy-removal.txt:2`. No broader scan was run. The receipt states that an earlier scratch commit still retains the copies and history was not rewritten; this recheck establishes final-tree absence only, not historical erasure.

VERDICT: PASS