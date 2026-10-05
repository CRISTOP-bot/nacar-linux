# Base-image package rationale

This table covers only packages explicitly requested by `config/package-lists/base.list.chroot`. Debian's transitive dependencies and Essential packages are not enumerated here; preserve the generated per-build inventory and inspect the actual closure before any release.

| Package | Why it is explicitly selected | Current status / verification |
| --- | --- | --- |
| `linux-image-amd64` | Debian's amd64 kernel metapackage; a kernel is required to boot the target system. | Selected for the amd64 image; confirm installed kernel, initramfs, and firmware behavior in QEMU. |
| `live-boot` | Supplies Debian Live boot support in the initramfs and locates/mounts the compressed Live filesystem. | Required by the Live design; boot not yet tested. |
| `live-config` | Configures the Live session during late userspace, including the transient Live account and related runtime settings. | Required by the chosen Debian Live approach; credential policy remains a release blocker. |
| `live-config-sysvinit` | Debian's live-config backend for a SysV-init-style service integration. OpenRC can work with SysV-style init scripts, but compatibility with `openrc-init` is not yet demonstrated. | Explicit compatibility experiment; must be proven at boot or replaced with a backend that actually supports the chosen OpenRC configuration. It is not evidence that SysV init is intended as PID 1. |
| `openrc` | Debian's OpenRC package provides OpenRC service/runlevel management and includes `openrc-init`; OpenRC is the intended PID 1 and service manager. | Requested through `init=/usr/sbin/openrc-init`; no boot proof yet. |
| `passwd` | Supplies `chpasswd` for setting the transient Live account password and restoring its prior hash if the console handoff fails. | Required by the experimental per-boot credential hook; command behavior and hook order still need QEMU validation. |
| `coreutils` | Makes the hook's `dd`, `base32`, and `tr` dependencies explicit rather than relying only on Debian Essential-package closure. | Selected for credential generation; measure the actual closure and verify tool versions in the image. |
| `bash` | Provides the familiar interactive shell requested for the minimum diagnostic Live environment. | Verify a usable console login and shell in QEMU. |
| `ca-certificates` | Provides trusted CA certificates for TLS clients used by the base system, including secure access to configured HTTPS repositories. | Kept for authenticated HTTPS; not a substitute for APT's signed repository metadata. |
| `ifupdown` | Provides Debian's traditional interface configuration used by the initial wired-network path. | Validate that its service/script integration starts under OpenRC; avoid installing a second network manager by default. |
| `iproute2` | Provides core interface, address, and route inspection/configuration tools. | Required for basic networking and diagnostics. |
| `iputils-ping` | Provides `ping` for a small, direct network connectivity diagnostic. | Diagnostic package; can be removed if the measured minimal profile excludes it. |
| `isc-dhcp-client` | Provides a DHCP client for acquiring wired-network configuration through the selected `ifupdown` path. | Verify DHCP and DNS in QEMU; do not assume wireless firmware is included. |
| `procps` | Provides standard process and memory diagnostics such as `ps` and `free`. | Minimal diagnostic utility set. |
| `util-linux` | Supplies core system/console and storage utilities commonly needed for inspection and recovery. | Review the exact dependency/installed closure; keep only if the minimal Live use cases need the explicit metapackage. |

## Dependency review rules

- Do not add a package without adding its purpose here and updating the generated package inventory expectations/tests.
- Review `Depends`, `Pre-Depends`, and selected `Recommends` (recommendations are disabled in the current build) from the built image's package database; do not mistake the explicit list for the complete image.
- Examine OpenRC service scripts and package maintainer scripts for systemd-only assumptions, unexpected autostart, privilege use, and network-manager overlap.
- Inspect each installed package's `/usr/share/doc/<package>/copyright`; keep upstream notices and required source/redistribution obligations intact.
- Measure image size and runtime services after boot before deciding that a package is justified or removable.
