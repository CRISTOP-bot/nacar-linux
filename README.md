# Debian + OpenRC Foundation

A small, Debian-first foundation for developing an installable GNU/Linux distribution with OpenRC. This repository is an early engineering baseline, **not a released or production-ready operating system**. The distribution's public name, logo, and visual identity have deliberately not been selected yet; the core build is kept independent of branding so a fork can supply its own.

## Current status

- **Implemented:** repository policy and documentation baseline; an amd64 Debian Trixie `live-build` configuration; a bootstrap script that builds in a fresh temporary directory, refuses to overwrite named output artifacts, and records a binary-package inventory and builder/source metadata with SHA-256 checksums.
- **Not yet verified:** building the ISO, OpenRC as PID 1 via `openrc-init`, BIOS/UEFI boot, live networking, install flow, clean-room reproducibility, and the resulting image's exact package closure.
- **Not implemented:** installer, graphical desktop, `distroctl`, signed custom repository, release signing, or branded assets. A gated GitHub Actions workflow can build and publish a release only after explicit release approval.

The initial image configuration is experimental. Do not distribute an ISO until the live-user credential policy and QEMU boot tests are complete; Debian Live's default live-user password must not silently become a public release default.

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
- `configs/branding/`, `assets/branding/` — forkable identity layer, currently intentionally unbranded.
- `docs/architecture/`, `docs/licensing/`, `docs/security/` — recorded decisions and release gates.
- `third-party/`, `THIRD_PARTY.md` — third-party provenance and per-build binary inventory policy.
- `tests/`, `.github/` — checks and contribution automation.

## Requirements and build

The supported initial target is **amd64 / Debian Trixie**. The build is intended for a Debian host with `live-build`, `xorriso`, `debootstrap`, `squashfs-tools`, `dosfstools`, `mtools`, GRUB/Syslinux support, `dpkg`, `sha256sum`, and `sudo` installed. Exact host versions are not locked yet, so the result is not yet claimed reproducible.

Run from a clean clone:

```sh
./build.sh
```

The script checks prerequisites, configures a fresh temporary build tree, invokes Debian `live-build`, and writes the ISO, TSV package inventory, builder/source metadata, and checksums under `dist/`. It refuses to overwrite matching outputs. Build artifacts and caches are excluded from Git. `./build.sh --check` checks local prerequisites without building.

The current environment used to prepare this baseline had no Git, `live-build`, `xorriso`, `debootstrap`, or QEMU. Consequently, no ISO has been built or boot-tested here. GitHub Actions runs shell and policy checks; a `v*` tag triggers a release build, and only a successful build can create a GitHub Release. That workflow remains gated on `RELEASE_STATUS=release-ready` and a tag matching `VERSION`; the status currently remains `blocked`. See `ROADMAP.md` for the next gates and `docs/architecture/decisions/0001-bootstrap-and-live-builder.md` for the design rationale.

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
