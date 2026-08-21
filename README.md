# interactive-questionnaire

English | [简体中文](README.zh-CN.md)

> An Agent Skill that turns an agent's scattered follow-up questions into structured questionnaires (plain-text or interactive HTML) with machine-parsable JSON answers.

![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)
![Release](https://img.shields.io/github/v/release/duskykitecn/interactive-questionnaire)
![Agent Skills](https://img.shields.io/badge/Agent_Skills-compatible-4B57D6)

## What this is

When an agent needs your preferences, requirements, or a decision, the default is to ask as thoughts occur: questions scattered across turns, answers as prose. That is tiring to fill in and hard to parse reliably.

This skill routes **every** question the agent would ask you onto one of two tracks:

- **Simple → plain text**: numbered questions (`1.` `2.`) and lettered options (`a.` `b.`), each with a short note on why it is asked, what it decides, and a recommended choice. Reply like `1: a,c`.
- **Complex → interactive HTML**: the agent assembles a form from a built-in template and 12 components (single/multi select, reveal toggles, sliders, ranges, steppers, text, ranking, and so on). You fill it in, click Copy result, and paste structured JSON back.

Once this skill is invoked, it stays in effect for the rest of the conversation. A silent end-of-turn check catches questions that slipped back into free-form chat and restates them in the required format.

## Demo

The same `demo.html` is served in three places:

- China: https://static.duskykite.com.cn/interactive-questionnaire/
- International: https://static.duskykite.xyz/interactive-questionnaire/
- GitHub Pages: https://duskykitecn.github.io/interactive-questionnaire/

All 12 components, light/dark theme, objections, “answer in text instead”, and result JSON. After a push to `main`, this repo’s GitHub Pages updates on its own; the custom hostnames are served from the org `static` hub under `/interactive-questionnaire/`. Maintainer setup is in [PUBLISHING.md](PUBLISHING.md) (Chinese). You can also open [`interactive-questionnaire/assets/demo.html`](interactive-questionnaire/assets/demo.html) locally.

## Install

This is an [Agent Skills](https://agentskills.io) package: a folder that contains `SKILL.md`. Install it by copying that folder into the host app’s skills directory (the path usually includes `skills`), or by uploading it through the app’s skill import UI.

Copy the **nested** `interactive-questionnaire/` folder (the one with `SKILL.md`), not the whole git repo.

### Skills directory

User-level (all projects for the current account), using common host apps as examples:

```bash
git clone https://github.com/duskykitecn/interactive-questionnaire.git

# Cursor
mkdir -p ~/.cursor/skills
cp -r interactive-questionnaire/interactive-questionnaire ~/.cursor/skills/

# Claude Code
mkdir -p ~/.claude/skills
cp -r interactive-questionnaire/interactive-questionnaire ~/.claude/skills/
```

Project-level (shared with a team): copy into whatever directory that app documents, e.g. `.cursor/skills/` or `.claude/skills/`. Other Agent Skills hosts use their own folder names; the copy is the same.

On Windows, replace `~` with `%USERPROFILE%`.

### Upload a package

Some hosts only accept an archive. The archive root must be the skill folder (`interactive-questionnaire/SKILL.md`). Use the `.zip` if the upload UI does not accept `.skill`.

China (does not go through GitHub):

- `.skill`: https://static.duskykite.com.cn/interactive-questionnaire/releases/latest/interactive-questionnaire.skill
- `.zip`: https://static.duskykite.com.cn/interactive-questionnaire/releases/latest/interactive-questionnaire.zip

International:

- `.skill`: https://static.duskykite.xyz/interactive-questionnaire/releases/latest/interactive-questionnaire.skill
- `.zip`: https://static.duskykite.xyz/interactive-questionnaire/releases/latest/interactive-questionnaire.zip

GitHub Releases carry the same files: https://github.com/duskykitecn/interactive-questionnaire/releases/latest

Build locally:

```bash
python scripts/package.py
```

On claude.ai, upload under **Settings → Capabilities** in the Skills section (plan and code-execution requirements apply; custom skills are usually account-scoped). The Claude API uses `POST /v1/skills`, then the returned `skill_id`.

## Usage

- **Enable**: name `interactive-questionnaire` in the conversation, or use `/interactive-questionnaire` where the host supports slash commands. After that, every question the agent needs to ask you goes through this skill.
- **Plain-text answers**: lettered choices (several letters for multi-select, e.g. `1: a,c`); free-text questions as ordinary sentences.
- **HTML form**: fill each field (every field can switch to free text or record an objection), then Copy result and paste the JSON back.
- **Result JSON**: one entry per question — `answer` (control value, plus `dirty` if you changed the default), `custom` (free text), or `objection`. A `system` object holds theme and display/fold mode. The contract is in [`interactive-questionnaire/SKILL.md`](interactive-questionnaire/SKILL.md).
- **Stop**: tell the agent to stop using this skill.

## Layout

```
interactive-questionnaire/            ← repo root
├── README.md                         ← this file
├── README.zh-CN.md                   ← Simplified Chinese
├── LICENSE
├── CHANGELOG.md                      ← Keep a Changelog
├── PUBLISHING.md                     ← maintainer handbook (release + GitHub/Gitee/CNB)
├── scripts/
│   ├── package.py                    ← local packager (Python 3 stdlib only)
│   ├── build_site.py                 ← flatten demo.html to /project-name/
│   └── write_release_body.py         ← GitHub Release notes (China / international URLs)
├── .github/workflows/
│   ├── release.yml                   ← v* tag → GitHub Release + static hub packages
│   ├── deploy-site.yml               ← optional: push demo into duskykitecn/static
│   └── sync-mirrors.yml              ← optional GitHub→mirror push (off; CNB uses .cnb.yml)
├── .cnb.yml                          ← CNB mirror: cron git-sync from GitHub
└── interactive-questionnaire/        ← the skill (this is what you install)
    ├── SKILL.md                      ← routing, text convention, assembly, JSON contract
    ├── assets/
    │   ├── template.html             ← HTML questionnaire shell
    │   └── demo.html                 ← all-component demo
    └── references/
        ├── components.md             ← component registry
        └── snippets/                 ← 12 component HTML snippets
```

## Local packaging

```bash
python scripts/package.py          # version from the latest CHANGELOG.md entry
python scripts/package.py 1.2.0    # or pass a version
```

Output lands in `dist/`: `interactive-questionnaire-vX.Y.Z.skill` and a `.zip` with the same contents.

## Versioning and release

Versions follow SemVer; notable changes go in [CHANGELOG.md](CHANGELOG.md). Pushing a `vX.Y.Z` tag packs the skill, attaches `.skill` / `.zip` to the GitHub Release, and copies those files onto the `static` hub. The full maintainer flow is in [PUBLISHING.md](PUBLISHING.md) (Chinese).

Repositories:

- GitHub (canonical): https://github.com/duskykitecn/interactive-questionnaire
- Gitee (mirror): https://gitee.com/duskykite/interactive-questionnaire
- CNB (mirror): https://cnb.cool/DuskyKite/interactive-questionnaire

## License

[CC BY-NC 4.0](LICENSE): copy, adapt, and redistribute with attribution and a note of changes; **no commercial use**. Ask the author for a commercial license. The legal text is on [Creative Commons](https://creativecommons.org/licenses/by-nc/4.0/).
