# Reconstructable AI-assisted engineering history

Four separate Projects preserve distinct work. MyScoutee system repositories share one Project; the legacy archive, e-kozig and math each have their own.

The current summary combines the October 1 reconstruction with the measured MSC-120/121 follow-ups through **2026-10-09T15:12:03.126Z**. The initial template/licensing/components turns and this October-10 accounting/publication turn are excluded from MSC-121. The task count comes from the live Project checked October 10. Usage is task allocation, not the account balance.

| Project | Tracked tasks | Tasks with measurements | Tokens (M), estimated | Allocated activity (h) | API equivalent (USD), estimated |
| --- | ---: | ---: | ---: | ---: | ---: |
| [MyScoutee](https://github.com/users/fssrepository/projects/2) | 120 | 113 | 37,113.1 | 931.9 | $28,005.06 |
| [MyScoutee Old](https://github.com/users/fssrepository/projects/3) | 6 | 6 | 3.4 | 0.2 AI; manual unknown | $5.43 |
| [E-Kozig](https://github.com/users/fssrepository/projects/4) | 16 | 16 | 457.8 | 9.5 | $260.28 |
| [Millennium Math Problems](https://github.com/users/fssrepository/projects/5) | 18 | 18 | 1,286.0 | 43.5 | $727.68 |

**Current recorded task allocation: 38,860,229,159 tokens.** MyScoutee has 120 tracked tasks, of which 113 have usage measurements. MSC-114–119 and the planned MSC-122 have no isolated usage measurement yet; they are excluded, not counted as zero. Other Projects retain their October 1 measurement boundaries. MSC-113 is counted once; MSC-120/121 include their latest checkpoint rather than both old and new totals. The current aggregate is reproducible from [the measurement ledger](guides/project-history/myscoutee/measurements.json) by task ID.

Activity includes tool/network waits and is not human labor. Costs are Standard API equivalents, not invoices. Task allocation and account usage below overlap and must never be added together.

<details>
<summary>Preserved October 1 reconstruction</summary>

The following allocation table is the historical reconstruction through October 1, 2026; it is not the current account balance.

| Project | Tasks | Tokens (M), estimated | Allocated activity (h) | API equivalent (USD), estimated |
| --- | ---: | ---: | ---: | ---: |
| [MyScoutee](https://github.com/users/fssrepository/projects/2) | 111 | 36,285.0 | 890.9 | $26,863 |
| [MyScoutee Old](https://github.com/users/fssrepository/projects/3) | 6 | 3.4 | 0.2 AI; manual unknown | $5 |
| [E-Kozig](https://github.com/users/fssrepository/projects/4) | 16 | 457.8 | 9.5 | $260 |
| [Millennium Math Problems](https://github.com/users/fssrepository/projects/5) | 18 | 1,286.0 | 43.5 | $728 |

Historical estimated token allocation across the listed AI work: **38,032,141,411**. The measured usage inventory below is a separate control total, not an amount to add to project budgets. Activity time includes tool/network waits; it is not human labor time. Legacy manual effort is unknown and excluded from numeric totals. USD is a standardized API list-price comparison, not a subscription invoice or amount paid.

The original reconstruction covered 11 source repositories and 226 consolidated source commits. That reconstruction contained 151 tasks; the live tracker also contains subsequent work. The task issue records share this public tracker for stable references, while their Project boards and totals are separate. Source repository visibility is unchanged.

</details>

## Current task measurements

MSC-121 is Closed / Project Done, including the final Helm-123 Mongo StatefulSet,
change-stream/cache freshness, Kubernetes status/SSE and blocking Redis telemetry
follow-ups. The final reader passed 28 focused tests and live cursor checks; no
post-reader CPU improvement or fresh full monolith/browser E2E is claimed.

The MSC-120 domain comparison and original MSC-121 playground qualification are recorded;
the unchanged historical image replay also shows no later-source regression.
The local response audit and stability repairs pass 134 Angular service tests. Project fields include the following measured
checkpoint, with mixed-conversation allocation explicitly estimated:

| Task | Tokens (M) | Active h | Allocated h | Standard API equivalent |
| --- | ---: | ---: | ---: | ---: |
| [MSC-120](https://github.com/fssrepository/myscoutee-roadmap/issues/158) | 193.714624 | 10.634 | 10.588 | $252.63 |
| [MSC-121](https://github.com/fssrepository/myscoutee-roadmap/issues/159) | 634.373124 | 30.467 | 30.421 | $889.43 |

Both tasks started October 7; qualification was recorded October 9. Models and
reasoning are read from the response metadata (GPT-6 Astra and GPT-6.1 Sol;
high/xhigh as recorded per task). The live Project and aggregate ledger retain
exact cutoffs, token components and task-interval boundaries. Time includes tool
waits; overlapping intervals between these two tasks are allocated once. The
Standard short-context cost normalization matches the existing method, with
[official rates](https://developers.openai.com/api/docs/models/compare) checked October 10.
It is not a subscription invoice. Later work is excluded until the next refresh.
These rows are included once in the current project summary above. The historical
reconstruction and account daily totals remain separate and unchanged.

## Earlier release checkpoint

[MSC-113: Granular profile ratings, fractional affinity and v1.3.3 release](https://github.com/fssrepository/myscoutee-roadmap/issues/151)
is complete. Home/Activities UI and rate sync/save/reload are verified. Two
images are deployed to Netcup; migration011 uses the shared DEB migration chain.
No DEB was built. All eight containers are healthy; six retained their identity.
Measured work through 2026-10-01T02:49:50.004Z: **28,648,921 tokens**, **1.369555 h**,
**$42.63 estimated Standard API equivalent**, gpt-6-astra / xhigh and high.
Includes implementation, QA, commits, migration, packaging, deployment and the
verifier follow-up (3/3 regressions and13/13 public checks). Final
accounting writes after cutoff cannot be self-counted. The October-1 task is
counted once; the historical allocation control and heatmap values through September 30 remain unchanged. The chart now also includes the available October records.

## Measured token activity

**Latest account `r` lifetime: 40,111,683,863 tokens (40.112B)**, reported October 10, 2026. This replaces 38.488B as the current account reading; that older value remains only in the historical calibration. The combined chart below also includes the two other retained account series and preserves its original September rows.

**42,358,256,064 tokens** in the combined daily record, through October 9, 2026. Darker blues indicate higher daily usage.

![Combined daily AI token usage, shown as a blue calendar heatmap](guides/project-history/media/token-activity.png)

[SVG](guides/project-history/media/token-activity.svg) · [PNG](guides/project-history/media/token-activity.png) · [Anonymous daily totals](guides/project-history/account-coverage.json) · [Regenerate the chart](guides/project-history/HEATMAP.md)

This measured usage total is separate from the estimated task allocation above. Additional measurements may already overlap local task evidence, so they are not added again to task budgets, activity hours or API-equivalent costs. The chart preserves every recorded value through September 30 and appends October 1–9 from the available account `r` record; newer records for the other two accounts are unavailable. The October-10 refresh revises the October-8 account `r` value from 220,793,037 to 416,565,655. October 9 now has a reported bucket of 140,711,289 and is included in the chart. Task usage is never inserted into provider daily buckets. The chart uses combined daily totals. Supporting JSON preserves the input series using account-name initials only; full account identifiers are not published.

## Restore from Git

- [myscoutee backup](guides/project-history/myscoutee/README.md)
- [myscoutee-old backup](guides/project-history/myscoutee-old/README.md)
- [e-kozig backup](guides/project-history/e-kozig/README.md)
- [math backup](guides/project-history/math/README.md)

Each source repository also has a `guides/project-history/` snapshot. Complete per-Project snapshots here and compact repository-specific copies preserve issue bodies, fields, values, view definitions, token/model/time ledgers, attribution assumptions and commit mappings. No chat history is needed. Git records versions; no date-named folder is used.

## Measurement method


- Local active and archived `.codex` histories are the primary execution evidence. All 649 JSONL files were inventoried, including split conversations; the history database was checked for additional coverage. Local retained conversations start on July 22, while account daily records reach February 4.
- Reuse the existing production audit method: unique response IDs when available; positive cumulative-counter differences for older records; unchanged counters contribute nothing; an initial partial counter or reset contributes only its recorded last response. Approval-review histories are not counted as extra user work. Cached input is inside input; reasoning output is inside output.
- Reuse the frozen September 12 film/book audit without changing its 14 phase totals: **2.295 billion logged tokens**, including the separately identified product campaign. Its cutoff excludes that audit's own work. Those tokens are reserved before allocating other account activity, so they are not counted twice.
- For other tasks, date/topic evidence from original commits and conversation requests supplies allocation weights. The daily account totals are control totals. Task splits remain estimates, particularly for mixed conversations and work before local history retention. Unrelated or unsupported activity remains unassigned. 189.2 M tokens for tasks without isolated daily evidence are comparable-task estimates reserved from the unassigned account balance; their daily attribution is unavailable.
- Active time follows the existing audit's union of recorded task intervals, so overlapping root intervals are not added twice. It includes tool execution and waiting within active tasks and is not a human timesheet. Missing AI timing is estimated from comparable observed work. Manual legacy work has no time estimate; archive dates do not establish its original development period. Frozen creative tasks also retain their 15–30 minute joint-window estimates.
- Historical start/finish fields describe when the work happened. GitHub issue creation/closure dates describe this retrospective import. A historical Done record is evidence of delivered work, not a claim that the current software was retested during import.
- Logged model/effort values take precedence. When missing, the creator's stated preference for the strongest available Codex model is combined with release dates: GPT-5.3-Codex from February 5, GPT-5.4 from March 5, GPT-5.5 from April 23, GPT-5.6 Sol from July 9, GPT-6 Astra from September 3. These are explicitly estimated selections; quota-driven fallbacks and rollout timing may differ. Missing reasoning effort remains unrecorded.
- USD estimates use [OpenAI's Standard API rates](https://developers.openai.com/api/docs/pricing), valued on 2026-10-01, for input, cached input, cache writes when observed, and output. Missing token mix is estimated from observed sessions. This standardized short-context comparison excludes Fast/Ultrafast, long-context and regional uplifts, subscription charging, infrastructure, and image/video/TTS-provider credits. It is not historical billing reconciliation.

Model date sources: [GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex/), [GPT-5.4](https://openai.com/index/introducing-gpt-5-4/), [GPT-5.5](https://openai.com/index/introducing-gpt-5-5/), [GPT-5.6](https://openai.com/index/gpt-5-6/), [GPT-6 Astra](https://openai.com/index/safety-overview-gpt-6-astra/).


- Four independent Projects separate MyScoutee, the manually developed legacy archive, e-kozig and mathematical research. Shared account tokens are allocated once across all four; a Project total is never an additional account total. Historical legacy AI usage is unverified and left blank. The current AI-assisted Project-administration task is measured separately. A final shared maintenance-run measurement is apportioned by snapshot ownership; its overlap with MSC-108 is removed and its net allocation uses the unassigned account allowance, without exact daily billing reconciliation.
- Mathematical experiments and videos do not establish a solution of the continuous Navier–Stokes problem. The claim withdrawal is a first-class task.

- Combined daily usage is published as anonymous totals only. The original task calibration remains separate: additional measurements may overlap existing task evidence and are not automatically added to task tokens, hours or costs.

## Reconstruction tools

The [history helper archive](guides/history-tools/README.md) preserves the source scripts and workflow notes used for the reconstruction. It excludes backup bundles, credentials and private conversation extracts.

## Task identifiers

MSC, OLD, EKO and MATH IDs are stable task identifiers. Commit bodies link their actual issue numbers; task ID numbers need not equal GitHub issue numbers. Mixed commits retain their contents and can refer to several tasks. Release/archive tags retain their original targets.

## License

This repository is licensed under the [GNU Affero General Public License v3.0](LICENSE).
