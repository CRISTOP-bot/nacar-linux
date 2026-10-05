# Changelog

## 0.1.0-dev - 2026-10-05

- Establish initial Debian Trixie amd64 / OpenRC live-image build configuration.
- Choose Nácar GNU/Linux as a provisional working name and use the `nacar-linux` artifact prefix; no trademark clearance or visual identity is claimed.
- Add project structure, licensing and provenance policy, contribution guidance, and initial test plan.
- Document the rationale and verification status of every explicitly selected base package.
- Add per-build source/builder metadata and checksums; reproducibility remains unestablished.
- Add an experimental per-boot Live credential hook with mocked success, failure, console, and rollback tests; QEMU verification remains required.
- No ISO built or boot-tested in this environment; this is not a release.
