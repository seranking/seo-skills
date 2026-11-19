# Claude Plugins Directory edition

The Claude Plugins Directory accepts only Markdown, text, JSON, YAML and image files from organizations it hasn't verified, and it refuses plugins whose files read credentials from the user's machine or download and run code. This repo's GitHub edition needs its Python scripts, installers and examples, so the directory gets its own edition, built from the same files:

- `build.py` builds the edition into a folder outside the repo and checks it: file types, content sniffing with `file` (libmagic; Markdown it reads as HTML or Python counts as a refused type), `#!` lines, credential reads, download-and-run commands and references to files the edition doesn't ship. `test_build.py` covers the markers and the checks.
- `snippets/<id>.md` holds the text that replaces a marked block or line in the edition.
- `overrides/` holds whole files that replace their GitHub-edition version (today: the `seo-google` pointer skill).
- `description.txt` is the plugin description the edition's manifests carry; the directory listing shows it.
- `.github/workflows/directory-edition.yml` publishes the edition of each release to the `claude-directory` branch; `release.yml` runs it after every release. The directory listing tracks that branch.
- The `validate` workflow runs the tests and builds the edition on every pull request, so a change the directory would refuse fails CI.

## Markers

Markers carry only an id, so an agent reading the GitHub edition's raw Markdown sees no directory-only instructions. Each id is used once, and each snippet file must be used.

```
<!-- dir-edition:begin seo-page-gsc -->
4b. **GSC URL performance** … `python3 scripts/gsc_query.py …`
<!-- dir-edition:end seo-page-gsc -->
```

The block is replaced by `snippets/seo-page-gsc.md`. Use `remove` instead of `begin` to drop a block without a replacement. To swap a single line, such as a table row or a list item, add `<!-- dir-edition:line <id> -->` at the end of the line; the whole line is replaced by `snippets/<id>.md`. GitHub shows none of the markers. Relative links to files the edition doesn't ship are rewritten to GitHub URLs at the released tag.

## Releasing and the listing

1. Merge changes to `main` and cut a release (`release.yml`). The `directory-edition` job builds the release's edition and pushes it to `claude-directory`. The first release that contains this folder is v2.11.3; older tags can't be built.
2. Check that the job passed and that `claude-directory` holds the new version.
3. An owner of the Claude organization that holds the listing (SE Ranking GTM) selects **Check for new commits** on the listing, reads the Review tab and, when the version passes, selects **Publish** (or **Publish update**). An Anthropic reviewer then approves it. The person who publishes needs a GitHub account connected in that organization with push access to this repo.

The first time only: the owner sets the listing's **Tracked branch or tag** to `claude-directory` on its Settings tab, after step 2. The branch can't be changed while the plugin is with a reviewer.

Edition-only fixes ship in a new patch release. The workflow refuses to publish different content under a version the branch already holds, or an older version, unless it is run with `force`.

## Building it locally

```bash
python3 directory-edition/test_build.py
python3 directory-edition/build.py --out /tmp/seo-skills-directory-edition
cd /tmp/seo-skills-directory-edition && claude plugin validate . --strict
```
