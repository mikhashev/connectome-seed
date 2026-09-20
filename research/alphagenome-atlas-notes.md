<!-- imported from Ark's sandbox C:/Users/mikha/.dpc/agents/agent_001/research/alphagenome-atlas-notes.md, sha256 95f25a24559133e96268bf64ff8c0c13cfc7e7c1e3d7b8f21008043d81621b63, mtime 2026-09-13 18:05:07 UTC, imported by CC on Mike's word 2026-09-13 18:09 UTC; content unchanged below except for one
Russian quotation, rendered into English on 2026-09-20 under the repository's language rule
(docs/CHECKLIST-research-repo.md § Language) and marked "(translated from Russian)" in place -->


# AlphaGenome Atlas — source note and its relation to connectome-seed

**Date of note:** 2026-09-13 (rev. 2 — figures correction, see §"Correction")
**Requested by:** Mike (Telegram, DPC Research) — "save it as md" (translated from Russian),
after Ark's chat note (#174)
**Author of the note:** Ark

## Source

| | |
|---|---|
| PDF | `C:\Users\mikha\.dpc\temp\alphagenome-atlas.pdf` |
| sha256 | `07011853872613cb7bd3ce8ca62cd2621ad50b0a16e6f5dec3e480b3d190af2c` |
| Pages | 83 |
| Title | AlphaGenome Atlas: in silico mutagenesis of the entire human genome improves prioritization and interpretation of non-coding variants |
| Authors | AlphaGenome Atlas team (Google DeepMind + Exeter, Broad, Harvard, Stowers, MSKCC, MGH, Google Research Zurich). Supervising: Heidi L. Rehm, Fei Chen, Caleb A. Lareau, Caroline F. Wright, Anne O'Donnell-Luria, Julia Zeitlinger, Pushmeet Kohli, Žiga Avsec |
| Website behind it | `https://alphagenome.google/atlas` |
| Extracted text | `alphagenome-atlas_full.md`, 282 891 bytes, 11 261 lines |
| Vision transcription | `alphagenome-vision-pages.md` (pages 6–7; pages 4–5 came inline and are not yet saved) |

## Correction (rev. 2, 2026-09-13 — my error, Ark)

Rev. 1 of this note said: **"Figures are NOT in the file … the extracted text carries captions and body text only"** and **"Do not quote formulas from this extraction."**

**Both statements were wrong, and the error is instructive.**

The numbers *are* in the text layer. `search_in_file` on the extraction finds, on page 4 alone: `253 billion` (line 345), `ZNFs` (379), `(n=2,601)` (393), `ChIP-seq 1,617` (533). Those are **figure-chart labels**, not prose. They were extracted — but in the PDF's internal drawing order, so they land as detached fragments between paragraphs.

What I saw was numbers floating out of context, and I read it as **symbol-font corruption**. The tool had in fact flagged something much narrower: `suspect_fonts: ["CMSY8"]`, `suspect_chars: 1` — *one glyph*, on a page, from a math-symbol font. From "one glyph is unreliable here" I produced "formulas from this extraction cannot be quoted" — a narrow instrument reading promoted to a wide instruction.

**Class: the instrument answered a narrow question; I read it as answering a wide one.** Same failure as the 1 200-characters-per-page reading of the PDF, earlier today. Recorded here because the correction matters more than the original claim.

**What vision actually added** — not content, **structure**. Compare:

- text layer (page 4): `253 billion` / `ZNFs` / `(n=2,601)` / `ChIP-seq 1,617` — present but unattributable; you cannot tell which bar or which axis they belong to
- vision (page 4): the same numbers, in order, inside the figure story — `TF binding ChIP-seq 1,617`, `Motifs (n=2,601)`, `253 billion Motif Instances`, and the motif-category split `Main 122 / Composite 104 / ZNF 94 / Unknown / Unresolved`

So the correct rule is not "do not read the figures". It is: **the extraction holds the figure's numbers, shredded; vision reassembles them.** For anything where *which number belongs where* matters, vision is the route.

**Unresolved contradiction, recorded rather than explained away.** The vision route reported for pages 4–7: *"page N has no text layer and was transcribed by a vision model"*. But the text-layer route clearly did produce page-4 content, including the chart labels above. The two statements cannot both be literally true. Possible readings: the tool's phrase means "no *usable* layer for that route", or the check is per-region (chart block vs body). **I did not resolve it and I am not guessing.** Which claim is load-bearing: the extraction demonstrably contains the labels (line numbers above), so the figure content was never actually missing.

### Cost, measured

| | |
|---|---|
| Vision, 4 pages (4–7) | **80.9 s** total — 27.1 / 16.1 / 21.4 / 16.3 s per page |
| Model | `qwen3.8 27b Mythos` (local) |
| Repeat call | **cached, 0.0 s** — re-reading a page costs nothing |
| Route choice | `mode='vision'` forces it; `mode='auto'` will not send a page that has a layer |

**This competes with the connectome-seed night run for the same GPU.** Vision should be batched before the night starts, not during.

## How it was read (so that nobody over-reads this note)

- **Route:** rev. 1 read pages 1–83 by the PDF text layer, `mode auto`, no vision. Rev. 2 adds vision for pages **4, 5, 6, 7** only.
- **Depth.** Pages **1–2** read line by line. Pages **4–7** read by vision (figures + body). **The remaining 75 pages are on disk but have not been read line by line.** Everything below is marked Observed or Inferred.
- **The `CMSY8` flag** on pages 4, 6, 7, 9, 11, 14–17, 21, 51–60, 61–67, 69–71, 73, 74, 76 marks **one glyph each**, not whole formulas (see Correction). On pages 10, 12, 19, 22–26, 29, 33, 39–42 the maths check did not run at all — a corruption there would be unflagged. Treat numerical claims drawn from those pages as unverified until re-read.

### Verbatim, page 2

> We recently described AlphaGenome (9), a state-of-the-art sequence-to-function model unifying long 1 megabase (Mb) DNA context, basepair resolution outputs, and joint prediction of multiple genomic assay modalities including TF binding, chromatin accessibility, histone modifications, gene transcript abundance, and splicing.

> we performed in silico saturation mutagenesis (ISM) across the human genome, generating precomputed predictions for all possible human single nucleotide variants (SNVs) as well as indels observed in different population datasets. To enable variant prioritization, we trained the AlphaGenome Variant Impact (AVI) score, integrating these ISM predictions with AlphaMissense, conservation metrics, and protein-coding features in a supervised framework.

### Verbatim, page 1 (abstract)

> AVI achieved state-of-the-art performance across diverse benchmarks with improved prioritization of deleterious non-coding variants. Application of the combined Atlas resource helped solve an epileptic encephalopathy rare disease case, increased the statistical power to detect rare non-coding variants driving population-level phenotypes, and enhanced the mechanistic interpretation of these variants.

## What it is (Observed, pp. 1–2, 4)

Precomputed database of variant effects: ISM across the whole human genome for every possible SNV plus observed indels. On top, a supervised score (AVI) turning precomputed predictions into one ranking number. Plus SHAP attribution per AVI score, and de-novo cis-regulatory motifs derived from the ISM maps.

**Scale (Fig. 1A, Observed via vision):** ~9 billion SNVs + observed indels; entire genome 3 billion bases. Twelve variant scores; biosamples behind them — DNase 305, ATAC 167, TF binding ChIP-seq **1 617**, histone ChIP-seq 1 116, CAGE 546, PRO-Cap 12, contact maps 28, polyadenylation 371; splice sites 2 (don/acc), splice-site usage 367, splice junctions 367.

**AVI architecture (Fig. 1B):** integrates AlphaGenome scores + AlphaMissense + 3 protein loss-of-function annotations from ENSEMBL VEP (protein termination, stop lost, start lost) + two conservation scores (PhastCons 470-way, Zoonomia Cactus 241-way) + indel-type indicators. Raw score → PHRED by ranking against all SNVs; indels mapped onto the SNV quantile curve.

**Training (Fig. 1C) — proxy labels, and this matters:** gnomAD v4.1 max filtering allele frequency; AF > 0.001 → proxy benign, AF < 0.001 → proxy impactful; n≈1e8 and n≈2e7. The model is trained to give higher scores to rarer variants *on average*. Stated by the authors.

**18 features**, against CADD v1.7's 150+ (Observed, p. 7).

## Performance, and where they lose (Observed, Fig. 2, via vision)

AUPRC, ClinVar pathogenic vs benign, by consequence — AVI first except where noted:

| category | AVI | best alternative |
|---|---|---|
| protein-altering | **0.90** | 0.86 GPN-Star-V |
| intronic | **0.76** | 0.44 GPN-Star-V |
| synonymous | **0.57** | 0.35 CADD v1.7 |
| 3' UTR | **0.50** | 0.18 GPN-Star-M |
| 5' UTR | 0.27 | **0.26** GPN-Star-V |
| non-coding Mendelian | 0.76 | **0.77** GPN-Star-M |

Genome-wide: ClinVar SNVs 0.97, ClinVar indels 0.99, fine-mapped GWAS 0.28 (vs 0.27), rare complex-trait variants 0.69 (vs 0.67). Error bars are 95 % CI from 100 bootstraps.

**They report their own losses** — 5'UTR and non-coding Mendelian. Worth noting as a discipline bar.

**Fig. 2D:** Spearman correlation between model predictions and **saturation genome editing (SGE) measurements**, ten genes, SNVs only; AVI highest in eight of ten (Observed p. 5; per-gene bars read, exact values not transcribed).

## The one structural connection to our work (Reported — Ark, chat #174, 2026-09-13)

The argument form is ours: a **cheap estimate replaces an expensive measurement**, and the artefact rests on the replacement being faithful.

> With roughly 9 billion possible single-letter mutations in the human genome, **testing each one in the lab is practically impossible**.

But the *kind* of cheap estimate differs, and that is what matters for our preregistration:

| | AlphaGenome Atlas | connectome-seed test (b) |
|---|---|---|
| Expensive truth | lab experiment | full training run (250 000 iterations) |
| Cheap substitute | **a trained model** (AVI), fitted on measured benchmarks | **a prefix of the same process** (1 000 / 5 000 / 25 000 iterations) |
| Calibrated against | experimental ground truth | nothing — it *is* the process, stopped early |

**Consequence (Inferred):** their success licenses *the trained-surrogate kind*, not *the prefix kind*. 2508.17464 tested the prefix kind and found ranking does not hold up. Their paper is not evidence about ours.

Confirmed at source, Methods (lines 4440–4441): *"For Spearman correlations, the AVI score was compared to the reported variant rankings within [the SGE screens]"* — their correlation is model-vs-experiment, not cheap-vs-expensive-of-the-same-process.

## Three conditions AlphaGenome has and we do not (Inferred)

1. **A trained surrogate with real labels.** AVI is supervised. We have no independent labels for "is this morphology any good" — our expensive measure is the same simulator, run longer.
2. **A finite, small space.** ~3×10⁹ positions × 3 substitutions is enumerable. Genome and morphology spaces are not.
3. **One fixed input.** One human reference genome. We have an unbounded population of individuals, none given in advance.

And: **they do not run a loop.** No population, no selection, no fitness landscape with inheritance. A catalogue of effects, not a developmental loop. Evolution replaced by enumeration.

## What it does not answer

- **It does not validate cheap ranking over a population.** Their cheap score ranks everything; the expensive measurement checks the **top**. Collaborators "used AlphaGenome Atlas to identify and experimentally verify key variants" — top-of-list verification, not rank correlation across a population.
- **Their map is predictions, not measurements.** Stated by the authors, with a clinical disclaimer. They can call it a map only because the top was verified in a lab.

## Possible consequence for our preregistration (proposed, NOT registered)

**Now evidenced, not merely inferred.** Page 7 (Observed via vision), triage of unsolved rare-disease cases:

> AVI ranked the known likely pathogenic and pathogenic variants … with a **recall of 29.5% compared to CADD v1.7's 12.5%** when considering the **top 50 variants ranked by either method**. When considering only variants filtered by gnomAD allele frequency of 0.001, the recall at top 50 variants increased to **74.3% and 61%** for AVI and CADD v1.7 respectively.

That is **top-k recall**, not rank correlation. In real use their cheap score is judged by whether it puts the truth in the top 50 — a much weaker requirement than agreeing across a population.

Separately, the same section reports a resolved case: AVI's top-ranked variant for an epileptic-encephalopathy proband was a non-coding VUS in intron 10 of DNM1, PHRED 24.7, **69 % of the score attributed directly to the splicing feature**, predicting a brain-specific cryptic splice acceptor giving a 13-aa in-frame extension. Blood RNA-seq had been inconclusive because the transcript is brain-specific.

So two hypotheses may be worth separating before the N-night:

- **(b1) rank agreement** — does the cheap prefix rank individuals the same way as the expensive full run? (Spearman over N, as currently registered.)
- **(b2) top-k hit** — does the cheap prefix put the eventual top individuals into the top-k of the full run? Weaker, closer to what AlphaGenome actually relies on, and closer to how a *search* would use it. 2508.17464 does not kill (b2): it never tested it.

Not registered. Decision is Mike's; would go into the preregistration before the N-night, not after.

## Boundary

- **Not** "the same thing at a different scale". A different solution to the same problem, working where a trained surrogate and a finite space exist. Our question is what happens where neither does.
- Anything here about our own experiment is Inferred unless marked Observed.
- The 75 pages not read line by line may contain details that change this note. Full text on disk beside this file; vision re-reads are cached and free.
