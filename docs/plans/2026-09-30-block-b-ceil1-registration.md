# Registration: rule #2.1 on the real block B at a fixed lambda = 1 (`ceil_1`) and `cert`

**Post-data registration. Not blind to:** block B's registered verdict and all its numbers
(U, "failed fit: rule #2.1 cannot hold the block even when trained on it alone"; `ceiling_block`
0.7744 at lambda 100; BF_1..BF_4 block ceilings at lambda 1: 0.9649, 1.0, 1.0, 1.0; N1 0.7882); the
414-board lambda law (`natural_fit_failure_replication/READING_NOTES.md` section 6: `lambda_c`
takes only 1 and 100 on 414 boards, the 247 at 100 carry |u.v| <= 1.31e-15, the 167 at 1 all pass);
the calibration's outcomes C2 (fit side witnessed, forced only) and C6 (no rank-limit witness on
block B's shape) and the replication's outcome RP1 (171 of 300 fresh certified boards fail at
lambda_c = 100, 165 of them read FF-sel); and the (iii-b) diagnostic on the recorded fits (four
readings, no refit, no natural gap). **Revision 1, the prediction commit (Mike, DPC Research chat, 2026-09-30 13:40 UTC: run it). Nothing is fitted or run by this file.**

## 0. The question, in plain words

Rule #2.1's block-only fit on the real block B chose lambda = 100 and scored 0.7744. Would the same
fit, with lambda **fixed at 1**, hold the block (>= 0.90)?

- **If yes**, block B's U is an artifact of the lambda choice (FF-sel): the fit could hold the block,
  the selector did not let it.
- **If no**, the U is a structural or optimiser limit (or a decoder limit, see section 3): the
  word "cannot" in B's label was right.

Nobody has computed this number. B's raw store holds no lambda = 1 record for rule #2.1 on the block
view (6 records: rule lambda 100, BF_1..4 lambda 1, N1).

## 1. Objects

Definitions are those of `docs/plans/2026-09-29-failed-fit-branch-calibration-registration.md`
("the calibration"); nothing is redefined here.

| object | definition | printed as |
|---|---|---|
| `cert` on B's real pattern | calibration section 6 item 1: the survey's capacity search on the 40-cell pattern (19 present, 21 absent, 399 pairs), budget of rev 1.9 section 6, exact `Fraction` count is the certificate | fraction, float, exact and `_tau` (section 6a) |
| `ceil_1` | calibration section 6 item 2 and section 3: rule #2.1's block-only fit on the real block with `LAMBDAS = [1]` (S-C4b shortcut), **quantised**, the registered object | exact and `_tau` (section 6a) |
| `ceil_1_float` | the same fit, float `fit_existence` output before quantisation (S-C4a) | exact and `_tau` |
| `ceil_1_starts100` | the same at 100 starts; the calibration script computes it (`separator_fits`), so it is included; **a diagnostic, it decides nothing** | float and quantised, exact and `_tau` |

Same 10 starts, same block mask and same bank (H.REAL) as B's real run. The fits use no new seed;
`cert` uses the calibration's seeds 93300-93307 on a pattern no earlier `cert` searched.

## 2. CONTROL (must pass before any value is read)

- The script first prints the sha256 of every input: B's raw store `raw_fits_real.json.gz`, the bank
  files of B's pin table, the three scripts it imports, the survey copy, this registration (LF).
- It then recomputes rule #2.1's block-only fit on the real block at **lambda = 100** through the
  same route as `ceil_1` and must reproduce `ceiling_block` = **0.7744360902255639** (= 309/399: 303 wins and
  12 ties of 399 pairs; the same number as 0.774436090225564 to 15 digits, which is how Ark printed it) **bit for bit**, **and** the exact and the `_tau` readings must be equal
  (the minimum gap between adjacent `p` levels on B's block is 3.2e-3, five orders above TAU = 1e-9).
- If either fails: **STOP**, print `CONTROL_FAILED`, compute and print nothing else, write
  `stop_record.json`. A control that fails is a defect of the script or environment, not a finding,
  and is never answered by re-pinning.
- Printed, not a stop: whether the fit's 40 `p` values are bit-equal to the stored ones.

## 3. Reading tree (fixed before the value; read in this order)

`cert` is read first.

- **(a) `cert` < 0.90** => a rank limit of the class on a real block, the first on a real bank
  (C6 declared none); this **outranks** the lambda reading.
- **(b) `cert` >= 0.90 and `ceil_1` < 0.90** => the label stands; the sub-kind FF-struct / FF-opt /
  FF-quant is not separated (calibration section 6).
- **(c) `cert` >= 0.90, `ceil_1` >= 0.90 and `ceil_1_float` >= 0.90** => **FF-sel on the real block**:
  the U is the lambda choice; the word "cannot" in B's label is wider than the measurement.
- **(d) DECODER SPLIT.** `ceil_1_float` < 0.90 <= `ceil_1` (quantised), or the reverse => the verdict
  is decided by the 5-bit decoder, not the fit: a separate outcome, neither (b) nor (c). In the
  script (d) is read after (a) and before (b)/(c), since (b)'s "`ceil_1` < 0.90" alone would
  otherwise swallow the reverse direction.
- **Rider.** If `ceil_1` is within +-0.02 of 0.90, i.e. in [0.88, 0.92], the reading is "at the cut",
  not a side; branch (b) or (c) is printed with that qualifier.
- **Tie and ulp.** Every branch is read on the exact values (the registered form). If the exact and
  the `_tau` readings of `ceil_1` fall on different sides of 0.90 the row is flagged
  `GATE_ULP_SPLIT` per calibration section 6a: the branch follows the exact value, the `_tau`
  branch is printed beside it. The same for `cert` (`CERT_ULP_SPLIT`) and `ceil_1_float`.

## 4. What it changes

No registered label is edited. The outcome adds a **dated reading line beside B's verdict** in
`results/genome/c6/checks/knockout_regrow_block_b/READING_NOTES.md`, and feeds the collapsed-lambda
declaration draft (`docs/plans/2026-09-29-collapsed-lambda-verdict-class-registration.md`, section 1.4,
the two real blocks). Branch (c) would make block B a natural FF-sel instance on a real block; (b)
would make B's collapse a structural limit; (a) would be reported first and separately.

## 5. Predictions (all: inference, not measurement)

**These are quoted verbatim, in Russian, as posted in the DPC Research chat (the one allowed
exception to English: quoted chat text). An English one-line gloss follows each. All times are
2026-09-29 UTC.** Every prediction below is **inference, not measurement**; Johnny asked for the
label "inference from family + 414-law, not measurement" and it applies to all of them.

### 5.1 Ark, 16:32:19 UTC, section 5 (prediction, falsifier, rider)

> **Прогноз: `ceil_1`(rule, block, B) ≥ 0.90**, большая часть массы в **0.93–0.97** (это интерквартильный диапазон вылеченного класса, а не придуманная полоса).
>
> **Фальсификатор:** < 0.90 ⇒ метка «cannot» стоит, подвид FF-struct/opt, первый экземпляр класса на реальном банке.
>
> **Райдер, который надо зарегистрировать вместе с прогнозом:** из 171 провала **26 сидят в ±0.02 от отсечки**. Если B сядет туда же — честное чтение **«у отсечки»**, а не сторона; иначе порог назначит вердикт вместо прибора.

Gloss: `ceil_1` >= 0.90, mass in 0.93-0.97 (the interquartile range of the 165 cured failures);
falsifier < 0.90 keeps the label; rider: 26 of 171 failures sit within +-0.02 of the cut, read "at
the cut".

### 5.2 Ark, 16:32:19 UTC, section 4 (decision tree)

> - **`cert` < 0.90** ⇒ мир-предел ранга, и это **первый экземпляр на реальном банке** (C6 объявлял, что такого нет; на 50 досках профиля 2,6,4,4,3 минимум был 0.9825). Такая находка **важнее** чтения про λ;
> - **`cert` ≥ 0.90, `ceil_1` < 0.90** ⇒ FF-struct/opt, метка стоит;
> - **оба ≥ 0.90** ⇒ U — целиком про выбор λ, FF-sel впервые на реальном блоке.

Gloss: the tree of section 3 above, `cert` first, a `cert` below 0.90 outranks the lambda reading.

### 5.3 Zcode, 16:46:18 UTC (two predictions, the decoder branch, the exact/tau line)

> 1. **`cert` (реальный узор B) ≥ 0.9649.** Основание — не вера, а §16: float-фит BF_1 (0.964912) — член свободного класса на этой форме (W — эффект столбца), значит `cap` ≥ 0.9649 ещё до поиска. Предсказание: поиск даст ≥ 0.9649, скорее выше. Фальсификатор: ниже — тогда §16-цепь (равенство классов на этой форме) падает, и это отдельная находка.
> 2. **`ceil_1` (rule, block, B) ≥ 0.90, масса в 0.93–0.97.** Со-подписываю IQR Арка и добавляю своё основание: N1 блока B = 0.7882 < 0.90 — блок **не** аддитивно-пройдённый (не класс доски 41), поэтому проход при λ = 1 может прийти только через взаимодействие, а оно при λ = 1 живо (fc_anchor на полном виде: |u·v| 1.84). Фальсификатор: < 0.90 — FF-struct/opt на реальном блоке, метка стоит.
>
> Если случится **float < 0.90 ≤ квантованный** — это класс `DECODER_SPLIT_AT_LC` (j=49/145/161/266, зеркало FF-quant, доска 41): вердикт решает 5-битный декодер, а не фит. Это **третья ветвь** — не «FF-sel подтверждён» и не «метка стоит». Назвать её в правиле чтения **сейчас, до фита**, иначе при таком исходе форму будут выбирать под ответ. Моё предсказание: расщепления не будет — оба ≥ 0.90.
>
> И одна строка гигиены: пары exact/tau обязательны у обоих чисел (на B зарегистрированные фиты имели зазор ≥ 1.8e-5, но это новый фит на реальном банке).

Gloss: `cert` >= 0.9649 (because BF_1's float fit is a member of the free class); `ceil_1` >= 0.90 with
mass in 0.93-0.97 (N1 alone is 0.7882, so a pass at lambda 1 must come through the interaction);
the decoder split is a third branch and no split is predicted; exact/tau pairs are required for
both numbers.

### 5.4 CC, 16:25:29 UTC (prediction)

> **Мой прогноз до значения:** ≥ 0.90. Основания: соседи по семье при λ = 1 держат B (0.9649–1.0), а на 414 досках нет ни одной, где λ = 1 не прошла бы там, где проходил выбранный λ. **Но оговорка @Johnny верна:** BF — другой фит, так что для rule #2.1 это инференс, не замер.

Gloss: `ceil_1` >= 0.90, because the family's neighbours at lambda 1 hold B and no board of 414 fails at
lambda 1 where the chosen lambda passed; BF is another fit, so this is inference.

### 5.5 Johnny, 16:37:08 UTC (the status line)

> Предсказание CC (≥ 0.90) — **инференс**, не замер: 414-закон про *тот же* фит на синтетических досках, а rule #2.1 на B при λ=1 — новый фит, не в 414. BF_1–4 — другие фиты. CC это уже назвал. В коммите предсказания пометить: «inference from family + 414-law, not measurement».

Gloss: CC's prediction is inference, since the 414-law is about the same fit on synthetic boards and
rule #2.1 on B at lambda 1 is a new fit; mark it "inference from family + 414-law, not measurement".

### 5.6 Ark, 17:30:33 UTC, item 3 (the premise of Zcode's `cert` prediction)

> **3. Одно возражение к прогнозу Zcode по `cert` — и оно не про числа, а про посылку.** Zcode предсказывает `cert` ≥ 0.9649, опираясь на то, что float-фит BF_1 (0.9649) — **член свободного класса** на форме B. Но это ровно то место, где rev 1.5 ослабила формулировку: **«включение, не равенство»**. При включении (free ⊆ класс rule #2.1) из члена большего класса нижняя граница на `cert` **не следует** — следует только `cert` ≤ cap(класса). Нижнюю границу даёт **равенство** классов на этой форме, а оно помечено как прочитанное из кода, не измеренное.
>
> Практически: прогноз можно оставить, но в коммите он должен нести **свою посылку** («опирается на равенство F = free на форме B, которое в rev 1.5 понижено до включения») — либо Zcode заменит основание. Иначе через месяц `cert`-число прочтут как подтверждение равенства, которого мы не измеряли.

Gloss: Zcode's `cert` >= 0.9649 rests on equality of the free class with rule #2.1's class on B's
form, which calibration rev 1.5 downgraded to inclusion; **the prediction carries that premise, and
a `cert` value is NOT a measurement of that equality.**

## 6. Cost

One process, CPU only, no GPU. Expected seconds to minutes: two lambda-forced fits plus one at 100
starts (the calibration measured about 30 CPU-s for its separator's fits per board) and one `cert`
search (about 26.5 CPU-s in the calibration). Under the 30-minute line, so no extra word is needed
before the run.

## 7. Script and pins

- Script: `results/genome/c6/checks/block_b_ceil1.py`; tests:
  `results/genome/c6/checks/test_block_b_ceil1.py`; outputs (committed, refuse to overwrite):
  `results/genome/c6/checks/block_b_ceil1/RESULT.md` and `result.json`.
- `REGISTRATION_SHA256_LF_PINNED` and `PREDICTION_COMMIT_PINNED` are `None` in the script while this
  registration is under review, and the script refuses to run the real measurement.
- **Two-commit order.** (1) The **registration commit** (this file, final revision) is the
  **prediction commit**: the predictions of section 5 and the tree of section 3 are frozen before
  any value exists. (2) The **script pin commit** then sets `REGISTRATION_SHA256_LF_PINNED` (LF
  sha256 of this file) and `PREDICTION_COMMIT_PINNED` (the commit of step 1). (3) The run, from that
  clean commit. The script also pins the raw store (`2461d921...398c6`) and the LF hashes of the B
  script, the calibration script and the replication script it imports.
