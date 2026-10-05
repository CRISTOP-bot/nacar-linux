# Build system and generated outputs

The initial image uses Debian's `live-build`; the project does not maintain its own package manager, initramfs generator, kernel, or ISO compositor. `auto/config` selects Debian Trixie amd64, a hybrid ISO, the official Debian mirror, a minimal bootstrap, and OpenRC's `openrc-init` boot argument. Explicit base packages are in `config/package-lists/base.list.chroot`.

## Nácar branding and upstream attribution

The user-visible surfaces are branded `Nácar GNU/Linux`: the ISO filename is `nacar.iso`, ISO9660 application/publisher/preparer/volume fields are set to Nácar values, active BIOS/UEFI boot-menu labels are rewritten to `Nacar`, the live hostname is `nacar`, and `/etc/issue` plus `PRETTY_NAME` in `/etc/os-release` use Nácar. `/etc/os-release` sets `ID=nacar` and retains `ID_LIKE=debian` to communicate technical compatibility. Debian package names, repository URLs, package copyright files, required notices, and build provenance remain intact; this is a Debian-based distribution, not an official Debian image. We do not erase legally required attribution or upstream license information.

## Local command

From the repository root, run `./build.sh`. It checks required host tools, creates a fresh temporary work directory, copies the build configuration and the installed `live-build` bootloader templates into it, and rewrites only visible boot-menu directives to Nácar while preserving upstream comment/notice lines. It generates Nácar `/etc/os-release` and login issue files, then invokes `live-build`; the root-only build step is run through `sudo` when needed. It writes `dist/nacar.iso`, `nacar.packages.tsv`, `nacar.build-info.txt`, and `nacar.sha256`. Existing outputs are never overwritten. Build metadata records Debian as the base distribution for provenance; this is not a reproducibility proof.

The work directory is created by `mktemp` for that invocation only and removed at exit. Build caches and ISO outputs must not be committed. The repository's `.gitignore` excludes `/build/`, `/dist/`, live-build trees, images, logs, inventories, and checksums. Keep project documentation under `docs/`, not under generated-output paths.

## Reproducibility and validation status

Debian package inputs and the host `live-build` version are not yet pinned to immutable snapshots. Consequently, the build has **not** been demonstrated reproducible. A successful `lb build` would still not prove OpenRC PID 1, Live credentials, BIOS/UEFI boot, networking, installation, or license compliance. Follow `ROADMAP.md` and `docs/architecture/boot-test-plan.md`; do not publish an ISO until the release gates pass.

`RELEASE_STATUS` is currently `blocked`. The manually dispatched `.github/workflows/verify-live-build.yml` builds `nacar.iso` inside a temporary privileged Debian Trixie Docker container, verifies the ISO metadata, boot-menu and Live-session branding, package inventory, embedded credential hook, and live-config component order, then uploads the ISO and sidecars as a private workflow artifact for 14 days. It does not create a GitHub Release or prove the image boots. The container needs mount capabilities for `live-build`; this isolated manual workflow uses the hosted runner's Docker engine. The separate tag-triggered release workflow remains gated by `RELEASE_STATUS=release-ready` and the tag/`VERSION` match. The release gate stays blocked until QEMU BIOS/UEFI boot tests and all other documented criteria pass.
