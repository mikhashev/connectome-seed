# The idea — verbatim

*English translation of [idea.md](idea.md), made 2026-09-13 on Mike's word; the Russian original is the record, this file is not.*

Source: Mike Shevchenko, Telegram, 2026-09-12 12:18, quoted into the DPC Research group on
2026-09-13 05:57 UTC as message 67 ([chat/67](chat/67-mike-055707.md)). Nothing below is edited.

> idea: USPEX for the digital evolution of nervous systems. Not "emulate a fly and call it an elephant",
> but grow a lineage of creatures from a real connectome-seed.
>
> 1. the seed is not all the weights, but a heritable grammar.
>    From FlyWire we take modules and motifs: neuron types, excitatory/inhibitory balance,
>    recurring graph motifs, sensory and motor circuits. This is the first genome, not a
>    cemented brain of 140k nodes.
>
> 2. body and brain grow together.
>    The genome describes: which segments/joints/sensors the body has and how neuromodules
>    are duplicated, connected, specialised. Not a "fly → elephant" jump, but a curriculum:
>    fly → beetle → six-legged truck → small quadruped → heavy quadruped.
>
> 3. USPEX operations, only on a living graph.
>    - heredity: we glue together the working brain and body modules of two ancestors;
>    - softmutation: we change connections where the controller is insensitive/plastic, rather than
>      chopping random axons;
>    - permutation: we change the role/type of modules or the sensory channel;
>    - random embryos and diversity archive keep everyone from turning into the same
>      simulator cockroach.
>
> 4. local relaxation = the offspring's life.
>    Each mutant first goes through a short "youth": limited plasticity/learning in
>    several safe worlds. Only after that do we measure fitness. This is the analogue of
>    DFT-relaxation in USPEX: we evaluate not the raw embryo, but what it stably
>    settles into.
>
> 5. fitness is not a single "didn't fall over".
>    multi-objective: energy, stability, speed, recovery after a broken
>    sensor/joint, novelty of strategy, transfer to unseen terrain. A separate held-out set
>    of arenas — otherwise the winner is whoever found a hole in MuJoCo.
>
> The project's main artefact is not a single elephant video, but an evolutionary tree: which mutation
> appeared, which module was inherited from the fly, what grew, where a line broke and which
> skills survived the change of body.
>
> This would not be a biological elephant. This would be the first honest connectome-seeded artificial
> organism.

The author's own named next step, from the same message:

> If you develop this further — the most interesting next step, in my view, is
> formalising the representation of the genome (exactly how the heritable grammar of modules
> and growth rules is written down). Almost everything else depends on it.

Two claims in the text did not survive the thread and are recorded here so the idea is read
with them: "first" is not true (OpenWorm since 2014, C. elegans whole-body simulators,
whole-fly-brain emulation on Loihi 2, and a connectome-as-controller fly in 2026 — see
[literature.md](literature.md)); and the short "youth" of point 4 is exactly the mechanism
arXiv 2508.17464 measured as the source of mis-ranking. Neither kills the idea; both change
where it starts.
