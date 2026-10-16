# Restorable Project history

Project snapshot checked 2026-10-16: 120 tasks. [Live Project](https://github.com/users/fssrepository/projects/2) · [Canonical complete backup](https://github.com/fssrepository/myscoutee-roadmap/tree/master/guides/project-history/myscoutee).

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
The 111-task calibration remains historical; the complete 120-task restoration snapshot also retains later task bodies and statuses. Mixed-session
attribution and exact measurement cutoffs are recorded beside each total.
The current README summary uses `current_project_totals`, merging measurements by
stable task ID. It includes MSC-115/116/117/119/120/121/122 once and preserves MSC-113 already present
in the historical total. The live Project currently tracks 120 tasks; 118 have
measurements. MSC-114 and MSC-118 remain unmeasured, not zero-cost tasks.

## MSC-121 closeout

Closed / Project Done. Final deployment evidence is Helm 123; usage is recorded through 2026-10-09T15:12:03.126Z. The latest task components and intervals are in `measurements.json` under `post_control_task_usage`; these replace earlier checkpoints by task ID. Historical calibration totals remain frozen. The October-10 publication turn is excluded.

The canonical roadmap `commit-map.json` records the October-10 consolidation;
repository subset maps retain their earlier reconstruction boundary. Runtime
verification is the recorded October-9 evidence; the October-10 SSH check could
not reach the KVM and did not restart it.

Consolidated source commits: [backend `0941aac8`](https://github.com/fssrepository/myscoutee-backend/commit/0941aac8a700b7c2c6cc7aef2b4dda61fbd44d99) and [frontend `3601abd4`](https://github.com/fssrepository/myscoutee/commit/3601abd40a05c4746c2d57c62e0d15cc7392bba6). The 15 original commits map to these two in `commit-map.json`; the backend gitlink records the new frontend commit.

## MSC-122 closeout

Closed / Project Done. Template and shared components 1.4.0 are published. The exact published template DEB was verified on VMware. Usage through 2026-10-12T18:56:15.981Z is recorded in `post_control_task_usage`: 1,134,112,133 tokens, 43.898 active/allocated hours and $1,557.73 Standard API equivalent. Earlier template planning excluded from MSC-121 is included here once.

## MSC-115 closeout

Closed / Project Done through QA step 119. Usage through 2026-10-15T11:52:55.467000+00:00: **1,328,857,714 tokens**, **48.248381 active/allocated hours**, **$1,749.59 Standard API equivalent**. Exact response components, interval union, scope exclusions and attribution limits are in `post_control_task_usage`. Separate template/live qualification and compilation optimization do not reopen this closed scope.

The three final backend commits were consolidated into [`799918535`](https://github.com/fssrepository/myscoutee-backend/commit/799918535e832f3e77eee27cef9fb57f49a93c01) at the user’s request. The final tree and frontend gitlink are identical; the original-to-consolidated mapping is in `commit-map.json`. The optimization follow-up note remains separate in scope.

## MSC-116 closeout

Closed / Project Done for consolidated development QA through step85, including the remaining MSC-119 introduction. Exact usage, selected windows, exclusions and overlap allocation are in `measurements.json`; reproduce the recorded cutoff with `measure-msc116.py --cutoff 2026-10-15T20:52:03.159Z`. Template runtime and external-host/publication qualification remain separate. No duplicate MSC-119 measurement was added.

## MSC-117 closeout

Closed / Project Done for the accepted development scope. **105,282,015 tokens**, **5.206302 active/allocated hours** through `2026-10-16T09:26:30.000Z`. Reproduce with `measure-msc117.py --cutoff 2026-10-16T09:26:30.000Z`. Full API-equivalent cost is unavailable (missing gpt-6.1-sol rate); $79.41 is a known-rate subtotal only. [QA evidence and limits](https://github.com/fssrepository/myscoutee-backend/blob/7f12b02ec102440d042b923cbd86a28e9573c94d/guides/qa/evidence/general/MSC117-20261016/summary.json); template/live qualification stays separate.
