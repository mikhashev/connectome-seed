# connectome-seed: project video storyboard (script, not a render)

**Length ceiling: 2:00, set by Mike, DPC Research chat 2026-09-24 13:39 UTC.**
**Revision 3:** 2026-09-24 UTC, by CC (subagent). Draft only: nothing rendered, nothing committed,
no repository file changed. Revisions 1 and 2 are summarised under "History" and in the changelogs
at the end.
**Direction for the look, set by Mike (DPC Research chat 2026-09-24 13:41 UTC):** less text;
everything must be understandable visually; it has to look stunning. So in this revision the picture
is the primary channel and the voice is secondary. Captions are 8 words or fewer. There are no
tables or dense cards on screen. P-labels, file names and sources appear only in the end card and in
the video description.
**Length, measured:** every scene's voice-over was synthesised with the same TTS as the first video
(pocket-tts, voice `alba`, processed exactly as `tools/viz/bank_narration.py` does: resample to
48 kHz, `trim_silence`, `compress_pauses`). Voice alone: **108.65 s, 317 words**. With leads and
holds: **1:55.45**. The measured table is §3.7; the clips are in
`connectome-seed-data/renderings/project_video/vo_measure/rev3/`.
**Repository state read:** `master` at `98d11a8` (connectome-seed). That commit ("Bring status lines
up to date before the project video") changed `README.md`, `ROADMAP.md`, `VISION.md` and
`results/genome/c6/README.md`, so some line numbers differ from revision 2 (which read `1ac12b0`).
In particular, README's "nothing is grown until the condition below has a number" is now
`README.md:103` (it was `:97`).
**Sources:** every factual claim is followed by a `Source` line giving file:line. Paths are relative
to the repository root. Line numbers are for `98d11a8`; every
one was re-opened for this revision.
**Result values:** the script contains no result value (no margin, SD, ratio, p-value or fold
count). Outcomes are stated in the words of the outcome notes and README.
**Caveats:** every claim that stays keeps its caveat, in the voice. Claims whose caveat would not
fit were dropped (listed under "Revision 3"). Cutting rule (two-way check, Ark and Muse): when a
claim is cut, its caveat goes with it; when a caveat is cut, its claim goes with it. A caveat that
outlives its claim reads as a claim.
**Vocabulary rule:** a term from the five slabs is always said and shown with the slab's own word:
"grammar", "body + brain", "operators", "youth", "fitness".

---

## 1. Logline

connectome-seed aims to "learn to make an elephant out of a fly": grow a lineage of artificial
organisms from a real connectome, seeded by a *grammar*, a rule that produces wiring. Today the team
works on one object, a column-averaged template of the fly visual system (the bank), and on rules
that must regenerate it. Growing waits on a condition that is not met, not refuted and found to be
underspecified. Three rules were registered and none has passed; a low-rank term separates a second
brain from its shuffles, with a flag at the headline rank. The next question, whether the two brains
share one structure, will be registered before any number exists. Nothing has been grown.

---

## 2. Visual style (the whole film)

Buildable procedurally in Blender Python (`bpy`, geometry nodes), no downloaded assets, rendered in
EEVEE on a GPU with about 4 GB free.

**Palette (fixed for the whole film)**

| role | colour | used for |
|---|---|---|
| background | near-black blue `#05070D`, a faint radial gradient to `#0B1020` | every scene |
| the bank, "real" | grey-blue emission `#7FA3C8` | hex columns, discs |
| sign +1 / −1 | warm `#FFB36B` / cool `#6BB8FF` | connection curves |
| FAIL / failed gate | red `#E5484D` | rule 1, rule 2.1 frame, grammar's "none passed" mark |
| flag / caveat | amber `#F5A524` | the lowest-reference notch, the family thread, the FlyWire flag |
| planned / not built | white wire at about 15 % alpha | wireframe slabs, the tree, the rule sphere |
| text | off-white `#E8ECF4`, one sans font (Blender's built-in `Bfont`), never bold | captions, one-word labels |

Green is never used. Nothing passed as a whole, so nothing gets a pass colour.

**The three states, as three materials (the core visual code)**
- **Solid = exists and was run.** Principled BSDF, roughness 0.35, with an emission of 1.5 to 3
  strength in its colour. With bloom it reads as lit glass.
- **Paused = ran, then paused.** The same mesh at emission 0.2 with a desaturated base, plus a
  floating pause glyph (two thin emissive bars). It is visibly the same object, switched down.
- **Planned = designed, not built.** A Wireframe modifier (thickness 0.004) with an emission-only
  material at about 15 % alpha (Blend mode "Blended", or Alpha Hashed), with no faces rendered.
- A one-line legend shows these three once, in scene 1, and again in scene 6: "solid: run ·
  dim: paused · wire: planned" (6 words).

**Lighting and render**
- World: black, strength 0. All light comes from emissive geometry, plus one very low area light
  (strength about 20 W, cool) from above to give the solids a rim.
- Bloom: in Blender 4.2+ EEVEE, a compositor Glare node (Fog Glow, threshold about 0.8, size 7).
  On older EEVEE, the scene bloom setting.
- Depth of field on (camera f-stop about 2.0 to 2.8), focus on the object being named. Background
  elements fall soft.
- Volumetrics off (memory). Soft shadows off. 1920 × 1080, 24 fps, 64 render samples.
- Film: a very light vignette and grain in the compositor.

**Camera language**
- One camera move per scene, slow and eased (Bezier in/out): a push-in, a quarter orbit or a
  lateral track. No cuts inside a scene. Scenes join with a 12-frame cross-dissolve.
- Framing is centred and symmetric for "state" shots (slabs), low and three-quarter for "object"
  shots (the bank).

**Motion rhythm**
- One visual change per spoken beat, landing on the word that names it.
- Things appear by growth (rings, arcs drawing along their length, tiles filling), never by pop.
- Steady emission only: no pulses travelling along curves (it would suggest neural activity; the
  bank is a static wiring template).

**Data already exported:** `connectome-seed-data/renderings/bank_scene/scene_data.json`, written by
`tools/viz/export_bank_scene_data.py`, holds `types` (65, in flyvis layout order), `real` (604
cells, each with sign and offset kernel), `shuffled` (the harness's own `shuffled_bank(REAL,
seed=0)`) and `focus` (the Mi9 → T4d kernel). Source: `tools/viz/export_bank_scene_data.py:5-12, 38`.
Scenes 2 and 5 reuse it; `tools/viz/bank_scene.py` / `bank_animation.py` are a starting point. The
lattice shown is extent 5 (91 columns per full-stride type), to keep geometry light; this is a
lattice parameter, not a count of the fly's columns
(`docs/notes/2026-09-20-what-is-the-genome-here.md:122-124`; `GLOSSARY.md:49`).

**Narration pipeline:** `tools/viz/bank_narration.py` can read the voice-over if it is laid out like
`bank_video_script.py` (`id`, `text`, `say`, `lead`, `hold`). The `say` strings spell
"connectome-seed" as "Connectome seed", "flyvis" as "fly vis", "FlyWire" as "Fly Wire" and "#2.1"
as "two point one". The exact texts measured are in `vo_measure/rev3/vo_texts.json` and
`vo_measure/rev3/measured.json`.

---

## 3. Scenes

Each scene's **Picture** is written first: it must carry the scene's idea with the sound off.
Durations are the measured voice plus lead and hold (§3.7).

### Scene 1: The goal, and five points
- **Duration:** 0:00.00 to 0:21.88 (21.88 s)
- **Caption:** "Goal: an elephant from a fly" (6 words). Legend, small, bottom left, in the last
  4 s: "solid: run · dim: paused · wire: planned".
- **Picture (primary):** Black. One hex column ignites at centre, grey-blue. Rings of columns grow
  out of it into a flat disc (91 columns, a distance-driven reveal): the real connectome the lineage
  starts from. The camera tilts from top-down to about 30° and the disc settles low in frame. Five
  thin upright slabs then rise behind it in a row, one per spoken point, each with its one-word label
  ("grammar", "body + brain", "operators", "youth", "fitness"), each brightening as it is named.
  They land in their states: "grammar" solid and glowing; "youth" dimmed with a pause glyph; the
  other three wireframe. On "evolutionary tree", a large tree draws itself behind the slabs as
  thin wire curves (a procedural L-system, 3 to 4 levels of binary branching). It stays wireframe.
  With sound off the viewer sees: a seed of real wiring, five parts of a plan in three different
  states, and a tree that is only drawn, not built.
- **Voice-over (secondary):** "connectome-seed's goal, in its author's words: learn to make an
  elephant out of a fly, by growing a lineage of creatures from a real connectome. Five points: a
  heritable grammar as the seed; body and brain growing together; operators on a living graph; a
  short youth before measurement; fitness with many objectives. The artefact: an evolutionary
  tree."
- **Source:**
  - "to learn to make an elephant out of a fly", the author's restatement of 2026-09-19:
    `VISION.md:24-27`; `README.md:71-73`.
  - "grow a lineage of creatures from a real connectome-seed": `idea.md:14-15`; `README.md:73-74`.
  - Points 1 to 5: `idea.md:17-44`. The tree as main artefact: `idea.md:46-48`.
  - Slab states: grammar is the main line (`docs/decisions/004-grammar-is-the-main-line.md:63-65`);
    point 4's test is paused, not cancelled (`docs/decisions/004-grammar-is-the-main-line.md:96-98`;
    `VISION.md:63-64` for point 4 being that test); points 2, 3 and 5 are designed for and not run
    (`README.md:102-103`; `ROADMAP.md:435-440`).

### Scene 2: The seed is a rule; the bank is what it must regenerate
- **Duration:** 0:21.88 to 0:37.58 (15.70 s)
- **Caption:** first "Seed: a rule that writes wiring" (6 words), then "The bank: a column-averaged
  template" (5 words).
- **Picture (primary):** The "grammar" slab slides forward and folds into a small icosphere, drawn
  as wireframe (planned: no rule has passed). From it, four thin particle streams draw a
  hypothetical wiring, one beat per spoken item: hex discs appear (which types exist), curves
  connect some of them (which pairs connect), small kernels light on neighbouring columns (where),
  and each curve takes its warm or cool colour (which sign). This drawing stays wireframe. The camera
  then pulls down to reveal, below it, the real bank, solid: 65 stacked, semi-transparent hex discs
  in three bands, 604 connection curves in warm and cool. **Column averaging, shown:** on one pair
  (Mi9 → T4d), several faint, slightly different kernels hover over separate columns, merge into one
  averaged kernel, and that one kernel is copied onto every column of the disc. A dotted line runs
  from the wire icosphere down to the solid bank: the rule's job is to regenerate this. The camera
  makes a quarter orbit around the bank.
- **Voice-over (secondary):** "The seed is a grammar: a rule that produces the wiring. Which types
  exist, which pairs connect, where, and with which sign. Such a rule must regenerate one object,
  the bank: flyvis's template of the fly visual system, averaged over columns."
- **Source:**
  - Grammar = a rule that produces the wiring table: which types exist, which pairs connect, at
    which offsets, with which signs: `VISION.md:198-201`; `GLOSSARY.md:90`.
  - "the seed is not all the weights, but a heritable grammar": `idea.md:17`.
  - The bank is "the object a rule has to regenerate": `GLOSSARY.md:45`.
  - flyvis's template; column-averaged, type-level; not one animal's wiring; no per-neuron weights;
    the model copies each mean to every column:
    `docs/notes/2026-09-23-where-our-bank-comes-from.md:20-27, 218-222`.
  - Mi9 → T4d as the flyvis paper's own example kernel:
    `docs/notes/2026-09-23-where-our-bank-comes-from.md:100-102`;
    `tools/viz/export_bank_scene_data.py:38`.
  - The number of types and pairs (65, 604) is shown as geometry only, not said or captioned;
    the counts are in `GLOSSARY.md:45, 47`.

### Scene 3: The condition that gates growing
- **Duration:** 0:37.58 to 0:53.61 (16.03 s)
- **Caption:** "Cheap ≈ expensive? Not met, not refuted." (6 words), then under it, smaller:
  "underspecified" (1 word).
- **Picture (primary):** The "youth" slab from scene 1 comes forward and opens into two tall
  vertical rails, left short (cheap) and right tall (expensive), drawn as solid light rods. Six small
  spheres (individuals) sit on each rail, joined across by thin lines. On the expensive rail, two of
  the spheres carry two faint "ghost" copies each (their repeat runs) that drift and overlap their
  neighbours, so the six cannot be put in order: the lines cross in a tangle rather than run level.
  No axis, no numbers. Then the rails dim to the paused material, and a pause glyph fades in over
  them. The rails stay visible (paused, not cancelled). The camera pushes in slowly across the
  tangle.
- **Voice-over (secondary):** "Before anything is grown, a condition must hold: a cheap evaluation
  of an individual, point four's youth, must be consistent with an expensive one. After ten runs it
  is not met, not refuted, and found to be underspecified. The line is paused, not cancelled."
- **Source:**
  - "Before anything is grown, show that a cheap evaluation of an individual is consistent with an
    expensive one": `VISION.md:54-55`; the condition verbatim: `docs/decisions/002-file-under-condition.md:49-51`;
    `README.md:165`.
  - The condition is point 4 ("youth") turned into a test: `VISION.md:63-66`.
  - "not met, it is not refuted, and it has been found to be underspecified":
    `docs/decisions/002-file-under-condition.md:113`.
  - "The expensive side does not rank. Ten runs exist — six individuals, two of them run three
    times": `docs/decisions/002-file-under-condition.md:117-118` (the tangle on the expensive rail).
  - Paused, not cancelled: `docs/decisions/004-grammar-is-the-main-line.md:96-98`; `README.md:27`.
  - ADR-002 is on `docs/blind-author-exclusions.txt`; only its words are used, none of its values.

### Scene 4: Three rules, none passed; what was fixed first, and what was not
- **Duration:** 0:53.61 to 1:16.81 (23.20 s)
- **Caption:** "Three rules. None passed." (4 words), then at the end "Exam fixed first. Family chosen
  after." (6 words).
- **Picture (primary):**
  1. The "grammar" slab glows (the main line). In front of it, the exam arrives first: a flat,
     solid plate (the bank's type-pair table seen from above), and a thin seal ring closes around its
     edge and locks with a click of light. It is sealed before anything else appears.
  2. Three small crystals (rules) float in from the left, one per spoken beat.
     - Rule 1 reaches the plate, turns red and cracks.
     - Rule 2 meets a gate arch before the plate. The arch turns red; the crystal stops there and
       dims. It never touches the plate.
     - Rule 2.1 reaches the plate. The plate shows two thin layers above it. The upper layer,
       "which pairs connect", fills with four ticks one after another; the fourth tick lights only
       half, in amber, with a small low notch (passed only against the lowest reference). The lower
       layer, "where pairs sit", turns red. Then a red frame closes around the whole crystal and
       plate: FAIL. The existence layer stays lit inside the red frame, so it cannot read as a pass.
  3. On "What was not": an amber thread draws from a small glowing plate off to the side (the
     bank's regularity numbers, faceless, no digits) to rules 2 and 2.1. That plate was already
     lit before the two crystals formed, and the thread carries no seal. The seal ring on the exam
     stays intact.
  The layer labels are two words each ("which pairs connect", "where pairs sit"); no P-labels,
  no check names. The camera tracks slowly left to right with the crystals.
- **Voice-over (secondary):** "The grammar is now the main line. Three rules were registered; none
  has passed. Rule two-point-one failed on where pairs sit; on which pairs connect it passed all
  four checks, the last only against the lowest reference. The exam and what counts as failure were
  written before any run. What was not: the family behind rules two and two-point-one, chosen after
  its author had read the bank's regularity numbers."
- **On screen, for the caveat (Mike's decision 1):** a small second line under the end caption
  reads "rules #2 and #2.1".
- **Source:**
  - Grammar as main line: `docs/decisions/004-grammar-is-the-main-line.md:63-65`.
  - Three registered, two run; rule #1 failed; rule #2 stopped at its gates and never reached the
    harness; rule #2.1 FAIL on offset only, existence passed P1, P2, P3 and P4, P4 against BF_1
    only: `results/genome/c6/README.md:5-9`; `README.md:28-35`.
  - Rule #2: two of seven gates failed; "a failed gate stops the work"; not run on C6:
    `docs/notes/2026-09-23-second-rule-stopped-at-gates.md:10-16`.
  - Offset failed P1, P2 and P3; existence passed P1, P2 and P3:
    `docs/notes/2026-09-23-rule-2-1-c6-what-it-showed.md:35-37, 44`. P4 passed: `:49`.
  - P4 passed only against BF_1, the lowest of the known BF reference points, disclosed by the
    rule's author before the run: `docs/notes/2026-09-23-rule-2-1-c6-what-it-showed.md:249`.
  - The exam written before any rule existed: `GLOSSARY.md:123`. A registration is "committed
    before the value it governs": `GLOSSARY.md:153`. "Registration before build, build before run,
    run once. Every choice fixed in writing first": `docs/briefs/2026-09-24-next-session-handover.md:56`.
  - The family caveat, in Mike's form (decision 1, DPC Research chat 2026-09-24 13:39 UTC):
    "Rule #2's family was chosen by an author who had seen rule #1's real-bank results and
    whole-bank regularity numbers. That caveat travels with any rule #2.1 result":
    `docs/plans/2026-09-23-rule-2-1-registration.md:371-373`; also
    `docs/notes/2026-09-23-rule-2-1-c6-what-it-showed.md:250`.

### Scene 5: A second brain, with a flag
- **Duration:** 1:16.81 to 1:35.22 (18.41 s)
- **Caption:** (a) while the pillars rise: "Rank 1: sealed before the run." (6 words), with a small
  seal glyph (the same seal as scene 4, "written before the run", §6) placed on the row of pillars
  before they rise; (b) after the amber flag is planted on the flyvis rank-1 pillar: "FlyWire
  separates. flyvis near-ties — flag." (6 words). Stack labels: "FlyWire", "flyvis, same 30 types".
- **Picture (primary):** The bank moves left and shrinks to 30 discs: "flyvis, same 30 types". A
  second stack of 30 discs rises on the right: "FlyWire", its kernels visibly more compact. The two
  stacks stay apart the whole scene; they are never overlaid or merged.
  **The shuffle, shown once:** behind each stack, a fan of 99 ghost copies spreads out (wire, 15 %
  alpha). In one of them the connection curves slide to new endpoints while small in/out bars
  beside each disc keep exactly their height: the wiring is rewired, each type's inputs and
  outputs are kept.
  **The result, shown as height:** under each stack, four short rank pillars (1, 2, 3, 4). Before
  the pillars rise, the small seal glyph appears on the row (caption a): the headline reading, r = 1
  for both arms together, was fixed before this run. For each rank, a bright pillar (the real bank)
  rises beside a grey band (the 99 shuffles).
  Under FlyWire, all four bright pillars rise clear above their bands. Under flyvis at ranks 2 to 4
  they rise clear; at rank 1 the bright pillar stops level with the top of its band, and an amber
  flag plants there (caption b). No values on the pillars. The camera pulls back slowly so both
  stacks and the flag are in frame.
- **Voice-over (secondary):** "On a second brain, one female fly from FlyWire, a fitted low-rank
  term separates the real bank from all 99 shuffles that rewire who connects to whom, at every rank
  tested. But flyvis, cut to the same thirty types, nearly tied at the headline rank: by the reading
  written in advance, a flag."
- **Source:**
  - The 30-type FlyWire bank, built by a registered procedure; flyvis restricted to the same 30
    types as the control arm: `docs/briefs/2026-09-24-next-session-handover.md:23-31`.
  - FlyWire v783 is one female fly: `docs/plans/2026-09-24-flywire-bf-p3-registration.md:173`.
  - "a rank-r term fitted on the residual of N1 separates the real 30-type bank from all 99 of its
    degree-preserving shuffles, at every rank tested": `docs/notes/2026-09-24-flywire-p3-what-it-showed.md:104-107`;
    `README.md:41-45`.
  - Ranks 1 to 4; FlyWire-30 branch A at every rank; flyvis-30 C at r = 1, A at r = 2 to 4:
    `docs/notes/2026-09-24-flywire-p3-what-it-showed.md:22-31` (branch column only; no values).
  - Headline r = 1; the registered row "read as a flag to re-examine both fits, not as a
    substantive finding on its own"; the flyvis-30 C at r = 1 is a near tie:
    `docs/notes/2026-09-24-flywire-p3-what-it-showed.md:37-44`; `README.md:41-43`.
  - The shuffle keeps each type's inputs and outputs (degree-preserving) and rewires the pairs:
    `GLOSSARY.md:139`.
  - FlyWire has no offset beyond 2 (the compact kernels): `docs/notes/2026-09-24-flywire-p3-what-it-showed.md:98-99`.
  - Caption (a), the seal: "The headline is r = 1, for continuity with the flyvis BF_1 result":
    `docs/plans/2026-09-24-flywire-bf-p3-registration.md:461`; "Pre-stated joint reading, headline
    r = 1 for both arms (Mike, chat 2026-09-24 07:28 UTC)": `:493`.
  - Caption (b), the flag: the flag belongs to the pair, not to flyvis alone — "re-examine both
    fits": `docs/plans/2026-09-24-flywire-bf-p3-registration.md:493-502`.

### Scene 6: Where it stands, and what is next
- **Duration:** 1:35.22 to 1:55.45 (20.23 s, including a 3.0 s end hold)
- **Caption:** "Nothing grown yet. Next: one structure?" (6 words). Legend returns, small, bottom
  left.
- **Picture (primary):** Back to the five slabs and the tree of scene 1, same states, each slab
  brightening as it is named: "grammar" solid, with a small red mark (no rule passed); "youth"
  dimmed with its pause glyph; "body + brain", "operators", "fitness" wireframe. **The gate, shown:**
  between the slabs and the tree stands a closed gate arch; on it, an empty number slot, a dash
  with no digits. A thin line runs from the "youth" slab to the slot: the tree waits on that
  condition, which has no number yet. The tree stays wireframe; only its root becomes solid, a small
  grey-blue hex prism (generation zero, the bank). Then the two stacks of scene 5 appear small, far
  apart, with a dotted bridge between them and a question mark on it. Before the bridge a small
  sealed plate (like the exam's seal in scene 4) lands first. The camera pulls back and holds for
  3 s.
- **End card (inside the 3 s hold and in the video description):** credits in the wording of
  `tools/viz/bank_video_script.py:28-35`; the repository link "github.com/mikhashev/connectome-seed"
  (Mike, 2026-09-24: the link, not a commit hash); the sources list (file names, P-labels) goes in
  the description, not on screen mid-film. Note: this storyboard's own `Source` line numbers are
  pinned to `98d11a8` (content read for this revision).
- **Voice-over (secondary):** "Grammar: no rule has passed. Youth: paused. Body and brain, operators
  and fitness: designed for, not run. Nothing is grown until the condition on youth has a number.
  Next: do the two brains share one structure? That test will be registered before any number
  exists."
- **Source:**
  - No rule has passed: `results/genome/c6/README.md:5-9`.
  - Point 4's test paused, not cancelled: `docs/decisions/004-grammar-is-the-main-line.md:96-98`.
  - Points 2, 3 and 5 "designed for and not run"; "nothing is grown until the condition below has
    a number": `README.md:102-103` (the condition: `README.md:165`; it is point 4 turned into a test:
    `VISION.md:63-64`); `ROADMAP.md:435-440`.
  - Next: question (ii), transfer, not tested, needs its own registration: `README.md:46-48`;
    `docs/notes/2026-09-24-flywire-p3-what-it-showed.md:111-112`; points a registration "must
    settle before any value exists": `docs/briefs/2026-09-24-next-session-handover.md:35-52`.
  - The generation-zero bank is the root of the evolutionary tree: `GLOSSARY.md:46`.

### 3.7 Measured timing

Synthesised 2026-09-24 with pocket-tts, voice `alba`, through the Python at
`…/scratchpad/ttsvenv/Scripts/python.exe`, processed with `bank_narration.py`'s own `resample`,
`trim_silence` and `compress_pauses`. Leads and holds follow `bank_video_script.py`'s pattern (0.8 s
lead on the first clip, 0.3 s otherwise; 0.3 s holds; 3.0 s end hold). The script and the exact
texts are `vo_measure/rev3/vo_measure.py` (the revision 2 script with the output folder changed)
and `vo_measure/rev3/vo_texts.json`; lengths are in `vo_measure/rev3/measured.json`.

| scene | voice (s) | lead | hold | scene (s) | timeline | words | clip |
|---|---|---|---|---|---|---|---|
| 1 | 20.78 | 0.8 | 0.3 | 21.88 | 0:00.00 to 0:21.88 | 58 | `S01_d27186b1d1.wav` |
| 2 | 15.10 | 0.3 | 0.3 | 15.70 | 0:21.88 to 0:37.58 | 42 | `S02_b542d4dacf.wav` |
| 3 | 15.43 | 0.3 | 0.3 | 16.03 | 0:37.58 to 0:53.61 | 44 | `S03_199ce62f02.wav` |
| 4 | 22.60 | 0.3 | 0.3 | 23.20 | 0:53.61 to 1:16.81 | 73 | `S04_ae4c5d0dfe.wav` |
| 5 | 17.81 | 0.3 | 0.3 | 18.41 | 1:16.81 to 1:35.22 | 55 | `S05_ddf292e136.wav` |
| 6 | 16.93 | 0.3 | 3.0 | 20.23 | 1:35.22 to 1:55.45 | 45 | `S06_71fb4d7c93.wav` |
| **total** | **108.65** | | | **115.45** | **1:55.45** | **317** | |

Margin under the ceiling: 4.55 s. TTS length varies by a few tenths of a second between syntheses
of the same text, so re-measure after any edit. The 12-frame cross-dissolves overlap the scenes and
add no time.

---

## 4. Status honesty

Exactly as the repository states it at `98d11a8`. Nothing here is rounded upward.

**Done (exists and was run):**
- The C6 specification and harness are committed (`README.md:28-30`).
- BF_1 alone on P3: branch A (`docs/notes/2026-09-24-bf1-p3-what-it-showed.md:13`). BF_1 there is
  fitted on its own on top of N1, not the same fitted object as the rank-1 term inside rule #2.1
  (`:56-58`). Not in the video (dropped for length).
- The second brain, question (i), was run once. On FlyWire-30 the term separates at every rank
  tested; the registered joint reading at the headline rank is a flag
  (`docs/notes/2026-09-24-flywire-p3-what-it-showed.md:37-44, 104-114`; `README.md:41-45`).

**Failed:**
- Rule #1 ran on C6 and failed (`results/genome/c6/README.md:6`).
- Rule #2 failed two of its seven gates and is not run on C6
  (`docs/notes/2026-09-23-second-rule-stopped-at-gates.md:10-16`).
- Rule #2.1: verdict FAIL, on the offset field only. Existence passed P1 to P4, P4 against BF_1
  only, the lowest reference point (`README.md:33-34`; `results/genome/c6/README.md:7-8`;
  `docs/notes/2026-09-23-rule-2-1-c6-what-it-showed.md:35-37, 44, 49, 249`). The family was chosen
  after the regularity numbers were read
  (`docs/plans/2026-09-23-rule-2-1-registration.md:371-373`; note `:250`).

**Not met / open:**
- **ADR-002's condition is not met, not refuted, found to be underspecified**
  (`docs/decisions/002-file-under-condition.md:51, 113`). The measurement line is paused, not
  cancelled, since 2026-09-20 (`docs/decisions/004-grammar-is-the-main-line.md:96-98`). Nothing is
  grown until it has a number (`README.md:103`).
- **Question (ii), transfer between the two brains, is open**: not registered, not run
  (`README.md:46-48`; `docs/briefs/2026-09-24-next-session-handover.md:35-52`).
- The flag at r = 1 on the FlyWire run has no registered rule that could lift it
  (`docs/notes/2026-09-24-flywire-p3-what-it-showed.md:76-79, 113-114`).
- **Points 2, 3 and 5 are designed for, not run. Nothing is grown** (`README.md:102-103`;
  `ROADMAP.md:435-440`).

---

## 5. Claims I could not source (kept out of the scenes)

- **That passing C6 gates the later points of the plan.** No file says it. What gates growing is
  the ADR-002 condition (`README.md:103`; `ROADMAP.md:435-440`); scene 6 shows that gate instead.
- **"Four of five slabs are still wireframe."** Point 4's test ran and is paused, so the
  repository gives three states, not two.
- **Any date or schedule** for question (ii), for resuming the measurement line, or for growing
  anything. No file gives one.
- **What a grown organism or body would look like.** No design file exists, so the video shows no
  creature, fly or elephant geometry.
- **A single overall "progress" figure.** The repository has none.
- **That any result generalises to individual flies.** The rule #2.1 note says the finding answers
  "is a type-level template compressible?", not "is an individual brain compressible?"
  (`docs/notes/2026-09-23-rule-2-1-c6-what-it-showed.md:252`).
- **Why the FlyWire and flyvis rank profiles differ.** The note offers only hypotheses
  (`docs/notes/2026-09-24-flywire-p3-what-it-showed.md:90-100`).
- **"the condition on youth"** (scene 6 voice) is a paraphrase, not a repository phrase. It rests on
  `README.md:103` ("the condition below") plus `VISION.md:63-64` (the condition "is the idea's
  point 4 turned into a test"). Flagged for reviewers.

---

## 6. What could mislead

- **Fly or elephant imagery.** It would suggest that a creature exists. None does. The goal stays
  in words and abstract geometry.
- **A growing tree.** Keep it wireframe. Only the generation-zero root is solid.
- **Glow and bloom.** The polished look must not read as activity. Emission is steady; nothing
  pulses or travels along a curve.
- **Connection curves.** Each is a type-level, column-averaged mean copied to every column, not a
  neuron-to-neuron wire. Scene 2 shows the averaging.
- **The rule 2.1 existence layer.** Four lit ticks can read as "almost passed". The whole crystal
  and plate sit inside a red FAIL frame, the fourth tick is half-lit amber, and nothing is green.
- **Rule 2 at the gate.** It must never touch the exam plate: it never ran on C6.
- **"Separates" (scene 5).** It means only that a fitted term does better on the real bank than on
  its shuffles. It does not mean the rule is a genome, or that the two brains share a structure.
- **Two brains side by side.** Never overlay or morph one stack into the other. Transfer was not
  tested (scene 6 puts a question mark on the bridge).
- **Pillars without values (scene 5).** They show order only (above the band, or level with it).
  No numbers, no p-values: with 99 shuffles the smallest printable p is a floor
  (`docs/notes/2026-09-23-rule-2-1-c6-what-it-showed.md:251`).
- **The tangle on the expensive rail (scene 3).** A qualitative picture of "the expensive side does
  not rank". No axis or values: the underlying values are in files on the exclusion list.
- **The pause glyph.** The repository says "paused, not cancelled". Keep the dimmed rails and slab
  visible.
- **The seal ring (scenes 4 and 6).** It stands for "written before the run". It must not appear on
  the family choice, which was made after the numbers were read.

---

## 7. Every number in the script, with its source

| number (as used) | where used | source |
|---|---|---|
| 5 points | S1, S6 | `idea.md:17-44` |
| 65 discs, 604 curves (geometry only, not said) | S2 | `GLOSSARY.md:45, 47` |
| extent 5, 91 columns (geometry only) | S1, S2 | `docs/notes/2026-09-20-what-is-the-genome-here.md:122-124`; `GLOSSARY.md:49` |
| 10 runs, 6 individuals, 2 run three times (spheres and ghosts) | S3 | `docs/decisions/002-file-under-condition.md:117-118` |
| 3 rules registered | S4 | `results/genome/c6/README.md:5` |
| 4 checks, the last only against the lowest reference | S4 | `docs/notes/2026-09-23-rule-2-1-c6-what-it-showed.md:35-37, 44, 49, 249`; `README.md:33-34` |
| 1 female fly (FlyWire v783) | S5 | `docs/plans/2026-09-24-flywire-bf-p3-registration.md:173` |
| 30 types | S5 | `docs/briefs/2026-09-24-next-session-handover.md:23-26` |
| 99 shuffles | S5 | `GLOSSARY.md:139`; `docs/notes/2026-09-24-flywire-p3-what-it-showed.md:105-106` |
| ranks 1 to 4 | S5 (pillars) | `docs/notes/2026-09-24-flywire-p3-what-it-showed.md:22-31` (rank and branch columns only) |
| 2 brains | S6 | `README.md:46-48` |

**Deliberately not used:** every margin, SD, ratio, p-value and fold count. Several sit in files on
`docs/blind-author-exclusions.txt`.

---

## Eye pass before publication (render vs Picture blocks)

Check the render against the written Picture blocks on these points before anything is published:

- The seal on the exam stays intact while the amber "what was not" thread runs, with no seal of its
  own (S4).
- The fourth tick on the existence layer is half-lit, inside the red FAIL frame (S4).
- Rule 2's crystal never touches the exam plate (S4).
- Solid, dim and wire are visually distinguishable at a glance (S1, S6).
- The amber flag is planted on the flyvis rank-1 pillar, not on FlyWire's (S5).
- In scene 5, the seal glyph appears on the pillar row before the pillars rise, and the two
  captions appear in order: the seal caption first, the flag caption after the flag is planted (S5).
- A thin line is visible from the "youth" slab to the empty number slot on the gate (S6).
- The legend ("solid: run · dim: paused · wire: planned") is readable where it appears (S1, S6).
- The end-card commit hash resolves on the public repository.

---

## History

- **Revision 1** (2026-09-24): target "2-3 minutes". **Revision 2** (2026-09-24): target
  "2:30-3:30", measured 3:27.90. Both targets were set by CC, the coordinating agent, in its briefs
  to subagents, not by Mike. Revision 2's target was set after the 3:20 length was already known.
- **Mike's first length decision is the 2:00 ceiling** (DPC Research chat 2026-09-24 13:39 UTC),
  followed by his direction on the look (13:41 UTC): less text, understandable visually, stunning.

---

## Revision 3 (2026-09-24): Mike's decisions of 13:39 and 13:41 UTC

**Changes, one line each**
1. Header: length ceiling 2:00 set by Mike; the "2:30 to 3:30" target removed; History section added.
2. Measured length 3:27.90 → 1:58.58 (voice 197.50 s → 111.78 s, 614 → 330 words); clips re-synthesised into `vo_measure/rev3/`.
3. Twelve scenes → six: S1+S2 → scene 1; S3+S4 (+S5's "regenerate" point) → scene 2; S6 → scene 3; S7+S9 → scene 4; S8+S11 → scene 5; S12 → scene 6.
4. Family caveat moved into scene 4's voice in Mike's form ("The exam and what counts as failure were written before any run. What was not: the family behind rules two and two-point-one, chosen after its author had read the bank's regularity numbers."); on screen "rules #2 and #2.1"; the PENDING MIKE marker removed. Source: `docs/plans/2026-09-23-rule-2-1-registration.md:371-373`; note `:250`.
5. The gate on growing is now said and shown in scene 6: "Nothing is grown until the condition on youth has a number" (Muse's causal link). Source: `README.md:103`.
6. Scene 1 caption "Goal: an elephant from a fly"; the curriculum and "not all the weights" on-screen lines removed.
7. Every caption cut to 8 words or fewer; the S4 provenance tag, footnotes, the S7 field layers, the S9 cards and 4 × 4 grid, and the S10 on-screen notes removed from the screen.
8. Visual style specified for the whole film (§2): palette, three state materials, bloom, depth of field, one camera move per scene, steady emission, EEVEE on about 4 GB.
9. Each scene's Picture rewritten as the primary channel: column averaging shown (S2), the tangle that does not rank (S3), the sealed exam and the amber thread for the family (S4), pillars against shuffle bands (S5), the gate with an empty number slot (S6).
10. Rule 2's voice line shortened to "stopped at its own gates" (the wording of `results/genome/c6/README.md:6`).
11. P-labels, check names and file names moved to the end card and description.
12. Line numbers re-read at `98d11a8`: README moved (e.g. `:97` → `:103`, goal quote `:65-67` → `:71-74`, rule #2.1 line now lists P2), ROADMAP `:434-439` → `:435-440`.

**Dropped for length (the video no longer says or shows these)**
- "Not by emulating a fly and calling it an elephant" (the idea's opening distinction).
- The curriculum fly → beetle → six-legged truck → small quadruped → heavy quadruped; "not all the weights".
- "The author named the first step: write down how the genome is represented".
- The bank's provenance: FIB-25 + FIB-19, "at least two female flies", lamina sources whose flies were not checked, merging by the larger estimate. (Dropped with its caveat, not stripped of it.)
- The counts 65 cell types and 604 compiled type pairs (with the 605 json entries / Lawf1 → Lawf1 footnote); now geometry only.
- Layout bands 8 / 21 + 2 / 34, stride [3, 2], the extent 5 vs 15 footnote.
- Scene 5 in full: one production over a lookup table; a bigger disc adds columns, not types; "an elephant needs a rule that generates the table"; 2,355 offset rows.
- In the condition scene: "the expensive side did not rank" (now only pictured), 25,000 vs 250,000 iterations, "On 20 September".
- The exam mechanics: the name C6, four fields, unseen pairs / folds, per-type baselines, the one-tenth length limit, 4,225 cells.
- The shuffle's definition as a scene, "real structure should beat every one of 99 shuffles", the perfect-copy (oracle) lesson.
- The separate "test written before the run" sentence per rule (now carried once, by Mike's caveat sentence).
- Rule 2's "two of seven gates" and "by its written plan"; rule 2.1's per-check card (P1 to P4 by field, "not scored", "computed, not used", "length within the limit").
- Scene 10 in full: BF_1 alone on the full bank (branch A), with its caveat "fitted on its own on top of N1; not the same fitted object as the term inside rule #2.1"; "most shuffled margins are exactly zero; none is positive"; the λ mechanism checked on one fold.
- In the FlyWire scene: "right optic lobe", "built by a registered procedure", "99 shuffles" as a spoken count for flyvis-30 (the voice keeps "all 99" for FlyWire).
- "Back to the five points", "That is the honest state", and the reachability endpoint (already out in revision 2).

---

## Revision 3.1 (2026-09-24): reviews by Ark, Johnny, Muse

1. S5 voice: "a low-rank term fitted on its own" → "a fitted low-rank term" (Johnny) — the source
   says "a rank-r term fitted on the residual of N1"
   (`docs/notes/2026-09-24-flywire-p3-what-it-showed.md:104-107`); "on its own" was a leftover of
   the dropped BF_1 caveat and inverted the source.
2. S5 captions added: "Rank 1: sealed before the run." with the seal glyph on the pillar row before
   it rises; "FlyWire separates. flyvis near-ties — flag." replaces "Second brain: it separates,
   with a flag" (Ark) — the flag belongs to the pair, not to flyvis alone
   (`docs/plans/2026-09-24-flywire-bf-p3-registration.md:461, 493-502`).
3. S4 voice: "Rule one failed. Rule two stopped at its own gates." removed (Mike, via reviewers: less
   text); the Picture block already carries it (crystal 1 cracks on the slab, crystal 2 dims at the
   arch and never touches the slab; caption "Three rules. None passed."), confirmed, not added.
4. S6 source for "generation zero": `GLOSSARY.md:74` (the register entry) → `GLOSSARY.md:46` (the
   generation-zero bank entry) (Muse) — the film names the bank, not the register.
5. Header "Caveats" line: added the two-way cutting check — "When a claim is cut, its caveat goes
   with it; when a caveat is cut, its claim goes with it. A caveat that outlives its claim reads as
   a claim." (Ark, Muse).
6. No "why the condition matters" line added (Muse withdrew it; it would read as a verdict on the
   project).
7. New section "Eye pass before publication (render vs Picture blocks)" added, listing the seal/
   thread, the half-lit fourth tick, rule 2 never touching the slab, solid/dim/wire distinguishability,
   the flag on the correct pillar, S5 caption/seal ordering, the youth-to-slot thread, legend
   readability and the end-card hash resolving (Johnny).
8. End card: hard-coded "98d11a8" replaced with "<commit containing
   tools/viz/project_video/storyboard.md, filled at render>"; note added that this storyboard's
   `Source` line numbers are pinned to `98d11a8` (content), an ancestor of that commit (Ark).
9. Scenes 4 and 5 re-synthesised and re-measured with the same TTS after the voice edits: voice
   111.78 s → 108.65 s (330 → 317 words); total with leads/holds 1:58.58 → 1:55.45, still under the
   2:00 ceiling (margin 4.55 s). §3.7 table and scene durations updated; new clips
   `S04_ae4c5d0dfe.wav`, `S05_ddf292e136.wav` in `vo_measure/rev3/`.

---

## Revision 2 (2026-09-24): reviews by Ark, Johnny, Muse, Zcode

Kept for the record; line numbers in this list are for `1ac12b0`.

1. S9 grid: existence passed all four checks; offset fails P1 to P3; P4 note "vs BF_1 only".
2. S10: "BF_1 fitted on its own on top of N1; inside rule #2.1 fitted jointly with X".
3. S10: the shrink-to-zero mechanism shown once, tagged as checked on one fold.
4. S6: "is consistent with"; "not met, not refuted, and found to be underspecified".
5. S4: "at least two" female flies; lamina flies not checked.
6. S4: "604 compiled type pairs"; the 605-entry footnote.
7. S9: PENDING MIKE marker for the family caveat (resolved in revision 3).
8. The method as a named idea across S7 to S12.
9. S9: plain words lead; P-numbers only on the card.
10. S7 link from C6 to the five-point plan: not sourced, dropped.
11. S12 as a return to the S2 slabs with sourced states.
12. S4 details moved to on-screen text; returning terms re-shown.
13. Timing measured, not estimated (3:27.90).
- A to G: S9 card caption; method sentence in S9; S7 back-reference ("almost everything else depends on it"); slab vocabulary; S10 caption; source-line fixes; header estimates replaced by measured totals.

### After render (2026-09-24)
- End card shows the repository link instead of a commit hash, on Mike's word (Revision 3.1 item 8
  superseded). Only the overlay layer was rebuilt; the 3D frames are unchanged.
- Eye pass of the scene 5 order, from the mp4 itself (CC): at 83.9 s the shuffle bands stand and no
  ring is drawn; at 85.3 s the seal rings round "1" on both stacks and no bright pillar has risen; at
  86.8 s the FlyWire pillars are rising. Seal before pillars: confirmed in pixels.
- End card reduced to the repository link alone, on Mike's word (DPC Research chat 2026-09-24
  16:19 UTC). Credits and "Explanatory illustration, not evidence" moved to the video description
  (`description.md`), whose last line is "Code and script: github.com/mikhashev/connectome-seed"
  (Mike, 16:20 UTC).
