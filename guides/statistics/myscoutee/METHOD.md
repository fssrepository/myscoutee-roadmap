# Measurement method


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

## MSC-113 measurement boundary

All MSC-113 work through 2026-10-01T02:49:50.004Z is included: implementation, QA, commits,
Project/roadmap administration, migration, packaging and v1.3.3 Netcup release.
28,648,921 tokens from 227 unique response IDs; 1.369555 active task hours,
including tool waits but excluding the gap between turns; estimated $42.63
using the frozen 2026-10-01 Standard rate card. Cached input is inside input;
reasoning is inside output. Final accounting writes after the stated cutoff
cannot be self-counted. These are not human hours or an invoice.

Backend/frontend snapshots share one task; no measured repository split is
claimed. The historical account control and September-30 heatmap remain frozen.
October-1 usage is recorded in `post_control_task_usage` and counted once in task
totals, without consuming the historical unassigned-account allowance. Canonical
commit mappings are in the roadmap backup to avoid self-referential source SHAs.


## MSC-115 measurement boundary (October 15 refresh)

The post-control ledger includes planning/implementation from October 2 through the October 6 MCP handoff, then the October 12–15 MSC-115 QA and closure conversations plus two guide subagents. Three archived segments of the first conversation are deduplicated by response ID. Only records matching their own thread ID count, excluding inherited parent history. Token and time scope excludes later MSC-116/118/119 work, unrelated README editing, separate frontend/cache/watcher investigation and the isolated compilation-optimization documentation response.

Active hours are the union of recorded root task intervals, with unfinished turns clipped at their final measured response and idle gaps excluded. Parallel child tokens count once; child time is not added on top of the parent. The isolated optimization response's elapsed interval is an attribution estimate. Selected intervals do not overlap the already measured MSC-120/121/122 intervals; unknown overlap with unmeasured work is not claimed resolved. The task stops at the accounting request (2026-10-15T11:52:55.467Z); this publication cannot self-count its final writes. The existing October 1 API-equivalent rates remain frozen.

Account lifetime tokens and combined daily series are separate overlapping views of task usage. The account API does not expose lifetime active hours: leave it unavailable, not zero or inferred from tokens. Its longest-turn statistic is not an aggregate duration.

## MSC-119 final measurement and consolidation

MSC-119 is closed; its remaining QA is owned by MSC-116. 47,314,132 tokens
from 330 unique responses, 2.125719 active hours,
2.114473 allocated hours and $72.06 API equivalent,
through 2026-10-15T19:28:57.277Z. The October 1 rates remain frozen.

`measure-msc119.py` reproduces the aggregate from retained local Codex histories
and the existing ledger, without network access or mutation. It uses explicit
request-boundary windows: October 7 implementation, publication preparation and
consolidation (excluding the abandoned architecture request), October 15 dedicated
MSC-119 checklist work and closure preparation. Source hashes identify threads
without publishing conversation IDs or text. Only each source's own response IDs
count. Mixed-task attribution remains an estimate; no full-session totals are
copied into both tasks. Recorded root intervals are clipped at these boundaries
and united, excluding idle gaps. Previously recorded other-task intervals retain
their allocation; the 0.011246 overlapping hours are
removed from MSC-119's incremental allocated time. Unmeasured-task overlap is not
claimed resolved. Final accounting writes after the cutoff are excluded.

MSC-116 stays open and its measurements are unchanged. Its execution QA is excluded
from this closed MSC-119 allocation. No future accounting revisit is required for
the transferred QA.

## MSC-117 measurement boundary

Measured unique response usage; task attribution follows explicit request windows. Includes initial October6 WebRTC implementation, same-thread MCP/dev startup and call-guide follow-up before the general guide-introduction request, October16 delegated QA/corrections/closure preparation, and the separate October16 synthetic-audio explanation. Original and continued archive segments are joined by thread identity and response IDs deduplicated. Excludes later mixed general-guide/role work, template baseline qualification already credited elsewhere, and final publication after cutoff. Root active intervals are unioned across overlapping threads; tool waits count, idle gaps do not. Previously allocated other-task time is subtracted. No claim of complete overlap attribution against unmeasured tasks. Cached input is within input and reasoning within output. Frozen Standard API-equivalent valuation is an estimate, not an invoice.

Cutoff `2026-10-16T09:26:30.000Z`: 105,282,015 tokens / 840 unique responses / 5.206302 unioned active and allocated hours. Archived continuation segments are deduplicated by response ID. Full cost is null because gpt-6.1-sol has no frozen ledger rate; known-rate subtotal $79.41 only is added to the current project valuation, explicitly marked incomplete. Existing MSC-119 extraction remains byte-equivalent as JSON under its original defaults.

## MSC-118 measurement boundary

182,287,382 tokens from 1343 unique response IDs through 2026-10-16T14:49:00Z. The explicit source windows in `measure-msc118.py` cover October7 implementation, October15 checklist reconciliation before MSC-119, and October16 QA with associated shared-list work and corrections. Reverted work is consumed effort and remains included. The 4.680690 root active hours are a union, not a sum of overlapping agents; 0.311205 hours already allocated elsewhere are removed, leaving 4.369485 allocated hours. The $242.00 estimate uses the existing frozen rate card. Account controls and the account heatmap are not changed by a task-level update. Publication after cutoff is excluded.

## MSC-122 regression increment

Use `measure-msc122-regression.py --cutoff 2026-10-17T07:51:53.465Z` for the two dedicated October 15–17 QA root threads. Deduplicate response IDs, union recorded root intervals and subtract overlaps already allocated to other tasks using the existing extractor. The aggregate replaces MSC-122 by task ID, retaining the October 12 delivery and the new regression as separate components. Include corrections, reverted attempts and failure/recovery; exclude accounting/publication after cutoff. The Template Project is another view of the same task, never a second allocation. Missing model rates remain unpriced; preserve the original frozen delivery valuation separately.

## MSC-123 deployment measurement

Reproduce with `measure-msc123.py --cutoff 2026-10-17T14:40:04.051000+00:00`. Explicit source/request windows, archived-segment response deduplication and active-interval union reuse the existing extractor. The cutoff is the last selected measured response before final accounting. Includes app/template release work, Components publication, requested template VMware installation, canonical publication verification and the requested Netcup production upgrade, corrections and failed attempts; excludes preceding template QA/closeout and bookkeeping after the cutoff. One shared allocation across five source repositories. No frozen gpt-6.1-sol rate exists; full valuation remains null. MSC-123 completed on 2026-10-17 after Netcup host, public, render and retention checks passed.

## MSC-114 initial CodeQL measurement

The isolated 1 October root session is selected from 05:00:25.000Z through 05:13:54.393Z. Reproduce with the canonical roadmap `measure-msc114.py`, which reuses `measure-msc119.py` for response-ID deduplication, component accounting, interval union and previous-allocation exclusion. 5,615,396 tokens / 47 responses; 0.199895 active and allocated hours. Frozen gpt-6-sol Standard API rates yield $1.70; no new price lookup or billing claim. Later licence/publication turns and all MSC-123 alert/dependency work are excluded. Full task measurement is stored only as a shared allocation, never added across repository subsets.


## MSC-126 measurement boundary

Reproduce with `measure-msc126.py --cutoff 2026-10-21T23:51:01Z`. Two dedicated root histories and their archived segments use the existing response-ID extractor. 288,442,597 tokens / 1,513 responses / 9.919969 active and 9.919969 allocated hours. Includes consumed implementation, corrections and reverted attempts, focused checks, applicable template/components work, migration, VMware, consolidation/publication and Netcup deployment through cutoff. Root intervals are unioned; prior allocations are subtracted. Tool/build/network waits count, idle gaps and final accounting writes do not. No child sessions were found for the selected roots. Cached input remains inside input and reasoning inside output. Full cost is null because the frozen rate card lacks the observed models; no new rates or billing inference. Template Project is a second view of this same allocation. MSC-125 remains unmeasured. Historical calibration, account controls and account heatmap are unchanged.

## MSC-127 measurement boundary

Measured unique response usage across 17 selected root histories; task attribution follows explicit requests and the consolidated MSC-127 delivery. Includes landing diagnostics, Lighthouse follow-up, shared modules, Sonar, packaging, documentation/QA reorganization, releases, runtime checks, corrections and reverted attempts. Mixed Sonar windows exclude initial e-kozig work and its isolated Pages publication. Excludes separate advertising analysis, Higgsfield lookup, prior MSC-126 accounting, and MSC-128 work from 2026-10-24T13:18:13.614Z onward. Root active intervals are unioned, tool waits included, idle gaps excluded, and previously allocated task time subtracted. Task attribution of mixed windows is an estimate. Cached input is inside input and reasoning inside output. Shared repository work is allocated once. Account totals and ChatGPT usage are separate overlapping views, never added to this measurement. Missing frozen model rates remain unpriced. Closure transfers outstanding qualification to MSC-128 and does not assert it passed.

Cutoff `2026-10-24T13:18:13.613Z`: 1,237,840,553 tokens from 6,744 responses; 30.687602 unioned active hours, 30.291569 allocated hours. Reproduce with `measure-msc127.py`; source hashes and exact windows are retained in the measurement. Final closure/accounting writes are outside this cutoff.

## October 24 missing-field reconciliation

The official [Standard API pricing table](https://developers.openai.com/api/docs/pricing), verified 24 October 2026, supplies the missing **gpt-6.1-sol** short-context rates per million tokens: **$2 input / $0.10 cached input / $10 output / $2.50 30-minute cache write**. `supplemental_rates_per_million` records this separately from the frozen October 1 rate card. Previously priced components retain their original valuation; `valuation_supplement` preserves the formerly unpriced token components and known subtotal. This completes MSC-117/122/123/124/126/127; earlier text describing unavailable costs records the pre-supplement state. API equivalent is a comparable estimate, not actual ChatGPT/Codex subscription billing; no speed, long-context or regional uplift is inferred.

MSC-125 is recovered with `measure-msc125.py` from its dedicated root session: **20 October 2026, 08:41:34.758–22:53:55.173 UTC**, **266,804,531 tokens**, **1,526 unique responses**, **8.059066 active/allocated hours**. The existing extractor deduplicates response IDs, unions active intervals and excludes idle gaps and already allocated overlaps. Separate traffic/marketing reports and MSC-124 sessions are excluded. Recovery/publication work is outside this historical measurement.

Current totals are derived from the merged task records by stable task ID. Partial later checkpoints preserve earlier measured fields, including MSC-113; historical calibration is unchanged. Account totals overlap task measurements and are not added. **MSC-128 remains unmeasured until completion**, at the owner's request.
