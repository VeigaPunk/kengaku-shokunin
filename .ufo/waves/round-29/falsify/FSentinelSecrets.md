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

VERDICT: PASS