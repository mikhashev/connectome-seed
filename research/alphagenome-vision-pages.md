<!-- imported from Ark's sandbox C:/Users/mikha/.dpc/agents/agent_001/research/alphagenome-vision-pages.md, sha256 05a874a57c6de66972e8e6045f3ebd49e32a60005094bfa94ccbc079c458543f, mtime 2026-09-13 18:04:10 UTC, imported by CC on Mike's word 2026-09-13 18:09 UTC; content unchanged below -->


# alphagenome-atlas.pdf

pages 6-7 of 83

## Page 6

A ClinVar, stratified by molecular consequence (AUPRC)

Protein altering
(+50101/-101100)
0.90
0.86
0.83
0.81
0.62
0.62
0.53
0.00 0.25 0.50 0.75

Intronic
(+3270/-353816)
0.76
0.44
0.36
0.33
0.15
0.05
0.02
0.0 0.2 0.4 0.6 0.8

Synonymous
(+511/-421382)
0.57
0.35
0.08
0.03
0.00
0.0 0.2 0.4 0.6

3' UTR
(+47/-18686)
0.50
0.18
0.16
0.10
0.03
0.01
0.01
0.0 0.2 0.4 0.6

5' UTR
(+143/-18739)
0.27
0.26
0.24
0.17
0.05
0.01
0.01
0.0 0.1 0.2 0.3

B Genome-wide benchmarks (AUPRC)

ClinVar SNVs
(+151026/-997941)
0.97
0.96
0.92
0.91
0.68
0.36
0.21
0.00 0.25 0.50 0.75 1.00

ClinVar Indels
(+106995/-44767)
0.99
0.99
0.94
0.91
0.85
0.00 0.25 0.50 0.75 1.00

Non-coding Mendelian
(TralGym)
(+308/-2228)
0.77
0.76
0.76
0.74
0.73
0.70
0.54
0.0 0.2 0.4 0.6 0.8

Fine-mapped GWAS
(TralGym)
(+409/-3686)
0.28
0.27
0.25
0.24
0.22
0.20
0.10
0.0 0.1 0.2 0.3

Rare complex
trait variants
(+2879/-2784)
0.69
0.67
0.67
0.65
0.64
0.61
0.41
0.0 0.2 0.4 0.6

Predictors
AVI
CADD v1.7
GPN-star (V)
GPN-star (M)
Cactus
Phastcons 470-way
gnomAD allele frequency
Evaluations
Non-coding evaluation

C Example: HBB locus

chr11:5225462-5227296
HBB
1
2.5
0.0
-1.0
ClinVar
AVI SHAP
chr11:5225460-5225610
HBB
1
0
-1
ClinVar
GPN-Star (V)
AVI SHAP
RNA-seq
Venous blood
30
0
PolyA
IRX
Unknown
Atlas motifs
chr11:5227067-5227167
HBB
1
0
-1
ClinVar
GPN-Star (V)
AVI SHAP
CAGE
25000
0
TATA
SP/KLF
NFY
SP/KLF
Atlas motifs

AVI features
Splicing
ATAC-seq
Contact maps
DNase-seq
ChIP-TF
ChIP-Histone
CAGE
PRO-cap
RNA-seq
Polyadenylation
AlphaMissense
Cactus
PhastCons
Protein Termination
Start Lost
Stop Lost

D Saturation genome editing (SNV only)

Spearman correlation
0.5
0.4
0.3
0.2
0.1
0.0
BAP1
BARD1
BRCA1
BRCA2
CTCF
PALEB2
RUNX2
SFPQ
VHL
XRCC2

E Dace et al. 2025: BRCA1 promoter

BRCA1
chr17:43125410:G>A
0
-1.5
1.5
6000
0
SGE scores
(Dace et al. 2025)
GPN-Star (V)
AVI SHAP
ISM:
K562 ChIP E2F1
NRF1
E2F
Atlas motifs
chr17:43125361-43125436

chr17:43125410:G>A
BRCA1
K562
ChIP E2F1
1000
500
0
2.0
1.0
0.0
RNA-seq
REF
ALT
chr17:43122910-43127910

Fig. 2 | AlphaGenome Variant Impact (AVI): a combined score for genome-wide coding and non-coding variant prioritization. (A) Comparison of AVI to other methods for classifying ClinVar pathogenic single nucleotide variants (SNVs) from benign SNVs, stratified by ClinVar variant consequences (AUPRC). Across the figure, error bars indicate 95% confidence intervals from 100 bootstraps, and black dashed lines indicate the value expected for a random classifier. (B) Comparison of AVI to other methods across additional genome wide benchmarks including complex traits and rare disease. This includes: ClinVar stratified by SNV versus Indel, TralGym Mendelian and Complex traits, as well as a benchmark for rare variants associated with complex traits. For more information, see Methods. (C) Visualization of AVI feature attributions across the HBB locus. Top: The transcript annotation for the HBB gene, alongside ClinVar known pathogenic (red) and benign (blue) variants shown above the AVI feature attributions. Both ClinVar and AVI feature attributions are represented at 4 bp resolution by the maximum datapoint within each 4 bp bin. Insets: Expanded locus views of chosen regions of HBB, including the 3' UTR (left) and the promoter (right). GPN-Star (V) is shown for comparison, as well as Atlas motifs and ISM scores for chosen tracks. Grey and white stripes in the insets mark base-pair resolution. For AVI the 3 data points within each stripe represent the 3 alternative bases at allele resolution. Alternative variants are ordered alphabetically. See fig. S7C for the conversion of AVI SHAP raw scores to AVI PHRED scores for interpretation. (D) Spearman correlation between model predictions and experimental saturation genome editing (SGE) assay measurements across 10 genes. Each color indicates one computational method, with model colors the same as shown in (A). Only SNVs from these screens are used in this evaluation.

## Page 7

Fig. 2 | (continued)
(E) Left: An example variant (chr17:43125410:G>A) in the promoter region of BRCA1 that was measured by SGE (31). Negative SGE scores indicate loss of cell fitness as a proxy for BRCA1 expression; red variants exceed author-defined thresholds for loss-of-function, while blue are under threshold. SGE scores are shown together with AVI SHAP, motif instances and AlphaGenome K562 ChIP-TF Active ISM contributions scores in this region. K562 was chosen as the closest cell line proxy available for the HAP1 cell line used in the original experiment. An Atlas E2F motif is identified in the ChIP-TF E2F1 track overlapping the variant. Grey and white stripes mark base-pair resolution. For SGE and AVI scores the 3 data points within each stripe represent the 3 alternative bases at allelic resolution. Alternative variants are ordered alphabetically.
Right: AlphaGenome E2F1 ChIP-TF and RNA-seq (K562) predictions for the reference and alternative sequence.

with an E2F motif instance called on the K562 E2F1 ChIP-seq track that is ablated in the presence of the alternative allele, alongside decrease in expression of the BRCA1 gene (Fig. 2E). Additional variant interpretations are shown in fig. S8.

We performed model ablations to assess the necessity of the 18 features chosen as input features to AVI (Table S2). Removing all protein features yielded significant performance drops on coding-variant skewed evaluations such as ClinVar and saturation genome editing. Conversely, ablating the core AlphaGenome features degraded performance across non-coding and regulatory evaluations. During model development, we evaluated numerous additional features, including extended VEP consequences and CADD-inspired features, which did not meaningfully affect model performance when included. Notably, although the AVI model was trained without AlphaMissense scores for indels, we found that supplying approximations of these scores during inference improved performance on coding indels and reduced reliance on the variant-info features (Table S2, Methods). Ultimately, only 18 features were required for robust performance across a diverse set of evaluations. This is a substantial reduction in features compared to CADD v1.7, which uses over 150 features.

AVI prioritization helped resolve a rare disease case and functionally characterizes deep intronic variants in DN M1

We applied AVI to data provided by the GREGoR Consortium, whose aim is to resolve currently unexplained rare genetic disorders (33). Rare disease cases can remain unsolved due to time constraints attempting to evaluate an average of 4-5 million variants per individual, the majority of which will be benign or variants of uncertain significance (VUS) (34). Retrospectively analyzing past solved cases, including both SNVs and indels, AVI ranked the known likely pathogenic and pathogenic variants among all variants in each patient more highly than CADD v1.7, with a recall of 29.5% compared to CADD v1.7's 12.5% when considering the top 50 variants ranked by either method (Fig. 3A). When considering only variants filtered by gnomAD allele frequency of 0.001, the recall at top 50 variants increased to 74.3% and 61% for AVI and CADD v1.7, respectively (fig. S9A). Next, we prioritized variants in unsolved rare disease cases in the cohort by systematically ranking and analyzing all small de novo variants in 814 individuals with parent and proband genomes available.

For a proband with epileptic encephalopathy (Fig. 3B), the top ranked variant by AVI was a heterozygous noncoding VUS in intron 10 of DN M1 (chr9:128225994:G>A, HGVS: NM_004408.4:c.1335+1605G>A) affecting a brain-specific transcript isoform encoding for the dynamin protein. This variant is 5' of exon 10a, which is exclusively present in brain-specific transcripts and absent from the MANE Select transcript (35). Of the variant's AVI PHRED 24.7 score, 69% was directly attributed to AlphaGenome's splicing feature and the precomputed scores pointed to altered splice site usage in the 'glutamatergic neuron' biosamples. Prediction of RNA-seq track coverage of the reference and alternative alleles showed that the variant creates a brain-specific cryptic splice acceptor site resulting in a 13 amino acid (aa) in-frame extension of exon 10a (Fig. 3C). Predictions in the 'venous blood' biosample showed negligible expression of exon 10a, explaining why previous RNA-seq from blood draws were inconclusive.

To probe the feasibility of this being a pathogenic variant, we performed a literature search and found that two recently published case studies showed the same brain-specific 13 aa extension of DN M1 in
