# USPEX (Oganov): same problems? — direct quotes, and what transfers to ADR-002

**Date:** 2026-09-17 · **Author:** Ark (review document, not a decision)
**Revision:** v3, 2026-09-17 (UTC). v1 was circulated in chat and reviewed by CC; the review found
a population error in §(c)1, which was corrected in v2 and the correction is marked in place. CC
also contributed the reliability-ceiling argument, §(c)2, attributed there. v3 applies four
corrections from Zcode, all accepted by Ark in writing: (2) the "three tasks" framing in §(a)3 was
wrong — the 16 held-out items are 6 scenes, and two of them, not one, flip the seed order when
dropped individually; (3) the r → nights conversion in §(c)1 gets its missing denominator (2 runs
per night, measured) and its correct consequence — 32 runs at r = 4, N = 8 is ~16 nights, not ~5,
and §(c)1a already means no nights figure is citable at all; (4) the local truncated file is a
different USPEX release (9.4.4), not a damaged copy of 10.6, per Zcode's reading of its raw
objects; (5) "65 of 8161 parameters" undercounts an individual, which also carries a seeded
data-order/augmentation stream. Verified quotes and numbers for all four are folded in below with
their sources, and the document is transferred into `connectome-seed` by CC.
**Requested by:** Mike — "поищи работы USPEX Оганова, там были такие же проблемы или нет" → "сделай разбор на одну страницу с прямыми цитатами, разнеси по трём пунктам".
**Answers to:** `docs/decisions/002-file-under-condition.md` (connectome-seed), whose condition is *"Show that a cheap evaluation of an individual is consistent with an expensive one."*

---

## Short answer

Yes, the same problems — and Oganov names both of them himself, in the first two numbered
points of his own paper. The difference is **where** they are allowed to appear: USPEX
*measures* the run-to-run scatter and *never lets the cheap side issue the verdict*. Our
condition asks the cheap side to rank. That is the one place the analogy does not hold, and it
is the place our project sits.

---

## (a) The problem they have — and it is our problem

**a1. Run-to-run scatter is a declared property of the method, not a defect.**
USPEX 10.6 manual, §4.12, variable `repeatForStatistics`:

> "USPEX simulations are stochastic, and redoing the simulation with the same input parameters
> does not necessarily yield the same results. While the final result — the ground state — is
> the same (hopefully!), the number of steps it takes to reach it and the trajectory in
> configurational space will differ from run to run. To quantify performance of the algorith
> [sic], you MUST collect some statistics — do not rely on just a single run (which may be lucky
> or unlucky…USPEX does not rely on luck!)."

This is our finding, stated by them: rerunning the same individual does not give the same
result, and a single run is not evidence. They reached it long before us and wrote it into the
manual. Their `fixRndSeed` exists ("For the same random seed, USPEX should produce the same
result"), but its default is `0`, and the statistics section is explicitly marked "only of
interest to developers".

**a2. Ranking is named as a problem first — before search.**
Oganov, Faraday Discuss. 2018, 211, 643–660 (DOI 10.1039/c8fd90033g), p. 644:

> "(1) The 'Ranking problem', i.e. the reliable calculation of relative structural energies.
> This turned out to be highly non-trivial, because the energy differences between different
> polymorphs are often very small and correctly ranking the structures by energy has long been
> (and to some extent still is) a challenge. (2) The 'Search problem'…"

p. 645: *"To sum up, CSP consists of two problems: search and ranking."* — and he notes the two
communities historically weighted them differently: organics attacked ranking (they can afford
enumeration), inorganics attacked search. Our (b) test is a pure ranking test.

**a3. Even the expensive side is not automatically trustworthy.**
p. 654: *"Even for the most basic property — the energy — for some systems the accuracy of
existing approximations is sorely insufficient… Comparing energies obtained by different modern
approximations for different blind test molecules, Hoja and Tkatchenko… found a rather poor
correlation."* Our version: the aggregate loss over 16 held-out items — six held-out scenes —
reorders seeds, and it is not one scene carrying that order. Dropping each scene individually at
the 250,008 rung, **two of the six scenes flip the order on their own**: `sequence_02_ambush_2`
(3 items) and `sequence_09_bandage_1` (3 items); `sequence_07_bamboo_1` and `sequence_12_cave_4`
do not (`results/night2/diagnostics/dropk/dropk_summary.md:18,20,22,24`). Same class of
statement — the arbiter is itself measured.

---

## (b) How they solved it

**b1. They measured the scatter, printed it, and never claimed one run proves anything.**
The manual's own sample output, 20 automatic repeats, target enthalpy 90.912:

```
Success rate: 100 percent
Average number of generations to get E=90.912: 29
Average number of structures  to get E=90.912: 1647
Standard deviation: 670
```

I recomputed from the 20 raw rows the manual prints: generation counts 14…60 (mean 28.95),
structure counts 757…3451 (mean 1646.9), and **670 is the sample standard deviation (n−1) of
the structure count** — coefficient of variation 40.7 %. (The manual does not say what its σ is
of; the arithmetic says it is the structure count, and that identification is mine, not its
text.) Their answer is not "make the run reproducible"; it is "spend 20 runs and publish the
spread".

**But read what that statistic actually is.** It requires `stopFitness` — a *target* — and the
manual states the dependency outright: *"Automatic analysis of statistics is enabled when
stopFitness is specified."* It measures **how long it takes to reach a known target**, i.e.
reachability and cost. It is not a statistic about ranking quality, and the manual adds: *"it
only makes sense to collect statistics with forcefields (e.g., using GULP)"* — collected
precisely where the expensive arbiter is **not** in the loop. This matters for us: the endpoint
USPEX chose is the one that survives run-to-run scatter, because it asks "did you get there",
not "who is better".

**b2. The cheap side does not issue the verdict. It proposes.**
This is the load-bearing inequality and it is architectural, not a convention: cheap = force
fields, semiempirical, MLF, evolutionary operators; expensive = DFT, variable-cell relaxation.
p. 646 gives the cheap side its only sanctioned ranking-adjacent job, and it is a *filter*:
semiempirical tight-binding *"for the relatively cheap yet reliable **pre-relaxation** of
crystal structures… and perhaps this is a right niche for such methods."* (Precision, from CC's
review: inside the search loop the cheap side **does** order candidates — that is what selection
is. What it never does is publish the verdict; promotion is the expensive side's right. The
weaker form is the correct one, and it is also the form ADR-002 could adopt.)

**b3. Cheap-vs-expensive has an explicit rule: reject, or recompute expensively.**
p. 648–649, on machine-learning force fields:

> "This works only as an interpolation, i.e. the new configurations should be sufficiently
> similar to the ones used for training the forcefield, and if a very different configuration is
> found, the errors can be very large, and such a configuration should either be rejected, or
> calculated at the ab initio level and then used for re-training the MLF."

With the failure case attached (Deringer et al., same volume): Hittorf's phosphorus, 84 atoms
per cell, *"could not be found in their random sampling search… and errors of the MLF for this
metastable phase are unusually large, above 100 meV per atom."* Their cheap side works because
it is **trained on expensive labels** and given an **out-of-distribution exit**.

**b4. A standing external arbiter, 27 years old.**
p. 645: *"traditional blind tests organized by the Cambridge Crystallographic Data Centre (CCDC)
were and still are entirely focused on organic crystals"*; Oganov's own team entered the 6th
one *"getting the right structure in 2 out of 5 cases"* (ref. 5, Reilly et al. 2016, Acta
Cryst. B 72(4), 439–459). Their analogue of our "external blind review is a mandatory gate" is
an institution, not a one-off.

---

## (c) What transfers to ADR-002

**1. Scatter is a property of the method, and it must be paid for in N — or dodged in the
endpoint.**

> **Correction, v1 → v2.** v1 said "σ/replica ≈ 0.14 … ~40 replicas per individual and ~53
> nights". That figure is wrong twice over, and CC found the first half of it.
>
> - *Population.* 1.7953 is `SD(0,1,2) n=3` — three seeds, night 2 (`results/night2/night_report.md:61`,
>   column header). The six-individual figure was already on record: **SD(n=6) = 5.1425**
>   (`results/night4/README.md:132`, full precision 5.142473, with a 95 % χ² interval
>   `[3.2100, 12.6126]`). Using n=3 under a population claim is the error.
> - *Kinds of quantity.* The denominator 12.7279 is not a standard deviation either. Its column
>   header at the same line is `replicate |0′-0|` — a single **absolute difference** between the
>   two twin runs at the 250k rung (1158.9237 − 1146.1958). So the ratio divides an SD by a
>   difference. The repository's own `SD/replicate` column mixes the two kinds the same way, so
>   this is a shared convention, not a private slip — which is exactly why it needs saying: the
>   convention does not survive being used in a cost estimate.
>
> Recomputing like for like (my arithmetic, from the records above): σ_rep from the two
> replicate pairs is 12.7279/1.1284 = 11.28 and 10.4309/1.1284 = 9.24 (mean 10.26) — where the
> divisor 1.1284 assumes the pair difference is a draw from an i.i.d. normal, which is an
> **assumption, not a measurement**. Then signal-to-noise = 5.1425/10.26 = **0.50** (not 0.14),
> and r = (σ_rep/σ_between)² = **4.0** with both pairs, 4.8 with the single pair — not ~40. Over
> the recorded CI on σ_between, r spans roughly **0.8 to 12**.
>
> Consequence, and it is the one that matters to Mike: the "~53 nights" line is not supported
> and must not be cited. v2 replaced it with "~5 nights" but never wrote down the r → nights
> conversion, so that number carried no derivation either. The missing denominator is **measured,
> not assumed: 2 runs per night**, the composition of every night on record — night 1 ran seed 0
> and its replicate 0′ (`results/night1/night_report.md:3-27`); night 2 ran seeds 1 and 2, by
> launch timestamp (`results/night2/night_report.md:30-34`); night 3 ran seeds 3 and 4 "to
> completion in one wave" (`results/night3/README.md:8-10`); night 4 ran "two jobs in one
> wave… replicate 3′ … FIRST, then the new seed 5" (`results/night4/README.md:8-12`). With r = 4
> replicates per individual at N = 8, that is 4 × 8 = 32 runs, and 32/2 = **~16 nights**, not ~5 —
> v2's figure used the right r but the wrong (unstated) denominator.
>
> **And under (c)1a below, no nights figure is citable at all** — not 53, not 16, not 5 —
> because every one of them comes from a signal/noise model the data themselves contradict (the
> moment estimate of σ²_between goes negative there). The arithmetic just given is shown only so
> that "~53 nights", or any other figure from this model, cannot be quoted as if it were a price;
> it is not itself a price.

**What survives the correction is the direction, and it is still bad.** The two twin offsets
(12.7279 and 10.4309 at the 250k rung) are larger than the SD across all six individuals
(5.1425) — and they consume most of the whole population's spread, 17.6 units from 1145.4 to
1162.9. One individual's two runs sit 10–13 units apart inside a population 17.6 wide. The
between-individual signal does not exceed the replicate spread. That statement needs no ratio
and no model, and it is enough to say the upper rung does not separate individuals.

**(c)1a. And the signal/noise decomposition itself does not fit the numbers** (my observation,
not reviewed). Under the additive model — value = individual effect + run noise — the variance
across individuals must be at least the run variance. Here it is not: 5.1425² = 26.4 against a
run variance of about 105. A single seed's replicate spread exceeds the scatter of all six
seeds, which the model forbids unless σ²_between is ≤ 0. So either the twin offset is not i.i.d.
noise at all — it is a saturating divergence, which is what the night-4 tail shows — or the
six-value SD is a small-sample artifact. Either way: **the cost of a ranking endpoint is being
estimated with an apparatus that has not been shown to fit.** That, not the number, is the
argument for testing the endpoint in (c)4 before spending nights on replicates.

**2. A cheap-vs-expensive correlation cannot exceed the expensive measure's own reliability.**
(CC's reading; the numbers below are mine.) The attenuation bound is |ρ| ≤ √r_yy. Here ρ =
0.8857 is computed between two points of the **same trajectory** — the 25k point statistic and
the 250k loss of the same run — so it is a within-trajectory coherence, while the between-
individual spread it is supposed to explain (5.14) is smaller than a single individual's
replicate spread (10.4–12.7). CC's conclusion follows: **ρ cannot be read as a fact about
individuals; it tracks realisations of run noise.** I would not put a *number* on the ceiling:
reliability is estimated from two replicate pairs, and the moment estimate of σ²_between goes
negative (see (c)1a), so no version of the model currently supplies a ceiling value. The
defensible form is qualitative and stronger than "preview at n=6": *the observation exceeds the
instrument.*

**3. Scatter is paid in N, or dodged in the endpoint — and the endpoint they chose is the
reachability one.** Their statistic measures iterations and structures to reach a fixed target.
Ours measures an ordering. If ADR-002 keeps the ordering endpoint, N must come from the measured
scatter — and (c)1a says that measurement is not yet in hand. Our §7 tolerance (replica under
1 % at 250k) is the right gate and it is still open: replica 0′ gave 1.11 %.

**4. Two endpoints, not one — and the reachability one is testable for free.**

> **Correction, v1 → v2.** v1 proposed "did this individual cross a fixed loss threshold within
> its run" and called it "naturally robust **by construction**". That was an inference, not a
> measurement, and CC falsified it without spending a run: the eight individuals' 250k rung
> values span 17.6 units, while the twin offsets are 12.7 and 10.4 — so *any* fixed threshold
> inside the population's own range sits within one twin gap of almost every individual. A
> binary "crossed / did not cross" on the final loss is the same noise in a different notation.

The correct analogue is not a threshold on quality but **the number of steps to a fixed
target** — which is precisely what USPEX counts (generations and structures to E = 90.912). Our
form: **iterations until the loss curve crosses a fixed level.** Its noise is measurable from
data already on disk — the checkpoint curves of all eight runs — so the whole question costs
minutes of CPU, no GPU and no night. **Proposed, not decided**, and a different hypothesis from
(b): if this endpoint is stable across the replicate pairs it is a road C that does not change
the population; if it is not, it dies for free. Per repository rule it would need its own
registration before it is read.

---

## Does the analogy license ADR-002?

No — and ADR-002 already says so, in its own Decision Drivers, written 2026-09-13:

> "The USPEX analogy breaks where it thinks it is strongest: DFT enthalpy is a physical quantity
> nobody chooses, fitness here is written by the author; DFT relaxation converges to something
> physical, 'youth' minimises a training loss."

Everything in §(b) rests on that: their arbiter is a physical quantity, ours is a chosen loss;
their cheap side is trained on the arbiter's labels, ours is a truncated copy of it; their
endpoint is a threshold on a physical observable, ours is an ordering produced by that chosen
loss. So §(b) does **not** license the condition in ADR-002 — it warns against exactly its
shape, and it supplies the two known workarounds: a trained filter with a stated exit, and a
reachability endpoint instead of a ranking endpoint.

---

## Boundaries — what this document does not establish

- **Oganov's paper:** read fully pp. 1–4, 6–7, 11–12 (text layer); pp. 5, 8–10, 13–18 not read.
  The figures were not seen (his Fig. 7 is the Hoja–Tkatchenko correlation plot — I have the
  text claim, not the plot).
- **The 20-run sample output** is the manual's illustrative example, not a published experiment
  of theirs; it has one entry point (`repeatForStatistics`/`stopFitness`), which I have read, and
  no statistical treatment beyond mean and sample sd, which I recomputed and matched.
- **The identification "670 is the sample σ of the structure count"** is mine by arithmetic —
  the manual prints the number without saying what it is of.
- **Manual version.** v1 quoted the 10.6 *online* manual and could not compare it with our local
  copy. Since then the official PDF of the 10.6 release has been downloaded and the six
  quotations — `repeatForStatistics`, the 20-run table, σ = 670, `stopFitness`, the GULP
  sentence, `fixRndSeed` — checked word for word against it (CC, 2026-09-17). The earlier local
  file is **not** a damaged copy of 10.6: **Zcode's reading, recovered from the file's raw
  objects and not independently reproduced**, is that it is a different release, USPEX **9.4.4
  (25 June 2017)**, whose own §4.12 sits at printed page 54 of *that* manual's table of
  contents — past the point where the file's bytes stop (196 of 724 objects missing) — so even
  fully repaired it could not have confirmed a single 10.6 quote. CC's own byte-level check of
  this file cannot confirm or refute the 9.4.4 identification either way: it has no `trailer`
  keyword, no `/Info` dictionary and no readable XMP metadata (checked directly against the file's
  raw bytes), so the version number above is Zcode's reading, stated as such, not a fact CC
  verified. Kept as `uspex-manual.pdf.truncated-2026-09-18` as evidence regardless of which
  release it turns out to be. One provenance trap, from the fresh PDF's own verification (CC,
  direct `pdftotext` read of `uspex-manual.pdf`): its title page says "Version 10.6, June 4,
  2026" while the running header on every content page still says "USPEX 10.5" — cite the version
  from the title page only.
- **Our own numbers**, and their standing after this revision: SD(0,1,2) n=3 = 1.7953 and
  replicate |0′−0| = 12.7279 (both `results/night2/night_report.md:61`, **verified by Ark**);
  SD(n=6) = 5.1425 and its CI (both `results/night4/README.md:132`, **verified by Ark**);
  |3′−3| = 10.4309 at the 250k rung (from the night-4 rung values, **verified by Ark**);
  population span 17.6 (computed by Ark from the rung values). 16 held-out items; ρ = 0.8857
  dropping to 0.714 on the 4↔5 swap; §7 replica 1.11 % — these three are **carried from the
  night-2 records and earlier readings, not re-measured for this document**. The "three
  `ambush_2` tasks" claim in v2 is withdrawn: per (a)3 above, at the 250,008 rung two of the six
  held-out scenes — `ambush_2` and `bandage_1` — each flip the seed order on their own when
  dropped individually, and the other four (including `bamboo_1` and `cave_4`) do not
  (`results/night2/diagnostics/dropk/dropk_summary.md:18,20,22,24`, **verified by CC in this
  revision**). "65 of 8161 parameters differ at iteration 0" is also incomplete, not wrong: that
  count is only the direct initialisation difference. The run script additionally seeds
  `random`, `numpy` and `torch` from the individual's seed, so data order and augmentation differ
  per individual too — an individual is 65 bias values *plus* a data-order stream
  (`docs/preregistration-cheap-vs-expensive.md:35`, "Clarified 2026-09-15 (Zcode 07:05 local;
  verified by CC, `tools/night/run_individual.py:208-210`, `:623-625`)"; confirmed again directly
  here against `tools/night/run_individual.py:8-14,282-284,703-705`, **verified by CC in this
  revision**). Individuals therefore differ by *more* than 65 numbers, and the twin pairs (seed 0
  vs 0′, seed 3 vs 3′) still diverge by 10–13 at the 250k rung despite identical inputs otherwise
  — which strengthens the saturating-divergence reading of §(c)1a below, not the reading that the
  seed sets very little. The σ_rep → r → nights chain is **arithmetic on an assumption**
  (i.i.d.-normal pair difference), not a measurement, and (c)1a means no nights figure is
  citable regardless of the arithmetic.
  **Verification pass, this revision.** CC checked ten of this document's own numbers directly
  against primary records: the two scene-drop flips and two non-flips above; the four nights'
  crew compositions in §(c)1; the 65/8161 data-order clarification above; and, for the manual
  (Sources, below), the fresh PDF's sha256/byte count/page count/title page/running header and
  its §4.12 averages recomputed from the raw 20-row table. Reported here, not independently
  recomputed by CC: Zcode's own re-check of this revision found 13/13 quotes and 10/10 numbers
  correct.
- **Attribution of the review.** The population error (v1→v2) was found by CC; the
  SD-vs-difference point, (c)1a, §(c)2's refusal to quote a ceiling, and §(b)2's narrowing are
  mine. The four v2→v3 corrections — the scene-flip count, the nights denominator, the manual
  version, and the 65/8161 undercount — are Zcode's, accepted by Ark in writing; the folding-in,
  the primary-record citations, and the transfer into `connectome-seed` are CC's.

## Sources

- Oganov, A. R. *Crystal structure prediction: reflections on present status and challenges.*
  Faraday Discuss., 2018, **211**, 643–660. DOI 10.1039/c8fd90033g. Local:
  `research/uspex/oganov-faraday.pdf` (sha256 `e3ee0b1b…27e`).
- **USPEX 10.6 manual (release 2026-06-04), §4.12 "Keywords for developers" — primary source,
  verified word for word.** Fresh official PDF: sha256
  `4969da978abd884fde38e3b645dc58344b1c93fef1711ced160bb60b02471751`, 7,965,545 bytes, 137 pages
  (checked directly, this revision, CC — byte count, sha256 and `pdftotext` page count all match
  the figures above), title page "MANUAL / Version 10.6, June 4, 2026". Downloaded from
  https://uspex-team.org/online_utilities/uspex_manual_release-10.6_04_06_2026/EnglishVersion/uspex_manual_english.pdf ;
  online HTML mirror of the same release at
  https://uspex-team.org/online_utilities/uspex_manual_release-10.6_04_06_2026/EnglishVersion/uspex_manual_english/sect0023.html .
  All six quotations already used in this document — `repeatForStatistics`, the 20-run table,
  σ = 670, `stopFitness`, the GULP sentence, `fixRndSeed` — were verified word for word against
  this PDF (differences only in how `pdftotext` renders the em-dash and the ellipsis). The
  manual's own printed averages, 29 / 1647, recompute exactly from its 20 raw rows to **28.95 /
  1646.9**, with sample standard deviation (n−1) of the structure count **669.83 → 670**; the
  population standard deviation (divisor n) is **652.87**, which does not round to 670 — so the
  sample-sd identification in this document is distinguishable from the alternative, and the
  manual itself still does not say what its σ is of (all recomputed directly from the PDF's §4.12
  text this revision, CC). New quote, if not already present above: *"Automatic analysis of
  statistics is enabled when stopFitness is specified"* (already quoted in §(b)1). **Provenance
  trap:** the title page says "Version 10.6" but the running header on every content page reads
  "USPEX 10.5" — cite the version from the title page only (checked directly, CC).
- **Superseded local file:** `uspex-manual.pdf.truncated-2026-09-18`, sha256
  `ff8a18148a8ac1160541f083c61fb71aad2f28a78935ac1297e9894b00b87023`, kept as evidence. Per the
  Boundaries note above, Zcode's unreproduced reading is that this is a different release (USPEX
  9.4.4, 25 June 2017), not a damaged 10.6 copy.
- **Zcode's HTML snapshot** of the online 10.6 manual: `research/uspex/uspex-manual-10.6-online/`
  (109 manifested files, `MANIFEST.sha256` + `PROVENANCE.md`; checked directly, CC, this
  revision) — secondary copy; the official PDF above is primary.
- **The source PDFs are not committed to this repository.** `.gitignore` excludes
  `sources/local/` for exactly this reason — "full-text copies with no confirmed redistribution
  licence" (`connectome-seed/.gitignore:18`, checked directly, CC). They live outside git history,
  at `connectome-seed/sources/local/uspex/`, and are identified here by sha256 only.
- `docs/decisions/002-file-under-condition.md` (connectome-seed), read in full.
- `results/night2/night_report.md:61`; `results/night4/README.md:132` — both read directly.
- `results/night2/diagnostics/dropk/dropk_summary.md:3,18-28` — scene-level drop-k table, read
  directly this revision (CC).
- `results/night1/night_report.md:3-27`; `results/night2/night_report.md:30-34`;
  `results/night3/README.md:8-10`; `results/night4/README.md:8-12` — the four nights' run
  compositions, read directly this revision (CC).
- `docs/preregistration-cheap-vs-expensive.md:35`; `tools/night/run_individual.py:8-14,282-284,
  703-705` — the seed's effect on data order and augmentation, read directly this revision (CC).
- Deringer et al., DOI 10.1039/c8fd00034d and Hoja & Tkatchenko, DOI 10.1039/c8fd00066b — cited
  from Oganov's text only; not read.
