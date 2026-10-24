# MyScoutee Template Project

[Live Project](https://github.com/users/fssrepository/projects/6) · [Backend](https://github.com/fssrepository/myscoutee-template) · [Frontend](https://github.com/fssrepository/myscoutee-template-frontend)

Shared MSC-122 tracks template 1.4.0 delivery; MSC-123 tracks the shared 1.4.1 fixes and publication. The Project uses the same typed fields and two views as MyScoutee: **Delivery history** and **AI usage and effort**.

Usage belongs to the existing [MSC-122 measurement](../myscoutee/measurements.json); this Project does not add another allocation to portfolio totals.

`project.json` preserves the issue, field values, repository associations and views. Validate locally with `python3 guides/statistics/myscoutee-template/restore_project.py`. To recreate a deleted Project, use the same restore procedure as [MyScoutee](../myscoutee/README.md). Credentials and restoration state stay outside Git.

MSC-122 usage: **1,304,324,997 tokens** through **2026-10-17T07:51:53.465Z**, including the original delivery and **170,212,864** regression tokens. Template regression **1–32 PASS / CLOSED**, including point 31 and cleanup. The [shared task](https://github.com/fssrepository/myscoutee-roadmap/issues/160) and both Projects use this same total; full API cost is unavailable.

MSC-123: signed template **1.4.1 installed and smoke-tested on VMware**, five Docker images published; [release](https://github.com/fssrepository/myscoutee-template/releases/tag/v1.4.1) is published with verified signatures, all nine matching assets and canonical public discovery. Components **1.4.1** is published to GitHub Packages and GitHub Releases. Main MyScoutee 1.4.1 is published and canonical discovery verified. The shared task has **347,361,510 tokens / 5.688961 allocated h** through `2026-10-17T14:40:04.051000+00:00`; counted once in the canonical MyScoutee ledger.

MSC-123 is **Done** after the requested production Netcup 1.4.1 upgrade and verification passed.

## MSC-126 release and deployment

Shared MSC-126 is Done for applicable template 1.4.5 source/images/standalone artifacts. No new template-host install is claimed. MSC-126 release batch complete: main/template loading groups and semantic captions, preferred-language/cache startup, guarded WebP/catalog/demo-lifecycle migrations, fullscreen mobile setup. Five v1.4.5 source releases/tags, five GHCR images and Components 1.4.5 published. Netcup 13/13 public checks; nine healthy containers; seven production users and original media retained. VMware verified. Installed DEBs remain 1.4.1. No matched Lighthouse gain or new template host qualification claimed. 288,442,597 tokens / 9.919969 allocated h through 2026-10-21T23:51:01Z; shared template/component effort counted once. Full API valuation unavailable.

**9.919969 active / 9.919969 allocated hours**, **1,513 responses**. Reproduce with `measure-msc126.py --cutoff 2026-10-21T23:51:01Z`. Usage is counted once in the canonical [MyScoutee measurement ledger](../myscoutee/measurements.json). [Release](https://github.com/fssrepository/myscoutee-backend/releases/tag/v1.4.5) · [Task](https://github.com/fssrepository/myscoutee-roadmap/issues/164). Remaining Lighthouse priorities await a new matched report. Historical account totals remain frozen; final accounting after cutoff is excluded.
