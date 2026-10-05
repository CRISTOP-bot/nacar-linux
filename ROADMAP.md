# Roadmap

This roadmap is ordered by dependency and proof, not by visual polish. A milestone is complete only when its exit criteria are demonstrated and the documentation is updated.

## M0 — repository foundation (in progress)

- [x] Separate new work from unrelated existing OS repositories.
- [x] Select Debian Trixie amd64 as the initial technical target; keep brand unselected.
- [x] Record the live-build/OpenRC design, licensing policy, third-party policy, security gates, and fork guidance.
- [x] Add an isolated live-build bootstrap configuration, output checksums, and package inventory generation.
- [x] Add shell syntax and Python structure/policy checks, including basic high-confidence secret patterns.
- [ ] Execute CI and build checks in an environment with Git and Debian Live tools installed.
- [ ] Confirm available Debian package versions and verify `openrc-init` is usable as PID 1 in the chosen live system.

## M1 — first bootable Live image

- [ ] Build on a clean Debian Trixie amd64 host/container with explicitly recorded tool versions.
- [ ] Resolve Live user credentials securely; do not publish the documented default Live password.
- [ ] Boot in QEMU BIOS and UEFI; assert `/proc/1/comm`/executable identifies OpenRC init and `rc-status` works.
- [ ] Verify a shell, kernel, initramfs, storage visibility, DHCP/DNS, and no unintended service startup.
- [ ] Save boot logs, image checksums, package inventory, and test commands as CI artifacts.

## M2 — installer design and minimal installation

- [ ] Specify installation threat model, partitioning and destructive-action confirmations.
- [ ] Separate tested storage/user/bootloader operations from TUI presentation.
- [ ] Start with one architecture and a documented filesystem/boot mode; test in disposable QEMU disks only.
- [ ] Implement dry-run and unit tests before enabling disk writes; never auto-select or erase a disk.

## M3 — reproducibility and security baseline

- [ ] Pin build-container digest and live-build/dependency versions.
- [ ] Use a dated Debian snapshot or equivalent immutable package inputs; verify signatures and source hashes.
- [ ] Build twice in isolated clean environments and compare normalized outputs; explain any unavoidable non-reproducible fields.
- [ ] Add QEMU BIOS/UEFI integration testing, package/systemd-assumption audit, license/provenance checks, and secret scanning.
- [ ] Establish a security-update process and document firmware policy.

## M4 — profiles and optional components

- [ ] Define and measure base, server, developer, and optional desktop profiles.
- [ ] Add a profile only with a package rationale, dependency closure, license record, resource measurements, and tests.
- [ ] Keep graphical components absent from base; evaluate lightweight options as independent packages.

## M5 — distribution identity, packages, and releases

- [ ] Select a distinct name, branding, maintainers, and trademark policy.
- [ ] Introduce custom packages/repository only for real project-owned functionality, with repository signing and key-rotation design.
- [ ] Define `distroctl` scope only after Debian-native tools and OpenRC commands are evaluated.
- [ ] Establish SemVer release process, source archives, changelog, package inventories, checksums, and tested release notes.

## Release blockers

No stable/public ISO release until M1 boot tests, safe Live credentials, installer behavior (if advertised), third-party notices, package inventory, and image checksums are reviewed. Reproducibility must be measured before claiming that builds are reproducible.
