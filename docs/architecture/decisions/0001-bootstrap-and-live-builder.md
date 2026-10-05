# ADR 0001: Debian Live as the first image bootstrap

- **Status:** accepted for the experimental first image; implementation not boot-verified.
- **Date:** 2026-10-05.

## Context

The project needs a real Debian-based live image early, without maintaining a bespoke package manager, kernel, initramfs, or ISO compositor. The working tree is a shared workspace containing unrelated operating-system projects, and none of those repositories was designated as the target for this effort.

Debian publishes `live-build` for Trixie, and Debian's Live manual documents the `iso-hybrid` image type. Debian publishes OpenRC in Trixie; its package includes `/usr/sbin/openrc-init`. The package's exact installed runtime and PID 1 behavior in this image still require a real boot test.

## Decision

Create a new, isolated repository directory named `openrc-debian-foundation`. Use Debian Trixie amd64 and official Debian Live `live-build` configuration for an initial minimal hybrid ISO. Start with the `main` archive, disable APT recommendations, request a minbase bootstrap, select only explicit base/live/kernel/network packages, and request `init=/usr/sbin/openrc-init` on the kernel command line.

Do not add an installer, desktop, repository, custom kernel, package-manager replacement, or branded artwork before the minimum Live image is booted and tested. Keep distribution identity unselected and isolate future branding from the core.

## Consequences

- Debian remains the package source of truth; package versions may drift because APT inputs are not pinned to an immutable snapshot yet.
- The build script records the final binary package/version/source inventory and checksums, but that alone does not prove source reproducibility or complete licensing compliance.
- Network-dependent ISO construction requires a Debian-compatible host, root privileges for the live-build stage, and substantial free disk space.
- `init=/usr/sbin/openrc-init` is a configuration request, not evidence that OpenRC boots correctly. PID 1, runlevel behavior, shutdown, live-config integration, and systemd absence must be checked in QEMU.
- BIOS/UEFI support and the Live credential configuration remain release gates until verified.

## Alternatives considered

- **Hand-built root filesystem/ISO:** rejected for M0 because it duplicates mature Debian boot/image plumbing and increases maintenance burden.
- **Alpine/Gentoo/custom package tools:** rejected because Debian-first is a core project constraint.
- **Copy an existing distribution's build scripts or artwork:** rejected because no such source was reviewed for provenance/licensing, and it would undermine the project's attribution/fork policy.
- **Build inside a pre-existing OS project directory:** rejected to avoid mixing unrelated work and violating repository-boundary expectations.

## References

- Debian Trixie OpenRC package metadata and file list: `https://packages.debian.org/trixie/openrc`, `https://packages.debian.org/trixie/amd64/openrc/filelist`.
- Debian Trixie `live-build` package: `https://packages.debian.org/trixie/live-build`.
- Debian Live manual: `https://live-team.pages.debian.net/live-manual/html/live-manual.en.html`.
