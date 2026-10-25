# Combined token activity

The README chart is generated from `account-coverage.json`. It shows combined
daily tokens, including cached input, from February through October 25, 2026 (latest returned day, partial).
It does not split the presentation by account or allocate usage to projects.

The same JSON preserves the daily input series under the account-name initials
`r`, `m`, and `s` for reproducibility. Full account identifiers are not published.
The JSON is supporting data in a public repository, not a private store.

Run from the repository root with Python 3 and Inkscape installed:

```bash
python3 guides/statistics/render_heatmap.py
```

This validates the daily total and writes `media/token-activity.svg` and a
double-resolution `media/token-activity.png`. The SVG contains a date and exact
token count in each recorded cell's tooltip. Weeks start on Monday. Five blue
bands mean positive usage up to 10 million, 100 million, 500 million, 1 billion,
and above 1 billion tokens. Gray means no recorded usage or an explicit zero;
missing records do not establish that no work occurred.

The chart is a measured usage inventory, independent of task estimates. Do not
add its total on top of task budgets: session-derived task estimates may
already include the same usage. Task usage is recorded separately and is never summed into this daily ledger.

The October 9 refresh preserves all original account and combined rows through
September 30 byte-for-value, then appends the available account `r` daily rows
for October 1–8. No fresh rows for `m` or `s` are available; missing coverage is
not zero usage. A later account report revised September 30, but that revision
is explicitly recorded as excluded in `coverage_notes` to preserve the requested
historical baseline.

The October-10 refresh corrects only the October-8 account `r` value from
220,793,037 to 416,565,655. The combined chart is now 42,358,256,064 tokens.
October 9 is available (140,711,289 tokens) and is included as requested on
October 10; the latest account lifetime is reported separately.

The October-12 refresh updates available October account `r` records through October 12. Combined total: 43,348,498,790; account `r` lifetime: 41,101,926,589. Every September row remains unchanged.

The October-15 refresh updates available October account `r` records through October 14. Combined total: 44,361,700,648; account `r` lifetime: 42,115,128,447. October 15 has no returned daily bucket. Historical September and other-account series remain unchanged.

The October-17 refresh updates available October account `r` records through October 16. Combined total: 45,088,868,957; account `r` lifetime: 42,842,296,756. October 17 has no returned daily bucket. September and other-account series remain unchanged.

The October-18 refresh adds the newly returned October-17 account `r` bucket:
**286,940,919 tokens**. Combined daily total: **45,375,809,876 tokens**;
current account lifetime: **43,129,237,675 tokens**. All earlier daily rows,
including September and the other accounts, remain unchanged. No October-18
daily bucket was returned. The account reading includes the later September-30
correction; the combined chart preserves its historical baseline.

The README distinguishes the current account's lifetime usage from the combined
three-account daily ledger. **B = billion (1,000,000,000); M = million (1,000,000).**
These overlapping totals include cached input and must not be added together
or to project/task measurements.

The October-24 refresh updates returned October account `r` buckets through October 23. Combined daily total: **47,302,979,678 tokens**; current account lifetime: **45,056,407,477 tokens**. September and other-account rows are preserved. No October-24 bucket or separate ChatGPT conversation-token total was returned. Missing coverage is not zero and no usage is inferred.

The October-25 refresh updates returned October account `r` buckets through October 25 (partial day). Combined daily total: **48,136,489,900 tokens**; current account lifetime: **45,889,917,699 tokens**. September and other-account rows are preserved. The report is Codex account usage; no independent ChatGPT conversation-token total is available or inferred.
