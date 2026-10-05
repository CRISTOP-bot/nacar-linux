# Changelog

## 0.1.0-dev - 2026-10-05

- Establish initial Debian Trixie amd64 / OpenRC live-image build configuration.
- Choose Nácar GNU/Linux as a provisional working name, keep `nacar-linux` as the repository slug, and use `nacar.iso` as the image filename; no trademark clearance or artwork is claimed.
- Add project structure, licensing and provenance policy, contribution guidance, and initial test plan.
- Document the rationale and verification status of every explicitly selected base package.
- Add per-build source/builder metadata and checksums; reproducibility remains unestablished.
- Add an experimental per-boot Live credential hook with mocked success, failure, console, and rollback tests; QEMU verification remains required.
- Brand ISO metadata, BIOS/UEFI menu labels, live hostname, and login identity as Nácar while retaining required Debian-based provenance and notices.
- Add a manual build workflow that creates `nacar.iso`, verifies branding and image contents, and uploads a private 14-day preview artifact; it does not publish a release or prove boot.
- Run the manual build in an ephemeral privileged Debian Trixie Docker container because live-build needs chroot mount access.
- No successful ISO build or boot test is recorded yet; this is not a release.
