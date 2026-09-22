# Absolute paths in the run records point at a directory that no longer exists

**Written:** 2026-09-23, by CC, on Mike's word (DPC Research group, 2026-09-22 19:41 UTC).
**What this is:** a reading key for the committed run records. It changes no record.

## The paths

Records written before 2026-09-18 carry absolute Windows paths of this shape:

```
C:\Users\mikha\AppData\Local\Temp\claude\c--Users-mikha-Documents-dpc-research-autoresearch-win-rtx\63f3961a-96ce-4048-8338-72c162ea66f8\scratchpad\flyvis-probe\...
```

A search of the tracked `results/**/*.json` for `63f3961a` or `Temp\claude` finds them in
**25 of 113** files (night 1: 3, night 2: 8, night 3: 3, night 4: 3, diagnostics: 8). They
appear in fields such as `meta.netdir`, `env.scratch_netdir`, `connectome_file`, the recorded
`argv` of a launch, and a wave's `jobs[]`. (Ark counted 81 of 113 on 2026-09-22 with a
broader pattern that also matches other absolute user paths; the two counts answer different
questions and both are correct for their pattern.)

## What they meant, and what they mean now

- `Temp\claude\<encoded project>\<session id>\scratchpad\` is the private working directory
  of one Claude Code session. The encoded project is `autoresearch-win-rtx`: the session that
  built and ran nights 1–4 had been opened on that neighbouring repository, so its working
  directory was a temporary folder rather than this repository.
- `flyvis-probe\.venv\` was the only working Python environment until 2026-09-18. It was then
  copied into this repository as `tools/.venv`, verified file by file (21,650 files, one
  combined digest, zero differing), and night 5 ran from it.
- `flyvis-probe\night\` and the other raw outputs were copied to
  `connectome-seed-archive/flyvis-probe-63f3961a/` outside the repository on 2026-09-20 and
  verified pairwise by hash.
- The scratchpad itself was deleted by Mike on 2026-09-20. **The paths in the records now
  resolve to nothing, for anyone.**
- `connectome_file` pointed into that venv's installed `flyvis` package. The connectome is not
  reproduced in this repository; it ships with `flyvis 1.2.0`
  (`flyvis/connectome/fib25-fib19_v2.2.json`), pinned in `tools/night/requirements-frozen.txt`.

## Why the records are not rewritten

Several records are pinned by hash in other documents (axis fingerprints, pre-registered
readings, `script_sha256` fields). Editing a path inside one would break the chain that makes
it a record. The paths are therefore left as written, and this note is the key.

## From now on

New records should name the connectome as **package + version + file**
(`flyvis 1.2.0 : connectome/fib25-fib19_v2.2.json`) and run directories relative to
`FLYVIS_ROOT_DIR`, not as absolute paths on one machine. Tracked as a board entry.
