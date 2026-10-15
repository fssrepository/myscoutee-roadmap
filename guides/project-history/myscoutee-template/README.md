# MyScoutee Template Project

[Live Project](https://github.com/users/fssrepository/projects/6) · [Backend](https://github.com/fssrepository/myscoutee-template) · [Frontend](https://github.com/fssrepository/myscoutee-template-frontend)

The shared MSC-122 issue tracks template 1.4.0 and components delivery. The Project uses the same typed fields and two views as MyScoutee: **Delivery history** and **AI usage and effort**.

Usage belongs to the existing [MSC-122 measurement](../myscoutee/measurements.json); this Project does not add another allocation to portfolio totals.

`project.json` preserves the issue, field values, repository associations and views. Validate locally with `python3 guides/project-history/myscoutee-template/restore_project.py`. To recreate a deleted Project, use the same restore procedure as [MyScoutee](../myscoutee/README.md). Credentials and restoration state stay outside Git.
