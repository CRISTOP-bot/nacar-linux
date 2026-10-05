# OpenRC runtime policy

OpenRC is selected as the intended init and service-management system. The initial Live package list requests Debian's `openrc` package, and `auto/config` passes `init=/usr/sbin/openrc-init` to the kernel. This is not yet a verified boot configuration.

Do not add a service merely because its package is installed. Each enabled service needs a documented reason, least-privilege execution, correct dependency ordering, stop/restart behavior, and tests. Prefer Debian's maintained OpenRC-compatible init scripts. Any service that assumes systemd needs an explicit compatibility investigation; do not silently add a systemd service manager.

Before calling this functional, test PID 1, runlevel transitions, logging, network startup, shutdown/reboot, and package install/remove behavior in QEMU. If Debian package integration requires compatibility adjustments, document the evidence and do not patch upstream code without preserving license and copyright notices.
