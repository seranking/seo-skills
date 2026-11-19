# Claude Plugins Directory edition

The Claude Plugins Directory accepts only Markdown, text, JSON, YAML and image files from organizations it hasn't verified, and it refuses plugins whose files read credentials from the user's machine or download and run code. This repo's GitHub edition needs its Python scripts, installers and examples, so the directory gets its own edition, built from the same files:

- `build.py` builds the edition into a folder and checks it: file types, `#!` lines, credential reads, download-and-run commands and references to files the edition doesn't ship.
- `overrides/` holds whole files that replace their GitHub-edition version (today: the `seo-google` pointer skill).
- `.github/workflows/directory-edition.yml` publishes the edition of each release to the `claude-directory` branch. `release.yml` runs it after every release, and you can run it by hand with a release tag. The directory listing tracks that branch.
- The `validate` workflow builds the edition on every pull request, so a change the directory would refuse fails CI.

## Marking text that only one edition has

In any Markdown file, wrap text the directory edition must not ship, and add what it ships instead:

```
<!-- dir-edition:remove -->
- Run `python3 scripts/gsc_query.py …`
<!-- dir-edition:end -->
<!-- dir-edition:only
- Search Console data isn't available in this edition; skip this step.
-->
```

GitHub shows neither marker, and the `only` text stays hidden there. Relative links to files the edition doesn't ship are rewritten to GitHub URLs.

## Building it locally

```bash
python3 directory-edition/build.py --out /tmp/seo-skills-directory-edition
cd /tmp/seo-skills-directory-edition && claude plugin validate . --strict
```
