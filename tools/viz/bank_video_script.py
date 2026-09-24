"""Caption and voice-over script for the video "real bank vs shuffled bank".

Pure data, no imports: read by tools/viz/bank_narration.py (text-to-speech, timeline) and by
tools/viz/bank_animation.py (Blender, through the timing file the narration step writes).

Each chunk is one caption shown on screen while its voice clip plays.
  id        stable key; bank_animation.py hangs its visual cues on these ids
  text      the caption, exactly as shown
  say       what the voice reads, if it differs from the caption (spelling of type names and
            numbers only, so the speech engine pronounces them; the meaning is identical)
  lead      seconds of silence before the clip
  hold      seconds of silence after the clip (room for the animation)

Accuracy notes (checked against the code the video depicts):
  * the bank is flyvis's FIB-25/FIB-19 type-level template as results/genome/c6/harness.py reads
    it: 65 types, 604 non-empty (source, target) cells, one sign and one offset kernel per cell;
  * the shuffle is shuffled_bank(REAL, seed=0), harness.py:907, i.e. rewire_and_permute
    (:871-900): double-edge swaps (s1,t1),(s2,t2) -> (s1,t2),(s2,t1), which keep every type's
    out- and in-degree; then every kernel object (offsets, hull, sign) is dealt to a random
    rewired cell. 424 of the 604 real cells are empty after the shuffle; Mi9->T4d's kernel lands
    at Tm9->T1;
  * the test sentence paraphrases P3 of docs/plans/2026-09-23-c6-control-specification.md with
    A9's 99 shuffled banks; no result is stated anywhere.
"""

TITLE = "The fly's visual wiring, real and shuffled"
SUBTITLE = "a type-level template from flyvis, and a shuffled copy used as a control"
END_LINES = [
    "flyvis (Lappalainen et al., Nature 2024), MIT licence;",
    "bank: flyvis connectome/fib25-fib19_v2.2.json, a type-level template from two FIB-SEM volumes;",
    "shuffle: connectome-seed C6 harness",
    "",
    "Made by the DPC Research team:",
    "Mike Shevchenko, with AI agents Ark, Johnny, Warren and Zcode, and Claude Code",
]
CAVEATS = [
    "One shuffle (seed 0) of the 99 the tests use.",
    "Type order is flyvis's layout, already grouped by pathway: part of the pattern is the order.",
    "An illustration of the control, not a result.",
]

CHUNKS = [
    dict(id="intro", lead=0.8, hold=0.3,
         text="A wiring template of the fly's visual system, from the flyvis model."),
    dict(id="intro2", lead=0.1, hold=0.4,
         text="It lists cell types, not single neurons. A shuffled copy is the control."),
    dict(id="types", lead=0.2, hold=0.4,
         text="65 cell types sit on the circle, in three groups."),
    dict(id="lines", lead=0.1, hold=0.8,
         text="Each line is one type sending synapses to another. Red is excitatory, blue "
              "inhibitory."),
    dict(id="focus", lead=0.2, hold=0.3,
         text="Follow one connection: Mi9 to T4d.",
         say="Follow one connection: M i nine, to T four D."),
    dict(id="kernel", lead=0.2, hold=1.0,
         text="Each connection carries a kernel: mean synapses at nearby column offsets on a "
              "hex lattice."),
    dict(id="shuffle", lead=0.3, hold=0.2,
         text="Now the shuffle. Pairs of connections swap their receiving types, again and again."),
    dict(id="degrees", lead=0.1, hold=0.7,
         text="Every type keeps its number of inputs and outputs. 424 of the 604 connections move "
              "to a new pair of types; 180 stay where they were."),
    dict(id="deal", lead=0.2, hold=1.2,
         text="Then the kernels, signs included, are dealt at random: the Mi9 to T4d kernel "
              "lands on Tm9 to T1, and Mi9 to T4d is now empty.",
         say="Then the kernels, signs included, are dealt at random: the M i nine to T four D "
             "kernel lands on T M nine, to T one, and M i nine to T four D is now empty."),
    dict(id="tables", lead=0.8, hold=0.3,
         text="As tables: rows send, columns receive, one square per connection."),
    dict(id="same", lead=0.1, hold=0.5,
         text="Same connections per type, the same 604 kernels. But the wiring differs, and not "
              "one connection keeps its own kernel, not even the 180 that stayed."),
    dict(id="tests", lead=0.2, hold=0.6,
         text="Our tests ask whether a proposed wiring rule beats the N1 baseline by more on the "
              "real bank than on every one of 99 shuffled copies, both for which connections "
              "exist and for their offset kernels.",
         say="Our tests ask whether a proposed wiring rule beats the N one baseline by more on "
             "the real bank than on every one of ninety-nine shuffled copies, both for which "
             "connections exist and for their offset kernels."),
    dict(id="cav1", lead=0.3, hold=0.2,
         text="Caveats: this is one shuffle, seed 0, of 99.",
         say="Caveats: this is one shuffle, seed zero, of ninety-nine."),
    dict(id="cav2", lead=0.1, hold=0.2,
         text="The order of types is flyvis's own layout, which already groups types by pathway, "
              "so part of the pattern you see comes from that ordering. Which line slides where "
              "is a drawing choice."),
    dict(id="cav3", lead=0.1, hold=0.6,
         text="This is an illustration of the control, not a result."),
    dict(id="source", lead=0.2, hold=1.8,
         text="Data: flyvis, 2024. Shuffle: our C6 harness.",
         say="Data: flyvis, 2024. Shuffle: from our C-six harness."),
    dict(id="team", lead=0.2, hold=2.2,
         text="Made by the DPC Research team: Mike Shevchenko, with AI agents Ark, Johnny, "
              "Warren and Zcode, and Claude Code.",
         say="Made by the D P C Research team: Mike Shevchenko, with A I agents Ark, Johnny, "
             "Warren and Z-code, and Claude Code."),
]
