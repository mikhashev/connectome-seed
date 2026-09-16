# Checklist — research repository, start here

**Status:** in force for this repository from 2026-09-15 (Mike's word «пиши чек-лист» 09:56);
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

Related: `docs/tool-hardening-package.md` (the code fixes these rules imply for this
repository, with falsifiers); `docs/preregistration-cheap-vs-expensive.md` §7 (void
conditions).
