# Checklist — research repository, start here

**Status:** in force for this repository from 2026-09-15 (Mike's word "write the checklist",
translated from Russian, 09:56);
written by Ark (08:50, 09:39, 09:51) with CC's additions; a new research repository starts by
reading the incidents below, not by re-deriving the principles.

1. Every measuring instrument has a positive control that must pass before any null is
   reportable. (L3 probe, autoresearch `docs/methodology/phase-3-design.md:166`; §3.9.)
2. If an instrument is taken out of the environment where it was watched, take the witness
   with it. (The seven `eval_rung` invariants absent from the diagnostics, 002 §5h.)
3. Two evaluations in one stage are compared to each other by the code, not by eye a day
   later. (The bit-identical 0.0, 002 §5h.)
4. Constants copied from a document are checked against the document at run time, and
   numbers never enter identifier names. (38.18 / 1146.1958 / K = 26; `n_above_floor_38.18`;
   002 §5h.)
5. Measure, item composition and threshold are fixed before the first look. (§3.2 step 4;
   b2, k, the item list, 002 §5e.)
6. The rule that draws the null is registered, not left in code. (The isotropic null
   deciding the (a) reading, 002 §5g.)
7. Duplicate key = refusal, never "latest file wins". (autoresearch
   `analyze_mi_channel.collect()`.)
8. R1 — Each metric brings its own measured floor, per metric and per state; inheritance is
   forbidden. (The (a) floor from the replicate; the ablation floor nearly reused for ρ; the
   floor is state-dependent, 002 §5h.)
9. R2 — Before an exact coincidence of two independently computed values is treated as
   evidence, measure the base rate of such coincidences at that precision. (Lattice 2⁻¹⁶,
   spread 25–46 steps, base rate ≈ 1/35, observed 1–2 %, 002 §5h.)
10. R3 — A comment does not assert the behaviour of code, least of all of a third-party
    library; a claim about a library's behaviour is a test, not a comment. (Protocol 13
    §3.11; the clamp incident: `splice_a.py:232-236` asserted flyvis does not clamp at
    evaluation, `network.py:527` says otherwise, 002 §5g.)
11. R4 — A witness must have the power to veto the result; a control that is only recorded
    is not a control. (`run_individual.py:571-573` vs `:635`; §3.9 "refuses to report
    without them"; 002 §5h.)
12. The script that produced a recorded number is committed before the run, and every
    output carries the script's hash. (`splice_a.py` revised after the run, 002 §5g.)
13. A quantity that entered the analysis through more than one formatter names its file in
    every argument at that precision. (`r4()` 4-decimal CSVs of night 1 vs the full-float
    four-way CSV of night 2, 002 §5h.)
14. A new readout is a new registration; it never judges a registered hypothesis after the
    data exist. (Row B, the ablation profile, MI in autoresearch: UNINFORMATIVE by its own
    pre-registration.)
15. Any table in a record is verified by recomputation from the primary file, not by reading —
    AND the primary file is verified by reading the code that produced it, not by
    recomputation. Recomputation catches a label/value mismatch; it cannot catch an error the
    primary file itself carries. (2026-09-15: five reviewer figures — a 40× noise ratio, an
    "unreachable region", "six invariants", a distance table with labels swapped in two
    columns — caught by someone else's recomputation, none by re-reading; and drop-k computed
    on 250,008 instead of the registered 250,000, which no recomputation from its CSV could
    have caught; 002 §5e/§5h/§5i.)
16. If a script prints a verdict, its verdict text must be the rule's text verbatim (or a
    pointer to it), and the verdict must be derived from every clause of the rule, not from
    one operationalised clause; a divergence between the printed verdict and the rule is a
    defect of the artefact, to be overridden in the record with a dated note, never silently
    edited in the artefact. (2026-09-16: `ablation_reading.json`'s `verdict.text` printed only
    the operational clause of `docs/next-session-plan.md` §2a — "exceeds 2863" — and called
    seeds 3 and 4 POSITIVE, while the clause it dropped ("of the size seen in seed 2, +21,157")
    was not met and R2 itself did not repeat; overridden in the record, not edited in the json —
    003 §6.)

17. A numeric control must not compare one measurement with an extremum of another on a
    quantised quantity. Before writing a numeric gate: (a) state what it proves — identity of
    code is proven by a code diff, not by a number; (b) derive any threshold from more than one
    realisation (several processes), with a documented margin, never from a single run; (c) check
    the quantisation step of the gated quantity (for float32 per-item losses: the ulp of the
    largest per-item values) and that the threshold is a multiple of it with room; (d) ask what
    the probability is that a correct implementation fails the gate — if it cannot be answered,
    the gate is not ready. (2026-09-16: step 1 stopped twice falsely at its copy-fidelity gate —
    exact equality, then one quantisation step over a 10-pair floor; Ark 20:23Z, Zcode 20:24Z;
    records in results/diagnostics/gray/.)

## Language

**The repository is in English.** Every tracked file — prose, code comments, UI strings, board
entries, READMEs — is written in English. The rule is the owner's, stated in the DPC Research
group's project description and again on 2026-09-20 after `atlas.html` opened in Russian.

**Quotations.** Most Russian in this repository is a verbatim quote of a participant (Mike, Ark,
Zcode). A quote is given in faithful English translation inside the same quotation marks, marked
**"(translated from Russian)"** once per quote, placed like the attribution beside it. Names,
dates, UTC times and message numbers stay exactly as recorded. The translation keeps the tone,
including profanity; it never changes who said what or what was decided. Where a Russian term was
used as a label inside English prose, it is translated and the translation is then used
consistently everywhere.

**No exemptions (since 2026-09-23).** The repository is English throughout, with no exemptions.
Until 2026-09-23 `idea.md` was kept as the Russian original beside an English `idea_en.md`, and
seven registered or hash-pinned files kept their Russian lines so that their recorded hashes
would keep reproducing. On 2026-09-23, on Mike's word, all of them were translated: `idea.md`
now holds the English text and `idea_en.md` is gone. **The originals are not lost — they live in
git history** (the last revision with Russian is commit `2488ecb`). A recorded sha256 of a
translated file refers to that original revision and reproduces from it, not from the current
file; each translated file carries a dated note saying so, and
[docs/notes/2026-09-23-translated-pinned-files.md](notes/2026-09-23-translated-pinned-files.md)
lists every such file, its old and new sha256, the records that cite the old one, and how to
reproduce it from history.

**Pinned files from here on.** A registered document or a file whose bytes are pinned by a
sha256 recorded elsewhere must not change silently — a language edit moves the hash just as a
content edit does. It is written in English from the start; if it ever has to change, the
change is dated in the file and listed beside the old hash, as the 2026-09-23 note does.

Related: `docs/tool-hardening-package.md` (the code fixes these rules imply for this
repository, with falsifiers); `docs/preregistration-cheap-vs-expensive.md` §7 (void
conditions).
