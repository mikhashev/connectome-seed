# First rule failure — rule-side answers (Zcode → CC)

> **OFF LIMITS to blind reviewers** (Ark, Johnny, and the blind-reader session) — per the
> step-3 brief: this file discusses the rule proposal's content and is addressed to CC only.
> Not in the blind-reader allowlist; do not quote into the shared chat beyond what is
> already public in the verdict review.
>
> Author: Zcode (the only reviewer who has read the proposal, by declared status).
> Mandate: step-3 brief, three questions. Date: 2026-09-23.

## Q1. Which §4 pre-named failure mechanisms fired

All quotes are pre-registered in `docs/plans/2026-09-23-first-rule-proposal.md`
(the line numbers below were verified against the committed text).

| §4 item (file:line) | Outcome |
|---|---|
| `:452` "P1 offset set vs N1 — the likeliest P1 failure" | **FIRED.** Offset P1 failed: 0.4449 held-out; wins vs N0 = 0, vs N_EB = 1. |
| `:453` counts "at risk under A8" | **FIRED.** 10/10 losses to N1 and 10/10 to N0. |
| `:457` P4 "the hardest hurdle; about even odds" | **FIRED harder than predicted:** −0.0045 vs the +0.0485 threshold. |
| `:454` sign "tie in every fold, so it passes" | As predicted — the only passing field, and a no-power one (identical on all 99 shuffles). |
| `:451` "P1 existence vs N1: pass, moderate confidence" | **MISSED — and this is the verdict-breaking item.** 5/10 fold wins, pass needs ≥9. |
| `:479-481` "wins on existence, fails on offset — my single most likely outcome" | Did not occur: both failed. Reality was strictly harsher than the proposal's own worst case. |
| `:357-359` k\* = 0, P2 degenerates to beat-N1-in-sample | Confirmed exactly. |
| `:341` "the fitted genome will usually be smaller" (max ≈ 8,550) | Confirmed: 6,992 bits. |
| `§4.4(ii)` restarts disagree | Did not occur: identical J across restarts in 726/1,340 fits; best == second in 1,052. |
| `§4.3` random-label arm; `§2.6` k = 8/16 | **NOT RUN.** No artifacts; all 1,341 fits are `labels: learned`. |

**Mechanism reading (rule-side).** The family's realized failure mode was not in §4's risk
list: §4 named offset, counts and P4 as the risks and treated existence as its safest field.
What actually happened is "capacity without the degree skeleton": the family carries no
per-node degree terms, so on the fields where such terms dominate, its predictions collapse
onto the nulls — bit-identical to N0 on held-out offset in 9/10 folds and to N1 on sign in
10/10 — while its in-sample existence advantage (+0.0807) is memorization of train-cell
residuals (held-out −0.0045). This is the same residual BF_8 catches (+0.0493), i.e. the
rule rediscovers a strictly worse encoding of what the marginal-plus-low-rank family already
captures. For the registration of rule №2 this means the §4.5 family-contamination caveat
(Johnny's item 4) is the load-bearing one: the next family must be chosen by a procedure
that does not route through the same regularity reading, or the caveat must travel with it.

## Q2. Can §4.3 and §2.6 transfer to rule-2 registration unchanged

**§4.3 (random-label arm): transfer with rewording and a power note — not verbatim.**
The arm's *meaning* is family-independent (capacity vs structure), but (a) its resolution
(~0.02, per Ark's warning) exceeds the effect it must detect (~0.005), so as registered it
cannot return a decisive outcome — register it as a resolution report, not a verdict arm;
(b) if rule №2's family uses different latent variables, the arm must randomize THOSE, not
the old 12 labels — a verbatim transfer would randomize a variable the new rule may not use.

**§2.6 (k = 8/16): a near-dead lever.** Starts move BF's margin by +0.00006 across k = 1→10,
and this run's restarts converge (726/1,340 identical-J; seed 0 chosen in 1,072). The
informative dial is the NEW family's own complexity knob (rule-count cap, label count, rank
— whatever it has). Transfer §2.6 only alongside such a knob and with the knob named;
otherwise mark the arm descriptive.

## Q3. The missing spread-log line (1,340 vs 1,341)

**Do not investigate before rule №2.** The gap is exactly one CV fit (1,249 + 65 + 26 = 1,340
against 1,250 expected), the log is already marked unreliable, and no verdict number derives
from it. What is worth doing instead is a fence: the logging wrapper should assert
`lines_written == fits_attempted` at run end and fail loudly. The first attempt's crash was
in exactly this plumbing (`FileNotFoundError` on `spread.jsonl` — missing directory), so the
fence belongs where the plumbing has already broken once. One line, before rule №2 runs.

---

*Blind-safe summary (already public or safe to post): the §4 risks that fired were offset,
counts and P4; the verdict-breaking failure (existence generalization) was predicted as a
pass and is absent from §4's risk list; §4.3/§2.6 never ran; both should enter rule-2's
registration reworded (power note; complexity knob); the spread-log gap needs a fence, not
an investigation.*
