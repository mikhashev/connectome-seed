"""Entry point of the registered GPU stage (GPU instrument registration, G1, G8): imports gpu_env
FIRST (the thread preamble, CUBLAS_WORKSPACE_CONFIG=:4096:8 before torch, the determinism flags),
then gpu_stage, whose main() is the registered v3-only driver. Everything runs under the main
guard, so the prep workers that Windows spawns (they re-run this file as __mp_main__) import
neither torch nor the engine. See gpu_stage.py for the outputs, run kinds and refusals.
"""
if __name__ == "__main__":
    import gpu_env  # noqa: F401  (G1: first import)
    import gpu_stage
    gpu_stage.main()
