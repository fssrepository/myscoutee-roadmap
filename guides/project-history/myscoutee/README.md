# Restorable Project history

Project snapshot checked 2026-10-17: 121 tasks. [Live Project](https://github.com/users/fssrepository/projects/2) · [Canonical complete backup](https://github.com/fssrepository/myscoutee-roadmap/tree/master/guides/project-history/myscoutee).

`project.json` preserves full issue bodies, statuses, typed field values and views. `measurements.json` preserves model/token/cost/time components and assumptions. `commit-map.json` links original and task-prefixed commit IDs. CSV/JSON provide convenient presentation exports. Recorded root intervals are retained in compressed JSON for timing reconstruction; there are no private chat texts.

## Validate offline

Run from the repository root:

```bash
python3 guides/project-history/myscoutee/restore_project.py
```

This validates all SHA256SUMS files and snapshot structure without network access.

## Recreate a deleted Project

Set `GITHUB_PROJECT_TOKEN` in your local shell to a credential with Projects write access. Run the same command with `--apply`. The script creates a new Project and restores task associations, fields, values, statuses and visible-column views; existing issues and source commits are preserved. Local progress is saved for retries. Use a separate `--state` file to create another copy. A repository subset restores only the tasks in that subset; use the complete backup to restore the whole Project.

If issues were deleted too, set `GITHUB_REPOSITORY_TOKEN` to an issue-write credential and add `--recreate-missing-issues`. The tracker repository must exist. Recreated issues may receive new issue numbers; stable task IDs remain. Historical execution dates remain in fields, while GitHub creation/closure timestamps reflect restoration.

Repository associations are included in `project.json`. Set `GITHUB_REPOSITORY_TOKEN` (or a suitable `GITHUB_TOKEN`) during restoration to reconnect them automatically. Separate Project-write and repository credentials are supported. Comments, automations and permission grants are outside this reconstruction. Read [METHOD.md](METHOD.md) for estimates, unknown values and measurement boundaries. Git versions these files; no dated folder is needed.

## Subsequent task measurements

The October 9 MSC-120/121 token update is retained in the existing
`measurements.json` `post_control_task_usage` ledger and in the live Project.
The 111-task calibration remains historical; the complete 121-task restoration snapshot also retains later task bodies and statuses. Mixed-session
attribution and exact measurement cutoffs are recorded beside each total.
The current README summary uses `current_project_totals`, merging measurements by
stable task ID. It includes MSC-114/115/116/117/118/119/120/121/122/123 once and preserves MSC-113 already present
in the historical total. The live Project currently tracks 121 tasks; all 121 have
measurements. The recovered MSC-114 initial batch is separate from later MSC-123 work.

## MSC-121 closeout

Closed / Project Done. Final deployment evidence is Helm 123; usage is recorded through 2026-10-09T15:12:03.126Z. The latest task components and intervals are in `measurements.json` under `post_control_task_usage`; these replace earlier checkpoints by task ID. Historical calibration totals remain frozen. The October-10 publication turn is excluded.

The canonical roadmap `commit-map.json` records the October-10 consolidation;
repository subset maps retain their earlier reconstruction boundary. Runtime
verification is the recorded October-9 evidence; the October-10 SSH check could
not reach the KVM and did not restart it.

Consolidated source commits: [backend `0941aac8`](https://github.com/fssrepository/myscoutee-backend/commit/0941aac8a700b7c2c6cc7aef2b4dda61fbd44d99) and [frontend `3601abd4`](https://github.com/fssrepository/myscoutee/commit/3601abd40a05c4746c2d57c62e0d15cc7392bba6). The 15 original commits map to these two in `commit-map.json`; the backend gitlink records the new frontend commit.

## MSC-122 closeout

Closed / Project Done. Original template/components 1.4.0 publication and exact DEB VMware verification remain accepted. October 17 template regression 1–32 PASS / CLOSED, including point 31 and cleanup; no new DEB installation is claimed. **1,304,324,997 tokens**, **46.917611 active / 46.804358 allocated hours**, through `2026-10-17T07:51:53.465Z`. The original 1,134,112,133-token delivery and 170,212,864-token regression increment are retained as components, counted once. Full API cost unavailable; $1,576.71 frozen known-rate subtotal only. Reproduce the increment with `measure-msc122-regression.py --cutoff 2026-10-17T07:51:53.465Z`. Corrections, reverted attempts and failure/recovery are included; final accounting/publication after cutoff excluded.

## MSC-115 closeout

Closed / Project Done through QA step 119. Usage through 2026-10-15T11:52:55.467000+00:00: **1,328,857,714 tokens**, **48.248381 active/allocated hours**, **$1,749.59 Standard API equivalent**. Exact response components, interval union, scope exclusions and attribution limits are in `post_control_task_usage`. Separate template/live qualification and compilation optimization do not reopen this closed scope.

The three final backend commits were consolidated into [`799918535`](https://github.com/fssrepository/myscoutee-backend/commit/799918535e832f3e77eee27cef9fb57f49a93c01) at the user’s request. The final tree and frontend gitlink are identical; the original-to-consolidated mapping is in `commit-map.json`. The optimization follow-up note remains separate in scope.

## MSC-116 closeout

Closed / Project Done for consolidated development QA through step85, including the remaining MSC-119 introduction. Exact usage, selected windows, exclusions and overlap allocation are in `measurements.json`; reproduce the recorded cutoff with `measure-msc116.py --cutoff 2026-10-15T20:52:03.159Z`. Template runtime and external-host/publication qualification remain separate. No duplicate MSC-119 measurement was added.

## MSC-117 closeout

Closed / Project Done for the accepted development scope. **105,282,015 tokens**, **5.206302 active/allocated hours** through `2026-10-16T09:26:30.000Z`. Reproduce with `measure-msc117.py --cutoff 2026-10-16T09:26:30.000Z`. Full API-equivalent cost is unavailable (missing gpt-6.1-sol rate); $79.41 is a known-rate subtotal only. [QA evidence and limits](https://github.com/fssrepository/myscoutee-backend/blob/7f12b02ec102440d042b923cbd86a28e9573c94d/guides/qa/evidence/general/MSC117-20261016/summary.json); template/live qualification stays separate.

## MSC-118 usage update

**182,287,382 tokens**, **4.680690 active / 4.369485 allocated hours**, **$242.00 frozen Standard API equivalent**, through `2026-10-16T14:49:00Z`. Includes implementation, checklist preparation, QA, shared-list corrections and reverted attempts. Reproduce with `measure-msc118.py --cutoff 2026-10-16T14:49:00Z`. Scoped eight-step guide QA is PASS / CLOSED; template regression 1–32 PASS / CLOSED on October 17, accounted under MSC-122.


## October 17 history consolidation

Consecutive task commits and the regression backup commits were consolidated; the MSC-120 backend sequence is one commit. `commit-map.json` retains original-to-consolidated identities. Application trees are preserved; the approved changes are concise README/accounting updates, fresh `/docs` artifacts from the existing `npm run build:github` command, plus the installer workflow’s existing supported-tag restriction. Existing release tags are unchanged. The refactor branch is integrated into master; the obsolete backend Pages site and branch are removed after preserving the current frontend demo.

## MSC-123 deployment/release update

MSC-123 complete: VMware/device scope closed; app/template signed 1.4.1 and Components registry published. Production Netcup upgraded from package 1.3.0 / frontend 1.3.3 to exact signed 1.4.1; host qualification, 13 public checks, Angular render and retained-data checks PASS. 347,361,510 tokens / 5.688961 allocated h through 2026-10-17T14:40:04.051000+00:00; shared allocation counted once. Full API cost unavailable. **5.688961 active / 5.688961 allocated hours**, 1,662 responses. Status: **Done**.

## Project metadata reconciliation

MSC-114 now retains all nine missing measurement fields for the isolated initial batch: **5,615,396 tokens**, **47 responses**, **0.199895 active/allocated h**, **$1.70 frozen API equivalent**, **gpt-6-sol / xhigh**, executed **1 October 2026**. Later security/dependency work remains allocated to MSC-123. MSC-121 Workstream is **QA and release**. Current totals include the recovered measurement once; historical calibration stays unchanged.

The requested documentation/metadata follow-up is folded into the existing MSC-123 commits: backend `756b9faf92edb65d327f1d3a621d01ba62a7bd76` and frontend `889d3281421b4a0a84f66e0866ced3ffd17ba7ac`. Six manuals now carry 1.4.1 internally and use stable filenames without version suffixes. The source mapping retains the preceding commit identities; signed release artifacts and existing tags retain their original identities.
