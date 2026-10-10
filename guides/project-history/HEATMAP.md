# Combined token activity

The README chart is generated from `account-coverage.json`. It shows combined
daily tokens, including cached input, from February through October 9, 2026.
It does not split the presentation by account or allocate usage to projects.

The same JSON preserves the daily input series under the account-name initials
`r`, `m`, and `s` for reproducibility. Full account identifiers are not published.
The JSON is supporting data in a public repository, not a private store.

Run from the repository root with Python 3 and Inkscape installed:

```bash
python3 guides/project-history/render_heatmap.py
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
