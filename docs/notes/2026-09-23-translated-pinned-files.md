# Translated registered and pinned files — old and new hashes

**Date:** 2026-09-23 · **Authority:** Mike, owner, in the Claude Code session of 2026-09-23: the
files that still contained Russian are translated into English. · **Written by:** a CC subagent.

## What happened

Until 2026-09-23 eight tracked files kept Russian text. `idea.md` was kept as the Russian
original beside an English `idea_en.md`. Seven other files were registered or pinned by a
recorded sha256, and `docs/CHECKLIST-research-repo.md` § Language left them untranslated so the
hashes would keep reproducing. On 2026-09-23 all of them were translated, `idea.md` took the
English text of `idea_en.md`, and `idea_en.md` was deleted.

**The originals are not lost.** The last revision with the Russian text is commit
**`2488ecb72d14aa5398149d9a727b58852873a091`**. Every hash recorded before 2026-09-23 refers
to that revision and **reproduces there**, not from the current file. The records that cite
these hashes (json, csv, logs, `SHA256SUMS.txt`, `SHA256.txt`, `disposition.sha256.json`) were
**not edited**. They are still valid for the revision they were taken from.

**Line endings.** The repository runs with `core.autocrlf=true`, and git stores files with LF
endings. Some pinned hashes were taken over the Windows CRLF checkout and some over the LF
bytes. The table says which form each recorded hash matches. The two ways to reproduce a hash:

```
git show 2488ecb:<path> | sha256sum                    # LF, as stored in git
git show 2488ecb:<path> | sed 's/$/\r/' | sha256sum    # CRLF, as checked out on Windows
```

"New" hashes are of the translated file as it will be stored (LF) and as checked out (CRLF).
A file can't print its own hash, so the new hashes are recorded only here.

Every "reproduces" in the table was checked on 2026-09-23 by running the command above.

## The table

| file | recorded hash (original, 2488ecb) | form, reproduces? | new sha256 LF / CRLF | what changed |
|---|---|---|---|---|
| `idea.md` | no record pins it; original `72810bac…e38db` (LF) | LF, yes | `415c020ea93cd332392fa861264ae582918cfab349ca04d941268916c4c72f82` / `2d3a6fb888e426fe48e8f8c122ec3973fe4e6d561c189c4c98b9e340b318dab6` | Russian original replaced by the English text of `idea_en.md` (2026-09-13); OpenWorm annotation corrected from 2014 to 2011 (literature.md §I.9) |
| `idea_en.md` | no record pins it; last revision `c743e0e1…44f1` (LF) | LF, yes | deleted | folded into `idea.md` |
| `docs/preregistration-cheap-vs-expensive.md` | no record found citing it; original `1ffd76b02765f30bfcc978da30a467b6ca1cef83fad16a2bc1ace284fc06af65` (LF) / `def407aeac74ede066cace14835f85f1667684f11ab57eecabd3643388729eb2` (CRLF) | both, yes | `e6a779ac235e89d28f47cd350373e815e2db089c153106661aafe9dea87538c1` / `1e0de0a55e933aa767fa3c779b1c947beb4efd9d01a80d7caa56c6eb96a66934` | 32 dated authorisation quotes translated, each marked "(translated from Russian)"; a translation note added to the end of the Date line (line 3), so no line number moves |
| `results/night2/diagnostics/rowB/rowB.py` | `195a89b555bedf3a0ff00a4c4e0542eafa6370243fbf9ed954f5fe8fbf7f4082` | CRLF, yes (LF form is `69b6878f…968d`) | `03ce968b0c65e919f1b107ce730e43e15c61c141f15a8a9c8f6c7d89aee601ba` / `2d19f87c55c81f77ca295ee0122d177b2c2535076eefaf14adaa8d91d040c5a9` | one docstring line translated; comment block appended at the end of the file; no executable line changed; line numbers unchanged |
| `results/night3/diagnostics/rowB/rowB.py` | same as night2 (byte-identical copy) | CRLF, yes | same as night2 (the copies are still byte-identical) | same as night2 |
| `results/diagnostics/gray/gray_stimulus.py` | `61eb8bf3068b0bc4a89568c144ab1a931c68a0c4a54659a24cd5b631fc067624` | LF, yes | `607b4136e2e557f5914fdd4f12a8825e1cd37b858895a510c0d6b0658583893a` / `6b9b9c53c7fcf1179046304eafdb106bd036ea415146f86ae6ed28cb3033dac0` | two docstring lines and the `meta["launch"]` string literal translated; comment block appended at the end; line numbers unchanged |
| `results/diagnostics/c3/README.md` | `4e13269642c8089033a4b61237dfa195da33451e6e6c353e638cdccdd803e811` | LF, yes | `06d6f0f0fba92455c9b2720b632d0106f89cf6e474150e2a69441b5be499e852` / `1747b3552102678977e8884e3921a3e5fb90013bdb0168b2154a3a2718882126` | launch-word line translated; one-line pointer in the formerly blank line 2 |
| `results/diagnostics/labels/README.md` | `db3e00857ccafda39eeed77a4bb210f16e6d539ad2d6953809458f4679a17085` | LF, yes | `241ac65703118e542c905cac60eeca3ca372dc3495cf39f9f189f697bb73172b` / `86b0d67f1cba511fede23fc20a01b5f3ce70628d9d8d704fc23071c6ea4815ab` | owner's-word line translated; one-line pointer in the formerly blank line 2 |
| `results/night5/diagnostics/rowB/PROFILES-READING.md` | §0 seal `a4d10e67f6eafa922f555625569ac5ca11db2de8bb27a01e597acbc0a945583d` | **no — not from any committed revision** (see below) | `d5a75ac9f328e88526247e2c1a745932d358ce8c4819c2e840a690da7382a519` / `b2ca1f0e712e1a5d8915405e29abef7d51ffab844d26b1f15b200dadf10c2df9` | §0(a) registered question: the English is now the registered text, marked "(translated from Russian)"; dated notes under §0(a) and under the §0z digest |

## Which records cite the old hashes (not edited)

- **`195a89b5…` (rowB.py):** `results/night2/diagnostics/rowB/` — `README.md`,
  `rowB_controls.json`, `rowB_distances.json`, `rowB_eval_records.json`, `rowB_preview.json`,
  `rowB_vs_rowA.json`, `rowB_profiles_{250008,25212,iter0}.csv`, `rowC_trajectory.csv`;
  `results/night3/diagnostics/rowB/` — `README.md`, `SHA256.txt`, `rowB3.py` (records it as
  `night2_rowB_script_sha256`; nothing checks it), `rowB_controls.json`, `rowB_distances.json`,
  `rowB_eval_records.json`, `rowB_exploratory.json`, `rowB_preview.json`, `rowB_vs_rowA.json`,
  `rowB_profiles_{250008,25212,iter0}.csv`, `rowC_trajectory.csv`;
  `results/night3/diagnostics/ablation/` — `README.md`, `ablation_controls.json`,
  `ablation_distances.json`, `ablation_reading.json`, `ablation_repeatability.json`;
  `results/diagnostics/gray/` — `README_v2_gate_stop.md`, `gray_controls.json`,
  `gray_readings.json`, `gray_repeat_controls.json`, `gray_v4_main_gate_stop.log`,
  `gray_v51_main.log`; `results/diagnostics/c3/partB/` — `c3B_floor.json`, `c3B_proc{1,2,3}.json`,
  `c3Bprime_proc1.json`.
- **`61eb8bf3…` (gray_stimulus.py):** `results/diagnostics/gray/` — `README.md`,
  `gray_controls.json`, `gray_readings.json`, `gray_repeat_controls.json`, `gray_losses.csv`,
  `gray_losses_repeat.csv`, `gray_v51_main.log`.
- **`4e132696…` (c3 README):** `results/diagnostics/c3/SHA256SUMS.txt`.
- **`db3e0085…` (labels README):** `results/diagnostics/labels/disposition.sha256.json`,
  `labels_per_type.csv`, `partition.json`.

`gray_stimulus.py` writes the translated `launch` literal only into outputs written after this
change. The gray outputs already on disk keep the original string, as JSON `\u` escapes. They
are records and were not touched.

## The §0 seal of PROFILES-READING.md does not reproduce

§0z says the digest `a4d10e67…` was taken at 2026-09-20T09:31:44Z over the file as saved at
09:30:25Z, "up to and including the line above this subsection". The file has one commit before
the translation, `9e101a5` (2026-09-20 17:03 +0700). Its blob is unchanged at `2488ecb`.
On 2026-09-23 the digest was checked against all of the following, and none of them matches:

- every prefix of that revision ending at or just before the `### 0z` heading, in LF and in
  CRLF, with zero, one or two trailing newlines;
- the same prefixes with the `OFF LIMITS` header block removed, and with the English-rendering
  paragraph removed;
- §0 alone, from `## 0.` or from `### (a)` to `### 0z`.

The bytes the digest was taken over were never committed. Per
`docs/CHECKLIST-research-repo.md` as of `2488ecb`, a language pass had translated §0 and CC then
restored it. The restoration may not have been byte-exact, or the header was added later. So
the order "declaration, then values" rests on the file's own statement and the commit time. It
does not rest on a digest anyone can recompute. This was already true before the translation.
