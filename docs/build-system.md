# Build system and generated outputs

The initial image uses Debian's `live-build`; the project does not maintain its own package manager, initramfs generator, kernel, or ISO compositor. `auto/config` selects Debian Trixie amd64, a hybrid ISO, the official Debian mirror, a minimal bootstrap, and OpenRC's `openrc-init` boot argument. Explicit base packages are in `config/package-lists/base.list.chroot`.

## Local command

From the repository root, run `./build.sh`. It checks required host tools, creates a new temporary work directory, copies the build configuration into it, and invokes `live-build`. The root-only build step is run through `sudo` when needed. It then collects the binary package/version/source inventory, writes builder/source metadata, copies these files and the ISO into `dist/`, and writes SHA-256 checksums covering the ISO, inventory, and metadata. It refuses to overwrite artifacts with the same version. The metadata improves traceability but is not a reproducibility proof.

The work directory is created by `mktemp` for that invocation only and removed at exit. Build caches and ISO outputs must not be committed. The repository's `.gitignore` excludes `/build/`, `/dist/`, live-build trees, images, logs, inventories, and checksums. Keep project documentation under `docs/`, not under generated-output paths.

## Reproducibility and validation status

Debian package inputs and the host `live-build` version are not yet pinned to immutable snapshots. Consequently, the build has **not** been demonstrated reproducible. A successful `lb build` would still not prove OpenRC PID 1, Live credentials, BIOS/UEFI boot, networking, installation, or license compliance. Follow `ROADMAP.md` and `docs/architecture/boot-test-plan.md`; do not publish an ISO until the release gates pass.

`RELEASE_STATUS` is currently `blocked`. The manually dispatched `.github/workflows/verify-live-build.yml` builds the experimental ISO and checks its package inventory, embedded hook, and that the live-config user-setup component precedes the custom-hook runner. Its ephemeral Debian container receives only `SYS_ADMIN` to perform live-build's required mounts; an explicit probe fails early if the runner does not honor that capability. The workflow does not upload or publish the image, and the ordering check is not a runtime test. The separate tag-triggered release workflow checks the release gate and tag/`VERSION` match. Neither workflow currently performs the required QEMU BIOS/UEFI boot tests, so the gate must remain blocked until those tests and the other documented release criteria are complete.
