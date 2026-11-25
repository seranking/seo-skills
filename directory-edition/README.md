# Claude Plugins Directory edition

The Claude Plugins Directory accepts only Markdown, text, JSON, YAML and image files from organizations it hasn't verified, and it refuses plugins whose files read credentials from the user's machine or download and run code. This repo's GitHub edition needs its Python scripts, installers and examples, so the directory gets its own edition, built from the same files:

- `build.py` builds the edition into a folder outside the repo and checks it: file types, content sniffing with `file` (libmagic; Markdown it reads as HTML or Python counts as a refused type), `#!` lines, credential reads and credential-shaped names, download-and-run commands, MCP servers the plugin doesn't declare and references to files the edition doesn't ship. `test_build.py` covers the markers and the checks.
- `snippets/<id>.md` holds the text that replaces a marked block or line in the edition.
- `substitutions/<id>.md` holds exact-text replacements for places a marker can't go, such as lines inside a fenced report template (a marker there would show on GitHub and could be copied into a report). Each names a file, the text to find (which must occur exactly once) and its replacement; an empty replacement drops the line. When the source text changes, the build fails until the substitution is updated.
- `REWRITES` in `build.py` rewrites wording that repeats across many skills (Firecrawl tool names, "Firecrawl not installed", the Planable setup line). Each rule must still match somewhere, or the build fails.
- `overrides/` holds whole files that replace their GitHub-edition version (today: the `seo-google` pointer skill).
- `description.txt` is the plugin description the edition's manifests carry; the directory listing shows it.
- `.github/workflows/directory-edition.yml` publishes the edition of each release to the `claude-directory` branch; `release.yml` runs it after every release. The directory listing tracks that branch.
- The `validate` workflow runs the tests and builds the edition on every pull request, so a change the directory would refuse fails CI.

## MCP servers

The directory refuses text that tells Claude or the user to add an MCP server the plugin doesn't declare. The plugin declares only the SE Ranking server, so the edition sends users to the Firecrawl and Planable connectors in the Claude directory instead of firecrawl.dev or Planable's setup guide, and names Firecrawl's tools without the `mcp__firecrawl-mcp__` prefix (a connector's tools are named differently). The build refuses the old wording.

## Credential check

The directory holds a version when a file seems to read a credential from the user's machine. Its check reads a lowercase `pass` followed by text in backticks as the `pass` password manager when it stands where a shell command would start: at the start of a line, or after `;` or `(`. "Default off; pass `--no-firecrawl`" held v2.11.4. Say "use" or "set" instead; `build.py` refuses the wording.

## Markers

Markers carry only an id, so an agent reading the GitHub edition's raw Markdown sees no directory-only instructions. Each id is used once, and each snippet file must be used.

```
<!-- dir-edition:begin seo-page-gsc -->
4b. **GSC URL performance** … `python3 scripts/gsc_query.py …`
<!-- dir-edition:end seo-page-gsc -->
```

The block is replaced by `snippets/seo-page-gsc.md`. Use `remove` instead of `begin` to drop a block without a replacement. To swap a single line, such as a table row or a list item, add `<!-- dir-edition:line <id> -->` at the end of the line; the whole line is replaced by `snippets/<id>.md`. Never put a marker inside a fenced code block: use a substitution there. Outside fences, GitHub shows none of the markers. `{ref}` in a snippet becomes the released tag, and relative links to files the edition doesn't ship are rewritten to GitHub URLs at that tag.

The edition's marketplace description and keywords are set by `build.py` so nothing reads as an Anthropic or "official" listing.

## Releasing and the listing

1. Merge changes to `main` and cut a release (`release.yml`). The `directory-edition` job builds the release's edition and pushes it to `claude-directory`. The first release that contains this folder is v2.11.3; older tags can't be built.
2. Check that the job passed and that `claude-directory` holds the new version.
3. An owner of the Claude organization that holds the listing (SE Ranking GTM) selects **Check for new commits** on the listing, reads the Review tab and, when the version passes, selects **Publish** (or **Publish update**). An Anthropic reviewer then approves it. The person who publishes needs a GitHub account connected in that organization with push access to this repo.

The first time only: the owner sets the listing's **Tracked branch or tag** to `claude-directory` on its Settings tab, after step 2. The branch can't be changed while the plugin is with a reviewer.

Edition-only fixes ship in a new patch release. The workflow refuses to publish different content under a version the branch already holds, or an older version, unless it is run with `force`.

## Checking a build against the directory before a release

The listing's Review tab names a file but not the reason. The submission form does, and it submits nothing:

1. Build the edition and push it to a temporary branch.
2. In the developer portal (claude.ai/directory/manage), select **Submit new**, then **Plugin bundle**. Enter the repository and the branch, then select **Validate**. Don't continue past the Source step.
3. Expand a finding to read why each file was flagged. The three name findings and the "Already in your submissions" note appear only because the form treats the build as a new plugin.
4. Delete the temporary branch.

## Building it locally

```bash
python3 directory-edition/test_build.py
python3 directory-edition/build.py --out /tmp/seo-skills-directory-edition
cd /tmp/seo-skills-directory-edition && claude plugin validate . --strict
```
