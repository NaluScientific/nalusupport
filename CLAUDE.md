# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Jekyll 4.4 site for support.naluscientific.com, on Ruby 3.4 (see `.ruby-version`). The theme is a vendored copy of Just the Docs 0.5.1 with Nalu customizations in `_layouts`, `_includes`, `_sass` and `assets`. There is no test suite or linter. A successful `jekyll build` is the only check.

`.github/workflows/build.yml` builds every push and pull request and uploads `_site` and the resolved `Gemfile.lock` as artifacts. On `main` it builds from the committed lockfile (frozen) and deploys to GitHub Pages. Without local Ruby, push a branch and inspect the artifacts with `gh run download`. To upgrade gems, change the `Gemfile`, push, and commit the `gemfile-lock` artifact.

Sass compiles with Dart Sass. `_config.yml` silences the `import`, `global-builtin` and `color-functions` deprecations from the vendored theme. Don't add new uses of these, or `/` division, in Nalu-owned SCSS.

Every root file not listed under `exclude` in `_config.yml` gets published. Add new tooling files to that list.

## Commands

```sh
bundle install
bundle exec jekyll serve --livereload   # dev server at http://localhost:4000
bundle exec jekyll build                # build into _site/

# Docker, no local Ruby needed. Live reload does not work with volume mounts on Windows.
docker build -t nalusupport .
docker run --rm -p 4000:4000 -v "$(pwd):/site" nalusupport

# Python maintenance scripts (pip install -r requirements.txt)
python update_naluscope_ver.py v0.24.1  # version must start with "v"
```

## Architecture

Most content changes are YAML edits in `_data/`, not page edits. Pages under `pages/` are front-matter stubs that pick a layout and a data key. The layout renders the tables from `site.data`.

| Data file | Layout | Page front-matter key | Rendered as |
|---|---|---|---|
| `_data/board.yml` | `_layouts/board.html` | `model:` | Per-board downloads: firmware, NaluScope manuals, quick start guides, product sheets |
| `_data/software.yml` | `_layouts/software.html` | `product:` | Software downloads per OS (`windows`, `linux`, `appimage`) |
| `_data/documentation.yml` | `_layouts/documentation.html` | `product:` | NaluDAQ manuals |
| `_data/guides.yml` | `_layouts/guides.html` | none | Flat list of guide PDFs |

Each product key has `current:` and `archived:` lists. To release a new version, move the old entry from `current` to the top of `archived` and add the new one to `current`. Board and documentation entries are `{name, url}`. Software entries are `{name, date, downloads: {os: url}}`.

The update scripts rewrite `board.yml`, `software.yml` and `guides.yml` with `yaml.dump`, which sorts keys alphabetically (`archived` before `current`) and normalizes formatting. Match that style in hand edits so script runs don't produce noisy diffs.

Jekyll ignores files in `pages/` that start with `_`, such as `pages/_firmware.md` and `pages/board/_upac-i.md`. They are unpublished.

## Update scripts and automation

- `update_naluscope_ver.py <tag>` archives the current NaluScope entry in `software.yml` and adds the new one with release URLs from `NaluScientific/NaluScope-Release`. It does the same for the "Manual" entry of every board in `board.yml`. The new manual URL reuses the board segment of the existing one (`NaluScope.X.Y.Z.-.<BOARD>.User.Manual.pdf`), so each board needs a manual entry in that format.
- `.github/workflows/update_naluscope.yml` runs weekly on Fridays. When the latest NaluScope-Release tag differs from `software.yml`, it runs the script above and opens and auto-merges a PR on branch `naluscope-<tag>`. Manual NaluScope bumps can race with it.
- `update_qs_docs_ver.py`, `update_product_docs_ver.py` and `update_guides_docs_ver.py` export Google Docs to PDF, upload them to a shared Drive folder and write the Drive links into `board.yml` or `guides.yml`. The doc IDs are in each script's `DOCUMENTS` dict. Entries are matched by exact name: `"Quick Start Guide (PDF)"`, `"Product Sheet (PDF)"` or the guide `name`. The scripts call `drive_utils.authenticate()`, an interactive OAuth flow that needs `credentials.json` from Google Cloud Console in the repo root. Never commit that file.
- `board_docs.py` is the service-account variant, run by the manually triggered `.github/workflows/board_docs.yml`.

## Conventions

Commit messages start with a type prefix: `ADD:`, `CHG:`, `FIX:`, `UPD:` or `DEL:`. Examples: `ADD: DSA-C10-8 FW v185`, `ADD: NaluScope v0.24.1`.
