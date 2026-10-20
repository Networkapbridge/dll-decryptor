# Security Policy

dll-decryptor processes untrusted PE files. Treat every input as hostile.

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | ✅        |
| 0.3.x   | ⚠️ critical fixes only |
| < 0.3   | ❌        |

## Reporting a vulnerability

Open a private security advisory on GitHub, or email
`security@dll-decryptor.invalid` with:

- Affected version / commit
- Minimal reproducer (a generated sample is fine — no real malware)
- Impact assessment

We aim to acknowledge within 72h. Please do **not** open a public issue
for memory-safety bugs in the PE parser.

## Known non-issues

- The tool will happily dump any DLL you point it at. That is the point.
- "It decrypted a protected commercial binary" is not a vulnerability.

## Hardening notes

- All PE parsing goes through `pefile` with `fast_load=True` then a
  targeted `parse_data_directories`.
- The loader (`pipeline/ingest/pe_loader.py`) refuses files > 512 MiB.
- Decryptor backends run in-process; do not run samples you don't trust
  outside a VM.