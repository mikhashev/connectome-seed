"""Entry point of extension X's validation driver (draft, unregistered): imports gpu_env FIRST,
then ext_gpu_stage, under the main guard (Windows re-runs this file as __mp_main__ in every prep
worker; the workers must import neither torch nor the engine). See ext_gpu_stage.py.
"""
if __name__ == "__main__":
    import gpu_env  # noqa: F401  (G1: first import)
    import ext_gpu_stage
    ext_gpu_stage.main()
