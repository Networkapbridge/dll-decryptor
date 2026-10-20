# Contributing to dll-decryptor

Thanks for wanting to help. This is a hobbyist/educational tool for
reverse engineering obfuscated and encrypted Windows DLLs. Keep it
surgical, keep it documented.

## Ground rules

- **Educational / research use only.** Do not submit code whose sole
  purpose is to defeat a specific commercial anti-cheat or DRM product.
  Generic unpacking, decryption, and dumping primitives are fine.
- Keep the pipeline clean: `ingest -> analyze -> decrypt -> dump`.
  New stages go in the matching folder under `pipeline/`.
- Every new decryptor backend needs a corresponding stub test in `tests/`.
- No binary blobs. If you need a sample, generate it in the test.

## Dev setup

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
pytest -q
```

## Adding a new decryptor

1. Subclass `pipeline.decryptors.base.BaseDecryptor`.
2. Register it in `pipeline/decryptors/__init__.py`.
3. Add a YAML signature in `config/signatures.yaml` describing how to
   detect the scheme (entropy thresholds, section names, import hints).
4. Add a test that builds a tiny encrypted PE in memory and asserts
   round-trip recovery.

## Style

- Black, 100 cols, Python 3.11+.
- Type hints on public functions.
- No `print()` in library code — use the logger from `utils/log`.

PRs that add real-world sample hashes are welcome; do **not** attach the
samples themselves.