# MyScoutee delivery history

A public retrospective of the MyScoutee system and its related creative work: application features, quality assurance, deployment, integrations, books, films and promotional assets.

The record covers **9 source repositories, 197 consolidated commits and 109 reconstructed tasks**. Source repositories keep their existing visibility. This repository contains curated task summaries and aggregate measurements, not private conversations or private source code.

[Open the delivery Project](https://github.com/users/fssrepository/projects/2) · [Browse tasks](https://github.com/fssrepository/myscoutee-roadmap/issues?q=is%3Aissue) · [Download task metrics](tasks.csv)

## Recorded scale

| Measure | Value |
| --- | ---: |
| Account tokens, 2026-02-04 through 2026-09-30 | **38,488,016,278** |
| Account daily records | **167** |
| Tokens allocated to listed tasks, estimated | **36.72 billion** |
| Account tokens still unassigned | **1.77 billion** |
| Standard API list-price equivalent of listed tasks | **approximately $27,183 USD** |

The account total is measured account-wide activity. It includes repeatedly processed context and is not a count of original words produced. The task allocation and USD value are retrospective estimates. The USD value is **not the amount paid for a ChatGPT subscription**, a provider invoice, or a proven monetary saving.

## Measurement method

- Local active and archived `.codex` histories are the primary execution evidence. All 649 JSONL files were inventoried, including split conversations; the history database was checked for additional coverage. Local retained conversations start on July 22, while account daily records reach February 4.
- Reuse the existing production audit method: unique response IDs when available; positive cumulative-counter differences for older records; unchanged counters contribute nothing; an initial partial counter or reset contributes only its recorded last response. Approval-review histories are not counted as extra user work. Cached input is inside input; reasoning output is inside output.
- Reuse the frozen September 12 film/book audit without changing its 14 phase totals: **2.295 billion logged tokens**, including the separately identified product campaign. Its cutoff excludes that audit's own work. Those tokens are reserved before allocating other account activity, so they are not counted twice.
- For other tasks, date/topic evidence from original commits and conversation requests supplies allocation weights. The daily account totals are control totals. Task splits remain estimates, particularly for mixed conversations and work before local history retention. Unrelated or unsupported activity remains unassigned. 107.2 M tokens for tasks without isolated daily evidence are comparable-task estimates reserved from the unassigned account balance; their daily attribution is unavailable.
- Active time follows the existing audit's union of recorded task intervals, so overlapping root intervals are not added twice. It includes tool execution and waiting within active tasks and is not a human timesheet. Missing timing is estimated from comparable observed work. Frozen creative tasks also retain their 15–30 minute joint-window estimates.
- Historical start/finish fields describe when the work happened. GitHub issue creation/closure dates describe this retrospective import. A historical Done record is evidence of delivered work, not a claim that the current software was retested during import.
- Logged model/effort values take precedence. When missing, the creator's stated preference for the strongest available Codex model is combined with release dates: GPT-5.3-Codex from February 5, GPT-5.4 from March 5, GPT-5.5 from April 23, GPT-5.6 Sol from July 9, GPT-6 Astra from September 3. These are explicitly estimated selections; quota-driven fallbacks and rollout timing may differ. Missing reasoning effort remains unrecorded.
- USD estimates use [OpenAI's Standard API rates](https://developers.openai.com/api/docs/pricing), valued on 2026-10-01, for input, cached input, cache writes when observed, and output. Missing token mix is estimated from observed sessions. This standardized short-context comparison excludes Fast/Ultrafast, long-context and regional uplifts, subscription charging, infrastructure, and image/video/TTS-provider credits. It is not historical billing reconciliation.

Model date sources: [GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex/), [GPT-5.4](https://openai.com/index/introducing-gpt-5-4/), [GPT-5.5](https://openai.com/index/introducing-gpt-5-5/), [GPT-5.6](https://openai.com/index/gpt-5-6/), [GPT-6 Astra](https://openai.com/index/safety-overview-gpt-6-astra/).

## Task identifiers and Git history

`MSC-N` corresponds to issue `#N` here. Commit subjects reference their relevant task IDs and commit bodies link the public issues. A mixed commit can reference several tasks. Task grouping changes commit metadata, not the application file contents; existing release tags continue to identify their original commits.

The public [CSV](tasks.csv) and [JSON](tasks.json) are presentation exports. Raw conversations, credentials, local machine paths and private evidence remain local. Individual issue descriptions distinguish frozen measurements from estimates.
