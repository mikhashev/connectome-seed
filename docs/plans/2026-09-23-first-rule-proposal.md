---
**Status:** PROPOSAL, written to be registered **before** the rule meets any data it is judged on.
No rule has been fitted, run or scored. No fold file was read (none existed when this was written).
**Written by:** CC (subagent), 2026-09-23, on Mike's instruction of 2026-09-23 ("read the literature
§I.1 (Sims, Hornby & Pollack, CPPN/HyperNEAT) and propose the first rule", paraphrased from
Russian, not quoted).
**Judged by:** `docs/plans/2026-09-23-c6-control-specification.md` as it stood when this was
written: git blob `137da3b8a6637d27d7739940b16462770d0c518c`, sha256
`d64eb9db57ed8372a3347f95003529b510e04018f2ea095fd830cf69d05bb92d` (commit `9116ff9`), **plus
its "Amendment — 2026-09-23, before any harness or rule" (A1–A14)**. Another agent was writing
that amendment while this file was drafted. I read it uncommitted, in the working-copy state with
sha256 `32f2e403a30a6669c9d93ffb07acbfa3147d20c1804a853071724440a030f261`, and this file is
aligned with A1 (types handed over as indices), A4 (N1 exactly), A5 (description length, decoder
source charged), A6 (k\*, the 18-component mark), A8 (stricter P1), A9 (99 shuffles) and A11
(P4, random projection). It was then committed in `9ed0dae` with the same sha256, so what I
read is what governs. If C6 is amended again, **C6 governs**, and §4 is read against the new
text without being edited. I did not open
`results/genome/c6/` (the folds and harness).
**No measured results.** Every number below is a structural count from the bank, a number
already on record in `results/genome/bank/REGULARITY-READING.md`, or arithmetic on the C6
accounting. ADR-003 applies: whoever runs C6 on this rule reports C6's labels; §4 here is the
reading, and it is written now.
---

# The first rule: named labels, named rules, named motifs

## Summary, in plain words

The fly's wiring table says, for each of 65 × 65 ordered pairs of cell types, whether they connect,
at which neighbouring columns, how strongly and with which sign. Today that table is simply
stored. The proposed genome replaces the storing with a small vocabulary:

- **Labels.** There are 12 named "developmental labels". Each cell type either carries a label or
  does not, so a type is described by 12 yes/no marks. The labels play the part of the molecular
  tags in the genomic-bottleneck paper, but they are discrete and they have names.
- **Rules.** A rule reads "a type carrying label *i* connects to a type carrying label *j*". It
  also says which spatial motif the connection uses, in which orientation, and how strong it is.
  There are at most 40 rules.
- **Motifs.** A motif is a small named pattern of neighbouring-column offsets, such as "same
  column only" or "same column plus one neighbour", stored once and reused by many rules. The
  library holds at most 16 motifs.
- **Sign.** Each type carries a single excitatory/inhibitory mark. It is not predicted pair by
  pair.

Two types connect if **any** rule matches their labels. Every label, rule and motif has a
permanent id derived from its name, so a child can inherit a whole module from a parent and the
family tree can say where the module came from. The whole genome, including the code that reads
it, is at most about **8,800 bits**. The table it replaces is about 90,000 bits, so the genome is
under the one-tenth limit C6 sets.

**What counts as success, fixed now:** the rule passes all four parts of C6 (P1–P4), and it also
beats the same rule with **randomly assigned labels**. That second test shows the labels found
something real, and that 12 yes/no marks per type cannot simply fit anything. My own prediction,
also written now: its best chance is on *which pairs connect*, and it is least likely to win on
*which offsets*. The hardest single hurdle is C6's random-projection control (P4).

---

## 0. Sources, and how far each was read this session

Everything was fetched again today, from the URLs in
`sources/local/2026-09-20-digital-evolution/PROVENANCE.md`, into `sources/local/2026-09-23-first-rule/`
(gitignored). The one new source was fetched from its author lab's site.

| work | copy | how far I read it this session |
|---|---|---|
| Sims 1994, *Evolving Virtual Creatures*, SIGGRAPH '94 | karlsims.com PDF; sha256 byte-identical to the 2026-09-20 copy (`d924c926…`) | §2 genotype graphs (nodes, connections, recursive-limit, reflection, terminal-only), §3 nested neural graphs, §5 mutation and mating. Read via the 2026-09-20 text extraction of the same bytes. Fitness sections not re-read. |
| Hornby & Pollack 2001, *Evolving L-systems to generate virtual creatures*, Computers & Graphics 25 | UCL course copy. **Today's bytes differ from the 2026-09-20 copy** (372,736 vs 431,977 bytes; sha256 `666b1754…` vs `7193a4a6…`). Quotes were checked against the 2026-09-20 text. | §2 the P0L-system, its constraints, initialisation, mutation, recombination, experimental setup |
| Hornby & Pollack 2002, *Creating High-Level Components with a Generative Representation for Body-Brain Evolution*, Artificial Life 8(3) 223–246 | Brandeis DEMO-lab preprint (`www.demo.cs.brandeis.edu/papers/hornby_alife02.pdf`, dated 26 August 2002, 30 pp.). The text layer cannot be extracted, so pages were rendered and read as images. | pp. 1–4 (abstract, introduction, direct vs generative), p. 6 (related work), p. 8 (§3.1 L-systems), pp. 10–11 (network command set, Table 2), pp. 13–18 (Table 3 body commands, example grammar, §3.3 EA and operators, §4 setup, Fig. 4 result). **pp. 5, 7, 9, 12, 19–30 not read.** |
| Stanley 2007, *Compositional Pattern Producing Networks*, GPEM (preprint) | Wayback copy of the eplex preprint; byte-identical to the 2026-09-20 copy | §2 list of regularities, §3 (coordinate frames, composition, the CPPN graph, CPPN-NEAT). §4 experiments not re-read. |
| Stauffer is not an author; the paper is **Stanley, D'Ambrosio & Gauci 2009**, *A Hypercube-Based Indirect Encoding…*, Artificial Life 15(2) | Wayback copy of the eplex preprint; byte-identical | §1, §3 (the substrate, the four-dimensional CPPN query, the threshold, substrate configuration), the scaling experiment, §8.3, Table 1 parameters |
| Shuvaev, Lachi, Koulakov & Zador 2024, *Encoding innate ability through a genomic bottleneck*, PNAS | `sources/shuvaev-2024-genomic-bottleneck-pnas.pdf` and its text `sources/pnas_genomic_bottleneck_full.md` | pp. 2–3 (the g-network), p. 9 (Discussion), p. 10 Methods (MNIST labels and g-network). CIFAR and RL methods not re-read. |

**One correction found while reading.** The S2 design (`docs/plans/2026-09-20-genome-design-around-s2.md`
§1) says Shuvaev et al.'s genome "maps to a weight matrix through a fixed random projection". The
Methods say something else: the g-network is a small **trained** network, and its inputs are fixed
binary labels. Input-layer neurons get Gray-coded pixel coordinates, and hidden neurons get
"simple binary codes ranging from 1 to 800 since their order is of no particular importance".
The fixed and arbitrary part is the **labels**, not the decoder. This matters here, because the
natural falsifier for a learned-label rule is exactly the arbitrary-label version (§4.3). I have
not edited Ark's text; this is for Ark to confirm.

---

## 1. What the literature offers

**Sims 1994.** *Genome:* a directed graph of morphological nodes. Each node describes a body part
and a joint, carries a recursive-limit, and contains **its own nested graph of neurons**. Edges
carry placement, scale and reflection. *Decoding:* the graph is traced from the root. A node is
instanced once per path, up to its recursive-limit, so one node can yield several copies of a
limb, and each copy has "a similar but independent local control system". *Shown:* swimming,
walking, jumping and following behaviours, evolved from scratch. The paper also records that
interbreeding populations "often converge toward homogeneity". *Transfers:* reuse by
instancing: one gene, many phenotype parts. Brain modules nested inside body modules. Two mating
operators, crossover and **grafting** (point 3 of `idea.md`). *Does not transfer:* identity. Sims
aligns the two parents' nodes "as they are stored", so a node's identity is its **position** in a
list. That is exactly the competing-conventions problem NEAT later named (literature.md §I entry 18).
His nodes are also deliberately unnamed ("the genetic descriptions actually have no concept of
specific categories of functional components").

**Hornby & Pollack 2001 and 2002 (GENRE).** *Genome:* a parametric context-free L-system,
"production rules … a rule-head … a number of condition-successor pairs". Conditions are
restricted to comparing a parameter with a constant, and successors to single-operation arithmetic
(2001). *Decoding:* parallel rewriting down to a string of construction commands. In 2002 one
command language builds **both** a body (turtle commands) **and** a network (`split`,
`duplicate`, `merge`, `loop`, … Table 2). Joint commands wire the current neuron to the new joint,
so body and brain are built together. *Shown (2002):* over 10 + 10 runs, the generative encoding
reached final fitnesses of 224–8,180, against 42–744 for the direct one. It was "more than 10 times
faster, on average". *The methodological point that transfers directly:* their direct
representation **is** "an L-system with one production rule … without the repeat operator or the
ability to call production rules", so "the only difference between the two systems was the
representation". C6 asks for the same thing: in §4.2, and concretely in A5, the rule and D_k run
on one interpreter and both programs are charged by one formula.
*Also transfers:* rule heads are **named symbols** (P0, P1), so a module has an identity that
mutation and recombination can act on ("variation operators … applied only to those production
rules which were used"). *Does not transfer:* the sequential turtle language. Our object is an
unordered table of type pairs, not a construction string, and nothing in it has an order to
rewrite along.

**Stanley 2007 (CPPN).** *Genome:* a NEAT-evolved graph of composed functions (Gaussian, sine,
absolute value, …). *Decoding:* the network is queried once per phenotype element, at that
element's coordinates, "without local interaction … composition replaces interaction". *Shown:*
symmetry, repetition, repetition with variation and elaborated regularity in 2-D images, using
interactive evolution with a human chooser. There is no benchmark. *Transfers:* a kernel as a
function of coordinates. That is exactly what a spatial offset profile over `(du, dv)` is, so the
**inside** of a motif could later be a CPPN. *Does not transfer:* the CPPN's own nodes carry NEAT
historical markings, but the **phenotype** has no modules: a "repeated motif" in the output is a
pattern in a function's values, not a part anyone can cut out. There is no developmental history
either (literature.md entry 11's warning).

**Stanley, D'Ambrosio & Gauci 2009 (HyperNEAT).** *Genome:* a connective CPPN.
*Decoding:* `CPPN(x1, y1, x2, y2) = w` is queried for every pair of substrate nodes, and a
connection is expressed only if |w| > 0.2 (Table 1). The experimenter chooses the substrate
geometry, and the paper says so ("HyperNEAT allows the experimenter to inject knowledge … by
grouping correlated objects or arranging sensors"). *Shown:* on an 11 × 11 visual-discrimination
substrate, the same evolved CPPN was re-queried at 33 × 33 and 55 × 55 with no further
evolution, and it "generalizes significantly better than P-NEAT (p < 0.01) and scales almost
perfectly". *Transfers:* the query shape "(source, target) → existence and weight" is the shape our
decoder has, and the threshold turns a continuous output into existence. *Does not transfer:*
(i) **identity**, for Ark's reason: there is no discrete module to inherit or graft, and nothing
for a birth id to attach to. (ii) **Coordinates**: our 65 types have none. C6 forbids reading their
names, `pattern` takes two values, and `layout` takes three. A CPPN over types would first need an
invented embedding, and that embedding would be the real genome. (iii) HyperNEAT's
strength, resolution-free geometry, is the one layer that is **already** a single production here.
Tiling the column motif over a hex disc makes the bank identical at extent 5 and 15
(`docs/notes/2026-09-20-what-is-the-genome-here.md` §5).

**Shuvaev et al. 2024 (genomic bottleneck).** *Genome:* the weights of a small trained g-network,
with a hidden layer of 30 units in the 322-fold MNIST case. *Decoding:* each neuron has a
fixed binary label, which the paper reads as "the presence of one type of a 'molecular tag'". The
g-network maps the pre-label and post-label to a weight. *Shown:* 322-fold compression with innate
MNIST performance "almost equal to that of the fully trained network". The optimisation is by
gradient, in a loop the authors call Lamarckian and "biologically unrealistic". *Transfers:* the
decomposition itself, **labels on neurons plus a rule over label pairs**. That is the skeleton of
the proposal below. Also the accounting stance: "the number of parameters specifying the
g-networks as a surrogate for the entropy H(G)", which is what C6 §4.2 does. *Does not transfer:*
their labels are fixed and arbitrary, and their rule is an opaque MLP. Neither has parts with
identity. A hidden unit of a g-network is not a module. And keying on cell type turns the phenotype
into a type-to-type block model (literature.md §A.1). Here that is not a loss: the bank **is**
a type-level table.

**What the five have in common, and the gap.** Every generative encoding above gains its power
from **reuse**: one gene is read many times. Only the rewrite systems (Sims's nodes, Hornby's rule
heads) have discrete parts that a crossover could exchange, and neither gives those parts a
lineage-stable identity. NEAT does (entry 18), but NEAT is a direct encoding. The proposal below
is a reuse-based encoding whose reused parts are discrete **and** carry v1 birth ids.

---

## 2. The proposed rule, fully specified

### 2.1 Representation: the genome G

| part | what it is | identity (v1 rule, `results/genome/bank/REGISTRY.md`) |
|---|---|---|
| **Types** (65, existing) | the bank's cell types, with `pattern`/stride and `layout` unchanged | existing `cs-birth-v1\|type\|<name>` ids; unchanged |
| **Label lexicon** Λ, `k = 12` labels | a label has no content except which types express it | new kind `label`; canonical string below |
| **Expression** `e_t ∈ {0,1}^12` per type | which labels type *t* carries; a type uses one expression vector as source *and* as target | a **value** of the type (changing a bit is a mutation, not a birth) |
| **Sign** `σ_t ∈ {+1, −1}` per type | the type's transmitter sign | a value of the type |
| **Count gains** `a_t`, `b_t` per type | how much type *t* scales the synapse counts it sends (`a`) and receives (`b`); 16 levels each | values of the type |
| **Rules** `r = (i_r, j_r, m_r, g_r, ρ_r, w_r)`, at most `R_max = 40` | "a type carrying label *i* connects to a type carrying label *j*", with motif *m*, orientation *g* ∈ D6 (12 lattice symmetries), reliability ρ (16 levels) and log-strength *w* (32 levels); at most one rule per ordered label pair | new kind `rule` |
| **Motif library** M, at most `M_max = 16` motifs, at most `O_max = 64` offsets in total | a motif is a D6-canonical set of integer `(du, dv)` offsets, each with a relative weight level (16 levels) | new kind `motif` |
| **Globals** | leak ε (16 levels); fallback log-strength `w_0` (32 levels) | part of the genome header; no id |

**Every number in G is a small integer on a fixed grid, and there are no 32-bit reals.** Under
C6 A5 a real costs 32 bits, and "the charged precision is the precision actually used". The
grids below are part of the charged decoder, and the rule is scored on what it outputs, rounding
included. So quantisation is the rule's own coarse precision, paid for in accuracy. It is not a
discount taken on the accounting. The grids are fixed now:

| quantity | stored as | value |
|---|---|---|
| ρ | symbol q ∈ 0…15 | (q + 0.5) / 16 |
| ε | symbol q ∈ 0…15 | 2^−(1 + q/2), from 0.5 down to about 0.003 |
| w, w_0 (natural log of a pair's total `n_syn`) | symbol q ∈ 0…31 | 0.17 · q, from 0 to 5.27 (the largest pair total is 144, ln 144 = 4.97) |
| a_t, b_t | symbol q ∈ 0…15 | 0.25 · (q − 8), from −2 to 1.75 |
| motif weight | symbol q ∈ 0…15 | π(o) ∝ exp(0.35 · q), normalised over the motif |
| motif offsets | integers | Elias-gamma coded, as A5 prescribes |

**Canonical strings for the new kinds** (the id is the first 12 hex digits of the string's sha256,
as for types and pairs):

- `motif`: `cs-birth-v1|motif|<shape>`, where `<shape>` is the lexicographically smallest of the
  12 images of the sorted offset list under `regularity.py`'s `rot(u, v) = (u + v, −u)` and
  `refl(u, v) = (v, u)`, written as `du,dv;du,dv;…`. This is `canon_pattern(pts, with_w=False,
  sym=True)`. **Shape only.** The weights π are content, so they can mutate without changing
  the id. A motif's name is its shape, just as a type's name is its name. This is the one kind
  whose name really is a content description, and it is fixed at birth like every other.
- `label` (generation 0): `cs-birth-v1|label|g0{<sorted type ids>}`: the ids of the types
  expressing it in the generation-zero genome. A later-born label uses the registry's operator
  form, `cs-birth-v1|label|dup(<parent id>)@<lineage event id>`. The gen-0 fit must assert that no
  two labels share an expression set (a duplicate would be redundant; the search removes it).
- `rule`: `cs-birth-v1|rule|<pre-label id>-><post-label id>`. This is unique because there is at
  most one rule per ordered label pair.
- **Pairs** keep their v1 ids, which are defined on all 4,225 cells (REGISTRY v1 rule 2). Under
  this genome a pair is **derived**. It exists because rules fire, and when a mutation makes a new
  pair fire, the pair "is born with the id its names give it", as the registry already provides.
- **Offsets** stay addressed as `(pair id, du, dv)`. This is the case REGISTRY.md's "When to
  revisit" anticipated: the motif is now the heritable element, and the offsets are its placements.

**Fold fits carry no ids.** The 10 + 200 + 250 + 65 fits C6 runs are exam instances, and they are
thrown away. Ids are given once, to the **generation-zero genome**. That genome is fitted by the
same procedure on all 4,225 cells, and only after C6 has run, so that building it cannot touch the
exam.

### 2.2 The decoder (fixed; charged as the rule's program under C6 A5)

For an ordered pair of types `(s, t)`:

1. **Firing rules.** `F(s,t) = { r : e_s[i_r] = 1 and e_t[j_r] = 1 }`.
2. **Existence** (noisy-OR): `p(s,t) = 1 − (1 − ε) · Π_{r ∈ F} (1 − ρ_r)`. Clip to [0.001, 0.999]
   as C6 §4.1 requires. The pair is expressed if `p > 0.5`.
3. **Winning rule.** `r* = argmax_{r ∈ F} ρ_r`, ties broken by `(i_r, j_r)` in index order. If `F`
   is empty, there is no winning rule and the fallback motif is used: the library motif whose shape
   is `{(0,0)}` if present, otherwise the motif with most assigned rules. The fallback strength is
   `w_0`.
4. **Offset set.** The support of motif `m_{r*}` mapped by `g_{r*}`. Image index `2q` is `rot^q`,
   and `2q+1` is `refl ∘ rot^q`, in the same order as `regularity.py`'s `d6_images`.
5. **Counts.** For each offset `o` in the set:
   `n̂(o) = exp( w_{r*} + a_s + b_t ) · π_{m_{r*}}(g_{r*}⁻¹ o)`.
   The exponent is the pair's total count, and π spreads it over the kernel.
6. **Sign.** `σ_s`. The sign belongs to the source type, never to the pair.

The decoder reads nothing but G and the harness's type indices 0–64 (C6 A1). It reads no name,
no birth id and no per-type field. It imports only numpy and the standard library (A5). **Its
source must compress to at most 560 bytes** (4,480 bits) under A5's lzma rule. That can be
measured on the file alone, before any fit, because it depends on no data. If the decoder
cannot be written that short, this proposal is withdrawn before anything is run. It is not
squeezed after a score is seen.

A genome copies byte for byte as a file of named integer arrays, and it decodes separately
through this decoder and then flyvis's compiler. That is the two-readings test (REGISTRY.md)
applied to G. The birth ids live in a side table, (element id → array row), which the decoder
never reads. It is not charged in C6, and the exam cannot see it.

### 2.3 How a held-out cell is predicted from training cells only

Everything in G is fitted on the nine training folds, and the held-out fold is then decoded. A
held-out cell `(s, t)` is predictable because **both of its types appear in about 90 % of their
other cells in training**. Their labels are fitted from those cells, and the labels carry the
information to the unseen pair: *s* sends to types that carry label *j*, *t* carries *j*,
therefore *s* → *t*. Concretely:

- **Existence**: step 2, from `e_s`, `e_t` and the rules.
- **Offset shape**: step 4. The winning rule's motif was chosen from the training cells that rule
  wins.
- **Counts**: step 5.
- **Sign**: `σ_s` follows N1's rule in C6 A4 exactly. It is the majority sign of *s*'s training
  non-empty cells. If there is a tie, or *s* has no training pair (Mi11 and Tm30 are never
  sources), it is the training majority sign, and a tie there gives +1. **On sign the rule is
  identical to N1 by construction.** It is not meant to win there. The 10 exceptions all rest
  on `NernPC2018` (`REGULARITY-READING.md` §1) and are the least trustworthy column, and a rule
  bent to fit them would be fitting one personal communication.

### 2.4 The fitting procedure (declared now; training cells only)

**Stage 1: labels, rules, reliabilities, leak (existence only).** Minimise the two-part code
length in bits,
`J = Σ_{training cells} −log2 P(observed existence) + 25 · |R|`
(25 bits is one rule's data cost, §2.5; the expression bits are a fixed 780 and do not enter the search).

- 10 restarts, seeds 0–9. Initialise `e_t[l] ~ Bernoulli(0.25)` from
  `numpy.random.default_rng(seed)`, drawing types in the harness's index order (which is birth-id
  order, C6 A1). Start with no rules, and ε at the level nearest the training base rate.
- Sweep until one full sweep changes nothing, or 50 sweeps:
  (a) for each ordered label pair `(i, j)` in index order, toggle its rule, choosing ρ as the best
  of its 16 levels, and keep the toggle if J falls and `|R| ≤ 40`. Then re-choose the ρ level of
  every present rule;
  (b) for each type in index order and each label, flip `e_t[l]` if J falls;
  (c) re-choose ε as the best of its 16 levels.
- Keep the restart with the lowest training J. The restart spread is recorded (§4.4).
- **Restarts are fixed at 10 unless timing forces fewer, and that is decided before the real
  folds.** The timing is measured on shuffled bank 0 only. If 1,315 fits (C6 A13) would take more
  than 48 hours across the machine's CPU cores, restarts drop to 3 for **every** fit, primary
  included. The decision is recorded before the primary split is run.

**Stage 2: motifs.** For each rule, collect the training non-empty cells it **wins**. Canonicalise
each cell's offset shape under D6. The library is the ≤ 16 most frequent canonical shapes among
won cells, counted by cells, with ties broken by the shape string. Stop adding motifs when the
offset total would exceed 64. Each motif's π is the mean over its cells of the D6-aligned,
sum-normalised `n_syn` profile, rounded on the log scale to the nearest weight level. A rule's motif is its won cells' most frequent shape. If that
shape is not in the library, the rule takes the library motif with the highest mean Jaccard
under the best orientation. `g_r` is the most frequent orientation, ties to the lowest index.

**Stage 3: strengths.** `w_r`, `a` and `b` come from ridge least squares (λ = 1e-3) on the log
of each won training cell's total json-matched `n_syn`. `w_0` is the mean of the same quantity
over all training non-empty cells. Each value is rounded to its nearest level, and then one pass
of coordinate descent over the levels (rules in index order, then `a`, then `b`) minimises the
training squared error of the log totals. A type with no training cell on a side gets level 8
(zero) on that side. Hull-filled rows are excluded throughout (C6 §2).

**Stage 4: signs.** As in §2.3.

Every step is deterministic given the training cells. The procedure reads no type name, no
`alpha_fixed`, no `alpha_references` and no `groundtruth_utils` field (C6 §2).

### 2.5 Description length under C6 A5

C6 A5 charges a predictor as (program, data). The decode module's source counts at 8 × its lzma
bytes. A real costs 32 bits, an integer costs its Elias-gamma length, a symbol from an alphabet of
size m costs ⌈log2 m⌉, a boolean 1 bit, and array names (8 bits per character) and shapes are
charged too. The learner is not charged.

**The bank (S_all, A5).** Each of the 604 stored cells costs 13 (address) + 1 (sign) + gamma(number
of offsets). Each of the 2,117 json-matched rows costs gamma(du) + gamma(dv) + 32. I computed this
from `offsets.csv` as a structural count, not a fit: **89,896 bits**, plus S_all's own short
program and array headers. **P2 ceiling ≈ 9,000 bits** (one tenth). The harness records the
exact figure (A6), and that figure governs.

| genome part (at the caps) | bits |
|---|---|
| expression, 65 × 12 booleans | 780 |
| sign, 65 booleans | 65 |
| count gains a, b: 130 symbols × 4 | 520 |
| rules: 40 × (4 + 4 label indices + 4 motif index + 4 orientation + 4 ρ + 5 w) | 1,000 |
| motifs: 16 lengths (gamma, ≈ 9 each) + 64 offsets × (gamma du + gamma dv, ≤ 14) + 64 weights × 4 | ≈ 1,300 at most |
| globals ε, `w_0` | 9 |
| array names and shapes, about 14 arrays | ≈ 400 |
| **data, maximum** | **≈ 4,070** |
| decoder source, cap (§2.2) | 4,480 |
| **genome total, maximum** | **≈ 8,550, against a ceiling of ≈ 9,000** |

**The margin is about 5 %, and it is the most fragile number in this proposal.** The fitted
genome will usually be smaller, because stage 1 pays 25 bits per rule and keeps a rule only if it
earns them. If the harness's exact DL(rule) still exceeds DL(bank)/10, C6 returns "not a
bottleneck", and that is reported as the result. The caps are not lowered after the fact.

**Parameters.**
- **Fitted:** no 32-bit reals. About 1,400 discrete symbols: 780 expression bits, 65 signs, 130
  count gains, at most 240 rule symbols, the motif offsets, lengths and weights, and 2 globals.
- **Fixed before any data:** `k = 12`, `R_max = 40`, `M_max = 16`, `O_max = 64`, every
  quantisation grid of §2.1, the noisy-OR decoder, the winning-rule precedence, the fallback, the
  D6 action, the restart seeds, the sweep order, the ridge λ, and the 560-byte decoder cap.
- **For comparison:** under A5, N1's data alone is about 336 reals (131 for existence, one per
  distinct offset, 130 for count effects), which is roughly 10,700 bits before its offset sets,
  signs and program. **D_0 = N1 is therefore longer than this rule**, so C6 A6 will very probably
  give k\* = 0, and P2's size-matched comparison becomes "beat N1 in-sample". The null this rule
  must beat stores more than the rule does.

### 2.6 The value of k, and why it sits below 18

`k = 12` is **fixed, not tuned**. It is also the rule's declared latent dimension for C6 A11:
**r = 12**. So P4 compares the rule with N1 plus a fixed random 65 × 12 projection and 780 fitted
reals. Three reasons for 12:

1. **The budget.** Each label costs 65 expression bits before any rule uses it. At k = 18 the
   labels alone add 390 bits, and each rule's label indices grow from 4 to 5 bits. That puts the
   genome at or over the ≈ 9,000-bit ceiling, with no room for the fit to choose its rules.
2. **What the 18 means.** `REGULARITY-READING.md` §2: the real-valued log-count matrix needs 18
   of 65 components for 90 % of its energy, against 30–32 when shuffled. Those are **real**
   components. C6 A6 prices rank 18 at M18 = 18 × 130 × 32 = 74,880 bits, about 83 % of the bank,
   which is no bottleneck at all. Under the ceiling a real factorisation can afford about two
   components, before its own program. A binary label costs 65 bits, not 4,160, and an OR of label
   rules can express block structure that a real factorisation needs several components for. So
   "fewer than 18" is not a handicap. It is the claim: **if the fly's table is regular in the way
   the spectrum suggests, a dozen yes/no marks per type, combined by rules, should carry what
   matters of what 18 real components carry.** If k had to reach 18 to work, the rule would spend
   as many dimensions as the spectrum and gain nothing in economy, and it would be no evidence of
   a grammar.
3. **Headroom.** 12 bits per type give 4,096 distinct codes for 65 types. The 59 distinct
   out-rows and 62 distinct in-columns (`REGULARITY-READING.md` §4) need at least 6 bits.
   Twelve leaves room for labels that group types without separating every one.

**Sensitivity, descriptive only:** k ∈ {8, 16} are run through the primary split alone and
reported beside k = 12, on P1's four fields and their description length. k = 16 may exceed the
P2 ceiling, and that is reported too. **The pass decision uses k = 12 only.** If k = 8 or k = 16
does better, that is reported and does not change the verdict.

---

## 3. Why this rule and not the obvious alternatives

**A pure low-rank factorisation** (each type gets a few real numbers, and the connection strength
is their product). This is what the "18 components" number describes. Under C6's own accounting
it is too expensive: every real number costs 32 bits, so the ceiling allows only about two
components, which is far too few. It also has no parts. A component is a direction in a space,
and no child can inherit "component 3" from one parent and "component 5" from another and get
something meaningful, because the components of two separately fitted genomes are not the same
directions. It also says nothing about offsets or signs. It is kept as a **baseline**, not as the
genome.

**A CPPN over type coordinates** (HyperNEAT-style). Our cell types have no coordinates.
HyperNEAT works because its neurons sit in a real geometric layout that the experimenter supplies,
and our only honest per-type inputs are two strides and three layout values. Giving types
coordinates means inventing an embedding, and then the embedding is the real genome and the CPPN
is decoration. Its strongest property, drawing the same wiring at any resolution, targets the one
part of our table that is already solved: tiling columns over the hex disc. And its modules have
no identity, so point 3 of `idea.md` (gluing two ancestors' modules) has nothing to glue. The
CPPN idea does have a proper place later: **inside a motif**, where the offset kernel really is a
function of `(du, dv)`.

**A direct table** (store every entry). This is today's genome, and it is D_k in C6. It can never
predict an unseen pair, it is not smaller than itself, and a mutation to it changes one entry at a
time. Hornby & Pollack 2002 measured what that does to search, with the direct form set up as the
same grammar restricted to one rule. Clune et al. 2011 show that below some level of regularity
the direct table wins. That is exactly why C6 includes D_k, and why "the direct table wins" is a
possible and honest outcome here.

**Why labels + rules + motifs.** Each piece does one job the bank's numbers point to. The labels
use the connection pattern's block structure (§2 of the reading). The motifs use the fact that
604 offset patterns fall into 144 shapes once symmetry is allowed (§3). The single sign per type
uses the fact that the source type predicts 594 of 604 signs (§1). And every piece has a name, so
it can be inherited, grafted and drawn in the tree.

---

## 4. Pre-stated predictions (written before any evaluation)

### 4.1 What counts as working

**The rule works** if, with k = 12 and r = 12, **both** of the following hold:
- **C6 passes as amended**, all four parts:
  - **P1:** it beats N1 on existence and on offset set in ≥ 9 of 10 folds each. On counts and
    sign it is worse than N1 in at most 2 of 10 folds, and its mean over folds is not worse (A8).
  - **P2:** DL(rule) ≤ DL(bank)/10, and it beats D_k\* in-sample on existence and offset set
    (A6). k\* is very probably 0, so D_k\* is N1.
  - **P3:** the margin is strictly above all 99 shuffled banks on existence and offset set (A9).
  - **P4:** its existence margin over N1 beats the best of 20 RP_12 margins (A11).
- **This proposal's own falsifier (§4.3) is beaten**: the learned labels beat random labels on
  existence **and** offset set in ≥ 9 of 10 folds.

What a pass licenses, and nothing more: *the fly's type-pair table is regenerated, on type pairs
the rule never saw, from under a tenth of the table's length in named labels, rules and motifs,
beyond what type marginals give, beyond what a random projection of the same rank gives, and with
labels that carry structure random labels do not.*

### 4.2 My own expectations, field by field (so that a surprise is visible)

| test | my expectation | why |
|---|---|---|
| P1 existence vs N1 | **pass**, moderate confidence | the binary pattern alone needs 22 components against 31–32 shuffled, and R1–R6 share out-rows. Block structure is what labels capture and what an additive source + target model cannot. **Risk:** the noisy-OR has no per-type degree term, and out-degrees run from 0 to 29 |
| P1 offset set vs N1 | **the likeliest P1 failure** | N1 uses the source's modal shape, and 212 of 604 pairs are `(0,0)` only. A per-rule motif is coarser than a per-source one for sources with unusual kernels |
| P1 counts vs N1 | **at risk** under A8's "at most 2 of 10" | the per-type gains mirror N1's α and β, but on a 16-level grid. Every offset the motif misses is scored as a predicted 0 |
| P1 sign vs N1 | tie in every fold, so it passes | identical by construction (§2.3) |
| P2 | length passes by a small margin (§2.5); in-sample against N1, same expectations as P1 | k\* ≈ 0 because N1's own data is longer than the rule |
| P3 | pass on existence; offset set uncertain | degree-preserving rewiring keeps what N1 uses and destroys the blocks labels use. Permuting contents destroys N1's per-source modal shape as well |
| **P4** | **the hardest hurdle; I expect about even odds** | RP_12 is N1 plus 780 fitted reals on a random projection, penalised. It keeps N1's degree terms, which the rule lacks. Beating it means the labels find more than any 12-dimensional capacity would |
| random labels (§4.3) | learned labels clearly better on existence | random codes cannot line up with blocks |
| dial (C6 §5.3) | the margin over D_k\* falls as f grows | if it does not, §5.3's registered reading applies |

### 4.3 The random-label falsifier (this proposal's addition to C6)

The same rule, decoder and budget, with the **expression bits drawn once at random and frozen**
(Bernoulli(0.25), seed 20260923, types in index order). Only stages 1(a), 1(c), 2, 3 and 4 are
fitted. The random labels are charged the same 780 bits.

This is the Shuvaev-style arm: fixed, arbitrary labels with a learned rule over them. It differs
from C6's P4. P4 asks whether *any* rank-12 capacity added to N1 does as well. This arm asks
whether *this* rule's gain comes from *where* the labels sit. If random labels match learned ones,
the 12 marks per type are acting as capacity, not as discovered structure. The arm is run on the
primary split only (10 fits).

### 4.4 Failing, and uninformative

- **Fail, named by C6's labels** (§5.2 and A11): "copy or marginal", "not a bottleneck", "below
  threshold for this family", "family fits anything", "ambient, not substantive structure". Added
  here: **"labels are capacity"** if the random-label arm is not beaten.
- **Partial, and worth recording as such:** it wins on existence but fails on offset set. Then the
  rule is a grammar of **which types wire to which**, and it is not a grammar of the spatial kernel.
  The next rule would keep the labels and replace the motif step. **This is my single most likely
  outcome.**
- **Uninformative:**
  (i) "rule did not run" (N0 is not beaten), which is a harness or search failure, not a verdict;
  (ii) the **restarts disagree**: if, in a majority of folds, the best and second-best restarts
  differ by less than 1 % in J and share fewer than half their rules (rules matched by the member
  sets of their two labels), the fitted genome is not identifiable, and a pass would say nothing
  about *which* labels the fly has;
  (iii) N1 and N0 are indistinguishable on a field in a majority of folds, so that field cannot
  separate anything and is reported as uninformative for this rule;
  (iv) the random-label arm **also** passes P1–P4. Then, at this budget, C6 cannot tell discovered
  structure from flexible capacity, and the exam, not the rule, needs a stronger arm.

### 4.5 What it would mean for the elephant

The representation is **generative by construction**. A new type is a new expression vector, and
the decoder gives it a complete row and column of the table: which types it talks to, with which
motifs and strengths, and its sign. No one writes those in. A single label flip changes a
coherent family of pairs at once, what Hornby & Pollack 2002 (p. 3) describe as "the ability to make
coordinated changes in several parts of a design simultaneously". So the rule **can** say things the fly never said.

**But C6 does not test that, and cannot.** C6 tests reproduction of held-out pairs between
**existing** types. Its leave-one-type-out split is descriptive, and under this rule it is close to
empty by design: a type with no training cells gets no fitted labels, so the rule predicts it as
unlabelled. Whether the new types and pairs it *can* produce are *good* is a question about
phenotypes (do they compile in flyvis, do they see), and that waits on the measurement line.

**The risk, stated plainly.** Everything C6 checks is compatible with this rule being **a good
compressor of one table and nothing more**. Its labels are fitted after the fact to one fly. They
are not developmental. "Developmental label" is a name I gave them, not a mechanism anyone
observed. A compressor also generates. The question is whether what it generates is what
evolution would have made, and one table cannot answer that. There is also a direct cost: the
rule's structure (labels for blocks, motifs for shapes, sign per type) was chosen **after I read
the whole-bank regularity numbers**, including cells that will later be held out. No parameter
was fitted on them, but the *family* was not chosen blind. Held-out success therefore shows that
the fitted *values* generalise. It does not show that the *family* was discovered without looking.
The second fly (a second connectome, or FlyWire's own types) is where this rule either keeps its
labels or turns out to have described one table.

---

## 5. Connection to points 2–5 and the tree

With v1 ids on labels, rules and motifs, the operators of `idea.md` point 3 become concrete:

| operator | in this genome | ids |
|---|---|---|
| **soft mutation** (point 3) | change a rule's `w` or ρ, a motif's π, or a label gain: a **value** change | no new element; the ids stay (REGISTRY rule 5) |
| **expression mutation** | flip `e_t[l]`: type *t* gains or loses a whole family of partners at once | no new element. Any pair that starts to fire is born with its pre-fixed v1 pair id |
| **structural mutation** | add a rule `(i, j)` | new `rule` element, id from `rule\|<i id>-><j id>`, `parent_ids` = [i, j] |
| **label duplication** | copy label *l* to *l′* (same expression, same rules re-pointed), then let the two diverge | new `label` id `dup(<l id>)@<event>`; the copied rules get new rule ids with `parent_ids` = the originals |
| **permutation** (point 3: "change the role/type of modules") | swap a rule's motif or orientation; move a label between types | value changes; no birth |
| **new cell type** | duplicate type *t* to *t′*: copy `e_t`, `σ_t`, pattern; later flips differentiate it. The decoder wires *t′* at once | new `type` id `cs-birth-v1\|type\|dup(<t id>)@<event>`, `parent_ids` = [t] |
| **heredity / crossover** (point 3: "glue together the working modules of two ancestors") | a **module** = a label with the rules that mention it and the motifs they use (its "regulon"). The child copies parent A. For each label of parent B absent from A (matched by id), **graft** it: copy the label, its rules and motifs, and its expression bits on every type the child shares with B (matched by type id). Where both parents have the same id, take either parent's version | homology is by id, never by position: NEAT's fix applied to Sims's grafting. Every grafted element keeps B's id, so the tree can say "this label came from the fly through parent B" |

- **Point 2 (body and brain together).** Labels are the natural place to couple them. A label's
  expression can later be conditioned on the body segment a type sits in, which is Sims's nested
  graph (neurons inside body nodes) with named parts. Nothing here builds that yet.
- **Point 4 (youth).** Unchanged. G decodes to a bank, flyvis compiles it, and training runs as
  before. G is the inherited object, and the trained weights are not written back into it. That
  is the opposite of Shuvaev et al.'s Lamarckian loop, and deliberately so (S2 design §1).
- **Point 5 (fitness).** Unchanged. The rule gives no fitness; it gives the thing fitness is
  measured on.
- **The tree.** Every node of the tree is a genome, and every element in it has `(id,
  generation_born, parent_ids)`. "Which module was inherited from the fly" becomes a query: which
  labels and rules in a descendant have a gen-0 id, and through which ancestors they passed.
- **The HybrID refinement** (literature.md "What this changes for us" item 4). The gen-0 genome
  will not reproduce the fly exactly, so a **residual table** holds the exceptions: pairs the rule
  gets wrong, and the 10 sign exceptions, each keyed by v1 pair id. With it, decoding gen 0
  reproduces the bank exactly, and the two-readings test passes. Whether the residual is inherited
  is §6 Q2. C6 judges the rule **without** the residual, since a residual cannot predict an unseen
  pair.

---

## 6. What is NOT claimed, and open questions

**Not claimed.**
- Nothing has been fitted or scored. Every expectation in §4.2 is a guess written down so it can be
  proved wrong.
- The labels are not claimed to correspond to any molecule, gene or developmental stage.
- Not "we predict biology". A pass is about this bank only (C6 §7).
- The rule does not address the type list. It takes 65 types as given, and how many types an
  organism has is the part a growth grammar most needs (REGULARITY-READING, last bullet).
- No claim that the operators of §5 produce viable or better offspring. That needs compiled
  phenotypes and the paused measurement line.
- The random-label arm and the k-sensitivity runs are this proposal's additions. They are not part
  of C6 unless the amendment makes them so.
- Nothing here licenses growing anything. `ROADMAP.md`'s prohibition stands.

**Open questions for Mike.** Each says what the choice affects, and gives a recommendation.

1. **Register this rule as the first candidate?** *Affects:* whether C6 is run on it at all. Once it
   is registered, its constants (k = 12, the caps, the procedure) cannot be changed after any
   number is seen. *Recommendation:* yes, after Ark (the design's owner) and Zcode (C6's owner)
   have read it, because it is their two documents it binds to.
2. **Is the residual (exceptions table) heritable?** *Affects:* the tree and the fly-likeness of
   generation 0. If it is inherited, gen 0 **is** the fly, and descendants carry the fly's
   exceptions as a direct-encoded appendix. If it is not, gen 0 is "the fly as the rule sees it",
   slightly different from the real one, and the tree records only the rule. *Recommendation:*
   heritable, but stored as a separate, visibly marked part, so the tree can always say how much
   of an organism is rule and how much is copied exceptions.
3. **New element kinds in the registry** (`label`, `rule`, `motif`, with the canonical strings of
   §2.1). *Affects:* REGISTRY.md and `extract_bank.py`, and whether crossover can match modules
   between two genomes. *Recommendation:* yes. The alternative is a genome with unnamed parts,
   which is the CPPN problem this proposal exists to avoid.
4. **Is the ~5 % length margin acceptable, or should the rule be made smaller now?** Under C6
   A5 the decoder's own source is charged, and that leaves the rule about 450 bits under the
   ceiling (§2.5). *Affects:* the risk of a "not a bottleneck" fail that says nothing about
   structure. Shrinking now means, for example, R_max = 32 or k = 10. That costs expressive power,
   but it is decided before any data, so it is still honest. Shrinking after a score would not be.
   *Recommendation:* keep the caps, and let the 560-byte decoder check (§2.2) decide. If the
   decoder cannot be written that short, come back with R_max = 32 rather than a larger allowance.
5. **Fixed k = 12, or k chosen by an inner cross-validation on the training folds?** *Affects:*
   honesty against flexibility. A fixed k cannot be tuned. An inner search might find a better k,
   but it adds a knob and nine times the fits. *Recommendation:* fixed, with k = 8 and k = 16
   reported alongside (§2.6).
6. **Who implements and runs it?** ADR-003: the reading is written here, before the numbers, and
   the runner reports C6's labels only. *Affects:* whether "the proposer saw the whole bank" (§4.5)
   also becomes "the proposer tuned the code while watching the scores". *Recommendation:* the C6
   harness is built and hashed first (the step in `docs/plans/2026-09-23-grammar-track-next-steps.md`).
   The rule's code is then written and hashed against a **shuffled** bank only, and it meets the
   real folds once.

## Sources

- `idea.md` (the goal: five points and the tree); `docs/decisions/004-grammar-is-the-main-line.md`.
- `docs/notes/2026-09-20-what-is-the-genome-here.md` §1, §2, §5.
- `docs/plans/2026-09-20-genome-design-around-s2.md` §1, §2 and its 2026-09-23 amendment (Ark's
  structural point, §5 of the amendment).
- `docs/plans/2026-09-23-c6-control-specification.md` (blob `137da3b8…`), §2–§5, and its
  uncommitted amendment A1–A14 as read (sha256 `32f2e403…`).
- `results/genome/bank/REGULARITY-READING.md` §1–§4; `REGISTRY.md` (revision v1);
  `regularity.py` `rot`, `refl`, `d6_images`, `canon_pattern`; `types.csv`, `type_pairs.csv`,
  `offsets.csv` (read for structural counts only; nothing fitted).
- `literature.md` §I.1 entries 9–13, §I.3 entry 18, "What this changes for us" items 1–4; §A.1.
- Local copies and page ranges: §0 above; `sources/local/2026-09-23-first-rule/`.

---

## Amendment pointer — 2026-09-23 (appended; the text above is unchanged)

The search procedure of §2.4 (stage 1) is to be fixed before any real run: Mike, owner,
2026-09-23 22:38 UTC, option B. The criterion a fix must meet was registered first, in
`docs/plans/2026-09-23-first-rule-search-criterion.md`. The model, decoder, caps, rule cost and
accounting stay frozen. The fixed procedure (SEARCH v2) will be declared in a dated appendix below
before its gates are run. The procedure as written above stays callable as SEARCH v1.

## Appendix — 2026-09-23: SEARCH v2, declared before its gates are run (appended)

**What is added.** Stage 1 of §2.4 gets one extra move, the **escape**, used only where §2.4
would stop. Everything else is the procedure above, step for step (SEARCH v1). Nothing else
changes: the model, the decoder (555 bytes), J, the grids, the caps, the 25-bit rule cost, stages
2–4 and the accounting. The code is `results/genome/c6/rules/first_rule/fit.py`, functions
`escape` and `_seed_candidates`.

**The escape.** When a full sweep changes nothing, and the restart has fewer than 40 rules and
at least one fresh label (a label that no rule uses), try a compound move.

1. **Candidates, in this fixed order.**
   - (1) If at least two labels are fresh, call the two lowest fresh labels i and j. Then, for
     each training non-empty cell (s, t) in index order: label i = the types with a training
     non-empty cell into t, and label j = the types with a training non-empty cell from s. The
     candidate rule is i → j.
   - (2) For each used label u in index order, with f the lowest fresh label: label f = the types
     t whose training cells from u's types are non-empty in more than half of them. The candidate
     rule is u → f.
   - (3) The same with u as the target: label f = the types s whose training cells into u's types
     are non-empty in more than half of them. The candidate rule is f → u.
2. **Seeding does not change J.** Re-seeding a fresh label changes no cell, since no rule reads
   it.
3. **Ranking.** Each candidate gets its rule at the best of the 16 ρ levels. Candidates are
   ranked by the resulting J change (+25 bits), with ties going to the candidate order.
4. **Refinement.** The first 12 candidates are refined in rank order. Refinement repeats rounds
   until a round changes nothing, for at most 50 rounds. Each round:
   - greedy flips of the candidate's fresh label(s), types in index order and labels in index
     order, each kept if J falls by more than 1e-9 bits;
   - then the new rule's ρ is re-chosen as in §2.4.
5. **Acceptance.** The first refined candidate whose J, recomputed from the genome, is lower than
   the restart's J before the escape (by more than 1e-9 bits) is kept, and the sweeps go on. If
   none is, the restart stops, as in v1.

**Properties.**

- The escape is deterministic: it has no random draw.
- Every kept move lowers J, so the search still terminates.
- The 50-sweep cap still applies.
- Restarts still use seeds 0 … k − 1 for the Bernoulli(0.25) initial labels.

**How it was designed.** Only the criterion's **development** tables were looked at (planted PG1
seeds 3000–3009, shuffled banks 1100–1109), under
`docs/plans/2026-09-23-first-rule-search-criterion.md` §2. Four versions were tried. The table
shows finds on the development tables, and false finds on the development shuffled banks.

| version | finds | false finds |
|---|---|---|
| a best rule on two fresh labels with random bits, then refinement | 3 of 10 | 0 of 10 |
| the same, also allowing one used label | 5 of 10 | 0 of 10 |
| + labels seeded from one source row | 5 of 10 | 0 of 10 |
| **+ labels seeded from one non-empty cell, as above (this v2)** | **10 of 10** | **0 of 10** |

The gate tables (planted 2000–2019, shuffled 1000–1019) had not been run when this was written.
v2 is committed before they are run, and it is not changed after.
