# Lessons from the ART report, for this repository

Not a review of the biology. This note reads one outside report the way we read our own runs,
to see which mistakes it shows that we could make here. Sources: Yoon, Athukoralage, Ameisen,
Kauderer-Abrams, Perry, Durrant, "Autonomous AI agents discover reverse transcriptases with
tandem repeat arrays" (Anthropic preprint PDF,
<https://www-cdn.anthropic.com/22573675ada52a8ca8a97a1a4b4326b2f208a071.pdf>, read in full via
`pdftotext`), and the news post "Claude discovers a novel enzyme system with CRISPR-like repeats"
(<https://www.anthropic.com/news/claude-discovers-novel-enzyme-system>, Sep 23, 2026).
Quotes below are verbatim from those two text extractions, each with its page (report) or "news".

## 1. What the report is

Anthropic ran an autonomous multi-agent harness (Claude Mythos 5) over 1.9 billion protein
clusters to survey reverse transcriptase (RT) loci and their neighbor genes. One agent, reading
raw DNA text rather than running a tool, noticed a tandem repeat array upstream of an RT in a
jumbo phage, with a partner gene downstream — a family they named array-associated RTs (ART).
Function is not shown: the array is transcribed into short, abundant RNAs during phage infection,
resembling a CRISPR-like architecture, but what the system does is not established. The news post
states this directly: "Our work to understand the primary function of ARTs is ongoing."

## 2. The lessons

### a. Selection after seeing the data

What they did, p.40: *"The two shown were chosen from these 12 after the flank had been
examined: the signal labeled automatically as 'tokens repeating an earlier pattern/text
verbatim' (repeat-signal 1), and the signal labeled as 'letters in repeated DNA/protein sequence
motifs, and garbled text' (repeat-signal 2)."* The twelve candidates were fixed by a rule before
the flank was examined (same page); the choice of the two shown from them was made after.

Why it is a trap: a pair picked once the answer is known looks diagnostic whatever it carries, so
it cannot also count as evidence for the answer. The report states the order openly; the step
that follows the look is the one that no longer tests anything.

For us: this is exactly the FlyWire P3 headline-rank problem. In that run the registered
headline was r = 1, and it happened to sit exactly where the two arms' rank profiles crossed
(`docs/plans/2026-09-24-flywire-bf-p3-registration.md`; outcome note
`docs/notes/2026-09-24-flywire-p3-what-it-showed.md` §4). The rule for choosing
the headline rank for question (ii) — transfer — must be written and registered before the run,
not read off after seeing which rank looks best.

### b. A null that cannot see the other world

What they did, p.38 (Methods, "Replicate campaigns"): the campaign was rerun ten times, and
*"All task records (n = 3,084), reports, and session transcripts (n = 5,632) of the replicates
were searched for identifiers from the original campaign... An ART locus on a contig outside this
identifier set would not be found by this search."* The Results text then states, p.10: *"none
read the DNA upstream of the RTs, and the array was missed in every rerun."*

Why it is a trap: "missed in every rerun" sounds like a measured reproducibility rate, but the
search could only ever find the *original* locus under its *original* identifiers. A rediscovery
under a different identifier, or a different but equally valid ART locus, was structurally
invisible to this check. The null cannot see the world in which the finding replicates in another
form.

For us: our own open item, question (ii) transfer (`docs/briefs/2026-09-24-next-session-handover.md`
§2), needs "its own null" — Ark's point, a fit on a shuffled source bank scored on the same
target — and that null must be built so it can register *both* outcomes, not just the one the
search happens to be able to see.

### c. A criterion written after the finding

What they did, p.39 (Methods, "Benchmark grading"): *"Submissions were graded on the ten binary
claims that are listed in Fig. 4B, which the authors selected as characteristic of the ART
family."* The Results text (p.10) uses the same idea in different words: *"scored by a judge
model (Mythos 5) against ten curated features that we deemed characteristic of the ART family."*
The rubric was written from the one system already found, then used to grade how well other runs
"recognized" it.

Why it is a trap: a rubric built from the answer will always reward descriptions that resemble
the answer, whatever the actual evidential strength of a run's output.

For us: the FlyWire P3 registration wrote lambda reading rules for branch B only (§5 of that
registration), and the actual flagged outcome was a C (outcome note §3) — "the registration gives
no lambda rule for C," recorded there as a defect, not repaired. Question (ii)'s registration
needs reading rules written for every branch, A, B and C, before the run, exactly because writing
one only for the branch you expect is the same failure as writing a rubric from the finding.

### d. The evaluator is the system being evaluated

What they did: the tournament that ranked the 19 campaign reports used *"a language-model judge
(Mythos 5)"* (p.31), and the fixed-input benchmark's grading was *"performed by a language-model
judge (Mythos 5)"* (p.39) — the same model that ran the original discovery campaign.

Why it is a trap: a judge built from the same model family as the system under test can share its
blind spots, and a self-graded result is not an independent check.

For us: keep the external blind review gate — every registration and every run here is reviewed
by Ark, Johnny and Zcode before and after it runs (`docs/briefs/2026-09-24-next-session-handover.md`
§3), and question (ii)'s registration should go through the same gate before anything is run.

### e. Reading about the object instead of reading the object

What they did, p.10: with the locus given directly in context, *"the most capable models
accurately described the array in at least 90% of attempts, compared to as low as 32% (Opus 5,
level 4) with tooling."* The same page: *"With files, 39% of their attempts never read a
contiguous stretch of 200 nt or more... When a stretch of at least 200 nt was read, recognition
was 16 to 32 percentage points higher."*

Why it is a trap: giving a model tools to search a file is not the same as making it look at a
stretch of the object as long as the pattern itself. More tooling, used to skim, was worse than
less tooling, used to read.

For us: this has already happened here. On 2026-09-23 two agents described our bank as "a subset of
the hemibrain" and "one female (hemibrain)"; the bank file and the flyvis paper show it is the
FIB-25/FIB-19 type-level template of two flies, and the hemibrain appears in the source only as a
citation (`docs/notes/2026-09-23-where-our-bank-comes-from.md`, §1, §3 and §4, corrections to
claims in the group chat). That was reading about the object instead of the object. The
agents' own records, outside this repository, hold further instances of the same kind: search tools reporting matches in
zero files, and a name read in place of the passage that explains it. The rule for any check we
build over a bank: the unit of reading is no smaller than the pattern being looked for.

### f. A number under a name it was not computed under

What they did: the news post says, *"After 21 hours spent searching this data by roughly 950
agents using 210 million tokens..."* (news). The report's own Methods (p.30) gives: *"Token use
was calculated as the sum over all sessions of uncached input tokens (11.3 million), output
tokens (14.9 million), and tokens that were written to the prompt cache (189.5 million), which
gave 215.6 million tokens."* 189.5 of the 215.6 million are cache-write tokens, not plain usage,
and the total differs from the news figure by about 5.6 million.

Why it is a trap: a number that travels from a technical total into a public summary can quietly
change what it means, and pick up or drop a component, without anyone deciding to change it.

For us: this is why FlyWire P3's script was fixed in `c55d3e3` to print registered rows verbatim
and the gap to four significant digits, rather than a paraphrase (outcome note §2, §6) — print
registered values under their own name, not a summary of them.

### g. What they did right

The report is consistently explicit about denominators, not just headline numbers: *"Of the 17
candidate partner families, only three were confirmed as previously unreported RT associations"*
(p.3); *"The ART report ranked third (32 wins in 36 games)"* out of a full round-robin, *"Every
ordered pair of reports was compared once (342 games)"* (p.31); the replicate check ran *"ten more
times"* and reported what its identifier-based search could and could not see (p.8, p.38).

For us: keep reporting denominators the way our own outcome notes do — e.g. the FlyWire
sensitivity builds "recovered 5 and 8 of the 69 flyvis-30 pairs missing from the FlyWire bank"
(`docs/notes/2026-09-24-flywire-p3-what-it-showed.md` §1) — a number without the total it is
drawn from is not a checked number.

### h. A pipeline sees only the features it was given

What they say, p.2: *"Novelty in such pipelines is prescribed in advance, and anomalies that fall
outside those features go undetected."* The array was noticed in raw sequence, outside the
pipeline: *"No earlier tool call contained a repeat analysis, and no established repeat finder was
run in the session."* (p.31).

Why it is a trap: every statistic answers only the question it was built for. A pipeline cannot
report structure that lies outside its features, however long it runs.

For us: N1, BF_1 and the rank spectrum all fix their features in advance. Nothing in this
repository yet looks at a raw bank without one of them in hand. Whether such a look belongs in the
plan is an open question for Mike, not a rule adopted by this note.

## 3. Where each lesson is applied

A lesson that names no place of use cannot be checked. Each one below names the document or step
where it must be visible, so a reviewer can tell whether it was followed.

Denominator for this note itself: as of 2026-09-24 none of lessons a, b, c or h has been applied.
The (ii) registration they point to is not yet written, and no run has tested them. Lessons d, e,
f and g describe practice already in use; this note adds no evidence that it is sufficient.

| lesson | where it must show | how a reviewer checks it |
|---|---|---|
| a | the (ii) registration | the headline-rank rule is in the committed registration before any (ii) number exists |
| b | the (ii) registration | the null is described, and the registration states the result that would mean "no transfer" |
| c | the (ii) registration | a lambda reading rule exists for every branch (A, B and C) |
| d | every result with a sign or a verdict | the external blind review is recorded before the outcome note is committed |
| e | any check over a bank | the check reads whole entries of the bank, not a search over names or summaries |
| f | every run script | registered rows and values are printed verbatim, under their registered names |
| g | every outcome note | each count is given with the total it is drawn from |
| h | the plan, when Mike decides | the decision is recorded, either way |

## 4. Checked against the source

Pages read directly: 1 (abstract), 2, 3, 4, 5, 6, 8, 9, 10, 14, 30, 31, 38, 39, 40, plus the news
post in full. Page numbers are the report's printed ones, which match the PDF page index. Four
details that are easy to carry from the wrong place:

- "specific Mythos 5 internal signals that respond to repeated DNA" is the report's own abstract
  (p.1), not the news post. The news post does not use that wording. The abstract's "repeated
  DNA" and p.40's "neither is specific to DNA" are both the report.
- On the ten computer-generated DNA pairs only repeat-signal 2 was measured (0.69 against 0.00,
  p.40); "10 of 10" pairs higher is stated only for the letter/digit-string control.
- The abstract's "~200-nucleotide units" (p.1) are array units; the repeats themselves are 15 to
  49 nt, with spacers of 120 to 220 nt (p.6).
- "210 million tokens" is the news post; the report's total is 215.6 million (p.30).
