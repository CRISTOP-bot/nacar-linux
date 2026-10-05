# Build system and generated outputs

The initial image uses Debian's `live-build`; the project does not maintain its own package manager, initramfs generator, kernel, or ISO compositor. `auto/config` selects Debian Trixie amd64, a hybrid ISO, the official Debian mirror, a minimal bootstrap, and OpenRC's `openrc-init` boot argument. Explicit base packages are in `config/package-lists/base.list.chroot`.

## Local command

From the repository root, run `./build.sh`. It checks required host tools, creates a new temporary work directory, copies the build configuration and the installed upstream live-build bootloader templates into it, and invokes `live-build`. A branding helper changes visible menu labels in that temporary copy while preserving comments, copyright notices, and technical settings. The root-only build step is run through `sudo` when needed. It then collects the binary package/version/source inventory, writes builder/source metadata, and stages `nacar.iso`, `nacar.packages.tsv`, `nacar.build-info.txt`, and `nacar.sha256` under `dist/`. The metadata improves traceability but is not a reproducibility proof.

The work directory is created by `mktemp` for that invocation only and removed at exit. Build caches and ISO outputs must not be committed. The repository's `.gitignore` excludes `/build/`, `/dist/`, live-build trees, images, logs, inventories, and checksums. Keep project documentation under `docs/`, not under generated-output paths.

## Reproducibility and validation status

Debian package inputs and the host `live-build` version are not yet pinned to immutable snapshots. Consequently, the build has **not** been demonstrated reproducible. A successful `lb build` would still not prove OpenRC PID 1, Live credentials, BIOS/UEFI boot, networking, installation, or license compliance. Follow `ROADMAP.md` and `docs/architecture/boot-test-plan.md`; do not publish an ISO until the release gates pass.

`RELEASE_STATUS` is currently `blocked`. The manually dispatched `.github/workflows/verify-live-build.yml` runs the build in a privileged Debian Trixie Docker container on an Ubuntu runner and verifies the image metadata, boot-menu labels, package inventory, embedded hook, and live-config ordering. The workflow deliberately does not upload or retain the ISO or sidecars, so the output will not become public with repository visibility; the runner discards it at job end. The ordering check is not a runtime test. Debian technical provenance is intentionally retained, including `/etc/debian_version`, Debian package copyright notices and repository URLs, and `ID_LIKE=debian`. The separate tag-triggered release workflow checks the release gate and tag/`VERSION` match. Neither workflow performs the required QEMU BIOS/UEFI boot tests, so the gate must remain blocked until those tests and the other documented release criteria are complete.
