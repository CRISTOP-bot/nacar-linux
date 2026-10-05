# Changelog

## 0.1.0-dev - 2026-10-05

- Establish initial Debian Trixie amd64 / OpenRC live-image build configuration.
- Choose Nácar GNU/Linux as a provisional working name and use `nacar-linux` as the repository slug; no trademark clearance or final visual identity is claimed.
- Add project structure, licensing and provenance policy, contribution guidance, and initial test plan.
- Add root agent guidance, a documentation index, and practical development and verification guides; clarify project status and the non-publication boundary for experimental ISO output.
- Document the rationale and verification status of every explicitly selected base package.
- Add per-build source/builder metadata and checksums; reproducibility remains unestablished.
- Add an experimental per-boot Live credential hook with mocked success, failure, console, and rollback tests; QEMU verification remains required.
- Add a manually dispatched build that creates `nacar.iso` and verifies package inventory and branding; the workflow does not upload or retain the ISO, so public repository access does not expose a build artifact, and runtime boot tests remain separate.
- Build inside a privileged Debian Trixie container on an Ubuntu Actions runner to provide live-build's required mount capabilities.
- Keep the preview experimental and the release gate blocked; a successful build and package inspection do not establish BIOS/UEFI boot or runtime behavior.
