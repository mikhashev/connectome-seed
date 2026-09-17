# Brief — pre-registration note: the two b2 measurability thresholds rest on a single pair

**Date:** 2026-09-17. Proposed text only — **not applied** to
`docs/preregistration-cheap-vs-expensive.md`. Written by CC's subagent, from
`docs/preregistration-cheap-vs-expensive.md` §4 (the top-k measurability paragraph), §7 (the run
0/run 0′ replicate table and the b2 measurability paragraph), §8/§9 (review and provenance
conventions), `docs/experiments/004-night4-replicate-3prime-and-seed-5.md` §§3–4, and
`results/diagnostics/c3/README.md`.

## Where

**Section §7, "Controls, and what would invalidate the run".** Insert as a new paragraph
immediately **after** the paragraph that begins `**Added 2026-09-15 (b2, secondary; Mike's word
18:05 local «ок давай впишем»; written before seeds 1 and 2 started) — measurability of a top-k
boundary.**` and ends `...Stated as a rule now, applied once, when all N individuals are in.` —
and immediately **before** the paragraph that begins `**Proposed (CC), decision Mike +
reviewers:** run seeds 1 and 2 to 250,000 next night...`. Both anchor paragraphs are on the
committed file as of `docs/preregistration-cheap-vs-expensive.md` HEAD; the new paragraph does not
touch either one's text.

(§4's own "Measurability of the top-k boundary" paragraph and its two following review paragraphs
state the same rule in the other direction — from the boundary requirement down to the two
numbers — and are left untouched; §7 is where the numbers 12.7279 / 0.3365 are actually measured
and tabled, so that is where their evidence base belongs.)

## Text to insert (§7)

> **Observed 2026-09-17 (CC's subagent on Sonnet; `docs/experiments/004-night4-replicate-3prime-and-seed-5.md` §2, §4 and `results/diagnostics/c3/README.md`, verified by CC), changes no rule.** The two replicate differences the b2 measurability paragraph above uses as instrument resolution — 12.7279 at 250,000 and 0.3365 at C3 = 25,000 — were measured on one pair, run 0 vs run 0′ (§7's table above). A second replicate pair is now on record: seed 3, run 003 vs run 903 (night 4; runs 003 and 903 each ran first in their wave, so the pair shares a wave position — unlike run 0/run 0′, where 0′ ran second) gives **+10.4309 at 250,000** and **−5.1847 at C3 = 25,000** (`004` §2). A third throw of seed 3 is also on record: run 703, stopped cleanly after iteration 26,000 (`results/diagnostics/c3/`, run under the `--stop-after-iter` patch, commit `a8a8008`) gives **703 − 003 = −4.7583** and **703 − 903 = +0.4265**, both at 25,000. Run 703's own read noise around a local linear trend is sd 2.20 (81 reads, step 25, window 24,000–26,000) and sd 1.84 (61 reads, step 100, window 20,000–26,000), flat across lags 25–100 (`results/diagnostics/c3/README.md` §7, readings (a)/(a′)/(g)); the evaluator's own repeat spread on one fixed state (same checkpoint, same path, five in-process calls) is ≤ 2e-4 (`README.md` §2) — four orders below the C3 figure. Reported, not recomputed by CC: on the stored checkpoints between iterations 200,000 and 250,000 (15 per run, eight runs), the residual standard deviation around a local linear trend is 1.74–4.07 per run, median 2.64 (Zcode, chat 2026-09-17 07:43Z). Consequently **0.3365 is not reproduced** — the C3 read noise alone (sd 1.84–2.20) is already ~6× larger than 0.3365, and the second pair's own C3 difference (−5.1847) is ≈15× larger in magnitude and of the opposite sign — while **12.7279 is one of two observations on record**, the second pair's 250,000 difference (+10.4309) landing close to it in size and sign. **The measurability rule and every threshold in §4 and §7 stand exactly as registered.** This paragraph records only that the two numbers feeding the rule's instrument-resolution input rested on a single observation each when they were written on 2026-09-15, and that §7's own timing rule — the rule is read once, at N, when all individuals are in — is unchanged and still binds: no boundary is evaluated by this paragraph, and no ρ, X, or verdict is computed here.

## One-line §8/§9 provenance entry

Append to §9 ("Provenance"), after the existing `**Review of `rho_ci.py`, 2026-09-15:**` entry, in
the same one-line-per-event style:

> **Single-pair resolution note, 2026-09-17.** Origin: `docs/experiments/004-night4-replicate-3prime-and-seed-5.md` and `results/diagnostics/c3/README.md`, read by CC's subagent 2026-09-17; text drafted by CC's subagent on Sonnet, verified by CC, for insertion in §7. Changes no tolerance, ladder rung, N, or decision rule of (a), (b), or (b2). Applied on Mike's word **[to be filled at commit]**, DPC Research chat **[time to be filled at commit]**.

## Why here and not a rule change

Every number above is Observed with a path, exactly as this file already requires (§9's own
"Sources"/"Observed" convention). Nothing in the note computes a ρ, an X, or a verdict, and it
proposes no change to N, the ladder, the metric, the held-out split, or either measurability
threshold — a change to any of those requires a new pre-registration, written before the next N
run starts, per §7's own void-conditions paragraph. The note exists only so that a reader of §4/§7
sees, next to the 12.7279/0.3365 figures, that a second and a third observation exist and what they
show, before N is chosen and the rule is applied once.
