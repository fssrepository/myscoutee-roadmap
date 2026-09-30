# Delivery history and project backups

Four separate Projects preserve distinct work. MyScoutee system repositories share one Project; the legacy archive, e-kozig and math each have their own.

| Project | Tasks | Tokens (M), estimated | Allocated activity (h) | API equivalent (USD), estimated |
| --- | ---: | ---: | ---: | ---: |
| [MyScoutee](https://github.com/users/fssrepository/projects/2) | 108 | 36,249.2 | 889.2 | $26,809 |
| [MyScoutee Old](https://github.com/users/fssrepository/projects/3) | 6 | 3.4 | 0.2 AI; manual unknown | $5 |
| [E-Kozig](https://github.com/users/fssrepository/projects/4) | 16 | 457.8 | 9.5 | $260 |
| [Millennium Math Problems](https://github.com/users/fssrepository/projects/5) | 18 | 1,286.0 | 43.5 | $728 |

Account-wide measured tokens: **38,488,016,278**, through September 30, 2026. Estimated allocation across listed AI work: **37,996,385,327**; remaining unassigned: **491,630,951**. Activity time includes tool/network waits; it is not human labor time. Legacy manual effort is unknown and excluded from numeric totals. USD is a standardized API list-price comparison, not a subscription invoice or amount paid.

11 source repositories, 226 consolidated source commits, and 148 retrospective tasks. The task issue records share this public tracker for stable references, while their Project boards and totals are separate. Source repository visibility is unchanged.

## Restore from Git

- [myscoutee backup](myscoutee/README.md)
- [myscoutee-old backup](myscoutee-old/README.md)
- [e-kozig backup](e-kozig/README.md)
- [math backup](math/README.md)

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

## Task identifiers

MSC, OLD, EKO and MATH IDs are stable task identifiers. Commit bodies link their actual issue numbers; task ID numbers need not equal GitHub issue numbers. Mixed commits retain their contents and can refer to several tasks. Release/archive tags retain their original targets.
