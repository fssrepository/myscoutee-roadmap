# History reconstruction tools

Source archive of the helpers used to consolidate Git histories and reconstruct
the portfolio's GitHub Projects. The scripts preserve how the work was done and
provide starting points for processing other repositories or accounts.

**These are historical scripts, not a ready-to-run pipeline.** Personal home paths use `/home/USER` placeholders; repository names, dated input
files, task mappings and measurement cutoffs are retained. Some create Git commits or refs,
rewrite history, push changes, or mutate GitHub Projects and issues. Review and
adapt a selected script and its inputs before executing it; do not run every
script in directory order or import scripts just to inspect them.

## Contents

| Folder | Purpose |
| --- | --- |
| [cleanup-small](cleanup-small/) | Initial history consolidation and publication for the smaller MyScoutee repositories. |
| [cleanup-main](cleanup-main/) | Backend/frontend inventory, consolidation planning, preservation and verification. |
| [cleanup-extra](cleanup-extra/) | Additional repository downloads and cleanup; migration of backup branches to archive tags. |
| [reconstruction](reconstruction/) | Usage extraction, task attribution, time and cost estimates, GitHub publication and restorable Project snapshots. |

[catalog.json](catalog.json) records every archived script's original workspace
folder, role, byte count and SHA-256 hash. Personal home paths have been anonymized; hashes describe the archived copies.
Earlier variants and one-time correction scripts remain labeled as historical
references, so they cannot be mistaken for additional steps in the final flow.

## Main workflow references

| Stage | Starting points | Inputs and outputs |
| --- | --- | --- |
| Inspect Git history | `cleanup-main/audit.py`, the cleanup `build_plan.py` and `prepare.py` scripts | Repository refs and commit inventories; generated plans and consolidation mappings. |
| Extract account/session usage | `reconstruction/read-account-usage.py`, `extract-usage.py`, `extract-additional.py`, `merge-history.py` | Authorized account access and local Codex SQLite/JSONL records; private usage extracts. |
| Build tasks and estimates | `reconstruction/build-tasks.py`, `time-totals.py`, `prepare-public.py` | Commit mappings, session/account extracts and the earlier production audit; task records and labeled estimates. |
| Publish Project tasks | `reconstruction/publish-portfolio.py`, `github_api.py` | Prepared/final task JSON and saved identity state; GitHub issues, items and fields. |
| Preserve Project records | `reconstruction/backup-portfolio.py` | Final task/state/summary JSON and commit mappings; the versioned Project snapshots. |
| Link repositories and verify views | `reconstruction/link-projects.py`, `finalize-views.py` | Project/repository IDs and field definitions; associations, views and read-back checks. |

The names describe the original workflow, not a supported command sequence.
For example, `extract.py` contains an earlier combined extractor, while
`extract-usage.py` includes the later unique-response accounting path.
`scope-correction.py`, `refine-builder.py`, `rename-projects.py`, `amend-*.py`
and the maintenance/documentation accounting helpers were specific corrections
or bounded recording steps. Replaying them against current data can undo later
decisions or count effort twice.

## Reusing the methods

1. Work from a separate copy of the needed helpers, outside this source archive.
2. Replace the original absolute paths, repository/account identities, task
   mappings, time windows and pricing assumptions for the new investigation.
   Several helpers infer the workspace from their own directory; simply moving
   or executing them here does not adapt those paths.
3. Inventory the selected script's input files before running it. Intermediate
   JSON, original cleanup manifests and raw session extracts are deliberately
   not bundled with these sources. They must be regenerated or supplied from
   the authorized private workspace. The existing Project snapshots preserve
   published results, not every intermediate extractor input.
4. Use the installed Git, Python and Codex tools appropriate to that workflow.
   The scripts primarily use Python's standard library; account extraction
   relies on the local Codex app-server interface and history schema used at
   the time. API/schema assumptions may need adapting.
5. Configure credentials locally. The historical GitHub helper reads the Git
   credential store and a local Projects token file; no credential values are
   included. Confirm the chosen account before publishing.
6. Inspect generated allocations and diffs before any publication or history
   rewrite. Keep recorded usage separate from estimates, unknown historical
   human effort, and API list-price equivalents.

## Preserved elsewhere

For restoring the existing Projects, use the maintained
[Project snapshots and restore tools](../project-history/README.md). Those
contain the published tasks, measurements, fields, views and repository links;
they do not depend on this helper archive or retained conversations.

This archive excludes Git `.bundle` backups, compressed worktree backups,
raw conversations, extracted prompts, credentials, generated inventories,
daily commit reports, publication logs and Python caches. The original local
workspace folders have not been moved or deleted. `backup.py` and similarly
named scripts are included because they are source code describing a process,
not the large backup artifacts themselves.
