# The second brain (FlyWire) on P3: what the run showed

Registration: `docs/plans/2026-09-24-flywire-bf-p3-registration.md` (as run: `d12415a`).
Scripts: `results/genome/c6/checks/flywire_bank_builder.py`, `flywire_sensitivity.py`,
`flywire_bf_p3.py`. Outputs: `results/genome/c6/checks/flywire_sensitivity/` and
`results/genome/c6/checks/flywire_bf_p3/` (`RESULT.md`, `summary.json`, `per_shuffle_rank{1..4}.csv`
per arm), committed in `c3e107b`. The run started at 2026-09-24 08:56:13 UTC and ended at 09:30:02
UTC, once, with 30 workers. The FlyWire bank itself lives outside the repository
(`connectome-seed-data/FlyWire/derived/`, registration §1).

Reviews of the run: Ark 09:34, Zcode 09:43, Johnny 09:43 UTC. Every number below was checked
against the files named with it; the lambda vectors were re-read by CC from the CSVs.

## 1. Registered outcome

- **Machine check:** passed. The wrapper on the full flyvis bank gave 0.028150051052145946,
  difference 0.0.
- **Sensitivity label (§3b):** "support difference real, reading stands". The two diagnostic
  builds recovered 5 and 8 of the 69 flyvis-30 pairs missing from the FlyWire bank, with no
  offset row at `max(|du|, |dv|) >= 3` (`flywire_sensitivity/RESULT.md`).

| arm | r | real margin | shuffled max | n shuffled >= real | p | p < 0.0125 | branch |
|---|---|---|---|---|---|---|---|
| FlyWire-30 | 1 | +0.03431 | +0.00412 | 0 | 0.01 | yes | A |
| FlyWire-30 | 2 | +0.01413 | +0.00540 | 0 | 0.01 | yes | A |
| FlyWire-30 | 3 | +0.01137 | +0.00465 | 0 | 0.01 | yes | A |
| FlyWire-30 | 4 | +0.00810 | +0.00464 | 0 | 0.01 | yes | A |
| flyvis-30 | 1 | +0.00928 | +0.00930 | 1 | 0.02 | no | C |
| flyvis-30 | 2 | +0.01796 | +0.00925 | 0 | 0.01 | yes | A |
| flyvis-30 | 3 | +0.02143 | +0.00751 | 0 | 0.01 | yes | A |
| flyvis-30 | 4 | +0.02794 | +0.00693 | 0 | 0.01 | yes | A |

(`summary.json` `arms.<arm>.per_rank`.) No branch B occurred on either arm, so neither registered
negative reading applies. On the real banks no fold chose `lambda = 100` (fraction 0.00, both arms,
every rank); on the shuffles 0.67 to 0.72 of folds did.

**Joint reading, headline r = 1: FlyWire-30 A, flyvis-30 C.** The registered row (§5a, registration
line 502), verbatim: *"Unexpected direction: FlyWire separates where the flyvis restriction does
not -- read as a flag to re-examine both fits, not as a substantive finding on its own."* At r = 2,
3 and 4 both arms are A, and the registered row is "The pattern is present in the second brain."
The headline is r = 1, as registered; the other ranks are reported beside it, not promoted.

**The flyvis-30 C at r = 1 is a near tie.** Real margin 0.0092849; the one shuffle at or above it,
shuffle31, 0.0092998. The gap is −1.4978e-05 (`RESULT.md` printed it as −0.00001).

**Printed by the script (§5a):** the full-65 flyvis BF_1 was A, but flyvis-30 is not A at r = 1,
so part of the separating structure lies outside the 30 column-assigned types. See the caveat in §4.

## 2. Registered items the run did not print

- **The named outcome of §5.** "A rank that separates while r = 1 does not is its own named
  outcome: *higher-rank structure survives where rank-1 does not*." It occurred on the flyvis-30
  arm (r = 1 C; r = 2, 3, 4 A). The script does not print it; this note does (Ark, Zcode).
- **The joint-reading text.** The script printed a paraphrase of the registered row, not the row
  itself (Zcode). §1 above quotes the registered row.

## 3. "Re-examine both fits": what the lambda record shows

A rerun would repeat the same numbers (the run is deterministic), and new seeds, banks or
thresholds would be fishing. What can be examined is the per-fold lambda record the registration
required (edit 3a). Counts re-read by CC from `per_shuffle_rank{r}.csv`:

| arm | r | lambda per fold on the real bank | shuffles with the same lambda vector | their margins |
|---|---|---|---|---|
| FlyWire-30 | 1 | 1 in all 10 folds | 0 of 99 | - |
| FlyWire-30 | 2-4 | mostly 3, some 1 | 0 of 99 at every rank | - |
| flyvis-30 | 1 | 3 in all 10 folds | **4 of 99** | 0.00524, 0.00779, 0.00890, **0.00930** |
| flyvis-30 | 2 | 3 in all 10 folds | 2 of 99 | 0.00537, 0.00925 |
| flyvis-30 | 3, 4 | mostly 3, some 1 | 0 of 99 | - |

The one shuffle that beat the real flyvis-30 bank at r = 1 (shuffle31) is one of the four that made
the same internal choice of lambda. On FlyWire-30, no shuffle at any rank made the choice the real
bank made. Read plainly: the flag at r = 1 comes from a small cluster of flyvis-30 shuffles that
imitate the real bank's fit, not from an absence of structure on FlyWire (Ark, Zcode, Johnny).

**Defect of the registration, recorded, not repaired now.** The two lambda readings (§5) were
written for branch B only. The observed flag is a C, and the registration gives no lambda rule
for C. So the reading above is informative, but it is not a registered way to lift the flag
(Ark, Johnny; the same class as a diagnostic without a reading rule).

## 4. Observations that are not registered readings

Each item below was seen after the run. None changes a branch or the joint reading.

- **The rank profiles cross.** FlyWire-30 margins fall with rank (0.0343, 0.0141, 0.0114, 0.0081);
  flyvis-30 margins rise (0.0093, 0.0180, 0.0214, 0.0279). The profiles cross between r = 1 and
  r = 2, and the registered headline, r = 1, is the crossing point. Had the headline been r = 2,
  the joint reading would have been A with A. This is a property of the criterion, recorded for
  future registrations, not a reason to change this one (Ark).
- **Different bars for the two arms.** The shuffle maximum at r = 1 is 0.00930 on flyvis-30
  (density 228/900 = 0.253) and 0.00412 on FlyWire-30 (165/900 = 0.183). A denser bank may give
  a richer null, since the shuffles keep degrees. This is a hypothesis (Ark), not a measurement.
- **Caveat to the §5a line.** flyvis-30 at r = 4 reaches 0.02794, against 0.02815 for the full-65
  bank at r = 1 (99.3 %). Cutting 65 types to 30 did not remove the signal on flyvis; it moved it
  to higher ranks. So "part of the structure lies outside the 30 types" holds at r = 1 only, and
  must not be read as "the dropped types carry a unique structure" (Ark, Zcode).
- **Opposite profiles and question (ii).** Johnny reads the opposite rank profiles as an argument
  against "the same structure in both brains". The banks also differ in support (FlyWire has no
  offset beyond 2, §3b of the registration), so the profiles could differ for that reason. Either
  way, the run does not support "the same structure"; question (ii) was not tested.

## 5. What this run shows, and what it does not

**Shows:** on the FlyWire right optic lobe, built from one female fly's raw connectome by a
registered procedure, a rank-r term fitted on the residual of N1 separates the real 30-type bank
from all 99 of its degree-preserving shuffles, at every rank tested, and survives the four-rank
correction. Cross-validation kept the term in every fold on the real bank.

**Does not show:**

- **That the structure is the same as in flyvis.** Question (ii), transfer from one brain to the
  other with its own null, is a separate registration and was not run.
- **A clean control at the headline rank.** The registered joint reading at r = 1 is a flag, and
  the registration has no rule to lift it (§3).
- **Anything about the 35 dropped types on FlyWire,** or about offsets beyond 2 there.
- **Independence from the pipeline.** The sensitivity builds did not reproduce the flyvis offset
  spectrum. The difference in support between the banks is real under the registered rule, but
  what causes it (the fly, or the flyvis json's own hand edits) is not known.

## 6. Next steps (for Mike to choose)

1. **Question (ii), transfer:** fit on one bank, score on the other, with its own null (a fit on
   a shuffled source bank). This needs a new registration.
2. **Write up** the two-brain result as it stands, with the flag and the defects above.
3. **Fix the two defects** in the run script for future runs: print the named outcome of §5, and
   print registered rows verbatim. This changes no number of this run.
