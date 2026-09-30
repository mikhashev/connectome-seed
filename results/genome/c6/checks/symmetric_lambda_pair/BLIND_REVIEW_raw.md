# Blind review, raw output (verbatim)

Blind review launched by the owner (Mike) in a separate Claude Code session, from the brief
`dpc-research/blind-review-brief-symmetric-pair.md` (outside the repo); returned to the owner and posted
by him in the DPC Research chat on 2026-09-30 16:47 UTC. Transcribed below without edits by CC.

---

Written for: the owner of the run, as the blind-review report the brief asked me to return (not saved into the repo).

Verdict: follows. The recorded outcome (branch (b); Object 2: B reads G, A reads U) follows from the outputs under the registration's rules, and the run was done in the registered order. Every value I recomputed by my own route equals the recorded one, including the float diagnostic to the last bit. Two precision notes below change no branch and no label.

Checks
1. Integrity, pins, order

item	result
registration LF sha256 at e7d973f, b44d383, f8e11db, HEAD	8865753e…7808 on all four, equals REGISTRATION_SHA256_LF_PINNED; file has LF endings, so raw = LF
PREDICTION_COMMIT_PINNED	e7d973f63cf2…401a9b, the full hash of the prediction commit
e7d973f	touches one file (the registration, 258 insertions); parent of b44d383; b44d383 parent of f8e11db
HEAD in RESULT.md / result.json	b44d383…3150; porcelain recorded empty
tree clean then	f8e11db adds only .gitattributes, RESULT.md, result.json, run.log on top of b44d383; every hashed input is byte-identical at b44d383 and HEAD
18 input hashes in result.json	all equal the LF sha256 of the files at b44d383; raw store 3c20e837…6006 equals the file and its SHA256SUMS line
recorded this_script_sha256_lf	1a084350…86da = the committed script at b44d383 (unchanged at HEAD)
order in time	commits 23:09:48, 23:10:05, 23:10:49 (+07:00); result.json utc 16:10:35Z = 23:10:35 local, so the run ended 30 s after the pin commit and 14 s before the output commit; my recomputation of the same three measurements takes 19 s on this machine, so the window is consistent
2. Object 1, recomputed by my own route. I did not use fit_at_A, train_shortcut, float_p, cert_search or the K-globals swap. I called the rule's P.train through the full registered path with the grid forced to one value (the fold loop runs), decoded with P.decode on block cells I built from type names, took the float fit from fit_existence directly, and ran best_auc from the original survey.py in docs/prereg-scripts with the registered staging and seeds 93300–93307.

object	mine	recorded
control, λ = 1	1024/1024 exact and TAU, 0 ties, 2 levels (0.12499997812209568, 0.8750000218779044), gap 0.7500000437558088; all 64 p bit-equal to real||block||rule	same
ceil_100_A quantised	0.5 = 512/1024: 0 wins, 1024 ties, 1 level (every p = 0.5)	same
ceil_100_A_float	0.5, 0 wins, 1024 ties, 1 level	same
cert_A	1024/1024 at stage 1, all 5 refines and both deep runs; search, Fraction and registered-AUC counts agree; spread 0; TAU 1.0	1/1, same
max |u·v| at λ = 100	3.289222246986234e-19	identical
Extra: block A's y is exactly the rank-1 board (ON×T4 ∪ OFF×T5), so the explicit member u = sign(ON), v = sign(T4), a = b = 0 alone certifies 1024/1024 without any search. Why the fit at λ = 100 is exactly 0.5: every source and every target has 4 of 8 present, so N1's ridge returns a = b = c = 0 (O = 0 on all 64 cells); both source role groups are exactly half present, so W = 0; λ = 100 shrinks u·v to 1e-19; the refit of c gives p = 0.5 everywhere. The value is the all-ties floor, not a partially failing fit. This is also CC's stated reason (N1 anchor 0.5) borne out.

3. Object 2, on the stored files. B's rule row: λ ko/full/block = 1/1/100, so of rule #2.1's three fits only the block-only one chose 100. Applying K.read_label and K.label_text myself to B's stored rows with only ceiling_block := 0.9624060150375939 (= 384/399 from block_b_ceil1/result.json, exact = TAU) gives G, deciding by the G clause: both D1 readings "-", every p_P > 0.10 (smallest BF_4 0.2442), gate passed; text identical to RESULT.md. KA.read_label/label_text on A's rows with ceiling_block := 0.5 gives U, "failed fit…", text identical. Reading controls: stored ceilings reproduce U/G and the stored texts for both blocks; p_P and leg_S_passes present for the primary and BF_1..4. B's stored readable is True and equals the script's derivation.

Precision note: "every other input the label reads came from λ = 1" is broader than the files support. BF_3's and BF_4's p_P come from knockout fits that selected λ = 3, and leg_S_passes rests on 99 shuffle fits that selected λ = 100 in 97–99 of 99 cases. Neither decides here (W needs p_P ≤ 0.0125; the BF p_P are ≥ 0.2442), and the run's lambda_provenance_B discloses both. The registration's own text (rule #2.1's fits, plus the shuffle fits) is accurate.

4. Section 3 trees on my values. cert 1 ≥ 0.90, so not (a); quantised and float both below 0.90, so not (d); (b). Not at the cut (0.5 outside [0.88, 0.92]); no ULP split on any object; TAU branch identical. Pair table A/1 G, A/100 U, B/1 G, B/100 U as printed.

5. Implementation and tests. tree reads (a), then (d), then (b)/(c), on exact values with the TAU branch beside; cert_ok_of compares the Fraction to 9/10. The control stops on exact ≠ 1.0, exact ≠ TAU, or p not bit-equal, then prints CONTROL_FAILED, writes stop_record.json, exits 1 and computes nothing else; the stored control and both reading controls run in gate_checks before any fit; refusals cover pin None or mismatch, prediction commit not an ancestor, dirty tree (whole repo), existing output. All line references in the registration resolve to the named functions. pytest: 54 passed in 0.40 s.

6. Predictions. Ark (A falls at λ = 100): yes. Zcode item 1 (below 0.90): yes; falsifier not met. Zcode item 2 (B reads G): yes, with the registration's note that the stored p_P 0.4795 stays. CC: below 0.90 in 0.50–0.70 (0.5000 sits at the lower edge, the floor), cert ≥ 0.90, no decoder split, branch (b), B reads G: all confirmed.

What I ran
One process, CPU, Python 3.10.20 / numpy 2.2.6 from tools/.venv with PYTHONUTF8=1. My script lived in C:\Users\mikha\AppData\Local\Temp\tmp.zoIa8huMAE (mktemp -d). Total 19.4 s: control fit 0.8 s, λ = 100 fit 0.7 s, cert search 16.3 s, label readings under 1 s. Hash checks and pytest a few seconds. No file was written in the repo (bytecode and pytest cache disabled; git status clean afterwards).

Not checked, and exposure
The emptiness of the porcelain at run time beyond the recorded string and the output commit's contents. Where stdout was captured: run.log has CRLF endings, is not gitignored and would have tripped the whole-repo porcelain check, so it was captured outside the repo and copied in; I cannot see where.
B's ceil_1 = 384/399 is taken from the hash-pinned block_b_ceil1/result.json, not recomputed. The stored p_P, n_ge and BF rows of both blocks are taken as stored, as the registration says.
The interpreter is the same venv the run used, so the environment is not independent.
The consent line and chat context are forbidden sources and were not opened.
Exposure: commit subjects (no values) and the auto-loaded memory index in my system prompt, whose entries name no result of this run; no memory file, chat, READING_NOTES, brief, retrospective, BLIND_REVIEW file or orchestrator scratch was opened.
