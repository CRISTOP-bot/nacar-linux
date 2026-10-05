# Nácar GNU/Linux

**Nácar GNU/Linux** is the working name for a small distribution based on Debian and built around OpenRC. Its GitHub slug is `nacar-linux`; the requested ISO filename is `nacar.iso`. This repository is an early engineering baseline, **not a released or production-ready operating system**. The name is provisional pending trademark review; no logo or visual identity has been selected.

## Current status

- **Implemented:** repository policy and documentation baseline; an amd64 Debian Trixie `live-build` configuration; a bootstrap script that builds in a fresh temporary directory, refuses to overwrite named output artifacts, and records a binary-package inventory and builder/source metadata with SHA-256 checksums.
- **Experimental, not boot-validated:** per-boot Live credential hook; its mocked tests cover console-only display and password restoration on failures.
- **Not yet verified:** building the ISO, OpenRC as PID 1 via `openrc-init`, credential-hook order, BIOS/UEFI boot, live networking, install flow, clean-room reproducibility, and the resulting image's exact package closure.
- **Not implemented:** installer, graphical desktop, `distroctl`, signed custom repository, release signing, or branded assets. A gated GitHub Actions workflow can build and publish a release only after explicit release approval.

The initial image configuration and per-boot console-password hook are experimental. The hook has mocked success/failure/rollback tests, but has not been validated in a built image. Do not distribute an ISO until its run order, console handoff, persistence behavior, and QEMU boot tests are complete; Debian Live's default password must not silently become a public release default.

## Principles

- Debian packages and upstream projects are preferred over reimplementing mature components.
- OpenRC is the intended init/service-management system; the first image explicitly requests `/usr/sbin/openrc-init`. This must be proven in a booted image, not inferred from build success.
- Minimal packages, disabled recommendations, and a main-only Debian archive are the initial size and licensing baseline. Main-only means some wireless devices may need separately reviewed firmware.
- Code, build configuration, distribution branding, and third-party components are kept separate.
- A feature is called implemented only after an executable test or boot test demonstrates it.

## Repository map

- `auto/`, `config/` — Debian Live build configuration and package selection.
- `build.sh`, `docs/build-system.md` — build entry point and output policy; generated output is ignored.
- `packages/` — profile policy and package selection.
- `system/openrc/` — OpenRC design notes and service policy.
- `installer/`, `src/` — implementation boundaries; no placeholder executable is presented as a feature.
- `configs/branding/`, `assets/branding/` — forkable identity layer; working name recorded, artwork and visual identity still unselected.
- `docs/architecture/`, `docs/licensing/`, `docs/security/` — recorded decisions and release gates.
- `third-party/`, `THIRD_PARTY.md` — third-party provenance and per-build binary inventory policy.
- `tests/`, `.github/` — checks and contribution automation.

## Requirements and build

The supported initial target is **amd64 / Debian Trixie**. The build is intended for a Debian host with `live-build`, `xorriso`, `debootstrap`, `squashfs-tools`, `dosfstools`, `mtools`, GRUB/Syslinux support, `dpkg`, `sha256sum`, and `sudo` installed. Exact host versions are not locked yet, so the result is not yet claimed reproducible.

Run from a clean clone:

```sh
./build.sh
```

The script checks prerequisites, configures a fresh temporary build tree, invokes `live-build`, brands the user-visible boot and session identity as Nácar, and writes `dist/nacar.iso` plus the package inventory, build metadata, and checksums. It refuses to overwrite existing outputs. Build artifacts and caches are excluded from Git. `./build.sh --check` checks local prerequisites without building.

No successful ISO build or boot test is recorded yet. The manual GitHub Actions workflow builds in a temporary privileged Debian Trixie container, checks the user-visible Nácar boot/ISO/session branding plus the package set and credential hook, and uploads a private preview artifact for 14 days; it does not create a release or prove boot. A `v*` tag triggers the separate release workflow, gated by `RELEASE_STATUS=release-ready` and a tag matching `VERSION`; the status remains `blocked`. See `ROADMAP.md`, `docs/build-system.md`, and `docs/architecture/decisions/0001-bootstrap-and-live-builder.md`.

## Development and tests

Run the checks with the Python standard library and Bash:

```sh
bash -n build.sh && sh -n auto/config
python3 -m unittest discover -s tests -v
```

A passing static check does not establish that the ISO boots. QEMU BIOS and UEFI checks are release gates, documented in `docs/architecture/boot-test-plan.md`.

## Contributing and licenses

Read `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md` before opening a contribution. Original project code is offered under GPL-3.0-or-later. Debian and other upstream works retain their own licenses and attribution; see `LICENSE`, `COPYRIGHT`, and `THIRD_PARTY.md`. Do not add copied third-party code before reviewing its exact source, version, copyright, and license and recording it in `THIRD_PARTY.md`.

## Forks and trademarks

Forks are welcome. Follow `FORKING.md`; replace distribution names, artwork, and other marks with an identity you have permission to use. A fork does not inherit permission to use another project's trademarks or imply endorsement.

## Versioning

`VERSION` records the current development version. Releases will follow Semantic Versioning when the project reaches a stable public interface and will include source references, a changelog, package inventory, and checksums. This development snapshot is not a release.
