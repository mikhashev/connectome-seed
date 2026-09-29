# Blind review: natural fit-failure replication, registered run from a9f1c82

Reviewer: a separate agent session (model Fable), 2026-09-29, briefed by CC with the allowed sources
only: the registration (rev 1.2) and the prediction commit b5513e3, this folder and the data folder,
the script and what it imports, and the two "seen" files cited in section 1. Forbidden: the
scratchpad, chat logs, memory files, retrospectives, commit messages beyond the start context. The
report below is the reviewer's, condensed and transcribed by CC.

## Verdict: follows

The recorded outcome (RP1; secondary J89-reproduced) derives from the outputs under the
registration's rules. Every board was recomputed from raw p and y and the stored cert members:
0 mismatches over 300 boards and about 125 fields each. The outcome is invariant to every
difference between b5513e3 (rev 1.1) and rev 1.2: under either text the labels are RP1 only.

## Checks

1. **Integrity and pins.** Both SHA256SUMS.txt copies verify; the registration LF sha256
   `0739ac5d...` equals the pin and the manifest; script, CAL and B script hashes at HEAD equal the
   manifest; git_head a9f1c82, tree clean within results/genome/c6 and docs/plans, registered form.
   Order from git: 6e806ae -> b5513e3 (14:15:54Z) -> 602360e (14:29:49Z) -> a9f1c82 (14:30:53Z) ->
   run 14:31:37Z (646 s) -> 29a70db. b5513e3 is an ancestor of a9f1c82 and touches only the
   registration.
2. **Freshness.** 131 unique seen patterns (z, z', 15 world boards, 99 permuted, B's 20 permuted
   ceilings) = manifest; 0 fresh-seen collisions, 0 fresh duplicates; every raw record's y equals the
   reviewer's fresh y(j).
3. **Per board.** 0 mismatches. S-R6 stops 0; cert counts agree on all 300; min cert 389/400;
   lambda only 1 and 100. Flags: GATE/CEIL_1/CERT_ULP_SPLIT 0, DECODER_SPLIT_AT_LC 3 (fresh:145, 161,
   266), CERT_BELOW_CUT 0, CERT_COUNTS_DISAGREE 0.
4. **Predictions (reviewer's counts = recorded).** N_c 300, failures 171, passes 129, rate 0.570
   (95 % CP [0.512, 0.627]). P1 hold; P2a hold; P2b hold (6 not FF-sel: fresh:40 FF-quant at
   lambda 1; fresh:146, 151, 179, 222, 229 FF-struct/opt not separated; the printed test does not
   reject); P3 hold (BF 166/139/144/144); P4' fail (114/129 = 0.884); P5 hold (171/186; 171/171;
   FF-sel 165/186). Labels: RP1. J89-reproduced on 5 boards.
5. **b5513e3 vs rev 1.2.** Prediction rows and label rows RP1-RP5 line-identical. Differences:
   (1) the P2b note and section 8 contradicted the table row at b5513e3; rev 1.2 resolved for the
   table row (stricter, committed before the run, immaterial here since 6 <= 10 < 16);
   (2) RP6's "cert counts void" became a flag, strictly a narrowing of a label condition, immaterial
   here since counts agree on all 300; (3)-(8) definitions and "as implemented" notes.
   "Consistency only" is accurate for (3)-(8); (1) and (2) resolve contradictions in the stricter
   direction or per the calibration's precedent.
6. **Missing / unlicensed:** none.

## Reservations (verdict unchanged)

- **RP5 / P2a wording.** "Any failure reading 'not separated'" is, as a substring, met by the five
  J89-row boards ("... FF-struct or FF-opt, not separated"). The script reads the row "not separated:
  rank limit or fit" (startswith), which is the registration's evident intent. A later revision
  should spell the row out.
- **RP6 narrowing** could have changed the label list in a different run.

## Exposure (the reviewer's)

Start context: git status, the five recent commit subjects (incl. 29a70db's), the memory index
titles. Also the subjects of 602360e and 6e806ae via git log, and one extra `git show --stat
602360e`. Imported the CAL and B scripts as modules; read no line of harness.py. Could not check:
that --estimate ran first, Mike's order and the reviewers' yes, the test suite, tree cleanliness
outside the two scoped folders.
