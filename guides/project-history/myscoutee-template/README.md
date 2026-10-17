# MyScoutee Template Project

[Live Project](https://github.com/users/fssrepository/projects/6) · [Backend](https://github.com/fssrepository/myscoutee-template) · [Frontend](https://github.com/fssrepository/myscoutee-template-frontend)

The shared MSC-122 issue tracks template 1.4.0 and components delivery. The Project uses the same typed fields and two views as MyScoutee: **Delivery history** and **AI usage and effort**.

Usage belongs to the existing [MSC-122 measurement](../myscoutee/measurements.json); this Project does not add another allocation to portfolio totals.

`project.json` preserves the issue, field values, repository associations and views. Validate locally with `python3 guides/project-history/myscoutee-template/restore_project.py`. To recreate a deleted Project, use the same restore procedure as [MyScoutee](../myscoutee/README.md). Credentials and restoration state stay outside Git.

MSC-122 usage: **1,304,324,997 tokens** through **2026-10-17T07:51:53.465Z**, including the original delivery and **170,212,864** regression tokens. Template regression **1–32 PASS / CLOSED**, including point 31 and cleanup. The [shared task](https://github.com/fssrepository/myscoutee-roadmap/issues/160) and both Projects use this same total; full API cost is unavailable.
