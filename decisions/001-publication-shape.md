---
adr: 001
title: "Publish under CC BY 4.0 with the thread transcripts kept out of history"
status: accepted
date: 2026-09-13
deciders: [Mike]
consulted: [Johnny, Warren, Ark, CC]
informed: []
depends_on: []
related: [ADR-002]
supersedes: []
session: DPC Research group thread, 2026-09-13 06:22–07:31 UTC
---

## Context and Problem Statement

The folder was created as a record and will become a public repository: private first, public
later, English throughout at the moment it opens (Mike, 06:46 UTC). Three things in the record
did not fit that: the licence had not been chosen; half of the folder by character count is
Russian because it is verbatim (`idea.md`, `chat/`); and the idea's transcript carries a
second voice's review whose provenance was not written down.

## Decision Drivers

- **Nothing in the repository is code.** It is notes, verified quotes, a reading list and one
  third-party PDF. A code licence would raise a question a reader should not have to ask.
- **The transcripts are evidence, not a publication.** Their value is that they are verbatim
  — who said what, in what order, including the errors and their corrections. A translated
  transcript is a retelling and cannot be cited as the record.
- **A repository that goes public later cannot un-publish its history.** A private branch
  that was ever pushed survives in reflogs and forks.
- **A quote carries its source.** The team's own standard, restated by Johnny in review.

## Decision

**Licence: CC BY 4.0** (Mike, 06:55 UTC; MIT considered first at 06:49 and withdrawn on
Johnny's and Warren's objection that MIT is a code licence). The one redistributed artefact,
the PNAS paper in `sources/`, is itself CC BY 4.0 (its first page: *"This open access article
is distributed under Creative Commons Attribution License 4.0 (CC BY)"*), so repository and
artefact carry the same licence.

**`chat/` is excluded via `.gitignore` from the first commit** (Mike, 06:50 UTC): the
transcripts never enter git history. They stay on disk locally as the record. Every link into
`chat/` from a published file is replaced by a plain attribution — name, role, date, UTC — so
the information survives and the link does not.

**`idea.md` is published as a marked translation** with the Russian original beside it.

### Rationale

CC BY 4.0 matches the content type and the artefact already inside the repository. Ignoring
`chat/` rather than branching it is the only mechanism that gives "never in history" as a
property instead of a promise. Plain attributions are what the README already carries; the
links were a convenience for the private folder, not information.

## Considered Options

- **MIT** — proposed first; a code licence for a repository without code. Withdrawn.
- **CC0** — also a text standard; not chosen, attribution is wanted.
- **`chat/` on a private branch** — rejected: a pushed branch is recoverable; gitignore is not
  a branch.
- **Translate `chat/`** — rejected: the translation would no longer be the record.

## Consequences

- **Positive:** the public repository is a clean, English, licensed set of documents whose
  every finding is attributed by name and time.
- **Negative:** a public reader cannot check the team against its own primary source. The
  repository does not promise that to a public reader.
- **Neutral:** the `.gitignore` also carries the scratch patterns; nothing else is excluded.

## Open Questions

- **Q1:** The **attribution string** for CC BY 4.0 — who is named as author. The README
  currently names Mike and three agents by role. — Mike
- **Q2:** The **second voice inside `chat/67`**. By the transcript's own attribution lines all
  three entries are `Mike Shevchenko`; Mike stated (06:53 UTC) he showed the idea to Grok, so
  the review is a model's output pasted by him — his to publish, but unnamed in the current
  README and `idea.md`. Name it as *Grok, 2026-09-12, shown the idea by Mike*, or drop it from
  the public version. CC's recommendation: drop — every point in it is either superseded by
  the reviews or wrong. — Mike

## Scope

- `LICENSE` — CC BY 4.0 text, with Q1's string. Not yet written.
- `.gitignore` — `chat/` plus scratch patterns. Done, `8695d26`.
- `README.md`, `literature.md`, `idea.md` — thirteen links into `chat/` to become attributions.
  Not yet done.
- `idea.md` — translation with the original kept. Not yet done.

## Authors

- **Mike** — Decision
- **Johnny, Warren** — the licence objection and the transcript-privacy point
- **Ark** — the transcript provenance check
- **CC** — measurement of what is Russian by character (50.5 % of the folder; README 0.5 %,
  `literature.md` 1.0 %, `idea.md` 62.4 %, `chat/` 70–95 %), the `.gitignore`, this record
