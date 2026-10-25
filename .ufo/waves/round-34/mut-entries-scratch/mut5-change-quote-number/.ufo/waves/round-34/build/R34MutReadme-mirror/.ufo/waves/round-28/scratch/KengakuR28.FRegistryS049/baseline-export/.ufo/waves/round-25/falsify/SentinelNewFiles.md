ATTACKS: round-25 changed-file secret/account sweep
Severity: LOW — private-network endpoint literals and one account identifier disclosed; no credential secret observed.
Exploit path: A repository reader can collect the historical private endpoint references for internal network reconnaissance and use the account identifier for targeted impersonation. No live endpoint requests were made.
Evidence (path:line — class only):
.ufo/waves/round-25/build/ProvinceScout.md:15 — private endpoint
.ufo/waves/round-25/build/SentinelReceipts.md:32 — private endpoint
LOG.md:7 — private endpoint
LOG.md:9 — private endpoint
LOG.md:11 — private endpoint
LOG.md:14 — private endpoint
LOG.md:15 — account identifier
PROVINCE.md:14 — private endpoint
PROVINCE.md:114 — private endpoint
PROVINCE.md:156 — private endpoint
SCORECARD.md:65 — private endpoint
SCORECARD.md:212 — private endpoint
SKILL.md:342 — private endpoint
SKILL.md:620 — private endpoint
SKILL.md:642 — private endpoint
corpus/README.md:35 — private endpoint
corpus/README.md:39 — private endpoint
corpus/README.md:41 — private endpoint
Impact: Internal topology disclosure and account-targeting data; current endpoint reachability is unverified.
Smallest remediation: Replace endpoint literals and account identifiers in committed docs/reports with neutral placeholders; keep originals only in access-restricted evidence.
VERDICT: BREAKS — private endpoint and account-identifier disclosure; no credential/token or active op:// reference found. Installs: none.
